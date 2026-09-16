from app.schemas.vehicle.models import (
    EvidenceConfidence,
    EvidenceItem,
    EvidenceProvenance,
    EvidenceSource,
    VehicleData,
)


def build_evidence(vehicle_data: VehicleData) -> list[EvidenceItem]:
    """Build deterministic, evidence-backed signals from vehicle data."""

    evidence: list[EvidenceItem] = []

    _add_registration_evidence(evidence, vehicle_data)
    _add_ownership_evidence(evidence, vehicle_data)
    _add_insurance_evidence(evidence, vehicle_data)
    _add_puc_evidence(evidence, vehicle_data)
    _add_finance_evidence(evidence, vehicle_data)
    _add_service_history_evidence(evidence, vehicle_data)
    _add_odometer_evidence(evidence, vehicle_data)
    _add_accident_evidence(evidence, vehicle_data)
    _add_challan_evidence(evidence, vehicle_data)
    _add_manufacturer_evidence(evidence, vehicle_data)

    return evidence


def _source(
    source_id: str,
    name: str,
    source_type: str,
) -> EvidenceSource:
    return EvidenceSource(
        id=source_id,
        name=name,
        type=source_type,
    )


def _provenance(
    observed_at: str | None = None,
    retrieved_at: str | None = None,
    reference_id: str | None = None,
) -> EvidenceProvenance:
    return EvidenceProvenance(
        observed_at=observed_at,
        retrieved_at=retrieved_at,
        reference_id=reference_id,
    )


def _add_registration_evidence(
    evidence: list[EvidenceItem],
    vehicle_data: VehicleData,
) -> None:
    registration = vehicle_data.registration

    source = _source(
        "government-registry",
        "Government vehicle registry",
        "government_registry",
    )

    if registration is None:
        evidence.append(
            EvidenceItem(
                id="registration-status",
                category="Registration",
                title="Registration status",
                value="Not available",
                status="unverified",
                confidence="low",
                explanation="No registration record was available.",
                source=source,
                provenance=_provenance(),
            )
        )
        return

    if registration.status == "active":
        status = "verified"
        confidence: EvidenceConfidence = "high"
        value = "Active"
        explanation = "The vehicle registration is currently active."
    elif registration.status in {"inactive", "suspended"}:
        status = "conflicting"
        confidence = "high"
        value = registration.status.title()
        explanation = (
            "The vehicle registration is not currently active "
            "and requires verification."
        )
    else:
        status = "unverified"
        confidence = "low"
        value = "Unknown"
        explanation = (
            "The registration record exists, but its current "
            "status could not be verified."
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
            source=source,
            provenance=_provenance(
                observed_at=registration.registration_date,
            ),
        )
    )


def _add_ownership_evidence(
    evidence: list[EvidenceItem],
    vehicle_data: VehicleData,
) -> None:
    ownership = vehicle_data.ownership

    source = _source(
        "government-registry",
        "Government ownership records",
        "government_registry",
    )

    if not ownership:
        evidence.append(
            EvidenceItem(
                id="ownership-history",
                category="Ownership",
                title="Ownership history",
                value="Not available",
                status="unverified",
                confidence="low",
                explanation="No ownership history was available.",
                source=source,
                provenance=_provenance(),
            )
        )
        return

    owner_count = len(ownership)

    if owner_count == 1:
        status = "verified"
        confidence: EvidenceConfidence = "high"
        value = "1 owner"
        explanation = (
            "The available ownership history shows a single owner."
        )
    elif owner_count == 2:
        status = "verified"
        confidence = "high"
        value = "2 owners"
        explanation = (
            "The available ownership history shows two owners."
        )
    else:
        status = "partially_verified"
        confidence = "medium"
        value = f"{owner_count} owners"
        explanation = (
            "The vehicle has multiple owners in the available "
            "ownership history and the timeline should be reviewed."
        )

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
            provenance=_provenance(
                observed_at=ownership[-1].start_date,
            ),
        )
    )


