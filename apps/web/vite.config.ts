import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const configuredApi = process.env.VITE_API_BASE_URL ?? "http://localhost:8000";
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
