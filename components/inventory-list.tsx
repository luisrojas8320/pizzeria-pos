"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Edit, Trash2, Plus, Minus } from "lucide-react"

interface InventoryItem {
  id: string
  name: string
  category: string
  currentStock: number
  minStock: number
  maxStock: number
  unit: string
  unitCost: number
  totalValue: number
  supplier: string
  lastRestocked: string
  expiryDate?: string
}

interface InventoryListProps {
  searchTerm: string
  categoryFilter: string
}

const mockInventory: InventoryItem[] = [
  {
    id: "1",
    name: "Queso Mozzarella",
    category: "ingredientes",
    currentStock: 2,
    minStock: 5,
    maxStock: 20,
    unit: "kg",
    unitCost: 8.5,
    totalValue: 17.0,
    supplier: "Distribuidora La Esperanza",
    lastRestocked: "2024-01-10",
    expiryDate: "2024-01-25",
  },
  {
    id: "2",
    name: "Masa para Pizza",
    category: "ingredientes",
    currentStock: 8,
    minStock: 15,
    maxStock: 50,
    unit: "unidades",
    unitCost: 0.8,
    totalValue: 6.4,
    supplier: "Alimentos del Norte",
    lastRestocked: "2024-01-12",
  },
  {
    id: "3",
    name: "Salsa de Tomate",
    category: "ingredientes",
    currentStock: 1,
    minStock: 3,
    maxStock: 10,
    unit: "litros",
    unitCost: 3.2,
    totalValue: 3.2,
    supplier: "Proveedora San Miguel",
    lastRestocked: "2024-01-08",
    expiryDate: "2024-02-15",
  },
  {
    id: "4",
    name: "Coca Cola 500ml",
    category: "bebidas",
    currentStock: 24,
    minStock: 12,
    maxStock: 48,
    unit: "unidades",
    unitCost: 1.2,
    totalValue: 28.8,
    supplier: "Distribuidora Coca Cola",
    lastRestocked: "2024-01-14",
  },
  {
    id: "5",
    name: "Cajas de Pizza",
    category: "empaques",
    currentStock: 0,
    minStock: 50,
    maxStock: 200,
    unit: "unidades",
    unitCost: 0.25,
    totalValue: 0,
    supplier: "Empaques del Norte",
    lastRestocked: "2024-01-05",
  },
]

const categoryLabels = {
  ingredientes: "Ingredientes",
  bebidas: "Bebidas",
  empaques: "Empaques",
  limpieza: "Limpieza",
}

