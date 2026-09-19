from fastapi.testclient import TestClient
import pytest

from app.api.ai import _build_configured_ai_service
from app.main import app
from tests.test_ai_integration import build_honda_high_risk_request
from app.generation.providers.ollama import OllamaClient
from app.generation.llm import LLMGenerator

client = TestClient(app)


def test_interpret_endpoint_returns_grounded_ai_response() -> None:
    request = build_honda_high_risk_request()

    response = client.post(
        "/api/v1/ai/interpret",
        json=request.model_dump(),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["summary"]
    assert data["reasoning"]
    assert data["recommendation"]

    assert data["supporting_evidence_ids"] == [
        "mileage-consistency",
        "accident-history",
    ]

    knowledge_ids = {
        reference["id"]
        for reference in data["knowledge_references"]
    }

    assert "odometer" in knowledge_ids
    assert "accident" in knowledge_ids

    assert data["grounding"]["status"] == "grounded"
    assert data["grounding"]["evidence_count"] == 2
    assert data["grounding"]["knowledge_count"] >= 2


def test_configured_ai_service_defaults_to_deterministic(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("AI_PROVIDER", raising=False)

    service = _build_configured_ai_service()

    assert service.generator.__class__.__name__ == "DeterministicGenerator"


def test_configured_ai_service_supports_deterministic_provider(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("AI_PROVIDER", "deterministic")

    service = _build_configured_ai_service()

    assert service.generator.__class__.__name__ == "DeterministicGenerator"


def test_configured_ai_service_supports_ollama_provider(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("AI_PROVIDER", "ollama")

    service = _build_configured_ai_service()

    assert service.generator.__class__.__name__ == "LLMGenerator"
    assert service.generator.client.__class__.__name__ == "OllamaClient"


def test_configured_ai_service_rejects_unknown_provider(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("AI_PROVIDER", "unknown-provider")

    with pytest.raises(
        ValueError,
        match="Unsupported AI_PROVIDER",
    ):
        _build_configured_ai_service()


def test_configured_ai_service_passes_ollama_environment_configuration(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("AI_PROVIDER", "ollama")
    monkeypatch.setenv(
        "OLLAMA_BASE_URL",
        "http://localhost:9999/",
    )
    monkeypatch.setenv(
        "OLLAMA_MODEL",
        "test-model",
    )
    monkeypatch.setenv(
        "OLLAMA_TIMEOUT",
        "45",
    )
    monkeypatch.setenv(
        "OLLAMA_THINK",
        "true",
    )

    service = _build_configured_ai_service()

    assert isinstance(service.generator, LLMGenerator)

    client = service.generator.client

    assert isinstance(client, OllamaClient)
    assert client.base_url == "http://localhost:9999"
    assert client.model == "test-model"
    assert client.timeout == 45.0
    assert client.think is True