from fastapi import FastAPI

from app.api.vehicles import router as vehicles_router


app = FastAPI(
    title="VehicleTrust AI API",
    description="Backend API for evidence-backed vehicle intelligence.",
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "vehicletrust-api",
    }


app.include_router(vehicles_router)