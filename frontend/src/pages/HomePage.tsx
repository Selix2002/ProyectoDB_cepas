import { useState, useMemo, useRef,useCallback,useEffect } from "react";
import html2canvas from "html2canvas-pro";
import DropdownMenu from "../components/DropdownMenu";
import type { GridReadyCallback } from "../components/CepasTable";
import type { GridApi, Column } from "ag-grid-community";
import { MoreVertical } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import { exportToExcel } from "../utils/exportExcel";
import { useAuth } from "../stores/AuthContext";
import { updateVisibleCol } from "../services/UsersQuery";

// --- Se importan los componentes necesarios para el dashboard ---
import CepasTable from "../components/CepasTable";
import MyPieChart from "../components/PieChart";
import { processDataForPieChart } from "../components/PieData";

export function HomePage() {
  const { logout, user } = useAuth();
  const navigate = useNavigate();
  const chartRef = useRef<HTMLDivElement>(null);
  const [filterVersion, setFilterVersion] = useState(0);
  // --- ESTADOS PARA GESTIONAR LA COMUNICACIÓN ---
  // Este estado almacenará los datos crudos que nos envíe la tabla.
  const [rawTableData, setRawTableData] = useState<any[]>([]);
  // Este estado guardará la columna que el usuario seleccione.
  const [selectedColumn, setSelectedColumn] = useState<{ field: string; name: string } | null>(null);
  // --- Estados existentes ---
  const [gridApi, setGridApi] = useState<GridApi>();
  const [columns, setColumns] = useState<Column[]>([]);
  const [menuOpen, setMenuOpen] = useState(false);
  const [adminMenuOpen, setAdminMenuOpen] = useState(false);

  // --- FUNCIONES CALLBACK QUE SE PASARÁN A CepasTable ---

  // 1. Esta es la función que `CepasTable` llamará cuando sus datos estén listos.
  //    Almacena los datos en el estado de HomePage.
  const handleDataLoaded = useCallback((data: any[]) => {
    setRawTableData(data);
  }, []); // Dependencia vacía

  const handleFilterChanged = useCallback(() => {
    console.log("[HomePage] Filter changed, incrementing version trigger.");
    setFilterVersion(currentVersion => currentVersion + 1);
  }, []);

  useEffect(() => {
    if (!gridApi) return;
    gridApi.addEventListener('filterChanged', handleFilterChanged);
    return () => {
      if (gridApi) gridApi.removeEventListener('filterChanged', handleFilterChanged);
    };
  }, [gridApi, handleFilterChanged]);
  
  // 2. Esta función se ejecutará cuando el usuario haga clic en un radio button de la tabla.
  //    Actualiza el estado para saber qué columna está seleccionada.
  const handleColumnSelect = useCallback((selection: { field: string; name: string } | null) => {
    // Si la selección es la misma, la anula (para deseleccionar).
    if (selection && selectedColumn && selection.field === selectedColumn.field) {
      setSelectedColumn(null);
    } else {
      setSelectedColumn(selection);
    }
  }, [selectedColumn]); 

  // 3. Esta función se pasa para que HomePage siga teniendo control sobre la API de la grilla.
  const handleGridReady: GridReadyCallback = (params) => {
    setGridApi(params.api);
    if (user?.hiddenColumns && user.hiddenColumns.length > 0) {
        const columnsToHide = user.hiddenColumns.map(String);
        params.api.setColumnsVisible(columnsToHide, false);
    }
    setColumns(params.api.getColumns() ?? []);
  };

  // --- PROCESAMIENTO DE DATOS PARA EL GRÁFICO ---
  // `useMemo` es una optimización. Este código solo se re-ejecuta si los datos
  // de la tabla o la columna seleccionada cambian.
  const pieChartData = useMemo(() => {
    // La lógica interna ahora comprueba el estado real de la grilla en el momento del cálculo.
    if (!selectedColumn) return [];
    
    if (gridApi && gridApi.isAnyFilterPresent()) {
      const filteredData: any[] = [];
      gridApi.forEachNodeAfterFilter(node => filteredData.push(node.data));
      console.log(`[HomePage] Recalculando gráfico con ${filteredData.length} filas filtradas.`);
      return processDataForPieChart(filteredData, selectedColumn);
    }
    
    console.log(`[HomePage] Recalculando gráfico con ${rawTableData.length} filas totales.`);
    return processDataForPieChart(rawTableData, selectedColumn);
    
  }, [rawTableData, selectedColumn, gridApi, filterVersion]); // <-- La nueva dependencia clave.




  // --- Funciones de la UI (sin cambios) ---
  const handleDownloadChart = async () => {
    const element = chartRef.current;
    if (!element) {
      console.error("Error: No se encontró el elemento del gráfico.");
      return;
    }
    
    try {
      const canvas = await html2canvas(element, {
        scale: 2,
        // Es una buena práctica mantener un color de fondo explícito.
        backgroundColor: '#1f2937', 
        useCORS: true,
        // La nueva librería podría tener mejor logging.
        logging: true, 
      });

      const data = canvas.toDataURL("image/jpeg", 1.0);
      const link = document.createElement("a");
      link.href = data;
      link.download = `grafico-${selectedColumn?.name || 'data'}.jpeg`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (error) {
      console.error("Error final al generar la imagen:", error);
    }
  };


  const handleExport = () => {
    if (!gridApi) return;
    exportToExcel(gridApi, "Cepas", "cepas.xlsx");
  };
  const handleLogout = () => {
    logout();
    navigate("/login");
  };
  const handleToggle = async (colId: string, visible: boolean) => {
    if (!gridApi || !user?.id) return;

    // 1) Actualiza visibilidad en pantalla
    gridApi.setColumnsVisible([colId], visible);
    setColumns(gridApi.getColumns() ?? []);

    // 2) Obtén todas las columnas (o [] si aún es null)
    const allCols = gridApi.getColumns() ?? [];

    // 3) Filtra las ocultas y extrae su ID
    const hiddenColumns = allCols
      .filter((col) => !col.isVisible())
      .map((col) => col.getColId());

    try {
      await updateVisibleCol(user.id, hiddenColumns);
    } catch (error) {
      console.error("Error al guardar la visibilidad de las columnas:", error);
    }
  };

  return (
    <div className="flex flex-col h-full min-h-screen bg-gray-900 text-white">
      {/* Cabecera */}
      <div className="relative h-16 flex items-center mt-8 justify-center border-b border-gray-700 px-4">
        {/* 2. MODIFICAR CONTENEDOR DE BOTONES DE ADMIN */}
        <div className="absolute left-4">
          {user?.isAdmin && (
            // Contenedor relativo para posicionar el menú desplegable
            <div className="relative">
              {/* Botón que activa el menú desplegable */}
              <button onClick={() => setAdminMenuOpen((v) => !v)}>
                + Crear Nuevo
              </button>

              {/* Menú desplegable que aparece condicionalmente */}
              {adminMenuOpen && (
                <div className="absolute top-full mt-2 w-48 bg-gray-800 border border-gray-700 rounded-md shadow-lg z-10">
                  <ul className="flex flex-col p-2">
                    <li className="mb-1">
                      <Link to="/home/addatribute">
                        <button className="w-full text-left p-2 hover:bg-gray-700 rounded">
                          Nuevo Atributo
                        </button>
                      </Link>
                    </li>
                    <li className="mb-1">
                      <Link to="/home/addcepa">
                        <button className="w-full text-left p-2 hover:bg-gray-700 rounded">
                          Nueva Cepa
                        </button>
                      </Link>
                    </li>
                    <li>
                      <Link to="/home/UserManagement">
                        <button className="w-full text-left p-2 hover:bg-gray-700 rounded">
                          Nuevo Usuario
                        </button>
                      </Link>
                    </li>
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Botones en esquina superior derecha (sin cambios) */}
        <div className="absolute top-1/2 right-4 transform -translate-y-1/2 flex space-x-2">
          <button className="logout" onClick={handleLogout}>
            Cerrar Sesión
          </button>
          <button onClick={handleExport}>Exportar</button>
          <button onClick={() => setMenuOpen((v) => !v)}>
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

      {/* --- SECCIÓN DEL GRÁFICO --- */}
      <div className="p-4">
        <h2 className="text-xl font-bold mb-2">Análisis de Columna: <span className="text-blue-400">{selectedColumn?.name || 'Ninguna'}</span></h2>
        <div ref={chartRef} className="bg-gray-800 p-2 rounded-lg" style={{ height: '400px' }}>
          {selectedColumn && pieChartData.length > 0 ? (
            <MyPieChart data={pieChartData} />
          ) : (
            <div className="flex items-center justify-center h-full text-gray-400">
              <p>Seleccione una columna en la tabla para generar un gráfico.</p>
            </div>
          )}
        </div>
        <div className="flex justify-center mt-4">
            <button
                onClick={handleDownloadChart}
                disabled={!selectedColumn} // El botón se deshabilita si no hay gráfico
                className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded disabled:bg-gray-600 disabled:cursor-not-allowed"
            >
                Descargar Gráfico
            </button>
        </div>
      </div>

      {/* --- SECCIÓN DE LA TABLA --- */}
      <div className="flex-1 border-t border-gray-700 p-4 box-border">
        {/* Aquí pasamos las funciones y el estado como props a CepasTable */}
        <CepasTable
          onGridReady={handleGridReady}
          onDataLoaded={handleDataLoaded}
          onColumnSelect={handleColumnSelect}
          selectedColumn={selectedColumn}
        />
      </div>
    </div>
  );
}

export default HomePage;
