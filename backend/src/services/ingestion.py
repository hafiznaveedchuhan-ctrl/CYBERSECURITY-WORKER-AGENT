"""Document ingestion service for RAG pipeline."""

import hashlib
from pathlib import Path
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import structlog

from src.models import Document, DocumentChunk
from src.services.embedding import EmbeddingService
from src.services.qdrant import get_qdrant_service

logger = structlog.get_logger()


class IngestionService:
    """Service for ingesting and chunking documents."""

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embedding_service = EmbeddingService()
        self.qdrant = get_qdrant_service()

    def _compute_checksum(self, content: str) -> str:
        """Compute SHA256 checksum of content."""
        return hashlib.sha256(content.encode()).hexdigest()

    def _chunk_text(self, text: str) -> list[dict]:
        """Split text into overlapping chunks."""
        chunks = []
        start = 0
        chunk_index = 0

        while start < len(text):
            end = start + self.chunk_size

            # Try to break at a sentence or paragraph boundary
            if end < len(text):
                # Look for paragraph break
                para_break = text.rfind("\n\n", start, end)
                if para_break > start + self.chunk_size // 2:
                    end = para_break + 2
                else:
                    # Look for sentence break
                    for sep in [". ", "! ", "? ", "\n"]:
                        sent_break = text.rfind(sep, start, end)
                        if sent_break > start + self.chunk_size // 2:
                            end = sent_break + len(sep)
                            break

            chunk_content = text[start:end].strip()
            if chunk_content:
                chunks.append({
                    "content": chunk_content,
                    "start_char": start,
                    "end_char": end,
                    "chunk_index": chunk_index,
                })
                chunk_index += 1

            # Move start with overlap
            start = end - self.chunk_overlap
            if start >= len(text):
                break

        return chunks

    async def ingest_file(
        self,
        file_path: Path,
        category: Optional[str],
        db: AsyncSession,
    ) -> Document:
        """Ingest a single file into the database and vector store."""
        content = file_path.read_text(encoding="utf-8")
        checksum = self._compute_checksum(content)

        # Check if document already exists
        result = await db.execute(
            select(Document).where(Document.source_path == str(file_path))
        )
        existing = result.scalar_one_or_none()

        if existing:
            if existing.checksum == checksum:
                logger.debug("Document unchanged, skipping", path=str(file_path))
                return existing
            else:
                # Delete old chunks from Qdrant
                await self.qdrant.delete_by_document("textbook_chunks", existing.id)
                # Update document
                existing.checksum = checksum
                document = existing
        else:
            # Create new document
            document = Document(
                title=file_path.stem.replace("-", " ").replace("_", " ").title(),
                source_path=str(file_path),
                content_type=file_path.suffix.lstrip("."),
                category=category,
                checksum=checksum,
            )
            db.add(document)
            await db.flush()

        # Chunk the content
        chunks = self._chunk_text(content)

        # Generate embeddings
        chunk_contents = [c["content"] for c in chunks]
        embeddings = await self.embedding_service.embed_texts(chunk_contents)

        # Store chunks in database and Qdrant
        chunk_ids = []
        payloads = []

        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            vector_id = f"{document.id}_{i}"
            chunk_ids.append(vector_id)

            # Database chunk
            db_chunk = DocumentChunk(
                document_id=document.id,
                chunk_index=chunk["chunk_index"],
                content=chunk["content"],
                start_char=chunk["start_char"],
                end_char=chunk["end_char"],
                vector_id=vector_id,
                metadata_={
                    "title": document.title,
                    "category": category,
                },
            )
            db.add(db_chunk)

            # Qdrant payload
            payloads.append({
                "document_id": document.id,
                "title": document.title,
                "category": category or "general",
                "chunk_index": chunk["chunk_index"],
                "content": chunk["content"][:500],  # Store preview
                "source_path": str(file_path),
            })

        # Upsert to Qdrant
        await self.qdrant.upsert_chunks(
            collection_name="textbook_chunks",
            ids=chunk_ids,
            vectors=embeddings,
            payloads=payloads,
        )

        await db.commit()
        await db.refresh(document)

        logger.info(
            "Ingested document",
            path=str(file_path),
            chunks=len(chunks),
            document_id=document.id,
        )

        return document

    async def ingest_directory(
        self,
        directory: Path,
        category: Optional[str],
        db: AsyncSession,
        patterns: list[str] = ["*.md", "*.mdx"],
    ) -> list[Document]:
        """Ingest all matching files from a directory."""
        documents = []

        for pattern in patterns:
            for file_path in directory.rglob(pattern):
                if file_path.is_file():
                    doc = await self.ingest_file(file_path, category, db)
                    documents.append(doc)

        logger.info(
            "Ingested directory",
            directory=str(directory),
            documents=len(documents),
        )

        return documents
