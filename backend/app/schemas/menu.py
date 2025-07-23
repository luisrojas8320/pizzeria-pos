from pydantic import BaseModel, Field, field_validator, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal


class MenuCategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    display_order: int = 0
    is_active: bool = True


class MenuCategoryCreate(MenuCategoryBase):
    pass


class MenuCategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None


class MenuCategoryInDB(MenuCategoryBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class MenuCategory(MenuCategoryInDB):
    pass


class RecipeIngredient(BaseModel):
    ingredient_id: int = Field(..., gt=0)
    quantity: Decimal = Field(..., gt=0)
    unit: str = Field(..., min_length=1, max_length=20)


class MenuItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    category_id: int = Field(..., gt=0)
    price: Decimal = Field(..., gt=0)
    cost: Decimal = Field(..., ge=0)
    is_available: bool = True
    preparation_time: int = Field(default=15, gt=0)
    calories: Optional[int] = Field(None, ge=0)
    image_url: Optional[str] = Field(None, max_length=500)
    display_order: int = 0
    
    @validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Price must be positive')
        return v
    
    @validator('cost')
    def validate_cost(cls, v):
        if v < 0:
            raise ValueError('Cost cannot be negative')
        return v


class MenuItemCreate(MenuItemBase):
    recipe: Optional[List[RecipeIngredient]] = None
    allergens: Optional[List[str]] = None


class MenuItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    category_id: Optional[int] = Field(None, gt=0)
    price: Optional[Decimal] = Field(None, gt=0)
    cost: Optional[Decimal] = Field(None, ge=0)
    recipe: Optional[List[RecipeIngredient]] = None
    is_available: Optional[bool] = None
    preparation_time: Optional[int] = Field(None, gt=0)
    calories: Optional[int] = Field(None, ge=0)
    allergens: Optional[List[str]] = None
    image_url: Optional[str] = Field(None, max_length=500)
    display_order: Optional[int] = None


class MenuItemInDB(MenuItemBase):
    id: int
    recipe: Optional[List[Dict[str, Any]]] = None
    allergens: Optional[List[str]] = None
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class MenuItem(MenuItemInDB):
    category: Optional[MenuCategory] = None
    variations: Optional[List['MenuItemVariation']] = []


class MenuItemVariationBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price_modifier: Decimal = Field(default=Decimal('0'))
    cost_modifier: Decimal = Field(default=Decimal('0'))
    is_available: bool = True


class MenuItemVariationCreate(MenuItemVariationBase):
    menu_item_id: int = Field(..., gt=0)


class MenuItemVariationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    price_modifier: Optional[Decimal] = None
    cost_modifier: Optional[Decimal] = None
    is_available: Optional[bool] = None


class MenuItemVariationInDB(MenuItemVariationBase):
    id: int
    menu_item_id: int
    
    class Config:
        from_attributes = True


class MenuItemVariation(MenuItemVariationInDB):
    pass


class MenuSummary(BaseModel):
    total_items: int
    total_categories: int
    available_items: int
    average_price: Decimal
    price_range: Dict[str, Decimal]


class MenuItemPopularity(BaseModel):
    menu_item_id: int
    name: str
    total_ordered: int
    total_revenue: Decimal
    order_frequency: str
    
    class Config:
        from_attributes = True


# Update forward references
MenuItem.model_rebuild()