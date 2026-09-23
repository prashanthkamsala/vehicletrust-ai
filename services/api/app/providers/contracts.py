from dataclasses import dataclass
from enum import Enum

from app.schemas.vehicle.models import VehicleData


class ProviderStatus(str, Enum):
    FOUND = "found"
    NOT_FOUND = "not_found"
    UNAVAILABLE = "unavailable"
    TIMEOUT = "timeout"
    INVALID_RESPONSE = "invalid_response"


@dataclass(frozen=True)
class ProviderResult:
    status: ProviderStatus
    vehicle: VehicleData | None = None
    message: str | None = None

    @property
    def is_success(self) -> bool:
        return self.status is ProviderStatus.FOUND and self.vehicle is not None
