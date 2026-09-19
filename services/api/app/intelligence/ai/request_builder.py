from app.intelligence.ai.contracts import (
    AIDecisionAssessment,
    AIEvidenceItem,
    AIEvidenceProvenance,
    AIEvidenceSource,
    AIRiskItem,
    AIRequest,
    AITrustAssessment,
    AITrustFactor,
    AIVehicleIdentity,
)
from app.schemas.vehicle.models import VehicleIntelligence


def build_ai_request(vehicle: VehicleIntelligence) -> AIRequest:
    """Translate deterministic vehicle intelligence into the AI contract."""

    return AIRequest(
        vehicle=AIVehicleIdentity(
            make=vehicle.identity.make,
            model=vehicle.identity.model,
            year=vehicle.identity.year,
            registration=vehicle.identity.registration,
        ),
        evidence=[
            AIEvidenceItem(
                id=evidence.id,
                category=evidence.category,
                title=evidence.title,
                value=evidence.value,
                status=evidence.status,
                confidence=evidence.confidence,
                explanation=evidence.explanation,
                source=AIEvidenceSource(
                    id=evidence.source.id,
                    name=evidence.source.name,
                    type=evidence.source.type,
                ),
                provenance=AIEvidenceProvenance(
                    observed_at=evidence.provenance.observed_at,
                    retrieved_at=evidence.provenance.retrieved_at,
                    reference_id=evidence.provenance.reference_id,
                ),
            )
            for evidence in vehicle.evidence
        ],
        risks=[
            AIRiskItem(
                id=risk.id,
                category=risk.category,
                title=risk.title,
                severity=risk.severity,
                status=risk.status,
                confidence=risk.confidence,
                explanation=risk.explanation,
                evidence_ids=list(risk.evidence_ids),
                recommended_action=risk.recommended_action,
            )
            for risk in vehicle.risks
        ],
        trust=AITrustAssessment(
            score=vehicle.trust.score,
            confidence=vehicle.trust.confidence,
            assessment=vehicle.trust.assessment,
            factors=[
                AITrustFactor(
                    id=factor.id,
                    name=factor.name,
                    impact=factor.impact,
                    contribution=factor.contribution,
                    evidence_ids=list(factor.evidence_ids),
                )
                for factor in vehicle.trust.factors
            ],
        ),
        decision=AIDecisionAssessment(
            recommendation=vehicle.decision.recommendation,
            confidence=vehicle.decision.confidence,
            rationale=vehicle.decision.rationale,
            priority_risk_ids=list(vehicle.decision.priority_risk_ids),
        ),
    )