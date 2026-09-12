from app.schemas.vehicle.models import (
    EvidenceItem,
    EvidenceSource,
    VehicleData,
)


def build_evidence(vehicle_data: VehicleData) -> list[EvidenceItem]:
    """Build deterministic evidence from observed vehicle data."""

    evidence: list[EvidenceItem] = []

    _add_registration_evidence(evidence, vehicle_data)
    _add_ownership_evidence(evidence, vehicle_data)
    _add_insurance_evidence(evidence, vehicle_data)
    _add_puc_evidence(evidence, vehicle_data)
    _add_finance_evidence(evidence, vehicle_data)
    _add_service_evidence(evidence, vehicle_data)
    _add_odometer_evidence(evidence, vehicle_data)
    _add_accident_evidence(evidence, vehicle_data)
    _add_challan_evidence(evidence, vehicle_data)
    _add_manufacturer_evidence(evidence, vehicle_data)

    return evidence


def _add_registration_evidence(
    evidence: list[EvidenceItem],
    vehicle_data: VehicleData,
) -> None:
    registration = vehicle_data.registration

    if registration is None:
        evidence.append(
            EvidenceItem(
                id="registration-unavailable",
                category="Registration",
                title="Registration record",
                value="Not available",
                status="unverified",
                confidence="low",
                explanation="No registration record was available.",
                source=_source(
                    "registration-engine",
                    "Vehicle registration data",
                    "registration",
                ),
            )
        )
        return

    if registration.status == "active":
        status = "verified"
        confidence = "high"
        value = "Active"
        explanation = (
            "The vehicle has an active registration record."
        )
    elif registration.status in {"inactive", "suspended"}:
        status = "conflicting"
        confidence = "high"
        value = registration.status.capitalize()
        explanation = (
            f"The registration status is {registration.status} and "
            "requires verification before proceeding."
        )
    else:
        status = "unverified"
        confidence = "low"
        value = "Unknown"
        explanation = (
            "The registration record exists, but its current status "
            "could not be verified."
        )

    evidence.append(
        EvidenceItem(
            id="registration-status",
            category="Registration",
            title="Registration status",
            value=value,
            status=status,
            confidence=confidence,
            explanation=explanation,
            source=_source(
                "registration-engine",
                "Vehicle registration data",
                "registration",
            ),
            observed_at=registration.registration_date,
        )
    )


def _add_ownership_evidence(
    evidence: list[EvidenceItem],
    vehicle_data: VehicleData,
) -> None:
    ownership = vehicle_data.ownership

    if not ownership:
        evidence.append(
            EvidenceItem(
                id="ownership-history",
                category="Ownership",
                title="Ownership history",
                value="Not available",
                status="unverified",
                confidence="low",
                explanation="No ownership records were available.",
                source=_source(
                    "ownership-engine",
                    "Vehicle ownership data",
                    "registration",
                ),
            )
        )
        return

    owner_count = len(ownership)

    if owner_count == 1:
        status = "verified"
        confidence = "high"
        value = "1 owner"
        explanation = (
            "The available records show a single recorded owner."
        )
    elif owner_count == 2:
        status = "verified"
        confidence = "high"
        value = "2 owners"
        explanation = (
            "The available records show two recorded owners."
        )
    else:
        status = "partially_verified"
        confidence = "medium"
        value = f"{owner_count} owners"
        explanation = (
            f"The available records show {owner_count} owners. "
            "Ownership history should be reviewed in the context "
            "of the vehicle's age and usage."
        )

    source = ownership[0].source

    evidence.append(
        EvidenceItem(
            id="ownership-history",
            category="Ownership",
            title="Ownership history",
            value=value,
            status=status,
            confidence=confidence,
            explanation=explanation,
            source=source,
            observed_at=ownership[-1].start_date,
        )
    )


