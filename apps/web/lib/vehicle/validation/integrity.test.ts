import { describe, expect, it } from "vitest";
import { demoVehicle } from "../mock-data";
import {
  isVehicleIntelligenceValid,
  validateVehicleIntelligence,
} from "./integrity";

describe("validateVehicleIntelligence", () => {
  it("accepts the current demo vehicle", () => {
    const issues = validateVehicleIntelligence(demoVehicle);

    expect(issues).toEqual([]);
    expect(isVehicleIntelligenceValid(demoVehicle)).toBe(true);
  });

  it("detects duplicate evidence IDs", () => {
    const vehicle = structuredClone(demoVehicle);

    vehicle.evidence.push({
      ...vehicle.evidence[0],
    });

    const issues = validateVehicleIntelligence(vehicle);

    expect(
      issues.some(
        (issue) => issue.code === "DUPLICATE_EVIDENCE_ID",
      ),
    ).toBe(true);
  });

  it("detects missing evidence referenced by a trust factor", () => {
    const vehicle = structuredClone(demoVehicle);

    vehicle.trust.factors[0].evidenceIds = [
      "missing-evidence",
    ];

    const issues = validateVehicleIntelligence(vehicle);

    expect(
      issues.some(
        (issue) => issue.code === "MISSING_FACTOR_EVIDENCE",
      ),
    ).toBe(true);
  });

  it("detects missing evidence referenced by a risk", () => {
    const vehicle = structuredClone(demoVehicle);

    vehicle.risks[0].evidenceIds = ["missing-evidence"];

    const issues = validateVehicleIntelligence(vehicle);

    expect(
      issues.some(
        (issue) => issue.code === "MISSING_RISK_EVIDENCE",
      ),
    ).toBe(true);
  });

  it("detects a trust score mismatch", () => {
    const vehicle = structuredClone(demoVehicle);

    vehicle.trust.score = 99;

    const issues = validateVehicleIntelligence(vehicle);

    expect(
      issues.some(
        (issue) => issue.code === "TRUST_SCORE_MISMATCH",
      ),
    ).toBe(true);
  });
});
