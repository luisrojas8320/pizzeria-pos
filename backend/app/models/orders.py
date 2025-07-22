from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, JSON, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, index=True, nullable=False)
    customer_name = Column(String(100), nullable=False)
    customer_phone = Column(String(20), nullable=True)
    customer_address = Column(Text, nullable=True)
    
    # Platform information
    platform = Column(String(50), nullable=False)  # uber_eats, pedidos_ya, bis, phone, whatsapp
    platform_order_id = Column(String(100), nullable=True)
    
    # Payment information
    payment_method = Column(String(50), nullable=False)  # cash, card, transfer
    
    # Order items (JSON array)
    items = Column(JSON, nullable=False)
    
    # Financial calculations
    subtotal = Column(DECIMAL(10, 2), nullable=False)
    tax_amount = Column(DECIMAL(10, 2), nullable=False, default=0)
    delivery_fee = Column(DECIMAL(10, 2), nullable=False, default=0)
    total = Column(DECIMAL(10, 2), nullable=False)
    
    # Cost calculations
    ingredient_cost = Column(DECIMAL(10, 2), nullable=False)
    packaging_cost = Column(DECIMAL(10, 2), nullable=False)
    commission_rate = Column(DECIMAL(5, 4), nullable=False)  # Platform commission rate
    commission_amount = Column(DECIMAL(10, 2), nullable=False)
    net_revenue = Column(DECIMAL(10, 2), nullable=False)
    net_profit = Column(DECIMAL(10, 2), nullable=False)
    
    # Order status
    status = Column(String(20), nullable=False, default="pending")  # pending, preparing, ready, delivered, cancelled
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    delivered_at = Column(DateTime(timezone=True), nullable=True)
    
    # Foreign keys
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    creator = relationship("User", foreign_keys=[created_by])


class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL(10, 2), nullable=False)
    total_price = Column(DECIMAL(10, 2), nullable=False)
    special_instructions = Column(Text, nullable=True)
    
    # Relationships
    order = relationship("Order", backref="order_items")
    menu_item = relationship("MenuItem")