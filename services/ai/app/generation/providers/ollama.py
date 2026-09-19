from typing import Any

import httpx

from app.generation.providers.base import LLMClient


class OllamaClient(LLMClient):
    """LLM client for a local Ollama server."""

    def __init__(
        self,
        *,
        base_url: str = "http://127.0.0.1:11434",
        model: str = "qwen3:8b",
        timeout: float = 120.0,
        think: bool = False,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout
        self.think = think

    def generate(
        self,
        prompt: str,
        *,
        response_format: dict | str | None = None,
    ) -> str:
        payload: dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "think": self.think,
        }

        if response_format is not None:
            payload["format"] = response_format

        response = httpx.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()

        result: dict[str, Any] = response.json()
        generated_text = result.get("response")

        if not isinstance(generated_text, str):
            raise ValueError(
                "Ollama response did not contain a valid 'response' field."
            )

        return generated_text