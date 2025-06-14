// src/services/api.ts
import axios from "axios";

const baseURL = import.meta.env.PROD
  ? import.meta.env.VITE_API_URL_PROD      // en Render: https://proyectodb-cepas-v14l.onrender.com
  : import.meta.env.VITE_API_URL_DEV; // en local: http://localhost:8000

export const api = axios.create({
  baseURL,
  timeout: 60_000,
});
