"use client"

import type React from "react"

import { useState } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Plus, X } from "lucide-react"
import { useToast } from "@/hooks/use-toast"

interface PurchaseItem {
  id: string
  name: string
  quantity: number
  unit: string
  unitCost: number
  total: number
}

interface PurchaseFormProps {
  onClose: () => void
}

const suppliers = [
  { id: "1", name: "Distribuidora La Esperanza", contact: "0987654321" },
  { id: "2", name: "Alimentos del Norte", contact: "0987654322" },
  { id: "3", name: "Proveedora San Miguel", contact: "0987654323" },
]

const commonItems = [
  { name: "Queso Mozzarella", unit: "kg" },
  { name: "Masa para Pizza", unit: "unidades" },
  { name: "Salsa de Tomate", unit: "litros" },
  { name: "Pepperoni", unit: "kg" },
  { name: "Jamón", unit: "kg" },
  { name: "Piña", unit: "kg" },
  { name: "Champiñones", unit: "kg" },
  { name: "Pimientos", unit: "kg" },
]

export function PurchaseForm({ onClose }: PurchaseFormProps) {
  const [purchaseItems, setPurchaseItems] = useState<PurchaseItem[]>([])
  const [supplier, setSupplier] = useState("")
  const [deliveryDate, setDeliveryDate] = useState("")
  const [notes, setNotes] = useState("")
  const { toast } = useToast()

  const addItem = () => {
    const newItem: PurchaseItem = {
      id: Date.now().toString(),
      name: "",
      quantity: 1,
      unit: "kg",
      unitCost: 0,
      total: 0,
    }
    setPurchaseItems([...purchaseItems, newItem])
  }

  const updateItem = (id: string, field: keyof PurchaseItem, value: any) => {
    setPurchaseItems(
      purchaseItems.map((item) => {
        if (item.id === id) {
          const updatedItem = { ...item, [field]: value }
          if (field === "quantity" || field === "unitCost") {
            updatedItem.total = updatedItem.quantity * updatedItem.unitCost
          }
          return updatedItem
        }
        return item
      }),
    )
  }

  const removeItem = (id: string) => {
    setPurchaseItems(purchaseItems.filter((item) => item.id !== id))
  }

  const calculateTotal = () => {
    return purchaseItems.reduce((total, item) => total + item.total, 0)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!supplier || purchaseItems.length === 0 || !deliveryDate) {
      toast({
        title: "Error",
        description: "Complete todos los campos obligatorios",
        variant: "destructive",
      })
      return
    }

    try {
      const purchaseData = {
        supplier,
        deliveryDate,
        notes,
        items: purchaseItems,
        total: calculateTotal(),
        createdAt: new Date().toISOString(),
        status: "pending",
      }


      toast({
        title: "Orden de compra creada",
        description: "La orden de compra se ha creado exitosamente",
      })

      onClose()
    } catch (error) {
      toast({
        title: "Error",
        description: "No se pudo crear la orden de compra",
        variant: "destructive",
      })
    }
  }

  return (
    <Dialog open={true} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Nueva Orden de Compra</DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Información General</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="supplier">Proveedor *</Label>
                  <Select value={supplier} onValueChange={setSupplier} required>
                    <SelectTrigger>
                      <SelectValue placeholder="Seleccionar proveedor" />
                    </SelectTrigger>
                    <SelectContent>
                      {suppliers.map((sup) => (
                        <SelectItem key={sup.id} value={sup.id}>
                          {sup.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="deliveryDate">Fecha de Entrega *</Label>
                  <Input
                    id="deliveryDate"
                    type="date"
                    value={deliveryDate}
                    onChange={(e) => setDeliveryDate(e.target.value)}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="notes">Notas</Label>
                  <Textarea
                    id="notes"
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                    placeholder="Instrucciones especiales..."
                    rows={4}
                  />
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Productos Comunes</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 gap-2 max-h-64 overflow-y-auto">
                  {commonItems.map((item, index) => (
                    <Button
                      key={index}
                      type="button"
                      variant="outline"
                      size="sm"
                      onClick={() => {
                        const newItem: PurchaseItem = {
                          id: Date.now().toString(),
                          name: item.name,
                          quantity: 1,
                          unit: item.unit,
                          unitCost: 0,
                          total: 0,
                        }
                        setPurchaseItems([...purchaseItems, newItem])
                      }}
                      className="justify-start text-left"
                    >
                      <Plus className="h-4 w-4 mr-2" />
                      {item.name} ({item.unit})
                    </Button>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <CardTitle className="text-lg">Productos a Comprar</CardTitle>
              <Button type="button" onClick={addItem} size="sm">
                <Plus className="h-4 w-4 mr-2" />
                Agregar Producto
              </Button>
            </CardHeader>
            <CardContent>
              {purchaseItems.length === 0 ? (
                <p className="text-center text-muted-foreground py-8">
                  No hay productos agregados. Haga clic en "Agregar Producto" para comenzar.
                </p>
              ) : (
                <div className="space-y-4">
                  {purchaseItems.map((item) => (
                    <div key={item.id} className="grid grid-cols-1 md:grid-cols-6 gap-4 p-4 border rounded-lg">
                      <div className="md:col-span-2">
                        <Label>Producto</Label>
                        <Input
                          value={item.name}
                          onChange={(e) => updateItem(item.id, "name", e.target.value)}
                          placeholder="Nombre del producto"
                        />
                      </div>
                      <div>
                        <Label>Cantidad</Label>
                        <Input
                          type="number"
                          min="1"
                          value={item.quantity}
                          onChange={(e) => updateItem(item.id, "quantity", Number.parseInt(e.target.value) || 1)}
                        />
                      </div>
                      <div>
                        <Label>Unidad</Label>
                        <Select value={item.unit} onValueChange={(value) => updateItem(item.id, "unit", value)}>
                          <SelectTrigger>
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="kg">kg</SelectItem>
                            <SelectItem value="litros">litros</SelectItem>
                            <SelectItem value="unidades">unidades</SelectItem>
                            <SelectItem value="cajas">cajas</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      <div>
                        <Label>Costo Unitario</Label>
                        <Input
                          type="number"
                          step="0.01"
                          min="0"
                          value={item.unitCost}
                          onChange={(e) => updateItem(item.id, "unitCost", Number.parseFloat(e.target.value) || 0)}
                        />
                      </div>
                      <div className="flex items-end gap-2">
                        <div className="flex-1">
                          <Label>Total</Label>
                          <div className="text-lg font-bold">${item.total.toFixed(2)}</div>
                        </div>
                        <Button type="button" variant="ghost" size="sm" onClick={() => removeItem(item.id)}>
                          <X className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  ))}
                  <div className="border-t pt-4">
                    <div className="flex justify-between items-center text-lg font-bold">
                      <span>Total de la Orden:</span>
                      <span>${calculateTotal().toFixed(2)}</span>
                    </div>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          <div className="flex justify-end gap-4">
            <Button type="button" variant="outline" onClick={onClose}>
              Cancelar
            </Button>
            <Button type="submit">Crear Orden de Compra</Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  )
}
