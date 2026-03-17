import type { Meta, StoryObj } from "@storybook/react";
import BulletinCard from "./BulletinCard";

const meta: Meta<typeof BulletinCard> = {
  title: "Components/BulletinCard",
  component: BulletinCard,
};

export default meta;
type Story = StoryObj<typeof BulletinCard>;

export const Default: Story = {
  args: {
    election: {
      process_key: "2022-BR-1",
      process: "142",
      plea: "2022",
      turn: "1",
      state: "SP",
      sections_counted: 312,
      eligible_voters: 34500000,
      compared_voters: 28000000,
      absent_voters: 6500000,
      cargos: [],
    },
  },
};

export const HighTurnout: Story = {
  args: {
    election: {
      process_key: "2022-BR-2",
      process: "142",
      plea: "2022",
      turn: "2",
      state: "MG",
      sections_counted: 210,
      eligible_voters: 15000000,
      compared_voters: 14250000,
      absent_voters: 750000,
      cargos: [],
    },
  },
};

export const ZeroVoters: Story = {
  args: {
    election: {
      process_key: "2022-BR-0",
      process: "142",
      plea: "2022",
      turn: "1",
      state: "RO",
      sections_counted: 0,
      eligible_voters: 0,
      compared_voters: 0,
      absent_voters: 0,
      cargos: [],
    },
  },
};
