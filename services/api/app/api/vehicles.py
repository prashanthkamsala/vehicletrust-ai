from fastapi import APIRouter, HTTPException, Query

from app.domain.vehicle_service import get_vehicle, get_vehicle_by_registration
from app.schemas.vehicle.models import VehicleIntelligence

router = APIRouter(
    prefix="/api/v1/vehicles",
    tags=["vehicles"],
)


@router.get(
    "/lookup",
    response_model=VehicleIntelligence,
)
def lookup_vehicle(
    registration: str = Query(min_length=1),
) -> VehicleIntelligence:
    vehicle = get_vehicle_by_registration(registration)

    if vehicle is None:
        raise HTTPException(
            status_code=404,
            detail=f'Vehicle with registration "{registration}" not found.',
        )

    return vehicle


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