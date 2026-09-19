import os

from fastapi import APIRouter

from app.domain.factory import (
    build_local_ai_service,
    build_ollama_ai_service,
)
from app.schemas.contracts import AIRequest, AIResponse


router = APIRouter(
    prefix="/api/v1/ai",
    tags=["ai"],
)


def _build_configured_ai_service():
    """Build the AI service selected by application configuration."""

    provider = os.getenv(
        "AI_PROVIDER",
        "deterministic",
    ).strip().lower()

    if provider == "deterministic":
        return build_local_ai_service()

    if provider == "ollama":
        return build_ollama_ai_service(
            base_url=os.getenv(
                "OLLAMA_BASE_URL",
                "http://127.0.0.1:11434",
            ),
            model=os.getenv(
                "OLLAMA_MODEL",
                "qwen3:8b",
            ),
            timeout=float(
                os.getenv(
                    "OLLAMA_TIMEOUT",
                    "120",
                )
            ),
            think=os.getenv(
                "OLLAMA_THINK",
                "false",
            ).strip().lower()
            in {"1", "true", "yes", "on"},
        )

    raise ValueError(
        f"Unsupported AI_PROVIDER: {provider!r}. "
        "Supported providers: deterministic, ollama."
    )


_ai_service = _build_configured_ai_service()


@router.post(
    "/interpret",
    response_model=AIResponse,
)
def interpret_vehicle(request: AIRequest) -> AIResponse:
    """Generate a grounded AI interpretation for vehicle intelligence."""

    return _ai_service.interpret(request)