from app.domain.vehicle_service import _build_vehicle_from_registration
from app.intelligence.ai.request_builder import build_ai_request


def test_build_ai_request_from_clean_vehicle() -> None:
    vehicle = _build_vehicle_from_registration("KA 05 MN 4821")

    assert vehicle is not None

    request = build_ai_request(vehicle)

    assert request.vehicle.make == "Toyota"
    assert request.vehicle.model == "Camry"
    assert request.vehicle.year == 2021
    assert request.vehicle.registration == "KA 05 MN 4821"

    assert request.trust.score == 100
    assert request.decision.recommendation == "buy"

    assert len(request.evidence) == len(vehicle.evidence)
    assert len(request.risks) == len(vehicle.risks)


def test_build_ai_request_preserves_risk_evidence_links() -> None:
    vehicle = _build_vehicle_from_registration("TS 09 PQ 7316")

    assert vehicle is not None

    request = build_ai_request(vehicle)

    evidence_ids = {evidence.id for evidence in request.evidence}

    for risk in request.risks:
        for evidence_id in risk.evidence_ids:
            assert evidence_id in evidence_ids


def test_build_ai_request_preserves_high_risk_decision() -> None:
    vehicle = _build_vehicle_from_registration("MH 12 XY 9087")

    assert vehicle is not None

    request = build_ai_request(vehicle)

    assert request.vehicle.make == "Honda"
    assert request.vehicle.model == "City"
    assert request.vehicle.registration == "MH 12 XY 9087"

    assert request.trust.score == 0
    assert request.decision.recommendation == "avoid"

    assert "odometer-inconsistency" in request.decision.priority_risk_ids
    assert "major-accident-history" in request.decision.priority_risk_ids


def test_build_ai_request_does_not_include_vin() -> None:
    vehicle = _build_vehicle_from_registration("KA 05 MN 4821")

    assert vehicle is not None

    request = build_ai_request(vehicle)

    assert not hasattr(request.vehicle, "vin")


def test_build_ai_request_preserves_evidence_provenance() -> None:
    vehicle = _build_vehicle_from_registration("MH 12 XY 9087")

    assert vehicle is not None

    request = build_ai_request(vehicle)

    for evidence in request.evidence:
        assert evidence.provenance is not None