// src/components/UserTable.tsx
import { useState, useEffect } from "react";
import { AgGridReact } from "ag-grid-react";
import {loader} from '../utils/loader';
import type {
  GridApi,
  GridReadyEvent,
  CellValueChangedEvent,
  ICellRendererParams,
  GetRowIdParams,
} from "ag-grid-community";
import {
  getUsers,
  updateUser,
  deleteUser,
} from "../services/UsersQuery";
import type { User, UserCreate } from "../interfaces/index";
import { useAuth } from "../stores/AuthContext";
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';


type RowUser = User & Partial<UserCreate>;

export default function UserTable() {
  const { user: currentUser } = useAuth();
  const [gridApi, setGridApi] = useState<GridApi | null>(null);
  const [rowData, setRowData] = useState<RowUser[]>([]);

  useEffect(() => {
    if (gridApi) loadUsers();
  }, [gridApi]);

  const loadUsers = async () => {
    try {
      loader(true);
      setRowData(await getUsers());
      loader(false);
    } catch (err) {
      console.error("Error cargando usuarios:", err);
    }
  };

  const onGridReady = (params: GridReadyEvent) => {
    setGridApi(params.api);
  };



  const onCellValueChanged = async (event: CellValueChangedEvent) => {
    const user = event.data as RowUser;
    const field = event.colDef.field;

    // 1) Prohibir editar al propio usuario
    if (user.id === currentUser?.id) return;

    try {
      if (user.id && (field === "username" || field === "isAdmin")) {
        await updateUser(user.id, user.username, user.isAdmin);
      }
    } catch (err) {
      console.error("Error guardando cambio de celda:", err);
    }
  };

  const onDeleteUser = async (user: RowUser) => {
    // 2) Prohibir eliminar al propio usuario
    if (user.id === currentUser?.id) return;
    if (!window.confirm(`¿Eliminar al usuario “${user.username}”?`)) return;
    try {
      loader(true);
      await deleteUser(user.id);
      loader(false);
      await loadUsers();
      gridApi?.applyTransaction({ remove: [user] });
    } catch (err) {
      console.error("Error eliminando usuario:", err);
    }
  };

  const columnDefs = [
    { 
      field: "id", 
      headerName: "ID", 
      editable: false, 
      width: 80,
      sort: "asc",
    },
    {
      field: "username",
      headerName: "Usuario",
      flex: 1,
      editable: (params: { data: { id: number | undefined } }) =>
        params.data.id !== currentUser?.id,
        },
    {
      field: "isAdmin",
      headerName: "Administrador",
      editable: (params: { data: { id: number | undefined } }) =>
        params.data.id !== currentUser?.id,
      cellEditor: "agSelectCellEditor",
      cellEditorParams: { values: [true, false] },
      valueFormatter: (p: { value: boolean }) => (p.value ? "Sí" : "No"),
      cellStyle: { display: "flex", justifyContent: "center" },
    },
    {
      headerName: "Eliminar Usuario",
      cellRenderer: (params: ICellRendererParams<RowUser>) => {
        if (params.data?.id === currentUser?.id) {
          return (
            <button
              disabled
              title="No puedes eliminarte a ti mismo"
              className="drop opacity-50 cursor-not-allowed"
            >
              🚫
            </button>
          );
        }
        return (
          <button
            onClick={() => params.data && onDeleteUser(params.data)}
            title="Eliminar usuario"
            className="drop"
          >
            🗑️
          </button>
        );
      },
      suppressHeaderMenuButton: true,
      sortable: false,
      filter: false,
      cellStyle: {
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      },
    },
  ];

  const defaultColDef = { sortable: true, filter: true,minWidth: 100 };

  return (
      <div className="ag-theme-alpine custom-space h-full">
        <AgGridReact
          rowData={rowData}
          columnDefs={columnDefs}
          defaultColDef={defaultColDef}
          domLayout="autoHeight"
          theme="legacy"
          onGridReady={onGridReady}
          onCellValueChanged={onCellValueChanged}
          getRowId={(params: GetRowIdParams<RowUser>) =>
            params.data.id.toString()
          }
          scrollbarWidth={16}
        />
      </div>
  );
}
