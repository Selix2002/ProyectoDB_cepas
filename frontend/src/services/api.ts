// src/services/api.ts
import axios from "axios";

// Lee la variable de entorno VITE_API_URL definida por Vite
const baseURL = import.meta.env.VITE_API_URL;

export const api = axios.create({
  baseURL,
  timeout: 60_000, // 60 segundos
});