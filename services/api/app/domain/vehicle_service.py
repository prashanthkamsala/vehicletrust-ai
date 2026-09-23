from app.intelligence.ai.client import AIServiceClient
from app.intelligence.ai.request_builder import build_ai_request
from app.intelligence.evidence.engine import build_evidence
from app.intelligence.risk.engine import build_risks
from app.intelligence.trust.engine import build_trust_assessment
from app.intelligence.decision.engine import build_decision_assessment
from app.providers.mock_india import MockIndiaProvider
from app.schemas.vehicle.models import (
    AIInterpretation,
    EvidenceItem,
    EvidenceProvenance,
    EvidenceSource,
    RiskItem,
    TrustAssessment,
    TrustFactor,
    VehicleIdentity,
    VehicleIntelligence,
)

_provider = MockIndiaProvider()
_ai_client = AIServiceClient()


def get_vehicle(vehicle_id: str) -> VehicleIntelligence | None:
    if vehicle_id != "demo-vehicle":
        return None

    return _build_demo_vehicle()


def get_vehicle_by_registration(
    registration: str,
) -> VehicleIntelligence | None:
    vehicle = _build_vehicle_from_registration(registration)

    if vehicle is None:
        return None

    ai_request = build_ai_request(vehicle)
    ai = _ai_client.interpret(ai_request)

    vehicle.ai = ai

    return vehicle


def _build_vehicle_from_registration(
    registration: str,
) -> VehicleIntelligence | None:
    provider_result = _provider.get_vehicle_by_registration(registration)

    if not provider_result.is_success:
        return None

    vehicle_data = provider_result.vehicle

    if vehicle_data is None:
        return None

    if vehicle_data.registration is None:
        return None

    manufacturer = vehicle_data.manufacturer

    if manufacturer is None:
        return None

    evidence = build_evidence(vehicle_data)
    risks = build_risks(evidence)
    trust = build_trust_assessment(
        evidence=evidence,
        risks=risks,
    )
    decision = build_decision_assessment(
        risks=risks,
        trust=trust,
        evidence_count=len(evidence),
    )

    return VehicleIntelligence(
        id=(
            "vehicle-"
            f"{vehicle_data.registration.registration_number.replace(' ', '-').lower()}"
        ),
        identity=VehicleIdentity(
            make=manufacturer.manufacturer,
            model=manufacturer.model or "Unknown",
            year=_extract_year(manufacturer.manufacturing_date),
            registration=vehicle_data.registration.registration_number,
            vin=_build_mock_vin(
                manufacturer.manufacturer,
                manufacturer.model,
                vehicle_data.registration.registration_number,
            ),
        ),
        data=vehicle_data,
        evidence=evidence,
        risks=risks,
        trust=trust,
        decision=decision,
        ai=AIInterpretation(
            summary="",
            reasoning="",
            recommendation="",
            grounding={
                "status": "insufficient",
                "evidence_count": 0,
                "knowledge_count": 0,
            },
        ),
    )

def _build_demo_vehicle() -> VehicleIntelligence:
    evidence = _build_demo_evidence()
    risks = _build_demo_risks()
    trust = _build_demo_trust()
    decision = build_decision_assessment(
        risks=risks,
        trust=trust,
        evidence_count=len(evidence),
    )
    ai = _build_demo_ai()

    return VehicleIntelligence(
        id="demo-vehicle",
        identity=VehicleIdentity(
            make="Toyota",
            model="Camry",
            year=2021,
            registration="KA 01 AB 1234",
            vin="DEMO1TOYOTA2021CAMRY",
        ),
        evidence=evidence,
        risks=risks,
        trust=trust,
        decision=decision,
        ai=ai,
    )


