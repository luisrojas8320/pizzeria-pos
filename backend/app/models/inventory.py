from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base


class Supplier(Base):
    __tablename__ = "suppliers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    contact_person = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    address = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class InventoryItem(Base):
    __tablename__ = "inventory_items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), nullable=False)  # dairy, meat, vegetables, etc.
    
    # Stock information
    current_stock = Column(DECIMAL(10, 3), nullable=False, default=0)
    min_threshold = Column(DECIMAL(10, 3), nullable=False, default=0)
    max_threshold = Column(DECIMAL(10, 3), nullable=True)
    unit = Column(String(20), nullable=False)  # kg, liters, pieces, etc.
    
    # Cost information
    cost_per_unit = Column(DECIMAL(10, 4), nullable=False)
    last_purchase_cost = Column(DECIMAL(10, 4), nullable=True)
    
    # Supplier information
    primary_supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)
    
    # Expiration tracking
    has_expiration = Column(Boolean, default=False)
    average_shelf_life = Column(Integer, nullable=True)  # days
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    primary_supplier = relationship("Supplier")


class StockMovement(Base):
    __tablename__ = "stock_movements"
    
    id = Column(Integer, primary_key=True, index=True)
    inventory_item_id = Column(Integer, ForeignKey("inventory_items.id"), nullable=False)
    movement_type = Column(String(20), nullable=False)  # purchase, usage, adjustment, waste
    quantity = Column(DECIMAL(10, 3), nullable=False)  # Positive for in, negative for out
    unit_cost = Column(DECIMAL(10, 4), nullable=True)
    total_cost = Column(DECIMAL(10, 2), nullable=True)
    
    # Reference information
    reference_type = Column(String(20), nullable=True)  # order, purchase, adjustment
    reference_id = Column(Integer, nullable=True)
    
    # Additional information
    notes = Column(Text, nullable=True)
    batch_number = Column(String(50), nullable=True)
    expiry_date = Column(DateTime(timezone=True), nullable=True)
    
    # User and timestamp
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    inventory_item = relationship("InventoryItem", backref="stock_movements")
    creator = relationship("User")