// src/pages/HomePage.tsx
import { useState } from 'react'
import DropdownMenu from '../components/DropdownMenu'
import CepasTable from '../components/CepasTable'
import type { GridReadyCallback } from '../components/CepasTable'
import type { GridApi, Column } from 'ag-grid-community'
import { SlidersHorizontal, FlaskConical, MoreVertical } from 'lucide-react'

export function HomePage() {
  const [menuOpen, setMenuOpen] = useState(false)
  const [columns, setColumns] = useState<Column[]>([])
  const [gridApi, setGridApi] = useState<GridApi>()

  // 1) Capturamos el GridApi y la lista inicial de Column[]  
  const handleGridReady: GridReadyCallback = params => {
    const api = params.api
    setGridApi(api)
    // usamos api.getColumns() para obtener las Column objects :contentReference[oaicite:0]{index=0}
    setColumns(api.getColumns() ?? [])
  }

  // 2) Al hacer toggle, llamamos a gridApi.setColumnsVisible(...) y luego
  //    volvemos a leer api.getColumns() para actualizar el estado de los checkboxes
  const handleToggle = (colId: string, visible: boolean) => {
    if (!gridApi) return
    // setColumnsVisible toma un array de IDs y el booleano deseado
    gridApi.setColumnsVisible([colId], visible)
    setColumns(gridApi.getColumns() ?? [])
  }

  return (
    <div className="flex flex-col min-h-screen bg-gray-900 text-white">
      {/* Cabecera */}
      <div className="relative h-16 flex items-center justify-center border-b border-gray-700 px-4">
        <button className="absolute left-4 bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded">
          + Añadir Cepa
        </button>
        <button
          className="absolute right-4 p-2 rounded hover:bg-gray-700"
          onClick={() => setMenuOpen(v => !v)}
        >
          <MoreVertical className="h-6 w-6 text-white" />
        </button>

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
            <span className="text-4xl font-bold leading-tight">
              N° ATRIBUTOS
            </span>
            <span className="text-sm text-gray-400">
              Registrados
            </span>
          </div>
        </div>

        {/* Total Cepas */}
        <div className="flex items-center space-x-4 bg-gray-800 rounded-lg p-10">
          <div className="bg-green-500 p-3 rounded-full">
            <FlaskConical className="h-6 w-6 text-white" />
          </div>
          <div className="flex flex-col">
            <span className="text-sm font-semibold text-green-400 uppercase">
              Total cepas
            </span>
            <span className="text-4xl font-bold leading-tight">
              N° DE CEPAS
            </span>
            <span className="text-sm text-gray-400">
              Registradas
            </span>
          </div>
        </div>
      </div>

      {/* Tabla de Cepas */}
      <div className="flex-1 border-t border-gray-700 p-4 box-border">
        <CepasTable onGridReady={handleGridReady} />
      </div>
    </div>
  )
}

export default HomePage