def _build_demo_evidence() -> list[EvidenceItem]:
    return [
        EvidenceItem(
            id="ownership-history",
            category="Ownership",
            title="Ownership history",
            value="Strong",
            status="verified",
            confidence="high",
            explanation="Ownership records show a consistent vehicle history.",
            source=EvidenceSource(
                id="registration-records",
                name="Vehicle registration records",
                type="registration",
            ),
            provenance=EvidenceProvenance(
                observed_at="2026-09-10",
            ),
        ),
        EvidenceItem(
            id="accident-history",
            category="Accident",
            title="Accident signals",
            value="Clear",
            status="verified",
            confidence="high",
            explanation="No significant accident indicators were identified.",
            source=EvidenceSource(
                id="vehicle-history-records",
                name="Vehicle history records",
                type="vehicle_history",
            ),
            provenance=EvidenceProvenance(
                observed_at="2026-09-10",
            ),
        ),
        EvidenceItem(
            id="service-history",
            category="Maintenance",
            title="Service history",
            value="Review",
            status="partially_verified",
            confidence="medium",
            explanation="Some maintenance records require additional verification.",
            source=EvidenceSource(
                id="service-records",
                name="Service records",
                type="maintenance",
            ),
            provenance=EvidenceProvenance(
                observed_at="2026-09-10",
            ),
        ),
        EvidenceItem(
            id="mileage-consistency",
            category="Mileage",
            title="Mileage consistency",
            value="Verified",
            status="verified",
            confidence="high",
            explanation="Available mileage records appear consistent over time.",
            source=EvidenceSource(
                id="mileage-records",
                name="Mileage records",
                type="vehicle_history",
            ),
            provenance=EvidenceProvenance(
                observed_at="2026-09-10",
            ),
        ),
    ]


def _build_demo_risks() -> list[RiskItem]:
    return [
        RiskItem(
            id="service-history-review",
            category="Maintenance",
            title="Service history requires review",
            severity="medium",
            status="needs_review",
            confidence="medium",
            explanation=(
                "Some maintenance records are incomplete or require "
                "additional verification."
            ),
            evidence_ids=["service-history"],
            recommended_action=(
                "Request the latest service invoices and maintenance "
                "records before purchase."
            ),
        ),
    ]


def _build_demo_trust() -> TrustAssessment:
    factors = [
        TrustFactor(
            id="ownership-factor",
            name="Ownership history",
            impact="positive",
            contribution=20,
            evidence_ids=["ownership-history"],
        ),
        TrustFactor(
            id="accident-factor",
            name="Accident history",
            impact="positive",
            contribution=25,
            evidence_ids=["accident-history"],
        ),
        TrustFactor(
            id="service-factor",
            name="Service history",
            impact="negative",
            contribution=-8,
            evidence_ids=["service-history"],
        ),
        TrustFactor(
            id="mileage-factor",
            name="Mileage consistency",
            impact="positive",
            contribution=15,
            evidence_ids=["mileage-consistency"],
        ),
    ]

    return TrustAssessment(
        base_score=35,
        calculated_score=87,
        score=87,
        confidence="high",
        assessment="Low-risk profile",
        factors=factors,
    )


def _build_demo_ai() -> AIInterpretation:
    return AIInterpretation(
        summary=("The available evidence indicates a relatively low-risk vehicle."),
        reasoning=(
            "Ownership and accident indicators look healthy. Mileage "
            "records are consistent, while the service history contains "
            "a signal that deserves additional verification."
        ),
        recommendation=(
            "Proceed with additional service-history verification before "
            "making a purchase decision."
        ),
        supporting_evidence_ids=[
            "ownership-history",
            "mileage-consistency",
            "service-history",
        ],
        knowledge_references=[],
        grounding={
            "status": "partially_grounded",
            "evidence_count": 3,
            "knowledge_count": 0,
        },
    )


def _extract_year(manufacturing_date: str | None) -> int:
    if not manufacturing_date:
        return 0

    try:
        return int(manufacturing_date[:4])
    except ValueError:
        return 0


def _build_mock_vin(
    manufacturer: str,
    model: str | None,
    registration: str,
) -> str:
    manufacturer_code = manufacturer.upper()[:3]
    model_code = (model or "VEHICLE").upper().replace(" ", "")[:6]
    registration_code = registration.replace(" ", "").upper()

    return f"MOCK{manufacturer_code}{model_code}{registration_code}"
