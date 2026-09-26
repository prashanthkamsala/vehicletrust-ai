import pytest

from app.domain.semantic_grounding import (
    SemanticGroundingError,
    validate_semantic_grounding,
)
from app.generation.llm_contracts import LLMExplanation
from app.schemas.contracts import (
    AIDecisionAssessment,
    AIEvidenceItem,
    AIEvidenceProvenance,
    AIEvidenceSource,
    AIRequest,
    AIRiskItem,
    AITrustAssessment,
    AITrustFactor,
    AIVehicleIdentity,
)


def build_request() -> AIRequest:
    return AIRequest(
        vehicle=AIVehicleIdentity(
            make="Honda",
            model="City",
            year=2021,
            registration="MH 12 XY 9087",
        ),
        evidence=[
            AIEvidenceItem(
                id="insurance-status",
                category="insurance",
                title="Insurance Status",
                value="Expired",
                status="verified",
                confidence="high",
                explanation="The insurance record is expired.",
                source=AIEvidenceSource(
                    id="mock-insurance",
                    name="Mock India Insurance Provider",
                    type="synthetic",
                ),
                provenance=AIEvidenceProvenance(
                    observed_at="2026-09-01",
                    retrieved_at="2026-09-19",
                    reference_id="INS-001",
                ),
            ),
            AIEvidenceItem(
                id="mileage-consistency",
                category="mileage",
                title="Odometer Consistency",
                value=("42,100 -> 67,300 -> 52,100 -> 58,900 km"),
                status="conflicting",
                confidence="high",
                explanation=(
                    "The recorded odometer history contains a decrease "
                    "between reported readings."
                ),
                source=AIEvidenceSource(
                    id="mock-vehicle-history",
                    name="Mock India Vehicle Provider",
                    type="synthetic",
                ),
                provenance=AIEvidenceProvenance(
                    observed_at="2026-09-01",
                    retrieved_at="2026-09-19",
                    reference_id="VEH-001",
                ),
            ),
            AIEvidenceItem(
                id="accident-history",
                category="accident",
                title="Accident History",
                value="Major accident recorded",
                status="conflicting",
                confidence="high",
                explanation=(
                    "The available accident records contain a major "
                    "accident history requiring review."
                ),
                source=AIEvidenceSource(
                    id="mock-accident-provider",
                    name="Mock India Accident Provider",
                    type="synthetic",
                ),
                provenance=AIEvidenceProvenance(
                    observed_at="2026-09-01",
                    retrieved_at="2026-09-19",
                    reference_id="ACC-001",
                ),
            ),
            AIEvidenceItem(
                id="finance-status",
                category="finance",
                title="Finance Status",
                value="Active finance",
                status="verified",
                confidence="high",
                explanation="The vehicle has an active finance record.",
                source=AIEvidenceSource(
                    id="mock-finance-provider",
                    name="Mock India Finance Provider",
                    type="synthetic",
                ),
                provenance=AIEvidenceProvenance(
                    observed_at="2026-09-01",
                    retrieved_at="2026-09-19",
                    reference_id="FIN-001",
                ),
            ),
        ],
        risks=[
            AIRiskItem(
                id="odometer-inconsistency",
                category="mileage",
                title="Odometer inconsistency",
                severity="high",
                status="needs_review",
                confidence="high",
                explanation=(
                    "The odometer history contains a decrease "
                    "between recorded readings."
                ),
                evidence_ids=["mileage-consistency"],
                recommended_action=(
                    "Verify the mileage history using independent records."
                ),
            ),
            AIRiskItem(
                id="major-accident-history",
                category="accident",
                title="Major accident history",
                severity="high",
                status="needs_review",
                confidence="high",
                explanation=(
                    "A major accident is present in the available " "vehicle history."
                ),
                evidence_ids=["accident-history"],
                recommended_action=(
                    "Verify the accident history and inspect the vehicle."
                ),
            ),
            AIRiskItem(
                id="active-finance",
                category="finance",
                title="Active finance",
                severity="medium",
                status="identified",
                confidence="high",
                explanation=(
                    "An active finance record is associated with " "the vehicle."
                ),
                evidence_ids=["finance-status"],
                recommended_action=(
                    "Verify the outstanding finance status before purchase."
                ),
            ),
        ],
        trust=AITrustAssessment(
            score=0,
            confidence="high",
            assessment="Very low trust due to significant identified risks.",
            factors=[
                AITrustFactor(
                    id="odometer-risk",
                    name="Odometer consistency",
                    impact="negative",
                    contribution=-30,
                    evidence_ids=["mileage-consistency"],
                ),
                AITrustFactor(
                    id="accident-risk",
                    name="Accident history",
                    impact="negative",
                    contribution=-30,
                    evidence_ids=["accident-history"],
                ),
                AITrustFactor(
                    id="finance-risk",
                    name="Finance status",
                    impact="negative",
                    contribution=-10,
                    evidence_ids=["finance-status"],
                ),
            ],
        ),
        decision=AIDecisionAssessment(
            recommendation="avoid",
            confidence="high",
            rationale=(
                "Multiple high-severity risks require resolution " "before purchase."
            ),
            priority_risk_ids=[
                "odometer-inconsistency",
                "major-accident-history",
                "active-finance",
            ],
        ),
    )


def valid_explanation() -> LLMExplanation:
    return LLMExplanation(
        summary=(
            "The 2021 Honda City has a very low deterministic trust "
            "score because the available records identify significant "
            "vehicle-history risks."
        ),
        reasoning=(
            "The verified records show expired insurance and active "
            "finance. The odometer history is conflicting, and the "
            "accident history requires review. These risks require "
            "additional verification."
        ),
        recommendation=(
            "The deterministic purchase decision is to avoid the "
            "purchase until the identified risks are resolved."
        ),
    )


