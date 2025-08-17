// src/components/CepasTable.tsx

import { AgGridReact } from "ag-grid-react";
import type {
  GridReadyEvent,
  CellValueChangedEvent,
  ICellRendererParams,
} from "ag-grid-community";
import { AllCommunityModule, ModuleRegistry } from "ag-grid-community";
import type { ColDef } from "ag-grid-community";
import { useState, useEffect, useCallback } from "react";
import { loader } from "../utils/loader";
import {
  fetchCepasFull,
  updateCepasJSONB_forTable,
} from "../services/CepasQuery";
import { useAuth } from "../stores/AuthContext";
import { actualizarCepaPorCampo } from "../utils/cepaUpdate";
import { getCepasColumnDefs } from "./CepasColumns";

ModuleRegistry.registerModules([AllCommunityModule]);

const filterRow = { id: 0 };

// Componente para el renderizador de celdas (sin cambios)
const RadioButtonCellRenderer = (
  params: ICellRendererParams & {
    onColumnSelect: (selection: { field: string; name: string }) => void;
    selectedColumn: { field: string; name: string } | null;
  }
) => {
  if (params.data && params.data.id === 0) {
    const field = params.colDef?.field;
    // Extraemos el headerName, si no existe, usamos el field como fallback.
    const name = params.colDef?.headerName || field;

    if (!field || !name) return null;

    const handleRadioClick = () => {
      params.onColumnSelect({ field, name });
    };

    return (
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          height: "100%",
        }}
      >
        <input
          type="radio"
          name="pie-chart-column-selector"
          style={{ cursor: "pointer" }}
          onChange={handleRadioClick}
          // MODIFICACIÓN: Comparamos el `field` del estado con el `field` de la columna actual.
          checked={params.selectedColumn?.field === field}
        />
      </div>
    );
  }
  return params.value ?? null;
};

export type GridReadyCallback = (params: GridReadyEvent) => void;

interface CepasTableProps {
  onGridReady?: GridReadyCallback;
  onDataLoaded: (data: any[]) => void;
  onColumnSelect: (selection: { field: string; name: string } | null) => void;
  selectedColumn: { field: string; name: string } | null;
}

