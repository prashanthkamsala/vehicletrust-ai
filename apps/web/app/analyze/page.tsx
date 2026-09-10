"use client";

import { useEffect, useState } from "react";
import { CheckCircle2, ShieldCheck } from "lucide-react";
import { useRouter, useSearchParams } from "next/navigation";

const analysisSteps = [
  "Validating vehicle identity",
  "Collecting available evidence",
  "Evaluating risk signals",
  "Preparing vehicle intelligence",
];

const STEP_DURATION = 900;

export default function AnalyzePage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const vehicle = searchParams.get("vehicle");

  const [activeStep, setActiveStep] = useState(0);

  useEffect(() => {
    if (!vehicle?.trim()) {
      router.replace("/");
      return;
    }

    const timer = window.setInterval(() => {
      setActiveStep((currentStep) => {
        if (currentStep >= analysisSteps.length - 1) {
          window.clearInterval(timer);

          window.setTimeout(() => {
            router.replace("/vehicles/demo-vehicle");
          }, 700);

          return currentStep;
        }

        return currentStep + 1;
      });
    }, STEP_DURATION);

    return () => window.clearInterval(timer);
  }, [router, vehicle]);

  const completedSteps = Math.min(activeStep, analysisSteps.length - 1);
  const progress =
    ((completedSteps + 1) / analysisSteps.length) * 100;

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
              We are validating the vehicle and evaluating the signals that
              matter before a purchase decision.
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
                className="h-full rounded-full bg-zinc-950 transition-all duration-700"
                style={{ width: `${progress}%` }}
              />
            </div>

            <div className="mt-7 space-y-4">
              {analysisSteps.map((step, index) => {
                const completed = index < activeStep;
                const active = index === activeStep;

                return (
                  <div key={step} className="flex items-center gap-3">
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
