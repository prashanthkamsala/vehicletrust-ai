from app.providers.base import VehicleDataProvider
from app.providers.contracts import ProviderResult, ProviderStatus
from app.schemas.vehicle.models import (
    AccidentRecord,
    ChallanRecord,
    EvidenceSource,
    FinanceDetails,
    InsuranceDetails,
    ManufacturerDetails,
    OdometerRecord,
    OwnershipRecord,
    PucDetails,
    ServiceRecord,
    VehicleData,
    VehicleRegistration,
)


class MockIndiaProvider(VehicleDataProvider):
    """Synthetic Indian vehicle data provider for local development."""

    def __init__(self) -> None:
        self._vehicles = self._build_vehicles()

    def get_vehicle_by_registration(
        self,
        registration: str,
    ) -> ProviderResult:
        normalized_registration = " ".join(
            registration.strip().upper().split()
        )

        vehicle = self._vehicles.get(normalized_registration)

        if vehicle is None:
            return ProviderResult(
                status=ProviderStatus.NOT_FOUND,
                message="Vehicle was not found for the supplied registration.",
            )

        return ProviderResult(
            status=ProviderStatus.FOUND,
            vehicle=vehicle,
        )

    def _build_vehicles(self) -> dict[str, VehicleData]:
        return {
            "KA 05 MN 4821": self._build_clean_vehicle(),
            "TS 09 PQ 7316": self._build_moderate_risk_vehicle(),
            "MH 12 XY 9087": self._build_high_risk_vehicle(),
        }

    @staticmethod
    def _build_clean_vehicle() -> VehicleData:
        registration_source = EvidenceSource(
            id="mock-rto-clean",
            name="Mock RTO Registry",
            type="government_registry",
        )

        service_source = EvidenceSource(
            id="mock-service-clean",
            name="Mock Service Network",
            type="service_network",
        )

        manufacturer_source = EvidenceSource(
            id="mock-oem-clean",
            name="Mock OEM Registry",
            type="manufacturer",
        )

        return VehicleData(
            registration=VehicleRegistration(
                registration_number="KA 05 MN 4821",
                registration_date="2021-06-18",
                registering_authority="Bengaluru Central RTO",
                state="Karnataka",
                status="active",
            ),
            ownership=[
                OwnershipRecord(
                    owner_sequence=1,
                    ownership_type="individual",
                    start_date="2021-06-18",
                    end_date=None,
                    source=registration_source,
                ),
            ],
            insurance=InsuranceDetails(
                status="active",
                policy_type="comprehensive",
                provider="Mock General Insurance",
                policy_number="MOCK-INS-10001",
                start_date="2026-06-01",
                expiry_date="2027-05-31",
            ),
            puc=PucDetails(
                status="valid",
                certificate_number="PUC-KA-10001",
                issue_date="2026-05-20",
                expiry_date="2027-05-19",
                emission_norm="BS-VI",
            ),
            finance=FinanceDetails(
                status="closed",
                financier="Mock Bank",
                start_date="2021-06-20",
                closure_date="2025-05-15",
            ),
            service_history=[
                ServiceRecord(
                    id="service-clean-001",
                    service_date="2022-06-10",
                    odometer_km=9800,
                    service_type="scheduled_service",
                    service_center="Mock Bengaluru Service Centre",
                    description="First scheduled service.",
                ),
                ServiceRecord(
                    id="service-clean-002",
                    service_date="2023-06-15",
                    odometer_km=21400,
                    service_type="scheduled_service",
                    service_center="Mock Bengaluru Service Centre",
                    description="Routine annual service.",
                ),
                ServiceRecord(
                    id="service-clean-003",
                    service_date="2024-06-20",
                    odometer_km=33700,
                    service_type="scheduled_service",
                    service_center="Mock Bengaluru Service Centre",
                    description="Routine annual service.",
                ),
                ServiceRecord(
                    id="service-clean-004",
                    service_date="2025-06-25",
                    odometer_km=46100,
                    service_type="scheduled_service",
                    service_center="Mock Bengaluru Service Centre",
                    description="Routine annual service.",
                ),
            ],
            odometer_history=[
                OdometerRecord(
                    observed_at="2022-06-10",
                    odometer_km=9800,
                    source=service_source,
                ),
                OdometerRecord(
                    observed_at="2023-06-15",
                    odometer_km=21400,
                    source=service_source,
                ),
                OdometerRecord(
                    observed_at="2024-06-20",
                    odometer_km=33700,
                    source=service_source,
                ),
                OdometerRecord(
                    observed_at="2025-06-25",
                    odometer_km=46100,
                    source=service_source,
                ),
            ],
            accident_history=[],
            challans=[],
            manufacturer=ManufacturerDetails(
                manufacturer="Toyota",
                model="Camry",
                variant="2.5 Hybrid",
                fuel_type="hybrid",
                transmission="automatic",
                manufacturing_date="2021-04-01",
                warranty_status="expired",
            ),
        )

    @staticmethod
    def _build_moderate_risk_vehicle() -> VehicleData:
        registration_source = EvidenceSource(
            id="mock-rto-moderate",
            name="Mock RTO Registry",
            type="government_registry",
        )

        service_source = EvidenceSource(
            id="mock-service-moderate",
            name="Mock Service Network",
            type="service_network",
        )

        accident_source = EvidenceSource(
            id="mock-insurance-moderate",
            name="Mock Insurance Claims",
            type="insurance_claims",
        )

        return VehicleData(
            registration=VehicleRegistration(
                registration_number="TS 09 PQ 7316",
                registration_date="2020-11-04",
                registering_authority="Hyderabad Central RTO",
                state="Telangana",
                status="active",
            ),
            ownership=[
                OwnershipRecord(
                    owner_sequence=1,
                    ownership_type="individual",
                    start_date="2020-11-04",
                    end_date="2024-02-12",
                    source=registration_source,
                ),
                OwnershipRecord(
                    owner_sequence=2,
                    ownership_type="individual",
                    start_date="2024-02-12",
                    end_date=None,
                    source=registration_source,
                ),
            ],
            insurance=InsuranceDetails(
                status="active",
                policy_type="third_party",
                provider="Mock General Insurance",
                policy_number="MOCK-INS-20001",
                start_date="2026-03-01",
                expiry_date="2027-02-28",
            ),
            puc=PucDetails(
                status="expired",
                certificate_number="PUC-TS-20001",
                issue_date="2025-01-10",
                expiry_date="2026-01-09",
                emission_norm="BS-VI",
            ),
            finance=FinanceDetails(
                status="closed",
                financier="Mock Finance Ltd",
                start_date="2020-11-10",
                closure_date="2024-08-19",
            ),
            service_history=[
                ServiceRecord(
                    id="service-moderate-001",
                    service_date="2022-01-14",
                    odometer_km=14200,
                    service_type="scheduled_service",
                    service_center="Mock Hyderabad Service Centre",
                    description="Routine service.",
                ),
                ServiceRecord(
                    id="service-moderate-002",
                    service_date="2023-07-22",
                    odometer_km=29600,
                    service_type="scheduled_service",
                    service_center="Independent Service Centre",
                    description="Routine service.",
                ),
                ServiceRecord(
                    id="service-moderate-003",
                    service_date="2025-03-18",
                    odometer_km=54800,
                    service_type="repair",
                    service_center="Independent Service Centre",
                    description="Brake and suspension repairs.",
                ),
            ],
            odometer_history=[
                OdometerRecord(
                    observed_at="2022-01-14",
                    odometer_km=14200,
                    source=service_source,
                ),
                OdometerRecord(
                    observed_at="2023-07-22",
                    odometer_km=29600,
                    source=service_source,
                ),
                OdometerRecord(
                    observed_at="2025-03-18",
                    odometer_km=54800,
                    source=service_source,
                ),
                OdometerRecord(
                    observed_at="2026-02-10",
                    odometer_km=62100,
                    source=service_source,
                ),
            ],
            accident_history=[
                AccidentRecord(
                    id="accident-moderate-001",
                    date="2024-09-03",
                    severity="moderate",
                    description="Front-end collision claim with bumper and headlamp replacement.",
                    source=accident_source,
                ),
            ],
            challans=[
                ChallanRecord(
                    id="challan-moderate-001",
                    date="2025-11-17",
                    status="paid",
                    amount=1000,
                    description="Traffic violation.",
                    source=registration_source,
                ),
            ],
            manufacturer=ManufacturerDetails(
                manufacturer="Hyundai",
                model="Creta",
                variant="SX",
                fuel_type="petrol",
                transmission="manual",
                manufacturing_date="2020-08-01",
                warranty_status="expired",
            ),
        )

    @staticmethod
    def _build_high_risk_vehicle() -> VehicleData:
        registration_source = EvidenceSource(
            id="mock-rto-high",
            name="Mock RTO Registry",
            type="government_registry",
        )

        service_source = EvidenceSource(
            id="mock-service-high",
            name="Mock Service Network",
            type="service_network",
        )

        accident_source = EvidenceSource(
            id="mock-insurance-high",
            name="Mock Insurance Claims",
            type="insurance_claims",
        )

        return VehicleData(
            registration=VehicleRegistration(
                registration_number="MH 12 XY 9087",
                registration_date="2019-02-21",
                registering_authority="Pune RTO",
                state="Maharashtra",
                status="active",
            ),
            ownership=[
                OwnershipRecord(
                    owner_sequence=1,
                    ownership_type="individual",
                    start_date="2019-02-21",
                    end_date="2021-10-08",
                    source=registration_source,
                ),
                OwnershipRecord(
                    owner_sequence=2,
                    ownership_type="individual",
                    start_date="2021-10-08",
                    end_date="2023-04-14",
                    source=registration_source,
                ),
                OwnershipRecord(
                    owner_sequence=3,
                    ownership_type="individual",
                    start_date="2023-04-14",
                    end_date=None,
                    source=registration_source,
                ),
            ],
            insurance=InsuranceDetails(
                status="expired",
                policy_type="comprehensive",
                provider="Mock General Insurance",
                policy_number="MOCK-INS-30001",
                start_date="2024-01-01",
                expiry_date="2025-12-31",
            ),
            puc=PucDetails(
                status="expired",
                certificate_number="PUC-MH-30001",
                issue_date="2024-01-05",
                expiry_date="2025-01-04",
                emission_norm="BS-IV",
            ),
            finance=FinanceDetails(
                status="active",
                financier="Mock Finance Ltd",
                start_date="2023-05-01",
                closure_date=None,
            ),
            service_history=[
                ServiceRecord(
                    id="service-high-001",
                    service_date="2021-06-10",
                    odometer_km=42100,
                    service_type="scheduled_service",
                    service_center="Mock Pune Service Centre",
                    description="Routine service.",
                ),
                ServiceRecord(
                    id="service-high-002",
                    service_date="2022-11-18",
                    odometer_km=67300,
                    service_type="repair",
                    service_center="Independent Service Centre",
                    description="Major mechanical repair.",
                ),
                ServiceRecord(
                    id="service-high-003",
                    service_date="2024-02-15",
                    odometer_km=52100,
                    service_type="repair",
                    service_center="Independent Service Centre",
                    description="Odometer reading is lower than the previous service record.",
                ),
            ],
            odometer_history=[
                OdometerRecord(
                    observed_at="2021-06-10",
                    odometer_km=42100,
                    source=service_source,
                ),
                OdometerRecord(
                    observed_at="2022-11-18",
                    odometer_km=67300,
                    source=service_source,
                ),
                OdometerRecord(
                    observed_at="2024-02-15",
                    odometer_km=52100,
                    source=service_source,
                ),
                OdometerRecord(
                    observed_at="2025-10-12",
                    odometer_km=58900,
                    source=service_source,
                ),
            ],
            accident_history=[
                AccidentRecord(
                    id="accident-high-001",
                    date="2023-08-27",
                    severity="major",
                    description="Major collision claim involving front and side body panels.",
                    source=accident_source,
                ),
            ],
            challans=[
                ChallanRecord(
                    id="challan-high-001",
                    date="2025-07-14",
                    status="open",
                    amount=5000,
                    description="Outstanding traffic violation.",
                    source=registration_source,
                ),
                ChallanRecord(
                    id="challan-high-002",
                    date="2025-09-02",
                    status="open",
                    amount=2000,
                    description="Outstanding traffic violation.",
                    source=registration_source,
                ),
            ],
            manufacturer=ManufacturerDetails(
                manufacturer="Honda",
                model="City",
                variant="VX",
                fuel_type="petrol",
                transmission="manual",
                manufacturing_date="2018-12-01",
                warranty_status="expired",
            ),
        )
