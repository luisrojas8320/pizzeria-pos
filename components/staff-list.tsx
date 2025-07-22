"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Phone, Mail, Calendar, DollarSign, Edit, Trash2 } from "lucide-react"

interface StaffMember {
  id: string
  name: string
  phone: string
  email?: string
  position: string
  hourlyRate: number
  startDate: string
  isActive: boolean
  hoursThisWeek: number
  status: "working" | "off" | "break"
}

const mockStaff: StaffMember[] = [
  {
    id: "1",
    name: "María González",
    phone: "0987654321",
    email: "maria@delizzia.com",
    position: "Cocinero Principal",
    hourlyRate: 6.5,
    startDate: "2023-06-15",
    isActive: true,
    hoursThisWeek: 40,
    status: "working",
  },
  {
    id: "2",
    name: "Carlos Ruiz",
    phone: "0987654322",
    position: "Ayudante de Cocina",
    hourlyRate: 4.5,
    startDate: "2023-08-01",
    isActive: true,
    hoursThisWeek: 35,
    status: "working",
  },
  {
    id: "3",
    name: "Ana López",
    phone: "0987654323",
    email: "ana@delizzia.com",
    position: "Delivery",
    hourlyRate: 4.0,
    startDate: "2023-09-10",
    isActive: true,
    hoursThisWeek: 30,
    status: "working",
  },
  {
    id: "4",
    name: "Luis Mendoza",
    phone: "0987654324",
    position: "Cajero",
    hourlyRate: 5.0,
    startDate: "2023-07-20",
    isActive: true,
    hoursThisWeek: 25,
    status: "off",
  },
]

const statusColors = {
  working: "bg-green-100 text-green-800",
  off: "bg-gray-100 text-gray-800",
  break: "bg-yellow-100 text-yellow-800",
}

const statusLabels = {
  working: "Trabajando",
  off: "Libre",
  break: "Descanso",
}

const positionLabels = {
  "cocinero-principal": "Cocinero Principal",
  "ayudante-cocina": "Ayudante de Cocina",
  delivery: "Delivery",
  cajero: "Cajero",
  limpieza: "Limpieza",
  gerente: "Gerente",
}

export function StaffList() {
  const [staff, setStaff] = useState<StaffMember[]>(mockStaff)

  const getInitials = (name: string) => {
    return name
      .split(" ")
      .map((n) => n[0])
      .join("")
      .toUpperCase()
  }

  const calculateWeeklySalary = (hourlyRate: number, hours: number) => {
    return (hourlyRate * hours).toFixed(2)
  }

  return (
    <div className="grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
      {staff.map((member) => (
        <Card key={member.id} className={!member.isActive ? "opacity-60" : ""}>
          <CardHeader className="pb-3">
            <div className="flex items-start justify-between">
              <div className="flex items-center gap-3 min-w-0 flex-1">
                <Avatar>
                  <AvatarFallback>{getInitials(member.name)}</AvatarFallback>
                </Avatar>
                <div className="min-w-0 flex-1">
                  <CardTitle className="text-lg truncate">{member.name}</CardTitle>
                  <p className="text-sm text-muted-foreground truncate">{member.position}</p>
                </div>
              </div>
              <div className="flex gap-1 flex-shrink-0">
                <Button variant="ghost" size="sm">
                  <Edit className="h-4 w-4" />
                </Button>
                <Button variant="ghost" size="sm">
                  <Trash2 className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <Badge className={statusColors[member.status]} variant="secondary">
                {statusLabels[member.status]}
              </Badge>
              <Badge variant={member.isActive ? "default" : "secondary"}>
                {member.isActive ? "Activo" : "Inactivo"}
              </Badge>
            </div>

            <div className="space-y-2 text-sm">
              <div className="flex items-center gap-2">
                <Phone className="h-4 w-4 text-muted-foreground flex-shrink-0" />
                <span className="truncate">{member.phone}</span>
              </div>
              {member.email && (
                <div className="flex items-center gap-2">
                  <Mail className="h-4 w-4 text-muted-foreground flex-shrink-0" />
                  <span className="truncate">{member.email}</span>
                </div>
              )}
              <div className="flex items-center gap-2">
                <Calendar className="h-4 w-4 text-muted-foreground flex-shrink-0" />
                <span className="truncate">Desde: {new Date(member.startDate).toLocaleDateString("es-EC")}</span>
              </div>
              <div className="flex items-center gap-2">
                <DollarSign className="h-4 w-4 text-muted-foreground flex-shrink-0" />
                <span className="truncate">${member.hourlyRate}/hora</span>
              </div>
            </div>

            <div className="border-t pt-3">
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <p className="text-muted-foreground">Horas Semana</p>
                  <p className="font-medium">{member.hoursThisWeek}h</p>
                </div>
                <div>
                  <p className="text-muted-foreground">Salario Semana</p>
                  <p className="font-medium">${calculateWeeklySalary(member.hourlyRate, member.hoursThisWeek)}</p>
                </div>
              </div>
            </div>

            <div className="flex gap-2">
              <Button variant="outline" size="sm" className="flex-1 bg-transparent">
                Ver Horarios
              </Button>
              <Button variant="outline" size="sm" className="flex-1 bg-transparent">
                Editar
              </Button>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
