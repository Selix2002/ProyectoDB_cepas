// src/pages/NewCepaPage.tsx
import { useState } from 'react';

export function NewCepaPage() {
  const [nombre, setNombre] = useState('');
  const [codLab, setCodLab] = useState('');
  // aquí puedes agregar más campos según tu modelo Cepa

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Acá iría la lógica para llamar a tu API y crear la cepa,
    // por ejemplo usando fetch o axios a POST /cepas/create
    console.log({ nombre, codLab });
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold mb-4">Añadir Nueva Cepa</h1>
      <form onSubmit={handleSubmit} className="max-w-md space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1" htmlFor="nombre">
            Nombre de la cepa
          </label>
          <input
            id="nombre"
            type="text"
            value={nombre}
            onChange={(e) => setNombre(e.target.value)}
            className="w-full border border-gray-300 rounded px-2 py-1"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1" htmlFor="codLab">
            Código de laboratorio
          </label>
          <input
            id="codLab"
            type="text"
            value={codLab}
            onChange={(e) => setCodLab(e.target.value)}
            className="w-full border border-gray-300 rounded px-2 py-1"
          />
        </div>
        {/* Agrega aquí más inputs según los campos que necesites */}
        <button
          type="submit"
          className="mt-4 bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
        >
          Crear Cepa
        </button>
      </form>
    </div>
  );
}

export default NewCepaPage;
