from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.vehicles import router as vehicles_router


app = FastAPI(
    title="VehicleTrust AI API",
    description="Backend API for evidence-backed vehicle intelligence.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "vehicletrust-api",
    }


app.include_router(vehicles_router)