from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.auth import get_current_active_user_or_owner, get_current_active_owner
from ..models.users import User
from ..models.menu import MenuCategory, MenuItem, MenuItemVariation
from ..schemas.menu import (
    MenuCategoryCreate, MenuCategoryUpdate, MenuCategory as MenuCategorySchema,
    MenuItemCreate, MenuItemUpdate, MenuItem as MenuItemSchema,
    MenuItemVariationCreate, MenuItemVariationUpdate, MenuItemVariation as MenuItemVariationSchema
)


router = APIRouter()


# Menu Categories
@router.post("/categories/", response_model=MenuCategorySchema)
def create_category(
    category_data: MenuCategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_owner)
) -> Any:
    """
    Create a new menu category. Only owners can create categories.
    """
    # Check if category name already exists
    existing_category = db.query(MenuCategory).filter(MenuCategory.name == category_data.name).first()
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category name already exists"
        )
    
    db_category = MenuCategory(**category_data.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.get("/categories/", response_model=List[MenuCategorySchema])
def read_categories(
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Retrieve menu categories
    """
    query = db.query(MenuCategory)
    
    if is_active is not None:
        query = query.filter(MenuCategory.is_active == is_active)
    
    categories = query.order_by(MenuCategory.display_order, MenuCategory.name).offset(skip).limit(limit).all()
    return categories


@router.put("/categories/{category_id}", response_model=MenuCategorySchema)
def update_category(
    category_id: int,
    category_update: MenuCategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_owner)
) -> Any:
    """
    Update menu category
    """
    category = db.query(MenuCategory).filter(MenuCategory.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    update_data = category_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(category, field, value)
    
    db.commit()
    db.refresh(category)
    return category


# Menu Items
@router.post("/items/", response_model=MenuItemSchema)
def create_menu_item(
    item_data: MenuItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_owner)
) -> Any:
    """
    Create a new menu item
    """
    # Verify category exists
    category = db.query(MenuCategory).filter(MenuCategory.id == item_data.category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category not found"
        )
    
    # Convert recipe and allergens to JSON if provided
    recipe_json = None
    if item_data.recipe:
        recipe_json = [ingredient.dict() for ingredient in item_data.recipe]
    
    db_item = MenuItem(
        name=item_data.name,
        description=item_data.description,
        category_id=item_data.category_id,
        price=item_data.price,
        cost=item_data.cost,
        recipe=recipe_json,
        is_available=item_data.is_available,
        preparation_time=item_data.preparation_time,
        calories=item_data.calories,
        allergens=item_data.allergens,
        image_url=item_data.image_url,
        display_order=item_data.display_order
    )
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("/items/", response_model=List[MenuItemSchema])
def read_menu_items(
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = None,
    is_available: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Retrieve menu items
    """
    query = db.query(MenuItem)
    
    if category_id:
        query = query.filter(MenuItem.category_id == category_id)
    
    if is_available is not None:
        query = query.filter(MenuItem.is_available == is_available)
    
    items = query.order_by(MenuItem.display_order, MenuItem.name).offset(skip).limit(limit).all()
    return items


@router.get("/items/{item_id}", response_model=MenuItemSchema)
def read_menu_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Get menu item by ID
    """
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )
    return item


@router.put("/items/{item_id}", response_model=MenuItemSchema)
def update_menu_item(
    item_id: int,
    item_update: MenuItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_owner)
) -> Any:
    """
    Update menu item
    """
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )
    
    update_data = item_update.dict(exclude_unset=True)
    
    # Handle recipe update
    if 'recipe' in update_data and update_data['recipe']:
        update_data['recipe'] = [ingredient.dict() for ingredient in update_data['recipe']]
    
    for field, value in update_data.items():
        setattr(item, field, value)
    
    db.commit()
    db.refresh(item)
    return item


@router.delete("/items/{item_id}")
def delete_menu_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_owner)
) -> Any:
    """
    Delete menu item (soft delete by setting is_available to False)
    """
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )
    
    item.is_available = False
    db.commit()
    return {"message": "Menu item deleted successfully"}


# Menu Item Variations
@router.post("/items/{item_id}/variations/", response_model=MenuItemVariationSchema)
def create_menu_item_variation(
    item_id: int,
    variation_data: MenuItemVariationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_owner)
) -> Any:
    """
    Create a new menu item variation
    """
    # Verify menu item exists
    menu_item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not menu_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )
    
    variation_data.menu_item_id = item_id
    db_variation = MenuItemVariation(**variation_data.dict())
    db.add(db_variation)
    db.commit()
    db.refresh(db_variation)
    return db_variation


@router.get("/items/{item_id}/variations/", response_model=List[MenuItemVariationSchema])
def read_menu_item_variations(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Get variations for a menu item
    """
    variations = db.query(MenuItemVariation).filter(MenuItemVariation.menu_item_id == item_id).all()
    return variations