def _add_insurance_evidence(
    evidence: list[EvidenceItem],
    vehicle_data: VehicleData,
) -> None:
    insurance = vehicle_data.insurance

    if insurance is None:
        evidence.append(
            EvidenceItem(
                id="insurance-status",
                category="Insurance",
                title="Insurance status",
                value="Not available",
                status="unverified",
                confidence="low",
                explanation="No insurance record was available.",
                source=_source(
                    "insurance-engine",
                    "Vehicle insurance data",
                    "insurance",
                ),
            )
        )
        return

    if insurance.status == "active":
        status = "verified"
        confidence = "high"
        value = "Active"
        explanation = "The available insurance record is active."
    elif insurance.status == "expired":
        status = "partially_verified"
        confidence = "high"
        value = "Expired"
        explanation = (
            "The available insurance record has expired and should "
            "be renewed or verified before use."
        )
    else:
        status = "unverified"
        confidence = "low"
        value = "Unknown"
        explanation = (
            "The insurance record exists, but its current status "
            "could not be verified."
        )

    evidence.append(
        EvidenceItem(
            id="insurance-status",
            category="Insurance",
            title="Insurance status",
            value=value,
            status=status,
            confidence=confidence,
            explanation=explanation,
            source=_source(
                "insurance-engine",
                "Vehicle insurance data",
                "insurance",
            ),
            observed_at=insurance.expiry_date,
        )
    )


def _add_puc_evidence(
    evidence: list[EvidenceItem],
    vehicle_data: VehicleData,
) -> None:
    puc = vehicle_data.puc

    if puc is None:
        evidence.append(
            EvidenceItem(
                id="puc-status",
                category="Compliance",
                title="PUC status",
                value="Not available",
                status="unverified",
                confidence="low",
                explanation="No PUC record was available.",
                source=_source(
                    "puc-engine",
                    "Vehicle PUC data",
                    "compliance",
                ),
            )
        )
        return

    if puc.status == "valid":
        status = "verified"
        confidence = "high"
        value = "Valid"
        explanation = "The available PUC record is valid."
    elif puc.status == "expired":
        status = "partially_verified"
        confidence = "high"
        value = "Expired"
        explanation = (
            "The available PUC record has expired and requires "
            "renewal or verification."
        )
    elif puc.status == "not_available":
        status = "unverified"
        confidence = "low"
        value = "Not available"
        explanation = "No current PUC certificate was available."
    else:
        status = "unverified"
        confidence = "low"
        value = "Unknown"
        explanation = "The PUC status could not be verified."

    evidence.append(
        EvidenceItem(
            id="puc-status",
            category="Compliance",
            title="PUC status",
            value=value,
            status=status,
            confidence=confidence,
            explanation=explanation,
            source=_source(
                "puc-engine",
                "Vehicle PUC data",
                "compliance",
            ),
            observed_at=puc.expiry_date,
        )
    )


def _add_finance_evidence(
    evidence: list[EvidenceItem],
    vehicle_data: VehicleData,
) -> None:
    finance = vehicle_data.finance

    if finance is None:
        evidence.append(
            EvidenceItem(
                id="finance-status",
                category="Finance",
                title="Finance status",
                value="Not available",
                status="unverified",
                confidence="low",
                explanation="No finance record was available.",
                source=_source(
                    "finance-engine",
                    "Vehicle finance data",
                    "finance",
                ),
            )
        )
        return

    if finance.status == "closed":
        status = "verified"
        confidence = "high"
        value = "Closed"
        explanation = "The available finance record is closed."
    elif finance.status == "active":
        status = "partially_verified"
        confidence = "high"
        value = "Active"
        explanation = (
            "An active finance record exists. Loan closure and "
            "lien-release documentation should be verified."
        )
    else:
        status = "unverified"
        confidence = "low"
        value = "Unknown"
        explanation = "The finance status could not be verified."

    evidence.append(
        EvidenceItem(
            id="finance-status",
            category="Finance",
            title="Finance status",
            value=value,
            status=status,
            confidence=confidence,
            explanation=explanation,
            source=_source(
                "finance-engine",
                "Vehicle finance data",
                "finance",
            ),
            observed_at=finance.closure_date or finance.start_date,
        )
    )


