// src/pages/HomePage.tsx
import { useState } from "react";
import DropdownMenu from "../components/DropdownMenu";
import CepasTable from "../components/CepasTable";
import type { GridReadyCallback } from "../components/CepasTable";
import type { GridApi, Column } from "ag-grid-community";
import { SlidersHorizontal, FlaskConical, MoreVertical } from "lucide-react";
import TableStats_col, { TableStats_row } from "../components/TableStats";
import { Link } from "react-router-dom";
import { exportToExcel } from '../utils/exportExcel';

export function HomePage() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [columns, setColumns] = useState<Column[]>([]);
  const [gridApi, setGridApi] = useState<GridApi>();
  const [rowCount_, setRowCount] = useState(0);

  // 1) Capturamos el GridApi y la lista inicial de Column[]
  const handleGridReady: GridReadyCallback = (params) => {
    const api = params.api;
    setGridApi(api);
    setColumns(api.getColumns() ?? []);
    const rowCount = api.getDisplayedRowCount();
    setRowCount(rowCount);
  };
  const handleExport = () => {
    console.log('Exportando a Excel: gridApi:', gridApi);
    if (!gridApi) return;
      exportToExcel(gridApi, 'Cepas', 'cepas.xlsx');
};

  // 2) Al hacer toggle, llamamos a gridApi.setColumnsVisible(...) y luego
  //    volvemos a leer api.getColumns() para actualizar el estado de los checkboxes
  const handleToggle = (colId: string, visible: boolean) => {
    if (!gridApi) return;
    // setColumnsVisible toma un array de IDs y el booleano deseado
    gridApi.setColumnsVisible([colId], visible);
    setColumns(gridApi.getColumns() ?? []);
  };

  return (
    <div className="flex flex-col min-h-screen bg-gray-900 text-white">
      {/* Cabecera */}
      <div className="relative h-16 flex items-center justify-center border-b border-gray-700 px-4">
        {/* Contenedor de botones en la esquina superior izquierda */}
        <div className="absolute left-4 flex space-x-2">
          <Link to="/home/addAtribute">
            <button>
              + Nuevo Atributo
            </button>
          </Link>

          <Link to="/home/addCepa">
            <button>
              + Nueva Cepa
            </button>
          </Link>
        </div>

        {/* Botón menú desplegable en esquina superior derecha */}
        {/* Botones en esquina superior derecha */}
        <div className="absolute top-1/2 right-4 transform -translate-y-1/2 flex space-x-2">
          <button onClick={handleExport}>
            Exportar
          </button>
          <button
            onClick={() => setMenuOpen((v) => !v)}
          >
            <MoreVertical className="h-6 w-6 text-white" />
          </button>
        </div>

        <DropdownMenu
          isOpen={menuOpen}
          columns={columns}
          onToggle={handleToggle}
          onClose={() => setMenuOpen(true)}
        />

        <span className="text-xl font-medium">
          Dashboard para Gestión de Cepas Bacterianas
        </span>
      </div>

      {/* Estadísticas */}
      <div className="p-15 flex flex-wrap items-center gap-4">
        {/* Atributos Definidos */}
        <div className="mr-auto flex items-center space-x-4 bg-gray-800 rounded-lg p-10">
          <div className="bg-green-500 p-3 rounded-full">
            <SlidersHorizontal className="h-6 w-6 text-white" />
          </div>
          <div className="flex flex-col">
            <span className="text-sm font-semibold text-green-400 uppercase">
              Atributos definidos
            </span>
            <TableStats_col colCount={columns.length} />
            <span className="text-sm text-gray-400">Registrados</span>
          </div>
        </div>

        {/* Total Cepas */}
        <div className="flex items-center space-x-4 bg-gray-800 rounded-lg p-10 div-cepas">
          <div className="bg-green-500 p-3 rounded-full">
            <FlaskConical className="h-6 w-6 text-white" />
          </div>
          <div className="flex flex-col">
            <span className="text-sm font-semibold text-green-400 uppercase">
              Total cepas
            </span>
            <TableStats_row rowCount={rowCount_} />
            <span className="text-sm text-gray-400">Registradas</span>
          </div>
        </div>
      </div>

      {/* Tabla de Cepas */}
      <div className="flex-1 border-t border-gray-700 p-4 box-border">
        <CepasTable onGridReady={handleGridReady} />
      </div>
    </div>
  );
}

export default HomePage;
