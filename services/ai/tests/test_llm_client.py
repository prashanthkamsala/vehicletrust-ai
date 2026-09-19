import pytest

from app.generation.providers.base import LLMClient


class FakeLLMClient(LLMClient):
    def generate(self, prompt: str) -> str:
        return f"generated: {prompt}"


def test_llm_client_can_be_implemented_by_a_provider():
    client = FakeLLMClient()

    result = client.generate("hello")

    assert result == "generated: hello"


def test_llm_client_cannot_be_instantiated_directly():
    with pytest.raises(TypeError):
        LLMClient()