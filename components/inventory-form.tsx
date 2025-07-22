"use client"

import type React from "react"

import { useState } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import { useToast } from "@/hooks/use-toast"

interface InventoryFormProps {
  onClose: () => void
}

export function InventoryForm({ onClose }: InventoryFormProps) {
  const [formData, setFormData] = useState({
    name: "",
    category: "",
    currentStock: 0,
    minStock: 0,
    maxStock: 0,
    unit: "",
    unitCost: 0,
    supplier: "",
    expiryDate: "",
    notes: "",
  })
  const { toast } = useToast()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!formData.name || !formData.category || !formData.unit || formData.unitCost <= 0) {
      toast({
        title: "Error",
        description: "Complete todos los campos obligatorios",
        variant: "destructive",
      })
      return
    }

    try {

      toast({
        title: "Producto agregado",
        description: `${formData.name} ha sido agregado al inventario`,
      })

      onClose()
    } catch (error) {
      toast({
        title: "Error",
        description: "No se pudo agregar el producto",
        variant: "destructive",
      })
    }
  }

  return (
    <Dialog open={true} onOpenChange={onClose}>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle>Nuevo Producto en Inventario</DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <Label htmlFor="name">Nombre del Producto *</Label>
            <Input
              id="name"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              placeholder="Nombre del producto"
              required
            />
          </div>

          <div>
            <Label htmlFor="category">Categoría *</Label>
            <Select
              value={formData.category}
              onValueChange={(value) => setFormData({ ...formData, category: value })}
              required
            >
              <SelectTrigger>
                <SelectValue placeholder="Seleccionar categoría" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="ingredientes">Ingredientes</SelectItem>
                <SelectItem value="bebidas">Bebidas</SelectItem>
                <SelectItem value="empaques">Empaques</SelectItem>
                <SelectItem value="limpieza">Limpieza</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label htmlFor="unit">Unidad *</Label>
              <Select
                value={formData.unit}
                onValueChange={(value) => setFormData({ ...formData, unit: value })}
                required
              >
                <SelectTrigger>
                  <SelectValue placeholder="Unidad" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="kg">kg</SelectItem>
                  <SelectItem value="litros">litros</SelectItem>
                  <SelectItem value="unidades">unidades</SelectItem>
                  <SelectItem value="cajas">cajas</SelectItem>
                  <SelectItem value="paquetes">paquetes</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label htmlFor="unitCost">Costo Unitario *</Label>
              <Input
                id="unitCost"
                type="number"
                step="0.01"
                min="0"
                value={formData.unitCost}
                onChange={(e) => setFormData({ ...formData, unitCost: Number.parseFloat(e.target.value) || 0 })}
                placeholder="0.00"
                required
              />
            </div>
          </div>

          <div className="grid grid-cols-3 gap-4">
            <div>
              <Label htmlFor="currentStock">Stock Actual</Label>
              <Input
                id="currentStock"
                type="number"
                min="0"
                value={formData.currentStock}
                onChange={(e) => setFormData({ ...formData, currentStock: Number.parseInt(e.target.value) || 0 })}
                placeholder="0"
              />
            </div>
            <div>
              <Label htmlFor="minStock">Stock Mínimo</Label>
              <Input
                id="minStock"
                type="number"
                min="0"
                value={formData.minStock}
                onChange={(e) => setFormData({ ...formData, minStock: Number.parseInt(e.target.value) || 0 })}
                placeholder="0"
              />
            </div>
            <div>
              <Label htmlFor="maxStock">Stock Máximo</Label>
              <Input
                id="maxStock"
                type="number"
                min="0"
                value={formData.maxStock}
                onChange={(e) => setFormData({ ...formData, maxStock: Number.parseInt(e.target.value) || 0 })}
                placeholder="0"
              />
            </div>
          </div>

          <div>
            <Label htmlFor="supplier">Proveedor</Label>
            <Input
              id="supplier"
              value={formData.supplier}
              onChange={(e) => setFormData({ ...formData, supplier: e.target.value })}
              placeholder="Nombre del proveedor"
            />
          </div>

          <div>
            <Label htmlFor="expiryDate">Fecha de Vencimiento</Label>
            <Input
              id="expiryDate"
              type="date"
              value={formData.expiryDate}
              onChange={(e) => setFormData({ ...formData, expiryDate: e.target.value })}
            />
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

          <div className="flex justify-end gap-4">
            <Button type="button" variant="outline" onClick={onClose}>
              Cancelar
            </Button>
            <Button type="submit">Agregar Producto</Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  )
}
