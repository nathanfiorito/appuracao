
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

/** @type { import('@storybook/nextjs-vite').StorybookConfig } */
const config = {
  stories: [
    "../src/**/*.mdx",
    "../src/**/*.stories.@(js|jsx|mjs|ts|tsx)",
  ],
  addons: [
    "@chromatic-com/storybook",
    "@storybook/addon-vitest",
    "@storybook/addon-a11y",
    "@storybook/addon-docs",
    "@storybook/addon-onboarding",
  ],
  framework: "@storybook/nextjs-vite",
  viteFinal: async (config) => {
    config.resolve.alias = {
      ...config.resolve.alias,
      "html5-qrcode": path.resolve(__dirname, "../src/__mocks__/html5-qrcode.ts"),
    };
    return config;
  },
};
export default config;