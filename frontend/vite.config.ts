import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
const target = "https://tu-backend-en-render.onrender.com"
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    proxy: {
      "/almacenamiento": {
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