def _add_insurance_evidence(
    evidence: list[EvidenceItem],
    vehicle_data: VehicleData,
) -> None:
    insurance = vehicle_data.insurance

    source = _source(
        "insurance-engine",
        "Vehicle insurance data",
        "insurance",
    )

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
                source=source,
                provenance=_provenance(),
            )
        )
        return

    if insurance.status == "active":
        status = "verified"
        confidence: EvidenceConfidence = "high"
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
            source=source,
            provenance=_provenance(
                observed_at=insurance.expiry_date,
            ),
        )
    )


def _add_puc_evidence(
    evidence: list[EvidenceItem],
    vehicle_data: VehicleData,
) -> None:
    puc = vehicle_data.puc

    source = _source(
        "government-registry",
        "Pollution certificate records",
        "government_registry",
    )

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
                source=source,
                provenance=_provenance(),
            )
        )
        return

    if puc.status == "valid":
        status = "verified"
        confidence: EvidenceConfidence = "high"
        value = "Valid"
        explanation = "The available PUC record is currently valid."
    elif puc.status == "expired":
        status = "partially_verified"
        confidence = "high"
        value = "Expired"
        explanation = (
            "The available PUC record has expired and should be renewed."
        )
    elif puc.status == "not_available":
        status = "unverified"
        confidence = "low"
        value = "Not available"
        explanation = "No current PUC certificate is available."
    else:
        status = "unverified"
        confidence = "low"
        value = "Unknown"
        explanation = (
            "A PUC record exists, but its current status "
            "could not be verified."
        )

    evidence.append(
        EvidenceItem(
            id="puc-status",
            category="Compliance",
            title="PUC status",
            value=value,
            status=status,
            confidence=confidence,
            explanation=explanation,
            source=source,
            provenance=_provenance(
                observed_at=puc.expiry_date,
            ),
        )
    )


def _add_finance_evidence(
    evidence: list[EvidenceItem],
    vehicle_data: VehicleData,
) -> None:
    finance = vehicle_data.finance

    source = _source(
        "finance-registry",
        "Vehicle finance records",
        "finance",
    )

    if finance is None:
        evidence.append(
            EvidenceItem(
                id="finance-status",
                category="Finance",
                title="Finance status",
                value="Not available",
                status="unverified",
                confidence="low",
                explanation=(
                    "No vehicle finance record was available."
                ),
                source=source,
                provenance=_provenance(),
            )
        )
        return

    if finance.status == "closed":
        status = "verified"
        confidence: EvidenceConfidence = "high"
        value = "Closed"
        explanation = (
            "The available finance record shows that financing is closed."
        )
        observed_at = finance.closure_date

    elif finance.status == "active":
        status = "partially_verified"
        confidence = "high"
        value = "Active"
        explanation = (
            "The vehicle has an active finance record and lender/lien "
            "details should be verified before purchase."
        )
        observed_at = finance.start_date

    else:
        status = "unverified"
        confidence = "low"
        value = "Unknown"
        explanation = (
            "A finance record exists, but its current status "
            "could not be verified."
        )
        observed_at = finance.start_date

    evidence.append(
        EvidenceItem(
            id="finance-status",
            category="Finance",
            title="Finance status",
            value=value,
            status=status,
            confidence=confidence,
            explanation=explanation,
            source=source,
            provenance=_provenance(
                observed_at=observed_at,
            ),
        )
    )


def _add_service_history_evidence(
    evidence: list[EvidenceItem],
    vehicle_data: VehicleData,
) -> None:
    service_history = vehicle_data.service_history

    source = _source(
        "service-history",
        "Vehicle service history",
        "service",
    )

    if not service_history:
        evidence.append(
            EvidenceItem(
                id="service-history",
                category="Service",
                title="Service history",
                value="No service records",
                status="unverified",
                confidence="low",
                explanation=(
                    "No service records were available for review."
                ),
                source=source,
                provenance=_provenance(),
            )
        )
        return

    has_complete_odometer = all(
        record.odometer_km is not None
        for record in service_history
    )

    if has_complete_odometer:
        status = "verified"
        confidence: EvidenceConfidence = "high"
        explanation = (
            "Service records are available with odometer observations."
        )
    else:
        status = "partially_verified"
        confidence = "medium"
        explanation = (
            "Service records are available, but some records do not "
            "contain odometer observations."
        )

    evidence.append(
        EvidenceItem(
            id="service-history",
            category="Service",
            title="Service history",
            value=f"{len(service_history)} service records",
            status=status,
            confidence=confidence,
            explanation=explanation,
            source=source,
            provenance=_provenance(
                observed_at=service_history[-1].service_date,
            ),
        )
    )


