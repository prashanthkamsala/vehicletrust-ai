import type {
  EvidenceConfidence,
  EvidenceItem,
  EvidenceStatus,
} from "../types";

export type EvidenceQuality = {
  label: string;
  description: string;
  status: EvidenceStatus;
  confidence: EvidenceConfidence;
};

export function getEvidenceQuality(
  evidence: EvidenceItem,
): EvidenceQuality {
  if (evidence.status === "conflicting") {
    return {
      label: "Conflicting evidence",
      description:
        "Available sources contain conflicting information that requires resolution.",
      status: evidence.status,
      confidence: evidence.confidence,
    };
  }

  if (evidence.status === "unverified") {
    return {
      label: "Unverified evidence",
      description:
        "This information is available but has not been sufficiently validated.",
      status: evidence.status,
      confidence: evidence.confidence,
    };
  }

  if (evidence.status === "partially_verified") {
    return {
      label: "Partially verified",
      description:
        "Some aspects of this information are supported, but additional verification is required.",
      status: evidence.status,
      confidence: evidence.confidence,
    };
  }

  return {
    label: "Verified evidence",
    description:
      "Available records support this information without a known conflict.",
    status: evidence.status,
    confidence: evidence.confidence,
  };
}
