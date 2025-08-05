import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    // Esto asegura que en desarrollo, las llamadas a /api se redirijan al backend
    proxy: {
      '/api': {
        target: 'https://proyectodb-cepas-v14l.onrender.com',
        changeOrigin: true,
      },
    },
  },
})