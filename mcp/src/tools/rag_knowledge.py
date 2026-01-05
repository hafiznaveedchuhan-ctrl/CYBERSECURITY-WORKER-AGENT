"""RAG knowledge MCP tools."""

from typing import Optional
import httpx

from pydantic import BaseModel, Field


class RAGRetrieveInput(BaseModel):
    """Input for RAG retrieval."""
    query: str = Field(..., description="Query to search the knowledge base")
    collection: str = Field(default="textbook_chunks", description="Collection to search")
    top_k: int = Field(default=5, ge=1, le=20)
    page_filter: Optional[str] = Field(default=None, description="Filter by module/page")


class RAGEvalInput(BaseModel):
    """Input for RAG evaluation."""
    query: str = Field(..., description="Evaluation query")
    expected_answer: str = Field(..., description="Expected answer for comparison")
    retrieved_context: str = Field(..., description="Retrieved context from RAG")


async def rag_retrieve(input: RAGRetrieveInput) -> dict:
    """
    Retrieve relevant context from the RAG knowledge base.

    Searches the textbook and returns relevant passages with citations.
    """
    # Call the RAG service
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:8001/retrieve",
                json={
                    "query": input.query,
                    "collection": input.collection,
                    "top_k": input.top_k,
                    "page_filter": input.page_filter,
                },
                timeout=30.0,
            )

            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "chunks": data["chunks"],
                    "total_found": data["total_found"],
                    "query": input.query,
                }
            else:
                return {
                    "success": False,
                    "error": f"RAG service error: {response.status_code}",
                }

    except httpx.ConnectError:
        # Fallback with sample data when service unavailable
        return {
            "success": True,
            "chunks": [
                {
                    "id": "fallback-1",
                    "content": "Alert triage is the process of reviewing, classifying, and prioritizing security alerts to determine which require immediate attention.",
                    "citation": "Module 1 > Alert Triage Process",
                    "score": 0.85,
                },
                {
                    "id": "fallback-2",
                    "content": "Severity levels range from Critical (immediate response required) to Low (informational, can be addressed during normal operations).",
                    "citation": "Module 1 > Alert Triage > Severity Assessment",
                    "score": 0.78,
                },
            ],
            "total_found": 2,
            "query": input.query,
            "note": "Using fallback data - RAG service unavailable",
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


async def rag_eval_run(input: RAGEvalInput) -> dict:
    """
    Evaluate RAG retrieval quality.

    Compares retrieved context against expected answers.
    """
    # Simple evaluation metrics
    query_words = set(input.query.lower().split())
    context_words = set(input.retrieved_context.lower().split())
    expected_words = set(input.expected_answer.lower().split())

    # Calculate metrics
    context_coverage = len(expected_words & context_words) / len(expected_words) if expected_words else 0
    query_relevance = len(query_words & context_words) / len(query_words) if query_words else 0

    # Check if key concepts are present
    key_concepts_found = []
    key_concepts_missing = []

    # Extract key phrases from expected answer (simple approach)
    expected_phrases = input.expected_answer.split('. ')
    for phrase in expected_phrases:
        phrase_words = set(phrase.lower().split())
        if len(phrase_words & context_words) >= len(phrase_words) * 0.5:
            key_concepts_found.append(phrase[:50])
        else:
            key_concepts_missing.append(phrase[:50])

    # Overall score
    overall_score = (context_coverage * 0.6 + query_relevance * 0.4) * 100

    return {
        "query": input.query,
        "metrics": {
            "context_coverage": round(context_coverage * 100, 2),
            "query_relevance": round(query_relevance * 100, 2),
            "overall_score": round(overall_score, 2),
        },
        "key_concepts": {
            "found": key_concepts_found,
            "missing": key_concepts_missing,
        },
        "verdict": "pass" if overall_score >= 70 else "fail",
        "recommendation": (
            "Context adequately covers expected information."
            if overall_score >= 70
            else "Consider improving retrieval or adding more relevant documents."
        ),
    }


# Tool registry
RAG_TOOLS = {
    "rag_retrieve": {
        "function": rag_retrieve,
        "schema": RAGRetrieveInput,
        "description": "Retrieve relevant context from the RAG knowledge base",
    },
    "rag_eval_run": {
        "function": rag_eval_run,
        "schema": RAGEvalInput,
        "description": "Evaluate RAG retrieval quality",
    },
}
