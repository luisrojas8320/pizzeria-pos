"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { AlertTriangle, Package } from "lucide-react"

const stockAlerts = [
  {
    item: "Queso Mozzarella",
    current: 2,
    minimum: 5,
    unit: "kg",
    severity: "high",
  },
  {
    item: "Masa para Pizza",
    current: 8,
    minimum: 15,
    unit: "unidades",
    severity: "medium",
  },
  {
    item: "Salsa de Tomate",
    current: 1,
    minimum: 3,
    unit: "litros",
    severity: "high",
  },
]

const severityColors = {
  high: "bg-red-100 text-red-800 border-red-200",
  medium: "bg-yellow-100 text-yellow-800 border-yellow-200",
  low: "bg-blue-100 text-blue-800 border-blue-200",
}

export function StockAlerts() {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle className="flex items-center gap-2">
          <AlertTriangle className="h-4 w-4 text-orange-500" />
          Alertas de Inventario
        </CardTitle>
        <Badge variant="destructive">{stockAlerts.length}</Badge>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {stockAlerts.map((alert, index) => (
            <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
              <div className="flex items-center gap-3">
                <Package className="h-4 w-4 text-muted-foreground" />
                <div>
                  <p className="font-medium">{alert.item}</p>
                  <p className="text-sm text-muted-foreground">
                    Stock actual: {alert.current} {alert.unit}
                  </p>
                </div>
              </div>
              <div className="text-right">
                <Badge className={severityColors[alert.severity as keyof typeof severityColors]} variant="outline">
                  {alert.severity === "high" ? "Crítico" : "Bajo"}
                </Badge>
                <p className="text-xs text-muted-foreground mt-1">
                  Min: {alert.minimum} {alert.unit}
                </p>
              </div>
            </div>
          ))}
          <Button className="w-full bg-transparent" variant="outline">
            Ver Todo el Inventario
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}
