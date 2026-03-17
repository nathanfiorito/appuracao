export interface CandidateResult {
  number: string;
  votes: number;
  name?: string;
}

export interface CargoResult {
  cargo_code: string;
  sections_counted: number;
  total_votes: number;
  blank_votes: number;
  null_votes: number;
  candidates: CandidateResult[];
}

export interface ElectionSummary {
  process_key: string;
  process: string;
  plea: string;
  turn: string;
  state: string;
  sections_counted: number;
  eligible_voters: number;
  compared_voters: number;
  absent_voters: number;
  cargos: CargoResult[];
}

export interface ResultsSummary {
  generated_at: string;
  elections: ElectionSummary[];
}

export interface IngestResponse {
  status: "accepted";
  execution_id: string;
}
