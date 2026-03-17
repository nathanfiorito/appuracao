import type { Meta, StoryObj } from "@storybook/react";
import ResultsTable from "./ResultsTable";

const meta: Meta<typeof ResultsTable> = {
  title: "Components/ResultsTable",
  component: ResultsTable,
};

export default meta;
type Story = StoryObj<typeof ResultsTable>;

export const Presidente: Story = {
  args: {
    cargo: {
      cargo_code: "1",
      sections_counted: 450,
      total_votes: 5000000,
      blank_votes: 120000,
      null_votes: 80000,
      candidates: [
        { number: "13", votes: 2900000, name: "Candidato A" },
        { number: "22", votes: 1900000, name: "Candidato B" },
      ],
    },
  },
};

export const Vereador: Story = {
  args: {
    cargo: {
      cargo_code: "13",
      sections_counted: 98,
      total_votes: 180000,
      blank_votes: 5000,
      null_votes: 3000,
      candidates: [
        { number: "44001", votes: 42000 },
        { number: "44002", votes: 31000 },
        { number: "44003", votes: 28500 },
        { number: "44004", votes: 21000 },
        { number: "44005", votes: 18000 },
        { number: "44006", votes: 15500 },
        { number: "44007", votes: 12000 },
        { number: "44008", votes: 4000 },
      ],
    },
  },
};

export const NoBlanksOrNulls: Story = {
  args: {
    cargo: {
      cargo_code: "11",
      sections_counted: 55,
      total_votes: 90000,
      blank_votes: 0,
      null_votes: 0,
      candidates: [
        { number: "55", votes: 54000 },
        { number: "10", votes: 36000 },
      ],
    },
  },
};
