import {
  AlertCircle,
  CheckCircle2,
} from "lucide-react";
import type { EvidenceItem } from "@/lib/vehicle/types";
import { getEvidenceQuality } from "@/lib/vehicle/evidence/quality";

type RiskEvidenceProps = {
  evidence: EvidenceItem[];
};

export function RiskEvidence({
  evidence,
}: RiskEvidenceProps) {
  if (evidence.length === 0) {
    return (
      <div className="rounded-xl border border-zinc-200 bg-white/70 p-4">
        <p className="text-sm text-zinc-500">
          No supporting evidence is currently linked to this risk.
        </p>
      </div>
    );
  }

  return (
    <div className="rounded-xl border border-amber-200/80 bg-white/80 p-4">
      <p className="text-xs font-semibold uppercase tracking-[0.14em] text-zinc-500">
        Supporting evidence
      </p>

      <div className="mt-3 space-y-3">
        {evidence.map((item) => {
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

              <div className="mt-4 border-t border-zinc-100 pt-3">
                <p className="text-[11px] font-semibold uppercase tracking-[0.12em] text-zinc-400">
                  Source
                </p>

                <p className="mt-1 text-xs font-medium text-zinc-700">
                  {item.source.name}
                </p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}