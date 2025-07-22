from typing import Any, List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc

from ..core.database import get_db
from ..core.auth import get_current_active_user_or_owner
from ..models.users import User
from ..models.orders import Order, OrderItem
from ..models.menu import MenuItem
from ..schemas.orders import (
    OrderCreate, Order as OrderSchema, OrderUpdate, OrderSummary,
    SalesReport, DailySalesReport, WeeklySalesReport, MonthlySalesReport
)
from ..services.orders import OrderService


router = APIRouter()


@router.post("/", response_model=OrderSchema)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Create a new order
    """
    return OrderService.create_order(db, order_data, current_user.id)


@router.get("/", response_model=List[OrderSummary])
def read_orders(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    platform: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Retrieve orders with optional filters
    """
    query = db.query(Order)
    
    if status:
        query = query.filter(Order.status == status)
    
    if platform:
        query = query.filter(Order.platform == platform)
    
    if start_date:
        query = query.filter(Order.created_at >= start_date)
    
    if end_date:
        query = query.filter(Order.created_at <= end_date)
    
    orders = query.order_by(desc(Order.created_at)).offset(skip).limit(limit).all()
    
    return [
        OrderSummary(
            id=order.id,
            order_number=order.order_number,
            customer_name=order.customer_name,
            platform=order.platform,
            total=order.total,
            status=order.status,
            created_at=order.created_at
        )
        for order in orders
    ]


@router.get("/{order_id}", response_model=OrderSchema)
def read_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Get order by ID
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return order


@router.put("/{order_id}", response_model=OrderSchema)
def update_order(
    order_id: int,
    order_update: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Update order status
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    update_data = order_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(order, field, value)
    
    db.commit()
    db.refresh(order)
    return order


@router.get("/reports/daily", response_model=DailySalesReport)
def get_daily_sales_report(
    date: Optional[datetime] = Query(default=None, description="Date for the report (defaults to today)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Get daily sales report
    """
    if not date:
        date = datetime.now().date()
    else:
        date = date.date()
    
    return OrderService.get_daily_sales_report(db, date)


@router.get("/reports/weekly", response_model=WeeklySalesReport)
def get_weekly_sales_report(
    start_date: Optional[datetime] = Query(default=None, description="Start date of the week"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Get weekly sales report
    """
    if not start_date:
        # Default to current week (Monday to Sunday)
        today = datetime.now().date()
        start_date = today - timedelta(days=today.weekday())
    else:
        start_date = start_date.date()
    
    return OrderService.get_weekly_sales_report(db, start_date)


@router.get("/reports/monthly", response_model=MonthlySalesReport)
def get_monthly_sales_report(
    year: int = Query(default=None, description="Year for the report"),
    month: int = Query(default=None, description="Month for the report"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Get monthly sales report
    """
    if not year:
        year = datetime.now().year
    if not month:
        month = datetime.now().month
    
    return OrderService.get_monthly_sales_report(db, year, month)


@router.get("/analytics/popular-items")
def get_popular_items(
    limit: int = Query(default=10, description="Number of items to return"),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Get most popular menu items
    """
    return OrderService.get_popular_items(db, limit, start_date, end_date)


@router.get("/analytics/platform-performance")
def get_platform_performance(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Get platform performance analytics
    """
    return OrderService.get_platform_performance(db, start_date, end_date)