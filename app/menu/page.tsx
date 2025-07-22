"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { SidebarTrigger } from "@/components/ui/sidebar"
import { Plus, Edit, Trash2, DollarSign, TrendingUp } from "lucide-react"
import { MenuItemForm } from "@/components/menu-item-form"

interface MenuItem {
  id: string
  name: string
  category: string
  price: number
  cost: number
  description?: string
  available: boolean
  popularity: number
}

const mockMenuItems: MenuItem[] = [
  {
    id: "1",
    name: "Pizza Margherita",
    category: "Pizzas",
    price: 12.5,
    cost: 4.2,
    description: "Salsa de tomate, mozzarella, albahaca fresca",
    available: true,
    popularity: 95,
  },
  {
    id: "2",
    name: "Pizza Pepperoni",
    category: "Pizzas",
    price: 14.0,
    cost: 4.8,
    description: "Salsa de tomate, mozzarella, pepperoni",
    available: true,
    popularity: 88,
  },
  {
    id: "3",
    name: "Pizza Hawaiana",
    category: "Pizzas",
    price: 15.5,
    cost: 5.2,
    description: "Salsa de tomate, mozzarella, jamón, piña",
    available: true,
    popularity: 72,
  },
  {
    id: "4",
    name: "Pizza Vegetariana",
    category: "Pizzas",
    price: 13.75,
    cost: 4.5,
    description: "Salsa de tomate, mozzarella, pimientos, cebolla, champiñones",
    available: true,
    popularity: 65,
  },
  {
    id: "5",
    name: "Coca Cola 500ml",
    category: "Bebidas",
    price: 2.5,
    cost: 1.2,
    description: "Bebida gaseosa",
    available: true,
    popularity: 90,
  },
  {
    id: "6",
    name: "Sprite 500ml",
    category: "Bebidas",
    price: 2.5,
    cost: 1.2,
    description: "Bebida gaseosa de limón",
    available: true,
    popularity: 75,
  },
]

export default function MenuPage() {
  const [menuItems, setMenuItems] = useState<MenuItem[]>(mockMenuItems)
  const [showForm, setShowForm] = useState(false)
  const [editingItem, setEditingItem] = useState<MenuItem | null>(null)
  const [searchTerm, setSearchTerm] = useState("")

  const filteredItems = menuItems.filter(
    (item) =>
      item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.category.toLowerCase().includes(searchTerm.toLowerCase()),
  )

  const calculateMargin = (price: number, cost: number) => {
    return (((price - cost) / price) * 100).toFixed(1)
  }

  const getMarginColor = (margin: number) => {
    if (margin >= 70) return "text-green-600"
    if (margin >= 50) return "text-yellow-600"
    return "text-red-600"
  }

  const handleEdit = (item: MenuItem) => {
    setEditingItem(item)
    setShowForm(true)
  }

  const handleDelete = (id: string) => {
    setMenuItems(menuItems.filter((item) => item.id !== id))
  }

  const toggleAvailability = (id: string) => {
    setMenuItems(menuItems.map((item) => (item.id === id ? { ...item, available: !item.available } : item)))
  }

  return (
    <div className="flex-1 space-y-4 p-4 md:p-8 pt-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between space-y-2 sm:space-y-0">
        <div className="flex items-center gap-2 sm:gap-4 min-w-0 flex-1">
          <SidebarTrigger className="flex-shrink-0" />
          <div className="min-w-0">
            <h2 className="text-2xl sm:text-3xl font-bold tracking-tight truncate">Gestión de Menú</h2>
            <p className="text-sm text-muted-foreground truncate">Administra los productos y precios de tu pizzería</p>
          </div>
        </div>
        <Button onClick={() => setShowForm(true)} className="flex-shrink-0">
          <Plus className="mr-2 h-4 w-4" />
          Nuevo Producto
        </Button>
      </div>

      <div className="flex gap-4 items-center">
        <div className="flex-1 max-w-sm">
          <Input placeholder="Buscar productos..." value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)} />
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Total Productos</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{menuItems.length}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Productos Activos</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{menuItems.filter((item) => item.available).length}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Precio Promedio</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              ${(menuItems.reduce((sum, item) => sum + item.price, 0) / menuItems.length).toFixed(2)}
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Margen Promedio</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {(
                menuItems.reduce((sum, item) => sum + Number.parseFloat(calculateMargin(item.price, item.cost)), 0) /
                menuItems.length
              ).toFixed(1)}
              %
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Menu Items Grid */}
      <div className="grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
        {filteredItems.map((item) => {
          const margin = Number.parseFloat(calculateMargin(item.price, item.cost))
          return (
            <Card key={item.id} className={!item.available ? "opacity-60" : ""}>
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <CardTitle className="text-lg">{item.name}</CardTitle>
                    <Badge variant="outline" className="mt-1">
                      {item.category}
                    </Badge>
                  </div>
                  <div className="flex gap-1">
                    <Button variant="ghost" size="sm" onClick={() => handleEdit(item)}>
                      <Edit className="h-4 w-4" />
                    </Button>
                    <Button variant="ghost" size="sm" onClick={() => handleDelete(item.id)}>
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                {item.description && <p className="text-sm text-muted-foreground">{item.description}</p>}

                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <div className="flex items-center gap-1 text-muted-foreground">
                      <DollarSign className="h-3 w-3" />
                      Precio
                    </div>
                    <div className="font-bold text-lg">${item.price.toFixed(2)}</div>
                  </div>
                  <div>
                    <div className="flex items-center gap-1 text-muted-foreground">
                      <TrendingUp className="h-3 w-3" />
                      Margen
                    </div>
                    <div className={`font-bold text-lg ${getMarginColor(margin)}`}>{margin}%</div>
                  </div>
                </div>

                <div className="text-sm">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Costo:</span>
                    <span>${item.cost.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Ganancia:</span>
                    <span className="font-medium">${(item.price - item.cost).toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Popularidad:</span>
                    <span>{item.popularity}%</span>
                  </div>
                </div>

                <div className="flex gap-2">
                  <Button
                    variant={item.available ? "default" : "secondary"}
                    size="sm"
                    className="flex-1"
                    onClick={() => toggleAvailability(item.id)}
                  >
                    {item.available ? "Disponible" : "No Disponible"}
                  </Button>
                </div>
              </CardContent>
            </Card>
          )
        })}
      </div>

      {showForm && (
        <MenuItemForm
          item={editingItem}
          onClose={() => {
            setShowForm(false)
            setEditingItem(null)
          }}
          onSave={(item) => {
            if (editingItem) {
              setMenuItems(menuItems.map((mi) => (mi.id === item.id ? item : mi)))
            } else {
              setMenuItems([...menuItems, { ...item, id: Date.now().toString() }])
            }
            setShowForm(false)
            setEditingItem(null)
          }}
        />
      )}
    </div>
  )
}
