// src/services/cepas.ts
import axios from "axios";

export interface Cepa {
  id: number;
  nombre: string;
  cod_lab: string;
  origen?: string;
  // añade aquí más campos según tu DTO de lectura
}

export const getCepsas = async (): Promise<Cepa[]> => {
  const res = await axios.get<Cepa[]>("/cepas/get-all");
  return res.data;
};
