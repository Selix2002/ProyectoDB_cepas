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

/**
 * Recorre el diccionario subido y, para cada cepa,
 * lanza un PATCH al endpoint /cepas/update-jsonb/:cepaNombre
 * insertando en su JSONB la nueva clave (attribute_name) con
 * el valor correspondiente.
 */
export async function updateCepasJSONB(
  fileDict: Record<string, string>
): Promise<void> {
  const { attribute_name: newKey, ...values } = fileDict;
  if (!newKey) {
    throw new Error("La clave `attribute_name` es obligatoria");
  }

  const requests = Object.entries(values).map(([cepaNombre, valor]) =>
    axios.patch(
      `/cepas/update-jsonb/${encodeURIComponent(cepaNombre)}`,
      {
        datos_extra: { [newKey]: valor },
      }
    )
  );

  await Promise.all(requests);
}

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
    // 1) obtenemos el objeto actual (o uno vacío si no existe)
    const current = existingDatosExtras[cepaNombre] ?? {};
    // 2) mergeamos la nueva clave/valor
    const mergedDatosExtra = { ...current, [newKey]: valor };

    // 3) enviamos TODO el objeto merged
    console.log("🔁 [updateCepasJSONB] payload:", { datos_extra: mergedDatosExtra });
    return axios.patch(
      `/cepas/update-jsonb/${encodeURIComponent(cepaNombre)}`,
      { datos_extra: mergedDatosExtra }
    );
  });

  await Promise.all(requests);
}