export function InventoryList({ searchTerm, categoryFilter }: InventoryListProps) {
  const [inventory, setInventory] = useState<InventoryItem[]>(mockInventory)

  const filteredInventory = inventory.filter((item) => {
    const matchesSearch = item.name.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesCategory = categoryFilter === "all" || item.category === categoryFilter
    return matchesSearch && matchesCategory
  })

  const getStockStatus = (item: InventoryItem) => {
    if (item.currentStock === 0) return { status: "out", label: "Agotado", color: "bg-red-500" }
    if (item.currentStock <= item.minStock) return { status: "low", label: "Bajo", color: "bg-orange-500" }
    if (item.currentStock >= item.maxStock) return { status: "high", label: "Alto", color: "bg-blue-500" }
    return { status: "normal", label: "Normal", color: "bg-green-500" }
  }

  const getStockPercentage = (item: InventoryItem) => {
    return Math.min((item.currentStock / item.maxStock) * 100, 100)
  }

  const updateStock = (id: string, change: number) => {
    setInventory(
      inventory.map((item) => {
        if (item.id === id) {
          const newStock = Math.max(0, item.currentStock + change)
          return {
            ...item,
            currentStock: newStock,
            totalValue: newStock * item.unitCost,
          }
        }
        return item
      }),
    )
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("es-EC", {
      year: "numeric",
      month: "short",
      day: "numeric",
    })
  }

  const isExpiringSoon = (expiryDate?: string) => {
    if (!expiryDate) return false
    const today = new Date()
    const expiry = new Date(expiryDate)
    const diffTime = expiry.getTime() - today.getTime()
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    return diffDays <= 7 && diffDays > 0
  }

  const isExpired = (expiryDate?: string) => {
    if (!expiryDate) return false
    const today = new Date()
    const expiry = new Date(expiryDate)
    return expiry < today
  }

  return (
    <div className="space-y-4">
      <div className="grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
        {filteredInventory.map((item) => {
          const stockStatus = getStockStatus(item)
          const stockPercentage = getStockPercentage(item)
          const expiringSoon = isExpiringSoon(item.expiryDate)
          const expired = isExpired(item.expiryDate)

          return (
            <Card key={item.id} className={expired ? "border-red-200 bg-red-50" : ""}>
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between">
                  <div className="min-w-0 flex-1">
                    <CardTitle className="text-lg truncate">{item.name}</CardTitle>
                    <div className="flex items-center gap-2 mt-1">
                      <Badge variant="outline" className="text-xs">
                        {categoryLabels[item.category as keyof typeof categoryLabels]}
                      </Badge>
                      <Badge className={`text-xs text-white ${stockStatus.color}`} variant="secondary">
                        {stockStatus.label}
                      </Badge>
                    </div>
                  </div>
                  <div className="flex gap-1 flex-shrink-0">
                    <Button variant="ghost" size="sm">
                      <Edit className="h-4 w-4" />
                    </Button>
                    <Button variant="ghost" size="sm">
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Stock Actual</span>
                    <span className="font-medium">
                      {item.currentStock} {item.unit}
                    </span>
                  </div>
                  <Progress value={stockPercentage} className="h-2" />
                  <div className="flex justify-between text-xs text-muted-foreground">
                    <span>Min: {item.minStock}</span>
                    <span>Max: {item.maxStock}</span>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <p className="text-muted-foreground">Costo Unitario</p>
                    <p className="font-medium">${item.unitCost.toFixed(2)}</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground">Valor Total</p>
                    <p className="font-medium">${item.totalValue.toFixed(2)}</p>
                  </div>
                </div>

                <div className="text-sm">
                  <p className="text-muted-foreground">Proveedor:</p>
                  <p className="font-medium truncate">{item.supplier}</p>
                </div>

                <div className="text-sm">
                  <p className="text-muted-foreground">Última Reposición:</p>
                  <p className="font-medium">{formatDate(item.lastRestocked)}</p>
                </div>

                {item.expiryDate && (
                  <div className="text-sm">
                    <p className="text-muted-foreground">Vencimiento:</p>
                    <p className={`font-medium ${expired ? "text-red-600" : expiringSoon ? "text-orange-600" : ""}`}>
                      {formatDate(item.expiryDate)}
                      {expired && " (Vencido)"}
                      {expiringSoon && !expired && " (Próximo a vencer)"}
                    </p>
                  </div>
                )}

                <div className="flex items-center justify-between pt-2 border-t">
                  <div className="flex items-center gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => updateStock(item.id, -1)}
                      disabled={item.currentStock === 0}
                    >
                      <Minus className="h-4 w-4" />
                    </Button>
                    <span className="text-sm font-medium w-8 text-center">{item.currentStock}</span>
                    <Button variant="outline" size="sm" onClick={() => updateStock(item.id, 1)}>
                      <Plus className="h-4 w-4" />
                    </Button>
                  </div>
                  <Button variant="outline" size="sm" className="bg-transparent">
                    Reabastecer
                  </Button>
                </div>
              </CardContent>
            </Card>
          )
        })}
      </div>

      {filteredInventory.length === 0 && (
        <Card>
          <CardContent className="text-center py-8">
            <p className="text-muted-foreground">
              No se encontraron productos que coincidan con los filtros seleccionados.
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
