"use client";

import { Suspense, useEffect, useState } from "react";
import { AlertCircle, CheckCircle2, ShieldCheck } from "lucide-react";
import { useRouter, useSearchParams } from "next/navigation";

import { ApiError, getVehicleByRegistration } from "@/lib/api/client";

const analysisSteps = [
  "Validating vehicle identity",
  "Collecting available evidence",
  "Evaluating risk signals",
  "Preparing vehicle intelligence",
];

const STEP_DURATION = 700;

type AnalysisState = "analyzing" | "not_found" | "error";

function AnalyzeContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const vehicle = searchParams.get("vehicle");

  const [activeStep, setActiveStep] = useState(0);
  const [state, setState] = useState<AnalysisState>("analyzing");
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    if (!vehicle?.trim()) {
      router.replace("/");
      return;
    }

    let cancelled = false;

    async function analyzeVehicle() {
      try {
        const vehicleData = await getVehicleByRegistration(vehicle!);

        if (cancelled) {
          return;
        }

        setActiveStep(analysisSteps.length - 1);

        const canonicalRegistration =
          vehicleData.identity.registration;

        window.setTimeout(() => {
          if (!cancelled) {
            router.replace(
              `/vehicles/${encodeURIComponent(canonicalRegistration)}`,
            );
          }
        }, 500);
      } catch (error) {
        if (cancelled) {
          return;
        }

        if (error instanceof ApiError && error.status === 404) {
          setState("not_found");
          setErrorMessage(
            `No vehicle was found for "${vehicle}".`,
          );
          return;
        }

        console.error("Vehicle analysis failed:", error);

        setState("error");
        setErrorMessage(
          "We could not complete the vehicle analysis. Please try again.",
        );
      }
    }

    analyzeVehicle();

    const progressTimer = window.setInterval(() => {
      setActiveStep((currentStep) => {
        if (currentStep >= analysisSteps.length - 1) {
          return currentStep;
        }

        return currentStep + 1;
      });
    }, STEP_DURATION);

    return () => {
      cancelled = true;
      window.clearInterval(progressTimer);
    };
  }, [router, vehicle]);

  if (state !== "analyzing") {
    return (
      <main className="min-h-screen bg-white text-zinc-950">
        <header className="border-b border-zinc-200">
          <div className="mx-auto flex h-16 max-w-7xl items-center px-6 lg:px-8">
            <div className="flex items-center gap-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-zinc-950 text-white">
                <ShieldCheck className="h-5 w-5" />
              </div>

              <span className="text-lg font-semibold tracking-tight">
                VehicleTrust AI
              </span>
            </div>
          </div>
        </header>

        <section className="flex min-h-[calc(100vh-4rem)] items-center justify-center px-6 py-20">
          <div className="w-full max-w-lg text-center">
            <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-zinc-100">
              <AlertCircle className="h-7 w-7 text-zinc-700" />
            </div>

            <p className="mt-8 text-sm font-semibold uppercase tracking-[0.16em] text-zinc-500">
              Vehicle analysis
            </p>

            <h1 className="mt-3 text-3xl font-semibold tracking-tight sm:text-4xl">
              {state === "not_found"
                ? "Vehicle not found"
                : "Analysis unavailable"}
            </h1>

            <p className="mx-auto mt-5 max-w-md text-base leading-7 text-zinc-600">
              {errorMessage}
            </p>

            <button
              type="button"
              onClick={() => router.push("/")}
              className="mt-8 inline-flex h-11 items-center justify-center rounded-xl bg-zinc-950 px-6 text-sm font-medium text-white transition-colors hover:bg-zinc-800"
            >
              Analyze another vehicle
            </button>
          </div>
        </section>
      </main>
    );
  }

  const progress =
    ((activeStep + 1) / analysisSteps.length) * 100;

  return (
    <main className="min-h-screen bg-white text-zinc-950">
      <header className="border-b border-zinc-200">
        <div className="mx-auto flex h-16 max-w-7xl items-center px-6 lg:px-8">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-zinc-950 text-white">
              <ShieldCheck className="h-5 w-5" />
            </div>

            <span className="text-lg font-semibold tracking-tight">
              VehicleTrust AI
            </span>
          </div>
        </div>
      </header>

      <section className="mx-auto flex min-h-[calc(100vh-4rem)] max-w-3xl items-center px-6 py-20 lg:px-8">
        <div className="w-full">
          <div className="text-center">
            <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-zinc-950 text-white">
              <ShieldCheck className="h-7 w-7" />
            </div>

            <p className="mt-8 text-sm font-semibold uppercase tracking-[0.16em] text-zinc-500">
              Vehicle analysis
            </p>

            <h1 className="mt-3 text-4xl font-semibold tracking-tight sm:text-5xl">
              Building your vehicle intelligence
            </h1>

            <p className="mx-auto mt-5 max-w-xl text-lg leading-8 text-zinc-600">
              We are validating the vehicle and evaluating the signals
              that matter before a purchase decision.
            </p>
          </div>

          <div className="mx-auto mt-12 max-w-xl rounded-3xl border border-zinc-200 bg-zinc-50 p-6 sm:p-8">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-zinc-700">
                Analysis progress
              </span>

              <span className="text-sm font-semibold text-zinc-950">
                {activeStep >= analysisSteps.length - 1
                  ? "Complete"
                  : "In progress"}
              </span>
            </div>

            <div className="mt-5 h-1.5 overflow-hidden rounded-full bg-zinc-200">
              <div
                className="h-full rounded-full bg-zinc-950 transition-all duration-500"
                style={{ width: `${progress}%` }}
              />
            </div>

            <div className="mt-7 space-y-4">
              {analysisSteps.map((step, index) => {
                const completed = index < activeStep;
                const active = index === activeStep;

                return (
                  <div
                    key={step}
                    className="flex items-center gap-3"
                  >
                    {completed ? (
                      <CheckCircle2 className="h-5 w-5 shrink-0 text-emerald-600" />
                    ) : active ? (
                      <span className="h-5 w-5 shrink-0 animate-pulse rounded-full border-2 border-zinc-950" />
                    ) : (
                      <span className="h-5 w-5 shrink-0 rounded-full border border-zinc-300" />
                    )}

                    <span
                      className={
                        completed || active
                          ? "text-sm font-medium text-zinc-900"
                          : "text-sm text-zinc-400"
                      }
                    >
                      {step}
                    </span>
                  </div>
                );
              })}
            </div>
          </div>

          <p className="mt-8 text-center text-xs text-zinc-400">
            Vehicle reference: {vehicle}
          </p>
        </div>
      </section>
    </main>
  );
}

function AnalyzeLoading() {
  return (
    <main className="min-h-screen bg-white text-zinc-950">
      <section className="flex min-h-screen items-center justify-center px-6">
        <div className="text-center">
          <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-zinc-950 text-white">
            <ShieldCheck className="h-7 w-7" />
          </div>

          <p className="mt-6 text-sm font-medium text-zinc-600">
            Preparing vehicle analysis…
          </p>
        </div>
      </section>
    </main>
  );
}

export default function AnalyzePage() {
  return (
    <Suspense fallback={<AnalyzeLoading />}>
      <AnalyzeContent />
    </Suspense>
  );
}