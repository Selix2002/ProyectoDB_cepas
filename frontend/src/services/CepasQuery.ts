// frontend/src/services/cepasQuery.ts

import api from "./api";
import axios from "axios";

/**
 * Fetch de cepas con control de errores y validación de datos.
 * @returns Promise<any[]>: array de cepas o array vacío si hay error o datos inválidos.
 */
export const fetchCepasFull = (): Promise<any[]> =>
  api
    .get("/cepas/get-all")
    .then((res) => {
      if (!res.data || !Array.isArray(res.data)) {
        console.error("fetchCepasFull → datos inválidos:", res.data);
        return [];
      }
      return res.data;
    })
    .catch((error) => {
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
 * @param data un objeto con los campos que cambiaron
 */
export const updateCepa = (
  cepaId: number,
  data: Record<string, any>
): Promise<any> =>
  api
    .patch(`/cepas/update/${cepaId}`, data)
    .then((res) => res.data)
    .catch((error) => {
      console.error(`Error al actualizar la cepa ${cepaId}:`, error);
      throw error;
    });

/**
 * Inserta una nueva clave/valor en el JSONB de cada cepa
 */
export async function updateCepasJSONB(
  fileDict: Record<string, string>
): Promise<void> {
  const { attribute_name: newKey, ...values } = fileDict;
  if (!newKey) {
    throw new Error("La clave `attribute_name` es obligatoria");
  }

  const requests = Object.entries(values).map(([cepaNombre, valor]) =>
    api.patch(
      `/cepas/update-jsonb/${encodeURIComponent(cepaNombre)}`,
      { datos_extra: { [newKey]: valor } }
    )
  );
  await Promise.all(requests);
}

/**
 * Variante que mergea con los datos_extra existentes (útil si trabajas con tabla editable)
 */
export async function updateCepasJSONB_forTable(
  fileDict: Record<string, string>,
  existingDatosExtras: Record<string, Record<string, any>>
): Promise<void> {
  const { attribute_name: newKey, ...values } = fileDict;
  if (!newKey) {
    throw new Error("La clave `attribute_name` es obligatoria");
  }
  console.log(fileDict);

  const requests = Object.entries(values).map(([cepaNombre, valor]) => {
    const current = existingDatosExtras[cepaNombre] ?? {};
    const mergedDatosExtra = { ...current, [newKey]: valor };
    console.log("🔁 [updateCepasJSONB] payload:", { datos_extra: mergedDatosExtra });

    return api.patch(
      `/cepas/update-jsonb/${encodeURIComponent(cepaNombre)}`,
      { datos_extra: mergedDatosExtra }
    );
  });

  await Promise.all(requests);
}

/**
 * Crea una nueva cepa vía POST /cepas/create
 */
export async function createCepa(
  data: Record<string, any>
): Promise<any> {
  return api
    .post("/cepas/create", data)
    .then((res) => res.data)
    .catch((error) => {
      console.error("Error al crear la cepa:", error);
      throw error;
    });
}
