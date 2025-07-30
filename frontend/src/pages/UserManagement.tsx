import { Link } from "react-router-dom";
import UserTable from '../components/UserTable';

export default function UserPage() {
  return (
    // Se eliminaron las clases de flexbox y altura para evitar conflictos con AG Grid.
    <div className="border rounded-lg m-4">
      {/* HEADER */}
      <div className="bg-white shadow p-6 relative">
        {/* BOTÓN VOLVER */}
        <Link to="/home">
          <button className="text-black bg-gray-200 hover:bg-gray-300 py-2 px-4 rounded">
            ← Volver
          </button>
        </Link>
        {/* TÍTULO CENTRADO */}
        <h1 className="text-4xl font-bold text-center absolute inset-0 pt-6">
          Gestión de Usuarios
        </h1>
      </div>

      {/* CONTENIDO: tabla / ag-Grid */}
      {/* Se eliminó el div contenedor intermedio */}
      <UserTable />
    </div>
  );
}
