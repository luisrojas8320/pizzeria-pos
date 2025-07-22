"use client"

import type React from "react"

import { useState } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import { Switch } from "@/components/ui/switch"
import { useToast } from "@/hooks/use-toast"

interface StaffFormProps {
  onClose: () => void
}

export function StaffForm({ onClose }: StaffFormProps) {
  const [formData, setFormData] = useState({
    name: "",
    phone: "",
    email: "",
    position: "",
    hourlyRate: 0,
    startDate: "",
    isActive: true,
    notes: "",
  })
  const { toast } = useToast()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!formData.name || !formData.phone || !formData.position || formData.hourlyRate <= 0) {
      toast({
        title: "Error",
        description: "Complete todos los campos obligatorios",
        variant: "destructive",
      })
      return
    }

    try {

      toast({
        title: "Empleado agregado",
        description: `${formData.name} ha sido agregado al personal`,
      })

      onClose()
    } catch (error) {
      toast({
        title: "Error",
        description: "No se pudo agregar el empleado",
        variant: "destructive",
      })
    }
  }

  return (
    <Dialog open={true} onOpenChange={onClose}>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle>Nuevo Empleado</DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <Label htmlFor="name">Nombre Completo *</Label>
            <Input
              id="name"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              placeholder="Nombre del empleado"
              required
            />
          </div>

          <div>
            <Label htmlFor="phone">Teléfono *</Label>
            <Input
              id="phone"
              value={formData.phone}
              onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
              placeholder="Número de teléfono"
              required
            />
          </div>

          <div>
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              placeholder="Correo electrónico"
            />
          </div>

          <div>
            <Label htmlFor="position">Posición *</Label>
            <Select
              value={formData.position}
              onValueChange={(value) => setFormData({ ...formData, position: value })}
              required
            >
              <SelectTrigger>
                <SelectValue placeholder="Seleccionar posición" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="cocinero-principal">Cocinero Principal</SelectItem>
                <SelectItem value="ayudante-cocina">Ayudante de Cocina</SelectItem>
                <SelectItem value="delivery">Delivery</SelectItem>
                <SelectItem value="cajero">Cajero</SelectItem>
                <SelectItem value="limpieza">Limpieza</SelectItem>
                <SelectItem value="gerente">Gerente</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label htmlFor="hourlyRate">Tarifa por Hora *</Label>
              <Input
                id="hourlyRate"
                type="number"
                step="0.01"
                min="0"
                value={formData.hourlyRate}
                onChange={(e) => setFormData({ ...formData, hourlyRate: Number.parseFloat(e.target.value) || 0 })}
                placeholder="0.00"
                required
              />
            </div>
            <div>
              <Label htmlFor="startDate">Fecha de Inicio</Label>
              <Input
                id="startDate"
                type="date"
                value={formData.startDate}
                onChange={(e) => setFormData({ ...formData, startDate: e.target.value })}
              />
            </div>
          </div>

          <div>
            <Label htmlFor="notes">Notas</Label>
            <Textarea
              id="notes"
              value={formData.notes}
              onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
              placeholder="Información adicional..."
              rows={3}
            />
          </div>

          <div className="flex items-center space-x-2">
            <Switch
              id="isActive"
              checked={formData.isActive}
              onCheckedChange={(checked) => setFormData({ ...formData, isActive: checked })}
            />
            <Label htmlFor="isActive">Empleado activo</Label>
          </div>

          <div className="flex justify-end gap-4">
            <Button type="button" variant="outline" onClick={onClose}>
              Cancelar
            </Button>
            <Button type="submit">Agregar Empleado</Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  )
}
