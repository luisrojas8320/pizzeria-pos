"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { SidebarTrigger } from "@/components/ui/sidebar"
import { Plus, Calendar, Clock, Users, UserCheck } from "lucide-react"
import { StaffForm } from "@/components/staff-form"
import { StaffSchedule } from "@/components/staff-schedule"
import { StaffList } from "@/components/staff-list"

export default function StaffPage() {
  const [showStaffForm, setShowStaffForm] = useState(false)
  const [activeTab, setActiveTab] = useState<"list" | "schedule">("list")

  return (
    <div className="flex-1 space-y-4 p-4 md:p-8 pt-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between space-y-2 sm:space-y-0">
        <div className="flex items-center gap-2 sm:gap-4 min-w-0 flex-1">
          <SidebarTrigger className="flex-shrink-0" />
          <div className="min-w-0">
            <h2 className="text-2xl sm:text-3xl font-bold tracking-tight truncate">Gestión de Personal</h2>
            <p className="text-sm text-muted-foreground truncate">Administra el personal y horarios</p>
          </div>
        </div>
        <Button onClick={() => setShowStaffForm(true)} className="flex-shrink-0">
          <Plus className="mr-2 h-4 w-4" />
          Nuevo Empleado
        </Button>
      </div>

      <div className="flex gap-2">
        <Button variant={activeTab === "list" ? "default" : "outline"} onClick={() => setActiveTab("list")} size="sm">
          <Users className="mr-2 h-4 w-4" />
          Personal
        </Button>
        <Button
          variant={activeTab === "schedule" ? "default" : "outline"}
          onClick={() => setActiveTab("schedule")}
          size="sm"
        >
          <Calendar className="mr-2 h-4 w-4" />
          Horarios
        </Button>
      </div>

      <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium flex items-center gap-2">
              <Users className="h-4 w-4" />
              <span className="truncate">Total Empleados</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">8</div>
            <p className="text-xs text-muted-foreground">Activos</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium flex items-center gap-2">
              <UserCheck className="h-4 w-4" />
              <span className="truncate">En Turno</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">4</div>
            <p className="text-xs text-muted-foreground">Trabajando ahora</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium flex items-center gap-2">
              <Clock className="h-4 w-4" />
              <span className="truncate">Horas Semana</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">156</div>
            <p className="text-xs text-muted-foreground">Total programadas</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium truncate">Costo Semanal</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">$780</div>
            <p className="text-xs text-muted-foreground">En salarios</p>
          </CardContent>
        </Card>
      </div>

      {activeTab === "list" ? <StaffList /> : <StaffSchedule />}

      {showStaffForm && <StaffForm onClose={() => setShowStaffForm(false)} />}
    </div>
  )
}
