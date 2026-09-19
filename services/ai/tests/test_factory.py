from app.domain.factory import (
    build_local_ai_service,
    build_ollama_ai_service,
)
from app.generation.deterministic import DeterministicGenerator
from app.generation.llm import LLMGenerator
from app.generation.providers.ollama import OllamaClient


def test_build_local_ai_service_uses_deterministic_generator() -> None:
    service = build_local_ai_service()

    assert isinstance(service.generator, DeterministicGenerator)


def test_build_ollama_ai_service_uses_ollama_generator() -> None:
    service = build_ollama_ai_service(
        model="test-model",
        think=False,
    )

    assert isinstance(service.generator, LLMGenerator)
    assert isinstance(service.generator.client, OllamaClient)
    assert service.generator.client.model == "test-model"
    assert service.generator.client.think is False