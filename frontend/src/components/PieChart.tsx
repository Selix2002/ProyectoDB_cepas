import React from "react";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from "chart.js";
import { Pie } from "react-chartjs-2";

// Registrar los elementos de Chart.js 
ChartJS.register(ArcElement, Tooltip, Legend);

interface Props {
  /** 
   * stats[field] = { valor1: count1, valor2: count2, … }
   */
  stats: Record<string, Record<string, number>>;
  /** campo seleccionado para graficar */
  selectedField: string;
  /** callback al cambiar la columna */
  onFieldChange: (field: string) => void;
}

const CepaStatsChart: React.FC<Props> = ({
  stats,
  selectedField,
  onFieldChange,
}) => {
  const fields = Object.keys(stats);
  if (fields.length === 0) return <p>No hay datos para graficar.</p>;

  // Si el selectedField no existe en stats, fallback al primero
  const field = fields.includes(selectedField)
    ? selectedField
    : fields[0];

  const dataObj = stats[field];
  const labels = Object.keys(dataObj);
  const data = {
    labels,
    datasets: [
      {
        data: Object.values(dataObj),
      },
    ],
  };

  return (
    <div className="cepa-stats-chart mt-6">
      <div className="flex items-center mb-4">
        <label className="mr-2 font-medium">Columna:</label>
        <select
          className="border rounded px-2 py-1"
          value={field}
          onChange={(e) => onFieldChange(e.target.value)}
        >
          {fields.map((f) => (
            <option key={f} value={f}>
              {f}
            </option>
          ))}
        </select>
      </div>
      <Pie data={data} />
    </div>
  );
};

export default CepaStatsChart;
