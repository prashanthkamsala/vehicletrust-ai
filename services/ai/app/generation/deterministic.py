from app.generation.base import AIGenerator
from app.retrieval.base import KnowledgeResult
from app.schemas.contracts import (
    AIGrounding,
    AIKnowledgeReference,
    AIRequest,
    AIResponse,
)


class DeterministicGenerator(AIGenerator):
    """Generate a grounded vehicle interpretation without an LLM."""

    def generate(
        self,
        request: AIRequest,
        knowledge: list[KnowledgeResult],
    ) -> AIResponse:
        supporting_evidence_ids = self._select_supporting_evidence(request)
        knowledge_references = self._build_knowledge_references(knowledge)

        summary = self._build_summary(request)
        reasoning = self._build_reasoning(request)
        recommendation = self._build_recommendation(request)

        grounding_status = self._determine_grounding_status(
            evidence_count=len(supporting_evidence_ids),
            knowledge_count=len(knowledge_references),
        )

        return AIResponse(
            summary=summary,
            reasoning=reasoning,
            recommendation=recommendation,
            supporting_evidence_ids=supporting_evidence_ids,
            knowledge_references=knowledge_references,
            grounding=AIGrounding(
                status=grounding_status,
                evidence_count=len(supporting_evidence_ids),
                knowledge_count=len(knowledge_references),
            ),
        )

    @staticmethod
    def _select_supporting_evidence(
        request: AIRequest,
    ) -> list[str]:
        """Select evidence directly connected to identified risks."""

        priority_risk_ids = set(request.decision.priority_risk_ids)

        selected: list[str] = []

        for risk in request.risks:
            if (
                risk.id in priority_risk_ids
                or not priority_risk_ids
            ):
                for evidence_id in risk.evidence_ids:
                    if evidence_id not in selected:
                        selected.append(evidence_id)

        if selected:
            return selected

        return [
            evidence.id
            for evidence in request.evidence
            if evidence.status in {
                "conflicting",
                "partially_verified",
            }
        ]

    @staticmethod
    def _build_knowledge_references(
        knowledge: list[KnowledgeResult],
    ) -> list[AIKnowledgeReference]:
        return [
            AIKnowledgeReference(
                id=result.document.id,
                title=result.document.title,
                category=result.document.category,
                relevance=result.relevance,
            )
            for result in knowledge
        ]

    @staticmethod
    def _build_summary(request: AIRequest) -> str:
        vehicle = request.vehicle
        return (
            f"{vehicle.year} {vehicle.make} {vehicle.model} has a "
            f"deterministic trust score of {request.trust.score}/100 "
            f"with a purchase decision of "
            f"{request.decision.recommendation}."
        )

    @staticmethod
    def _build_reasoning(request: AIRequest) -> str:
        if not request.risks:
            return (
                "No identified risks were provided by the deterministic "
                "vehicle intelligence layer."
            )

        risk_descriptions = [
            f"{risk.title} ({risk.severity})"
            for risk in request.risks
        ]

        return (
            "The deterministic vehicle intelligence identified: "
            + ", ".join(risk_descriptions)
            + "."
        )

    @staticmethod
    def _build_recommendation(request: AIRequest) -> str:
        return (
            f"The deterministic decision is "
            f"{request.decision.recommendation}. "
            f"{request.decision.rationale}"
        )

    @staticmethod
    def _determine_grounding_status(
        *,
        evidence_count: int,
        knowledge_count: int,
    ) -> str:
        if evidence_count > 0 and knowledge_count > 0:
            return "grounded"

        if evidence_count > 0 or knowledge_count > 0:
            return "partially_grounded"

        return "insufficient"