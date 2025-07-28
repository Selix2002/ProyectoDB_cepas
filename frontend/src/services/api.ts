// src/services/api.ts
import axios from "axios";

const baseURL = "https://proyectodb-cepas-v14l.onrender.com"

export const api = axios.create({
  baseURL,
  timeout: 60_000,
});