export default function CepasTable({
  onGridReady,
  onDataLoaded,
  onColumnSelect,
  selectedColumn,
}: CepasTableProps) {
  // --- SECCIÓN DE HOOKS (DEBEN ESTAR AL INICIO Y EN EL NIVEL SUPERIOR) ---
  const [rowData, setRowData] = useState<any[]>([]);
  const [columnDefs, setColumnDefs] = useState<ColDef[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<Error | null>(null);
  const { user } = useAuth();
  const [notification, setNotification] = useState<{
    text: string;
    type: "success" | "error";
  } | null>(null);
  const [pinnedTopRowDataState, setPinnedTopRowDataState] = useState<any[]>([]);
  // EFECTO 1: Para obtener los datos (se ejecuta una sola vez)
  useEffect(() => {
    console.log("[CepasTable] Fetching data... (should only run once)");
    setLoading(true);
    loader(true);
    fetchCepasFull()
      .then((data) => {
        onDataLoaded(data);
        setRowData(data);
        setPinnedTopRowDataState([filterRow]);
      })
      .catch((err) => {
        setError(err);
      })
      .finally(() => {
        setLoading(false);
        loader(false);
      });
  }, [onDataLoaded]);
  // EFECTO 2: Para actualizar las columnas cuando cambia la selección
  useEffect(() => {
    // No hacer nada si aún no han llegado los datos
    if (rowData.length === 0) {
      return;
    }
    
    console.log("[CepasTable] Updating column definitions because selection changed.");
    
    // Generamos las columnas a partir de los datos existentes.
    const baseColumnDefs = getCepasColumnDefs(rowData);
    
    const enhancedColumnDefs = baseColumnDefs.map((colDef) => ({
      ...colDef,
      cellRenderer: RadioButtonCellRenderer,
      // Pasamos la selección actual para que el radio button correcto esté marcado.
      cellRendererParams: {
        onColumnSelect,
        selectedColumn,
      },
    }));

    setColumnDefs(enhancedColumnDefs);
  }, [rowData, selectedColumn, onColumnSelect]); // Depende de los datos y la selección, pero no llama al fetch.



  const handleCellValueChanged = async (params: CellValueChangedEvent) => {
    if (params.data.id === filterRow.id) return;
    if (params.oldValue === params.newValue) return;

    const updatedRow = params.data;
    const field = params.colDef.field as string;
    const rawValue = params.newValue;
    const texto =
      typeof rawValue === "string" ? rawValue.trim() : String(rawValue).trim();

    if (!texto || texto.toLowerCase() === "null") {
      setNotification({
        text: 'No se puede dejar la casilla vacía; si quieres vaciarla, escribe "N/I"',
        type: "error",
      });
      setTimeout(() => setNotification(null), 3000);
      return;
    }

    const JSONB_PREFIX = "datos_extra.";
    const isJSONBField = field.startsWith(JSONB_PREFIX);
    const jsonKey = isJSONBField ? field.slice(JSONB_PREFIX.length) : "";

    try {
      if (isJSONBField) {
        const existingDatosExtras = rowData.reduce<
          Record<string, Record<string, any>>
        >((acc, row) => {
          acc[row.nombre] = row.datos_extra ?? {};
          return acc;
        }, {});
        const merged = {
          ...existingDatosExtras[updatedRow.nombre],
          [jsonKey]: texto,
        };
        await updateCepasJSONB_forTable(
          { attribute_name: jsonKey, [updatedRow.nombre]: texto },
          existingDatosExtras
        );
        setRowData((rows) =>
          rows.map((r) =>
            r.nombre === updatedRow.nombre ? { ...r, datos_extra: merged } : r
          )
        );
      } else {
        await actualizarCepaPorCampo(updatedRow.id, field, texto);
        setRowData((rows) =>
          rows.map((r) =>
            r.id === updatedRow.id ? { ...r, [field]: texto } : r
          )
        );
      }
      setNotification({ text: "Cambios guardados con éxito", type: "success" });
    } catch (err) {
      setNotification({
        text: "Hubo un error al guardar los cambios",
        type: "error",
      });
    } finally {
      setTimeout(() => setNotification(null), 3000);
    }
  };

  // Función para determinar si una celda es editable.
  const isCellEditable = useCallback(
    (params: any) => {
      // La fila de selectores no es editable.
      if (params.data && params.data.id === filterRow.id) {
        return false;
      }
      // Solo los administradores pueden editar las demás celdas.
      return user?.isAdmin ?? false;
    },
    [user]
  );

  if (loading) return <div>Cargando cepas...</div>;
  if (error) return <div>Error al cargar datos: {error.message}</div>;

  return (
    <>
      {notification && (
        <div className={`absolute top-4 left-1/2 -translate-x-1/2 z-10 ...`}>
          {notification.text}
        </div>
      )}
      <div className="relative h-full">
        <div className="ag-theme-alpine custom-space">
          <AgGridReact
            columnDefs={columnDefs}
            rowData={rowData}
            theme="legacy"
            pinnedTopRowData={pinnedTopRowDataState}
            enableRowPinning={false}
            onGridReady={onGridReady}
            onCellValueChanged={handleCellValueChanged}
            defaultColDef={{
              minWidth: 100,
              filter: true,
              sortable: true,
              editable: isCellEditable,
              resizable: true,
              wrapHeaderText: true,
            }}
            rowHeight={50}
            pagination
            paginationPageSize={20}
            paginationPageSizeSelector={[20, 50, 70, 100]}
            domLayout="autoHeight"
          />
        </div>
      </div>
    </>
  );
}
