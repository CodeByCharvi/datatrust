import {
  Bar, BarChart, CartesianGrid, Line, LineChart,
  ResponsiveContainer, Tooltip, XAxis, YAxis,
} from "recharts";

export default function ResultChart({ chart, columns, rows }) {
  if (!rows || rows.length === 0) return null;

  if (chart === "number" && typeof rows[0][0] === "number") {
    return <p style={{ fontSize: 48, margin: "16px 0" }}>{rows[0][0].toLocaleString()}</p>;
  }

  if ((chart === "bar" || chart === "line") && columns.length === 2) {
    const data = rows.map((r) => ({ label: String(r[0]), value: Number(r[1]) }));
    const Chart = chart === "bar" ? BarChart : LineChart;

    return (
      <div style={{ width: "100%", height: 300, margin: "16px 0" }}>
        <ResponsiveContainer>
          <Chart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="label" />
            <YAxis
              width={70}
              tickFormatter={(v) => v.toLocaleString("en-US", { notation: "compact" })}
            />
            <Tooltip />
            {chart === "bar" ? (
              <Bar dataKey="value" name={columns[1]} fill="#4f46e5" />
            ) : (
              <Line dataKey="value" name={columns[1]} stroke="#4f46e5" dot={false} />
            )}
          </Chart>
        </ResponsiveContainer>
      </div>
    );
  }

  return null;
}