"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { SidebarTrigger } from "@/components/ui/sidebar"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { TrendingUp, TrendingDown, Calendar, Target, Users, DollarSign } from "lucide-react"
import { AnalyticsChart } from "@/components/analytics-chart"
import { PredictionsChart } from "@/components/predictions-chart"
import { Badge } from "@/components/ui/badge"

export default function AnalyticsPage() {
  const [timeRange, setTimeRange] = useState("30d")

  return (
    <div className="flex-1 space-y-4 p-4 md:p-8 pt-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between space-y-2 sm:space-y-0">
        <div className="flex items-center gap-2 sm:gap-4 min-w-0 flex-1">
          <SidebarTrigger className="flex-shrink-0" />
          <div className="min-w-0">
            <h2 className="text-2xl sm:text-3xl font-bold tracking-tight truncate">Análisis Avanzado</h2>
            <p className="text-sm text-muted-foreground truncate">Insights y predicciones para tu pizzería</p>
          </div>
        </div>
        <Select value={timeRange} onValueChange={setTimeRange}>
          <SelectTrigger className="w-full sm:w-[180px]">
            <SelectValue placeholder="Período" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="7d">Últimos 7 días</SelectItem>
            <SelectItem value="30d">Últimos 30 días</SelectItem>
            <SelectItem value="90d">Últimos 90 días</SelectItem>
            <SelectItem value="1y">Último año</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* KPI Cards */}
      <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium flex items-center gap-2">
              <TrendingUp className="h-4 w-4 text-green-500" />
              <span className="truncate">Crecimiento Ventas</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">+18.5%</div>
            <p className="text-xs text-muted-foreground">vs período anterior</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium flex items-center gap-2">
              <Users className="h-4 w-4 text-blue-500" />
              <span className="truncate">Retención Clientes</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-blue-600">72%</div>
            <p className="text-xs text-muted-foreground">Clientes que regresan</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium flex items-center gap-2">
              <Target className="h-4 w-4 text-purple-500" />
              <span className="truncate">Eficiencia Operativa</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-purple-600">89%</div>
            <p className="text-xs text-muted-foreground">Tiempo promedio entrega</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium flex items-center gap-2">
              <DollarSign className="h-4 w-4 text-orange-500" />
              <span className="truncate">ROI Marketing</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-orange-600">3.2x</div>
            <p className="text-xs text-muted-foreground">Retorno inversión</p>
          </CardContent>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid gap-4 grid-cols-1 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="truncate">Tendencias de Consumo</CardTitle>
          </CardHeader>
          <CardContent>
            <AnalyticsChart />
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle className="truncate">Predicciones de Demanda</CardTitle>
          </CardHeader>
          <CardContent>
            <PredictionsChart />
          </CardContent>
        </Card>
      </div>

      {/* Insights Cards */}
      <div className="grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <Calendar className="h-5 w-5 text-blue-500" />
              <span className="truncate">Patrones Estacionales</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm">Viernes - Domingo</span>
                <Badge className="bg-green-100 text-green-800">+45% ventas</Badge>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm">Días de quincena</span>
                <Badge className="bg-blue-100 text-blue-800">+28% pedidos</Badge>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm">Días festivos</span>
                <Badge className="bg-purple-100 text-purple-800">+65% demanda</Badge>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm">Época escolar</span>
                <Badge className="bg-orange-100 text-orange-800">+20% familias</Badge>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <TrendingUp className="h-5 w-5 text-green-500" />
              <span className="truncate">Oportunidades</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-3">
              <div className="p-3 bg-green-50 border border-green-200 rounded-lg">
                <p className="text-sm font-medium text-green-800">Horario Extendido</p>
                <p className="text-xs text-green-600">Abrir hasta las 23:00 podría generar +15% ingresos</p>
              </div>
              <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg">
                <p className="text-sm font-medium text-blue-800">Menú Desayunos</p>
                <p className="text-xs text-blue-600">Demanda matutina sin atender: 8:00-11:00</p>
              </div>
              <div className="p-3 bg-purple-50 border border-purple-200 rounded-lg">
                <p className="text-sm font-medium text-purple-800">Programa Lealtad</p>
                <p className="text-xs text-purple-600">72% clientes frecuentes sin incentivos</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <TrendingDown className="h-5 w-5 text-red-500" />
              <span className="truncate">Áreas de Mejora</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-3">
              <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-sm font-medium text-red-800">Tiempo de Entrega</p>
                <p className="text-xs text-red-600">Promedio 35 min, objetivo: 25 min</p>
              </div>
              <div className="p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                <p className="text-sm font-medium text-yellow-800">Desperdicio Ingredientes</p>
                <p className="text-xs text-yellow-600">8% desperdicio, reducir a 5%</p>
              </div>
              <div className="p-3 bg-orange-50 border border-orange-200 rounded-lg">
                <p className="text-sm font-medium text-orange-800">Satisfacción Cliente</p>
                <p className="text-xs text-orange-600">15% quejas por temperatura de entrega</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Recommendations */}
      <Card>
        <CardHeader>
          <CardTitle className="truncate">Recomendaciones Personalizadas para Ibarra</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 grid-cols-1 md:grid-cols-2">
            <div className="space-y-4">
              <h4 className="font-medium text-sm text-muted-foreground">ESTRATEGIAS LOCALES</h4>
              <div className="space-y-3">
                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0" />
                  <div>
                    <p className="text-sm font-medium">Promociones Universitarias</p>
                    <p className="text-xs text-muted-foreground">
                      Descuentos para estudiantes de UTN e PUCE en horarios de almuerzo
                    </p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-green-500 rounded-full mt-2 flex-shrink-0" />
                  <div>
                    <p className="text-sm font-medium">Alianzas Empresariales</p>
                    <p className="text-xs text-muted-foreground">
                      Convenios con empresas locales para almuerzos corporativos
                    </p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-purple-500 rounded-full mt-2 flex-shrink-0" />
                  <div>
                    <p className="text-sm font-medium">Eventos Culturales</p>
                    <p className="text-xs text-muted-foreground">Participar en festivales y eventos de la ciudad</p>
                  </div>
                </div>
              </div>
            </div>
            <div className="space-y-4">
              <h4 className="font-medium text-sm text-muted-foreground">OPTIMIZACIONES OPERATIVAS</h4>
              <div className="space-y-3">
                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-orange-500 rounded-full mt-2 flex-shrink-0" />
                  <div>
                    <p className="text-sm font-medium">Gestión de Inventario</p>
                    <p className="text-xs text-muted-foreground">
                      Implementar sistema de reorden automático basado en demanda
                    </p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-red-500 rounded-full mt-2 flex-shrink-0" />
                  <div>
                    <p className="text-sm font-medium">Capacitación Personal</p>
                    <p className="text-xs text-muted-foreground">
                      Entrenar equipo en técnicas de preparación más eficientes
                    </p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-yellow-500 rounded-full mt-2 flex-shrink-0" />
                  <div>
                    <p className="text-sm font-medium">Marketing Digital</p>
                    <p className="text-xs text-muted-foreground">
                      Aumentar presencia en redes sociales y Google My Business
                    </p>
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
