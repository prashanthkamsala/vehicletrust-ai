import { VehicleIntelligencePreview } from "@/components/vehicle/vehicle-intelligence-preview";
import {
  ArrowRight,
  CarFront,
  CheckCircle2,
  FileSearch,
  Gauge,
  ShieldCheck,
  Sparkles,
} from "lucide-react";

const capabilities = [
  {
    icon: FileSearch,
    title: "Vehicle history",
    description: "Bring together the signals that matter before a purchase.",
  },
  {
    icon: ShieldCheck,
    title: "Risk intelligence",
    description: "Identify potential ownership, accident, and maintenance risks.",
  },
  {
    icon: Gauge,
    title: "Trust score",
    description: "Turn complex vehicle evidence into a simple decision signal.",
  },
  {
    icon: Sparkles,
    title: "AI explanation",
    description: "Understand what the evidence means and why it matters.",
  },
];

export default function Home() {
  return (
    <main className="min-h-screen bg-white text-zinc-950">
      <header className="border-b border-zinc-200">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6 lg:px-8">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-zinc-950 text-white">
              <CarFront className="h-5 w-5" />
            </div>

            <span className="text-lg font-semibold tracking-tight">
              VehicleTrust AI
            </span>
          </div>

          <nav className="hidden items-center gap-8 text-sm text-zinc-600 md:flex">
            <a
              href="#how-it-works"
              className="transition-colors hover:text-zinc-950"
            >
              How it works
            </a>

            <a
              href="#capabilities"
              className="transition-colors hover:text-zinc-950"
            >
              Capabilities
            </a>

            <button className="rounded-full border border-zinc-300 px-4 py-2 font-medium text-zinc-900 transition-colors hover:bg-zinc-50">
              Sign in
            </button>
          </nav>
        </div>
      </header>

      <section className="relative overflow-hidden">
        <div className="mx-auto max-w-5xl px-6 pb-24 pt-24 text-center lg:px-8 lg:pb-32 lg:pt-32">
          <div className="mx-auto mb-6 flex w-fit items-center gap-2 rounded-full border border-zinc-200 bg-zinc-50 px-4 py-2 text-sm font-medium text-zinc-700">
            <Sparkles className="h-4 w-4" />
            Evidence-backed vehicle intelligence
          </div>

          <h1 className="mx-auto max-w-4xl text-5xl font-semibold tracking-tight text-zinc-950 sm:text-6xl lg:text-7xl">
            Know the vehicle.
            <br />
            <span className="text-zinc-500">Trust the decision.</span>
          </h1>

          <p className="mx-auto mt-7 max-w-2xl text-lg leading-8 text-zinc-600 sm:text-xl">
            Analyze a vehicle using its VIN or registration number and turn
            complex vehicle information into a clear, evidence-backed
            decision.
          </p>

          <div className="mx-auto mt-10 max-w-2xl">
            <form className="flex flex-col gap-3 rounded-2xl border border-zinc-300 bg-white p-2 shadow-sm sm:flex-row">
              <div className="flex min-w-0 flex-1 items-center gap-3 px-4">
                <CarFront className="h-5 w-5 shrink-0 text-zinc-400" />

                <input
                  type="text"
                  placeholder="Enter VIN or registration number"
                  aria-label="VIN or registration number"
                  className="h-12 min-w-0 flex-1 bg-transparent text-base outline-none placeholder:text-zinc-400"
                />
              </div>

              <button
                type="submit"
                className="inline-flex h-12 items-center justify-center gap-2 rounded-xl bg-zinc-950 px-6 font-medium text-white transition-all hover:bg-zinc-800"
              >
                Analyze
                <ArrowRight className="h-4 w-4" />
              </button>
            </form>

            <div className="mt-5 flex flex-wrap items-center justify-center gap-x-6 gap-y-2 text-sm text-zinc-500">
              <span className="inline-flex items-center gap-2">
                <CheckCircle2 className="h-4 w-4" />
                Vehicle history
              </span>

              <span className="inline-flex items-center gap-2">
                <CheckCircle2 className="h-4 w-4" />
                Risk signals
              </span>

              <span className="inline-flex items-center gap-2">
                <CheckCircle2 className="h-4 w-4" />
                AI insights
              </span>
            </div>
          </div>
        </div>
      </section>

      <VehicleIntelligencePreview />

      <section
        id="capabilities"
        className="border-t border-zinc-200 bg-zinc-50"
      >
        <div className="mx-auto max-w-7xl px-6 py-20 lg:px-8 lg:py-24">
          <div className="max-w-2xl">
            <p className="text-sm font-semibold uppercase tracking-wider text-zinc-500">
              Vehicle intelligence
            </p>

            <h2 className="mt-3 text-3xl font-semibold tracking-tight sm:text-4xl">
              From vehicle data to a decision you can understand.
            </h2>

            <p className="mt-4 text-lg leading-8 text-zinc-600">
              VehicleTrust brings evidence together, identifies meaningful
              signals, and explains what they mean for the vehicle you are
              evaluating.
            </p>
          </div>

          <div className="mt-12 grid gap-px overflow-hidden rounded-2xl border border-zinc-200 bg-zinc-200 sm:grid-cols-2 lg:grid-cols-4">
            {capabilities.map((capability) => {
              const Icon = capability.icon;

              return (
                <article
                  key={capability.title}
                  className="bg-white p-7"
                >
                  <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-zinc-100">
                    <Icon className="h-5 w-5 text-zinc-800" />
                  </div>

                  <h3 className="mt-6 font-semibold">
                    {capability.title}
                  </h3>

                  <p className="mt-2 text-sm leading-6 text-zinc-600">
                    {capability.description}
                  </p>
                </article>
              );
            })}
          </div>
        </div>
      </section>

      <section
        id="how-it-works"
        className="border-t border-zinc-200 bg-white"
      >
        <div className="mx-auto max-w-7xl px-6 py-20 lg:px-8 lg:py-24">
          <div className="text-center">
            <p className="text-sm font-semibold uppercase tracking-wider text-zinc-500">
              How VehicleTrust thinks
            </p>

            <h2 className="mt-3 text-3xl font-semibold tracking-tight sm:text-4xl">
              Evidence first. Intelligence second. Decision last.
            </h2>
          </div>

          <div className="mx-auto mt-14 grid max-w-4xl gap-6 md:grid-cols-4">
            {[
              ["01", "Identity", "Identify the vehicle."],
              ["02", "Evidence", "Collect relevant signals."],
              ["03", "Risk", "Evaluate meaningful risks."],
              ["04", "Trust", "Explain the overall picture."],
            ].map(([number, title, description]) => (
              <div key={number} className="text-center">
                <div className="text-sm font-semibold text-zinc-400">
                  {number}
                </div>

                <h3 className="mt-3 font-semibold">{title}</h3>

                <p className="mt-2 text-sm leading-6 text-zinc-600">
                  {description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <footer className="border-t border-zinc-200">
        <div className="mx-auto flex max-w-7xl flex-col gap-3 px-6 py-8 text-sm text-zinc-500 sm:flex-row sm:items-center sm:justify-between lg:px-8">
          <span>VehicleTrust AI</span>
          <span>Vehicle intelligence, built around evidence.</span>
        </div>
      </footer>
    </main>
  );
}
