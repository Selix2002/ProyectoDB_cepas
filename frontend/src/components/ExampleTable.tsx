import { useMemo, useState, useEffect } from 'react';
import { AgGridReact } from 'ag-grid-react';
import { AllCommunityModule, ModuleRegistry } from 'ag-grid-community';
import { fetchCepasFull } from '../services/CepasQuery';

ModuleRegistry.registerModules([AllCommunityModule]);

/**
 * CepasTable: componente independiente que renderiza un Ag Grid con datos de cepas cargadas desde la API.
 */
export function CepasTable() {
  const columnDefs = useMemo(
    () => [
      { headerName: 'ID',            field: 'id',                           filter: 'agNumberColumnFilter' },
      { headerName: 'Nombre',        field: 'nombre',                       filter: 'agTextColumnFilter'   },
      { headerName: 'Código Lab',    field: 'cod_lab',                      filter: 'agTextColumnFilter'   },
      { headerName: 'Envío PUQ',     field: 'almacenamiento.envio_puq',     filter: 'agTextColumnFilter'   },
      { headerName: '–80 °C',        field: 'almacenamiento.temperatura_menos80', filter: 'agTextColumnFilter' },
      { headerName: 'Medio Cultivo', field: 'medio_cultivo.medio',          filter: 'agTextColumnFilter'   },
      // Añade aquí más columnas según tus relaciones...
    ],
    []
  );

  const [rowData, setRowData] = useState<any[]>([]);

  useEffect(() => {
    fetchCepasFull()
      .then((data) => {
        console.log('Datos obtenidos:', data);
        setRowData(data);
      })
      .catch((error) => console.error('Error al cargar cepas:', error));
  }, []);

  return (
    <div className="ag-theme-alpine custom-space w-full h-full">
      <AgGridReact
        columnDefs={columnDefs}
        rowData={rowData}
        defaultColDef={{
          sortable: true,
          filter: true,
          resizable: true,
          flex: 1,
          editable: true,
          columnGroupShow: true,
        }}
        pagination
        paginationPageSize={20}
      />
    </div>
  );
}

export default CepasTable;
