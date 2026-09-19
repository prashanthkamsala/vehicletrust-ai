from abc import ABC, abstractmethod


class LLMClient(ABC):
    """Provider-neutral interface for text generation."""

    @abstractmethod
    def generate(
        self,
        prompt: str,
        *,
        response_format: dict | str | None = None,
    ) -> str:
        """Generate text from the supplied prompt."""
        raise NotImplementedError