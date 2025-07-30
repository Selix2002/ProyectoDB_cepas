import { Link } from "react-router-dom";
import { useRef } from "react"; // 1. Importar useRef
import UserTable, { type UserTableHandles } from '../components/UserTable'; // 2. Importar el tipo

export default function UserPage() {
  // 3. Crear la ref para el componente UserTable
  const userTableRef = useRef<UserTableHandles>(null);

  // 4. Crear la función que llama al método expuesto por la ref
  const handleAddUser = () => {
    userTableRef.current?.onAddUser();
  };

  return (
    <div className="flex flex-col h-full min-h-screen bg-gray-900 text-white">
      {/* HEADER */}
      <div className="flex-none shadow p-6 relative bg-gray-900 flex justify-start items-center">
        {/* BOTONES A LA IZQUIERDA */}
        <div className="flex items-center gap-4">
          <Link to="/home">
            <button className="text-white hover:bg-gray-700 p-2 rounded">
              ← Volver
            </button>
          </Link>

          {/* 5. Botón para añadir usuario */}
          <button
            onClick={handleAddUser}
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >
            + Añadir Usuario
          </button>
        </div>

        {/* TÍTULO CENTRADO (usando posicionamiento absoluto) */}
        <h1 className="absolute left-1/2 -translate-x-1/2 text-4xl font-bold">
          Gestión de Usuarios
        </h1>
      </div>

      {/* CONTENIDO: tabla / ag-Grid */}
      <div className="flex-1 border-t border-gray-700 p-4 box-border">
        {/* 6. Pasar la ref al componente hijo */}
        <UserTable ref={userTableRef} />
      </div>
    </div>
  );
}
