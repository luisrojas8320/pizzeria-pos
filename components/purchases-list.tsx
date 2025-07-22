"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Calendar, Phone, Truck } from "lucide-react"

interface Purchase {
  id: string
  orderNumber: string
  supplier: string
  supplierContact: string
  items: Array<{
    name: string
    quantity: number
    unit: string
    unitCost: number
    total: number
  }>
  total: number
  status: "pending" | "ordered" | "received" | "cancelled"
  deliveryDate: string
  createdAt: string
  notes?: string
}

interface PurchasesListProps {
  searchTerm: string
  statusFilter: string
}

const mockPurchases: Purchase[] = [
  {
    id: "1",
    orderNumber: "PUR-001",
    supplier: "Distribuidora La Esperanza",
    supplierContact: "0987654321",
    items: [
      { name: "Queso Mozzarella", quantity: 10, unit: "kg", unitCost: 8.5, total: 85.0 },
      { name: "Masa para Pizza", quantity: 50, unit: "unidades", unitCost: 0.8, total: 40.0 },
    ],
    total: 125.0,
    status: "pending",
    deliveryDate: "2024-01-20",
    createdAt: "2024-01-15T10:00:00Z",
    notes: "Entregar en la mañana",
  },
  {
    id: "2",
    orderNumber: "PUR-002",
    supplier: "Alimentos del Norte",
    supplierContact: "0987654322",
    items: [
      { name: "Salsa de Tomate", quantity: 5, unit: "litros", unitCost: 3.2, total: 16.0 },
      { name: "Pepperoni", quantity: 3, unit: "kg", unitCost: 12.0, total: 36.0 },
    ],
    total: 52.0,
    status: "ordered",
    deliveryDate: "2024-01-18",
    createdAt: "2024-01-14T14:30:00Z",
  },
  {
    id: "3",
    orderNumber: "PUR-003",
    supplier: "Proveedora San Miguel",
    supplierContact: "0987654323",
    items: [{ name: "Jamón", quantity: 5, unit: "kg", unitCost: 9.5, total: 47.5 }],
    total: 47.5,
    status: "received",
    deliveryDate: "2024-01-16",
    createdAt: "2024-01-12T09:15:00Z",
  },
]

const statusColors = {
  pending: "bg-yellow-100 text-yellow-800",
  ordered: "bg-blue-100 text-blue-800",
  received: "bg-green-100 text-green-800",
  cancelled: "bg-red-100 text-red-800",
}

const statusLabels = {
  pending: "Pendiente",
  ordered: "Ordenado",
  received: "Recibido",
  cancelled: "Cancelado",
}

export function PurchasesList({ searchTerm, statusFilter }: PurchasesListProps) {
  const [purchases, setPurchases] = useState<Purchase[]>(mockPurchases)

  const filteredPurchases = purchases.filter((purchase) => {
    const matchesSearch =
      purchase.supplier.toLowerCase().includes(searchTerm.toLowerCase()) ||
      purchase.orderNumber.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesStatus = statusFilter === "all" || purchase.status === statusFilter
    return matchesSearch && matchesStatus
  })

  const updatePurchaseStatus = (purchaseId: string, newStatus: Purchase["status"]) => {
    setPurchases(
      purchases.map((purchase) => (purchase.id === purchaseId ? { ...purchase, status: newStatus } : purchase)),
    )
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("es-EC", {
      year: "numeric",
      month: "short",
      day: "numeric",
    })
  }

  return (
    <div className="space-y-4">
      {filteredPurchases.map((purchase) => (
        <Card key={purchase.id}>
          <CardHeader className="pb-3">
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between space-y-2 sm:space-y-0">
              <div className="flex items-center gap-4 min-w-0 flex-1">
                <CardTitle className="text-lg truncate">{purchase.orderNumber}</CardTitle>
                <Badge className={statusColors[purchase.status]} variant="secondary">
                  {statusLabels[purchase.status]}
                </Badge>
              </div>
              <div className="flex items-center gap-2 text-sm text-muted-foreground flex-shrink-0">
                <Calendar className="h-4 w-4" />
                <span>Entrega: {formatDate(purchase.deliveryDate)}</span>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
              {/* Supplier Info */}
              <div className="space-y-2">
                <h4 className="font-medium text-sm text-muted-foreground">PROVEEDOR</h4>
                <div className="space-y-1">
                  <p className="font-medium truncate">{purchase.supplier}</p>
                  <div className="flex items-center gap-1 text-sm text-muted-foreground">
                    <Phone className="h-3 w-3 flex-shrink-0" />
                    <span className="truncate">{purchase.supplierContact}</span>
                  </div>
                  <div className="flex items-center gap-1 text-sm text-muted-foreground">
                    <Truck className="h-3 w-3 flex-shrink-0" />
                    <span className="truncate">Entrega: {formatDate(purchase.deliveryDate)}</span>
                  </div>
                </div>
              </div>

              {/* Purchase Items */}
              <div className="space-y-2">
                <h4 className="font-medium text-sm text-muted-foreground">PRODUCTOS</h4>
                <div className="space-y-1 max-h-32 overflow-y-auto">
                  {purchase.items.map((item, index) => (
                    <div key={index} className="flex justify-between text-sm">
                      <span className="truncate mr-2">
                        {item.quantity} {item.unit} {item.name}
                      </span>
                      <span className="flex-shrink-0">${item.total.toFixed(2)}</span>
                    </div>
                  ))}
                  {purchase.notes && (
                    <p className="text-xs text-muted-foreground italic mt-2 truncate">Nota: {purchase.notes}</p>
                  )}
                </div>
              </div>

              {/* Actions */}
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <h4 className="font-medium text-sm text-muted-foreground">TOTAL</h4>
                  <span className="text-lg font-bold">${purchase.total.toFixed(2)}</span>
                </div>
                <div className="space-y-2">
                  <Select
                    value={purchase.status}
                    onValueChange={(value) => updatePurchaseStatus(purchase.id, value as Purchase["status"])}
                  >
                    <SelectTrigger className="w-full">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="pending">Pendiente</SelectItem>
                      <SelectItem value="ordered">Ordenado</SelectItem>
                      <SelectItem value="received">Recibido</SelectItem>
                      <SelectItem value="cancelled">Cancelado</SelectItem>
                    </SelectContent>
                  </Select>
                  <div className="flex gap-2">
                    <Button variant="outline" size="sm" className="flex-1 bg-transparent">
                      Ver Detalles
                    </Button>
                    <Button variant="outline" size="sm" className="flex-1 bg-transparent">
                      Imprimir
                    </Button>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      ))}

      {filteredPurchases.length === 0 && (
        <Card>
          <CardContent className="text-center py-8">
            <p className="text-muted-foreground">
              No se encontraron compras que coincidan con los filtros seleccionados.
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
