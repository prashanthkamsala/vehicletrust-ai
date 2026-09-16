from app.intelligence.evidence.engine import build_evidence
from app.intelligence.risk.engine import build_risks
from app.intelligence.trust.engine import build_trust_assessment
from app.providers.mock_india import MockIndiaProvider
from app.intelligence import trust


provider = MockIndiaProvider()


def _build_vehicle_trust(registration: str):
    vehicle_data = provider.get_vehicle_by_registration(registration)

    assert vehicle_data is not None

    evidence = build_evidence(vehicle_data)
    risks = build_risks(evidence)

    return build_trust_assessment(
        evidence=evidence,
        risks=risks,
    )


def test_clean_vehicle_has_high_trust() -> None:
    trust = _build_vehicle_trust("KA 05 MN 4821")

    assert trust.score >= 90
    assert trust.assessment == "Very high trust"
    assert trust.confidence == "high"
    assert trust.calculated_score == 100
    assert trust.score == 100


def test_moderate_vehicle_has_moderate_trust() -> None:
    trust = _build_vehicle_trust("TS 09 PQ 7316")

    assert 60 <= trust.score <= 89
    assert trust.assessment in {"Moderate trust", "High trust"}
    assert trust.calculated_score == 72
    assert trust.score == 72


def test_high_risk_vehicle_has_low_trust() -> None:
    trust = _build_vehicle_trust("MH 12 XY 9087")

    assert trust.score < 60
    assert trust.assessment in {"Low trust", "Very low trust"}
    assert trust.calculated_score == -16
    assert trust.score == 0


def test_trust_score_is_bounded() -> None:
    trust = _build_vehicle_trust("MH 12 XY 9087")

    assert 0 <= trust.score <= 100


def test_trust_factors_trace_to_evidence() -> None:
    trust = _build_vehicle_trust("MH 12 XY 9087")

    evidence_ids = {
        evidence_id
        for factor in trust.factors
        for evidence_id in factor.evidence_ids
    }

    assert evidence_ids
    assert all(evidence_id for evidence_id in evidence_ids)


def test_high_risk_vehicle_contains_negative_trust_factors() -> None:
    trust = _build_vehicle_trust("MH 12 XY 9087")

    negative_factors = [
        factor
        for factor in trust.factors
        if factor.impact == "negative"
    ]

    factor_ids = {factor.id for factor in negative_factors}

    assert "odometer-factor" in factor_ids
    assert "accident-factor" in factor_ids
    assert "finance-factor" in factor_ids
    assert "insurance-factor" in factor_ids
    assert "puc-factor" in factor_ids
    assert "challan-factor" in factor_ids
    assert "ownership-factor" in factor_ids