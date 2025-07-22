"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Phone, Mail, MapPin, Calendar, Star, TrendingUp } from "lucide-react"

interface Customer {
  id: string
  name: string
  phone: string
  email?: string
  address?: string
  totalOrders: number
  totalSpent: number
  averageOrder: number
  lastOrder: string
  joinDate: string
  type: "regular" | "frequent" | "vip" | "new"
  favoriteItems: string[]
}

interface CustomersListProps {
  searchTerm: string
  filterType: string
}

const mockCustomers: Customer[] = [
  {
    id: "1",
    name: "Juan Pérez",
    phone: "0987654321",
    email: "juan@email.com",
    address: "Av. Cristóbal Colón 123, Ibarra",
    totalOrders: 25,
    totalSpent: 487.5,
    averageOrder: 19.5,
    lastOrder: "2024-01-14",
    joinDate: "2023-08-15",
    type: "frequent",
    favoriteItems: ["Pizza Margherita", "Coca Cola 500ml"],
  },
  {
    id: "2",
    name: "María Silva",
    phone: "0987654322",
    email: "maria@email.com",
    address: "Calle García Moreno 456, Ibarra",
    totalOrders: 42,
    totalSpent: 892.3,
    averageOrder: 21.25,
    lastOrder: "2024-01-15",
    joinDate: "2023-05-20",
    type: "vip",
    favoriteItems: ["Pizza Pepperoni", "Pizza Hawaiana"],
  },
  {
    id: "3",
    name: "Carlos Mendoza",
    phone: "0987654323",
    address: "Barrio El Olivo, Casa 789",
    totalOrders: 8,
    totalSpent: 156.75,
    averageOrder: 19.59,
    lastOrder: "2024-01-12",
    joinDate: "2023-12-01",
    type: "regular",
    favoriteItems: ["Pizza Hawaiana"],
  },
  {
    id: "4",
    name: "Ana García",
    phone: "0987654324",
    email: "ana@email.com",
    totalOrders: 3,
    totalSpent: 52.25,
    averageOrder: 17.42,
    lastOrder: "2024-01-10",
    joinDate: "2024-01-05",
    type: "new",
    favoriteItems: ["Pizza Vegetariana"],
  },
]

const typeColors = {
  regular: "bg-gray-100 text-gray-800",
  frequent: "bg-blue-100 text-blue-800",
  vip: "bg-purple-100 text-purple-800",
  new: "bg-green-100 text-green-800",
}

const typeLabels = {
  regular: "Regular",
  frequent: "Frecuente",
  vip: "VIP",
  new: "Nuevo",
}

export function CustomersList({ searchTerm, filterType }: CustomersListProps) {
  const [customers, setCustomers] = useState<Customer[]>(mockCustomers)

  const filteredCustomers = customers.filter((customer) => {
    const matchesSearch =
      customer.name.toLowerCase().includes(searchTerm.toLowerCase()) || customer.phone.includes(searchTerm)
    const matchesFilter = filterType === "all" || customer.type === filterType
    return matchesSearch && matchesFilter
  })

  const getInitials = (name: string) => {
    return name
      .split(" ")
      .map((n) => n[0])
      .join("")
      .toUpperCase()
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("es-EC", {
      year: "numeric",
      month: "short",
      day: "numeric",
    })
  }

  const getCustomerInsights = (customer: Customer) => {
    const insights = []

    if (customer.totalOrders >= 20) {
      insights.push("Cliente leal")
    }
    if (customer.averageOrder > 20) {
      insights.push("Alto valor")
    }
    if (customer.type === "new") {
      insights.push("Oportunidad de fidelización")
    }

    return insights
  }

  return (
    <div className="space-y-4">
      <div className="grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
        {filteredCustomers.map((customer) => {
          const insights = getCustomerInsights(customer)

          return (
            <Card key={customer.id}>
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-3 min-w-0 flex-1">
                    <Avatar>
                      <AvatarFallback>{getInitials(customer.name)}</AvatarFallback>
                    </Avatar>
                    <div className="min-w-0 flex-1">
                      <CardTitle className="text-lg truncate">{customer.name}</CardTitle>
                      <Badge className={typeColors[customer.type]} variant="secondary">
                        {typeLabels[customer.type]}
                      </Badge>
                    </div>
                  </div>
                  {customer.type === "vip" && <Star className="h-5 w-5 text-purple-500 flex-shrink-0" />}
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2 text-sm">
                  <div className="flex items-center gap-2">
                    <Phone className="h-4 w-4 text-muted-foreground flex-shrink-0" />
                    <span className="truncate">{customer.phone}</span>
                  </div>
                  {customer.email && (
                    <div className="flex items-center gap-2">
                      <Mail className="h-4 w-4 text-muted-foreground flex-shrink-0" />
                      <span className="truncate">{customer.email}</span>
                    </div>
                  )}
                  {customer.address && (
                    <div className="flex items-center gap-2">
                      <MapPin className="h-4 w-4 text-muted-foreground flex-shrink-0" />
                      <span className="truncate">{customer.address}</span>
                    </div>
                  )}
                  <div className="flex items-center gap-2">
                    <Calendar className="h-4 w-4 text-muted-foreground flex-shrink-0" />
                    <span className="truncate">Cliente desde: {formatDate(customer.joinDate)}</span>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <p className="text-muted-foreground">Total Pedidos</p>
                    <p className="font-bold text-lg">{customer.totalOrders}</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground">Total Gastado</p>
                    <p className="font-bold text-lg">${customer.totalSpent.toFixed(2)}</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground">Promedio</p>
                    <p className="font-medium">${customer.averageOrder.toFixed(2)}</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground">Último Pedido</p>
                    <p className="font-medium">{formatDate(customer.lastOrder)}</p>
                  </div>
                </div>

                {customer.favoriteItems.length > 0 && (
                  <div>
                    <p className="text-sm text-muted-foreground mb-2">Productos Favoritos:</p>
                    <div className="flex flex-wrap gap-1">
                      {customer.favoriteItems.slice(0, 2).map((item, index) => (
                        <Badge key={index} variant="outline" className="text-xs">
                          {item}
                        </Badge>
                      ))}
                      {customer.favoriteItems.length > 2 && (
                        <Badge variant="outline" className="text-xs">
                          +{customer.favoriteItems.length - 2} más
                        </Badge>
                      )}
                    </div>
                  </div>
                )}

                {insights.length > 0 && (
                  <div>
                    <p className="text-sm text-muted-foreground mb-2">Insights:</p>
                    <div className="flex flex-wrap gap-1">
                      {insights.map((insight, index) => (
                        <Badge key={index} variant="secondary" className="text-xs bg-orange-100 text-orange-800">
                          <TrendingUp className="h-3 w-3 mr-1" />
                          {insight}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}

                <div className="flex gap-2">
                  <Button variant="outline" size="sm" className="flex-1 bg-transparent">
                    Ver Historial
                  </Button>
                  <Button variant="outline" size="sm" className="flex-1 bg-transparent">
                    Contactar
                  </Button>
                </div>
              </CardContent>
            </Card>
          )
        })}
      </div>

      {filteredCustomers.length === 0 && (
        <Card>
          <CardContent className="text-center py-8">
            <p className="text-muted-foreground">
              No se encontraron clientes que coincidan con los filtros seleccionados.
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
