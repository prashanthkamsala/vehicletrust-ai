import type { TrustFactor, VehicleIntelligence } from "./types";
import { createTrustAssessment } from "./trust/score";

const demoTrustFactors: TrustFactor[] = [
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

const demoBaseScore = 35;

export const demoVehicle: VehicleIntelligence = {
  id: "demo-vehicle",

  identity: {
    make: "Toyota",
    model: "Camry",
    year: 2021,
    registration: "KA 01 AB 1234",
    vin: "DEMO1TOYOTA2021CAMRY",
  },

  evidence: [
    {
      id: "ownership-history",
      category: "Ownership",
      title: "Ownership history",
      value: "Strong",
      status: "verified",
      confidence: "high",
      explanation:
        "Ownership records show a consistent vehicle history.",
      source: {
        id: "registration-records",
        name: "Vehicle registration records",
        type: "registration",
      },
      observedAt: "2026-09-10",
    },

    {
      id: "accident-history",
      category: "Accident",
      title: "Accident signals",
      value: "Clear",
      status: "verified",
      confidence: "high",
      explanation:
        "No significant accident indicators were identified.",
      source: {
        id: "vehicle-history-records",
        name: "Vehicle history records",
        type: "vehicle_history",
      },
      observedAt: "2026-09-10",
    },

    {
      id: "service-history",
      category: "Maintenance",
      title: "Service history",
      value: "Review",
      status: "partially_verified",
      confidence: "medium",
      explanation:
        "Some maintenance records require additional verification.",
      source: {
        id: "service-records",
        name: "Service records",
        type: "maintenance",
      },
      observedAt: "2026-09-10",
    },

    {
      id: "mileage-consistency",
      category: "Mileage",
      title: "Mileage consistency",
      value: "Verified",
      status: "verified",
      confidence: "high",
      explanation:
        "Available mileage records appear consistent over time.",
      source: {
        id: "mileage-records",
        name: "Mileage records",
        type: "vehicle_history",
      },
      observedAt: "2026-09-10",
    },
  ],

  risks: [
    {
      id: "service-history-review",
      category: "Maintenance",
      title: "Service history requires review",
      severity: "medium",
      status: "needs_review",
      confidence: "medium",
      explanation:
        "Some maintenance records are incomplete or require additional verification.",
      evidenceIds: ["service-history"],
      recommendedAction:
        "Request the latest service invoices and maintenance records before purchase.",
    },
  ],

  trust: createTrustAssessment({
    baseScore: demoBaseScore,
    confidence: "high",
    assessment: "Low-risk profile",
    factors: demoTrustFactors,
  }),

  ai: {
    summary:
      "The available evidence indicates a relatively low-risk vehicle.",

    reasoning:
      "Ownership and accident indicators look healthy. Mileage records are consistent, while the service history contains a signal that deserves additional verification.",

    recommendation:
      "Proceed with additional service-history verification before making a purchase decision.",
  },
};

export function getDemoVehicle(): VehicleIntelligence {
  return demoVehicle;
}