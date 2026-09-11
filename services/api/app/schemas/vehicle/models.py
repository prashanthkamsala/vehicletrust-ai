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

TrustImpact = Literal[
    "positive",
    "negative",
    "neutral",
]


class EvidenceSource(BaseModel):
    id: str
    name: str
    type: str


class EvidenceItem(BaseModel):
    id: str
    category: str
    title: str
    value: str
    status: EvidenceStatus
    confidence: EvidenceConfidence
    explanation: str
    source: EvidenceSource
    observed_at: str | None = None


class RiskItem(BaseModel):
    id: str
    category: str
    title: str
    severity: RiskSeverity
    status: RiskStatus
    confidence: EvidenceConfidence
    explanation: str
    evidence_ids: list[str] = Field(default_factory=list)
    recommended_action: str


class TrustFactor(BaseModel):
    id: str
    name: str
    impact: TrustImpact
    contribution: int
    evidence_ids: list[str] = Field(default_factory=list)


class TrustAssessment(BaseModel):
    base_score: int = Field(ge=0, le=100)
    score: int = Field(ge=0, le=100)
    confidence: EvidenceConfidence
    assessment: str
    factors: list[TrustFactor] = Field(default_factory=list)


class AIInterpretation(BaseModel):
    summary: str
    reasoning: str
    recommendation: str


class VehicleIdentity(BaseModel):
    make: str
    model: str
    year: int
    registration: str
    vin: str


class VehicleIntelligence(BaseModel):
    id: str
    identity: VehicleIdentity
    evidence: list[EvidenceItem] = Field(default_factory=list)
    risks: list[RiskItem] = Field(default_factory=list)
    trust: TrustAssessment
    ai: AIInterpretation
