from pathlib import Path

from app.domain.ai_service import AIService
from app.generation.deterministic import DeterministicGenerator
from app.generation.llm import LLMGenerator
from app.generation.providers.ollama import OllamaClient
from app.retrieval.knowledge_retriever import KnowledgeRetriever
from app.retrieval.local import LocalKeywordRetriever
from app.retrieval.semantic import SemanticRetriever

def _build_knowledge_retriever() -> KnowledgeRetriever:
    """Build the local vehicle knowledge retrieval stack."""

    knowledge_dir = (
        Path(__file__).resolve().parents[2]
        / "knowledge"
        / "vehicle"
    )

    local_retriever = LocalKeywordRetriever(knowledge_dir)
    retriever = SemanticRetriever(local_retriever.documents)

    return KnowledgeRetriever(
        retriever,
    )


def build_local_ai_service() -> AIService:
    """Build the default deterministic local AI service."""

    knowledge_retriever = _build_knowledge_retriever()
    generator = DeterministicGenerator()

    return AIService(
        retriever=knowledge_retriever,
        generator=generator,
    )


def build_ollama_ai_service(
    *,
    base_url: str = "http://127.0.0.1:11434",
    model: str = "qwen3:8b",
    timeout: float = 120.0,
    think: bool = False,
) -> AIService:
    """Build a local AI service backed by Ollama."""

    knowledge_retriever = _build_knowledge_retriever()

    client = OllamaClient(
        base_url=base_url,
        model=model,
        timeout=timeout,
        think=think,
    )

    generator = LLMGenerator(
        client,
    )

    return AIService(
        retriever=knowledge_retriever,
        generator=generator,
    )