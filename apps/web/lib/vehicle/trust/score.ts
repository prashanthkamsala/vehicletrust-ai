import type {
  EvidenceConfidence,
  TrustAssessment,
  TrustFactor,
} from "../types";

export interface TrustScoreInput {
  baseScore: number;
  factors: TrustFactor[];
}

export interface TrustAssessmentInput extends TrustScoreInput {
  confidence: EvidenceConfidence;
  assessment: string;
}

export function calculateTrustScore({
  baseScore,
  factors,
}: TrustScoreInput): number {
  return factors.reduce(
    (score, factor) => score + factor.contribution,
    baseScore,
  );
}

export function validateTrustScore(
  declaredScore: number,
  input: TrustScoreInput,
): boolean {
  return declaredScore === calculateTrustScore(input);
}

export function createTrustAssessment({
  baseScore,
  factors,
  confidence,
  assessment,
}: TrustAssessmentInput): TrustAssessment {
  const score = calculateTrustScore({
    baseScore,
    factors,
  });

  return {
    baseScore,
    score,
    confidence,
    assessment,
    factors,
  };
}