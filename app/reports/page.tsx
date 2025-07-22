"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { DatePickerWithRange } from "@/components/date-picker-range"
import { SidebarTrigger } from "@/components/ui/sidebar"
import { SalesChart } from "@/components/sales-chart"
import { ProductsChart } from "@/components/products-chart"
import { PlatformChart } from "@/components/platform-chart"
import { FileText, Table } from "lucide-react"
import { addDays } from "date-fns"
import type { DateRange } from "react-day-picker"

export default function ReportsPage() {
  const [dateRange, setDateRange] = useState<DateRange | undefined>({
    from: addDays(new Date(), -30),
    to: new Date(),
  })
  const [reportType, setReportType] = useState("sales")

  const handleExportPDF = () => {
    // Implementation for PDF export
  }

  const handleExportExcel = () => {
    // Implementation for Excel export
  }

  return (
    <div className="flex-1 space-y-4 p-4 md:p-8 pt-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between space-y-2 sm:space-y-0">
        <div className="flex items-center gap-2 sm:gap-4 min-w-0 flex-1">
          <SidebarTrigger className="flex-shrink-0" />
          <div className="min-w-0">
            <h2 className="text-2xl sm:text-3xl font-bold tracking-tight truncate">Reportes y Análisis</h2>
            <p className="text-sm text-muted-foreground truncate">Visualiza el rendimiento de tu pizzería</p>
          </div>
        </div>
        <div className="flex gap-2 flex-shrink-0">
          <Button variant="outline" onClick={handleExportPDF}>
            <FileText className="mr-2 h-4 w-4" />
            <span className="hidden sm:inline">Exportar </span>PDF
          </Button>
          <Button variant="outline" onClick={handleExportExcel}>
            <Table className="mr-2 h-4 w-4" />
            <span className="hidden sm:inline">Exportar </span>Excel
          </Button>
        </div>
      </div>

      <div className="flex flex-col sm:flex-row gap-4 items-stretch sm:items-center">
        <Select value={reportType} onValueChange={setReportType}>
          <SelectTrigger className="w-full sm:w-[200px]">
            <SelectValue placeholder="Tipo de reporte" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="sales">Ventas</SelectItem>
            <SelectItem value="products">Productos</SelectItem>
            <SelectItem value="platforms">Plataformas</SelectItem>
            <SelectItem value="customers">Clientes</SelectItem>
          </SelectContent>
        </Select>
        <DatePickerWithRange date={dateRange} setDate={setDateRange} />
      </div>

      {/* Summary Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Ventas Totales</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">$12,450.75</div>
            <p className="text-xs text-muted-foreground">+15.2% vs período anterior</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Pedidos Totales</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">847</div>
            <p className="text-xs text-muted-foreground">+8.1% vs período anterior</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Ticket Promedio</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">$14.70</div>
            <p className="text-xs text-muted-foreground">+2.3% vs período anterior</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Margen de Ganancia</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">68.5%</div>
            <p className="text-xs text-muted-foreground">+1.2% vs período anterior</p>
          </CardContent>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid gap-4 md:grid-cols-2">
        <Card className="col-span-2">
          <CardHeader>
            <CardTitle>Ventas por Día</CardTitle>
          </CardHeader>
          <CardContent>
            <SalesChart />
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Productos Más Vendidos</CardTitle>
          </CardHeader>
          <CardContent>
            <ProductsChart />
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Ventas por Plataforma</CardTitle>
          </CardHeader>
          <CardContent>
            <PlatformChart />
          </CardContent>
        </Card>
      </div>

      {/* Detailed Tables */}
      <Card>
        <CardHeader>
          <CardTitle>Resumen Detallado</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
              <div>
                <h4 className="font-medium mb-2">Top 5 Productos</h4>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span>Pizza Margherita</span>
                    <span className="font-medium">156 vendidas</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Pizza Pepperoni</span>
                    <span className="font-medium">134 vendidas</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Pizza Hawaiana</span>
                    <span className="font-medium">98 vendidas</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Pizza Vegetariana</span>
                    <span className="font-medium">87 vendidas</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Coca Cola 500ml</span>
                    <span className="font-medium">245 vendidas</span>
                  </div>
                </div>
              </div>
              <div>
                <h4 className="font-medium mb-2">Horarios Pico</h4>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span>12:00 - 14:00</span>
                    <span className="font-medium">35% ventas</span>
                  </div>
                  <div className="flex justify-between">
                    <span>19:00 - 21:00</span>
                    <span className="font-medium">28% ventas</span>
                  </div>
                  <div className="flex justify-between">
                    <span>18:00 - 19:00</span>
                    <span className="font-medium">15% ventas</span>
                  </div>
                  <div className="flex justify-between">
                    <span>21:00 - 22:00</span>
                    <span className="font-medium">12% ventas</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Otros horarios</span>
                    <span className="font-medium">10% ventas</span>
                  </div>
                </div>
              </div>
              <div>
                <h4 className="font-medium mb-2">Métodos de Pago</h4>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span>Efectivo</span>
                    <span className="font-medium">45% pedidos</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Tarjeta</span>
                    <span className="font-medium">25% pedidos</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Plataforma</span>
                    <span className="font-medium">20% pedidos</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Transferencia</span>
                    <span className="font-medium">10% pedidos</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
