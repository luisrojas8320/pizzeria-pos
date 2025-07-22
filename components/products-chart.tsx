"use client"

import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis, Tooltip } from "recharts"

const data = [
  { product: "Margherita", cantidad: 156 },
  { product: "Pepperoni", cantidad: 134 },
  { product: "Hawaiana", cantidad: 98 },
  { product: "Vegetariana", cantidad: 87 },
  { product: "Coca Cola", cantidad: 245 },
]

export function ProductsChart() {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data} layout="horizontal">
        <XAxis type="number" />
        <YAxis dataKey="product" type="category" width={80} />
        <Tooltip formatter={(value) => [`${value}`, "Cantidad vendida"]} labelStyle={{ color: "#000" }} />
        <Bar dataKey="cantidad" fill="#f97316" radius={[0, 4, 4, 0]} />
      </BarChart>
    </ResponsiveContainer>
  )
}
