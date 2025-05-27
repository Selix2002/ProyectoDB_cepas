// src/pages/HomePage.tsx
//import { useQuery } from "@tanstack/react-query";
//import { getCepsas, type Cepa } from "../services/cepas";
//import { CepsasTable } from "../components/CepasTable";

// src/pages/HomePage.tsx
//import React from 'react';


export function HomePage() {
  return (
    <div className="flex flex-col h-screen m-0 p-0 box-border">
      {/* Cabecera */}
      <div className="div-head flex-none h-16 min-h-0 border flex items-center justify-center px-4 relative">
        <div className="div-title absolute left-4 border rounded px-4 py-2">
          DIV_TITLE
        </div>
        <span className="text-xl font-medium">DIV_HEAD</span>
        <div className="div-button absolute right-4 border rounded px-4 py-2">
          DIV_AddCepa
        </div>
      </div>

      {/* Sección general */}
      <div className="div-general basis-0 grow-[2] min-h-0 border p-4 box-border flex items-center justify-center overflow-auto">
        <div className="flex w-full h-full space-x-4">
          <div className="flex-1 border rounded p-4 flex items-center justify-center">
            DIV_TotalCepas
          </div>
          <div className="flex-1 border rounded p-4 flex items-center justify-center">
            DIV_TotalAtrib
          </div>
        </div>
      </div>

      {/* Búsqueda */}
      <div className="div-busqueda flex-none h-16 min-h-0 border flex items-center justify-center overflow-hidden px-4">
        DIV_BUSQUEDA
      </div>

      {/* Filtros */}
      <div className="div-filtros flex-auto border p-4 box-border flex flex-col overflow-auto">        {/* Título */}
        <div className="div-filtros-title border rounded px-4 py-2 w-full max-w-lg mb-4">
          TITLE
        </div>
        {/* Contenedores de filtros */}
        <div className="flex flex-1 w-full space-x-4 mb-4">
          <div className="flex-1 border rounded p-4 flex items-center justify-center" >
            DIV_FILTROS
          </div>
          <div className="flex-1 border rounded p-4 flex items-center justify-center">
            DIV_AddFiltros
          </div>
        </div>
        {/* Botón de aplicar */}
        <div className="div-apply-filtros border rounded px-4 py-2 self-start">
          DIV_ApplyFiltros
        </div>
      </div>

      {/* Tabla */}
      <div className="div-tabla flex-none h-64 border p-4 box-border flex items-center justify-center overflow-auto">        DIV_TABLA
      </div>
    </div>
  );
}
