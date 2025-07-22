from typing import Any, List, Optional
from datetime import datetime, date, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from ..core.database import get_db
from ..core.auth import get_current_active_user_or_owner, get_current_active_owner
from ..models.users import User
from ..models.purchases import PurchaseOrder, PurchaseOrderItem, PurchaseSchedule
from ..models.inventory import Supplier
from ..schemas.purchases import (
    PurchaseOrderCreate, PurchaseOrder as PurchaseOrderSchema, 
    PurchaseOrderUpdate, PurchaseOrderSummary,
    PurchaseScheduleCreate, PurchaseSchedule as PurchaseScheduleSchema,
    SupplierCreate, Supplier as SupplierSchema,
    PurchaseAnalytics
)


router = APIRouter()


# Suppliers
@router.post("/suppliers/", response_model=SupplierSchema)
def create_supplier(
    supplier_data: SupplierCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_owner)
) -> Any:
    """
    Create a new supplier
    """
    db_supplier = Supplier(**supplier_data.dict())
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier


@router.get("/suppliers/", response_model=List[SupplierSchema])
def read_suppliers(
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Retrieve suppliers
    """
    query = db.query(Supplier)
    
    if is_active is not None:
        query = query.filter(Supplier.is_active == is_active)
    
    suppliers = query.order_by(Supplier.name).offset(skip).limit(limit).all()
    return suppliers


# Purchase Orders
@router.post("/", response_model=PurchaseOrderSchema)
def create_purchase_order(
    order_data: PurchaseOrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Create a new purchase order
    """
    # Verify supplier exists
    supplier = db.query(Supplier).filter(Supplier.id == order_data.supplier_id).first()
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Supplier not found"
        )
    
    # Generate purchase number
    purchase_count = db.query(PurchaseOrder).count()
    purchase_number = f"PO{datetime.now().strftime('%Y%m%d')}{purchase_count + 1:04d}"
    
    # Calculate totals
    subtotal = sum(item.quantity_ordered * item.unit_cost for item in order_data.items)
    tax_amount = subtotal * 0.12  # 12% IVA in Ecuador
    total_cost = subtotal + tax_amount + order_data.shipping_cost
    
    # Create purchase order
    db_order = PurchaseOrder(
        purchase_number=purchase_number,
        supplier_id=order_data.supplier_id,
        priority=order_data.priority,
        subtotal=subtotal,
        tax_amount=tax_amount,
        shipping_cost=order_data.shipping_cost,
        total_cost=total_cost,
        expected_delivery_date=order_data.expected_delivery_date,
        notes=order_data.notes,
        payment_terms=order_data.payment_terms,
        created_by=current_user.id
    )
    
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    # Create order items
    for item_data in order_data.items:
        total_item_cost = item_data.quantity_ordered * item_data.unit_cost
        
        db_item = PurchaseOrderItem(
            purchase_order_id=db_order.id,
            inventory_item_id=item_data.inventory_item_id,
            quantity_ordered=item_data.quantity_ordered,
            unit=item_data.unit,
            unit_cost=item_data.unit_cost,
            total_cost=total_item_cost,
            batch_number=item_data.batch_number,
            expiry_date=item_data.expiry_date,
            notes=item_data.notes
        )
        db.add(db_item)
    
    db.commit()
    db.refresh(db_order)
    return db_order


