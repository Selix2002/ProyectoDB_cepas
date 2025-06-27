// src/components/CepasTable.tsx

import { AgGridReact } from "ag-grid-react";
import type { GridReadyEvent, CellValueChangedEvent } from "ag-grid-community";
import { AllCommunityModule, ModuleRegistry } from "ag-grid-community";
import type { ColDef } from "ag-grid-community";
import { useState, useEffect, useMemo } from "react";
import {
  fetchCepasFull,
  updateCepasJSONB_forTable,
} from "../services/CepasQuery";
import { actualizarCepaPorCampo } from "../utils/cepaUpdate";
import { getCepasColumnDefs } from "./CepasColumns";

ModuleRegistry.registerModules([AllCommunityModule]);

export type GridReadyCallback = (params: GridReadyEvent) => void;

interface CepasTableProps {
  onGridReady?: GridReadyCallback;
}

export default function CepasTable({ onGridReady }: CepasTableProps) {
  const [rowData, setRowData] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<Error | null>(null);
  const [columnDefs, setColumnDefs] = useState<ColDef[]>([]);

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
        setColumnDefs(getCepasColumnDefs(data));
      })
      .catch((err) => {
        console.error("Error al cargar cepas:", err);
        setError(err);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  // 2) Handler que dispara cuando el usuario termina de editar una celda

  const handleCellValueChanged = async (params: CellValueChangedEvent) => {
    // 1) Si no hubo cambio, salimos
    if (params.oldValue === params.newValue) return;

    const updatedRow = params.data;
    const field = params.colDef.field as string;
    const rawValue = params.newValue;
    const texto =
      typeof rawValue === "string" ? rawValue.trim() : String(rawValue).trim();

    // 2) Validación de texto
    if (!texto || texto.toLowerCase() === "null") {
      setNotification({
        text: 'No se puede dejar la casilla vacía; si quieres vaciarla, escribe "N/I"',
        type: "error",
      });
      setTimeout(() => setNotification(null), 3000);
      return;
    }

    // 3) ¿Es JSONB? detectamos prefijo
    const JSONB_PREFIX = "datos_extra.";
    const isJSONBField = field.startsWith(JSONB_PREFIX);
    // extraemos la clave real (ej: "EL XD")
    const jsonKey = isJSONBField ? field.slice(JSONB_PREFIX.length) : "";

    try {
      console.log("isJSONBField:", isJSONBField);
      if (isJSONBField) {
        // ————— Rama JSONB —————
        // 3.1) Recolectar los datos_extra actuales de todas las filas
        const existingDatosExtras = rowData.reduce<
          Record<string, Record<string, any>>
        >((acc, row) => {
          acc[row.nombre] = row.datos_extra ?? {};
          return acc;
        }, {});

        // 3.2) Mergeamos sólo la clave modificada
        const merged = {
          ...existingDatosExtras[updatedRow.nombre],
          [jsonKey]: texto,
        };

        // 3.3) Console.log para inspeccionar payload
        console.log("🛠️ JSONB PATCH >>", {
          cepa: updatedRow.nombre,
          datos_extra: merged,
        });

        // 3.4) Enviamos al endpoint JSONB
        await updateCepasJSONB_forTable(
          { attribute_name: jsonKey, [updatedRow.nombre]: texto },
          existingDatosExtras
        );

        // 3.5) Reflejamos localmente
        setRowData((rows) =>
          rows.map((r) =>
            r.nombre === updatedRow.nombre ? { ...r, datos_extra: merged } : r
          )
        );
      } else {
        // ————— Rama campo normal —————
        const simplePayload = { [field]: texto };

        console.log("🔧 SIMPLE PATCH >>", {
          id: updatedRow.id,
          ...simplePayload,
        });

        await actualizarCepaPorCampo(updatedRow.id, field, texto);

        // Actualizamos localmente ese campo
        setRowData((rows) =>
          rows.map((r) =>
            r.id === updatedRow.id ? { ...r, [field]: texto } : r
          )
        );
      }

      setNotification({ text: "Cambios guardados con éxito", type: "success" });
    } catch (err) {
      console.error("Error al actualizar:", err);
      setNotification({
        text: "Hubo un error al guardar los cambios",
        type: "error",
      });
    } finally {
      setTimeout(() => setNotification(null), 3000);
    }
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

      {/* Contenedor con scroll horizontal y barra de progreso */}
      <div
        className="relative h-full"
      >
        <div
          className="ag-theme-alpine custom-space h-full" 
        >
          <AgGridReact
            columnDefs={columnDefs}
            rowData={rowData}
            scrollbarWidth={16}
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

