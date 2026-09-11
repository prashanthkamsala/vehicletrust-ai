from fastapi import APIRouter, HTTPException

from app.domain.vehicle_service import get_vehicle
from app.schemas.vehicle.models import VehicleIntelligence


router = APIRouter(
    prefix="/api/v1/vehicles",
    tags=["vehicles"],
)


@router.get(
    "/{vehicle_id}",
    response_model=VehicleIntelligence,
)
def get_vehicle_by_id(vehicle_id: str) -> VehicleIntelligence:
    vehicle = get_vehicle(vehicle_id)

    if vehicle is None:
        raise HTTPException(
            status_code=404,
            detail=f'Vehicle "{vehicle_id}" not found.',
        )

    return vehicle