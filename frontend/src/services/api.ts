// src/services/api.ts
import axios from "axios";

const baseURL = "127.0.0.1:7000"

export const api = axios.create({
  baseURL,
  timeout: 60_000,
});