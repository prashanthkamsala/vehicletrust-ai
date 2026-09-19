from app.schemas.contracts import (
    AIDecisionAssessment,
    AIEvidenceItem,
    AIEvidenceProvenance,
    AIEvidenceSource,
    AIGrounding,
    AIKnowledgeReference,
    AIRiskItem,
    AIRequest,
    AIResponse,
    AITrustAssessment,
    AITrustFactor,
    AIVehicleIdentity,
)


def build_request() -> AIRequest:
    return AIRequest(
        vehicle=AIVehicleIdentity(
            make="Hyundai",
            model="Creta",
            year=2022,
            registration="TS 09 PQ 7316",
        ),
        evidence=[
            AIEvidenceItem(
                id="puc-status",
                category="Compliance",
                title="PUC status",
                value="Expired",
                status="partially_verified",
                confidence="high",
                explanation="The available PUC record shows an expired certificate.",
                source=AIEvidenceSource(
                    id="registration-records",
                    name="Vehicle registration records",
                    type="registration",
                ),
                provenance=AIEvidenceProvenance(
                    observed_at="2026-09-10",
                    reference_id="mock-puc-001",
                ),
            ),
        ],
        risks=[
            AIRiskItem(
                id="expired-puc",
                category="Compliance",
                title="PUC certificate has expired",
                severity="medium",
                status="needs_review",
                confidence="high",
                explanation="The latest available PUC record is expired.",
                evidence_ids=["puc-status"],
                recommended_action="Request a valid PUC certificate before purchase.",
            ),
        ],
        trust=AITrustAssessment(
            score=72,
            confidence="medium",
            assessment="Moderate trust",
            factors=[
                AITrustFactor(
                    id="puc-factor",
                    name="PUC status",
                    impact="negative",
                    contribution=-8,
                    evidence_ids=["puc-status"],
                ),
            ],
        ),
        decision=AIDecisionAssessment(
            recommendation="review",
            confidence="medium",
            rationale="The vehicle has issues that should be reviewed before purchase.",
            priority_risk_ids=["expired-puc"],
        ),
    )


def test_ai_request_accepts_vehicle_intelligence_context() -> None:
    request = build_request()

    assert request.vehicle.make == "Hyundai"
    assert request.vehicle.model == "Creta"
    assert request.vehicle.registration == "TS 09 PQ 7316"
    assert len(request.evidence) == 1
    assert len(request.risks) == 1
    assert request.trust.score == 72
    assert request.decision.recommendation == "review"


def test_ai_request_preserves_evidence_traceability() -> None:
    request = build_request()

    evidence_ids = {evidence.id for evidence in request.evidence}

    for risk in request.risks:
        for evidence_id in risk.evidence_ids:
            assert evidence_id in evidence_ids


def test_ai_request_preserves_deterministic_decision() -> None:
    request = build_request()

    assert request.trust.score == 72
    assert request.decision.recommendation == "review"
    assert request.decision.priority_risk_ids == ["expired-puc"]


def test_ai_response_contains_grounding_information() -> None:
    response = AIResponse(
        summary="The vehicle requires additional compliance verification.",
        reasoning="The available evidence shows an expired PUC certificate.",
        recommendation="Verify the PUC status before making a final decision.",
        supporting_evidence_ids=["puc-status"],
        knowledge_references=[
            AIKnowledgeReference(
                id="puc-compliance",
                title="PUC compliance guidance",
                category="puc",
                relevance="Explains the significance of a valid PUC certificate.",
            ),
        ],
        grounding=AIGrounding(
            status="grounded",
            evidence_count=1,
            knowledge_count=1,
        ),
    )

    assert response.grounding.status == "grounded"
    assert response.grounding.evidence_count == 1
    assert response.grounding.knowledge_count == 1
    assert response.supporting_evidence_ids == ["puc-status"]
    assert len(response.knowledge_references) == 1