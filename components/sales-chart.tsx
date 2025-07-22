"use client"

import { Line, LineChart, ResponsiveContainer, XAxis, YAxis, Tooltip, Legend } from "recharts"

const data = [
  { date: "01 Ene", ventas: 450, costos: 180, ganancia: 270 },
  { date: "02 Ene", ventas: 520, costos: 210, ganancia: 310 },
  { date: "03 Ene", ventas: 380, costos: 150, ganancia: 230 },
  { date: "04 Ene", ventas: 680, costos: 270, ganancia: 410 },
  { date: "05 Ene", ventas: 750, costos: 300, ganancia: 450 },
  { date: "06 Ene", ventas: 620, costos: 250, ganancia: 370 },
  { date: "07 Ene", ventas: 590, costos: 240, ganancia: 350 },
]

export function SalesChart() {
  return (
    <ResponsiveContainer width="100%" height={350}>
      <LineChart data={data}>
        <XAxis dataKey="date" stroke="#888888" fontSize={12} tickLine={false} axisLine={false} />
        <YAxis
          stroke="#888888"
          fontSize={12}
          tickLine={false}
          axisLine={false}
          tickFormatter={(value) => `$${value}`}
        />
        <Tooltip
          formatter={(value, name) => [
            `$${value}`,
            name === "ventas" ? "Ventas" : name === "costos" ? "Costos" : "Ganancia",
          ]}
          labelStyle={{ color: "#000" }}
        />
        <Legend />
        <Line type="monotone" dataKey="ventas" stroke="#f97316" strokeWidth={2} name="Ventas" />
        <Line type="monotone" dataKey="costos" stroke="#ef4444" strokeWidth={2} name="Costos" />
        <Line type="monotone" dataKey="ganancia" stroke="#22c55e" strokeWidth={2} name="Ganancia" />
      </LineChart>
    </ResponsiveContainer>
  )
}
