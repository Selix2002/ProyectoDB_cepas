// src/pages/NewCepaPage.tsx
import React, { useState, useEffect, useRef } from "react";
import { createCepa, fetchCepasFull } from "../services/CepasQuery";
import ModalConfirmation from "../components/ModalConfirmation";
import { getCepasColumnDefs } from "../components/CepasColumns";
import type { ColDef } from "ag-grid-community";
import { Link } from "react-router-dom";



export default function NewCepaPage() {
  const [columns, setColumns] = useState<ColDef[]>([]);
  const [formData, setFormData] = useState<Record<string, string>>({});
  const [fileData, setFileData] = useState<Record<string, string>>({});
  const [showModal, setShowModal] = useState(false);
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const inputRefs = useRef<Array<HTMLInputElement | null>>([]);

  useEffect(() => {
    fetchCepasFull()
      .then((data) => {
        const defs = getCepasColumnDefs(data);
        setColumns(defs);
        const initial: Record<string, string> = {};
        defs
          .filter(
            (col): col is ColDef & { field: string } =>
              typeof col.field === "string" && col.field !== "id"
          )
          .forEach((col) => {
            initial[col.field] = "";
          });
        setFormData(initial);
      })
      .catch((error) => console.error("Error cargando cepas:", error));
  }, []);

  const handleInputChange = (field: string, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleDownloadTemplate = () => {
    const contenido = columns
      .filter(
        (col): col is ColDef & { field: string } =>
          typeof col.field === "string" && col.field !== "id"
      )
      .map((col) => {
        const field = col.headerName;
        return `${field}=`;
      })
      .join("\n");
    const blob = new Blob([contenido], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "plantilla_cepa.txt";
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (ev) => {
      const text = ev.target?.result as string;

      // 1) Definimos las claves esperadas y cuántas líneas procesar
      const expectedKeys = columns
        .filter(
          (col): col is ColDef & { field: string } =>
            typeof col.field === "string" && col.field !== "id"
        )
        .map((col) => col.headerName!);
      const maxLines = expectedKeys.length;

      // 2) Leemos solo hasta maxLines líneas
      const rawLines = text.split("\n").slice(0, maxLines);

      // 3) Extraemos las claves sin validar aún el "="
      const rawKeys = rawLines.map((line) =>
        line.includes("=") ? line.split("=")[0].trim() : line.trim()
      );

      // 4) Comprobamos si faltan claves en el archivo
      const missingKeys = expectedKeys.filter((k) => !rawKeys.includes(k));
      if (missingKeys.length > 0) {
        alert(
          `Faltan las siguientes claves en la plantilla: ${missingKeys.join(
            ", "
          )}`
        );
        return;
      }

      // 5) Ahora validamos línea a línea la presencia de "=" y parseamos
      const parsed: Record<string, string> = {};
      for (let i = 0; i < rawLines.length; i++) {
        const line = rawLines[i];
        if (!line.includes("=")) {
          alert(`Formato inválido en línea ${i + 1}: falta el carácter '='`);
          return;
        }
        //NO USAR '=' EN LOS VALORES O CLAVES. SE ROMPE EL PARSEO
        const [rawKey, ...rest] = line.split("=");
        const key = rawKey.trim();
        const value = rest.join("=").trim();

        if (!key) {
          alert(`Clave vacía en línea ${i + 1}`);
          return;
        }
        parsed[key] = value;
      }

      // 6) “Cepa” no puede quedar vacía
      if (!parsed["Cepa"]?.trim()) {
        alert('El valor de la clave "Cepa" no puede estar en blanco');
        return;
      }

      // 7) Rellenar con "N/I" las demás claves vacías
      Object.keys(parsed).forEach((key) => {
        if (key !== "Cepa" && !parsed[key].trim()) {
          parsed[key] = "N/I";
        }
      });

      // 8) Actualizamos estado y mostramos modal de confirmación
      setFormData((prev) => ({ ...prev, ...parsed }));
      setFileData(parsed);
      setShowModal(true);
    };

    reader.readAsText(file);
    e.target.value = "";
  };

  // Handler para el botón "Añadir Cepa"
  const handleAddCepa = (): void => {
    const relations = [
      "almacenamiento",
      "medio_cultivo",
      "morfologia",
      "actividad_enzimatica",
      "crecimiento_temperatura",
      "resistencia_antibiotica",
      "caracterizacion_genetica",
      "proyecto",
    ];

    const payload: Record<string, any> = {
      nombre: null,
      cod_lab: null,
      origen: null,
      pigmentacion: null,
      almacenamiento: {},
      medio_cultivo: {},
      morfologia: {},
      actividad_enzimatica: {},
      crecimiento_temperatura: {},
      resistencia_antibiotica: {},
      caracterizacion_genetica: {},
      proyecto: {},
      datos_extra: {},
    };

    for (const [fieldPath, rawValue] of Object.entries(formData)) {
      const value = rawValue.trim() === "" ? "N/I" : rawValue;

      if (fieldPath.includes(".")) {
        const [parent, child] = fieldPath.split(".");

        if (relations.includes(parent)) {
          // relación conocida → anidado
          payload[parent] = payload[parent] || {};
          payload[parent][child] = value;
        } else if (parent === "datos_extra") {
          // campos extra → sin el prefijo
          payload.datos_extra[child] = value;
        } else {
          // cualquier otro parent inesperado
          payload.datos_extra[fieldPath] = value;
        }
      } else {
        // campo plano
        payload[fieldPath] = value;
      }
    }

    // eliminar datos_extra si quedó vacío
    if (!Object.keys(payload.datos_extra).length) {
      delete payload.datos_extra;
    }

    console.log("Payload a subir a la DB:", payload);
    //SUBIR A LA BASE DE DATOS
    createCepa(payload)
      .then((response) => {
        console.log("Cepa creada con éxito:", response);
        alert("Cepa creada con éxito");
        setFormData({});
        setFileData({});
        // Aquí podrías redirigir a otra página o mostrar un mensaje de éxito
      })
      .catch((error) => {
        console.error("Error al crear la cepa:", error);
        alert(
          "Error al crear la cepa. Por favor, revisa la consola para más detalles."
        );
      });
  };
  const handleConfirmYes = (): void => {
    // 1) Lookup headerName → field
    const headerToField = columns
      .filter(
        (col): col is ColDef & { field: string } =>
          typeof col.field === "string" && col.field !== "id"
      )
      .reduce<Record<string, string>>((acc, col) => {
        if (col.headerName) acc[col.headerName] = col.field;
        return acc;
      }, {});

    // 2) Inicializa todos los campos que tu DTO espera
    const payload: Record<string, any> = {
      nombre: null,
      cod_lab: null,
      origen: null,
      pigmentacion: null,
      almacenamiento: {},
      medio_cultivo: {},
      morfologia: {},
      actividad_enzimatica: {},
      crecimiento_temperatura: {},
      resistencia_antibiotica: {},
      caracterizacion_genetica: {},
      proyecto: {},
      datos_extra: {},
    };

    // 3) Recorre formData y va llenando payload
    for (const [headerName, rawValue] of Object.entries(formData)) {
      const val = rawValue === "" ? null : rawValue;
      const field = headerToField[headerName];

      if (!field) {
        // Sólo añadimos a datos_extra si tiene valor no nulo
        if (val != null) {
          payload.datos_extra[headerName] = val;
        }
        continue;
      }

      // Campos anidados: "parent.child"
      if (field.includes(".")) {
        const [parent, child] = field.split(".");
        payload[parent] = payload[parent] || {};
        payload[parent][child] = val;
      } else {
        // Campo plano
        payload[field] = val;
      }
    }

    // 4) Elimina objetos anidados completamente vacíos
    for (const key of Object.keys(payload)) {
      const val = payload[key];
      if (
        val &&
        typeof val === "object" &&
        !Array.isArray(val) &&
        Object.values(val).every((v) => v == null)
      ) {
        delete payload[key];
      }
    }

    // 5) Si datos_extra está vacío, lo quitamos
    try{
      if (!Object.keys(payload.datos_extra).length) {
        delete payload.datos_extra;
      }
    }catch{
      console.log("Data extra vacio");
    }


    // 6) Loguea el objeto final listo para subir
    console.log("Objeto final a subir a la DB:", payload);

    // 7) Llama a la función de creación
    createCepa(payload)
      .then((response) => {
        console.log("Cepa creada con éxito:", response);
        // Aquí podrías redirigir a otra página o mostrar un mensaje de éxito
      })
      .catch((error) => {
        console.error("Error al crear la cepa:", error);
        alert(
          "Error al crear la cepa. Por favor, revisa la consola para más detalles."
        );
      });
    // 8) Limpia el formulario
    setFormData({});
    setFileData({});
    inputRefs.current = [];
    // 9) Limpia el input de archivo
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }

    // 10) Cierra el modal
    setShowModal(false);
  };

  const handleConfirmNo = () => setShowModal(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setShowModal(true);
  };

  return (
    <div className="flex flex-col min-h-screen bg-gray-900 text-white">
      <header className="flex items-center justify-between p-4 border-b border-gray-700">
        <div className="relative p-4">
          <Link to="/">
          <button
            className="bg-gray-200 hover:bg-gray-300 text-white font-semibold rounded"
          >
            Volver
          </button>
          </Link>
          {/* ... aquí va el resto del contenido de tu página ... */}
        </div>

        <h1 className="text-2xl font-bold">Agregar Nueva Cepa</h1>
        <div className="space-x-2">
          <button
            onClick={handleDownloadTemplate}
            className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded"
          >
            Descargar Plantilla
          </button>
          <button
            onClick={() => fileInputRef.current?.click()}
            className="bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded"
          >
            Subir Archivo
          </button>
          <input
            type="file"
            accept=".txt"
            ref={fileInputRef}
            className="hidden"
            onChange={handleFileUpload}
          />
        </div>
      </header>

      <main className="flex-grow p-6">
        <form onSubmit={handleSubmit} className="space-y-4 max-w-xl mx-auto">
          {columns
            .filter(
              (col): col is ColDef & { field: string } =>
                typeof col.field === "string" && col.field !== "id"
            )
            .map((col, idx) => {
              const field = col.field;
              const label = col.headerName ?? field;
              return (
                <div key={field} className="flex flex-col">
                  <label htmlFor={field} className="mb-1 capitalize">
                    {label}
                  </label>
                  <input
                    id={field}
                    name={field}
                    type="text"
                    value={formData[field] || ""}
                    ref={(el) => {
                      inputRefs.current[idx] = el;
                    }}
                    onChange={(e) => handleInputChange(field, e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === "Enter") {
                        e.preventDefault();
                        const next = inputRefs.current[idx + 1];
                        next?.focus();
                      }
                    }}
                    className="bg-gray-800 text-white p-2 rounded border border-gray-700"
                  />
                </div>
              );
            })}

          <button
            type="button"
            className="bg-purple-500 hover:bg-purple-600 text-white font-semibold py-2 px-4 rounded"
            onClick={handleAddCepa}
          >
            Añadir Cepa
          </button>
        </form>
      </main>

      <ModalConfirmation
        visible={showModal}
        data={Object.keys(fileData).length ? fileData : formData}
        onConfirm={handleConfirmYes}
        onCancel={handleConfirmNo}
      />
    </div>
  );
}