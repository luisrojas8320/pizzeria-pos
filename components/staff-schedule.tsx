"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { ChevronLeft, ChevronRight, Plus } from "lucide-react"

interface ScheduleEntry {
  id: string
  staffId: string
  staffName: string
  position: string
  date: string
  startTime: string
  endTime: string
  hours: number
}

const mockSchedule: ScheduleEntry[] = [
  {
    id: "1",
    staffId: "1",
    staffName: "María González",
    position: "Cocinero Principal",
    date: "2024-01-15",
    startTime: "08:00",
    endTime: "16:00",
    hours: 8,
  },
  {
    id: "2",
    staffId: "2",
    staffName: "Carlos Ruiz",
    position: "Ayudante de Cocina",
    date: "2024-01-15",
    startTime: "10:00",
    endTime: "18:00",
    hours: 8,
  },
  {
    id: "3",
    staffId: "3",
    staffName: "Ana López",
    position: "Delivery",
    date: "2024-01-15",
    startTime: "12:00",
    endTime: "20:00",
    hours: 8,
  },
]

export function StaffSchedule() {
  const [currentWeek, setCurrentWeek] = useState(new Date())
  const [schedule, setSchedule] = useState<ScheduleEntry[]>(mockSchedule)

  const getWeekDays = (date: Date) => {
    const week = []
    const startOfWeek = new Date(date)
    startOfWeek.setDate(date.getDate() - date.getDay())

    for (let i = 0; i < 7; i++) {
      const day = new Date(startOfWeek)
      day.setDate(startOfWeek.getDate() + i)
      week.push(day)
    }
    return week
  }

  const weekDays = getWeekDays(currentWeek)
  const dayNames = ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"]

  const getScheduleForDay = (date: Date) => {
    const dateString = date.toISOString().split("T")[0]
    return schedule.filter((entry) => entry.date === dateString)
  }

  const navigateWeek = (direction: "prev" | "next") => {
    const newDate = new Date(currentWeek)
    newDate.setDate(currentWeek.getDate() + (direction === "next" ? 7 : -7))
    setCurrentWeek(newDate)
  }

  const formatDate = (date: Date) => {
    return date.toLocaleDateString("es-EC", {
      day: "numeric",
      month: "short",
    })
  }

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="truncate">Horarios de la Semana</CardTitle>
            <div className="flex items-center gap-2 flex-shrink-0">
              <Button variant="outline" size="sm" onClick={() => navigateWeek("prev")}>
                <ChevronLeft className="h-4 w-4" />
              </Button>
              <span className="text-sm font-medium whitespace-nowrap">
                {formatDate(weekDays[0])} - {formatDate(weekDays[6])}
              </span>
              <Button variant="outline" size="sm" onClick={() => navigateWeek("next")}>
                <ChevronRight className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-7 gap-4">
            {weekDays.map((day, index) => {
              const daySchedule = getScheduleForDay(day)
              const isToday = day.toDateString() === new Date().toDateString()

              return (
                <div key={index} className="space-y-2">
                  <div className="text-center">
                    <div className={`text-sm font-medium ${isToday ? "text-orange-600" : "text-muted-foreground"}`}>
                      {dayNames[index]}
                    </div>
                    <div className={`text-lg ${isToday ? "text-orange-600 font-bold" : ""}`}>{day.getDate()}</div>
                  </div>
                  <div className="space-y-2 min-h-[200px]">
                    {daySchedule.map((entry) => (
                      <div key={entry.id} className="p-2 bg-orange-50 border border-orange-200 rounded text-xs">
                        <div className="font-medium truncate">{entry.staffName}</div>
                        <div className="text-muted-foreground truncate">{entry.position}</div>
                        <div className="font-medium">
                          {entry.startTime} - {entry.endTime}
                        </div>
                        <Badge variant="secondary" className="text-xs">
                          {entry.hours}h
                        </Badge>
                      </div>
                    ))}
                    <Button variant="outline" size="sm" className="w-full h-8 text-xs bg-transparent">
                      <Plus className="h-3 w-3 mr-1" />
                      Agregar
                    </Button>
                  </div>
                </div>
              )
            })}
          </div>
        </CardContent>
      </Card>

      <div className="grid gap-4 grid-cols-1 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="truncate">Resumen Semanal</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex justify-between">
                <span className="text-muted-foreground">Total Horas Programadas:</span>
                <span className="font-medium">156h</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Costo Total:</span>
                <span className="font-medium">$780.00</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Empleados Activos:</span>
                <span className="font-medium">8</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Promedio Horas/Empleado:</span>
                <span className="font-medium">19.5h</span>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="truncate">Alertas de Horarios</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="flex items-start gap-2">
                <Badge variant="destructive" className="text-xs">
                  Crítico
                </Badge>
                <div className="text-sm">
                  <p className="font-medium">Domingo sin cobertura</p>
                  <p className="text-muted-foreground text-xs">No hay personal programado para el domingo</p>
                </div>
              </div>
              <div className="flex items-start gap-2">
                <Badge variant="secondary" className="text-xs bg-yellow-100 text-yellow-800">
                  Advertencia
                </Badge>
                <div className="text-sm">
                  <p className="font-medium">Sobrecarga de horas</p>
                  <p className="text-muted-foreground text-xs">María González: 45h esta semana</p>
                </div>
              </div>
              <div className="flex items-start gap-2">
                <Badge variant="outline" className="text-xs">
                  Info
                </Badge>
                <div className="text-sm">
                  <p className="font-medium">Horario pico cubierto</p>
                  <p className="text-muted-foreground text-xs">12:00-14:00 y 19:00-21:00 bien staffed</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
