from unittest import result

from app.intelligence.evidence.engine import build_evidence
from app.intelligence.risk.engine import build_risks
from app.providers.mock_india import MockIndiaProvider


provider = MockIndiaProvider()


def _build_vehicle_risks(registration: str):
    result = provider.get_vehicle_by_registration(registration)

    assert result.is_success
    assert result.vehicle is not None

    vehicle = result.vehicle

    evidence = build_evidence(vehicle)

    return build_risks(evidence)


def test_clean_vehicle_has_no_derived_risks() -> None:
    risks = _build_vehicle_risks("KA 05 MN 4821")

    assert risks == []


def test_moderate_vehicle_derives_expected_risks() -> None:
    risks = _build_vehicle_risks("TS 09 PQ 7316")

    risk_ids = {risk.id for risk in risks}

    assert "expired-puc" in risk_ids
    assert "multiple-ownership-history" in risk_ids

    assert "expired-insurance" not in risk_ids
    assert "active-finance" not in risk_ids
    assert "odometer-inconsistency" not in risk_ids
    assert "major-accident-history" not in risk_ids
    assert "open-challans" not in risk_ids


def test_high_risk_vehicle_derives_all_expected_risks() -> None:
    risks = _build_vehicle_risks("MH 12 XY 9087")

    risk_ids = {risk.id for risk in risks}

    assert "odometer-inconsistency" in risk_ids
    assert "major-accident-history" in risk_ids
    assert "active-finance" in risk_ids
    assert "expired-insurance" in risk_ids
    assert "expired-puc" in risk_ids
    assert "open-challans" in risk_ids
    assert "multiple-ownership-history" in risk_ids


def test_high_risk_risks_are_traceable_to_evidence() -> None:
    result = provider.get_vehicle_by_registration("MH 12 XY 9087")

    assert result.is_success
    assert result.vehicle is not None

    vehicle = result.vehicle

    evidence = build_evidence(vehicle)
    risks = build_risks(evidence)
    evidence_ids = {item.id for item in evidence}

    assert len(risks) > 0

    for risk in risks:
        assert len(risk.evidence_ids) > 0

        for evidence_id in risk.evidence_ids:
            assert evidence_id in evidence_ids


def test_odometer_risk_has_high_severity_and_confidence() -> None:
    risks = _build_vehicle_risks("MH 12 XY 9087")

    odometer_risk = next(
        risk for risk in risks if risk.id == "odometer-inconsistency"
    )

    assert odometer_risk.severity == "high"
    assert odometer_risk.status == "needs_review"
    assert odometer_risk.confidence == "high"
    assert odometer_risk.evidence_ids == ["mileage-consistency"]
