import httpx
import pytest

from app.generation.providers.ollama import OllamaClient

def mock_response(status_code: int, *, json: dict) -> httpx.Response:
    request = httpx.Request(
        "POST",
        "http://127.0.0.1:11434/api/generate",
    )
    return httpx.Response(
        status_code,
        json=json,
        request=request,
    )


def test_ollama_client_sends_prompt_and_returns_generated_text(monkeypatch):
    captured: dict[str, object] = {}

    def mock_post(url, *, json, timeout):
        captured["url"] = url
        captured["json"] = json
        captured["timeout"] = timeout

        return mock_response(
            200,
            json={
                "model": "qwen3:8b",
                "response": "Vehicle trust depends on evidence.",
            },
        )

    monkeypatch.setattr(httpx, "post", mock_post)

    client = OllamaClient()

    result = client.generate("Explain vehicle trust.")

    assert result == "Vehicle trust depends on evidence."
    assert captured["url"] == "http://127.0.0.1:11434/api/generate"
    assert captured["json"] == {
        "model": "qwen3:8b",
        "prompt": "Explain vehicle trust.",
        "stream": False,
        "think": False,
    }
    assert captured["timeout"] == 120.0


def test_ollama_client_uses_custom_configuration(monkeypatch):
    captured: dict[str, object] = {}

    def mock_post(url, *, json, timeout):
        captured["url"] = url
        captured["json"] = json
        captured["timeout"] = timeout

        return mock_response(
            200,
            json={"response": "Generated response."},
        )

    monkeypatch.setattr(httpx, "post", mock_post)

    client = OllamaClient(
        base_url="http://localhost:9999/",
        model="test-model",
        timeout=30.0,
    )

    result = client.generate("Test prompt.")

    assert result == "Generated response."
    assert captured["url"] == "http://localhost:9999/api/generate"
    assert captured["json"] == {
        "model": "test-model",
        "prompt": "Test prompt.",
        "stream": False,
        "think": False,
    }
    assert captured["timeout"] == 30.0


def test_ollama_client_raises_for_http_errors(monkeypatch):
    def mock_post(url, *, json, timeout):
        return mock_response(
            500,
            json={"error": "model unavailable"},
        )

    monkeypatch.setattr(httpx, "post", mock_post)

    client = OllamaClient()

    with pytest.raises(httpx.HTTPStatusError):
        client.generate("Test prompt.")


def test_ollama_client_rejects_missing_response(monkeypatch):
    def mock_post(url, *, json, timeout):
        return mock_response(
            200,
            json={"model": "qwen3:8b"},
        )

    monkeypatch.setattr(httpx, "post", mock_post)

    client = OllamaClient()

    with pytest.raises(ValueError, match="valid 'response' field"):
        client.generate("Test prompt.")


def test_ollama_client_can_enable_thinking(monkeypatch):
    captured: dict[str, object] = {}

    def mock_post(url, *, json, timeout):
        captured["json"] = json

        return mock_response(
            200,
            json={"response": "Generated response."},
        )

    monkeypatch.setattr(httpx, "post", mock_post)

    client = OllamaClient(think=True)

    result = client.generate("Test prompt.")

    assert result == "Generated response."
    assert captured["json"] == {
        "model": "qwen3:8b",
        "prompt": "Test prompt.",
        "stream": False,
        "think": True,
    }

def test_ollama_client_can_request_json_format(monkeypatch):
    captured: dict[str, object] = {}

    def mock_post(url, *, json, timeout):
        captured["json"] = json

        return mock_response(
            200,
            json={"response": '{"summary":"Test"}'},
        )

    monkeypatch.setattr(httpx, "post", mock_post)

    client = OllamaClient()

    result = client.generate(
        "Return JSON.",
        response_format={"type": "json"},
    )

    assert result == '{"summary":"Test"}'
    assert captured["json"] == {
        "model": "qwen3:8b",
        "prompt": "Return JSON.",
        "stream": False,
        "think": False,
        "format": {"type": "json"},
    }