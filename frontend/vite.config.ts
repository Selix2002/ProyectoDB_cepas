import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
const target = "http://localhost:8000"
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    proxy: {
      "/users": {
        target: target,
        changeOrigin: true,
      },
      "/cepas":{
        target: target,
        changeOrigin:true
      }
    },
  },
});
