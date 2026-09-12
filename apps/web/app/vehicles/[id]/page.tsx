import { ArrowLeft, ShieldCheck } from "lucide-react";
import Link from "next/link";
import { notFound } from "next/navigation";
import { getVehicleByRegistration } from "@/lib/api/client";
import type { VehicleIntelligence } from "@/lib/vehicle/types";
import { TrustBreakdown } from "@/components/vehicle/trust-breakdown";
import { EvidenceExplorer } from "@/components/vehicle/evidence-explorer";

type VehiclePageProps = {
  params: Promise<{ id: string }>;
};

export default async function VehiclePage({
  params,
}: VehiclePageProps) {
  const { id } = await params;
  const registration = decodeURIComponent(id);

  let vehicle: VehicleIntelligence;

  try {
    vehicle = await getVehicleByRegistration(registration);
  } catch (error) {
    if (error instanceof Error && "status" in error && error.status === 404) {
      notFound();
    }

    throw error;
  }

  return (
    <main className="min-h-screen bg-zinc-50 text-zinc-950">
      <header className="border-b border-zinc-200 bg-white">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6 lg:px-8">
          <Link
            href="/"
            className="inline-flex items-center gap-2 text-sm font-medium text-zinc-600 transition-colors hover:text-zinc-950"
          >
            <ArrowLeft className="h-4 w-4" />
            VehicleTrust AI
          </Link>

          <div className="inline-flex items-center gap-2 rounded-full border border-zinc-200 bg-zinc-50 px-3 py-1.5 text-xs font-medium text-zinc-700">
            <span className="h-2 w-2 rounded-full bg-emerald-500" />
            Analysis complete
          </div>
        </div>
      </header>

      <div className="mx-auto max-w-7xl px-6 py-10 lg:px-8 lg:py-14">
        <section className="overflow-hidden rounded-3xl border border-zinc-200 bg-white shadow-sm">
          <div className="border-b border-zinc-200 px-6 py-7 sm:px-8 lg:px-10">
            <div className="flex flex-col gap-6 lg:flex-row lg:items-start lg:justify-between">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.16em] text-zinc-500">
                  Vehicle intelligence
                </p>

                <h1 className="mt-3 text-3xl font-semibold tracking-tight text-zinc-950 sm:text-4xl">
                  {vehicle.identity.year} {vehicle.identity.make}{" "}
                  {vehicle.identity.model}
                </h1>

                <div className="mt-3 flex flex-wrap items-center gap-x-3 gap-y-1 text-sm text-zinc-500">
                  <span>{vehicle.identity.registration}</span>
                  <span className="text-zinc-300">•</span>
                  <span>VIN {vehicle.identity.vin}</span>
                </div>
              </div>

              <div className="inline-flex w-fit items-center gap-2 rounded-full border border-zinc-200 bg-zinc-50 px-4 py-2 text-sm font-medium text-zinc-700">
                <ShieldCheck className="h-4 w-4" />
                {vehicle.trust.assessment}
              </div>
            </div>
          </div>

          <div className="grid lg:grid-cols-[320px_1fr]">
            <div className="flex flex-col items-center justify-center border-b border-zinc-200 bg-zinc-50 px-6 py-10 lg:border-b-0 lg:border-r lg:px-10">
              <p className="text-xs font-semibold uppercase tracking-[0.16em] text-zinc-500">
                Trust score
              </p>

              <div className="mt-6 flex h-52 w-52 items-center justify-center rounded-full border-[12px] border-zinc-200 bg-white">
                <div className="text-center">
                  <div className="text-6xl font-semibold tracking-tight text-zinc-950">
                    {vehicle.trust.score}
                  </div>

                  <div className="mt-2 text-xs font-semibold uppercase tracking-[0.18em] text-zinc-500">
                    / 100
                  </div>

                  <div className="mt-3 text-xs text-zinc-500">
                    {vehicle.trust.confidence} confidence
                  </div>
                </div>
              </div>

              <div className="mt-6 inline-flex items-center gap-2 text-sm font-medium text-zinc-700">
                <ShieldCheck className="h-4 w-4" />
                {vehicle.trust.assessment}
              </div>
            </div>

            <div className="p-6 sm:p-8 lg:p-10">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.16em] text-zinc-500">
                  AI assessment
                </p>

                <h2 className="mt-2 text-2xl font-semibold tracking-tight text-zinc-950">
                  What the available evidence tells us
                </h2>

                <p className="mt-5 max-w-3xl text-base font-medium leading-7 text-zinc-800">
                  {vehicle.ai.summary}
                </p>

                <p className="mt-4 max-w-3xl text-sm leading-7 text-zinc-600">
                  {vehicle.ai.reasoning}
                </p>
              </div>

              <div className="mt-8 grid gap-3 sm:grid-cols-3">
                <div className="rounded-2xl border border-zinc-200 bg-zinc-50 p-4">
                  <p className="text-xs font-semibold uppercase tracking-[0.12em] text-zinc-500">
                    Evidence
                  </p>
                  <p className="mt-2 text-2xl font-semibold text-zinc-950">
                    {vehicle.evidence.length}
                  </p>
                  <p className="mt-1 text-xs text-zinc-500">
                    evidence items analyzed
                  </p>
                </div>

                <div className="rounded-2xl border border-zinc-200 bg-zinc-50 p-4">
                  <p className="text-xs font-semibold uppercase tracking-[0.12em] text-zinc-500">
                    Risks
                  </p>
                  <p className="mt-2 text-2xl font-semibold text-zinc-950">
                    {vehicle.risks.length}
                  </p>
                  <p className="mt-1 text-xs text-zinc-500">
                    issues requiring attention
                  </p>
                </div>

                <div className="rounded-2xl border border-zinc-200 bg-zinc-50 p-4">
                  <p className="text-xs font-semibold uppercase tracking-[0.12em] text-zinc-500">
                    Confidence
                  </p>
                  <p className="mt-2 text-2xl font-semibold capitalize text-zinc-950">
                    {vehicle.trust.confidence}
                  </p>
                  <p className="mt-1 text-xs text-zinc-500">
                    evidence confidence
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div className="border-t border-zinc-200 bg-zinc-50 px-6 py-4 sm:px-8 lg:px-10">
            <div className="flex flex-col gap-2 text-xs text-zinc-500 sm:flex-row sm:items-center sm:justify-between">
              <span>
                Assessment generated from available vehicle evidence
              </span>

              <span>
                {vehicle.evidence.length} evidence items · {vehicle.risks.length} risks
              </span>
            </div>
          </div>
        </section>
        <TrustBreakdown
          baseScore={vehicle.trust.baseScore}
          calculatedScore={vehicle.trust.calculatedScore}
          score={vehicle.trust.score}
          assessment={vehicle.trust.assessment}
          confidence={vehicle.trust.confidence}
          factors={vehicle.trust.factors}
        />
        <div className="mt-6">
          <EvidenceExplorer evidence={vehicle.evidence} />
        </div>

        <p className="mt-6 text-center text-xs text-zinc-400">
          Assessment generated from available vehicle evidence.
        </p>
      </div>
    </main>
  );
}