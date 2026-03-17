"use client";

import { useEffect, useState } from "react";
import { fetchResults } from "@/lib/api";
import type { ResultsSummary } from "@/lib/types";
import BulletinCard from "@/components/BulletinCard";
import ResultsTable from "@/components/ResultsTable";

const POLL_INTERVAL_MS = 30_000;

export default function ResultsPage() {
  const [data, setData] = useState<ResultsSummary | null>(null);
  const [error, setError] = useState<string>("");
  const [loading, setLoading] = useState(true);

  async function load() {
    try {
      const results = await fetchResults();
      setData(results);
      setError("");
    } catch (err) {
      setError(String(err));
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
    const interval = setInterval(load, POLL_INTERVAL_MS);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="text-center py-16">
        <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-green-700 mx-auto mb-4" />
        <p className="text-gray-600">Carregando resultados...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
        <p className="text-red-800 font-semibold">Erro ao carregar resultados</p>
        <p className="text-red-700 text-sm mt-1">{error}</p>
        <button
          onClick={load}
          className="mt-4 px-4 py-2 bg-red-700 text-white rounded hover:bg-red-800 transition"
        >
          Tentar novamente
        </button>
      </div>
    );
  }

  if (!data || data.elections.length === 0) {
    return (
      <div className="text-center py-16 text-gray-500">
        <p className="text-lg">Nenhum resultado disponivel ainda.</p>
        <p className="text-sm mt-2">Seja o primeiro a escanear um Boletim de Urna!</p>
        <a
          href="/scan"
          className="inline-block mt-6 bg-green-700 text-white px-6 py-3 rounded-lg hover:bg-green-800 transition"
        >
          Escanear BU
        </a>
      </div>
    );
  }

  const generatedAt = new Date(data.generated_at).toLocaleString("pt-BR");

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Resultados da Apuração</h2>
        <p className="text-xs text-gray-500">Atualizado: {generatedAt}</p>
      </div>

      {data.elections.map((election) => (
        <div key={election.process_key} className="space-y-4">
          <BulletinCard election={election} />

          {election.cargos.map((cargo) => (
            <ResultsTable key={cargo.cargo_code} cargo={cargo} />
          ))}
        </div>
      ))}

      <p className="text-xs text-gray-400 text-center">
        Atualização automática a cada 30 segundos.
      </p>
    </div>
  );
}
