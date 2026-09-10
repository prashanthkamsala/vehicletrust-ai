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
  score: number;
  confidence: EvidenceConfidence;
  assessment: string;
  factors: TrustFactor[];
}

export interface AIInterpretation {
  summary: string;
  reasoning: string;
  recommendation: string;
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
  evidence: EvidenceItem[];
  risks: RiskItem[];
  trust: TrustAssessment;
  ai: AIInterpretation;
}
