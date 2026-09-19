from app.domain.factory import build_local_ai_service
from app.schemas.contracts import (
    AIDecisionAssessment,
    AIEvidenceItem,
    AIEvidenceProvenance,
    AIEvidenceSource,
    AIRiskItem,
    AIRequest,
    AITrustAssessment,
    AIVehicleIdentity,
)


def build_honda_high_risk_request() -> AIRequest:
    evidence = [
        AIEvidenceItem(
            id="mileage-consistency",
            category="Mileage",
            title="Mileage consistency",
            value="Inconsistent: 67,300 km to 52,100 km",
            status="conflicting",
            confidence="high",
            explanation="The odometer history contains a decrease.",
            source=AIEvidenceSource(
                id="mock-india-provider",
                name="Mock India Provider",
                type="vehicle_history",
            ),
            provenance=AIEvidenceProvenance(
                observed_at="2026-09-10",
            ),
        ),
        AIEvidenceItem(
            id="accident-history",
            category="Accident",
            title="Major accident history",
            value="Major accident reported",
            status="conflicting",
            confidence="high",
            explanation="A major accident is present in the available records.",
            source=AIEvidenceSource(
                id="mock-india-provider",
                name="Mock India Provider",
                type="vehicle_history",
            ),
            provenance=AIEvidenceProvenance(
                observed_at="2026-09-10",
            ),
        ),
        AIEvidenceItem(
            id="insurance-status",
            category="Insurance",
            title="Insurance status",
            value="Expired",
            status="verified",
            confidence="high",
            explanation="The available insurance record is expired.",
            source=AIEvidenceSource(
                id="mock-india-provider",
                name="Mock India Provider",
                type="vehicle_history",
            ),
            provenance=AIEvidenceProvenance(
                observed_at="2026-09-10",
            ),
        ),
        AIEvidenceItem(
            id="puc-status",
            category="Compliance",
            title="PUC status",
            value="Expired",
            status="verified",
            confidence="high",
            explanation="The available PUC record is expired.",
            source=AIEvidenceSource(
                id="mock-india-provider",
                name="Mock India Provider",
                type="vehicle_history",
            ),
            provenance=AIEvidenceProvenance(
                observed_at="2026-09-10",
            ),
        ),
        AIEvidenceItem(
            id="finance-status",
            category="Finance",
            title="Finance status",
            value="Active",
            status="verified",
            confidence="high",
            explanation="The vehicle has an active finance record.",
            source=AIEvidenceSource(
                id="mock-india-provider",
                name="Mock India Provider",
                type="vehicle_history",
            ),
            provenance=AIEvidenceProvenance(
                observed_at="2026-09-10",
            ),
        ),
    ]

    risks = [
        AIRiskItem(
            id="odometer-inconsistency",
            category="Mileage",
            title="Odometer inconsistency",
            severity="high",
            status="needs_review",
            confidence="high",
            explanation="The odometer history contains a decrease.",
            evidence_ids=["mileage-consistency"],
            recommended_action="Verify the mileage history.",
        ),
        AIRiskItem(
            id="major-accident-history",
            category="Accident",
            title="Major accident history",
            severity="high",
            status="needs_review",
            confidence="high",
            explanation="A major accident is present in the available records.",
            evidence_ids=["accident-history"],
            recommended_action="Review accident and repair records.",
        ),
        AIRiskItem(
            id="expired-insurance",
            category="Insurance",
            title="Expired insurance",
            severity="medium",
            status="identified",
            confidence="high",
            explanation="The insurance record is expired.",
            evidence_ids=["insurance-status"],
            recommended_action="Verify current insurance coverage.",
        ),
        AIRiskItem(
            id="expired-puc",
            category="Compliance",
            title="Expired PUC",
            severity="medium",
            status="identified",
            confidence="high",
            explanation="The PUC record is expired.",
            evidence_ids=["puc-status"],
            recommended_action="Verify current PUC status.",
        ),
        AIRiskItem(
            id="active-finance",
            category="Finance",
            title="Active finance",
            severity="medium",
            status="identified",
            confidence="high",
            explanation="The vehicle has an active finance record.",
            evidence_ids=["finance-status"],
            recommended_action="Verify finance closure status.",
        ),
    ]

    return AIRequest(
        vehicle=AIVehicleIdentity(
            make="Honda",
            model="City",
            year=2020,
            registration="MH 12 XY 9087",
        ),
        evidence=evidence,
        risks=risks,
        trust=AITrustAssessment(
            score=0,
            confidence="high",
            assessment="Very low trust due to significant evidence risks.",
        ),
        decision=AIDecisionAssessment(
            recommendation="avoid",
            confidence="high",
            rationale="Multiple high-severity risks require investigation.",
            priority_risk_ids=[
                "odometer-inconsistency",
                "major-accident-history",
            ],
        ),
    )


def test_local_ai_pipeline_produces_grounded_response() -> None:
    request = build_honda_high_risk_request()

    service = build_local_ai_service()

    response = service.interpret(request)

    assert response.grounding.status == "grounded"
    assert response.grounding.evidence_count == 2
    assert response.grounding.knowledge_count >= 2

    assert "mileage-consistency" in response.supporting_evidence_ids
    assert "accident-history" in response.supporting_evidence_ids

    knowledge_ids = {
        reference.id
        for reference in response.knowledge_references
    }

    assert "odometer" in knowledge_ids
    assert "accident" in knowledge_ids


def test_local_ai_pipeline_preserves_deterministic_decision() -> None:
    request = build_honda_high_risk_request()

    service = build_local_ai_service()

    response = service.interpret(request)

    assert request.decision.recommendation == "avoid"
    assert "avoid" in response.recommendation
    assert str(request.trust.score) in response.summary


def test_local_ai_pipeline_retrieves_risk_specific_knowledge() -> None:
    request = build_honda_high_risk_request()

    service = build_local_ai_service()

    response = service.interpret(request)

    knowledge_ids = {
        reference.id
        for reference in response.knowledge_references
    }

    assert {
        "odometer",
        "accident",
        "insurance",
        "finance",
        "puc",
    }.issubset(knowledge_ids)