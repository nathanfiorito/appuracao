import type { Meta, StoryObj } from "@storybook/react";
import QrScanner from "./QrScanner";

const meta: Meta<typeof QrScanner> = {
  title: "Components/QrScanner",
  component: QrScanner,
  parameters: {
    // Camera won't work in Storybook — renders button layout only
    docs: {
      description: {
        component:
          "Componente de leitura de QR Code via câmera. No Storybook, a câmera não é ativada, mas o layout e botões ficam visíveis.",
      },
    },
  },
};

export default meta;
type Story = StoryObj<typeof QrScanner>;

export const Default: Story = {
  args: {
    onScan: (text: string) => console.log("QR scanned:", text),
    onError: (err: string) => console.error("QR error:", err),
  },
};
