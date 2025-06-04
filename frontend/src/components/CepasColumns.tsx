
// src/components/cepasColumns.ts
import type { ColDef } from "ag-grid-community";

export const cepasColumnDefs: ColDef[] = [
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
    headerName: "AMP (µg/ml)",
    field: "resistencia_antibiotica.amp",
    filter: "agNumberColumnFilter",
  },
  {
    headerName: "CTX (µg/ml)",
    field: "resistencia_antibiotica.ctx",
    filter: "agNumberColumnFilter",
  },
  {
    headerName: "CXM (µg/ml)",
    field: "resistencia_antibiotica.cxm",
    filter: "agNumberColumnFilter",
  },
  {
    headerName: "CAZ (µg/ml)",
    field: "resistencia_antibiotica.caz",
    filter: "agNumberColumnFilter",
  },
  {
    headerName: "AK (µg/ml)",
    field: "resistencia_antibiotica.ak",
    filter: "agNumberColumnFilter",
  },
  {
    headerName: "C (µg/ml)",
    field: "resistencia_antibiotica.c",
    filter: "agTextColumnFilter",
  },
  {
    headerName: "TE (µg/ml)",
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
    headerName: "Responsable",
    field: "proyecto.responsable",
    filter: "agTextColumnFilter",
  },
  {
    headerName: "Nombre del Proyecto",
    field: "proyecto.nombre_proyecto",
    filter: "agTextColumnFilter",
  },
  // Si después agregas más columnas, las añades aquí
];
