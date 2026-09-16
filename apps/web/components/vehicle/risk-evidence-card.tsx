"use client";

import {
  AlertTriangle,
  CheckCircle2,
  ChevronDown,
  ChevronUp,
  CircleAlert,
} from "lucide-react";
import { useState } from "react";

import type {
  EvidenceItem,
  RiskItem,
  RiskSeverity,
} from "@/lib/vehicle/types";

type RiskEvidenceCardProps = {
  risk: RiskItem;
  evidence: EvidenceItem[];
};

const severityConfig: Record<
  RiskSeverity,
  {
    label: string;
    icon: typeof AlertTriangle;
    className: string;
  }
> = {
  low: {
    label: "Low severity",
    icon: CheckCircle2,
    className: "bg-zinc-100 text-zinc-600",
  },
  medium: {
    label: "Medium severity",
    icon: CircleAlert,
    className: "bg-amber-50 text-amber-700",
  },
  high: {
    label: "High severity",
    icon: AlertTriangle,
    className: "bg-red-50 text-red-700",
  },
  critical: {
    label: "Critical severity",
    icon: AlertTriangle,
    className: "bg-red-100 text-red-800",
  },
};

export function RiskEvidenceCard({
  risk,
  evidence,
}: RiskEvidenceCardProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  const severity = severityConfig[risk.severity];
  const SeverityIcon = severity.icon;

  const supportingEvidence = risk.evidenceIds
    .map((evidenceId) =>
      evidence.find((item) => item.id === evidenceId),
    )
    .filter((item): item is EvidenceItem => item !== undefined);

  return (
    <article className="rounded-2xl border border-zinc-200 bg-white">
      <div className="p-5 sm:p-6">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
          <div className="min-w-0">
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-xs font-semibold uppercase tracking-[0.12em] text-zinc-400">
                {risk.category}
              </span>

              <span
                className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-semibold ${severity.className}`}
              >
                <SeverityIcon className="h-3.5 w-3.5" />
                {severity.label}
              </span>
            </div>

            <h3 className="mt-2 text-base font-semibold text-zinc-950">
              {risk.title}
            </h3>

            <p className="mt-2 text-sm leading-6 text-zinc-600">
              {risk.explanation}
            </p>
          </div>

          <div className="shrink-0 text-left sm:text-right">
            <p className="text-xs font-medium uppercase tracking-[0.1em] text-zinc-400">
              Confidence
            </p>

            <p className="mt-1 text-sm font-semibold capitalize text-zinc-800">
              {risk.confidence}
            </p>
          </div>
        </div>

        <div className="mt-5 flex flex-col gap-3 border-t border-zinc-100 pt-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-xs font-medium uppercase tracking-[0.1em] text-zinc-400">
              Supporting evidence
            </p>

            <p className="mt-1 text-sm font-medium text-zinc-700">
              {supportingEvidence.length} linked{" "}
              {supportingEvidence.length === 1 ? "item" : "items"}
            </p>
          </div>

          <button
            type="button"
            onClick={() => setIsExpanded((expanded) => !expanded)}
            className="inline-flex items-center justify-center gap-2 rounded-xl border border-zinc-200 px-4 py-2 text-sm font-semibold text-zinc-700 transition hover:bg-zinc-50"
            aria-expanded={isExpanded}
          >
            {isExpanded ? "Hide evidence" : "View evidence"}

            {isExpanded ? (
              <ChevronUp className="h-4 w-4" />
            ) : (
              <ChevronDown className="h-4 w-4" />
            )}
          </button>
        </div>
      </div>

      {isExpanded && (
        <div className="border-t border-zinc-200 bg-zinc-50 px-5 py-5 sm:px-6">
          {supportingEvidence.length > 0 ? (
            <div className="space-y-3">
              {supportingEvidence.map((item) => (
                <div
                  key={item.id}
                  className="rounded-xl border border-zinc-200 bg-white p-4"
                >
                  <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
                    <div>
                      <p className="text-xs font-semibold uppercase tracking-[0.1em] text-zinc-400">
                        {item.category}
                      </p>

                      <p className="mt-1 text-sm font-semibold text-zinc-900">
                        {item.title}
                      </p>

                      <p className="mt-1 text-sm font-medium text-zinc-700">
                        {item.value}
                      </p>
                    </div>

                    <span className="shrink-0 text-xs font-semibold capitalize text-zinc-500">
                      {item.confidence} confidence
                    </span>
                  </div>

                  <p className="mt-3 text-sm leading-6 text-zinc-600">
                    {item.explanation}
                  </p>

                  <div className="mt-3 flex flex-wrap gap-x-5 gap-y-2 text-xs text-zinc-500">
                    <span>
                      Source:{" "}
                      <span className="font-medium text-zinc-700">
                        {item.source.name}
                      </span>
                    </span>

                    {item.observedAt && (
                      <span>
                        Observed:{" "}
                        <span className="font-medium text-zinc-700">
                          {item.observedAt}
                        </span>
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-zinc-500">
              No matching evidence records were found for this risk.
            </p>
          )}
        </div>
      )}

      <div className="border-t border-zinc-100 bg-zinc-50 px-5 py-4 sm:px-6">
        <p className="text-xs font-medium uppercase tracking-[0.1em] text-zinc-400">
          Recommended action
        </p>

        <p className="mt-1 text-sm leading-6 text-zinc-700">
          {risk.recommendedAction}
        </p>
      </div>
    </article>
  );
}