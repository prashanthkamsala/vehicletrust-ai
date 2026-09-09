import {
  AlertTriangle,
  ArrowRight,
  CheckCircle2,
  ShieldCheck,
} from "lucide-react";

const signals = [
  {
    label: "Ownership history",
    value: "Strong",
    status: "positive",
  },
  {
    label: "Accident signals",
    value: "Clear",
    status: "positive",
  },
  {
    label: "Service history",
    value: "Review",
    status: "warning",
  },
  {
    label: "Mileage consistency",
    value: "Verified",
    status: "positive",
  },
] as const;

export function VehicleIntelligencePreview() {
  return (
    <section className="mx-auto max-w-5xl px-6 pb-24 lg:px-8">
      <div className="overflow-hidden rounded-3xl border border-zinc-200 bg-white shadow-[0_24px_80px_-32px_rgba(0,0,0,0.25)]">
        <div className="border-b border-zinc-200 px-6 py-5 sm:px-8">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.16em] text-zinc-500">
                Vehicle intelligence
              </p>

              <h2 className="mt-2 text-xl font-semibold tracking-tight">
                2021 Toyota Camry
              </h2>

              <p className="mt-1 text-sm text-zinc-500">
                KA 01 AB 1234 · Example vehicle profile
              </p>
            </div>

            <div className="inline-flex items-center gap-2 rounded-full border border-zinc-200 bg-zinc-50 px-3 py-1.5 text-xs font-medium text-zinc-700">
              <span className="h-2 w-2 rounded-full bg-emerald-500" />
              Analysis complete
            </div>
          </div>
        </div>

        <div className="grid lg:grid-cols-[260px_1fr]">
          <div className="border-b border-zinc-200 bg-zinc-50 p-8 text-center lg:border-b-0 lg:border-r">
            <div className="mx-auto flex h-40 w-40 items-center justify-center rounded-full border-[10px] border-zinc-200">
              <div>
                <div className="text-5xl font-semibold tracking-tight">
                  87
                </div>

                <div className="mt-1 text-xs font-semibold uppercase tracking-[0.18em] text-zinc-500">
                  Trust score
                </div>

                <div className="mt-2 text-xs text-zinc-500">
                  High confidence
                </div>
              </div>
            </div>

            <div className="mt-6 flex items-center justify-center gap-2 text-sm font-medium text-zinc-700">
              <ShieldCheck className="h-4 w-4" />
              Low-risk profile
            </div>
          </div>

          <div className="p-6 sm:p-8">
            <div className="grid gap-3 sm:grid-cols-2">
              {signals.map((signal) => (
                <div
                  key={signal.label}
                  className="flex items-center justify-between rounded-2xl border border-zinc-200 p-4"
                >
                  <div className="flex items-center gap-3">
                    {signal.status === "positive" ? (
                      <CheckCircle2 className="h-5 w-5 text-emerald-600" />
                    ) : (
                      <AlertTriangle className="h-5 w-5 text-amber-600" />
                    )}

                    <span className="text-sm font-medium">
                      {signal.label}
                    </span>
                  </div>

                  <span
                    className={
                      signal.status === "positive"
                        ? "text-sm font-medium text-emerald-700"
                        : "text-sm font-medium text-amber-700"
                    }
                  >
                    {signal.value}
                  </span>
                </div>
              ))}
            </div>

            <div className="mt-6 rounded-2xl bg-zinc-950 p-6 text-white">
              <div className="flex items-center gap-2 text-sm font-medium">
                <ShieldCheck className="h-4 w-4" />
                AI assessment
              </div>

              <p className="mt-3 max-w-2xl text-sm leading-6 text-zinc-300">
                The available signals indicate a relatively low-risk vehicle.
                Ownership and accident indicators look healthy, while the
                service history deserves additional verification before
                purchase.
              </p>
            </div>

            <button className="mt-6 inline-flex items-center gap-2 text-sm font-semibold text-zinc-950 transition-colors hover:text-zinc-600">
              View intelligence report
              <ArrowRight className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}
