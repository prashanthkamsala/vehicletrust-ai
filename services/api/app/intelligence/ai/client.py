import httpx

from app.intelligence.ai.contracts import AIRequest
from app.schemas.vehicle.models import (
    AIGrounding,
    AIInterpretation,
    AIKnowledgeReference,
)


class AIServiceClient:
    """HTTP client for the VehicleTrust AI service."""

    def __init__(
        self,
        *,
        base_url: str = "http://127.0.0.1:8001",
        timeout: float = 30.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def interpret(self, request: AIRequest) -> AIInterpretation:
        """Request an AI interpretation from the AI service."""
        response = httpx.post(
            f"{self.base_url}/api/v1/ai/interpret",
            json=request.model_dump(mode="json"),
            timeout=self.timeout,
        )
        response.raise_for_status()

        data = response.json()

        return AIInterpretation(
            summary=data["summary"],
            reasoning=data["reasoning"],
            recommendation=data["recommendation"],
            supporting_evidence_ids=data["supporting_evidence_ids"],
            knowledge_references=[
                AIKnowledgeReference(
                    id=reference["id"],
                    title=reference["title"],
                    category=reference["category"],
                    relevance=reference["relevance"],
                )
                for reference in data["knowledge_references"]
            ],
            grounding=AIGrounding(
                status=data["grounding"]["status"],
                evidence_count=data["grounding"]["evidence_count"],
                knowledge_count=data["grounding"]["knowledge_count"],
            ),
        )