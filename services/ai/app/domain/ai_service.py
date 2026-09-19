from app.domain.grounding import validate_ai_response
from app.generation.base import AIGenerator
from app.retrieval.base import KnowledgeResult
from app.retrieval.knowledge_retriever import KnowledgeRetriever
from app.schemas.contracts import AIRequest, AIResponse


class AIService:
    """Orchestrate retrieval, generation, and grounding validation."""

    def __init__(
        self,
        retriever: KnowledgeRetriever,
        generator: AIGenerator,
    ) -> None:
        self.retriever = retriever
        self.generator = generator

    def interpret(self, request: AIRequest) -> AIResponse:
        """Generate a grounded interpretation for an AI request."""

        knowledge = self.retriever.retrieve(request)

        response = self.generator.generate(
            request,
            knowledge,
        )

        validate_ai_response(
            response,
            evidence_ids={
                evidence.id
                for evidence in request.evidence
            },
            knowledge_results=knowledge,
        )

        return response