// frontend/src/services/api.ts
import axios from 'axios'

export const api = axios.create({
  baseURL: __API_URL__,      // sustituido en build por VITE_API_URL o VITE_API_URL_DEV
  timeout: 10000,
})
