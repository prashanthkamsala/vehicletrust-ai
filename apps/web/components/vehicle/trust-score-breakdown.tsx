import {
  AlertCircle,
  CheckCircle2,
  ChevronDown,
  ExternalLink,
  Minus,
  Plus,
} from "lucide-react";
import type {
  EvidenceItem,
  TrustFactor,
} from "@/lib/vehicle/types";
import { getEvidenceQuality } from "@/lib/vehicle/evidence/quality";

type TrustScoreBreakdownProps = {
  baseScore: number;
  score: number;
  factors: TrustFactor[];
  evidence: EvidenceItem[];
};

export function TrustScoreBreakdown({
  baseScore,
  score,
  factors,
  evidence,
}: TrustScoreBreakdownProps) {
  const contributionTotal = factors.reduce(
    (total, factor) => total + factor.contribution,
    0,
  );

  function getEvidenceForFactor(factor: TrustFactor) {
    return factor.evidenceIds
      .map((evidenceId) =>
        evidence.find((item) => item.id === evidenceId),
      )
      .filter(
        (item): item is EvidenceItem => item !== undefined,
      );
  }

  return (
    <section className="rounded-2xl border border-zinc-200 bg-white p-6 sm:p-7">
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.16em] text-zinc-500">
          Score explanation
        </p>

        <h2 className="mt-2 text-xl font-semibold tracking-tight">
          Why this score?
        </h2>

        <p className="mt-2 max-w-2xl text-sm leading-6 text-zinc-600">
          Your Trust Score is calculated from the underlying vehicle
          signals and their contribution to the overall assessment.
        </p>
      </div>

      <div className="mt-6 divide-y divide-zinc-100 rounded-xl border border-zinc-200">
        {factors.map((factor) => {
          const positive = factor.impact === "positive";
          const negative = factor.impact === "negative";
          const linkedEvidence = getEvidenceForFactor(factor);

          return (
            <details
              key={factor.id}
              className="group"
            >
              <summary className="flex cursor-pointer list-none items-center justify-between gap-4 p-4 outline-none transition-colors hover:bg-zinc-50 focus-visible:bg-zinc-50 [&::-webkit-details-marker]:hidden">
                <div className="flex min-w-0 items-center gap-3">
                  {positive ? (
                    <CheckCircle2 className="h-5 w-5 shrink-0 text-emerald-600" />
                  ) : negative ? (
                    <AlertCircle className="h-5 w-5 shrink-0 text-amber-600" />
                  ) : (
                    <Minus className="h-5 w-5 shrink-0 text-zinc-400" />
                  )}

                  <div className="min-w-0">
                    <p className="text-sm font-medium text-zinc-900">
                      {factor.name}
                    </p>

                    <p className="mt-1 text-xs text-zinc-500">
                      {linkedEvidence.length} linked evidence{" "}
                      {linkedEvidence.length === 1 ? "item" : "items"}
                    </p>
                  </div>
                </div>

                <div className="flex shrink-0 items-center gap-3">
                  <span
                    className={
                      positive
                        ? "inline-flex items-center gap-1 text-sm font-semibold text-emerald-700"
                        : negative
                          ? "inline-flex items-center gap-1 text-sm font-semibold text-amber-700"
                          : "inline-flex items-center gap-1 text-sm font-semibold text-zinc-500"
                    }
                  >
                    {factor.contribution > 0 ? (
                      <Plus className="h-3.5 w-3.5" />
                    ) : null}

                    {factor.contribution}
                  </span>

                  <ChevronDown className="h-4 w-4 text-zinc-400 transition-transform group-open:rotate-180" />
                </div>
              </summary>

              <div className="border-t border-zinc-100 bg-zinc-50/60 px-4 pb-4 pt-4">
                {linkedEvidence.length > 0 ? (
                  <div className="space-y-3">
                    <p className="text-xs font-semibold uppercase tracking-[0.14em] text-zinc-500">
                      Supporting evidence
                    </p>

                    {linkedEvidence.map((item) => {
                      const quality = getEvidenceQuality(item);
                      const verified = item.status === "verified";

                      return (
                        <div
                          key={item.id}
                          className="rounded-xl border border-zinc-200 bg-white p-4"
                        >
                          <div className="flex items-start justify-between gap-4">
                            <div className="flex min-w-0 items-start gap-3">
                              {verified ? (
                                <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-emerald-600" />
                              ) : (
                                <AlertCircle className="mt-0.5 h-4 w-4 shrink-0 text-amber-600" />
                              )}

                              <div className="min-w-0">
                                <p className="text-sm font-semibold text-zinc-900">
                                  {item.title}
                                </p>

                                <p className="mt-1 text-xs text-zinc-500">
                                  {item.category} · {quality.label}
                                </p>
                              </div>
                            </div>

                            <span
                              className={
                                verified
                                  ? "shrink-0 text-xs font-semibold text-emerald-700"
                                  : "shrink-0 text-xs font-semibold text-amber-700"
                              }
                            >
                              {quality.confidence} confidence
                            </span>
                          </div>

                          <p className="mt-3 text-sm leading-6 text-zinc-600">
                            {item.explanation}
                          </p>

                          <div className="mt-3 rounded-lg bg-zinc-50 p-3">
                            <p className="text-xs leading-5 text-zinc-600">
                              {quality.description}
                            </p>
                          </div>

                          <div className="mt-4 flex flex-wrap items-center justify-between gap-3 border-t border-zinc-100 pt-3">
                            <div>
                              <p className="text-[11px] font-semibold uppercase tracking-[0.12em] text-zinc-400">
                                Source
                              </p>

                              <p className="mt-1 text-xs font-medium text-zinc-700">
                                {item.source.name}
                              </p>
                            </div>

                            <span className="inline-flex items-center gap-1 text-xs text-zinc-400">
                              {item.source.type}
                              <ExternalLink className="h-3 w-3" />
                            </span>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                ) : (
                  <p className="text-sm text-zinc-500">
                    No supporting evidence is currently linked to this
                    factor.
                  </p>
                )}
              </div>
            </details>
          );
        })}
      </div>

      <div className="mt-5 rounded-xl bg-zinc-50 p-4">
        <div className="flex items-center justify-between text-sm">
          <span className="text-zinc-600">Base score</span>

          <span className="font-medium text-zinc-900">
            {baseScore}
          </span>
        </div>

        <div className="mt-3 flex items-center justify-between text-sm">
          <span className="text-zinc-600">
            Factor contribution
          </span>

          <span className="font-medium text-zinc-900">
            {contributionTotal > 0 ? "+" : ""}
            {contributionTotal}
          </span>
        </div>

        <div className="mt-4 flex items-center justify-between border-t border-zinc-200 pt-4">
          <span className="font-semibold text-zinc-950">
            Trust score
          </span>

          <span className="text-lg font-semibold text-zinc-950">
            {score}
          </span>
        </div>
      </div>
    </section>
  );
}