"use client"

import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts"

const data = [
  { name: "Uber Eats", value: 35, color: "#000000" },
  { name: "Pedidos Ya", value: 28, color: "#ff6b35" },
  { name: "Bis", value: 20, color: "#4285f4" },
  { name: "Presencial", value: 17, color: "#34a853" },
]

export function PlatformChart() {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          labelLine={false}
          label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
          outerRadius={80}
          fill="#8884d8"
          dataKey="value"
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={entry.color} />
          ))}
        </Pie>
        <Tooltip formatter={(value) => [`${value}%`, "Porcentaje"]} />
      </PieChart>
    </ResponsiveContainer>
  )
}
