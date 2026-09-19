from abc import ABC, abstractmethod

from app.retrieval.base import KnowledgeResult
from app.schemas.contracts import AIRequest, AIResponse


class AIGenerator(ABC):
    """Contract for generating grounded AI interpretations."""

    @abstractmethod
    def generate(
        self,
        request: AIRequest,
        knowledge: list[KnowledgeResult],
    ) -> AIResponse:
        """Generate an AI response from deterministic intelligence and knowledge."""
        raise NotImplementedError