from sqlalchemy import Column, Integer, String, DECIMAL, Boolean, DateTime, Text, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base


class MenuCategory(Base):
    __tablename__ = "menu_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class MenuItem(Base):
    __tablename__ = "menu_items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey("menu_categories.id"), nullable=False)
    
    # Pricing
    price = Column(DECIMAL(10, 2), nullable=False)
    cost = Column(DECIMAL(10, 2), nullable=False)  # Cost to make
    
    # Recipe/ingredients (JSON array with ingredient_id and quantity)
    recipe = Column(JSON, nullable=True)
    
    # Availability
    is_available = Column(Boolean, default=True)
    preparation_time = Column(Integer, nullable=False, default=15)  # minutes
    
    # Nutrition/details
    calories = Column(Integer, nullable=True)
    allergens = Column(JSON, nullable=True)  # Array of allergen strings
    
    # Display
    image_url = Column(String(500), nullable=True)
    display_order = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    category = relationship("MenuCategory", backref="items")


class MenuItemVariation(Base):
    __tablename__ = "menu_item_variations"
    
    id = Column(Integer, primary_key=True, index=True)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)
    name = Column(String(100), nullable=False)  # Size, crust type, etc.
    price_modifier = Column(DECIMAL(10, 2), default=0)  # Additional cost
    cost_modifier = Column(DECIMAL(10, 2), default=0)  # Additional cost to make
    is_available = Column(Boolean, default=True)
    
    # Relationships
    menu_item = relationship("MenuItem", backref="variations")