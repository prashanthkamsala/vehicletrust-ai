import { describe, expect, it } from "vitest";
import type { TrustFactor } from "../types";
import {
  calculateTrustScore,
  createTrustAssessment,
  validateTrustScore,
} from "./score";

describe("calculateTrustScore", () => {
  it("calculates the score from the base score and positive factors", () => {
    const factors: TrustFactor[] = [
      {
        id: "ownership",
        name: "Ownership history",
        impact: "positive",
        contribution: 20,
        evidenceIds: ["ownership-history"],
      },
      {
        id: "accident",
        name: "Accident history",
        impact: "positive",
        contribution: 25,
        evidenceIds: ["accident-history"],
      },
    ];

    const score = calculateTrustScore({
      baseScore: 35,
      factors,
    });

    expect(score).toBe(80);
  });

  it("includes negative factors in the calculation", () => {
    const factors: TrustFactor[] = [
      {
        id: "service",
        name: "Service history",
        impact: "negative",
        contribution: -8,
        evidenceIds: ["service-history"],
      },
    ];

    const score = calculateTrustScore({
      baseScore: 35,
      factors,
    });

    expect(score).toBe(27);
  });

  it("returns the base score when there are no factors", () => {
    const score = calculateTrustScore({
      baseScore: 35,
      factors: [],
    });

    expect(score).toBe(35);
  });

  it("calculates the current demo vehicle score correctly", () => {
    const factors: TrustFactor[] = [
      {
        id: "ownership-factor",
        name: "Ownership history",
        impact: "positive",
        contribution: 20,
        evidenceIds: ["ownership-history"],
      },
      {
        id: "accident-factor",
        name: "Accident history",
        impact: "positive",
        contribution: 25,
        evidenceIds: ["accident-history"],
      },
      {
        id: "service-factor",
        name: "Service history",
        impact: "negative",
        contribution: -8,
        evidenceIds: ["service-history"],
      },
      {
        id: "mileage-factor",
        name: "Mileage consistency",
        impact: "positive",
        contribution: 15,
        evidenceIds: ["mileage-consistency"],
      },
    ];

    const score = calculateTrustScore({
      baseScore: 35,
      factors,
    });

    expect(score).toBe(87);
  });
});

describe("validateTrustScore", () => {
  const factors: TrustFactor[] = [
    {
      id: "ownership-factor",
      name: "Ownership history",
      impact: "positive",
      contribution: 20,
      evidenceIds: ["ownership-history"],
    },
    {
      id: "accident-factor",
      name: "Accident history",
      impact: "positive",
      contribution: 25,
      evidenceIds: ["accident-history"],
    },
    {
      id: "service-factor",
      name: "Service history",
      impact: "negative",
      contribution: -8,
      evidenceIds: ["service-history"],
    },
    {
      id: "mileage-factor",
      name: "Mileage consistency",
      impact: "positive",
      contribution: 15,
      evidenceIds: ["mileage-consistency"],
    },
  ];

  it("accepts a score that matches the calculated score", () => {
    expect(
      validateTrustScore(87, {
        baseScore: 35,
        factors,
      }),
    ).toBe(true);
  });

  it("rejects a score that does not match the calculated score", () => {
    expect(
      validateTrustScore(92, {
        baseScore: 35,
        factors,
      }),
    ).toBe(false);
  });
});

describe("createTrustAssessment", () => {
  it("creates a trust assessment with a calculated score", () => {
    const factors: TrustFactor[] = [
      {
        id: "ownership",
        name: "Ownership history",
        impact: "positive",
        contribution: 20,
        evidenceIds: ["ownership-history"],
      },
      {
        id: "service",
        name: "Service history",
        impact: "negative",
        contribution: -8,
        evidenceIds: ["service-history"],
      },
    ];

    const assessment = createTrustAssessment({
      baseScore: 35,
      factors,
      confidence: "high",
      assessment: "Low-risk profile",
    });

    expect(assessment).toEqual({
      baseScore: 35,
      score: 47,
      confidence: "high",
      assessment: "Low-risk profile",
      factors,
    });
  });
});