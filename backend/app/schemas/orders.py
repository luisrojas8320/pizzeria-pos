from pydantic import BaseModel, validator, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal
from enum import Enum


class Platform(str, Enum):
    UBER_EATS = "uber_eats"
    PEDIDOS_YA = "pedidos_ya" 
    BIS = "bis"
    PHONE = "phone"
    WHATSAPP = "whatsapp"


class PaymentMethod(str, Enum):
    CASH = "cash"
    CARD = "card"
    TRANSFER = "transfer"


class OrderStatus(str, Enum):
    PENDING = "pending"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class OrderItemBase(BaseModel):
    menu_item_id: int
    quantity: int = Field(..., gt=0)
    unit_price: Decimal = Field(..., gt=0)
    special_instructions: Optional[str] = None
    
    @validator('quantity')
    def validate_quantity(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be positive')
        return v


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemInDB(OrderItemBase):
    id: int
    order_id: int
    total_price: Decimal
    
    class Config:
        from_attributes = True


class OrderItem(OrderItemInDB):
    pass


class OrderBase(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=100)
    customer_phone: Optional[str] = Field(None, regex=r'^\+?[\d\s\-\(\)]{7,20}$')
    customer_address: Optional[str] = None
    platform: Platform
    platform_order_id: Optional[str] = None
    payment_method: PaymentMethod
    delivery_fee: Decimal = Field(default=Decimal('0'), ge=0)
    
    @validator('customer_phone')
    def validate_phone(cls, v):
        if v and len(v.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')) < 7:
            raise ValueError('Phone number too short')
        return v


class OrderCreate(OrderBase):
    items: List[OrderItemCreate] = Field(..., min_items=1)
    
    @validator('items')
    def validate_items(cls, v):
        if not v:
            raise ValueError('Order must have at least one item')
        return v


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    delivered_at: Optional[datetime] = None


class OrderInDB(OrderBase):
    id: int
    order_number: str
    subtotal: Decimal
    tax_amount: Decimal
    total: Decimal
    ingredient_cost: Decimal
    packaging_cost: Decimal
    commission_rate: Decimal
    commission_amount: Decimal
    net_revenue: Decimal
    net_profit: Decimal
    status: OrderStatus
    created_at: datetime
    delivered_at: Optional[datetime]
    created_by: int
    
    class Config:
        from_attributes = True


class Order(OrderInDB):
    items: List[OrderItem] = []


class OrderSummary(BaseModel):
    id: int
    order_number: str
    customer_name: str
    platform: Platform
    total: Decimal
    status: OrderStatus
    created_at: datetime
    
    class Config:
        from_attributes = True


class SalesReport(BaseModel):
    period_start: datetime
    period_end: datetime
    total_orders: int
    total_revenue: Decimal
    total_costs: Decimal
    total_profit: Decimal
    average_order_value: Decimal
    platform_breakdown: Dict[str, Dict[str, Any]]
    top_items: List[Dict[str, Any]]


class DailySalesReport(SalesReport):
    hourly_breakdown: Dict[str, Dict[str, Any]]


class WeeklySalesReport(SalesReport):
    daily_breakdown: Dict[str, Dict[str, Any]]


class MonthlySalesReport(SalesReport):
    weekly_breakdown: Dict[str, Dict[str, Any]]