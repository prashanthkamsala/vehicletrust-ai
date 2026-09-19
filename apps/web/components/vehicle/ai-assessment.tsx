"use client";

import {
  BookOpen,
  CheckCircle2,
  FileSearch,
  ShieldCheck,
  Sparkles,
} from "lucide-react";

import type {
  AIGroundingStatus,
  AIInterpretation,
  EvidenceItem,
} from "@/lib/vehicle/types";

type AIAssessmentProps = {
  ai: AIInterpretation;
  evidence: EvidenceItem[];
};

const groundingConfig: Record<
  AIGroundingStatus,
  {
    label: string;
    description: string;
    className: string;
    icon: typeof CheckCircle2;
  }
> = {
  grounded: {
    label: "Grounded",
    description: "The explanation is supported by vehicle evidence and relevant knowledge.",
    className: "bg-emerald-50 text-emerald-700",
    icon: CheckCircle2,
  },
  partially_grounded: {
    label: "Partially grounded",
    description: "The explanation has supporting evidence, but additional verification may be useful.",
    className: "bg-amber-50 text-amber-700",
    icon: FileSearch,
  },
  insufficient: {
    label: "Insufficient evidence",
    description: "There is not enough supporting evidence for a reliable AI explanation.",
    className: "bg-zinc-100 text-zinc-600",
    icon: FileSearch,
  },
};

export function AIAssessment({
  ai,
  evidence,
}: AIAssessmentProps) {
  const grounding = groundingConfig[ai.grounding.status];
  const GroundingIcon = grounding.icon;

  const supportingEvidence = ai.supportingEvidenceIds
    .map((evidenceId) =>
      evidence.find((item) => item.id === evidenceId),
    )
    .filter((item): item is EvidenceItem => item !== undefined);

  return (
    <section
      aria-labelledby="ai-assessment-title"
      className="overflow-hidden rounded-3xl border border-zinc-200 bg-white shadow-sm"
    >
      <div className="border-b border-zinc-200 px-6 py-6 sm:px-8 lg:px-10">
        <div className="flex flex-col gap-5 lg:flex-row lg:items-start lg:justify-between">
          <div>
            <div className="flex items-center gap-2">
              <Sparkles className="h-4 w-4 text-zinc-500" />

              <p className="text-xs font-semibold uppercase tracking-[0.16em] text-zinc-500">
                AI assessment
              </p>
            </div>

            <h2
              id="ai-assessment-title"
              className="mt-2 text-2xl font-semibold tracking-tight text-zinc-950"
            >
              What the available evidence tells us
            </h2>

            <p className="mt-1 max-w-2xl text-sm leading-6 text-zinc-500">
              A grounded explanation generated from the vehicle evidence,
              identified risks, deterministic trust assessment, and relevant
              vehicle knowledge.
            </p>
          </div>

          <div className="shrink-0">
            <span
              className={`inline-flex items-center gap-2 rounded-full px-3 py-1.5 text-xs font-semibold ${grounding.className}`}
            >
              <GroundingIcon className="h-3.5 w-3.5" />
              {grounding.label}
            </span>
          </div>
        </div>
      </div>

      <div className="p-6 sm:p-8 lg:p-10">
        <div className="grid gap-8 lg:grid-cols-[minmax(0,1fr)_280px]">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.12em] text-zinc-400">
              Summary
            </p>

            <p className="mt-3 max-w-3xl text-base font-medium leading-7 text-zinc-800">
              {ai.summary}
            </p>

            <div className="mt-7">
              <p className="text-xs font-semibold uppercase tracking-[0.12em] text-zinc-400">
                Reasoning
              </p>

              <p className="mt-3 max-w-3xl text-sm leading-7 text-zinc-600">
                {ai.reasoning}
              </p>
            </div>

            <div className="mt-7 rounded-2xl border border-zinc-200 bg-zinc-50 p-5">
              <div className="flex items-start gap-3">
                <ShieldCheck className="mt-0.5 h-5 w-5 shrink-0 text-zinc-500" />

                <div>
                  <p className="text-xs font-semibold uppercase tracking-[0.12em] text-zinc-400">
                    Recommendation
                  </p>

                  <p className="mt-2 text-sm font-semibold leading-6 text-zinc-900">
                    {ai.recommendation}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <aside className="rounded-2xl border border-zinc-200 bg-zinc-50 p-5">
            <p className="text-xs font-semibold uppercase tracking-[0.12em] text-zinc-400">
              Grounding
            </p>

            <p className="mt-2 text-sm leading-6 text-zinc-600">
              {grounding.description}
            </p>

            <div className="mt-5 grid grid-cols-2 gap-3">
              <div className="rounded-xl border border-zinc-200 bg-white p-3">
                <p className="text-xs text-zinc-500">Evidence used</p>

                <p className="mt-1 text-xl font-semibold text-zinc-950">
                  {ai.grounding.evidenceCount}
                </p>
              </div>

              <div className="rounded-xl border border-zinc-200 bg-white p-3">
                <p className="text-xs text-zinc-500">Knowledge used</p>

                <p className="mt-1 text-xl font-semibold text-zinc-950">
                  {ai.grounding.knowledgeCount}
                </p>
              </div>
            </div>
          </aside>
        </div>

        {supportingEvidence.length > 0 && (
          <div className="mt-10 border-t border-zinc-200 pt-8">
            <div className="flex items-center gap-2">
              <FileSearch className="h-4 w-4 text-zinc-500" />

              <p className="text-xs font-semibold uppercase tracking-[0.12em] text-zinc-500">
                Supporting evidence
              </p>
            </div>

            <p className="mt-1 text-sm text-zinc-500">
              These evidence items directly support the AI explanation.
            </p>

            <div className="mt-4 grid gap-3 md:grid-cols-2">
              {supportingEvidence.map((item) => (
                <div
                  key={item.id}
                  className="rounded-2xl border border-zinc-200 bg-zinc-50 p-4"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="min-w-0">
                      <p className="text-sm font-semibold text-zinc-900">
                        {item.title}
                      </p>

                      <p className="mt-1 text-sm font-medium text-zinc-700">
                        {item.value}
                      </p>
                    </div>

                    <span className="shrink-0 rounded-full bg-white px-2.5 py-1 text-[11px] font-semibold capitalize text-zinc-600">
                      {item.status.replace("_", " ")}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {ai.knowledgeReferences.length > 0 && (
          <div className="mt-10 border-t border-zinc-200 pt-8">
            <div className="flex items-center gap-2">
              <BookOpen className="h-4 w-4 text-zinc-500" />

              <p className="text-xs font-semibold uppercase tracking-[0.12em] text-zinc-500">
                Knowledge used
              </p>
            </div>

            <p className="mt-1 text-sm text-zinc-500">
              General vehicle knowledge retrieved to provide context for the
              evidence.
            </p>

            <div className="mt-4 grid gap-3 md:grid-cols-2">
              {ai.knowledgeReferences.map((reference) => (
                <div
                  key={reference.id}
                  className="rounded-2xl border border-zinc-200 bg-white p-4"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="min-w-0">
                      <p className="text-sm font-semibold text-zinc-900">
                        {reference.title}
                      </p>

                      <p className="mt-1 text-xs font-medium uppercase tracking-[0.1em] text-zinc-400">
                        {reference.category}
                      </p>
                    </div>
                  </div>

                  <p className="mt-3 text-xs leading-5 text-zinc-500">
                    {reference.relevance}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </section>
  );
}