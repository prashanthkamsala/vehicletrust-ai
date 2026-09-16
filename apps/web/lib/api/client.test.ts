import { beforeEach, describe, expect, it, vi } from "vitest";

import { ApiError, getVehicle } from "./client";

describe("getVehicle", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it("returns vehicle intelligence for a successful response", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(
        JSON.stringify({
          id: "demo-vehicle",
          identity: {
            make: "Toyota",
            model: "Camry",
            year: 2021,
            registration: "KA 01 AB 1234",
            vin: "DEMO1TOYOTA2021CAMRY",
          },
          evidence: [],
          risks: [],
          trust: {
            baseScore: 35,
            score: 87,
            confidence: "high",
            assessment: "Low-risk profile",
            factors: [],
          },
          ai: {
            summary: "Low-risk vehicle.",
            reasoning: "Evidence looks healthy.",
            recommendation: "Verify service history.",
          },
        }),
        {
          status: 200,
          headers: {
            "Content-Type": "application/json",
          },
        },
      ),
    );

    const vehicle = await getVehicle("demo-vehicle");

    expect(vehicle.id).toBe("demo-vehicle");
    expect(vehicle.trust.score).toBe(87);
  });

  it("throws ApiError when the API returns an error", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(
        JSON.stringify({
          detail: 'Vehicle "unknown-vehicle" not found.',
        }),
        {
          status: 404,
          headers: {
            "Content-Type": "application/json",
          },
        },
      ),
    );

    await expect(getVehicle("unknown-vehicle")).rejects.toEqual(
      expect.objectContaining({
        name: "ApiError",
        status: 404,
        message: 'Vehicle "unknown-vehicle" not found.',
      }),
    );

    expect(ApiError).toBeDefined();
  });
});
