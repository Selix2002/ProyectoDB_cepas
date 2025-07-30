import { Link } from "react-router-dom"
import UserTable from '../components/UserTable';
export default function UserPage() {
  return (
    <div className="h-screen flex flex-col border rounded-lg m-4 overflow-hidden">
      {/* HEADER */}
      <div className="flex-none bg-white shadow p-6 relative">
        {/* BOTÓN VOLVER */}
        <Link to="/home">
        <button className="text-white">
          ← Volver
        </button>
        </Link>
        {/* TÍTULO CENTRADO */}
        <h1 className="text-4xl font-bold text-center">
          Gestión de Usuarios
        </h1>
      </div>

      {/* CONTENIDO: tabla / ag-Grid */}
      <div className="flex-1 border-t border-gray-700 p-4 box-border">
        <div className="w-full h-full border-dashed border-2 border-gray-200 flex items-center justify-center">
        <UserTable />
        </div>
      </div>
    </div>
  );
}
