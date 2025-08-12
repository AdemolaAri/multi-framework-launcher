import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [vue()],
  base: "/vue/",
  server: {
    host: "0.0.0.0",
    port: 5173,
    strictPort: true,
    headers: {
      "X-Frame-Options": "SAMEORIGIN",
      "Access-Control-Allow-Origin": "*",
    },
    cors: true,
  },
  build: {
    outDir: "dist",
    assetsDir: "assets",
  },
});
