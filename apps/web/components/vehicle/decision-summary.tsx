"use client";

import {
  AlertTriangle,
  CheckCircle2,
  CircleAlert,
  ShieldAlert,
} from "lucide-react";

import type {
  DecisionRecommendation,
  RiskItem,
  RiskSeverity,
} from "@/lib/vehicle/types";

type DecisionSummaryProps = {
  recommendation: DecisionRecommendation;
  confidence: "high" | "medium" | "low";
  rationale: string;
  priorityRiskIds: string[];
  risks: RiskItem[];
};

const recommendationConfig: Record<
  DecisionRecommendation,
  {
    label: string;
    description: string;
    icon: typeof CheckCircle2;
    containerClassName: string;
    badgeClassName: string;
    iconClassName: string;
  }
> = {
  buy: {
    label: "Buy",
    description: "The available evidence supports moving forward.",
    icon: CheckCircle2,
    containerClassName: "border-emerald-200 bg-emerald-50/60",
    badgeClassName: "bg-emerald-100 text-emerald-800",
    iconClassName: "text-emerald-600",
  },
  review: {
    label: "Review",
    description: "The vehicle needs further verification before purchase.",
    icon: CircleAlert,
    containerClassName: "border-amber-200 bg-amber-50/60",
    badgeClassName: "bg-amber-100 text-amber-800",
    iconClassName: "text-amber-600",
  },
  avoid: {
    label: "Avoid",
    description: "The current evidence presents significant purchase risk.",
    icon: ShieldAlert,
    containerClassName: "border-red-200 bg-red-50/60",
    badgeClassName: "bg-red-100 text-red-800",
    iconClassName: "text-red-600",
  },
  insufficient_evidence: {
    label: "Insufficient evidence",
    description:
      "There is not enough reliable evidence to make a purchase decision.",
    icon: AlertTriangle,
    containerClassName: "border-zinc-200 bg-zinc-50",
    badgeClassName: "bg-zinc-100 text-zinc-700",
    iconClassName: "text-zinc-500",
  },
};

const severityClassName: Record<RiskSeverity, string> = {
  critical: "bg-red-100 text-red-800",
  high: "bg-red-50 text-red-700",
  medium: "bg-amber-50 text-amber-700",
  low: "bg-zinc-100 text-zinc-600",
};

export function DecisionSummary({
  recommendation,
  confidence,
  rationale,
  priorityRiskIds,
  risks,
}: DecisionSummaryProps) {
  const config = recommendationConfig[recommendation];
  const RecommendationIcon = config.icon;

  const priorityRisks = priorityRiskIds
    .map((riskId) => risks.find((risk) => risk.id === riskId))
    .filter((risk): risk is RiskItem => risk !== undefined);

  return (
    <section
      aria-labelledby="decision-summary-title"
      className={`rounded-3xl border p-6 sm:p-8 ${config.containerClassName}`}
    >
      <div className="flex flex-col gap-6">
        <div className="flex flex-col gap-5 sm:flex-row sm:items-start sm:justify-between">
          <div className="flex items-start gap-4">
            <div
              className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-white shadow-sm ${config.iconClassName}`}
            >
              <RecommendationIcon className="h-6 w-6" />
            </div>

            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.14em] text-zinc-500">
                Purchase decision
              </p>

              <h2
                id="decision-summary-title"
                className="mt-1 text-2xl font-bold tracking-tight text-zinc-950 sm:text-3xl"
              >
                Should you buy this vehicle?
              </h2>

              <p className="mt-2 max-w-2xl text-sm leading-6 text-zinc-600">
                {config.description}
              </p>
            </div>
          </div>

          <div className="shrink-0">
            <span
              className={`inline-flex items-center rounded-full px-4 py-2 text-sm font-bold uppercase tracking-[0.08em] ${config.badgeClassName}`}
            >
              {config.label}
            </span>
          </div>
        </div>

        <div className="rounded-2xl border border-white/80 bg-white/80 p-5">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
            <div className="min-w-0">
              <p className="text-xs font-semibold uppercase tracking-[0.12em] text-zinc-400">
                Assessment
              </p>

              <p className="mt-2 max-w-3xl text-sm leading-6 text-zinc-700">
                {rationale}
              </p>
            </div>

            <div className="shrink-0 sm:text-right">
              <p className="text-xs font-semibold uppercase tracking-[0.12em] text-zinc-400">
                Confidence
              </p>

              <p className="mt-1 text-sm font-bold capitalize text-zinc-900">
                {confidence}
              </p>
            </div>
          </div>
        </div>

        {priorityRisks.length > 0 && (
          <div>
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.12em] text-zinc-500">
                  Priority concerns
                </p>

                <p className="mt-1 text-sm text-zinc-600">
                  Resolve these issues before making a final purchase decision.
                </p>
              </div>

              <span className="shrink-0 text-xs font-semibold text-zinc-500">
                {priorityRisks.length}{" "}
                {priorityRisks.length === 1 ? "item" : "items"}
              </span>
            </div>

            <div className="mt-4 grid gap-3">
              {priorityRisks.map((risk) => (
                <div
                  key={risk.id}
                  className="flex items-start gap-3 rounded-2xl border border-white/80 bg-white/80 p-4"
                >
                  <AlertTriangle
                    className="mt-0.5 h-4 w-4 shrink-0 text-red-600"
                    aria-hidden="true"
                  />

                  <div className="min-w-0 flex-1">
                    <div className="flex flex-wrap items-center gap-2">
                      <p className="text-sm font-semibold text-zinc-900">
                        {risk.title}
                      </p>

                      <span
                        className={`rounded-full px-2 py-0.5 text-[11px] font-semibold capitalize ${severityClassName[risk.severity]}`}
                      >
                        {risk.severity}
                      </span>
                    </div>

                    <p className="mt-1 text-sm leading-5 text-zinc-600">
                      {risk.recommendedAction}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </section>
  );
}