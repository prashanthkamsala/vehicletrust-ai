from app.retrieval.base import KnowledgeResult
from app.schemas.contracts import AIResponse


class GroundingValidationError(ValueError):
    """Raised when an AI response violates grounding requirements."""


def validate_ai_response(
    response: AIResponse,
    *,
    evidence_ids: set[str],
    knowledge_results: list[KnowledgeResult],
) -> None:
    """Validate that an AI response references available grounding sources."""

    available_knowledge_ids = {
        result.document.id
        for result in knowledge_results
    }

    unknown_evidence_ids = (
        set(response.supporting_evidence_ids) - evidence_ids
    )

    if unknown_evidence_ids:
        raise GroundingValidationError(
            "AI response references unknown evidence IDs: "
            + ", ".join(sorted(unknown_evidence_ids))
        )

    unknown_knowledge_ids = (
        {
            reference.id
            for reference in response.knowledge_references
        }
        - available_knowledge_ids
    )

    if unknown_knowledge_ids:
        raise GroundingValidationError(
            "AI response references unknown knowledge IDs: "
            + ", ".join(sorted(unknown_knowledge_ids))
        )

    if response.grounding.evidence_count != len(
        response.supporting_evidence_ids
    ):
        raise GroundingValidationError(
            "AI grounding evidence count does not match "
            "supporting evidence references."
        )

    if response.grounding.knowledge_count != len(
        response.knowledge_references
    ):
        raise GroundingValidationError(
            "AI grounding knowledge count does not match "
            "knowledge references."
        )

    evidence_count = response.grounding.evidence_count
    knowledge_count = response.grounding.knowledge_count

    if response.grounding.status == "grounded":
        if evidence_count == 0 or knowledge_count == 0:
            raise GroundingValidationError(
                "A grounded response must reference both evidence "
                "and domain knowledge."
            )

    elif response.grounding.status == "partially_grounded":
        if evidence_count == 0 and knowledge_count == 0:
            raise GroundingValidationError(
                "A partially grounded response must reference evidence "
                "or domain knowledge."
            )

    elif response.grounding.status == "insufficient":
        if evidence_count > 0 or knowledge_count > 0:
            raise GroundingValidationError(
                "An insufficient response must not reference evidence "
                "or domain knowledge."
            )