def _add_service_evidence(
    evidence: list[EvidenceItem],
    vehicle_data: VehicleData,
) -> None:
    records = vehicle_data.service_history

    if not records:
        evidence.append(
            EvidenceItem(
                id="service-history",
                category="Maintenance",
                title="Service history",
                value="Not available",
                status="unverified",
                confidence="low",
                explanation="No service records were available.",
                source=_source(
                    "service-engine",
                    "Vehicle service data",
                    "maintenance",
                ),
            )
        )
        return

    records_with_odometer = [
        record for record in records if record.odometer_km is not None
    ]

    if len(records_with_odometer) == len(records):
        status = "verified"
        confidence = "high"
        value = f"{len(records)} records"
        explanation = (
            "Service records are available with odometer readings "
            "for the recorded maintenance events."
        )
    else:
        status = "partially_verified"
        confidence = "medium"
        value = f"{len(records)} records"
        explanation = (
            "Service records are available, but some records do not "
            "include odometer readings."
        )

    evidence.append(
        EvidenceItem(
            id="service-history",
            category="Maintenance",
            title="Service history",
            value=value,
            status=status,
            confidence=confidence,
            explanation=explanation,
            source=_source(
                "service-engine",
                "Vehicle service data",
                "maintenance",
            ),
            observed_at=records[-1].service_date,
        )
    )


def _add_odometer_evidence(
    evidence: list[EvidenceItem],
    vehicle_data: VehicleData,
) -> None:
    records = sorted(
        vehicle_data.odometer_history,
        key=lambda record: record.observed_at,
    )

    if not records:
        evidence.append(
            EvidenceItem(
                id="mileage-consistency",
                category="Mileage",
                title="Mileage consistency",
                value="Not available",
                status="unverified",
                confidence="low",
                explanation="No odometer records were available.",
                source=_source(
                    "odometer-engine",
                    "Vehicle mileage data",
                    "vehicle_history",
                ),
            )
        )
        return

    decreases = [
        (previous, current)
        for previous, current in zip(records, records[1:])
        if current.odometer_km < previous.odometer_km
    ]

    source = records[-1].source

    if decreases:
        previous, current = decreases[0]

        evidence.append(
            EvidenceItem(
                id="mileage-consistency",
                category="Mileage",
                title="Mileage consistency",
                value=(
                    f"Inconsistent: {previous.odometer_km:,} km to "
                    f"{current.odometer_km:,} km"
                ),
                status="conflicting",
                confidence="high",
                explanation=(
                    "A later odometer observation is lower than an "
                    "earlier recorded reading. The discrepancy requires "
                    "investigation and supporting documentation."
                ),
                source=source,
                observed_at=current.observed_at,
            )
        )
        return

    evidence.append(
        EvidenceItem(
            id="mileage-consistency",
            category="Mileage",
            title="Mileage consistency",
            value="Consistent",
            status="verified",
            confidence="high",
            explanation=(
                "The available odometer records increase consistently "
                "over time."
            ),
            source=source,
            observed_at=records[-1].observed_at,
        )
    )


