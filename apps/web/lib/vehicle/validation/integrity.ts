import { calculateTrustScore } from "../trust/score";
import type { VehicleIntelligence } from "../types";

export type IntegrityIssue = {
  code:
    | "DUPLICATE_EVIDENCE_ID"
    | "MISSING_FACTOR_EVIDENCE"
    | "MISSING_RISK_EVIDENCE"
    | "TRUST_SCORE_MISMATCH";
  message: string;
  path: string;
};

export function validateVehicleIntelligence(
  vehicle: VehicleIntelligence,
): IntegrityIssue[] {
  const issues: IntegrityIssue[] = [];

  const evidenceIds = new Set<string>();

  vehicle.evidence.forEach((evidence, index) => {
    if (evidenceIds.has(evidence.id)) {
      issues.push({
        code: "DUPLICATE_EVIDENCE_ID",
        message: `Evidence ID "${evidence.id}" is duplicated.`,
        path: `evidence[${index}].id`,
      });

      return;
    }

    evidenceIds.add(evidence.id);
  });

  vehicle.trust.factors.forEach((factor, factorIndex) => {
    factor.evidenceIds.forEach((evidenceId, evidenceIndex) => {
      if (!evidenceIds.has(evidenceId)) {
        issues.push({
          code: "MISSING_FACTOR_EVIDENCE",
          message: `Trust factor "${factor.name}" references missing evidence "${evidenceId}".`,
          path: `trust.factors[${factorIndex}].evidenceIds[${evidenceIndex}]`,
        });
      }
    });
  });

  vehicle.risks.forEach((risk, riskIndex) => {
    risk.evidenceIds.forEach((evidenceId, evidenceIndex) => {
      if (!evidenceIds.has(evidenceId)) {
        issues.push({
          code: "MISSING_RISK_EVIDENCE",
          message: `Risk "${risk.title}" references missing evidence "${evidenceId}".`,
          path: `risks[${riskIndex}].evidenceIds[${evidenceIndex}]`,
        });
      }
    });
  });

  const calculatedScore = calculateTrustScore({
    baseScore: vehicle.trust.baseScore,
    factors: vehicle.trust.factors,
  });

  if (vehicle.trust.score !== calculatedScore) {
    issues.push({
      code: "TRUST_SCORE_MISMATCH",
      message: `Trust score ${vehicle.trust.score} does not match the calculated score ${calculatedScore}.`,
      path: "trust.score",
    });
  }

  return issues;
}

export function isVehicleIntelligenceValid(
  vehicle: VehicleIntelligence,
): boolean {
  return validateVehicleIntelligence(vehicle).length === 0;
}
