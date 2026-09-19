export type EvidenceStatus =
  | "verified"
  | "partially_verified"
  | "unverified"
  | "conflicting";

export type EvidenceConfidence = "high" | "medium" | "low";

export type RiskSeverity = "low" | "medium" | "high" | "critical";

export type RiskStatus =
  | "identified"
  | "needs_review"
  | "resolved"
  | "dismissed";

export interface EvidenceSource {
  id: string;
  name: string;
  type: string;
}

export interface EvidenceItem {
  id: string;
  category: string;
  title: string;
  value: string;
  status: EvidenceStatus;
  confidence: EvidenceConfidence;
  explanation: string;
  source: EvidenceSource;
  observedAt?: string;
}

export interface VehicleRegistration {
  registrationNumber: string;
  registrationDate?: string;
  registeringAuthority?: string;
  state?: string;
  status?: "active" | "inactive" | "suspended" | "unknown";
}

export interface OwnershipRecord {
  ownerSequence: number;
  ownershipType?: string;
  startDate?: string;
  endDate?: string;
  source: EvidenceSource;
}

export interface InsuranceDetails {
  status: "active" | "expired" | "unknown";
  policyType?: string;
  provider?: string;
  policyNumber?: string;
  startDate?: string;
  expiryDate?: string;
}

export interface PucDetails {
  status: "valid" | "expired" | "not_available" | "unknown";
  certificateNumber?: string;
  issueDate?: string;
  expiryDate?: string;
  emissionNorm?: string;
}

export interface FinanceDetails {
  status: "active" | "closed" | "unknown";
  financier?: string;
  startDate?: string;
  closureDate?: string;
}

export interface ServiceRecord {
  id: string;
  serviceDate: string;
  odometerKm?: number;
  serviceType?: string;
  serviceCenter?: string;
  description?: string;
}

export interface OdometerRecord {
  observedAt: string;
  odometerKm: number;
  source: EvidenceSource;
}

export interface AccidentRecord {
  id: string;
  date?: string;
  severity?: "minor" | "moderate" | "major" | "unknown";
  description?: string;
  source: EvidenceSource;
}

export interface ChallanRecord {
  id: string;
  date?: string;
  status: "open" | "paid" | "cancelled" | "unknown";
  amount?: number;
  description?: string;
  source: EvidenceSource;
}

export interface ManufacturerDetails {
  manufacturer: string;
  model?: string;
  variant?: string;
  fuelType?: string;
  transmission?: string;
  manufacturingDate?: string;
  warrantyStatus?: "active" | "expired" | "unknown";
}

export interface VehicleData {
  registration?: VehicleRegistration;
  ownership?: OwnershipRecord[];
  insurance?: InsuranceDetails;
  puc?: PucDetails;
  finance?: FinanceDetails;
  serviceHistory?: ServiceRecord[];
  odometerHistory?: OdometerRecord[];
  accidentHistory?: AccidentRecord[];
  challans?: ChallanRecord[];
  manufacturer?: ManufacturerDetails;
}

export interface RiskItem {
  id: string;
  category: string;
  title: string;
  severity: RiskSeverity;
  status: RiskStatus;
  confidence: EvidenceConfidence;
  explanation: string;
  evidenceIds: string[];
  recommendedAction: string;
}

export interface TrustFactor {
  id: string;
  name: string;
  impact: "positive" | "negative" | "neutral";
  contribution: number;
  evidenceIds: string[];
}

export interface TrustAssessment {
  baseScore: number;
  calculatedScore: number;
  score: number;
  confidence: EvidenceConfidence;
  assessment: string;
  factors: TrustFactor[];
}

export type DecisionRecommendation =
  | "buy"
  | "review"
  | "avoid"
  | "insufficient_evidence";

export interface DecisionAssessment {
  recommendation: DecisionRecommendation;
  confidence: EvidenceConfidence;
  rationale: string;
  priorityRiskIds: string[];
}

export type AIGroundingStatus =
  | "grounded"
  | "partially_grounded"
  | "insufficient";

export interface AIKnowledgeReference {
  id: string;
  title: string;
  category: string;
  relevance: string;
}

export interface AIGrounding {
  status: AIGroundingStatus;
  evidenceCount: number;
  knowledgeCount: number;
}

export interface AIInterpretation {
  summary: string;
  reasoning: string;
  recommendation: string;
  supportingEvidenceIds: string[];
  knowledgeReferences: AIKnowledgeReference[];
  grounding: AIGrounding;
}

export interface VehicleIdentity {
  make: string;
  model: string;
  year: number;
  registration: string;
  vin: string;
}

export interface VehicleIntelligence {
  id: string;
  identity: VehicleIdentity;
  data?: VehicleData;
  evidence: EvidenceItem[];
  risks: RiskItem[];
  trust: TrustAssessment;
  decision: DecisionAssessment;
  ai: AIInterpretation;
}