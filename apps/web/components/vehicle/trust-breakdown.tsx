import { CheckCircle2, Minus, Plus } from "lucide-react";

import type { TrustFactor } from "@/lib/vehicle/types";

type TrustBreakdownProps = {
  baseScore: number;
  calculatedScore: number;
  score: number;
  assessment: string;
  confidence: string;
  factors: TrustFactor[];
};

export function TrustBreakdown({
  baseScore,
  calculatedScore,
  score,
  assessment,
  confidence,
  factors,
}: TrustBreakdownProps) {
  const positiveFactors = factors.filter(
    (factor) => factor.impact === "positive",
  );

  const negativeFactors = factors.filter(
    (factor) => factor.impact === "negative",
  );

  const neutralFactors = factors.filter(
    (factor) => factor.impact === "neutral",
  );

  const positiveTotal = positiveFactors.reduce(
    (total, factor) => total + factor.contribution,
    0,
  );

  const negativeTotal = negativeFactors.reduce(
    (total, factor) => total + factor.contribution,
    0,
  );

  const scoreWasCapped = calculatedScore > score;
  const scoreWasFloored = calculatedScore < score;

  return (
    <section className="overflow-hidden rounded-3xl border border-zinc-200 bg-white shadow-sm">
      <div className="border-b border-zinc-200 px-6 py-6 sm:px-8">
        <div className="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.16em] text-zinc-500">
              Trust breakdown
            </p>

            <h2 className="mt-2 text-2xl font-semibold tracking-tight text-zinc-950">
              Why this score?
            </h2>

            <p className="mt-1 max-w-2xl text-sm text-zinc-500">
              The final trust score is derived from the available vehicle
              evidence and its identified signals.
            </p>
          </div>

          <div className="shrink-0 text-sm text-zinc-500">
            <span>Confidence </span>
            <span className="font-semibold capitalize text-zinc-900">
              {confidence}
            </span>
          </div>
        </div>
      </div>

      <div className="border-b border-zinc-200 px-6 py-5 sm:px-8">
        <div className="grid gap-3 sm:grid-cols-4">
          <ScoreMetric
            label="Base"
            value={baseScore}
            description="Starting score"
          />

          <ScoreMetric
            label="Positive"
            value={positiveTotal}
            description="Positive signals"
            variant="positive"
            prefix="+"
          />

          <ScoreMetric
            label="Negative"
            value={negativeTotal}
            description="Negative signals"
            variant="negative"
          />

          <ScoreMetric
            label="Final"
            value={score}
            description="Trust score"
            emphasized
          />
        </div>
      </div>

      <div className="px-6 py-6 sm:px-8">
        <div className="grid gap-8 lg:grid-cols-2">
          {positiveFactors.length > 0 && (
            <FactorGroup
              title="Positive signals"
              factors={positiveFactors}
              variant="positive"
            />
          )}

          {negativeFactors.length > 0 && (
            <FactorGroup
              title="Negative signals"
              factors={negativeFactors}
              variant="negative"
            />
          )}
        </div>

        {neutralFactors.length > 0 && (
          <div className="mt-8">
            <FactorGroup
              title="Neutral signals"
              factors={neutralFactors}
              variant="neutral"
            />
          </div>
        )}

        {factors.length === 0 && (
          <div className="rounded-2xl border border-dashed border-zinc-200 bg-zinc-50 px-5 py-8 text-center">
            <p className="text-sm font-medium text-zinc-700">
              No trust factors are available.
            </p>

            <p className="mt-1 text-xs text-zinc-500">
              Additional vehicle evidence is required to explain the score.
            </p>
          </div>
        )}
      </div>

      <div className="border-t border-zinc-200 bg-zinc-50 px-6 py-5 sm:px-8">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-start gap-3">
            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-white">
              <CheckCircle2 className="h-5 w-5 text-zinc-500" />
            </div>

            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.12em] text-zinc-500">
                Final assessment
              </p>

              <p className="mt-1 text-sm font-medium text-zinc-800">
                {assessment}
              </p>
            </div>
          </div>

          <div className="text-left sm:text-right">
            <p className="text-xs text-zinc-500">
              Calculated score
            </p>

            <p className="mt-1 text-lg font-semibold tracking-tight text-zinc-950">
              {calculatedScore}
              <span className="mx-2 text-zinc-300">→</span>
              {score}
              <span className="ml-1 text-xs font-medium text-zinc-400">
                / 100
              </span>
            </p>

            {scoreWasFloored && (
              <p className="mt-1 text-xs text-zinc-500">
                Final score floored at the minimum of 0.
              </p>
            )}

            {scoreWasCapped && (
              <p className="mt-1 text-xs text-zinc-500">
                Final score capped at the maximum of 100.
              </p>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}

type ScoreMetricProps = {
  label: string;
  value: number;
  description: string;
  variant?: "positive" | "negative";
  prefix?: string;
  emphasized?: boolean;
};

function ScoreMetric({
  label,
  value,
  description,
  variant,
  prefix = "",
  emphasized = false,
}: ScoreMetricProps) {
  const valueClass =
    variant === "positive"
      ? "text-emerald-700"
      : variant === "negative"
        ? "text-red-700"
        : "text-zinc-950";

  return (
    <div
      className={`rounded-2xl border p-4 ${
        emphasized
          ? "border-zinc-300 bg-zinc-50"
          : "border-zinc-200 bg-white"
      }`}
    >
      <p className="text-xs font-medium text-zinc-500">{label}</p>

      <p
        className={`mt-1 text-2xl font-semibold tracking-tight ${valueClass}`}
      >
        {prefix}
        {value}
      </p>

      <p className="mt-1 text-xs text-zinc-400">{description}</p>
    </div>
  );
}

type FactorGroupProps = {
  title: string;
  factors: TrustFactor[];
  variant: "positive" | "negative" | "neutral";
};

function FactorGroup({
  title,
  factors,
  variant,
}: FactorGroupProps) {
  return (
    <div>
      <div className="mb-3 flex items-center justify-between">
        <h3 className="text-sm font-semibold text-zinc-950">
          {title}
        </h3>

        <span className="text-xs text-zinc-400">
          {factors.length}{" "}
          {factors.length === 1 ? "factor" : "factors"}
        </span>
      </div>

      <div className="divide-y divide-zinc-100 overflow-hidden rounded-2xl border border-zinc-200">
        {factors.map((factor) => (
          <div
            key={factor.id}
            className="flex items-center justify-between gap-4 px-4 py-3.5 sm:px-5"
          >
            <div className="flex min-w-0 items-center gap-3">
              <FactorIcon variant={variant} />

              <div className="min-w-0">
                <p className="truncate text-sm font-medium text-zinc-950">
                  {factor.name}
                </p>

                <p className="mt-1 text-xs text-zinc-500">
                  {factor.evidenceIds.length} linked{" "}
                  {factor.evidenceIds.length === 1
                    ? "evidence item"
                    : "evidence items"}
                </p>
              </div>
            </div>

            <span
              className={`shrink-0 text-sm font-semibold ${
                variant === "positive"
                  ? "text-emerald-700"
                  : variant === "negative"
                    ? "text-red-700"
                    : "text-zinc-500"
              }`}
            >
              {factor.contribution > 0
                ? `+${factor.contribution}`
                : factor.contribution}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

function FactorIcon({
  variant,
}: {
  variant: "positive" | "negative" | "neutral";
}) {
  if (variant === "positive") {
    return (
      <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-emerald-50">
        <Plus className="h-4 w-4 text-emerald-700" />
      </div>
    );
  }

  if (variant === "negative") {
    return (
      <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-red-50">
        <Minus className="h-4 w-4 text-red-700" />
      </div>
    );
  }

  return (
    <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-zinc-100">
      <Minus className="h-4 w-4 text-zinc-500" />
    </div>
  );
}