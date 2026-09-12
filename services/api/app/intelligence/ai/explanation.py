from app.schemas.vehicle.models import (
    AIInterpretation,
    EvidenceItem,
    RiskItem,
    TrustAssessment,
)


def build_ai_interpretation(
    evidence: list[EvidenceItem],
    risks: list[RiskItem],
    trust: TrustAssessment,
) -> AIInterpretation:
    """Build an evidence-backed vehicle explanation."""

    if not evidence:
        return AIInterpretation(
            summary="Insufficient vehicle evidence is available for a reliable assessment.",
            reasoning="The intelligence engine did not receive enough evidence to explain the vehicle's trust profile.",
            recommendation="Obtain additional vehicle records before making a decision.",
        )

    if not risks:
        return AIInterpretation(
            summary=(
                f"The available evidence indicates a {trust.assessment.lower()} "
                "vehicle with no significant risks identified."
            ),
            reasoning=_build_reasoning(evidence, trust),
            recommendation=(
                "The available evidence supports proceeding, subject to "
                "normal physical inspection and verification of original documents."
            ),
        )

    high_risks = [
        risk for risk in risks if risk.severity in {"high", "critical"}
    ]
    medium_risks = [risk for risk in risks if risk.severity == "medium"]

    summary = _build_risk_summary(
    trust,
    risks,
    high_risks,
    medium_risks,
    )
    reasoning = _build_risk_reasoning(evidence, risks, trust)
    recommendation = _build_recommendation(risks)

    return AIInterpretation(
        summary=summary,
        reasoning=reasoning,
        recommendation=recommendation,
    )


def _build_reasoning(
    evidence: list[EvidenceItem],
    trust: TrustAssessment,
) -> str:
    """Explain the positive signals supporting the trust assessment."""

    positive_signals = [
        factor.name
        for factor in trust.factors
        if factor.impact == "positive"
    ]

    if positive_signals:
        signals = ", ".join(positive_signals[:5])

        return (
            f"The trust assessment is supported by positive signals including "
            f"{signals}. The available evidence should still be verified against "
            "original documents and the vehicle's physical condition."
        )

    return (
        "The available evidence does not contain enough positive signals to "
        "support a stronger trust assessment."
    )


def _build_risk_summary(
    trust: TrustAssessment,
    risks: list[RiskItem],
    high_risks: list[RiskItem],
    medium_risks: list[RiskItem],
) -> str:
    """Summarize identified risks using the complete risk set."""

    total_risks = len(risks)

    if high_risks:
        high_count = len(high_risks)
        risk_word = "risk" if high_count == 1 else "risks"

        return (
            f"The vehicle has a {trust.assessment.lower()} profile with "
            f"{high_count} high-severity {risk_word} requiring attention "
            f"and {total_risks} risk"
            f"{'s' if total_risks != 1 else ''} identified overall."
        )

    risk_word = "risk" if total_risks == 1 else "risks"

    return (
        f"The vehicle has a {trust.assessment.lower()} profile with "
        f"{total_risks} {risk_word} identified. "
        "The identified issues should be reviewed before making a final decision."
    )


def _build_risk_reasoning(
    evidence: list[EvidenceItem],
    risks: list[RiskItem],
    trust: TrustAssessment,
) -> str:
    risk_titles = [risk.title for risk in risks[:5]]

    if not risk_titles:
        return _build_reasoning(evidence, trust)

    risk_text = ", ".join(risk_titles)

    return (
        f"The trust score of {trust.score}/100 reflects the available evidence "
        f"and identified risk signals. The main areas requiring attention are: "
        f"{risk_text}. These findings should be verified using the evidence "
        "referenced by each risk before making a final decision."
    )


def _build_recommendation(risks: list[RiskItem]) -> str:
    """Build a clean, actionable recommendation from identified risks."""

    actions: list[str] = []

    for risk in risks:
        action = risk.recommended_action.strip()

        if not action:
            continue

        if action not in actions:
            actions.append(action)

    if not actions:
        return (
            "Review the available vehicle records and complete an independent "
            "physical inspection before making a final decision."
        )

    cleaned_actions = [
        action.rstrip(".; ") for action in actions[:3]
    ]

    if len(cleaned_actions) == 1:
        return f"Recommended action: {cleaned_actions[0]}."

    return "Priority actions: " + "; ".join(cleaned_actions) + "."