@router.get("/", response_model=List[PurchaseOrderSummary])
def read_purchase_orders(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    supplier_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Retrieve purchase orders with filters
    """
    query = db.query(PurchaseOrder).join(Supplier)
    
    if status:
        query = query.filter(PurchaseOrder.status == status)
    
    if supplier_id:
        query = query.filter(PurchaseOrder.supplier_id == supplier_id)
    
    if start_date:
        query = query.filter(PurchaseOrder.order_date >= start_date)
    
    if end_date:
        query = query.filter(PurchaseOrder.order_date <= end_date)
    
    orders = query.order_by(desc(PurchaseOrder.order_date)).offset(skip).limit(limit).all()
    
    return [
        PurchaseOrderSummary(
            id=order.id,
            purchase_number=order.purchase_number,
            supplier_name=order.supplier.name,
            status=order.status,
            total_cost=order.total_cost,
            order_date=order.order_date,
            expected_delivery_date=order.expected_delivery_date
        )
        for order in orders
    ]


@router.get("/{order_id}", response_model=PurchaseOrderSchema)
def read_purchase_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Get purchase order by ID
    """
    order = db.query(PurchaseOrder).filter(PurchaseOrder.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Purchase order not found"
        )
    return order


@router.put("/{order_id}", response_model=PurchaseOrderSchema)
def update_purchase_order(
    order_id: int,
    order_update: PurchaseOrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Update purchase order
    """
    order = db.query(PurchaseOrder).filter(PurchaseOrder.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Purchase order not found"
        )
    
    update_data = order_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(order, field, value)
    
    db.commit()
    db.refresh(order)
    return order


# Purchase Schedules
@router.post("/schedules/", response_model=PurchaseScheduleSchema)
def create_purchase_schedule(
    schedule_data: PurchaseScheduleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_owner)
) -> Any:
    """
    Create a purchase schedule
    """
    scheduled_items_json = [item.dict() for item in schedule_data.scheduled_items]
    
    db_schedule = PurchaseSchedule(
        name=schedule_data.name,
        description=schedule_data.description,
        frequency=schedule_data.frequency,
        day_of_week=schedule_data.day_of_week,
        day_of_month=schedule_data.day_of_month,
        scheduled_items=scheduled_items_json,
        is_active=schedule_data.is_active,
        auto_create=schedule_data.auto_create
    )
    
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule


@router.get("/schedules/", response_model=List[PurchaseScheduleSchema])
def read_purchase_schedules(
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Retrieve purchase schedules
    """
    query = db.query(PurchaseSchedule)
    
    if is_active is not None:
        query = query.filter(PurchaseSchedule.is_active == is_active)
    
    schedules = query.order_by(PurchaseSchedule.name).offset(skip).limit(limit).all()
    return schedules


@router.get("/schedules/weekly", response_model=List[dict])
def get_weekly_schedule(
    week_start: Optional[date] = Query(default=None, description="Start of week (Monday)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Get weekly purchase schedule
    """
    if not week_start:
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
    
    # Get active weekly schedules
    schedules = db.query(PurchaseSchedule).filter(
        PurchaseSchedule.is_active == True,
        PurchaseSchedule.frequency == "weekly"
    ).all()
    
    weekly_schedule = []
    for schedule in schedules:
        if schedule.day_of_week is not None:
            scheduled_date = week_start + timedelta(days=schedule.day_of_week)
            weekly_schedule.append({
                "schedule_id": schedule.id,
                "name": schedule.name,
                "date": scheduled_date,
                "items": schedule.scheduled_items,
                "auto_create": schedule.auto_create
            })
    
    return sorted(weekly_schedule, key=lambda x: x["date"])


@router.get("/analytics/", response_model=PurchaseAnalytics)
def get_purchase_analytics(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Get purchase analytics
    """
    query = db.query(PurchaseOrder).filter(PurchaseOrder.status != "cancelled")
    
    if start_date:
        query = query.filter(PurchaseOrder.order_date >= start_date)
    
    if end_date:
        query = query.filter(PurchaseOrder.order_date <= end_date)
    
    orders = query.all()
    
    total_orders = len(orders)
    total_spent = sum(order.total_cost for order in orders) if orders else 0
    average_order_value = total_spent / total_orders if total_orders > 0 else 0
    
    # Top suppliers
    supplier_stats = {}
    for order in orders:
        supplier_name = order.supplier.name
        if supplier_name not in supplier_stats:
            supplier_stats[supplier_name] = {
                "name": supplier_name,
                "orders": 0,
                "total_spent": 0
            }
        supplier_stats[supplier_name]["orders"] += 1
        supplier_stats[supplier_name]["total_spent"] += float(order.total_cost)
    
    top_suppliers = sorted(
        supplier_stats.values(),
        key=lambda x: x["total_spent"],
        reverse=True
    )[:5]
    
    return PurchaseAnalytics(
        total_orders=total_orders,
        total_spent=total_spent,
        average_order_value=average_order_value,
        top_suppliers=top_suppliers,
        cost_trends={},  # Would need more complex calculation
        delivery_performance={}  # Would need delivery tracking
    )