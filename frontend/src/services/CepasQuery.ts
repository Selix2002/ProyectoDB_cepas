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
 * Fetch de almacenamiento con control de errores y validación de datos.
 * @returns Promise<any[]>: array de storage o array vacío si hay error o datos inválidos.
 */
export const fetchStorageFull = (): Promise<any[]> =>
  axios
    .get("/almacenamiento/get-all")
    .then((res) => {
      // Si tu API wrappea los datos en { data: […] }, extráelos:
      const payload = Array.isArray(res.data)
        ? res.data
        : res.data.data ?? [];
      if (!Array.isArray(payload)) {
        console.error("fetchStorageFull → datos inválidos:", res.data);
        return [];
      }
      return payload;
    })
    .catch((error) => {
      if (axios.isAxiosError(error)) {
        console.error(
          `fetchStorageFull AxiosError [${error.response?.status}]:`,
          error.message
        );
      } else {
        console.error("fetchStorageFull Error inesperado:", error);
      }
      return [];
    });
