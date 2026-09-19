from abc import ABC, abstractmethod

from pydantic import BaseModel, Field


class KnowledgeDocument(BaseModel):
    id: str
    title: str
    category: str
    content: str
    keywords: list[str] = Field(default_factory=list)


class KnowledgeResult(BaseModel):
    document: KnowledgeDocument
    relevance: str


class Retriever(ABC):
    """Contract for retrieving domain knowledge."""

    @abstractmethod
    def search(
        self,
        query: str,
        *,
        limit: int = 5,
    ) -> list[KnowledgeResult]:
        """Return knowledge relevant to the supplied query."""
        raise NotImplementedError