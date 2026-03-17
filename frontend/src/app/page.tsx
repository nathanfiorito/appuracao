import Link from "next/link";

export default function Home() {
  return (
    <div className="space-y-8">
      <section className="text-center py-12">
        <h2 className="text-3xl font-bold mb-4">Apuração Independente de Votos</h2>
        <p className="text-gray-600 max-w-xl mx-auto mb-8">
          Contribua para a transparência eleitoral escaneando o QR Code do
          Boletim de Urna com seu celular. Os votos são verificados
          criptograficamente e totalizados de forma independente.
        </p>
        <div className="flex gap-4 justify-center">
          <Link
            href="/scan"
            className="bg-green-700 text-white px-6 py-3 rounded-lg font-semibold hover:bg-green-800 transition"
          >
            Escanear Boletim de Urna
          </Link>
          <Link
            href="/results"
            className="border border-green-700 text-green-700 px-6 py-3 rounded-lg font-semibold hover:bg-green-50 transition"
          >
            Ver Resultados
          </Link>
        </div>
      </section>

      <section className="grid md:grid-cols-3 gap-6">
        <div className="bg-white rounded-lg p-6 shadow-sm border">
          <h3 className="font-semibold text-lg mb-2">1. Escaneie</h3>
          <p className="text-gray-600 text-sm">
            Aponte a câmera do celular para o QR Code impresso no Boletim de Urna
            (BU) afixado na seção eleitoral.
          </p>
        </div>
        <div className="bg-white rounded-lg p-6 shadow-sm border">
          <h3 className="font-semibold text-lg mb-2">2. Valide</h3>
          <p className="text-gray-600 text-sm">
            Os dados são verificados com hash SHA-512 e assinatura digital
            Ed25519 emitida pelo TSE. Apenas BUs autenticos são aceitos.
          </p>
        </div>
        <div className="bg-white rounded-lg p-6 shadow-sm border">
          <h3 className="font-semibold text-lg mb-2">3. Confira</h3>
          <p className="text-gray-600 text-sm">
            Acompanhe a totalização independente em tempo real. Os resultados
            ficam disponíveis publicamente via CDN.
          </p>
        </div>
      </section>
    </div>
  );
}
