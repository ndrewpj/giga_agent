import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import compression from "vite-plugin-compression";

export default defineConfig({
  plugins: [
    react(),
    compression({
      algorithm: "gzip",
      ext: ".gz",
      // включаем .map
      filter: /\.(js|mjs|json|css|map)$/i,
      threshold: 1024, // сжимать файлы больше 1КБ
      deleteOriginFile: false,
    }),
  ],
  server: {
    proxy: {
      "/files": {
        target: "http://127.0.0.1:9092/",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/files/, ""),
      },
      "/graph": {
        target: "http://127.0.0.1:2024/",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/graph/, ""),
      },
    },
    port: 3000,
  },
  build: {
    outDir: "dist",
    sourcemap: false,
  },
});
