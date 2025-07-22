"use client"

import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"

const recentOrders = [
  {
    id: "ORD-001",
    customer: "Juan Pérez",
    items: "Pizza Margherita x2",
    total: 24.5,
    status: "preparing",
    platform: "Uber Eats",
    time: "14:30",
  },
  {
    id: "ORD-002",
    customer: "María Silva",
    items: "Pizza Pepperoni x1, Coca Cola x2",
    total: 18.75,
    status: "ready",
    platform: "Pedidos Ya",
    time: "14:25",
  },
  {
    id: "ORD-003",
    customer: "Carlos Mendoza",
    items: "Pizza Hawaiana x1",
    total: 15.0,
    status: "delivered",
    platform: "Bis",
    time: "14:15",
  },
  {
    id: "ORD-004",
    customer: "Ana García",
    items: "Pizza Vegetariana x1, Sprite x1",
    total: 17.25,
    status: "preparing",
    platform: "Presencial",
    time: "14:35",
  },
]

const statusColors = {
  preparing: "bg-yellow-100 text-yellow-800",
  ready: "bg-green-100 text-green-800",
  delivered: "bg-blue-100 text-blue-800",
}

const statusLabels = {
  preparing: "Preparando",
  ready: "Listo",
  delivered: "Entregado",
}

export function RecentOrders() {
  return (
    <ScrollArea className="h-[300px]">
      <div className="space-y-4">
        {recentOrders.map((order) => (
          <div key={order.id} className="flex items-center justify-between space-x-4">
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1">
                <p className="text-sm font-medium truncate">{order.id}</p>
                <Badge variant="outline" className="text-xs">
                  {order.platform}
                </Badge>
              </div>
              <p className="text-sm text-muted-foreground truncate">{order.customer}</p>
              <p className="text-xs text-muted-foreground truncate">{order.items}</p>
            </div>
            <div className="text-right">
              <p className="text-sm font-medium">${order.total.toFixed(2)}</p>
              <p className="text-xs text-muted-foreground">{order.time}</p>
              <Badge
                className={`text-xs ${statusColors[order.status as keyof typeof statusColors]}`}
                variant="secondary"
              >
                {statusLabels[order.status as keyof typeof statusLabels]}
              </Badge>
            </div>
          </div>
        ))}
      </div>
    </ScrollArea>
  )
}
