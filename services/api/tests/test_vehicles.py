from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_demo_vehicle() -> None:
    response = client.get("/api/v1/vehicles/demo-vehicle")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == "demo-vehicle"

    assert data["identity"]["make"] == "Toyota"
    assert data["identity"]["model"] == "Camry"
    assert data["identity"]["year"] == 2021

    assert len(data["evidence"]) == 4
    assert len(data["risks"]) == 1

    assert data["trust"]["baseScore"] == 35
    assert data["trust"]["score"] == 87

    assert data["trust"]["factors"][0]["evidenceIds"] == [
        "ownership-history"
    ]

    assert data["risks"][0]["recommendedAction"] == (
        "Request the latest service invoices and maintenance records before purchase."
    )


def test_demo_vehicle_contains_traceable_risk() -> None:
    response = client.get("/api/v1/vehicles/demo-vehicle")

    assert response.status_code == 200

    data = response.json()

    evidence_ids = {
        evidence["id"]
        for evidence in data["evidence"]
    }

    for risk in data["risks"]:
        for evidence_id in risk["evidenceIds"]:
            assert evidence_id in evidence_ids


def test_lookup_clean_vehicle() -> None:
    response = client.get(
        "/api/v1/vehicles/lookup",
        params={"registration": "KA 05 MN 4821"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["identity"]["make"] == "Toyota"
    assert data["identity"]["model"] == "Camry"
    assert data["identity"]["registration"] == "KA 05 MN 4821"

    assert data["data"]["registration"]["status"] == "active"
    assert len(data["data"]["ownership"]) == 1
    assert data["data"]["insurance"]["status"] == "active"
    assert data["data"]["puc"]["status"] == "valid"
    assert data["data"]["finance"]["status"] == "closed"

    assert len(data["data"]["serviceHistory"]) == 4
    assert len(data["data"]["accidentHistory"]) == 0
    assert len(data["data"]["challans"]) == 0


def test_lookup_moderate_risk_vehicle() -> None:
    response = client.get(
        "/api/v1/vehicles/lookup",
        params={"registration": "TS 09 PQ 7316"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["identity"]["make"] == "Hyundai"
    assert data["identity"]["model"] == "Creta"
    assert data["identity"]["registration"] == "TS 09 PQ 7316"

    assert len(data["data"]["ownership"]) == 2
    assert data["data"]["insurance"]["status"] == "active"
    assert data["data"]["puc"]["status"] == "expired"
    assert data["data"]["finance"]["status"] == "closed"

    assert len(data["data"]["accidentHistory"]) == 1
    assert data["data"]["accidentHistory"][0]["severity"] == "moderate"

    assert len(data["data"]["challans"]) == 1
    assert data["data"]["challans"][0]["status"] == "paid"


def test_lookup_high_risk_vehicle() -> None:
    response = client.get(
        "/api/v1/vehicles/lookup",
        params={"registration": "MH 12 XY 9087"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["identity"]["make"] == "Honda"
    assert data["identity"]["model"] == "City"
    assert data["identity"]["registration"] == "MH 12 XY 9087"

    assert len(data["data"]["ownership"]) == 3
    assert data["data"]["insurance"]["status"] == "expired"
    assert data["data"]["puc"]["status"] == "expired"
    assert data["data"]["finance"]["status"] == "active"

    assert len(data["data"]["accidentHistory"]) == 1
    assert data["data"]["accidentHistory"][0]["severity"] == "major"

    assert len(data["data"]["challans"]) == 2

    odometer_history = data["data"]["odometerHistory"]

    assert odometer_history[0]["odometerKm"] < odometer_history[1]["odometerKm"]
    assert odometer_history[2]["odometerKm"] < odometer_history[1]["odometerKm"]


def test_lookup_normalizes_registration() -> None:
    response = client.get(
        "/api/v1/vehicles/lookup",
        params={"registration": "ka 05 mn 4821"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["identity"]["registration"] == "KA 05 MN 4821"


def test_lookup_unknown_registration_returns_404() -> None:
    response = client.get(
        "/api/v1/vehicles/lookup",
        params={"registration": "KA 00 ZZ 0000"},
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": 'Vehicle with registration "KA 00 ZZ 0000" not found.'
    }


def test_get_unknown_vehicle_returns_404() -> None:
    response = client.get("/api/v1/vehicles/unknown-vehicle")

    assert response.status_code == 404

    assert response.json() == {
        "detail": 'Vehicle "unknown-vehicle" not found.'
    }