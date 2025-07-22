from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, Text, Boolean, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"
    
    id = Column(Integer, primary_key=True, index=True)
    purchase_number = Column(String(50), unique=True, index=True, nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    
    # Order details
    status = Column(String(20), nullable=False, default="pending")  # pending, ordered, received, cancelled
    priority = Column(String(20), nullable=False, default="normal")  # urgent, high, normal, low
    
    # Financial information
    subtotal = Column(DECIMAL(10, 2), nullable=False)
    tax_amount = Column(DECIMAL(10, 2), nullable=False, default=0)
    shipping_cost = Column(DECIMAL(10, 2), nullable=False, default=0)
    total_cost = Column(DECIMAL(10, 2), nullable=False)
    
    # Dates
    order_date = Column(DateTime(timezone=True), server_default=func.now())
    expected_delivery_date = Column(DateTime(timezone=True), nullable=True)
    actual_delivery_date = Column(DateTime(timezone=True), nullable=True)
    
    # Additional information
    notes = Column(Text, nullable=True)
    payment_terms = Column(String(100), nullable=True)
    
    # User tracking
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    received_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    supplier = relationship("Supplier", backref="purchase_orders")
    creator = relationship("User", foreign_keys=[created_by])
    receiver = relationship("User", foreign_keys=[received_by])


class PurchaseOrderItem(Base):
    __tablename__ = "purchase_order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    purchase_order_id = Column(Integer, ForeignKey("purchase_orders.id"), nullable=False)
    inventory_item_id = Column(Integer, ForeignKey("inventory_items.id"), nullable=False)
    
    # Quantities
    quantity_ordered = Column(DECIMAL(10, 3), nullable=False)
    quantity_received = Column(DECIMAL(10, 3), nullable=True, default=0)
    unit = Column(String(20), nullable=False)
    
    # Pricing
    unit_cost = Column(DECIMAL(10, 4), nullable=False)
    total_cost = Column(DECIMAL(10, 2), nullable=False)
    
    # Quality control
    quality_rating = Column(Integer, nullable=True)  # 1-5 scale
    notes = Column(Text, nullable=True)
    
    # Batch tracking
    batch_number = Column(String(50), nullable=True)
    expiry_date = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    purchase_order = relationship("PurchaseOrder", backref="items")
    inventory_item = relationship("InventoryItem")


class PurchaseSchedule(Base):
    __tablename__ = "purchase_schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    
    # Schedule settings
    frequency = Column(String(20), nullable=False)  # weekly, biweekly, monthly
    day_of_week = Column(Integer, nullable=True)  # 0=Monday, 6=Sunday
    day_of_month = Column(Integer, nullable=True)  # For monthly schedules
    
    # Items to purchase (JSON with item_id, min_quantity, max_quantity)
    scheduled_items = Column(JSON, nullable=False)
    
    # Settings
    is_active = Column(Boolean, default=True)
    auto_create = Column(Boolean, default=False)  # Auto-create purchase orders
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_run = Column(DateTime(timezone=True), nullable=True)