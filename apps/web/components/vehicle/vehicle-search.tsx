"use client";

import { ArrowRight, CarFront } from "lucide-react";
import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

export function VehicleSearch() {
  const router = useRouter();
  const [value, setValue] = useState("");
  const [error, setError] = useState("");

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const vehicle = value.trim();

    if (!vehicle) {
      setError("Enter a VIN or registration number to continue.");
      return;
    }

    setError("");
    router.push(`/analyze?vehicle=${encodeURIComponent(vehicle)}`);
  }

  return (
    <div>
      <form
        onSubmit={handleSubmit}
        className="flex flex-col gap-3 rounded-2xl border border-zinc-300 bg-white p-2 shadow-sm sm:flex-row"
      >
        <div className="flex min-w-0 flex-1 items-center gap-3 px-4">
          <CarFront className="h-5 w-5 shrink-0 text-zinc-400" />

          <input
            type="text"
            value={value}
            onChange={(event) => setValue(event.target.value)}
            placeholder="Enter VIN or registration number"
            aria-label="VIN or registration number"
            aria-invalid={Boolean(error)}
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

      {error ? (
        <p className="mt-3 text-sm font-medium text-red-600" role="alert">
          {error}
        </p>
      ) : null}
    </div>
  );
}
