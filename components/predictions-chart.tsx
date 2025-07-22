"use client"

import { Line, LineChart, ResponsiveContainer, XAxis, YAxis, Tooltip, Legend } from "recharts"

const data = [
  { day: "Lun", actual: 850, prediccion: 820, confianza: 95 },
  { day: "Mar", actual: 920, prediccion: 900, confianza: 92 },
  { day: "Mié", actual: 1100, prediccion: 1080, confianza: 88 },
  { day: "Jue", actual: 1250, prediccion: 1200, confianza: 90 },
  { day: "Vie", actual: 1800, prediccion: 1750, confianza: 94 },
  { day: "Sáb", actual: 2100, prediccion: 2050, confianza: 96 },
  { day: "Dom", actual: 1600, prediccion: 1580, confianza: 93 },
]

export function PredictionsChart() {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <XAxis dataKey="day" stroke="#888888" fontSize={12} tickLine={false} axisLine={false} />
        <YAxis
          stroke="#888888"
          fontSize={12}
          tickLine={false}
          axisLine={false}
          tickFormatter={(value) => `$${value}`}
        />
        <Tooltip
          formatter={(value, name) => [`$${value}`, name === "actual" ? "Ventas Reales" : "Predicción IA"]}
          labelStyle={{ color: "#000" }}
        />
        <Legend />
        <Line
          type="monotone"
          dataKey="actual"
          stroke="#f97316"
          strokeWidth={3}
          name="Ventas Reales"
          dot={{ fill: "#f97316", strokeWidth: 2, r: 4 }}
        />
        <Line
          type="monotone"
          dataKey="prediccion"
          stroke="#3b82f6"
          strokeWidth={2}
          strokeDasharray="5 5"
          name="Predicción IA"
          dot={{ fill: "#3b82f6", strokeWidth: 2, r: 3 }}
        />
      </LineChart>
    </ResponsiveContainer>
  )
}
