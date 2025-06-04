import axios from "axios";

/**
 * Fetch de cepas con control de errores y validación de datos.
 * @returns Promise<any[]>: array de cepas o array vacío si hay error o datos inválidos.
 */
export const fetchCepasFull = (): Promise<any[]> =>
  axios
    .get("/cepas/get-all")
    .then((res) => {
      // Validamos que res.data sea un array
      if (!res.data || !Array.isArray(res.data)) {
        console.error("fetchCepasFull → datos inválidos:", res.data);
        return [];
      }
      return res.data;
    })
    .catch((error) => {
      // Errores de red, timeout, 5xx, etc.
      if (axios.isAxiosError(error)) {
        console.error(
          `fetchCepasFull AxiosError [${error.response?.status}]:`,
          error.message
        );
      } else {
        console.error("fetchCepasFull Error inesperado:", error);
      }
      return [];
    });

    /**
 * updateCepa: envía un PATCH a /cepas/update/{id}
 * @param cepaId el ID de la cepa a actualizar
 * @param data un objeto con los campos que cambiaron (p. ej. { nombre: "XYZ" } o { almacenamiento: { temperatura_menos80: true } })
 */
export const updateCepa = (
  cepaId: number,
  data: Record<string, any>
): Promise<any> =>
  axios
    .patch(`/cepas/update/${cepaId}`, data)
    .then((res) => res.data)
    .catch((error) => {
      console.error(`Error al actualizar la cepa ${cepaId}:`, error);
      throw error;
    });
