// src/pages/HomePage.tsx
import React, { useState } from 'react'
import DropdownMenu from '../components/DropdownMenu'
import CepasTable from '../components/CepasTable'
import { SlidersHorizontal, FlaskConical, MoreVertical } from 'lucide-react'

export function HomePage() {
  const [menuOpen, setMenuOpen] = useState(false)
  return (
    <div className="flex flex-col min-h-screen m-0 p-0 box-border bg-gray-900 text-white">
      {/* Cabecera */}
      <div className="relative flex-none h-16 flex items-center justify-center px-4 border-b border-gray-700">
        {/* Botón Añadir Cepa en esquina superior izquierda */}
        <button className="absolute left-4 bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded">
          + Añadir Cepa
        </button>
        {/* Botón menú desplegable en esquina superior derecha */}
        <button
          className="absolute right-4 p-2 rounded hover:bg-gray-700"
          onClick={() => setMenuOpen(!menuOpen)}
        >
          <MoreVertical className="h-6 w-6 text-white" />
        </button>

        <DropdownMenu
          isOpen={menuOpen}
          onClose={() => setMenuOpen(false)}
        />
        {/* Título centrado */}
        <span className="text-xl font-medium">Dashboard para Gestión de Cepas Bacterianas</span>
      </div>

      {/* Estadísticas */}
      <div className="p-15 flex flex-wrap items-center gap-4">
        {/* Atributos Definidos: empuja todo lo demás a la derecha */}
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

        {/* Total Cepas: alineada a la derecha */}
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
        <CepasTable />
      </div>
    </div>
  )
}

export default HomePage
