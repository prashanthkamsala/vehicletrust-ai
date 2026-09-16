from app.intelligence.ai.explanation import build_ai_interpretation
from app.intelligence.evidence.engine import build_evidence
from app.intelligence.risk.engine import build_risks
from app.intelligence.trust.engine import build_trust_assessment
from app.providers.mock_india import MockIndiaProvider


provider = MockIndiaProvider()


def _build_intelligence(registration: str):
    vehicle_data = provider.get_vehicle_by_registration(registration)

    assert vehicle_data is not None

    evidence = build_evidence(vehicle_data)
    risks = build_risks(evidence)
    trust = build_trust_assessment(
        evidence=evidence,
        risks=risks,
    )

    interpretation = build_ai_interpretation(
        evidence=evidence,
        risks=risks,
        trust=trust,
    )

    return interpretation, evidence, risks, trust


def test_clean_vehicle_gets_positive_explanation():
    interpretation, evidence, risks, trust = _build_intelligence(
        "KA 05 MN 4821"
    )

    assert trust.score == 100
    assert risks == []

    assert interpretation.summary
    assert "very high trust" in interpretation.summary.lower()
    assert "no significant risks" in interpretation.summary.lower()

    assert interpretation.reasoning
    assert interpretation.recommendation


def test_moderate_risk_vehicle_mentions_identified_risks():
    interpretation, evidence, risks, trust = _build_intelligence(
        "TS 09 PQ 7316"
    )

    assert trust.score == 72
    assert len(risks) == 2

    assert "moderate trust" in interpretation.summary.lower()
    assert "risk" in interpretation.summary.lower()

    assert "PUC certificate has expired" in interpretation.reasoning
    assert "Multiple ownership history" in interpretation.reasoning

    assert interpretation.recommendation


def test_high_risk_vehicle_mentions_high_severity_risks():
    interpretation, evidence, risks, trust = _build_intelligence(
        "MH 12 XY 9087"
    )

    assert trust.score == 0

    high_risks = [
        risk for risk in risks if risk.severity == "high"
    ]

    assert len(high_risks) == 2

    assert "very low trust" in interpretation.summary.lower()
    assert "high-severity" in interpretation.summary.lower()

    assert "Odometer inconsistency detected" in interpretation.reasoning
    assert "Major accident history requires investigation" in interpretation.reasoning

    assert interpretation.recommendation


def test_explanation_does_not_invent_risks():
    interpretation, evidence, risks, trust = _build_intelligence(
        "KA 05 MN 4821"
    )

    risk_titles = {risk.title for risk in risks}

    for risk_title in risk_titles:
        assert risk_title in interpretation.reasoning

    assert "significant risks" in interpretation.summary.lower()


def test_missing_evidence_produces_cautious_explanation():
    interpretation = build_ai_interpretation(
        evidence=[],
        risks=[],
        trust=build_trust_assessment(
            evidence=[],
            risks=[],
        ),
    )

    assert "insufficient" in interpretation.summary.lower()
    assert "did not receive enough evidence" in interpretation.reasoning.lower()
    assert "additional vehicle records" in interpretation.recommendation.lower()