// hooks/useCombinedData.ts
import { useState, useEffect } from "react";
import { fetchCepasFull, fetchStorageFull } from "../services/CepasQuery";

export function useCombinedData() {
  const [rowData, setRowData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let isMounted = true;
    setLoading(true);

    Promise.all([fetchCepasFull(), fetchStorageFull()])
      .then(([cepasData, storageRaw]) => {
        // Asegúrate de que storageRaw sea un array
        const storageList: any[] = Array.isArray(storageRaw)
          ? storageRaw
          : [];

        // Para depurar, puedes descomentar estos logs:
        // console.log("cepasData:", cepasData);
        // console.log("storageList:", storageList);

        // Fusiona: para cada cepa, busca el storage cuyo cepa_id === cepa.id
        const combined = cepasData.map((cepa: any) => {
          const almacen = storageList.find(
            (s: any) => s.cepa_id === cepa.id
          );

          // Si existe almacenamiento, mergea sus campos en la cepa
          if (almacen) {
            return {
              ...cepa,
              ...almacen,
            };
          }

          // Si no, devuelve la cepa tal cual
          return { ...cepa };
        });

        if (isMounted) {
          setRowData(combined);
          console.log(combined);
        }
      })
      .catch((err) => {
        console.error("🔴 error combinando datos:", err);
        if (isMounted) setError(err);
      })
      .finally(() => {
        if (isMounted) setLoading(false);
      });

    return () => {
      isMounted = false;
    };
  }, []);

  return { rowData, loading, error };
}
