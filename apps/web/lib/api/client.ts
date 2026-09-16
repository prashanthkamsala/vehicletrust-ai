import type { VehicleIntelligence } from "../vehicle/types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

export class ApiError extends Error {
  readonly status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

export async function getVehicle(
  vehicleId: string,
): Promise<VehicleIntelligence> {
  const response = await fetch(
    `${API_BASE_URL}/api/v1/vehicles/${encodeURIComponent(vehicleId)}`,
  );

  if (!response.ok) {
    let message = `Request failed with status ${response.status}.`;

    try {
      const errorBody = (await response.json()) as {
        detail?: string;
      };

      if (errorBody.detail) {
        message = errorBody.detail;
      }
    } catch {
      // Keep the default HTTP error message when the response is not JSON.
    }

    throw new ApiError(message, response.status);
  }

  return (await response.json()) as VehicleIntelligence;
}

export async function getVehicleByRegistration(
  registration: string,
): Promise<VehicleIntelligence> {
  const response = await fetch(
    `${API_BASE_URL}/api/v1/vehicles/lookup?registration=${encodeURIComponent(
      registration,
    )}`,
  );

  if (!response.ok) {
    let message = `Request failed with status ${response.status}.`;

    try {
      const errorBody = (await response.json()) as {
        detail?: string;
      };

      if (errorBody.detail) {
        message = errorBody.detail;
      }
    } catch {
      // Keep the default HTTP error message when the response is not JSON.
    }

    throw new ApiError(message, response.status);
  }

  return (await response.json()) as VehicleIntelligence;
}