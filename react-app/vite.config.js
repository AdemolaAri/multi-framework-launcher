import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  base: '/react/',
  server: {
    host: '0.0.0.0',
    port: 3000,
    strictPort: true,
    headers: {
      'X-Frame-Options': 'SAMEORIGIN',
      'Access-Control-Allow-Origin': '*'
    },
    cors: true
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets'
  }
});