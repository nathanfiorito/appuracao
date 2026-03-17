import type { CargoResult } from "@/lib/types";

const CARGO_NAMES: Record<string, string> = {
  "1": "Presidente",
  "3": "Governador",
  "5": "Senador",
  "6": "Deputado Federal",
  "7": "Deputado Estadual",
  "8": "Deputado Distrital",
  "11": "Prefeito",
  "13": "Vereador",
};

interface Props {
  cargo: CargoResult;
}

export default function ResultsTable({ cargo }: Props) {
  const cargoName = CARGO_NAMES[cargo.cargo_code] ?? `Cargo ${cargo.cargo_code}`;
  const totalValid = cargo.total_votes - cargo.blank_votes - cargo.null_votes;

  return (
    <div className="bg-white rounded-lg border shadow-sm overflow-hidden">
      <div className="px-4 py-3 bg-gray-50 border-b flex items-center justify-between">
        <h3 className="font-semibold">{cargoName}</h3>
        <span className="text-xs text-gray-500">{cargo.sections_counted} seções apuradas</span>
      </div>

      <table className="w-full text-sm">
        <thead>
          <tr className="text-left text-gray-500 border-b">
            <th className="px-4 py-2">Número</th>
            <th className="px-4 py-2 text-right">Votos</th>
            <th className="px-4 py-2 text-right">%</th>
          </tr>
        </thead>
        <tbody>
          {cargo.candidates.map((c) => (
            <tr key={c.number} className="border-b last:border-0 hover:bg-gray-50">
              <td className="px-4 py-2 font-mono">{c.number}</td>
              <td className="px-4 py-2 text-right font-semibold">{c.votes.toLocaleString("pt-BR")}</td>
              <td className="px-4 py-2 text-right text-gray-600">
                {totalValid > 0 ? ((c.votes / totalValid) * 100).toFixed(1) : "0.0"}%
              </td>
            </tr>
          ))}
          <tr className="bg-gray-50 text-gray-500 text-xs">
            <td className="px-4 py-2">Brancos</td>
            <td className="px-4 py-2 text-right">{cargo.blank_votes.toLocaleString("pt-BR")}</td>
            <td className="px-4 py-2 text-right">
              {cargo.total_votes > 0
                ? ((cargo.blank_votes / cargo.total_votes) * 100).toFixed(1)
                : "0.0"}%
            </td>
          </tr>
          <tr className="bg-gray-50 text-gray-500 text-xs">
            <td className="px-4 py-2">Nulos</td>
            <td className="px-4 py-2 text-right">{cargo.null_votes.toLocaleString("pt-BR")}</td>
            <td className="px-4 py-2 text-right">
              {cargo.total_votes > 0
                ? ((cargo.null_votes / cargo.total_votes) * 100).toFixed(1)
                : "0.0"}%
            </td>
          </tr>
        </tbody>
        <tfoot>
          <tr className="font-semibold border-t">
            <td className="px-4 py-2">Total</td>
            <td className="px-4 py-2 text-right">{cargo.total_votes.toLocaleString("pt-BR")}</td>
            <td className="px-4 py-2 text-right">100%</td>
          </tr>
        </tfoot>
      </table>
    </div>
  );
}
