from abc import ABC, abstractmethod

from app.providers.contracts import ProviderResult


class VehicleDataProvider(ABC):
    """Contract for vehicle data providers."""

    @abstractmethod
    def get_vehicle_by_registration(
        self,
        registration: str,
    ) -> ProviderResult:
        """Return a normalized provider result for a registration number."""
        raise NotImplementedError
