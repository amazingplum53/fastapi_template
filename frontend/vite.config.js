import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        auth: "frontend/src/auth.jsx",
      },
      output: {
        entryFileNames: "[name].js",
      },
    },
    outDir: "static/js",
    emptyOutDir: false,
  },
  plugins: [react()],
});
