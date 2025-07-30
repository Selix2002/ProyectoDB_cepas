import { Link } from "react-router-dom"
import UserTable from '../components/UserTable';
export default function UserPage() {
  return (
    <div className="flex flex-col h-full min-h-screen">
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
      <div className="border-dashed border-2 border-gray-200 bg-white p-4">
            <UserTable />
      </div>
    </div>
  );
}
