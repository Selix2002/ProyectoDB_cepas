// src/components/CepasTable.tsx

import { AgGridReact } from "ag-grid-react";
import type { GridReadyEvent, CellValueChangedEvent } from "ag-grid-community";
import { AllCommunityModule, ModuleRegistry } from "ag-grid-community";
import { useState, useEffect, useMemo } from "react";
import { fetchCepasFull } from "../services/CepasQuery";
import { actualizarCepaPorCampo } from "../utils/cepaUpdate";
import { cepasColumnDefs } from "./CepasColumns";

ModuleRegistry.registerModules([AllCommunityModule]);

export type GridReadyCallback = (params: GridReadyEvent) => void;

interface CepasTableProps {
  onGridReady?: GridReadyCallback;
}

export default function CepasTable({ onGridReady }: CepasTableProps) {
  const [rowData, setRowData] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<Error | null>(null);

  const paginationPageSizeSelector = useMemo(() => [10, 20, 50, 70, 100], []);

  // Estado para controlar la notificación (texto y tipo)
  const [notification, setNotification] = useState<{
    text: string;
    type: "success" | "error";
  } | null>(null);

  // 1) Carga inicial de datos
  useEffect(() => {
    setLoading(true);
    fetchCepasFull()
      .then((data) => {
        setRowData(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err as Error);
        setLoading(false);
      });
  }, []);

  // 2) Handler que dispara cuando el usuario termina de editar una celda
  const handleCellValueChanged = async (params: CellValueChangedEvent) => {
    // 2.1) Si no hubo cambio real, no hacemos nada
    if (params.oldValue === params.newValue) return;

    const updatedRow = params.data;
    const changedField = params.colDef.field as string;
    const newValue = params.newValue;

    // 2.2) Si el usuario dejó la casilla vacía ("" o solo espacios), mostramos error y NO llamamos al backend
    const texto = typeof newValue === "string" ? newValue.trim() : String(newValue).trim();
    console.log(texto);
    console.log(typeof texto);
    if (texto == "" || texto == null || texto == "null") {
      setNotification({
        text: 'No se puede dejar la casilla vacía, si desea dejarla vacía, escribir "N/I"',
        type: "error",
      });
     
      setTimeout(() => setNotification(null), 3000);
      return; // Salimos sin llamar a actualizarCepaPorCampo
    }

    try {
      // 2.3) Si pasa el chequeo, llamamos al util que arma el payload y hace el update
      await actualizarCepaPorCampo(updatedRow.id, changedField, newValue);

      setNotification({
        text: "Cambios guardados con éxito!",
        type: "success",
      });
    } catch (err) {
      console.error("Error al actualizar en backend:", err);
      setNotification({
        text: "Hubo un error al guardar los cambios",
        type: "error",
      });
    }

    // 2.4) Limpiar la notificación tras 3 segundos
    setTimeout(() => setNotification(null), 3000);
  };

  if (loading) return <div>Cargando cepas...</div>;
  if (error) return <div>Error al cargar datos: {error.message}</div>;

  return (
    <>
      {/* Notificación */}
      {notification && (
        <div
          className={`mb-2 px-4 py-2 rounded text-center ${
            notification.type === "success"
              ? "bg-blue-600 text-white"
              : "bg-red-600 text-white"
          }`}
        >
          {notification.text}
        </div>
      )}

      <div style={{ width: "100%", overflowX: "auto" }}>
        <div
          className="ag-theme-alpine custom-space"
          style={{ width: "100%", minWidth: "1000px" }}
        >
          <AgGridReact
            columnDefs={cepasColumnDefs}
            rowData={rowData}
            onGridReady={onGridReady}
            onCellValueChanged={handleCellValueChanged}
            defaultColDef={{
              minWidth: 100,
              filter: true,
              sortable: true,
              editable: true,
              resizable: true,
              wrapHeaderText: true,
            }}
            pagination
            paginationPageSize={10}
            paginationPageSizeSelector={paginationPageSizeSelector}
            domLayout="autoHeight"
          />
        </div>
      </div>
    </>
  );
}
