import type { IngestResponse, ResultsSummary } from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "";
const RESULTS_URL = process.env.NEXT_PUBLIC_RESULTS_URL ?? "";

export async function submitBulletin(qrCodes: string[]): Promise<IngestResponse> {
  const res = await fetch(`${API_URL}/bulletins`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ qr_codes: qrCodes }),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API error ${res.status}: ${text}`);
  }

  return res.json();
}

export async function fetchResults(): Promise<ResultsSummary> {
  const res = await fetch(RESULTS_URL, {
    cache: "no-store",
    headers: { Accept: "application/json" },
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch results: ${res.status}`);
  }

  return res.json();
}
