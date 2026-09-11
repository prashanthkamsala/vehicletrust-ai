from app.schemas.vehicle.models import (
    AIInterpretation,
    EvidenceItem,
    EvidenceSource,
    RiskItem,
    TrustAssessment,
    TrustFactor,
    VehicleIdentity,
    VehicleIntelligence,
)


def get_vehicle(vehicle_id: str) -> VehicleIntelligence | None:
    if vehicle_id != "demo-vehicle":
        return None

    evidence = [
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
            observed_at="2026-09-10",
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
            observed_at="2026-09-10",
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
            observed_at="2026-09-10",
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
            observed_at="2026-09-10",
        ),
    ]

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
        risks=[
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
        ],
        trust=TrustAssessment(
            base_score=35,
            score=87,
            confidence="high",
            assessment="Low-risk profile",
            factors=factors,
        ),
        ai=AIInterpretation(
            summary=(
                "The available evidence indicates a relatively low-risk vehicle."
            ),
            reasoning=(
                "Ownership and accident indicators look healthy. Mileage "
                "records are consistent, while the service history contains "
                "a signal that deserves additional verification."
            ),
            recommendation=(
                "Proceed with additional service-history verification before "
                "making a purchase decision."
            ),
        ),
    )
