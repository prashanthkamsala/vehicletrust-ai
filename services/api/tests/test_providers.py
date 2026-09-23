from app.providers.contracts import ProviderStatus
from app.providers.mock_india import MockIndiaProvider


def test_mock_provider_returns_clean_vehicle() -> None:
    provider = MockIndiaProvider()

    result = provider.get_vehicle_by_registration("KA 05 MN 4821")

    assert result.status is ProviderStatus.FOUND
    assert result.is_success
    assert result.vehicle is not None

    vehicle = result.vehicle

    assert vehicle.registration is not None
    assert vehicle.registration.registration_number == "KA 05 MN 4821"
    assert vehicle.manufacturer is not None
    assert vehicle.manufacturer.manufacturer == "Toyota"
    assert len(vehicle.ownership) == 1
    assert len(vehicle.service_history) == 4


def test_mock_provider_normalizes_registration() -> None:
    provider = MockIndiaProvider()

    result = provider.get_vehicle_by_registration("ka 05 mn 4821")

    assert result.status is ProviderStatus.FOUND
    assert result.vehicle is not None
    assert result.vehicle.registration is not None
    assert result.vehicle.registration.registration_number == "KA 05 MN 4821"


def test_mock_provider_returns_moderate_risk_vehicle() -> None:
    provider = MockIndiaProvider()

    result = provider.get_vehicle_by_registration("TS 09 PQ 7316")

    assert result.status is ProviderStatus.FOUND
    assert result.vehicle is not None

    vehicle = result.vehicle

    assert len(vehicle.ownership) == 2
    assert vehicle.insurance is not None
    assert vehicle.insurance.status == "active"
    assert vehicle.puc is not None
    assert vehicle.puc.status == "expired"
    assert len(vehicle.accident_history) == 1


def test_mock_provider_returns_high_risk_vehicle() -> None:
    provider = MockIndiaProvider()

    result = provider.get_vehicle_by_registration("MH 12 XY 9087")

    assert result.status is ProviderStatus.FOUND
    assert result.vehicle is not None

    vehicle = result.vehicle

    assert len(vehicle.ownership) == 3
    assert vehicle.finance is not None
    assert vehicle.finance.status == "active"
    assert vehicle.insurance is not None
    assert vehicle.insurance.status == "expired"
    assert len(vehicle.accident_history) == 1
    assert len(vehicle.challans) == 2


def test_mock_provider_returns_not_found_for_unknown_registration() -> None:
    provider = MockIndiaProvider()

    result = provider.get_vehicle_by_registration("KA 00 ZZ 0000")

    assert result.status is ProviderStatus.NOT_FOUND
    assert not result.is_success
    assert result.vehicle is None
    assert result.message is not None
