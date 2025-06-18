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

/**
 * Define aquí la forma exacta del payload que acepta el DTO de update en el backend.
 */
export interface CepaUpdatePayload {
  // Campos directos de Cepa
  nombre?: string;
  cod_lab?: string;
  origen?: string;
  pigmentacion?: string;
  datos_extra?: Record<string, any>; // Para campos JSONB adicionales
  // … agrega aquí el resto de columnas escalares de tu tabla CEPAS

  // Relaciones uno-a-uno como objetos anidados
  almacenamiento?: {
    envio_puq?: string;
    temperatura_menos80?: string;
    
    // … demás campos de Almacenamiento
  };
  medio_cultivo?: {
    medio?: string;
    // … demás campos de MedioCultivo
  };
  morfologia?: {
    gram?: string;
    morfologia_1?: string;
    morfologia_2?: string;
  };
  actividad_enzimatica?: {
    aia?: string;
    amilasa?: string;
    catalasa?: string;
    celulasa?: string;
    fosfatasa?: string;
    lecitinasa?: string;
    ureasa?: string;
    lipasa?: string;
    proteasa?: string;
    // … demás campos de ActividadEnzimatica
  };
  crecimiento_temperatura?: {
    temp_5?: number;
    temp_25?: number;
    temp_37?: number;
    // … demás campos de CrecimientoTemperatura
  };
  resistencia_antibiotica?: {
    amp?: string;
    ctx?: string;
    cxm?: string;
    caz?: string;
    ak?: string;
    c?: string;
    te?: string;
    am_ecoli?: string;
    am_saureus?: string;
    // … demás campos de ResistenciaAntibiotica
  };
  caracterizacion_genetica?: {
    gen_16s?: string;
    metabolomica?: string;

  };
  proyecto?: {
    nombre_proyecto?: string;
    responsable?: string;
    // … demás campos de Proyecto
  };
}

/**
 * updateCepa: envía un PATCH a /cepas/update/{cepaId}
 */
export const updateCepa = (
  cepaId: number,
  data: CepaUpdatePayload
): Promise<any> =>
  axios
    .patch(`/cepas/update/${cepaId}`, data)
    .then((res) => res.data)
    .catch((error) => {
      console.log("Data", data);
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

export async function createCepa(
  data: Record<string, any>
): Promise<any> {
  return axios
    .post("/cepas/create", data)
    .then((res) => res.data)
    .catch((error) => {
      console.error("Error al crear la cepa:", error);
      throw error;
    });
}