def _add_odometer_evidence(
    evidence: list[EvidenceItem],
    vehicle_data: VehicleData,
) -> None:
    odometer_history = vehicle_data.odometer_history

    source = _source(
        "odometer-history",
        "Vehicle odometer records",
        "service",
    )

    if not odometer_history:
        evidence.append(
            EvidenceItem(
                id="mileage-consistency",
                category="Mileage",
                title="Odometer consistency",
                value="Not available",
                status="unverified",
                confidence="low",
                explanation=(
                    "No usable odometer observations were available."
                ),
                source=source,
                provenance=_provenance(),
            )
        )
        return

    is_consistent = all(
        current.odometer_km >= previous.odometer_km
        for previous, current in zip(
            odometer_history,
            odometer_history[1:],
        )
    )

    if is_consistent:
        evidence.append(
            EvidenceItem(
                id="mileage-consistency",
                category="Mileage",
                title="Odometer consistency",
                value="Consistent",
                status="verified",
                confidence="high",
                explanation=(
                    "The available odometer observations increase "
                    "consistently over time."
                ),
                source=source,
                provenance=_provenance(
                    observed_at=odometer_history[-1].observed_at,
                ),
            )
        )
        return

    conflict_previous = None
    conflict_current = None

    for previous, current in zip(
        odometer_history,
        odometer_history[1:],
    ):
        if current.odometer_km < previous.odometer_km:
            conflict_previous = previous
            conflict_current = current
            break

    if conflict_previous is not None and conflict_current is not None:
        value = (
            f"Inconsistent: {conflict_previous.odometer_km:,} km to "
            f"{conflict_current.odometer_km:,} km"
        )
        observed_at = conflict_current.observed_at
    else:
        value = "Inconsistent"
        observed_at = odometer_history[-1].observed_at

    evidence.append(
        EvidenceItem(
            id="mileage-consistency",
            category="Mileage",
            title="Odometer consistency",
            value=value,
            status="conflicting",
            confidence="high",
            explanation=(
                "A later odometer observation is lower than an earlier "
                "observation. This requires investigation using service "
                "invoices, inspection records, or other independent evidence."
            ),
            source=source,
            provenance=_provenance(
                observed_at=observed_at,
            ),
        )
    )


def _add_accident_evidence(
    evidence: list[EvidenceItem],
    vehicle_data: VehicleData,
) -> None:
    accident_history = vehicle_data.accident_history

    source = _source(
        "insurance-claims",
        "Vehicle accident and claims data",
        "insurance",
    )

    if not accident_history:
        evidence.append(
            EvidenceItem(
                id="accident-history",
                category="Accident",
                title="Accident history",
                value="No recorded accidents",
                status="verified",
                confidence="medium",
                explanation=(
                    "No accidents were recorded in the available data. "
                    "This does not rule out incidents that were never reported."
                ),
                source=source,
                provenance=_provenance(),
            )
        )
        return

    major_accidents = [
        accident
        for accident in accident_history
        if accident.severity == "major"
    ]

    moderate_accidents = [
        accident
        for accident in accident_history
        if accident.severity == "moderate"
    ]

    if major_accidents:
        latest = major_accidents[-1]

        evidence.append(
            EvidenceItem(
                id="accident-history",
                category="Accident",
                title="Accident history",
                value="Major accident recorded",
                status="conflicting",
                confidence="high",
                explanation=(
                    "A major accident is present in the available history "
                    "and should be independently verified using claim, "
                    "repair, and inspection records."
                ),
                source=source,
                provenance=_provenance(
                    observed_at=latest.date,
                    reference_id=latest.id,
                ),
            )
        )
        return

    if moderate_accidents:
        latest = moderate_accidents[-1]

        evidence.append(
            EvidenceItem(
                id="accident-history",
                category="Accident",
                title="Accident history",
                value="Moderate accident recorded",
                status="partially_verified",
                confidence="high",
                explanation=(
                    "A moderate accident is present in the available "
                    "accident or claims history."
                ),
                source=source,
                provenance=_provenance(
                    observed_at=latest.date,
                    reference_id=latest.id,
                ),
            )
        )
        return

    latest = accident_history[-1]

    evidence.append(
        EvidenceItem(
            id="accident-history",
            category="Accident",
            title="Accident history",
            value="Accident history requires review",
            status="partially_verified",
            confidence="medium",
            explanation=(
                "Accident records exist, but the available records "
                "do not indicate a major or moderate accident."
            ),
            source=source,
            provenance=_provenance(
                observed_at=latest.date,
                reference_id=latest.id,
            ),
        )
    )


