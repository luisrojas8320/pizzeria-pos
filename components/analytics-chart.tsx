"use client"

import { Area, AreaChart, ResponsiveContainer, XAxis, YAxis, Tooltip, Legend } from "recharts"

const data = [
  { month: "Ene", ventas: 8500, prediccion: 8200, tendencia: 8300 },
  { month: "Feb", ventas: 9200, prediccion: 9100, tendencia: 9000 },
  { month: "Mar", ventas: 8800, prediccion: 9300, tendencia: 9200 },
  { month: "Abr", ventas: 10500, prediccion: 9800, tendencia: 9800 },
  { month: "May", ventas: 11200, prediccion: 10800, tendencia: 10500 },
  { month: "Jun", ventas: 12800, prediccion: 11500, tendencia: 11800 },
  { month: "Jul", ventas: 13500, prediccion: 12800, tendencia: 12500 },
  { month: "Ago", ventas: 12900, prediccion: 13200, tendencia: 13000 },
]

export function AnalyticsChart() {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <AreaChart data={data}>
        <XAxis dataKey="month" stroke="#888888" fontSize={12} tickLine={false} axisLine={false} />
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
            name === "ventas" ? "Ventas Reales" : name === "prediccion" ? "Predicción" : "Tendencia",
          ]}
          labelStyle={{ color: "#000" }}
        />
        <Legend />
        <Area
          type="monotone"
          dataKey="ventas"
          stackId="1"
          stroke="#f97316"
          fill="#f97316"
          fillOpacity={0.6}
          name="Ventas Reales"
        />
        <Area
          type="monotone"
          dataKey="prediccion"
          stackId="2"
          stroke="#3b82f6"
          fill="#3b82f6"
          fillOpacity={0.4}
          name="Predicción"
        />
        <Area
          type="monotone"
          dataKey="tendencia"
          stackId="3"
          stroke="#10b981"
          fill="#10b981"
          fillOpacity={0.3}
          name="Tendencia"
        />
      </AreaChart>
    </ResponsiveContainer>
  )
}
