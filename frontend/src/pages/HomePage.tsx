// src/pages/HomePage.tsx
import { useState } from "react";
import DropdownMenu from "../components/DropdownMenu";
import CepasTable from "../components/CepasTable";
import type { GridReadyCallback } from "../components/CepasTable";
import type { GridApi, Column } from "ag-grid-community";
import { MoreVertical } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import { exportToExcel } from "../utils/exportExcel";
import { useAuth } from "../stores/AuthContext";
import { updateVisibleCol } from "../services/UsersQuery";


export function HomePage() {
  const [menuOpen, setMenuOpen] = useState(false);
  // 1. AÑADIR NUEVO ESTADO PARA EL MENÚ DE ADMIN
  const [adminMenuOpen, setAdminMenuOpen] = useState(false);
  const [columns, setColumns] = useState<Column[]>([]);
  const [gridApi, setGridApi] = useState<GridApi>();
  const { logout, user } = useAuth();
  const navigate = useNavigate();

  const handleGridReady: GridReadyCallback = (params) => {
    const api = params.api;
    setGridApi(api);

    // Si el usuario y sus preferencias existen, las aplicamos
    if (user?.hiddenColumns && user.hiddenColumns.length > 0) {
      // Los IDs de columna en AG-Grid suelen ser strings, los convertimos
      const columnsToHide = user.hiddenColumns.map(String);
      api.setColumnsVisible(columnsToHide, false);
    }

    // Actualizamos el estado local de las columnas para el DropdownMenu
    setColumns(api.getColumns() ?? []);
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
      .filter(col => !col.isVisible())
      .map(col => col.getColId());
  
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

      {/* Tabla de Cepas */}
      <div className="flex-1 border-t border-gray-700 p-4 box-border">
        <CepasTable onGridReady={handleGridReady} />
      </div>
    </div>
  );
}

export default HomePage;