def _add_challan_evidence(
    evidence: list[EvidenceItem],
    vehicle_data: VehicleData,
) -> None:
    challans = vehicle_data.challans

    source = _source(
        "government-registry",
        "Vehicle challan records",
        "government_registry",
    )

    if not challans:
        evidence.append(
            EvidenceItem(
                id="challan-status",
                category="Compliance",
                title="Challan status",
                value="No recorded challans",
                status="verified",
                confidence="medium",
                explanation=(
                    "No challan records were available in the supplied data."
                ),
                source=source,
                provenance=_provenance(),
            )
        )
        return

    open_challans = [
        challan
        for challan in challans
        if challan.status == "open"
    ]

    if open_challans:
        total_amount = sum(
            challan.amount or 0
            for challan in open_challans
        )

        latest = open_challans[-1]

        evidence.append(
            EvidenceItem(
                id="challan-status",
                category="Compliance",
                title="Challan status",
                value=(
                    f"{len(open_challans)} open challan(s), "
                    f"₹{total_amount:,.0f}"
                ),
                status="partially_verified",
                confidence="high",
                explanation=(
                    "Open challans are present and should be verified "
                    "and resolved before purchase."
                ),
                source=source,
                provenance=_provenance(
                    observed_at=latest.date,
                    reference_id=latest.id,
                ),
            )
        )
        return

    latest = challans[-1]

    evidence.append(
        EvidenceItem(
            id="challan-status",
            category="Compliance",
            title="Challan status",
            value="No open challans",
            status="verified",
            confidence="medium",
            explanation=(
                "No open challans were found in the available records."
            ),
            source=source,
            provenance=_provenance(
                observed_at=latest.date,
                reference_id=latest.id,
            ),
        )
    )


def _add_manufacturer_evidence(
    evidence: list[EvidenceItem],
    vehicle_data: VehicleData,
) -> None:
    manufacturer = vehicle_data.manufacturer

    source = _source(
        "manufacturer-record",
        "Vehicle manufacturer records",
        "manufacturer",
    )

    if manufacturer is None:
        evidence.append(
            EvidenceItem(
                id="manufacturer-details",
                category="Vehicle",
                title="Manufacturer details",
                value="Not available",
                status="unverified",
                confidence="low",
                explanation=(
                    "No manufacturer information was available."
                ),
                source=source,
                provenance=_provenance(),
            )
        )
        return

    model = manufacturer.model or "Unknown"

    evidence.append(
        EvidenceItem(
            id="manufacturer-details",
            category="Vehicle",
            title="Manufacturer details",
            value=f"{manufacturer.manufacturer} {model}",
            status="verified",
            confidence="high",
            explanation=(
                "Manufacturer and model information is available "
                "from the supplied vehicle record."
            ),
            source=source,
            provenance=_provenance(
                observed_at=manufacturer.manufacturing_date,
            ),
        )
    )