def test_valid_vehicle_explanation_passes() -> None:
    validate_semantic_grounding(
        valid_explanation(),
        build_request(),
    )


def test_verified_evidence_cannot_be_described_as_conflicting() -> None:
    explanation = valid_explanation().model_copy(
        update={
            "reasoning": (
                "The insurance record is conflicting and requires "
                "additional verification."
            )
        }
    )

    with pytest.raises(
        SemanticGroundingError,
        match="insurance-status.*verified",
    ):
        validate_semantic_grounding(
            explanation,
            build_request(),
        )


def test_conflicting_evidence_can_be_described_as_conflicting() -> None:
    explanation = valid_explanation().model_copy(
        update={
            "reasoning": (
                "The odometer history is conflicting and requires "
                "additional verification."
            )
        }
    )

    validate_semantic_grounding(
        explanation,
        build_request(),
    )


def test_conflicting_evidence_cannot_be_described_as_verified() -> None:
    explanation = valid_explanation().model_copy(
        update={"reasoning": ("The odometer history is verified and consistent.")}
    )

    with pytest.raises(
        SemanticGroundingError,
        match="mileage-consistency.*conflicting",
    ):
        validate_semantic_grounding(
            explanation,
            build_request(),
        )


def test_unsupported_tampering_claim_is_rejected() -> None:
    explanation = valid_explanation().model_copy(
        update={
            "reasoning": (
                "The odometer was deliberately tampered with to hide "
                "the vehicle's actual mileage."
            )
        }
    )

    with pytest.raises(
        SemanticGroundingError,
        match="unsupported.*tampering",
    ):
        validate_semantic_grounding(
            explanation,
            build_request(),
        )


def test_unsupported_mechanical_failure_claim_is_rejected() -> None:
    explanation = valid_explanation().model_copy(
        update={
            "reasoning": (
                "The conflicting records indicate that the vehicle "
                "has a mechanical failure."
            )
        }
    )

    with pytest.raises(
        SemanticGroundingError,
        match="unsupported.*mechanical",
    ):
        validate_semantic_grounding(
            explanation,
            build_request(),
        )


def test_deterministic_avoid_decision_cannot_be_changed() -> None:
    explanation = valid_explanation().model_copy(
        update={
            "recommendation": (
                "The vehicle is suitable for purchase and the buyer " "can proceed."
            )
        }
    )

    with pytest.raises(
        SemanticGroundingError,
        match="deterministic decision.*avoid",
    ):
        validate_semantic_grounding(
            explanation,
            build_request(),
        )


def test_high_severity_risk_cannot_be_downgraded() -> None:
    explanation = valid_explanation().model_copy(
        update={
            "reasoning": (
                "The odometer inconsistency is only a low-severity "
                "issue and does not require significant review."
            )
        }
    )

    with pytest.raises(
        SemanticGroundingError,
        match="odometer-inconsistency.*high",
    ):
        validate_semantic_grounding(
            explanation,
            build_request(),
        )


def test_cautious_explanation_with_explicit_verification_passes() -> None:
    explanation = LLMExplanation(
        summary=(
            "The available records identify significant risks that "
            "require further verification."
        ),
        reasoning=(
            "The insurance record is verified as expired, while the "
            "odometer and accident records are conflicting. Active "
            "finance is also verified. The available evidence does "
            "not establish the cause of the conflicting records."
        ),
        recommendation=(
            "The deterministic decision is to avoid the purchase "
            "until the identified risks are independently verified "
            "and resolved."
        ),
    )

    validate_semantic_grounding(
        explanation,
        build_request(),
    )


def test_conflicting_evidence_is_not_invalidated_by_verified_claim_for_another_evidence() -> None:
    request = AIRequest(
        vehicle=AIVehicleIdentity(
            make="Honda",
            model="Civic",
            year=2020,
            registration="KA 01 AB 7744",
        ),
        evidence=[
            AIEvidenceItem(
                id="mileage-consistency",
                category="Mileage",
                title="Odometer consistency",
                value="Inconsistent",
                status="conflicting",
                confidence="high",
                explanation="The odometer history contains a decrease.",
                source=AIEvidenceSource(
                    id="odometer-history",
                    name="Vehicle odometer records",
                    type="service",
                ),
                provenance=AIEvidenceProvenance(
                    observed_at="2026-09-10",
                ),
            ),
            AIEvidenceItem(
                id="accident-history",
                category="Accident",
                title="Major accident history",
                value="Major accident recorded",
                status="verified",
                confidence="high",
                explanation=(
                    "A major accident is recorded in the available "
                    "vehicle history."
                ),
                source=AIEvidenceSource(
                    id="accident-record",
                    name="Vehicle accident records",
                    type="service",
                ),
                provenance=AIEvidenceProvenance(
                    observed_at="2026-09-10",
                ),
            ),
        ],
        risks=[],
        trust=AITrustAssessment(
            score=20,
            confidence="high",
            assessment="Low trust",
        ),
        decision=AIDecisionAssessment(
            recommendation="avoid",
            confidence="high",
            rationale="Multiple high-impact risks require resolution.",
        ),
    )

    explanation = LLMExplanation(
        summary=(
            "The vehicle has conflicting odometer history and a "
            "verified major accident record."
        ),
        reasoning=(
            "The odometer inconsistency requires verification due to "
            "conflicting evidence, the major accident is confirmed by "
            "verified records."
        ),
        recommendation="avoid",
    )

    validate_semantic_grounding(
        explanation=explanation,
        request=request,
    )