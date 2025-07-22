"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import { Switch } from "@/components/ui/switch"
import { useToast } from "@/hooks/use-toast"

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

interface MenuItemFormProps {
  item?: MenuItem | null
  onClose: () => void
  onSave: (item: MenuItem) => void
}

export function MenuItemForm({ item, onClose, onSave }: MenuItemFormProps) {
  const [formData, setFormData] = useState({
    name: "",
    category: "",
    price: 0,
    cost: 0,
    description: "",
    available: true,
    popularity: 0,
  })
  const { toast } = useToast()

  useEffect(() => {
    if (item) {
      setFormData({
        name: item.name,
        category: item.category,
        price: item.price,
        cost: item.cost,
        description: item.description || "",
        available: item.available,
        popularity: item.popularity,
      })
    }
  }, [item])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    if (!formData.name || !formData.category || formData.price <= 0 || formData.cost <= 0) {
      toast({
        title: "Error",
        description: "Complete todos los campos obligatorios",
        variant: "destructive",
      })
      return
    }

    if (formData.cost >= formData.price) {
      toast({
        title: "Error",
        description: "El costo no puede ser mayor o igual al precio",
        variant: "destructive",
      })
      return
    }

    const newItem: MenuItem = {
      id: item?.id || Date.now().toString(),
      ...formData,
    }

    onSave(newItem)

    toast({
      title: item ? "Producto actualizado" : "Producto creado",
      description: `${formData.name} ${item ? "actualizado" : "creado"} exitosamente`,
    })
  }

  const calculateMargin = () => {
    if (formData.price > 0 && formData.cost > 0) {
      return (((formData.price - formData.cost) / formData.price) * 100).toFixed(1)
    }
    return "0.0"
  }

  return (
    <Dialog open={true} onOpenChange={onClose}>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle>{item ? "Editar Producto" : "Nuevo Producto"}</DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <Label htmlFor="name">Nombre *</Label>
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
                <SelectItem value="Pizzas">Pizzas</SelectItem>
                <SelectItem value="Bebidas">Bebidas</SelectItem>
                <SelectItem value="Entradas">Entradas</SelectItem>
                <SelectItem value="Postres">Postres</SelectItem>
                <SelectItem value="Extras">Extras</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label htmlFor="price">Precio de Venta *</Label>
              <Input
                id="price"
                type="number"
                step="0.01"
                min="0"
                value={formData.price}
                onChange={(e) => setFormData({ ...formData, price: Number.parseFloat(e.target.value) || 0 })}
                placeholder="0.00"
                required
              />
            </div>
            <div>
              <Label htmlFor="cost">Costo *</Label>
              <Input
                id="cost"
                type="number"
                step="0.01"
                min="0"
                value={formData.cost}
                onChange={(e) => setFormData({ ...formData, cost: Number.parseFloat(e.target.value) || 0 })}
                placeholder="0.00"
                required
              />
            </div>
          </div>

          {formData.price > 0 && formData.cost > 0 && (
            <div className="p-3 bg-muted rounded-lg">
              <div className="text-sm text-muted-foreground">Análisis de Rentabilidad</div>
              <div className="grid grid-cols-2 gap-4 mt-2 text-sm">
                <div>
                  <span className="text-muted-foreground">Ganancia:</span>
                  <span className="ml-2 font-medium">${(formData.price - formData.cost).toFixed(2)}</span>
                </div>
                <div>
                  <span className="text-muted-foreground">Margen:</span>
                  <span className="ml-2 font-medium">{calculateMargin()}%</span>
                </div>
              </div>
            </div>
          )}

          <div>
            <Label htmlFor="description">Descripción</Label>
            <Textarea
              id="description"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              placeholder="Descripción del producto..."
              rows={3}
            />
          </div>

          <div>
            <Label htmlFor="popularity">Popularidad (%)</Label>
            <Input
              id="popularity"
              type="number"
              min="0"
              max="100"
              value={formData.popularity}
              onChange={(e) => setFormData({ ...formData, popularity: Number.parseInt(e.target.value) || 0 })}
              placeholder="0"
            />
          </div>

          <div className="flex items-center space-x-2">
            <Switch
              id="available"
              checked={formData.available}
              onCheckedChange={(checked) => setFormData({ ...formData, available: checked })}
            />
            <Label htmlFor="available">Producto disponible</Label>
          </div>

          <div className="flex justify-end gap-4">
            <Button type="button" variant="outline" onClick={onClose}>
              Cancelar
            </Button>
            <Button type="submit">{item ? "Actualizar" : "Crear"} Producto</Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  )
}
