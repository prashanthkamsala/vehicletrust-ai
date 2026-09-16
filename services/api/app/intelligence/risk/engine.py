from app.schemas.vehicle.models import EvidenceItem, RiskItem


def build_risks(evidence: list[EvidenceItem]) -> list[RiskItem]:
    """Derive actionable risks from deterministic evidence."""

    evidence_by_id = {item.id: item for item in evidence}
    risks: list[RiskItem] = []

    _add_mileage_risk(risks, evidence_by_id)
    _add_accident_risk(risks, evidence_by_id)
    _add_finance_risk(risks, evidence_by_id)
    _add_insurance_risk(risks, evidence_by_id)
    _add_puc_risk(risks, evidence_by_id)
    _add_challan_risk(risks, evidence_by_id)
    _add_ownership_risk(risks, evidence_by_id)

    return risks


def _add_mileage_risk(
    risks: list[RiskItem],
    evidence: dict[str, EvidenceItem],
) -> None:
    item = evidence.get("mileage-consistency")

    if item is None or item.status != "conflicting":
        return

    risks.append(
        RiskItem(
            id="odometer-inconsistency",
            category="Mileage",
            title="Odometer inconsistency detected",
            severity="high",
            status="needs_review",
            confidence=item.confidence,
            explanation=(
                "Recorded odometer readings contain a decrease over time. "
                "The discrepancy should be investigated using service "
                "invoices, inspection records, or other supporting evidence."
            ),
            evidence_ids=[item.id],
            recommended_action=(
                "Request service invoices and inspection records covering "
                "the inconsistent odometer readings before purchase."
            ),
        )
    )


def _add_accident_risk(
    risks: list[RiskItem],
    evidence: dict[str, EvidenceItem],
) -> None:
    item = evidence.get("accident-history")

    if item is None or item.status != "conflicting":
        return

    risks.append(
        RiskItem(
            id="major-accident-history",
            category="Accident",
            title="Major accident history requires investigation",
            severity="high",
            status="needs_review",
            confidence=item.confidence,
            explanation=(
                "The available evidence contains a major accident signal. "
                "The extent of structural or mechanical damage should be "
                "verified using claims and repair documentation."
            ),
            evidence_ids=[item.id],
            recommended_action=(
                "Obtain the insurance claim and repair records and arrange "
                "an independent inspection before purchase."
            ),
        )
    )


def _add_finance_risk(
    risks: list[RiskItem],
    evidence: dict[str, EvidenceItem],
) -> None:
    item = evidence.get("finance-status")

    if item is None or item.value != "Active":
        return

    risks.append(
        RiskItem(
            id="active-finance",
            category="Finance",
            title="Active vehicle finance requires verification",
            severity="medium",
            status="needs_review",
            confidence=item.confidence,
            explanation=(
                "An active finance record is associated with the vehicle. "
                "Ownership transfer should only proceed after confirming "
                "the lender's release and applicable documentation."
            ),
            evidence_ids=[item.id],
            recommended_action=(
                "Request the lender's outstanding-loan and lien-release "
                "documentation before completing the purchase."
            ),
        )
    )


def _add_insurance_risk(
    risks: list[RiskItem],
    evidence: dict[str, EvidenceItem],
) -> None:
    item = evidence.get("insurance-status")

    if item is None or item.value != "Expired":
        return

    risks.append(
        RiskItem(
            id="expired-insurance",
            category="Insurance",
            title="Insurance record has expired",
            severity="medium",
            status="needs_review",
            confidence=item.confidence,
            explanation=(
                "The available insurance record is expired. Current "
                "coverage should be verified before the vehicle is used "
                "or transferred."
            ),
            evidence_ids=[item.id],
            recommended_action=(
                "Verify current insurance coverage and obtain valid "
                "policy documentation before purchase."
            ),
        )
    )


def _add_puc_risk(
    risks: list[RiskItem],
    evidence: dict[str, EvidenceItem],
) -> None:
    item = evidence.get("puc-status")

    if item is None or item.value != "Expired":
        return

    risks.append(
        RiskItem(
            id="expired-puc",
            category="Compliance",
            title="PUC certificate has expired",
            severity="medium",
            status="needs_review",
            confidence=item.confidence,
            explanation=(
                "The available pollution-under-control certificate is "
                "expired and requires verification or renewal."
            ),
            evidence_ids=[item.id],
            recommended_action=(
                "Verify the current PUC status and obtain a valid "
                "certificate before purchase."
            ),
        )
    )


def _add_challan_risk(
    risks: list[RiskItem],
    evidence: dict[str, EvidenceItem],
) -> None:
    item = evidence.get("challan-status")

    if item is None or "open challan(s)" not in item.value:
        return

    risks.append(
        RiskItem(
            id="open-challans",
            category="Compliance",
            title="Open traffic challans require resolution",
            severity="medium",
            status="needs_review",
            confidence=item.confidence,
            explanation=(
                "The available records contain open traffic challans. "
                "Outstanding obligations should be resolved or verified "
                "before ownership transfer."
            ),
            evidence_ids=[item.id],
            recommended_action=(
                "Verify the outstanding challans and obtain confirmation "
                "of payment or resolution before purchase."
            ),
        )
    )


def _add_ownership_risk(
    risks: list[RiskItem],
    evidence_by_id: dict[str, EvidenceItem],
) -> None:
    evidence = evidence_by_id.get("ownership-history")

    if evidence is None:
        return

    if evidence.status == "unverified":
        return

    if evidence.value in {"2 owners", "3 owners"}:
        risks.append(
            RiskItem(
                id="multiple-ownership-history",
                category="Ownership",
                title="Multiple ownership history",
                severity="low",
                status="needs_review",
                confidence=evidence.confidence,
                explanation=(
                    "The vehicle has multiple recorded owners. "
                    "This is not inherently negative, but the ownership "
                    "timeline should be reviewed as part of the vehicle assessment."
                ),
                evidence_ids=["ownership-history"],
                recommended_action=(
                    "Review the ownership timeline and verify the transfer "
                    "history against available records."
                ),
            )
        )