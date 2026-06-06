import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        login: "src/auth/login.jsx",
      },
      output: {
        entryFileNames: "assets/[name].js",
      },
    },
    outDir: "../static/js",
    emptyOutDir: false,
  },
  plugins: [react()],
});
