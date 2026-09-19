from typing import Literal

from pydantic import BaseModel, Field


EvidenceStatus = Literal[
    "verified",
    "partially_verified",
    "unverified",
    "conflicting",
]

EvidenceConfidence = Literal[
    "high",
    "medium",
    "low",
]

RiskSeverity = Literal[
    "low",
    "medium",
    "high",
    "critical",
]

RiskStatus = Literal[
    "identified",
    "needs_review",
    "resolved",
    "dismissed",
]

DecisionRecommendation = Literal[
    "buy",
    "review",
    "avoid",
    "insufficient_evidence",
]


class AIVehicleIdentity(BaseModel):
    make: str
    model: str
    year: int
    registration: str


class AIEvidenceSource(BaseModel):
    id: str
    name: str
    type: str


class AIEvidenceProvenance(BaseModel):
    observed_at: str | None = None
    retrieved_at: str | None = None
    reference_id: str | None = None


class AIEvidenceItem(BaseModel):
    id: str
    category: str
    title: str
    value: str
    status: EvidenceStatus
    confidence: EvidenceConfidence
    explanation: str
    source: AIEvidenceSource
    provenance: AIEvidenceProvenance


class AIRiskItem(BaseModel):
    id: str
    category: str
    title: str
    severity: RiskSeverity
    status: RiskStatus
    confidence: EvidenceConfidence
    explanation: str
    evidence_ids: list[str] = Field(default_factory=list)
    recommended_action: str


class AITrustFactor(BaseModel):
    id: str
    name: str
    impact: Literal["positive", "negative", "neutral"]
    contribution: int
    evidence_ids: list[str] = Field(default_factory=list)


class AITrustAssessment(BaseModel):
    score: int
    confidence: EvidenceConfidence
    assessment: str
    factors: list[AITrustFactor] = Field(default_factory=list)


class AIDecisionAssessment(BaseModel):
    recommendation: DecisionRecommendation
    confidence: EvidenceConfidence
    rationale: str
    priority_risk_ids: list[str] = Field(default_factory=list)


class AIRequest(BaseModel):
    vehicle: AIVehicleIdentity
    evidence: list[AIEvidenceItem] = Field(default_factory=list)
    risks: list[AIRiskItem] = Field(default_factory=list)
    trust: AITrustAssessment
    decision: AIDecisionAssessment