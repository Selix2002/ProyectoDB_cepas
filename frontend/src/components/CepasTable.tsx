// src/components/CepsasTable.tsx
import {
    type ColumnDef,
    useReactTable,
    getCoreRowModel,
    flexRender,
  } from "@tanstack/react-table";
  import { type Cepa } from "../services/cepas";
  
  type Props = { data: Cepa[] };
  
  const columns: ColumnDef<Cepa>[] = [
    { accessorKey: "id", header: "ID" },
    { accessorKey: "nombre", header: "Nombre" },
    { accessorKey: "origen", header: "Origen" },
    {
      id: "acciones",
      header: "Acciones",
      // Aquí quito la destructuración de `row` porque no lo uso,
      // y podrías usar flexRender si quisieras también.
      cell: () => (
        <div className="flex gap-2">
          <button>👁️</button>
          <button>✏️</button>
          <button>🗑️</button>
        </div>
      ),
    },
  ];
  
  export function CepsasTable({ data }: Props) {
    const table = useReactTable({
      data,
      columns,
      getCoreRowModel: getCoreRowModel(),
    });
  
    return (
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          {table.getHeaderGroups().map(hg => (
            <tr key={hg.id}>
              {hg.headers.map(header => (
                <th
                  key={header.id}
                  className="px-4 py-2 text-left text-sm font-medium"
                >
                  {header.isPlaceholder
                    ? null
                    : flexRender(
                        header.column.columnDef.header,
                        header.getContext()
                      )}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {table.getRowModel().rows.map(row => (
            <tr key={row.id}>
              {row.getVisibleCells().map(cell => (
                <td key={cell.id} className="px-4 py-2 text-sm">
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    );
  }
  