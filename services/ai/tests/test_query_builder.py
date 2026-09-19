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
from app.retrieval.query_builder import build_retrieval_queries


def build_request(
    *,
    risks: list[AIRiskItem] | None = None,
    evidence: list[AIEvidenceItem] | None = None,
) -> AIRequest:
    return AIRequest(
        vehicle=AIVehicleIdentity(
            make="Honda",
            model="City",
            year=2021,
            registration="MH 12 XY 9087",
        ),
        evidence=evidence or [],
        risks=risks or [],
        trust=AITrustAssessment(
            score=0,
            confidence="low",
            assessment="Very low trust",
        ),
        decision=AIDecisionAssessment(
            recommendation="avoid",
            confidence="high",
            rationale="High-severity risks require investigation.",
        ),
    )


def test_builds_queries_from_risks() -> None:
    request = build_request(
        risks=[
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
        ],
    )

    queries = build_retrieval_queries(request)

    assert len(queries) == 1
    assert "Mileage" in queries[0]
    assert "Odometer inconsistency" in queries[0]
    assert "verification guidance" in queries[0]


def test_builds_queries_from_multiple_risks() -> None:
    request = build_request(
        risks=[
            AIRiskItem(
                id="expired-insurance",
                category="Insurance",
                title="Insurance has expired",
                severity="medium",
                status="needs_review",
                confidence="high",
                explanation="The available insurance record is expired.",
                evidence_ids=["insurance-status"],
                recommended_action="Verify current insurance coverage.",
            ),
            AIRiskItem(
                id="expired-puc",
                category="Compliance",
                title="PUC certificate has expired",
                severity="medium",
                status="needs_review",
                confidence="high",
                explanation="The available PUC record is expired.",
                evidence_ids=["puc-status"],
                recommended_action="Obtain a valid PUC certificate.",
            ),
        ],
    )

    queries = build_retrieval_queries(request)

    assert len(queries) == 2
    assert "Insurance" in queries[0]
    assert "Compliance" in queries[1]


def test_falls_back_to_uncertain_evidence_when_no_risks_exist() -> None:
    request = build_request(
        evidence=[
            AIEvidenceItem(
                id="mileage-consistency",
                category="Mileage",
                title="Mileage consistency",
                value="Inconsistent",
                status="conflicting",
                confidence="high",
                explanation="Mileage records contain an unexpected decrease.",
                source=AIEvidenceSource(
                    id="mileage-records",
                    name="Mileage records",
                    type="vehicle_history",
                ),
                provenance=AIEvidenceProvenance(
                    observed_at="2026-09-10",
                ),
            ),
        ],
    )

    queries = build_retrieval_queries(request)

    assert len(queries) == 1
    assert "Mileage" in queries[0]
    assert "Inconsistent" in queries[0]


def test_returns_empty_when_no_risks_or_uncertain_evidence_exist() -> None:
    request = build_request()

    assert build_retrieval_queries(request) == []


def test_does_not_create_duplicate_queries() -> None:
    risk = AIRiskItem(
        id="expired-puc",
        category="Compliance",
        title="PUC certificate has expired",
        severity="medium",
        status="needs_review",
        confidence="high",
        explanation="The available PUC record is expired.",
        evidence_ids=["puc-status"],
        recommended_action="Obtain a valid PUC certificate.",
    )

    request = build_request(risks=[risk, risk])

    queries = build_retrieval_queries(request)

    assert len(queries) == 1