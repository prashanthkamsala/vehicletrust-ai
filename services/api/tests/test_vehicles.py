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


def test_get_unknown_vehicle_returns_404() -> None:
    response = client.get("/api/v1/vehicles/unknown-vehicle")

    assert response.status_code == 404
    assert response.json() == {
        "detail": 'Vehicle "unknown-vehicle" not found.'
    }