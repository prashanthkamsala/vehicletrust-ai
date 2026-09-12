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
    observed_at: str | None = Field(default=None, serialization_alias="observedAt")


class RiskItem(BaseModel):
    id: str
    category: str
    title: str
    severity: RiskSeverity
    status: RiskStatus
    confidence: EvidenceConfidence
    explanation: str
    evidence_ids: list[str] = Field(
        default_factory=list,
        serialization_alias="evidenceIds",
    )
    recommended_action: str = Field(serialization_alias="recommendedAction")


class TrustFactor(BaseModel):
    id: str
    name: str
    impact: TrustImpact
    contribution: int
    evidence_ids: list[str] = Field(
        default_factory=list,
        serialization_alias="evidenceIds",
    )


class TrustAssessment(BaseModel):
    base_score: int = Field(
        ge=0,
        le=100,
        serialization_alias="baseScore",
    )
    calculated_score: int = Field(serialization_alias="calculatedScore")
    score: int = Field(
        ge=0,
        le=100,
        serialization_alias="score",
    )
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

class VehicleRegistration(BaseModel):
    registration_number: str = Field(serialization_alias="registrationNumber")
    registration_date: str | None = Field(
        default=None,
        serialization_alias="registrationDate",
    )
    registering_authority: str | None = Field(
        default=None,
        serialization_alias="registeringAuthority",
    )
    state: str | None = None
    status: Literal[
        "active",
        "inactive",
        "suspended",
        "unknown",
    ] | None = None


class OwnershipRecord(BaseModel):
    owner_sequence: int = Field(serialization_alias="ownerSequence")
    ownership_type: str | None = Field(
        default=None,
        serialization_alias="ownershipType",
    )
    start_date: str | None = Field(
        default=None,
        serialization_alias="startDate",
    )
    end_date: str | None = Field(
        default=None,
        serialization_alias="endDate",
    )
    source: EvidenceSource


class InsuranceDetails(BaseModel):
    status: Literal["active", "expired", "unknown"]
    policy_type: str | None = Field(
        default=None,
        serialization_alias="policyType",
    )
    provider: str | None = None
    policy_number: str | None = Field(
        default=None,
        serialization_alias="policyNumber",
    )
    start_date: str | None = Field(
        default=None,
        serialization_alias="startDate",
    )
    expiry_date: str | None = Field(
        default=None,
        serialization_alias="expiryDate",
    )


class PucDetails(BaseModel):
    status: Literal[
        "valid",
        "expired",
        "not_available",
        "unknown",
    ]
    certificate_number: str | None = Field(
        default=None,
        serialization_alias="certificateNumber",
    )
    issue_date: str | None = Field(
        default=None,
        serialization_alias="issueDate",
    )
    expiry_date: str | None = Field(
        default=None,
        serialization_alias="expiryDate",
    )
    emission_norm: str | None = Field(
        default=None,
        serialization_alias="emissionNorm",
    )


class FinanceDetails(BaseModel):
    status: Literal["active", "closed", "unknown"]
    financier: str | None = None
    start_date: str | None = Field(
        default=None,
        serialization_alias="startDate",
    )
    closure_date: str | None = Field(
        default=None,
        serialization_alias="closureDate",
    )


class ServiceRecord(BaseModel):
    id: str
    service_date: str = Field(serialization_alias="serviceDate")
    odometer_km: int | None = Field(
        default=None,
        serialization_alias="odometerKm",
    )
    service_type: str | None = Field(
        default=None,
        serialization_alias="serviceType",
    )
    service_center: str | None = Field(
        default=None,
        serialization_alias="serviceCenter",
    )
    description: str | None = None


class OdometerRecord(BaseModel):
    observed_at: str = Field(serialization_alias="observedAt")
    odometer_km: int = Field(serialization_alias="odometerKm")
    source: EvidenceSource


class AccidentRecord(BaseModel):
    id: str
    date: str | None = None
    severity: Literal[
        "minor",
        "moderate",
        "major",
        "unknown",
    ] | None = None
    description: str | None = None
    source: EvidenceSource


class ChallanRecord(BaseModel):
    id: str
    date: str | None = None
    status: Literal[
        "open",
        "paid",
        "cancelled",
        "unknown",
    ]
    amount: float | None = None
    description: str | None = None
    source: EvidenceSource


class ManufacturerDetails(BaseModel):
    manufacturer: str
    model: str | None = None
    variant: str | None = None
    fuel_type: str | None = Field(
        default=None,
        serialization_alias="fuelType",
    )
    transmission: str | None = None
    manufacturing_date: str | None = Field(
        default=None,
        serialization_alias="manufacturingDate",
    )
    warranty_status: Literal[
        "active",
        "expired",
        "unknown",
    ] | None = Field(
        default=None,
        serialization_alias="warrantyStatus",
    )


class VehicleData(BaseModel):
    registration: VehicleRegistration | None = None
    ownership: list[OwnershipRecord] = Field(default_factory=list)
    insurance: InsuranceDetails | None = None
    puc: PucDetails | None = None
    finance: FinanceDetails | None = None
    service_history: list[ServiceRecord] = Field(
        default_factory=list,
        serialization_alias="serviceHistory",
    )
    odometer_history: list[OdometerRecord] = Field(
        default_factory=list,
        serialization_alias="odometerHistory",
    )
    accident_history: list[AccidentRecord] = Field(
        default_factory=list,
        serialization_alias="accidentHistory",
    )
    challans: list[ChallanRecord] = Field(default_factory=list)
    manufacturer: ManufacturerDetails | None = None


class VehicleIntelligence(BaseModel):
    id: str
    identity: VehicleIdentity
    data: VehicleData | None = None
    evidence: list[EvidenceItem] = Field(default_factory=list)
    risks: list[RiskItem] = Field(default_factory=list)
    trust: TrustAssessment
    ai: AIInterpretation
