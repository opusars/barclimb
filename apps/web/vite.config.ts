import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const appEnvironment = process.env.VITE_APP_ENV ?? "local";
if (!["local", "staging", "production"].includes(appEnvironment)) {
  throw new Error("VITE_APP_ENV must be local, staging, or production");
}
if (appEnvironment !== "local" && process.env.VITE_API_BASE_URL) {
  throw new Error(
    "deployed Web uses same-origin /api and must not set VITE_API_BASE_URL",
  );
}
const configuredApi =
  appEnvironment === "local"
    ? (process.env.VITE_API_BASE_URL ?? "http://localhost:8000")
    : "https://same-origin.invalid";
const backendOrigin = configuredApi
  .replace(/\/api\/v1\/?$/, "")
  .replace(/\/$/, "");

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": {
        target: backendOrigin,
        changeOrigin: false,
      },
    },
  },
});
