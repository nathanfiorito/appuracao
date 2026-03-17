import type { ElectionSummary } from "@/lib/types";

interface Props {
  election: ElectionSummary;
}

export default function BulletinCard({ election }: Props) {
  const turnout =
    election.eligible_voters > 0
      ? ((election.compared_voters / election.eligible_voters) * 100).toFixed(1)
      : "0.0";

  return (
    <div className="bg-white rounded-lg border shadow-sm p-4 space-y-1 text-sm">
      <div className="flex justify-between items-start">
        <div>
          <p className="font-semibold">
            {election.state} — Pleito {election.plea} / Turno {election.turn}
          </p>
          <p className="text-gray-500 text-xs">Processo: {election.process}</p>
        </div>
        <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">
          {election.sections_counted} seções
        </span>
      </div>

      <div className="grid grid-cols-3 gap-2 pt-2 text-center">
        <div>
          <p className="font-semibold">{election.eligible_voters.toLocaleString("pt-BR")}</p>
          <p className="text-xs text-gray-500">Aptos</p>
        </div>
        <div>
          <p className="font-semibold">{election.compared_voters.toLocaleString("pt-BR")}</p>
          <p className="text-xs text-gray-500">Compareceram</p>
        </div>
        <div>
          <p className="font-semibold">{turnout}%</p>
          <p className="text-xs text-gray-500">Participação</p>
        </div>
      </div>
    </div>
  );
}
