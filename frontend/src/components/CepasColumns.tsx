
// src/components/cepasColumns.ts
import type { ColDef } from "ag-grid-community";

export const getCepasColumnDefs = (data: any[]): ColDef[] => {


const fixedCols: ColDef[] = [


  {
    headerName: "ID",
    field: "id",
    filter: "agNumberColumnFilter",
    pinned: "left",
    width: 80,
    editable: false,
    sort: "asc",            // ← aquí indicamos orden ascendente por defecto
  },
  {
    headerName: "Cepa",
    field: "nombre",
    filter: "agTextColumnFilter",
    pinned: "left",
    width: 80,
  },
  {
    headerName: "Código Lab",
    field: "cod_lab",
    filter: "agTextColumnFilter",
    width: 150,
  },
  { headerName: "Origen", field: "origen", filter: "agTextColumnFilter" },
  {
    headerName: "Pigmentación",
    field: "pigmentacion",
    filter: "agTextColumnFilter",
  },
  {
    headerName: "Envío a Punta Arenas",
    field: "almacenamiento.envio_puq",
    filter: "agTextColumnFilter",
  },
  {
    headerName: "Temperatura -80°",
    field: "almacenamiento.temperatura_menos80",
    filter: "agTextColumnFilter",
  },
  {
    headerName: "Medio",
    field: "medio_cultivo.medio",
    filter: "agTextColumnFilter",
  },
  {
    headerName: "Gram",
    field: "morfologia.gram",
    filter: "agTextColumnFilter",
  },
  {
    headerName: "Morfología 1",
    field: "morfologia.morfologia_1",
    filter: "agTextColumnFilter",
  },
  {
    headerName: "Morfología 2",
    field: "morfologia.morfologia_2",
    filter: "agTextColumnFilter",
  },
  {
    headerName: "Lecitinasa",
    field: "actividad_enzimatica.lecitinasa",
    filter: "agTextColumnFilter",
  },
  {
    headerName: "Ureasa",
    field: "actividad_enzimatica.ureasa",
    filter: "agTextColumnFilter",
  },
  {
    headerName: "Lipasa",
    field: "actividad_enzimatica.lipasa",
    filter: "agTextColumnFilter",
  },
  {
    headerName: "Amilasa",
    field: "actividad_enzimatica.amilasa",
    filter: "agTextColumnFilter",
  },
  {
    headerName: "Proteasa",
    field: "actividad_enzimatica.proteasa",
    filter: "agTextColumnFilter",
  },
  {
    headerName: "Catalasa",
    field: "actividad_enzimatica.catalasa",
    filter: "agTextColumnFilter",
  },
  {
    headerName: "Celulasa",
    field: "actividad_enzimatica.celulasa",
    filter: "agNumberColumnFilter",
  },
  {
    headerName: "Fosfatasa",
    field: "actividad_enzimatica.fosfatasa",
    filter: "agNumberColumnFilter",
  },
  {
    headerName: "AIA",
    field: "actividad_enzimatica.aia",
    filter: "agNumberColumnFilter",
  },
  {
    headerName: "+ 5°C",
    field: "crecimiento_temperatura.temp_5",
    filter: "agNumberColumnFilter",
  },
  {
    headerName: "+ 25°C",
    field: "crecimiento_temperatura.temp_25",
    filter: "agNumberColumnFilter",
  },
  {
    headerName: "+ 37°C",
    field: "crecimiento_temperatura.temp_37",
    filter: "agNumberColumnFilter",
  },
  {
    headerName: "AMP ",
    field: "resistencia_antibiotica.amp",
    filter: "agNumberColumnFilter",
  },
  {
    headerName: "CTX ",
    field: "resistencia_antibiotica.ctx",
    filter: "agNumberColumnFilter",
  },
  {
    headerName: "CXM ",
    field: "resistencia_antibiotica.cxm",
    filter: "agNumberColumnFilter",
  },
  {
    headerName: "CAZ ",
    field: "resistencia_antibiotica.caz",
    filter: "agNumberColumnFilter",
  },
  {
    headerName: "AK ",
    field: "resistencia_antibiotica.ak",
    filter: "agNumberColumnFilter",
  },
  {
    headerName: "C ",
    field: "resistencia_antibiotica.c",
    filter: "agTextColumnFilter",
  },
  {
    headerName: "TE ",
    field: "resistencia_antibiotica.te",
    filter: "agTextColumnFilter",
  },
  {
    headerName: "AM E.COLI",
    field: "resistencia_antibiotica.am_ecoli",
    filter: "agTextColumnFilter",
  },
  {
    headerName: "AM SAUREUS",
    field: "resistencia_antibiotica.am_saureus",
    filter: "agTextColumnFilter",
  },
  {
    headerName: "Gen. 16s",
    field: "caracterizacion_genetica.gen_16s",
    filter: "agTextColumnFilter",
  },
  {
    headerName: "Metabolómica",
    field: "caracterizacion_genetica.metabolomica",
    filter: "agTextColumnFilter",
  },
  {
    headerName: "Nicolas",
    field: "proyecto.responsable",
    filter: "agTextColumnFilter",
  },
  {
    headerName: "Nombre del Proyecto",
    field: "proyecto.nombre_proyecto",
    filter: "agTextColumnFilter",
  },

]

const extraKeys = Array.from(
  new Set(
    data
      .filter((c) => c.datos_extra)               // filtra solo cepas con datos_extra
      .flatMap((c) => Object.keys(c.datos_extra!)) // todas las claves
  )
);

  // 3. Generar una columna para cada clave
  const extraCols: ColDef[] = extraKeys.map((key) => ({
    headerName: key,
    // usamos valueGetter para leer params.data.datos_extra[key]
    valueGetter: (params) =>
      params.data.datos_extra ? params.data.datos_extra[key] : null,
    // si quieres edición inline:
    editable: true,
    field: `datos_extra.${key}`, // opcional, en caso de usar APIs de Ag-Grid que requieran field
  }));
  return [...fixedCols, ...extraCols];
}
