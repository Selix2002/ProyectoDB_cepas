import React, { useState, useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import { fetchCepasFull, updateCepasJSONB } from "../services/CepasQuery";
import ModalConfirmation from "../components/ModalConfirmation";
import { loader } from '../utils/loader';


export default function NewAttributePage() {
  const [cepas, setCepas] = useState<{ id: number; nombre: string }[]>([]);
  const inputRefs = useRef<Array<HTMLInputElement | null>>([]);
  const [fileDict, setFileDict] = useState<Record<string, string>>({});
  const [showModal, setShowModal] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    loader(true);
    fetchCepasFull()
      .then((data) => setCepas(data))
      .catch((error) => console.error("Error cargando cepas:", error));
    loader(false);
  }, []);

  // Generar y descargar plantilla
  const handleDownloadTemplate = () => {
    const lines = ["attribute_name="];
    cepas.forEach((cepa) => lines.push(`${cepa.nombre}=`));
    const blob = new Blob([lines.join("\n")], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "template_addAttribute.txt";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  // Procesar archivo .txt
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (evt) => {
      try {
        const text = evt.target?.result;
        if (typeof text !== "string") throw new Error("Archivo vacío o formato inválido");
        const lines = text.split(/\r?\n/);
        const dict: Record<string, string> = {};
        lines.forEach((line, idx) => {
          if (!line.trim()) return;
          if (!line.includes("=")) {
            throw new Error(`Formato inválido en línea ${idx + 1}: falta '='`);
          }
          const [rawKey, ...rest] = line.split("=");
          const key = rawKey.trim();
          const valueRaw = rest.join("=").trim();
          dict[key] = valueRaw === "" ? "N/I" : valueRaw;
        });
        const expectedKeys = ["attribute_name", ...cepas.map((c) => c.nombre)];
        const missing = expectedKeys.filter((k) => !(k in dict));
        if (missing.length > 0) throw new Error(`Faltan las siguientes claves: ${missing.join(", ")}`);
        const extra = Object.keys(dict).filter((k) => !expectedKeys.includes(k));
        if (extra.length > 0) throw new Error(`Claves no esperadas: ${extra.join(", ")}`);
        if (!dict["attribute_name"] || dict["attribute_name"] === "N/I") {
          throw new Error('Debe ingresar un valor válido para "attribute_name"');
        }
        setFileDict(dict);
        setShowModal(true);
      } catch (err: any) {
        const msg = err instanceof Error ? err.message : "Error al procesar el archivo";
        alert(`Error al procesar el archivo: ${msg}`);
        console.error(msg);
      }
    };
    reader.readAsText(file);
    e.target.value = "";
  };

  // Mover focus con Enter
  const handleKeyDown = (
    e: React.KeyboardEvent<HTMLInputElement>,
    index: number
  ) => {
    if (e.key === "Enter") {
      e.preventDefault();
      const nextInput = inputRefs.current[index + 1];
      if (nextInput) nextInput.focus();
    }
  };

  // Confirmación: SI y NO (modal y flujo inputs)
  const handleConfirmYes = async (dictToSave?: Record<string, string>) => {
    const dict = dictToSave ?? fileDict;
    try {
      loader(true);
      await updateCepasJSONB(dict);
      alert("¡Atributos añadidos con éxito!");
      setFileDict({});
      setShowModal(false);
      loader(false);
      inputRefs.current.forEach((el) => { if (el) el.value = ""; });
    } catch (err: any) {
      console.error(err);
      alert(`Error al actualizar la base de datos: ${err.response?.data?.detail ?? err.message}`);
    }
  };

  // Construye dict desde inputs y llama a handleConfirmYes
  const handleAddAttribute = () => {
    const dict: Record<string, string> = {};
    const attributeName = inputRefs.current[0]?.value.trim();
    if (!attributeName) {
      alert('Debe ingresar un valor para "Nombre del atributo".');
      return;
    }
    dict["attribute_name"] = attributeName;
    cepas.forEach((cepa, idx) => {
      const val = inputRefs.current[idx + 1]?.value.trim();
      dict[cepa.nombre] = val && val !== "" ? val : "N/I";
    });
    handleConfirmYes(dict);
  };

  const handleConfirmNo = () => {
    setShowModal(false);
  };

  return (
    <div className="min-h-screen bg-[#213547]">
      {/* Header fijo con botón de volver */}
      <header className="fixed top-0 left-0 w-full bg-[#213547] p-8 z-10">
        <div className="absolute top-4 left-4">
          <Link to="/home">
            <button className="bg-gray-500 hover:bg-gray-600 text-white font-semibold py-2 px-4 rounded">
              ← Volver
            </button>
          </Link>
        </div>
        <div className="absolute top-4 right-4 flex space-x-2">
          <button onClick={handleDownloadTemplate} className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded">
            Descargar plantilla
          </button>
          <button onClick={() => fileInputRef.current?.click()} className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded">
            Subir archivo
          </button>
          <input type="file" accept=".txt" ref={fileInputRef} onChange={handleFileChange} style={{ display: "none" }} />
        </div>
      </header>

      {/* Formulario principal */}
      <main className="pt-32 p-8">
        <h1 className="text-2xl text-center font-bold text-white mb-6">Añadir Nuevo Atributo</h1>
        <div className="max-w-md mx-auto bg-white p-6 rounded-lg shadow-lg max-h-[70vh] overflow-y-auto">
          <div className="mb-4">
            <input
              ref={(el) => { inputRefs.current[0] = el; }}
              onKeyDown={(e) => handleKeyDown(e, 0)}
              type="text"
              name="attribute_name"
              placeholder="Nombre del atributo"
              className="w-full p-2 border border-gray-300 rounded text-black"
            />
          </div>
          {cepas.map((cepa, idx) => (
            <div className="mb-4" key={cepa.id}>
              <input
                ref={(el) => { inputRefs.current[idx + 1] = el; }}
                onKeyDown={(e) => handleKeyDown(e, idx + 1)}
                type="text"
                name={cepa.nombre}
                placeholder={cepa.nombre}
                className="w-full p-2 border border-gray-300 rounded text-black"
              />
            </div>
          ))}
          <div className="flex justify-end mt-6">
            <button onClick={handleAddAttribute} className="bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded">
              Añadir atributo
            </button>
          </div>
        </div>

        {/* Modal de confirmación */}
        <ModalConfirmation
          visible={showModal}
          data={fileDict}
          onConfirm={() => handleConfirmYes()}
          onCancel={handleConfirmNo}
        />
      </main>
    </div>
  );
}