def _add_accident_evidence(
    evidence: list[EvidenceItem],
    vehicle_data: VehicleData,
) -> None:
    accidents = vehicle_data.accident_history

    if not accidents:
        evidence.append(
            EvidenceItem(
                id="accident-history",
                category="Accident",
                title="Accident history",
                value="No recorded accidents",
                status="verified",
                confidence="medium",
                explanation=(
                    "No accident records were present in the available "
                    "data. This does not rule out incidents that were "
                    "not reported to the available sources."
                ),
                source=_source(
                    "accident-engine",
                    "Vehicle accident data",
                    "vehicle_history",
                ),
            )
        )
        return

    major_accidents = [
        accident
        for accident in accidents
        if accident.severity == "major"
    ]

    moderate_accidents = [
        accident
        for accident in accidents
        if accident.severity == "moderate"
    ]

    if major_accidents:
        status = "conflicting"
        confidence = "high"
        value = f"{len(accidents)} recorded accident(s)"
        explanation = (
            f"The available records contain {len(major_accidents)} "
            "major accident signal(s). The underlying claims and "
            "repair records should be reviewed."
        )
    elif moderate_accidents:
        status = "partially_verified"
        confidence = "high"
        value = f"{len(accidents)} recorded accident(s)"
        explanation = (
            "The available records contain moderate accident signals "
            "that should be reviewed with repair documentation."
        )
    else:
        status = "partially_verified"
        confidence = "medium"
        value = f"{len(accidents)} recorded accident(s)"
        explanation = (
            "The available records contain accident signals. "
            "Severity and repair impact should be verified."
        )

    evidence.append(
        EvidenceItem(
            id="accident-history",
            category="Accident",
            title="Accident history",
            value=value,
            status=status,
            confidence=confidence,
            explanation=explanation,
            source=accidents[0].source,
            observed_at=accidents[0].date,
        )
    )


def _add_challan_evidence(
    evidence: list[EvidenceItem],
    vehicle_data: VehicleData,
) -> None:
    challans = vehicle_data.challans

    if not challans:
        evidence.append(
            EvidenceItem(
                id="challan-status",
                category="Compliance",
                title="Traffic challans",
                value="No recorded challans",
                status="verified",
                confidence="medium",
                explanation=(
                    "No traffic challans were present in the available "
                    "data."
                ),
                source=_source(
                    "challan-engine",
                    "Vehicle challan data",
                    "compliance",
                ),
            )
        )
        return

    open_challans = [
        challan for challan in challans if challan.status == "open"
    ]

    if open_challans:
        total_amount = sum(
            challan.amount or 0 for challan in open_challans
        )

        evidence.append(
            EvidenceItem(
                id="challan-status",
                category="Compliance",
                title="Traffic challans",
                value=(
                    f"{len(open_challans)} open challan(s), "
                    f"₹{total_amount:,.0f}"
                ),
                status="partially_verified",
                confidence="high",
                explanation=(
                    "Open traffic challans are present in the available "
                    "records and should be resolved or verified before "
                    "purchase."
                ),
                source=open_challans[0].source,
                observed_at=open_challans[0].date,
            )
        )
        return

    evidence.append(
        EvidenceItem(
            id="challan-status",
            category="Compliance",
            title="Traffic challans",
            value=f"{len(challans)} recorded, none open",
            status="verified",
            confidence="medium",
            explanation=(
                "Recorded challans are present, but none are currently "
                "marked as open."
            ),
            source=challans[0].source,
            observed_at=challans[-1].date,
        )
    )


def _add_manufacturer_evidence(
    evidence: list[EvidenceItem],
    vehicle_data: VehicleData,
) -> None:
    manufacturer = vehicle_data.manufacturer

    if manufacturer is None:
        evidence.append(
            EvidenceItem(
                id="manufacturer-details",
                category="Manufacturer",
                title="Manufacturer details",
                value="Not available",
                status="unverified",
                confidence="low",
                explanation="No manufacturer record was available.",
                source=_source(
                    "manufacturer-engine",
                    "Manufacturer vehicle data",
                    "manufacturer",
                ),
            )
        )
        return

    model = manufacturer.model or "Unknown model"

    evidence.append(
        EvidenceItem(
            id="manufacturer-details",
            category="Manufacturer",
            title="Manufacturer details",
            value=f"{manufacturer.manufacturer} {model}",
            status="verified",
            confidence="high",
            explanation=(
                "Manufacturer and model information is available "
                "from the vehicle data provider."
            ),
            source=_source(
                "manufacturer-engine",
                "Manufacturer vehicle data",
                "manufacturer",
            ),
            observed_at=manufacturer.manufacturing_date,
        )
    )


def _source(source_id: str, name: str, source_type: str) -> EvidenceSource:
    return EvidenceSource(
        id=source_id,
        name=name,
        type=source_type,
    )
