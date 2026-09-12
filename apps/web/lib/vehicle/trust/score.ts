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
  const calculatedScore = calculateTrustScore({
    baseScore,
    factors,
  });

  const score = Math.min(100, Math.max(0, calculatedScore));

  return {
    baseScore,
    calculatedScore,
    score,
    confidence,
    assessment,
    factors,
  };
}