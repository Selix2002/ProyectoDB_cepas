import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig(({ mode }) => {
  // 1) Carga las variables de entorno (incluye VITE_API_URL)
  const env = loadEnv(mode, process.cwd(), '')

  // 2) Extrae la URL de tu API (por ejemplo "http://localhost:8000" o tu URL en Render)
  const API_URL = "https://proyectodb-cepas-v14l.onrender.com"

  return {
    plugins: [react(), tailwindcss()],
    server: {
      proxy: {
        // Proxyea todas las llamadas a /almacenamiento y /cepas
        '/almacenamiento': {
          target: API_URL,
          changeOrigin: true,
        },
        '/cepas': {
          target: API_URL,
          changeOrigin: true,
        },
      },
    },
    // Opcional: si necesitas exponer más vars a tu cliente
    define: {
      'process.env': {}
    }
  }
})
