"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { SidebarTrigger } from "@/components/ui/sidebar"
import { DashboardChart } from "@/components/dashboard-chart"
import { RecentOrders } from "@/components/recent-orders"
import { StockAlerts } from "@/components/stock-alerts"
import { DollarSign, ShoppingBag, TrendingUp, Clock, Users } from "lucide-react"

interface DashboardMetrics {
  dailySales: number
  activeOrders: number
  completedOrders: number
  stockAlerts: number
  staffOnDuty: number
  avgOrderValue: number
}

export default function Dashboard() {
  const [metrics, setMetrics] = useState<DashboardMetrics>({
    dailySales: 0,
    activeOrders: 0,
    completedOrders: 0,
    stockAlerts: 0,
    staffOnDuty: 0,
    avgOrderValue: 0,
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Simulate API call
    const fetchMetrics = async () => {
      try {
        // Mock data - replace with actual API call
        await new Promise((resolve) => setTimeout(resolve, 1000))
        setMetrics({
          dailySales: 1250.75,
          activeOrders: 8,
          completedOrders: 45,
          stockAlerts: 3,
          staffOnDuty: 4,
          avgOrderValue: 27.8,
        })
      } catch (error) {
      } finally {
        setLoading(false)
      }
    }

    fetchMetrics()

    // Set up real-time updates
    const interval = setInterval(fetchMetrics, 30000) // Update every 30 seconds
    return () => clearInterval(interval)
  }, [])

  const currentTime = new Date().toLocaleString("es-EC", {
    timeZone: "America/Guayaquil",
    dateStyle: "full",
    timeStyle: "short",
  })

  return (
    <div className="flex-1 space-y-4 p-4 md:p-8 pt-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between space-y-2 sm:space-y-0">
        <div className="flex items-center gap-2 sm:gap-4 min-w-0 flex-1">
          <SidebarTrigger className="flex-shrink-0" />
          <div className="min-w-0">
            <h2 className="text-2xl sm:text-3xl font-bold tracking-tight truncate">Dashboard</h2>
            <p className="text-sm text-muted-foreground truncate">{currentTime}</p>
          </div>
        </div>
        <div className="flex items-center space-x-2 flex-shrink-0">
          <Badge variant="outline" className="text-green-600">
            <div className="w-2 h-2 bg-green-500 rounded-full mr-2" />
            Sistema Activo
          </Badge>
        </div>
      </div>

      <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Ventas del Día</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">${loading ? "..." : metrics.dailySales.toFixed(2)}</div>
            <p className="text-xs text-muted-foreground">+12.5% desde ayer</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Pedidos Activos</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{loading ? "..." : metrics.activeOrders}</div>
            <p className="text-xs text-muted-foreground">En preparación</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Pedidos Completados</CardTitle>
            <ShoppingBag className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{loading ? "..." : metrics.completedOrders}</div>
            <p className="text-xs text-muted-foreground">Hoy</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Valor Promedio</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">${loading ? "..." : metrics.avgOrderValue.toFixed(2)}</div>
            <p className="text-xs text-muted-foreground">Por pedido</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-4 grid-cols-1 lg:grid-cols-7">
        <Card className="lg:col-span-4">
          <CardHeader>
            <CardTitle className="truncate">Ventas por Hora</CardTitle>
          </CardHeader>
          <CardContent className="pl-2">
            <DashboardChart />
          </CardContent>
        </Card>
        <Card className="lg:col-span-3">
          <CardHeader>
            <CardTitle className="truncate">Pedidos Recientes</CardTitle>
          </CardHeader>
          <CardContent>
            <RecentOrders />
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <StockAlerts />
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle>Personal en Turno</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium">María González</p>
                  <p className="text-sm text-muted-foreground">Cocinera Principal</p>
                </div>
                <Badge variant="secondary">Activa</Badge>
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium">Carlos Ruiz</p>
                  <p className="text-sm text-muted-foreground">Ayudante de Cocina</p>
                </div>
                <Badge variant="secondary">Activo</Badge>
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium">Ana López</p>
                  <p className="text-sm text-muted-foreground">Delivery</p>
                </div>
                <Badge variant="secondary">En Ruta</Badge>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
