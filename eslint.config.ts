import globals from "globals";
import eslint from "@eslint/js";
import tseslint from "typescript-eslint";
import pluginReact from "eslint-plugin-react";
import eslintConfigPrettier from "eslint-config-prettier";
import { includeIgnoreFile } from "@eslint/compat";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const gitignorePath = path.resolve(__dirname, ".gitignore");

export default tseslint.config(
  {
    name: "eslint/recommended",
    ...eslint.configs.recommended,
  },
  tseslint.configs.stylisticTypeChecked,
  tseslint.configs.strictTypeChecked,
  {
    name: "typescript-eslint/enable typed linting",
    languageOptions: {
      parserOptions: {
        projectService: true,
        tsconfigRootDir: import.meta.dirname,
      },
    },
  },
  {
    ...tseslint.configs.disableTypeChecked,
    files: ["postcss.config.cjs"],
    name: "typescript-eslint/ignore postcss.config.cjs",
  },
  includeIgnoreFile(gitignorePath),
  {
    name: "eslint-config-prettier",
    ...eslintConfigPrettier,
  },
  {
    name: "eslint-plugin-react/recommended",
    ...pluginReact.configs.flat.recommended,
  },
  {
    name: "eslint-plugin-react/jsx-runtime",
    ...pluginReact.configs.flat["jsx-runtime"],
  },
  {
    name: "eslint-plugin-react/set version",
    settings: {
      react: {
        version: "detect",
      },
    },
  },
  {
    name: "overrides",
    files: ["**/*.{js,mjs,cjs,jsx,mjsx,ts,tsx,mtsx}"],
    languageOptions: {
      globals: {
        ...globals.serviceworker,
        ...globals.browser,
        ...globals.node,
      },
    },
  },
);
