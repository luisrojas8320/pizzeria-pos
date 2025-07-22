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
import { Badge } from "@/components/ui/badge"
import { Plus, Minus, X } from "lucide-react"
import { useToast } from "@/hooks/use-toast"

interface OrderItem {
  id: string
  name: string
  price: number
  quantity: number
  notes?: string
}

interface OrderFormProps {
  onClose: () => void
}

const menuItems = [
  { id: "1", name: "Pizza Margherita", price: 12.5, category: "Pizzas" },
  { id: "2", name: "Pizza Pepperoni", price: 14.0, category: "Pizzas" },
  { id: "3", name: "Pizza Hawaiana", price: 15.5, category: "Pizzas" },
  { id: "4", name: "Pizza Vegetariana", price: 13.75, category: "Pizzas" },
  { id: "5", name: "Coca Cola 500ml", price: 2.5, category: "Bebidas" },
  { id: "6", name: "Sprite 500ml", price: 2.5, category: "Bebidas" },
  { id: "7", name: "Agua 500ml", price: 1.5, category: "Bebidas" },
]

export function OrderForm({ onClose }: OrderFormProps) {
  const [orderItems, setOrderItems] = useState<OrderItem[]>([])
  const [customerName, setCustomerName] = useState("")
  const [customerPhone, setCustomerPhone] = useState("")
  const [customerAddress, setCustomerAddress] = useState("")
  const [paymentMethod, setPaymentMethod] = useState("")
  const [platform, setPlatform] = useState("")
  const [notes, setNotes] = useState("")
  const { toast } = useToast()

  const addItem = (menuItem: (typeof menuItems)[0]) => {
    const existingItem = orderItems.find((item) => item.id === menuItem.id)
    if (existingItem) {
      setOrderItems(
        orderItems.map((item) => (item.id === menuItem.id ? { ...item, quantity: item.quantity + 1 } : item)),
      )
    } else {
      setOrderItems([
        ...orderItems,
        {
          id: menuItem.id,
          name: menuItem.name,
          price: menuItem.price,
          quantity: 1,
        },
      ])
    }
  }

  const updateQuantity = (id: string, quantity: number) => {
    if (quantity <= 0) {
      setOrderItems(orderItems.filter((item) => item.id !== id))
    } else {
      setOrderItems(orderItems.map((item) => (item.id === id ? { ...item, quantity } : item)))
    }
  }

  const removeItem = (id: string) => {
    setOrderItems(orderItems.filter((item) => item.id !== id))
  }

  const calculateTotal = () => {
    return orderItems.reduce((total, item) => total + item.price * item.quantity, 0)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (orderItems.length === 0) {
      toast({
        title: "Error",
        description: "Debe agregar al menos un producto al pedido",
        variant: "destructive",
      })
      return
    }

    if (!customerName || !paymentMethod || !platform) {
      toast({
        title: "Error",
        description: "Complete todos los campos obligatorios",
        variant: "destructive",
      })
      return
    }

    try {
      // Here you would make the API call to create the order
      const orderData = {
        customerName,
        customerPhone,
        customerAddress,
        paymentMethod,
        platform,
        notes,
        items: orderItems,
        total: calculateTotal(),
        createdAt: new Date().toISOString(),
      }


      toast({
        title: "Pedido creado",
        description: `Pedido para ${customerName} creado exitosamente`,
      })

      onClose()
    } catch (error) {
      toast({
        title: "Error",
        description: "No se pudo crear el pedido",
        variant: "destructive",
      })
    }
  }

  return (
    <Dialog open={true} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Nuevo Pedido</DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Customer Information */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Información del Cliente</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="customerName">Nombre *</Label>
                  <Input
                    id="customerName"
                    value={customerName}
                    onChange={(e) => setCustomerName(e.target.value)}
                    placeholder="Nombre del cliente"
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="customerPhone">Teléfono</Label>
                  <Input
                    id="customerPhone"
                    value={customerPhone}
                    onChange={(e) => setCustomerPhone(e.target.value)}
                    placeholder="Número de teléfono"
                  />
                </div>
                <div>
                  <Label htmlFor="customerAddress">Dirección</Label>
                  <Textarea
                    id="customerAddress"
                    value={customerAddress}
                    onChange={(e) => setCustomerAddress(e.target.value)}
                    placeholder="Dirección de entrega"
                    rows={3}
                  />
                </div>
              </CardContent>
            </Card>

            {/* Order Details */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Detalles del Pedido</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="platform">Plataforma *</Label>
                  <Select value={platform} onValueChange={setPlatform} required>
                    <SelectTrigger>
                      <SelectValue placeholder="Seleccionar plataforma" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="presencial">Presencial</SelectItem>
                      <SelectItem value="uber-eats">Uber Eats</SelectItem>
                      <SelectItem value="pedidos-ya">Pedidos Ya</SelectItem>
                      <SelectItem value="bis">Bis</SelectItem>
                      <SelectItem value="telefono">Teléfono</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="paymentMethod">Método de Pago *</Label>
                  <Select value={paymentMethod} onValueChange={setPaymentMethod} required>
                    <SelectTrigger>
                      <SelectValue placeholder="Seleccionar método de pago" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="efectivo">Efectivo</SelectItem>
                      <SelectItem value="tarjeta">Tarjeta</SelectItem>
                      <SelectItem value="transferencia">Transferencia</SelectItem>
                      <SelectItem value="plataforma">Pago por Plataforma</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="notes">Notas Especiales</Label>
                  <Textarea
                    id="notes"
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                    placeholder="Instrucciones especiales..."
                    rows={3}
                  />
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Menu Items */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Seleccionar Productos</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {menuItems.map((item) => (
                  <div key={item.id} className="border rounded-lg p-4">
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <h4 className="font-medium">{item.name}</h4>
                        <Badge variant="outline" className="text-xs">
                          {item.category}
                        </Badge>
                      </div>
                      <span className="font-bold">${item.price.toFixed(2)}</span>
                    </div>
                    <Button type="button" onClick={() => addItem(item)} className="w-full" size="sm">
                      <Plus className="h-4 w-4 mr-2" />
                      Agregar
                    </Button>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Order Summary */}
          {orderItems.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Resumen del Pedido</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {orderItems.map((item) => (
                    <div key={item.id} className="flex items-center justify-between">
                      <div className="flex-1">
                        <span className="font-medium">{item.name}</span>
                        <span className="text-muted-foreground ml-2">${item.price.toFixed(2)} c/u</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Button
                          type="button"
                          variant="outline"
                          size="sm"
                          onClick={() => updateQuantity(item.id, item.quantity - 1)}
                        >
                          <Minus className="h-4 w-4" />
                        </Button>
                        <span className="w-8 text-center">{item.quantity}</span>
                        <Button
                          type="button"
                          variant="outline"
                          size="sm"
                          onClick={() => updateQuantity(item.id, item.quantity + 1)}
                        >
                          <Plus className="h-4 w-4" />
                        </Button>
                        <Button type="button" variant="ghost" size="sm" onClick={() => removeItem(item.id)}>
                          <X className="h-4 w-4" />
                        </Button>
                        <span className="w-16 text-right font-medium">${(item.price * item.quantity).toFixed(2)}</span>
                      </div>
                    </div>
                  ))}
                  <div className="border-t pt-4">
                    <div className="flex justify-between items-center text-lg font-bold">
                      <span>Total:</span>
                      <span>${calculateTotal().toFixed(2)}</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          <div className="flex justify-end gap-4">
            <Button type="button" variant="outline" onClick={onClose}>
              Cancelar
            </Button>
            <Button type="submit">Crear Pedido</Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  )
}
