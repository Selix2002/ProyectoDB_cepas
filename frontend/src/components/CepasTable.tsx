import { useMemo} from "react";
import { AgGridReact } from "ag-grid-react";
import { AllCommunityModule, ModuleRegistry } from "ag-grid-community";
import { useCombinedData } from "../hooks/useCepasFull";
ModuleRegistry.registerModules([AllCommunityModule]);

/**
 * CepasTable: componente independiente que renderiza un Ag Grid con datos de cepas cargadas desde la API.
 */
export function CepasTable() {
  const { rowData, loading, error } = useCombinedData();
  const paginationPageSizeSelector = useMemo(() => [10, 20, 50, 70, 100], []);

const columnDefs = useMemo(
  () => [
    {
      headerName: "ID",
      field: "id",
      filter: "agNumberColumnFilter",
      pinned: "left",
      width: 80,
      editable: false, // No editable
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
      field: "envio_puq",
      filter: "agTextColumnFilter",
    },
    { headerName: "Temperatura -80°", field: "temperatura_menos80", filter: "agTextColumnFilter" },
    {
      headerName: "Morfología",
      field: "morfologia",
      filter: "agTextColumnFilter",
    },
    {
      headerName: "Lecitinasa",
      field: "lecitinasa",
      filter: "agTextColumnFilter",
    },
    { headerName: "Ureasa", field: "ureasa", filter: "agTextColumnFilter" },
    { headerName: "Lipasa", field: "lipasa", filter: "agTextColumnFilter" },
    { headerName: "Amilasa", field: "amilasa", filter: "agTextColumnFilter" },
    {
      headerName: "Proteasa",
      field: "proteasa",
      filter: "agTextColumnFilter",
    },
    {
      headerName: "Catalasa",
      field: "catalasa",
      filter: "agTextColumnFilter",
    },
    {
      headerName: "Celulasa",
      field: "celulasa",
      filter: "agTextColumnFilter",
    },
    {
      headerName: "Fosfatasa",
      field: "fosfatasa",
      filter: "agTextColumnFilter",
    },
    { headerName: "AIA", field: "aia", filter: "agTextColumnFilter" },
    { headerName: "-80° C", field: "-80C", filter: "agNumberColumnFilter" },
    { headerName: "+5 °C", field: "+5C", filter: "agNumberColumnFilter" },
    { headerName: "+25 °C", field: "+25C", filter: "agNumberColumnFilter" },
    { headerName: "+37 °C", field: "+37C", filter: "agNumberColumnFilter" },
    {
      headerName: "+AMP (µg/ml)",
      field: "+AMP_mg_ml_",
      filter: "agNumberColumnFilter",
    },
    {
      headerName: "+CTX (µg/ml)",
      field: "+CTX_mg_ml_",
      filter: "agNumberColumnFilter",
    },
    {
      headerName: "+CXM (µg/ml)",
      field: "+CXM_mg_ml_",
      filter: "agNumberColumnFilter",
    },
    {
      headerName: "+CAZ (µg/ml)",
      field: "+CAZ_mg_ml_",
      filter: "agNumberColumnFilter",
    },
    {
      headerName: "+AK (µg/ml)",
      field: "+AK_mg_ml_",
      filter: "agNumberColumnFilter",
    },
    {
      headerName: "+C (µg/ml)",
      field: "+C_mg_ml_",
      filter: "agNumberColumnFilter",
    },
    {
      headerName: "+TE (µg/ml)",
      field: "+TE_mg_ml_",
      filter: "agNumberColumnFilter",
    },
    {
      headerName: "AM E.coli",
      field: "am_e_coli",
      filter: "agTextColumnFilter",
    },
    {
      headerName: "AM S.aureus",
      field: "am_s_aureus",
      filter: "agTextColumnFilter",
    },
    {
      headerName: "16S rRNA",
      field: "16s_rna",
      filter: "agTextColumnFilter",
    },
    {
      headerName: "Metabolómica",
      field: "metabolomica",
      filter: "agTextColumnFilter",
    },
    { headerName: "Nicolás", field: "nicolas", filter: "agTextColumnFilter" },
    {
      headerName: "Proyecto",
      field: "proyecto",
      filter: "agTextColumnFilter",
    },
    // Añade aquí más columnas según tus relaciones...
  ],
  []
);
   if (loading) return <div>Cargando cepas...</div>;
  if (error) return <div>Error al cargar datos: {error.message}</div>;
  return (
    // 1) Este wrapper limita el ancho y añade scroll horizontal
    <div
      style={{
        width: "flex", // ancho máximo visible
        overflowX: "auto", // habilita scroll-x cuando haga falta
      }}
    >
      {/* 2) El grid en sí puede tener un minWidth mayor */}
      <div
        className="ag-theme-alpine custom-space"
        style={{
          width: "100%", // ocupa todo el wrapper
          minWidth: "1000px", // ancho mínimo para forzar scroll
        }}
      >
        <AgGridReact
          columnDefs={columnDefs}
          rowData={rowData}
          defaultColDef={{
            minWidth: 100, // ancho mínimo de cada columna
            filter: true, // habilita el filtrado por defecto
            sortable: true,
            editable: true, // habilita la edición de celdas
            resizable: true,
            wrapHeaderText: true, // habilita el redimensionamiento de columnas
          }}
          pagination
          paginationPageSize={10}
          paginationPageSizeSelector={paginationPageSizeSelector}
          domLayout="autoHeight"
          //autoHeaderHeight={true}
        />
      </div>
    </div>
  );
}

export default CepasTable;

