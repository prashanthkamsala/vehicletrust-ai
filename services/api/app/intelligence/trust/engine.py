from app.schemas.vehicle.models import (
    EvidenceItem,
    RiskItem,
    TrustAssessment,
    TrustFactor,
)


BASE_SCORE = 50


def build_trust_assessment(
    evidence: list[EvidenceItem],
    risks: list[RiskItem],
) -> TrustAssessment:
    """Build a deterministic, explainable trust assessment."""

    evidence_by_id = {item.id: item for item in evidence}

    factors: list[TrustFactor] = []

    _add_registration_factor(factors, evidence_by_id)
    _add_ownership_factor(factors, evidence_by_id, risks)
    _add_mileage_factor(factors, evidence_by_id)
    _add_insurance_factor(factors, evidence_by_id)
    _add_puc_factor(factors, evidence_by_id)
    _add_finance_factor(factors, evidence_by_id)
    _add_accident_factor(factors, evidence_by_id)
    _add_challan_factor(factors, evidence_by_id)

    calculated_score = _calculate_calculated_score(factors)
    score = _bound_score(calculated_score)

    confidence = _calculate_confidence(evidence)
    assessment = _build_assessment(score)

    return TrustAssessment(
        base_score=BASE_SCORE,
        calculated_score=calculated_score,
        score=score,
        confidence=confidence,
        assessment=assessment,
        factors=factors,
    )


def _add_registration_factor(
    factors: list[TrustFactor],
    evidence: dict[str, EvidenceItem],
) -> None:
    item = evidence.get("registration-status")

    if item is None:
        return

    if item.value == "Active" and item.status == "verified":
        factors.append(
            TrustFactor(
                id="registration-factor",
                name="Active registration",
                impact="positive",
                contribution=10,
                evidence_ids=[item.id],
            )
        )


def _add_ownership_factor(
    factors: list[TrustFactor],
    evidence: dict[str, EvidenceItem],
    risks: list[RiskItem],
) -> None:
    item = evidence.get("ownership-history")

    if item is None or item.status == "unverified":
        return

    if item.value == "1 owner":
        factors.append(
            TrustFactor(
                id="ownership-factor",
                name="Single ownership",
                impact="positive",
                contribution=10,
                evidence_ids=[item.id],
            )
        )
        return

    if item.value in {"2 owners", "3 owners"}:
        contribution = -3

        factors.append(
            TrustFactor(
                id="ownership-factor",
                name="Multiple ownership",
                impact="negative",
                contribution=contribution,
                evidence_ids=[item.id],
            )
        )


def _add_mileage_factor(
    factors: list[TrustFactor],
    evidence: dict[str, EvidenceItem],
) -> None:
    item = evidence.get("mileage-consistency")

    if item is None:
        return

    if item.status == "verified" and item.value == "Consistent":
        factors.append(
            TrustFactor(
                id="mileage-factor",
                name="Mileage consistency",
                impact="positive",
                contribution=10,
                evidence_ids=[item.id],
            )
        )
    elif item.status == "conflicting":
        factors.append(
            TrustFactor(
                id="odometer-factor",
                name="Odometer inconsistency",
                impact="negative",
                contribution=-25,
                evidence_ids=[item.id],
            )
        )


def _add_insurance_factor(
    factors: list[TrustFactor],
    evidence: dict[str, EvidenceItem],
) -> None:
    item = evidence.get("insurance-status")

    if item is None:
        return

    if item.value == "Active" and item.status == "verified":
        factors.append(
            TrustFactor(
                id="insurance-factor",
                name="Active insurance",
                impact="positive",
                contribution=5,
                evidence_ids=[item.id],
            )
        )
    elif item.value == "Expired":
        factors.append(
            TrustFactor(
                id="insurance-factor",
                name="Expired insurance",
                impact="negative",
                contribution=-8,
                evidence_ids=[item.id],
            )
        )


def _add_puc_factor(
    factors: list[TrustFactor],
    evidence: dict[str, EvidenceItem],
) -> None:
    item = evidence.get("puc-status")

    if item is None:
        return

    if item.value == "Valid" and item.status == "verified":
        factors.append(
            TrustFactor(
                id="puc-factor",
                name="Valid PUC",
                impact="positive",
                contribution=5,
                evidence_ids=[item.id],
            )
        )
    elif item.value == "Expired":
        factors.append(
            TrustFactor(
                id="puc-factor",
                name="Expired PUC",
                impact="negative",
                contribution=-5,
                evidence_ids=[item.id],
            )
        )


def _add_finance_factor(
    factors: list[TrustFactor],
    evidence: dict[str, EvidenceItem],
) -> None:
    item = evidence.get("finance-status")

    if item is None:
        return

    if item.value == "Closed" and item.status == "verified":
        factors.append(
            TrustFactor(
                id="finance-factor",
                name="Closed finance",
                impact="positive",
                contribution=5,
                evidence_ids=[item.id],
            )
        )
    elif item.value == "Active":
        factors.append(
            TrustFactor(
                id="finance-factor",
                name="Active finance",
                impact="negative",
                contribution=-10,
                evidence_ids=[item.id],
            )
        )


def _add_accident_factor(
    factors: list[TrustFactor],
    evidence: dict[str, EvidenceItem],
) -> None:
    item = evidence.get("accident-history")

    if item is None:
        return

    if item.value == "No recorded accidents":
        factors.append(
            TrustFactor(
                id="accident-factor",
                name="No recorded accidents",
                impact="positive",
                contribution=5,
                evidence_ids=[item.id],
            )
        )
    elif item.status == "conflicting":
        factors.append(
            TrustFactor(
                id="accident-factor",
                name="Major accident history",
                impact="negative",
                contribution=-20,
                evidence_ids=[item.id],
            )
        )


def _add_challan_factor(
    factors: list[TrustFactor],
    evidence: dict[str, EvidenceItem],
) -> None:
    item = evidence.get("challan-status")

    if item is None:
        return

    if "open challan(s)" in item.value:
        factors.append(
            TrustFactor(
                id="challan-factor",
                name="Open challans",
                impact="negative",
                contribution=-5,
                evidence_ids=[item.id],
            )
        )


def _calculate_calculated_score(factors: list[TrustFactor]) -> int:
    return BASE_SCORE + sum(factor.contribution for factor in factors)


def _bound_score(calculated_score: int) -> int:
    return min(100, max(0, calculated_score))


def _calculate_confidence(
    evidence: list[EvidenceItem],
) -> str:
    if not evidence:
        return "low"

    high_confidence = sum(
        1 for item in evidence if item.confidence == "high"
    )
    medium_confidence = sum(
        1 for item in evidence if item.confidence == "medium"
    )

    total = len(evidence)

    if high_confidence / total >= 0.7:
        return "high"

    if (high_confidence + medium_confidence) / total >= 0.7:
        return "medium"

    return "low"


def _build_assessment(score: int) -> str:
    if score >= 90:
        return "Very high trust"

    if score >= 75:
        return "High trust"

    if score >= 60:
        return "Moderate trust"

    if score >= 40:
        return "Low trust"

    return "Very low trust"