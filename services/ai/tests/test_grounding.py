import pytest

from app.domain.grounding import (
    GroundingValidationError,
    validate_ai_response,
)
from app.retrieval.base import KnowledgeDocument, KnowledgeResult
from app.schemas.contracts import (
    AIGrounding,
    AIKnowledgeReference,
    AIResponse,
)


def build_knowledge_result() -> KnowledgeResult:
    return KnowledgeResult(
        document=KnowledgeDocument(
            id="odometer",
            title="Odometer Verification Guidance",
            category="odometer",
            content="An odometer decrease requires investigation.",
            keywords=["odometer", "mileage", "inconsistency"],
        ),
        relevance="Keyword relevance score: 8",
    )


def build_response(
    *,
    evidence_ids: list[str] | None = None,
    knowledge_ids: list[str] | None = None,
    grounding_status: str = "grounded",
    evidence_count: int | None = None,
    knowledge_count: int | None = None,
) -> AIResponse:
    evidence_ids = evidence_ids or []
    knowledge_ids = knowledge_ids or []

    references = [
        AIKnowledgeReference(
            id=knowledge_id,
            title="Odometer Verification Guidance",
            category="odometer",
            relevance="Relevant to the identified mileage risk.",
        )
        for knowledge_id in knowledge_ids
    ]

    return AIResponse(
        summary="The available evidence requires additional verification.",
        reasoning="The vehicle records contain an odometer inconsistency.",
        recommendation="Verify the mileage history before making a final decision.",
        supporting_evidence_ids=evidence_ids,
        knowledge_references=references,
        grounding=AIGrounding(
            status=grounding_status,
            evidence_count=(
                len(evidence_ids)
                if evidence_count is None
                else evidence_count
            ),
            knowledge_count=(
                len(references)
                if knowledge_count is None
                else knowledge_count
            ),
        ),
    )


def test_valid_grounded_response_passes() -> None:
    response = build_response(
        evidence_ids=["mileage-consistency"],
        knowledge_ids=["odometer"],
    )

    validate_ai_response(
        response,
        evidence_ids={"mileage-consistency"},
        knowledge_results=[build_knowledge_result()],
    )


def test_unknown_evidence_reference_fails() -> None:
    response = build_response(
        evidence_ids=["unknown-evidence"],
        knowledge_ids=["odometer"],
    )

    with pytest.raises(
        GroundingValidationError,
        match="unknown evidence IDs",
    ):
        validate_ai_response(
            response,
            evidence_ids={"mileage-consistency"},
            knowledge_results=[build_knowledge_result()],
        )


def test_unknown_knowledge_reference_fails() -> None:
    response = build_response(
        evidence_ids=["mileage-consistency"],
        knowledge_ids=["unknown-knowledge"],
    )

    with pytest.raises(
        GroundingValidationError,
        match="unknown knowledge IDs",
    ):
        validate_ai_response(
            response,
            evidence_ids={"mileage-consistency"},
            knowledge_results=[build_knowledge_result()],
        )


def test_incorrect_evidence_count_fails() -> None:
    response = build_response(
        evidence_ids=["mileage-consistency"],
        knowledge_ids=["odometer"],
        evidence_count=0,
    )

    with pytest.raises(
        GroundingValidationError,
        match="evidence count",
    ):
        validate_ai_response(
            response,
            evidence_ids={"mileage-consistency"},
            knowledge_results=[build_knowledge_result()],
        )


def test_incorrect_knowledge_count_fails() -> None:
    response = build_response(
        evidence_ids=["mileage-consistency"],
        knowledge_ids=["odometer"],
        knowledge_count=0,
    )

    with pytest.raises(
        GroundingValidationError,
        match="knowledge count",
    ):
        validate_ai_response(
            response,
            evidence_ids={"mileage-consistency"},
            knowledge_results=[build_knowledge_result()],
        )


def test_grounded_response_requires_both_evidence_and_knowledge() -> None:
    response = build_response(
        grounding_status="grounded",
        evidence_ids=["mileage-consistency"],
        knowledge_ids=[],
    )

    with pytest.raises(
        GroundingValidationError,
        match="must reference both evidence and domain knowledge",
    ):
        validate_ai_response(
            response,
            evidence_ids={"mileage-consistency"},
            knowledge_results=[],
        )


def test_partially_grounded_response_requires_at_least_one_source() -> None:
    response = build_response(
        grounding_status="partially_grounded",
    )

    with pytest.raises(
        GroundingValidationError,
        match="partially grounded response must reference evidence "
        "or domain knowledge",
    ):
        validate_ai_response(
            response,
            evidence_ids=set(),
            knowledge_results=[],
        )


def test_insufficient_response_must_not_reference_sources() -> None:
    response = build_response(
        grounding_status="insufficient",
        evidence_ids=["mileage-consistency"],
        knowledge_ids=[],
    )

    with pytest.raises(
        GroundingValidationError,
        match="insufficient response must not reference evidence "
        "or domain knowledge",
    ):
        validate_ai_response(
            response,
            evidence_ids={"mileage-consistency"},
            knowledge_results=[],
        )