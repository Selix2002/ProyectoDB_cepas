import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig(({ mode }) => {
  // 1) Carga todas las env vars en process.cwd()
  const env = loadEnv(mode, process.cwd(), '')

  // 2) Define la base de tu API: en dev usamos VITE_API_URL_DEV; en prod, VITE_API_URL
  const API_URL = env.VITE_API_URL_PROD

  return {
    plugins: [react(), tailwindcss()],
    define: {
      // 3) Reemplaza en el código todas las referencias a import.meta.env.API_URL por la cadena final
      __API_URL__: JSON.stringify(API_URL),
    },
    server: {
      proxy: {
        '/users': { target: API_URL, changeOrigin: true },
        '/cepas': { target: API_URL, changeOrigin: true },
      },
    },
  }
})
