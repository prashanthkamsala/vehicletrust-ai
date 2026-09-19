from app.generation.deterministic import DeterministicGenerator
from app.retrieval.base import KnowledgeDocument, KnowledgeResult
from app.schemas.contracts import (
    AIDecisionAssessment,
    AIEvidenceItem,
    AIEvidenceProvenance,
    AIEvidenceSource,
    AIRiskItem,
    AITrustAssessment,
    AITrustFactor,
    AIVehicleIdentity,
    AIRequest,
)


def build_request() -> AIRequest:
    return AIRequest(
        vehicle=AIVehicleIdentity(
            make="Honda",
            model="City",
            year=2020,
            registration="MH 12 XY 9087",
        ),
        evidence=[
            AIEvidenceItem(
                id="odometer-inconsistency",
                category="mileage",
                title="Odometer inconsistency",
                value="67,300 km to 52,100 km",
                status="conflicting",
                confidence="high",
                explanation="The recorded mileage decreases.",
                source=AIEvidenceSource(
                    id="mock-provider",
                    name="Mock India Provider",
                    type="mock",
                ),
                provenance=AIEvidenceProvenance(),
            ),
            AIEvidenceItem(
                id="insurance-expired",
                category="insurance",
                title="Insurance expired",
                value="Expired",
                status="verified",
                confidence="high",
                explanation="The insurance policy has expired.",
                source=AIEvidenceSource(
                    id="mock-provider",
                    name="Mock India Provider",
                    type="mock",
                ),
                provenance=AIEvidenceProvenance(),
            ),
        ],
        risks=[
            AIRiskItem(
                id="odometer-risk",
                category="mileage",
                title="Odometer inconsistency",
                severity="high",
                status="needs_review",
                confidence="high",
                explanation="Mileage records contain a decrease.",
                evidence_ids=["odometer-inconsistency"],
                recommended_action="Verify mileage history.",
            ),
            AIRiskItem(
                id="insurance-risk",
                category="insurance",
                title="Expired insurance",
                severity="medium",
                status="identified",
                confidence="high",
                explanation="Insurance coverage has expired.",
                evidence_ids=["insurance-expired"],
                recommended_action="Verify current insurance coverage.",
            ),
        ],
        trust=AITrustAssessment(
            score=42,
            confidence="medium",
            assessment="Low trust due to multiple identified risks.",
            factors=[
                AITrustFactor(
                    id="mileage",
                    name="Mileage consistency",
                    impact="negative",
                    contribution=-20,
                    evidence_ids=["odometer-inconsistency"],
                ),
            ],
        ),
        decision=AIDecisionAssessment(
            recommendation="avoid",
            confidence="high",
            rationale="High-severity mileage evidence requires verification.",
            priority_risk_ids=["odometer-risk"],
        ),
    )


def build_knowledge_result() -> KnowledgeResult:
    return KnowledgeResult(
        document=KnowledgeDocument(
            id="odometer",
            title="Odometer Verification Guidance",
            category="odometer",
            content="Mileage decreases require investigation.",
            keywords=["odometer", "mileage"],
        ),
        relevance="Keyword relevance score: 8",
    )


def test_generator_preserves_deterministic_decision() -> None:
    request = build_request()

    response = DeterministicGenerator().generate(
        request,
        [build_knowledge_result()],
    )

    assert "avoid" in response.recommendation
    assert "High-severity mileage evidence requires verification." in (
        response.recommendation
    )


def test_generator_selects_evidence_from_priority_risks() -> None:
    request = build_request()

    response = DeterministicGenerator().generate(
        request,
        [build_knowledge_result()],
    )

    assert response.supporting_evidence_ids == [
        "odometer-inconsistency",
    ]


def test_generator_builds_knowledge_references() -> None:
    request = build_request()

    response = DeterministicGenerator().generate(
        request,
        [build_knowledge_result()],
    )

    assert len(response.knowledge_references) == 1
    assert response.knowledge_references[0].id == "odometer"
    assert (
        response.knowledge_references[0].title
        == "Odometer Verification Guidance"
    )


def test_generator_reports_grounded_response() -> None:
    request = build_request()

    response = DeterministicGenerator().generate(
        request,
        [build_knowledge_result()],
    )

    assert response.grounding.status == "grounded"
    assert response.grounding.evidence_count == 1
    assert response.grounding.knowledge_count == 1


def test_generator_without_knowledge_is_partially_grounded() -> None:
    request = build_request()

    response = DeterministicGenerator().generate(
        request,
        [],
    )

    assert response.grounding.status == "partially_grounded"
    assert response.grounding.evidence_count == 1
    assert response.grounding.knowledge_count == 0


def test_generator_without_evidence_or_knowledge_is_insufficient() -> None:
    request = build_request()
    request.risks = []
    request.evidence = []

    response = DeterministicGenerator().generate(
        request,
        [],
    )

    assert response.supporting_evidence_ids == []
    assert response.grounding.status == "insufficient"
    assert response.grounding.evidence_count == 0
    assert response.grounding.knowledge_count == 0