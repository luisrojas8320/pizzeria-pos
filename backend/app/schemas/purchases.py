from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from decimal import Decimal
from enum import Enum


class PurchaseOrderStatus(str, Enum):
    PENDING = "pending"
    ORDERED = "ordered"
    RECEIVED = "received"
    CANCELLED = "cancelled"


class PurchasePriority(str, Enum):
    URGENT = "urgent"
    HIGH = "high"
    NORMAL = "normal"
    LOW = "low"


class SupplierBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    contact_person: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, pattern=r'^\+?[\d\s\-\(\)]{7,20}$')
    email: Optional[str] = Field(None, pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    address: Optional[str] = None
    is_active: bool = True


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    contact_person: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, pattern=r'^\+?[\d\s\-\(\)]{7,20}$')
    email: Optional[str] = Field(None, pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    address: Optional[str] = None
    is_active: Optional[bool] = None


class SupplierInDB(SupplierBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class Supplier(SupplierInDB):
    pass


class PurchaseOrderItemBase(BaseModel):
    inventory_item_id: int = Field(..., gt=0)
    quantity_ordered: Decimal = Field(..., gt=0)
    unit: str = Field(..., min_length=1, max_length=20)
    unit_cost: Decimal = Field(..., gt=0)
    batch_number: Optional[str] = Field(None, max_length=50)
    expiry_date: Optional[datetime] = None
    notes: Optional[str] = None
    
    @field_validator('quantity_ordered', 'unit_cost')
    @classmethod
    def validate_positive(cls, v):
        if v <= 0:
            raise ValueError('Value must be positive')
        return v


class PurchaseOrderItemCreate(PurchaseOrderItemBase):
    pass


class PurchaseOrderItemUpdate(BaseModel):
    quantity_received: Optional[Decimal] = Field(None, ge=0)
    quality_rating: Optional[int] = Field(None, ge=1, le=5)
    notes: Optional[str] = None


class PurchaseOrderItemInDB(PurchaseOrderItemBase):
    id: int
    purchase_order_id: int
    quantity_received: Optional[Decimal] = None
    total_cost: Decimal
    quality_rating: Optional[int] = None
    
    class Config:
        from_attributes = True


class PurchaseOrderItem(PurchaseOrderItemInDB):
    pass


class PurchaseOrderBase(BaseModel):
    supplier_id: int = Field(..., gt=0)
    priority: PurchasePriority = PurchasePriority.NORMAL
    expected_delivery_date: Optional[datetime] = None
    notes: Optional[str] = None
    payment_terms: Optional[str] = Field(None, max_length=100)


class PurchaseOrderCreate(PurchaseOrderBase):
    items: List[PurchaseOrderItemCreate] = Field(..., min_items=1)
    shipping_cost: Decimal = Field(default=Decimal('0'), ge=0)
    
    @field_validator('items')
    @classmethod
    def validate_items(cls, v):
        if not v:
            raise ValueError('Purchase order must have at least one item')
        return v


class PurchaseOrderUpdate(BaseModel):
    status: Optional[PurchaseOrderStatus] = None
    expected_delivery_date: Optional[datetime] = None
    actual_delivery_date: Optional[datetime] = None
    notes: Optional[str] = None
    received_by: Optional[int] = None


class PurchaseOrderInDB(PurchaseOrderBase):
    id: int
    purchase_number: str
    status: PurchaseOrderStatus
    subtotal: Decimal
    tax_amount: Decimal
    shipping_cost: Decimal
    total_cost: Decimal
    order_date: datetime
    actual_delivery_date: Optional[datetime]
    created_by: int
    received_by: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class PurchaseOrder(PurchaseOrderInDB):
    supplier: Optional[Supplier] = None
    items: List[PurchaseOrderItem] = []


class PurchaseOrderSummary(BaseModel):
    id: int
    purchase_number: str
    supplier_name: str
    status: PurchaseOrderStatus
    total_cost: Decimal
    order_date: datetime
    expected_delivery_date: Optional[datetime]
    
    class Config:
        from_attributes = True


class PurchaseScheduleFrequency(str, Enum):
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"


class ScheduledItem(BaseModel):
    item_id: int = Field(..., gt=0)
    min_quantity: Decimal = Field(..., gt=0)
    max_quantity: Decimal = Field(..., gt=0)
    
    @field_validator('max_quantity')
    @classmethod
    def validate_max_greater_than_min(cls, v, values):
        if 'min_quantity' in values and v <= values['min_quantity']:
            raise ValueError('Max quantity must be greater than min quantity')
        return v


class PurchaseScheduleBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    frequency: PurchaseScheduleFrequency
    day_of_week: Optional[int] = Field(None, ge=0, le=6)  # 0=Monday
    day_of_month: Optional[int] = Field(None, ge=1, le=31)
    is_active: bool = True
    auto_create: bool = False


class PurchaseScheduleCreate(PurchaseScheduleBase):
    scheduled_items: List[ScheduledItem] = Field(..., min_items=1)
    
    @field_validator('scheduled_items')
    @classmethod
    def validate_scheduled_items(cls, v):
        if not v:
            raise ValueError('Schedule must have at least one item')
        return v


class PurchaseScheduleUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    frequency: Optional[PurchaseScheduleFrequency] = None
    day_of_week: Optional[int] = Field(None, ge=0, le=6)
    day_of_month: Optional[int] = Field(None, ge=1, le=31)
    scheduled_items: Optional[List[ScheduledItem]] = None
    is_active: Optional[bool] = None
    auto_create: Optional[bool] = None


class PurchaseScheduleInDB(PurchaseScheduleBase):
    id: int
    scheduled_items: List[Dict[str, Any]]
    created_at: datetime
    updated_at: Optional[datetime]
    last_run: Optional[datetime]
    
    class Config:
        from_attributes = True


class PurchaseSchedule(PurchaseScheduleInDB):
    pass


class PurchaseAnalytics(BaseModel):
    total_orders: int
    total_spent: Decimal
    average_order_value: Decimal
    top_suppliers: List[Dict[str, Any]]
    cost_trends: Dict[str, Any]
    delivery_performance: Dict[str, Any]