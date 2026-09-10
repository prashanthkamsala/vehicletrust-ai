import {
  AlertTriangle,
  ArrowLeft,
  CheckCircle2,
  ShieldCheck,
} from "lucide-react";
import Link from "next/link";
import { notFound } from "next/navigation";
import { RiskEvidence } from "@/components/vehicle/risk-evidence";
import { TrustScoreBreakdown } from "@/components/vehicle/trust-score-breakdown";
import { getDemoVehicle } from "@/lib/vehicle/mock-data";

type VehiclePageProps = {
  params: Promise<{ id: string }>;
};

export default async function VehiclePage({
  params,
}: VehiclePageProps) {
  const { id } = await params;

  if (id !== "demo-vehicle") {
    notFound();
  }

  const vehicle = getDemoVehicle();

  function getEvidenceForRisk(evidenceIds: string[]) {
    return evidenceIds
      .map((evidenceId) =>
        vehicle.evidence.find((item) => item.id === evidenceId),
      )
      .filter((item) => item !== undefined);
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
        <section className="rounded-3xl border border-zinc-200 bg-white shadow-sm">
          <div className="border-b border-zinc-200 px-6 py-7 sm:px-8">
            <p className="text-xs font-semibold uppercase tracking-[0.16em] text-zinc-500">
              Vehicle intelligence
            </p>

            <div className="mt-3 flex flex-col justify-between gap-5 sm:flex-row sm:items-end">
              <div>
                <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">
                  {vehicle.identity.year} {vehicle.identity.make}{" "}
                  {vehicle.identity.model}
                </h1>

                <p className="mt-2 text-sm text-zinc-500">
                  {vehicle.identity.registration} · VIN{" "}
                  {vehicle.identity.vin}
                </p>
              </div>

              <div className="inline-flex w-fit items-center gap-2 rounded-xl border border-zinc-200 bg-zinc-50 px-4 py-2.5 text-sm font-medium text-zinc-700">
                <ShieldCheck className="h-4 w-4" />
                {vehicle.trust.assessment}
              </div>
            </div>
          </div>

          <div className="grid lg:grid-cols-[300px_1fr]">
            <div className="border-b border-zinc-200 bg-zinc-50 p-8 lg:border-b-0 lg:border-r lg:p-10">
              <p className="text-xs font-semibold uppercase tracking-[0.16em] text-zinc-500">
                Trust score
              </p>

              <div className="mt-7 flex items-center justify-center">
                <div className="flex h-52 w-52 items-center justify-center rounded-full border-[12px] border-zinc-200">
                  <div className="text-center">
                    <div className="text-6xl font-semibold tracking-tight">
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
              </div>

              <div className="mt-7 flex items-center justify-center gap-2 text-sm font-medium text-zinc-700">
                <ShieldCheck className="h-4 w-4" />
                {vehicle.trust.assessment}
              </div>
            </div>

            <div className="p-6 sm:p-8 lg:p-10">
              <TrustScoreBreakdown
                baseScore={vehicle.trust.baseScore}
                score={vehicle.trust.score}
                factors={vehicle.trust.factors}
                evidence={vehicle.evidence}
              />

              <div className="mt-10 flex items-end justify-between gap-4">
                <div>
                  <p className="text-xs font-semibold uppercase tracking-[0.16em] text-zinc-500">
                    Evidence
                  </p>

                  <h2 className="mt-2 text-2xl font-semibold tracking-tight">
                    What we found
                  </h2>
                </div>

                <span className="hidden text-sm text-zinc-500 sm:block">
                  {vehicle.evidence.length} evidence items
                </span>
              </div>

              <div className="mt-7 grid gap-4 sm:grid-cols-2">
                {vehicle.evidence.map((evidence) => {
                  const verified = evidence.status === "verified";

                  return (
                    <article
                      key={evidence.id}
                      className="rounded-2xl border border-zinc-200 p-5"
                    >
                      <div className="flex items-start justify-between gap-4">
                        <div className="flex items-center gap-3">
                          {verified ? (
                            <CheckCircle2 className="h-5 w-5 shrink-0 text-emerald-600" />
                          ) : (
                            <AlertTriangle className="h-5 w-5 shrink-0 text-amber-600" />
                          )}

                          <div>
                            <p className="text-sm font-semibold">
                              {evidence.title}
                            </p>

                            <p className="mt-1 text-xs text-zinc-500">
                              {evidence.category}
                            </p>
                          </div>
                        </div>

                        <span
                          className={
                            verified
                              ? "text-sm font-semibold text-emerald-700"
                              : "text-sm font-semibold text-amber-700"
                          }
                        >
                          {evidence.value}
                        </span>
                      </div>

                      <p className="mt-4 text-sm leading-6 text-zinc-600">
                        {evidence.explanation}
                      </p>

                      <div className="mt-4 flex items-center justify-between border-t border-zinc-100 pt-3 text-xs text-zinc-500">
                        <span>
                          Confidence:{" "}
                          <span className="font-medium text-zinc-700">
                            {evidence.confidence}
                          </span>
                        </span>

                        <span>{evidence.source.name}</span>
                      </div>
                    </article>
                  );
                })}
              </div>

              <div className="mt-8">
                <div>
                  <p className="text-xs font-semibold uppercase tracking-[0.16em] text-zinc-500">
                    Risk assessment
                  </p>

                  <h2 className="mt-2 text-2xl font-semibold tracking-tight">
                    What needs attention
                  </h2>
                </div>

                <div className="mt-6 space-y-4">
                  {vehicle.risks.map((risk) => {
                    const linkedEvidence = getEvidenceForRisk(
                      risk.evidenceIds,
                    );

                    return (
                      <article
                        key={risk.id}
                        className="rounded-2xl border border-amber-200 bg-amber-50/50 p-5"
                      >
                        <div className="flex items-start gap-3">
                          <AlertTriangle className="mt-0.5 h-5 w-5 shrink-0 text-amber-600" />

                          <div className="min-w-0 flex-1">
                            <div className="flex flex-wrap items-center justify-between gap-3">
                              <div>
                                <p className="text-sm font-semibold text-zinc-950">
                                  {risk.title}
                                </p>

                                <p className="mt-1 text-xs text-zinc-500">
                                  {risk.category} · {risk.severity} risk
                                </p>
                              </div>

                              <span className="text-xs font-medium text-amber-700">
                                {risk.confidence} confidence
                              </span>
                            </div>

                            <p className="mt-4 text-sm leading-6 text-zinc-700">
                              {risk.explanation}
                            </p>

                            <div className="mt-5">
                              <RiskEvidence
                                evidence={linkedEvidence}
                              />
                            </div>

                            <div className="mt-4 rounded-xl bg-white/80 p-4">
                              <p className="text-xs font-semibold uppercase tracking-[0.12em] text-zinc-500">
                                Recommended action
                              </p>

                              <p className="mt-2 text-sm leading-6 text-zinc-700">
                                {risk.recommendedAction}
                              </p>
                            </div>
                          </div>
                        </div>
                      </article>
                    );
                  })}
                </div>
              </div>

              <div className="mt-8 rounded-2xl bg-zinc-950 p-6 text-white sm:p-7">
                <div className="flex items-center gap-2">
                  <ShieldCheck className="h-5 w-5" />

                  <h2 className="text-sm font-semibold">
                    AI interpretation
                  </h2>
                </div>

                <p className="mt-4 text-sm font-medium leading-7 text-white">
                  {vehicle.ai.summary}
                </p>

                <p className="mt-3 max-w-3xl text-sm leading-7 text-zinc-300">
                  {vehicle.ai.reasoning}
                </p>
              </div>

              <div className="mt-6 rounded-2xl border border-zinc-200 bg-zinc-50 p-6 sm:p-7">
                <p className="text-xs font-semibold uppercase tracking-[0.16em] text-zinc-500">
                  Recommendation
                </p>

                <h2 className="mt-2 text-xl font-semibold tracking-tight">
                  What to do next
                </h2>

                <p className="mt-3 max-w-3xl text-sm leading-7 text-zinc-600">
                  {vehicle.ai.recommendation}
                </p>
              </div>
            </div>
          </div>
        </section>

        <p className="mt-6 text-center text-xs text-zinc-400">
          Demo intelligence data · Evidence sources will be connected in a
          future release.
        </p>
      </div>
    </main>
  );
}