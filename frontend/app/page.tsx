"use client";

import { useMemo, useState } from "react";

type ApiResult = {
  postal: string;
  address: string | null;
  type: "PUBLIC" | "PRIVATE" | "NON_RESIDENTIAL" | "NOT_FOUND";
};

function Spinner() {
  return (
    <span
      aria-label="Loading"
      className="inline-block h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white"
    />
  );
}

export default function Home() {
  const [postal, setPostal] = useState("");
  const [result, setResult] = useState<ApiResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const trimmed = postal.trim();

  const isSixDigits = useMemo(() => {
    return /^\d{6}$/.test(trimmed);
  }, [trimmed]);

  async function onCheck() {
    if (loading) return;

    setError(null);
    setResult(null);

    if (!isSixDigits) {
      setError("Please enter a valid 6-digit postal code.");
      return;
    }

    setLoading(true);
    try {
      const r = await fetch(
        `http://127.0.0.1:8000/?postal=${encodeURIComponent(trimmed)}`,
      );

      const j = await r.json().catch(() => null);

      if (!r.ok) {
        setError(j?.detail ?? "Request failed");
        return;
      }

      setResult(j as ApiResult);
    } catch {
      setError("Cannot reach backend");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-black text-white">
      <div className="mx-auto max-w-xl px-6 py-10">
        <div className="mb-6">
          <h1 className="text-3xl font-semibold tracking-tight">Rich or Not</h1>
          <p className="mt-2 text-sm text-white/60">
            Enter a Singapore postal code to classify property type.
          </p>
        </div>

        <div className="rounded-xl border border-white/15 bg-white/5 p-5 shadow-sm">
          <label className="text-sm text-white/70">Postal code</label>

          <div className="mt-2 flex gap-2">
            <input
              value={postal}
              onChange={(e) => {
                // Clear result + error as user types (and keep digits only)
                const next = e.target.value.replace(/\D/g, "");
                setPostal(next);
                setError(null);
                setResult(null);
              }}
              onKeyDown={(e) => {
                if (e.key === "Enter") onCheck();
              }}
              placeholder="e.g. 528769"
              inputMode="numeric"
              className="w-full rounded-lg border border-white/15 bg-black px-4 py-3 text-base outline-none placeholder:text-white/30 focus:border-white/30"
              maxLength={6}
            />

            <button
              onClick={onCheck}
              disabled={!isSixDigits || loading}
              className="inline-flex items-center justify-center gap-2 rounded-lg border border-white/15 bg-white/10 px-4 py-3 text-sm font-semibold hover:bg-white/15 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? (
                <>
                  <Spinner />
                  Checking…
                </>
              ) : (
                "Check"
              )}
            </button>
          </div>

          <div className="mt-2 flex items-center justify-between text-xs text-white/40">
            <div>{isSixDigits ? "✓ Looks good" : "Enter 6 digits"}</div>
            <div>Press Enter to submit</div>
          </div>

          {error && (
            <div className="mt-4 rounded-lg border border-red-400/30 bg-red-500/10 px-4 py-3 text-sm text-red-200">
              {error}
            </div>
          )}

          {result && (
            <div className="mt-4 rounded-lg border border-white/10 bg-black/30 px-4 py-4 text-sm">
              <div className="grid grid-cols-3 gap-y-2">
                <div className="text-white/60">Postal Entered</div>
                <div className="col-span-2 font-semibold tabular-nums">
                  {result.postal}
                </div>

                <div className="text-white/60">Address</div>
                <div className="col-span-2">
                  {result.address ?? <span className="text-white/40">-</span>}
                </div>

                <div className="text-white/60">Property Type</div>
                <div className="col-span-2 font-semibold">{result.type}</div>
              </div>
            </div>
          )}
        </div>

        <div className="mt-6 text-xs text-white/35">
          Backend: <span className="text-white/50">http://127.0.0.1:8000</span>
        </div>
      </div>
    </main>
  );
}
