"""Markdown chunker for document processing."""

import re
from typing import Optional
from uuid import uuid4

import structlog

logger = structlog.get_logger()


class Chunk:
    """Represents a document chunk."""

    def __init__(
        self,
        id: str,
        content: str,
        module: str,
        section: Optional[str] = None,
        heading: Optional[str] = None,
        page: Optional[int] = None,
        start_char: int = 0,
        end_char: int = 0,
    ):
        self.id = id
        self.content = content
        self.module = module
        self.section = section
        self.heading = heading
        self.page = page
        self.start_char = start_char
        self.end_char = end_char

    def to_dict(self) -> dict:
        """Convert to dictionary for indexing."""
        return {
            "id": self.id,
            "content": self.content,
            "module": self.module,
            "section": self.section,
            "heading": self.heading,
            "page": self.page,
            "start_char": self.start_char,
            "end_char": self.end_char,
        }


class MarkdownChunker:
    """Chunks markdown documents for vector indexing."""

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        min_chunk_size: int = 100,
    ):
        """
        Initialize chunker.

        Args:
            chunk_size: Target size for each chunk in characters
            chunk_overlap: Overlap between consecutive chunks
            min_chunk_size: Minimum chunk size (smaller chunks are merged)
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_size = min_chunk_size

    def chunk_markdown(
        self,
        content: str,
        module: str,
        section: Optional[str] = None,
    ) -> list[Chunk]:
        """
        Chunk markdown content.

        Uses heading-aware chunking that tries to keep
        related content together.

        Args:
            content: Markdown content to chunk
            module: Module identifier
            section: Optional section identifier

        Returns:
            List of Chunk objects
        """
        chunks = []

        # Split by headings
        sections = self._split_by_headings(content)

        current_heading = None
        char_offset = 0

        for section_content, heading in sections:
            if heading:
                current_heading = heading

            # Chunk the section content
            section_chunks = self._chunk_text(
                section_content,
                char_offset,
            )

            for text, start, end in section_chunks:
                chunk = Chunk(
                    id=str(uuid4()),
                    content=text.strip(),
                    module=module,
                    section=section,
                    heading=current_heading,
                    start_char=start,
                    end_char=end,
                )

                if len(chunk.content) >= self.min_chunk_size:
                    chunks.append(chunk)

            char_offset += len(section_content)

        logger.info(
            "Content chunked",
            module=module,
            total_chunks=len(chunks),
            content_length=len(content),
        )

        return chunks

    def _split_by_headings(self, content: str) -> list[tuple[str, Optional[str]]]:
        """
        Split content by markdown headings.

        Returns list of (content, heading) tuples.
        """
        # Pattern for markdown headings
        heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)

        sections = []
        last_end = 0
        current_heading = None

        for match in heading_pattern.finditer(content):
            # Add content before this heading
            if match.start() > last_end:
                section_content = content[last_end:match.start()]
                if section_content.strip():
                    sections.append((section_content, current_heading))

            current_heading = match.group(2).strip()
            last_end = match.end()

        # Add remaining content
        if last_end < len(content):
            remaining = content[last_end:]
            if remaining.strip():
                sections.append((remaining, current_heading))

        return sections if sections else [(content, None)]

    def _chunk_text(
        self,
        text: str,
        offset: int = 0,
    ) -> list[tuple[str, int, int]]:
        """
        Chunk text into smaller pieces with overlap.

        Returns list of (text, start_char, end_char) tuples.
        """
        if len(text) <= self.chunk_size:
            return [(text, offset, offset + len(text))]

        chunks = []
        start = 0

        while start < len(text):
            end = start + self.chunk_size

            # Try to break at a sentence or paragraph boundary
            if end < len(text):
                # Look for sentence end
                for sep in ['. ', '.\n', '\n\n', '\n', ' ']:
                    break_point = text.rfind(sep, start + self.min_chunk_size, end)
                    if break_point != -1:
                        end = break_point + len(sep)
                        break

            chunk_text = text[start:end]
            chunks.append((chunk_text, offset + start, offset + end))

            # Move start with overlap
            start = end - self.chunk_overlap
            if start < 0:
                start = end

        return chunks

    def chunk_with_context(
        self,
        content: str,
        module: str,
        context_window: int = 2,
    ) -> list[Chunk]:
        """
        Chunk with surrounding context included.

        Each chunk includes context from surrounding chunks
        for better semantic understanding.

        Args:
            content: Content to chunk
            module: Module identifier
            context_window: Number of chunks before/after to include

        Returns:
            List of chunks with context
        """
        base_chunks = self.chunk_markdown(content, module)

        enhanced_chunks = []

        for i, chunk in enumerate(base_chunks):
            # Gather context from surrounding chunks
            context_parts = []

            # Previous context
            for j in range(max(0, i - context_window), i):
                context_parts.append(f"[Previous] {base_chunks[j].content[:200]}...")

            # Current chunk
            context_parts.append(chunk.content)

            # Following context
            for j in range(i + 1, min(len(base_chunks), i + context_window + 1)):
                context_parts.append(f"[Following] {base_chunks[j].content[:200]}...")

            enhanced_content = "\n\n".join(context_parts)

            enhanced_chunk = Chunk(
                id=chunk.id,
                content=enhanced_content,
                module=chunk.module,
                section=chunk.section,
                heading=chunk.heading,
                page=chunk.page,
                start_char=chunk.start_char,
                end_char=chunk.end_char,
            )
            enhanced_chunks.append(enhanced_chunk)

        return enhanced_chunks
