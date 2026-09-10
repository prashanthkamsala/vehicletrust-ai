import { describe, expect, it } from "vitest";
import { getEvidenceQuality } from "./quality";
import type { EvidenceItem } from "../types";

function createEvidence(
  status: EvidenceItem["status"],
  confidence: EvidenceItem["confidence"],
): EvidenceItem {
  return {
    id: "test-evidence",
    category: "Test",
    title: "Test evidence",
    value: "Test",
    status,
    confidence,
    explanation: "Test explanation.",
    source: {
      id: "test-source",
      name: "Test source",
      type: "test",
    },
  };
}

describe("getEvidenceQuality", () => {
  it("describes verified evidence", () => {
    const result = getEvidenceQuality(
      createEvidence("verified", "high"),
    );

    expect(result.label).toBe("Verified evidence");
    expect(result.status).toBe("verified");
    expect(result.confidence).toBe("high");
  });

  it("describes partially verified evidence", () => {
    const result = getEvidenceQuality(
      createEvidence("partially_verified", "medium"),
    );

    expect(result.label).toBe("Partially verified");
    expect(result.status).toBe("partially_verified");
    expect(result.confidence).toBe("medium");
  });

  it("describes unverified evidence", () => {
    const result = getEvidenceQuality(
      createEvidence("unverified", "low"),
    );

    expect(result.label).toBe("Unverified evidence");
    expect(result.status).toBe("unverified");
    expect(result.confidence).toBe("low");
  });

  it("describes conflicting evidence", () => {
    const result = getEvidenceQuality(
      createEvidence("conflicting", "medium"),
    );

    expect(result.label).toBe("Conflicting evidence");
    expect(result.status).toBe("conflicting");
    expect(result.confidence).toBe("medium");
  });
});
