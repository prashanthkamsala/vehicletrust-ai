export type VehicleSignalStatus = "positive" | "warning" | "negative";

export interface VehicleSignal {
  id: string;
  category: string;
  label: string;
  value: string;
  status: VehicleSignalStatus;
  explanation: string;
}

export interface VehicleIntelligence {
  id: string;
  identity: {
    make: string;
    model: string;
    year: number;
    registration: string;
    vin: string;
  };
  trustScore: {
    value: number;
    confidence: string;
    assessment: string;
  };
  signals: VehicleSignal[];
  aiAssessment: string;
  recommendation: string;
}

export const demoVehicle: VehicleIntelligence = {
  id: "demo-vehicle",
  identity: {
    make: "Toyota",
    model: "Camry",
    year: 2021,
    registration: "KA 01 AB 1234",
    vin: "DEMO1TOYOTA2021CAMRY",
  },
  trustScore: {
    value: 87,
    confidence: "High confidence",
    assessment: "Low-risk profile",
  },
  signals: [
    {
      id: "ownership",
      category: "Ownership",
      label: "Ownership history",
      value: "Strong",
      status: "positive",
      explanation: "Ownership records show a consistent vehicle history.",
    },
    {
      id: "accident",
      category: "Accident",
      label: "Accident signals",
      value: "Clear",
      status: "positive",
      explanation: "No significant accident indicators were identified.",
    },
    {
      id: "service",
      category: "Maintenance",
      label: "Service history",
      value: "Review",
      status: "warning",
      explanation: "Some maintenance records require additional verification.",
    },
    {
      id: "mileage",
      category: "Mileage",
      label: "Mileage consistency",
      value: "Verified",
      status: "positive",
      explanation: "Available mileage records appear consistent over time.",
    },
  ],
  aiAssessment:
    "The available signals indicate a relatively low-risk vehicle. Ownership and accident indicators look healthy, while the service history deserves additional verification before purchase.",
  recommendation:
    "Proceed with additional service-history verification before making a purchase decision.",
};

export function getDemoVehicle(): VehicleIntelligence {
  return demoVehicle;
}
