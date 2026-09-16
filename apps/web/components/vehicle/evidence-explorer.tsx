import {
  AlertTriangle,
  CheckCircle2,
  Clock3,
  FileCheck2,
  HelpCircle,
  ShieldAlert,
} from "lucide-react";

import type {
  EvidenceConfidence,
  EvidenceItem,
  EvidenceStatus,
} from "@/lib/vehicle/types";

type EvidenceExplorerProps = {
  evidence: EvidenceItem[];
};

const statusConfig: Record<
  EvidenceStatus,
  {
    label: string;
    icon: typeof CheckCircle2;
    className: string;
  }
> = {
  verified: {
    label: "Verified",
    icon: CheckCircle2,
    className: "bg-emerald-50 text-emerald-700",
  },
  partially_verified: {
    label: "Partially verified",
    icon: ShieldAlert,
    className: "bg-amber-50 text-amber-700",
  },
  unverified: {
    label: "Unverified",
    icon: HelpCircle,
    className: "bg-zinc-100 text-zinc-600",
  },
  conflicting: {
    label: "Conflicting",
    icon: AlertTriangle,
    className: "bg-red-50 text-red-700",
  },
};

const confidenceConfig: Record<
  EvidenceConfidence,
  {
    label: string;
  }
> = {
  high: {
    label: "High confidence",
  },
  medium: {
    label: "Medium confidence",
  },
  low: {
    label: "Low confidence",
  },
};

export function EvidenceExplorer({
  evidence,
}: EvidenceExplorerProps) {
  return (
    <section className="overflow-hidden rounded-3xl border border-zinc-200 bg-white shadow-sm">
      <div className="border-b border-zinc-200 px-6 py-6 sm:px-8 lg:px-10">
        <p className="text-xs font-semibold uppercase tracking-[0.16em] text-zinc-500">
          Evidence explorer
        </p>

        <div className="mt-2">
          <h2 className="text-2xl font-semibold tracking-tight text-zinc-950">
            Evidence behind the assessment
          </h2>

          <p className="mt-1 max-w-2xl text-sm text-zinc-500">
            Review the underlying vehicle evidence used to derive risks,
            trust factors, and the overall assessment.
          </p>
        </div>
      </div>

      <div className="divide-y divide-zinc-200">
        {evidence.length > 0 ? (
          evidence.map((item) => (
            <EvidenceCard key={item.id} evidence={item} />
          ))
        ) : (
          <div className="px-6 py-10 text-center sm:px-8 lg:px-10">
            <FileCheck2 className="mx-auto h-8 w-8 text-zinc-400" />

            <p className="mt-3 text-sm font-medium text-zinc-700">
              No evidence is available.
            </p>

            <p className="mt-1 text-xs text-zinc-500">
              Additional vehicle records are required to generate an
              evidence-backed assessment.
            </p>
          </div>
        )}
      </div>
    </section>
  );
}

function EvidenceCard({
  evidence,
}: {
  evidence: EvidenceItem;
}) {
  const status = statusConfig[evidence.status];
  const StatusIcon = status.icon;
  const confidence = confidenceConfig[evidence.confidence];

  return (
    <article className="px-6 py-6 sm:px-8 lg:px-10">
      <div className="flex flex-col gap-5 lg:flex-row lg:items-start lg:justify-between">
        <div className="min-w-0">
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-xs font-semibold uppercase tracking-[0.12em] text-zinc-400">
              {evidence.category}
            </span>

            <span
              className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-semibold ${status.className}`}
            >
              <StatusIcon className="h-3.5 w-3.5" />
              {status.label}
            </span>
          </div>

          <h3 className="mt-2 text-base font-semibold text-zinc-950">
            {evidence.title}
          </h3>

          <p className="mt-1 text-lg font-semibold tracking-tight text-zinc-900">
            {evidence.value}
          </p>

          <p className="mt-3 max-w-3xl text-sm leading-6 text-zinc-600">
            {evidence.explanation}
          </p>
        </div>

        <div className="shrink-0 rounded-2xl bg-zinc-50 px-4 py-3 lg:min-w-52">
          <div className="flex items-center gap-2 text-xs font-semibold text-zinc-700">
            <ShieldAlert className="h-4 w-4 text-zinc-500" />
            {confidence.label}
          </div>

          <div className="mt-3">
            <p className="text-xs font-medium uppercase tracking-[0.1em] text-zinc-400">
              Source
            </p>

            <p className="mt-1 text-sm font-semibold text-zinc-800">
              {evidence.source.name}
            </p>

            <p className="mt-0.5 text-xs text-zinc-500">
              {evidence.source.type}
            </p>
          </div>

          {evidence.observedAt && (
            <div className="mt-3 flex items-start gap-2">
              <Clock3 className="mt-0.5 h-3.5 w-3.5 shrink-0 text-zinc-400" />

              <div>
                <p className="text-xs font-medium uppercase tracking-[0.1em] text-zinc-400">
                  Observed
                </p>

                <p className="mt-1 text-xs font-medium text-zinc-600">
                  {evidence.observedAt}
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </article>
  );
}