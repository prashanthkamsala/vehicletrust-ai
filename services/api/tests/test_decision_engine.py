from app.intelligence.decision.engine import build_decision_assessment
from app.intelligence.evidence.engine import build_evidence
from app.intelligence.risk.engine import build_risks
from app.intelligence.trust.engine import build_trust_assessment
from app.providers.mock_india import MockIndiaProvider


provider = MockIndiaProvider()


def _build_vehicle_assessment(registration: str):
    vehicle_data = provider.get_vehicle_by_registration(registration)

    assert vehicle_data is not None

    evidence = build_evidence(vehicle_data)
    risks = build_risks(evidence)
    trust = build_trust_assessment(
        evidence=evidence,
        risks=risks,
    )

    decision = build_decision_assessment(
        risks=risks,
        trust=trust,
        evidence_count=len(evidence),
    )

    return evidence, risks, trust, decision


def test_clean_vehicle_gets_buy_recommendation():
    evidence, risks, trust, decision = _build_vehicle_assessment(
        "KA 05 MN 4821",
    )

    assert len(evidence) > 0
    assert risks == []
    assert trust.score == 100
    assert decision.recommendation == "buy"
    assert decision.confidence == "high"
    assert decision.priority_risk_ids == []


def test_moderate_vehicle_gets_review_recommendation():
    evidence, risks, trust, decision = _build_vehicle_assessment(
        "TS 09 PQ 7316",
    )

    assert len(evidence) > 0
    assert len(risks) > 0
    assert trust.score == 72
    assert decision.recommendation == "review"
    assert decision.confidence in {"high", "medium"}
    assert len(decision.priority_risk_ids) > 0


def test_high_risk_vehicle_gets_avoid_recommendation():
    evidence, risks, trust, decision = _build_vehicle_assessment(
        "MH 12 XY 9087",
    )

    assert len(evidence) > 0
    assert len(risks) >= 2
    assert trust.score == 0
    assert decision.recommendation == "avoid"
    assert decision.confidence == "high"
    assert "odometer-inconsistency" in decision.priority_risk_ids
    assert "major-accident-history" in decision.priority_risk_ids


def test_empty_evidence_produces_insufficient_evidence():
    _, _, trust, decision = _build_vehicle_assessment(
        "KA 05 MN 4821",
    )

    decision = build_decision_assessment(
        risks=[],
        trust=trust,
        evidence_count=0,
    )

    assert decision.recommendation == "insufficient_evidence"
    assert decision.confidence == "low"
    assert decision.priority_risk_ids == []


def test_priority_risks_are_limited_to_three():
    evidence, risks, trust, decision = _build_vehicle_assessment(
        "MH 12 XY 9087",
    )

    assert len(evidence) > 0
    assert len(risks) > 3
    assert len(decision.priority_risk_ids) == 3