from app.intelligence.evidence.engine import build_evidence
from app.providers.mock_india import MockIndiaProvider


provider = MockIndiaProvider()


def test_clean_vehicle_produces_verified_evidence() -> None:
    vehicle = provider.get_vehicle_by_registration("KA 05 MN 4821")

    assert vehicle is not None

    evidence = build_evidence(vehicle)

    evidence_by_id = {item.id: item for item in evidence}

    assert evidence_by_id["registration-status"].status == "verified"
    assert evidence_by_id["insurance-status"].status == "verified"
    assert evidence_by_id["puc-status"].status == "verified"
    assert evidence_by_id["finance-status"].status == "verified"
    assert evidence_by_id["mileage-consistency"].status == "verified"
    assert evidence_by_id["accident-history"].value == "No recorded accidents"


def test_moderate_vehicle_produces_review_signals() -> None:
    vehicle = provider.get_vehicle_by_registration("TS 09 PQ 7316")

    assert vehicle is not None

    evidence = build_evidence(vehicle)

    evidence_by_id = {item.id: item for item in evidence}

    assert evidence_by_id["puc-status"].value == "Expired"
    assert evidence_by_id["puc-status"].status == "partially_verified"

    assert evidence_by_id["accident-history"].status == "partially_verified"

    assert evidence_by_id["challan-status"].status == "verified"


def test_high_risk_vehicle_detects_odometer_conflict() -> None:
    vehicle = provider.get_vehicle_by_registration("MH 12 XY 9087")

    assert vehicle is not None

    evidence = build_evidence(vehicle)

    evidence_by_id = {item.id: item for item in evidence}

    mileage = evidence_by_id["mileage-consistency"]

    assert mileage.status == "conflicting"
    assert mileage.confidence == "high"
    assert "67,300 km" in mileage.value
    assert "52,100 km" in mileage.value


def test_high_risk_vehicle_detects_major_accident() -> None:
    vehicle = provider.get_vehicle_by_registration("MH 12 XY 9087")

    assert vehicle is not None

    evidence = build_evidence(vehicle)

    evidence_by_id = {item.id: item for item in evidence}

    accident = evidence_by_id["accident-history"]

    assert accident.status == "conflicting"
    assert accident.confidence == "high"


def test_high_risk_vehicle_detects_open_challans() -> None:
    vehicle = provider.get_vehicle_by_registration("MH 12 XY 9087")

    assert vehicle is not None

    evidence = build_evidence(vehicle)

    evidence_by_id = {item.id: item for item in evidence}

    challans = evidence_by_id["challan-status"]

    assert challans.status == "partially_verified"
    assert "2 open challan(s)" in challans.value
