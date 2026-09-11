from abc import ABC, abstractmethod

from app.schemas.vehicle.models import VehicleData


class VehicleDataProvider(ABC):
    """Contract for vehicle data providers."""

    @abstractmethod
    def get_vehicle_by_registration(
        self,
        registration: str,
    ) -> VehicleData | None:
        """Return vehicle data for a registration number."""
        raise NotImplementedError
