import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Apuração Paralela",
  description: "Apuração independente de votos via QR Code do Boletim de Urna",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body className="min-h-screen bg-gray-50 text-gray-900 antialiased">
        <header className="bg-green-700 text-white py-3 px-4 shadow">
          <div className="max-w-4xl mx-auto flex items-center justify-between">
            <h1 className="font-bold text-lg">Apuração Paralela</h1>
            <nav className="flex gap-4 text-sm">
              <a href="/" className="hover:underline">Início</a>
              <a href="/scan" className="hover:underline">Escanear BU</a>
              <a href="/results" className="hover:underline">Resultados</a>
            </nav>
          </div>
        </header>
        <main className="max-w-4xl mx-auto px-4 py-8">{children}</main>
      </body>
    </html>
  );
}
