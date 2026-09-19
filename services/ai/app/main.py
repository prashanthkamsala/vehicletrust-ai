from fastapi import FastAPI

from app.api.ai import router as ai_router


app = FastAPI(
    title="VehicleTrust AI Service",
    description="AI and RAG service for grounded vehicle intelligence.",
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "vehicletrust-ai",
    }


app.include_router(ai_router)