"use client";

import { useState } from "react";
import dynamic from "next/dynamic";
import { submitBulletin } from "@/lib/api";

// Dynamic import to avoid SSR issues with camera API
const QrScanner = dynamic(() => import("@/components/QrScanner"), { ssr: false });

type Status = "idle" | "scanning" | "collected" | "submitting" | "success" | "error";

export default function ScanPage() {
  const [status, setStatus] = useState<Status>("idle");
  const [scannedParts, setScannedParts] = useState<string[]>([]);
  const [expectedTotal, setExpectedTotal] = useState<number>(1);
  const [executionId, setExecutionId] = useState<string>("");
  const [errorMsg, setErrorMsg] = useState<string>("");

  function handleScan(text: string) {
    // Avoid duplicates
    if (scannedParts.includes(text)) return;

    // Parse QRBU header to know total expected parts
    const match = text.match(/QRBU:(\d+):(\d+)/);
    const total = match ? parseInt(match[2]) : 1;
    setExpectedTotal(total);

    const updated = [...scannedParts, text];
    setScannedParts(updated);

    if (updated.length >= total) {
      setStatus("collected");
    } else {
      setStatus("scanning");
    }
  }

  async function handleSubmit() {
    setStatus("submitting");
    try {
      const result = await submitBulletin(scannedParts);
      setExecutionId(result.execution_id);
      setStatus("success");
    } catch (err) {
      setErrorMsg(String(err));
      setStatus("error");
    }
  }

  function handleReset() {
    setScannedParts([]);
    setExpectedTotal(1);
    setExecutionId("");
    setErrorMsg("");
    setStatus("idle");
  }

  return (
    <div className="max-w-sm mx-auto space-y-6">
      <h2 className="text-2xl font-bold text-center">Escanear Boletim de Urna</h2>

      {(status === "idle" || status === "scanning") && (
        <div className="space-y-4">
          <p className="text-sm text-gray-600 text-center">
            {scannedParts.length === 0
              ? "Aponte a câmera para o QR Code do Boletim de Urna."
              : `Parte ${scannedParts.length}/${expectedTotal} escaneada. Continue escaneando.`}
          </p>

          {scannedParts.length > 0 && (
            <div className="bg-green-50 border border-green-200 rounded p-3">
              <p className="text-sm text-green-800 font-medium">
                {scannedParts.length}/{expectedTotal} partes coletadas
              </p>
            </div>
          )}

          <QrScanner onScan={handleScan} onError={setErrorMsg} />
        </div>
      )}

      {status === "collected" && (
        <div className="space-y-4">
          <div className="bg-green-50 border border-green-200 rounded p-4 text-center">
            <p className="text-green-800 font-semibold">
              {scannedParts.length} parte(s) coletada(s)
            </p>
            <p className="text-green-700 text-sm">Pronto para enviar.</p>
          </div>
          <button
            onClick={handleSubmit}
            className="w-full bg-green-700 text-white py-3 rounded-lg font-semibold hover:bg-green-800 transition"
          >
            Enviar para Apuração
          </button>
          <button onClick={handleReset} className="w-full text-gray-500 text-sm underline">
            Cancelar
          </button>
        </div>
      )}

      {status === "submitting" && (
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-green-700 mx-auto mb-4" />
          <p className="text-gray-600">Enviando e verificando...</p>
        </div>
      )}

      {status === "success" && (
        <div className="space-y-4">
          <div className="bg-green-50 border border-green-300 rounded-lg p-6 text-center">
            <p className="text-2xl mb-2">Registrado!</p>
            <p className="text-green-800 font-semibold">Boletim enviado com sucesso.</p>
            <p className="text-xs text-gray-500 mt-2 break-all">ID: {executionId}</p>
          </div>
          <a
            href="/results"
            className="block w-full text-center bg-green-700 text-white py-3 rounded-lg font-semibold hover:bg-green-800 transition"
          >
            Ver Resultados
          </a>
          <button onClick={handleReset} className="w-full text-gray-500 text-sm underline">
            Escanear outro BU
          </button>
        </div>
      )}

      {status === "error" && (
        <div className="space-y-4">
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <p className="text-red-800 font-semibold">Erro ao enviar</p>
            <p className="text-red-700 text-sm mt-1">{errorMsg}</p>
          </div>
          <button
            onClick={handleReset}
            className="w-full bg-gray-700 text-white py-3 rounded-lg font-semibold hover:bg-gray-800 transition"
          >
            Tentar novamente
          </button>
        </div>
      )}
    </div>
  );
}
