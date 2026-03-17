"use client";

import { useEffect, useRef, useState } from "react";

interface Props {
  onScan: (text: string) => void;
  onError?: (err: string) => void;
}

export default function QrScanner({ onScan, onError }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);
  const scannerRef = useRef<unknown>(null);
  const [active, setActive] = useState(false);

  useEffect(() => {
    return () => {
      // Cleanup on unmount
      stopScanner();
    };
  }, []);

  async function startScanner() {
    if (typeof window === "undefined") return;

    const { Html5Qrcode } = await import("html5-qrcode");
    const scanner = new Html5Qrcode("qr-reader");
    scannerRef.current = scanner;

    try {
      await scanner.start(
        { facingMode: "environment" },
        { fps: 10, qrbox: { width: 280, height: 280 } },
        (decodedText) => {
          onScan(decodedText);
        },
        undefined
      );
      setActive(true);
    } catch (err) {
      onError?.(String(err));
    }
  }

  async function stopScanner() {
    const scanner = scannerRef.current as { stop?: () => Promise<void>; clear?: () => void } | null;
    if (scanner?.stop) {
      try {
        await scanner.stop();
        scanner.clear?.();
      } catch {
        // ignore cleanup errors
      }
    }
    setActive(false);
  }

  return (
    <div className="space-y-4">
      <div
        id="qr-reader"
        ref={containerRef}
        className="w-full max-w-sm mx-auto rounded-lg overflow-hidden border-2 border-green-700"
        style={{ minHeight: active ? undefined : "0px" }}
      />

      {!active ? (
        <button
          onClick={startScanner}
          className="w-full bg-green-700 text-white py-3 rounded-lg font-semibold hover:bg-green-800 transition"
        >
          Iniciar Camera
        </button>
      ) : (
        <button
          onClick={stopScanner}
          className="w-full border border-gray-400 text-gray-700 py-3 rounded-lg hover:bg-gray-100 transition"
        >
          Parar Camera
        </button>
      )}
    </div>
  );
}
