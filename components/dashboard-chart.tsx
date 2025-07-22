"use client"

import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis, Tooltip } from "recharts"

const data = [
  { hour: "08:00", sales: 45 },
  { hour: "09:00", sales: 78 },
  { hour: "10:00", sales: 120 },
  { hour: "11:00", sales: 165 },
  { hour: "12:00", sales: 280 },
  { hour: "13:00", sales: 320 },
  { hour: "14:00", sales: 290 },
  { hour: "15:00", sales: 180 },
  { hour: "16:00", sales: 140 },
  { hour: "17:00", sales: 160 },
  { hour: "18:00", sales: 220 },
  { hour: "19:00", sales: 310 },
  { hour: "20:00", sales: 280 },
  { hour: "21:00", sales: 190 },
]

export function DashboardChart() {
  return (
    <ResponsiveContainer width="100%" height={350}>
      <BarChart data={data}>
        <XAxis dataKey="hour" stroke="#888888" fontSize={12} tickLine={false} axisLine={false} />
        <YAxis
          stroke="#888888"
          fontSize={12}
          tickLine={false}
          axisLine={false}
          tickFormatter={(value) => `$${value}`}
        />
        <Tooltip formatter={(value) => [`$${value}`, "Ventas"]} labelStyle={{ color: "#000" }} />
        <Bar dataKey="sales" fill="#f97316" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  )
}
