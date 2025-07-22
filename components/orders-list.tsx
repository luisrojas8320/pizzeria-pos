"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Clock, MapPin, Phone, CreditCard } from "lucide-react"

interface Order {
  id: string
  orderNumber: string
  customerName: string
  customerPhone: string
  customerAddress: string
  items: Array<{
    name: string
    quantity: number
    price: number
  }>
  total: number
  status: "pending" | "preparing" | "ready" | "delivered" | "cancelled"
  paymentMethod: string
  platform: string
  createdAt: string
  estimatedTime?: string
  notes?: string
}

interface OrdersListProps {
  searchTerm: string
  statusFilter: string
}

const mockOrders: Order[] = [
  {
    id: "1",
    orderNumber: "ORD-001",
    customerName: "Juan Pérez",
    customerPhone: "0987654321",
    customerAddress: "Av. Cristóbal Colón 123, Ibarra",
    items: [
      { name: "Pizza Margherita", quantity: 2, price: 12.5 },
      { name: "Coca Cola 500ml", quantity: 2, price: 2.5 },
    ],
    total: 30.0,
    status: "preparing",
    paymentMethod: "efectivo",
    platform: "uber-eats",
    createdAt: "2024-01-15T14:30:00Z",
    estimatedTime: "25 min",
    notes: "Sin cebolla en una pizza",
  },
  {
    id: "2",
    orderNumber: "ORD-002",
    customerName: "María Silva",
    customerPhone: "0987654322",
    customerAddress: "Calle García Moreno 456, Ibarra",
    items: [
      { name: "Pizza Pepperoni", quantity: 1, price: 14.0 },
      { name: "Sprite 500ml", quantity: 1, price: 2.5 },
    ],
    total: 16.5,
    status: "ready",
    paymentMethod: "tarjeta",
    platform: "pedidos-ya",
    createdAt: "2024-01-15T14:25:00Z",
    estimatedTime: "Listo",
  },
  {
    id: "3",
    orderNumber: "ORD-003",
    customerName: "Carlos Mendoza",
    customerPhone: "0987654323",
    customerAddress: "Barrio El Olivo, Casa 789",
    items: [{ name: "Pizza Hawaiana", quantity: 1, price: 15.5 }],
    total: 15.5,
    status: "delivered",
    paymentMethod: "efectivo",
    platform: "bis",
    createdAt: "2024-01-15T14:15:00Z",
  },
  {
    id: "4",
    orderNumber: "ORD-004",
    customerName: "Ana García",
    customerPhone: "0987654324",
    customerAddress: "Presencial",
    items: [
      { name: "Pizza Vegetariana", quantity: 1, price: 13.75 },
      { name: "Agua 500ml", quantity: 1, price: 1.5 },
    ],
    total: 15.25,
    status: "pending",
    paymentMethod: "efectivo",
    platform: "presencial",
    createdAt: "2024-01-15T14:35:00Z",
    estimatedTime: "30 min",
  },
]

const statusColors = {
  pending: "bg-gray-100 text-gray-800",
  preparing: "bg-yellow-100 text-yellow-800",
  ready: "bg-green-100 text-green-800",
  delivered: "bg-blue-100 text-blue-800",
  cancelled: "bg-red-100 text-red-800",
}

const statusLabels = {
  pending: "Pendiente",
  preparing: "Preparando",
  ready: "Listo",
  delivered: "Entregado",
  cancelled: "Cancelado",
}

const platformLabels = {
  "uber-eats": "Uber Eats",
  "pedidos-ya": "Pedidos Ya",
  bis: "Bis",
  presencial: "Presencial",
  telefono: "Teléfono",
}

const paymentLabels = {
  efectivo: "Efectivo",
  tarjeta: "Tarjeta",
  transferencia: "Transferencia",
  plataforma: "Plataforma",
}

export function OrdersList({ searchTerm, statusFilter }: OrdersListProps) {
  const [orders, setOrders] = useState<Order[]>(mockOrders)

  const filteredOrders = orders.filter((order) => {
    const matchesSearch =
      order.customerName.toLowerCase().includes(searchTerm.toLowerCase()) ||
      order.orderNumber.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesStatus = statusFilter === "all" || order.status === statusFilter
    return matchesSearch && matchesStatus
  })

  const updateOrderStatus = (orderId: string, newStatus: Order["status"]) => {
    setOrders(orders.map((order) => (order.id === orderId ? { ...order, status: newStatus } : order)))
  }

  const formatTime = (dateString: string) => {
    return new Date(dateString).toLocaleTimeString("es-EC", {
      hour: "2-digit",
      minute: "2-digit",
    })
  }

  return (
    <div className="space-y-4">
      {filteredOrders.map((order) => (
        <Card key={order.id}>
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <CardTitle className="text-lg">{order.orderNumber}</CardTitle>
                <Badge className={statusColors[order.status]} variant="secondary">
                  {statusLabels[order.status]}
                </Badge>
                <Badge variant="outline">{platformLabels[order.platform as keyof typeof platformLabels]}</Badge>
              </div>
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <Clock className="h-4 w-4" />
                {formatTime(order.createdAt)}
                {order.estimatedTime && <span className="ml-2 font-medium">{order.estimatedTime}</span>}
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Customer Info */}
              <div className="space-y-2">
                <h4 className="font-medium text-sm text-muted-foreground">CLIENTE</h4>
                <div className="space-y-1">
                  <p className="font-medium">{order.customerName}</p>
                  {order.customerPhone && (
                    <div className="flex items-center gap-1 text-sm text-muted-foreground">
                      <Phone className="h-3 w-3" />
                      {order.customerPhone}
                    </div>
                  )}
                  {order.customerAddress && order.customerAddress !== "Presencial" && (
                    <div className="flex items-center gap-1 text-sm text-muted-foreground">
                      <MapPin className="h-3 w-3" />
                      {order.customerAddress}
                    </div>
                  )}
                  <div className="flex items-center gap-1 text-sm text-muted-foreground">
                    <CreditCard className="h-3 w-3" />
                    {paymentLabels[order.paymentMethod as keyof typeof paymentLabels]}
                  </div>
                </div>
              </div>

              {/* Order Items */}
              <div className="space-y-2">
                <h4 className="font-medium text-sm text-muted-foreground">PRODUCTOS</h4>
                <div className="space-y-1">
                  {order.items.map((item, index) => (
                    <div key={index} className="flex justify-between text-sm">
                      <span>
                        {item.quantity}x {item.name}
                      </span>
                      <span>${(item.price * item.quantity).toFixed(2)}</span>
                    </div>
                  ))}
                  {order.notes && <p className="text-xs text-muted-foreground italic mt-2">Nota: {order.notes}</p>}
                </div>
              </div>

              {/* Actions */}
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <h4 className="font-medium text-sm text-muted-foreground">TOTAL</h4>
                  <span className="text-lg font-bold">${order.total.toFixed(2)}</span>
                </div>
                <div className="space-y-2">
                  <Select
                    value={order.status}
                    onValueChange={(value) => updateOrderStatus(order.id, value as Order["status"])}
                  >
                    <SelectTrigger className="w-full">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="pending">Pendiente</SelectItem>
                      <SelectItem value="preparing">Preparando</SelectItem>
                      <SelectItem value="ready">Listo</SelectItem>
                      <SelectItem value="delivered">Entregado</SelectItem>
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

      {filteredOrders.length === 0 && (
        <Card>
          <CardContent className="text-center py-8">
            <p className="text-muted-foreground">
              No se encontraron pedidos que coincidan con los filtros seleccionados.
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
