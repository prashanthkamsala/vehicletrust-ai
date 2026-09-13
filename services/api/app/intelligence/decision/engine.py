from app.schemas.vehicle.models import (
    DecisionAssessment,
    EvidenceConfidence,
    RiskItem,
    RiskSeverity,
    TrustAssessment,
)


def build_decision_assessment(
    risks: list[RiskItem],
    trust: TrustAssessment,
    evidence_count: int,
) -> DecisionAssessment:
    """Derive a conservative purchase decision from trust and risk signals."""

    if evidence_count == 0:
        return DecisionAssessment(
            recommendation="insufficient_evidence",
            confidence="low",
            rationale=(
                "There is not enough vehicle evidence available to make "
                "a reliable purchase decision."
            ),
            priority_risk_ids=[],
        )

    critical_risks = [
        risk for risk in risks if risk.severity == "critical"
    ]
    high_risks = [
        risk for risk in risks if risk.severity == "high"
    ]
    medium_risks = [
        risk for risk in risks if risk.severity == "medium"
    ]

    priority_risks = sorted(
        risks,
        key=_risk_priority,
        reverse=True,
    )

    priority_risk_ids = [
        risk.id for risk in priority_risks[:3]
    ]

    if critical_risks or len(high_risks) >= 2:
        return DecisionAssessment(
            recommendation="avoid",
            confidence=_decision_confidence(
                critical_risks + high_risks,
            ),
            rationale=_build_avoid_rationale(
                critical_risks,
                high_risks,
            ),
            priority_risk_ids=priority_risk_ids,
        )

    if high_risks or len(medium_risks) >= 2 or trust.score < 75:
        return DecisionAssessment(
            recommendation="review",
            confidence=_decision_confidence(
                high_risks + medium_risks,
            ),
            rationale=_build_review_rationale(
                high_risks,
                medium_risks,
                trust,
            ),
            priority_risk_ids=priority_risk_ids,
        )

    return DecisionAssessment(
        recommendation="buy",
        confidence=_decision_confidence(risks),
        rationale=(
            "The available evidence indicates a strong trust profile "
            "without high-severity risks requiring resolution."
        ),
        priority_risk_ids=priority_risk_ids,
    )


def _risk_priority(risk: RiskItem) -> tuple[int, int]:
    severity_weight = {
        "critical": 4,
        "high": 3,
        "medium": 2,
        "low": 1,
    }

    status_weight = {
        "needs_review": 2,
        "identified": 1,
        "resolved": 0,
        "dismissed": 0,
    }

    return (
        severity_weight[risk.severity],
        status_weight[risk.status],
    )


def _decision_confidence(
    risks: list[RiskItem],
) -> EvidenceConfidence:
    if not risks:
        return "high"

    if all(risk.confidence == "high" for risk in risks):
        return "high"

    if any(risk.confidence == "high" for risk in risks):
        return "medium"

    return "low"


def _build_avoid_rationale(
    critical_risks: list[RiskItem],
    high_risks: list[RiskItem],
) -> str:
    if critical_risks:
        return (
            "The vehicle has one or more critical risks that should be "
            "resolved before purchase."
        )

    return (
        f"The vehicle has {len(high_risks)} high-severity risks that "
        "require resolution or independent verification before purchase."
    )


def _build_review_rationale(
    high_risks: list[RiskItem],
    medium_risks: list[RiskItem],
    trust: TrustAssessment,
) -> str:
    if high_risks:
        return (
            "The vehicle has a high-severity risk that requires "
            "verification before purchase."
        )

    if len(medium_risks) >= 2:
        return (
            f"The vehicle has {len(medium_risks)} medium-severity risks "
            "that should be reviewed before purchase."
        )

    return (
        f"The trust score is {trust.score}/100, so the vehicle should "
        "be reviewed carefully before purchase."
    )