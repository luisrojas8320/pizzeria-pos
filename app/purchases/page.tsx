"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { SidebarTrigger } from "@/components/ui/sidebar"
import { Plus, Search, Filter, Calendar, Truck } from "lucide-react"
import { PurchaseForm } from "@/components/purchase-form"
import { PurchasesList } from "@/components/purchases-list"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

export default function PurchasesPage() {
  const [showPurchaseForm, setShowPurchaseForm] = useState(false)
  const [searchTerm, setSearchTerm] = useState("")
  const [statusFilter, setStatusFilter] = useState("all")

  return (
    <div className="flex-1 space-y-4 p-4 md:p-8 pt-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between space-y-2 sm:space-y-0">
        <div className="flex items-center gap-2 sm:gap-4 min-w-0 flex-1">
          <SidebarTrigger className="flex-shrink-0" />
          <div className="min-w-0">
            <h2 className="text-2xl sm:text-3xl font-bold tracking-tight truncate">Gestión de Compras</h2>
            <p className="text-sm text-muted-foreground truncate">Administra las compras y proveedores</p>
          </div>
        </div>
        <Button onClick={() => setShowPurchaseForm(true)} className="flex-shrink-0">
          <Plus className="mr-2 h-4 w-4" />
          Nueva Compra
        </Button>
      </div>

      <div className="flex flex-col sm:flex-row gap-4 items-stretch sm:items-center">
        <div className="flex-1 max-w-sm">
          <div className="relative">
            <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Buscar compras..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-8"
            />
          </div>
        </div>
        <Select value={statusFilter} onValueChange={setStatusFilter}>
          <SelectTrigger className="w-full sm:w-[180px]">
            <Filter className="mr-2 h-4 w-4" />
            <SelectValue placeholder="Filtrar por estado" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">Todos los estados</SelectItem>
            <SelectItem value="pending">Pendiente</SelectItem>
            <SelectItem value="ordered">Ordenado</SelectItem>
            <SelectItem value="received">Recibido</SelectItem>
            <SelectItem value="cancelled">Cancelado</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium flex items-center gap-2">
              <Calendar className="h-4 w-4" />
              <span className="truncate">Pendientes</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">5</div>
            <p className="text-xs text-muted-foreground">Órdenes por procesar</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium flex items-center gap-2">
              <Truck className="h-4 w-4" />
              <span className="truncate">En Tránsito</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">3</div>
            <p className="text-xs text-muted-foreground">Esperando entrega</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium truncate">Recibidas Hoy</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">2</div>
            <p className="text-xs text-muted-foreground">Completadas</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium truncate">Total Mes</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">$2,450</div>
            <p className="text-xs text-muted-foreground">En compras</p>
          </CardContent>
        </Card>
      </div>

      <PurchasesList searchTerm={searchTerm} statusFilter={statusFilter} />

      {showPurchaseForm && <PurchaseForm onClose={() => setShowPurchaseForm(false)} />}
    </div>
  )
}
