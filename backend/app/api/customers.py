from typing import Any, List, Optional
from datetime import datetime, date, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, func
from decimal import Decimal

from ..core.database import get_db
from ..core.auth import get_current_active_user_or_owner
from ..models.users import User
from ..models.customers import Customer, CustomerFeedback
from ..models.orders import Order


router = APIRouter()


@router.get("/")
def read_customers(
    skip: int = 0,
    limit: int = 100,
    is_vip: Optional[bool] = None,
    phone: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Retrieve customers
    """
    query = db.query(Customer)
    
    if is_vip is not None:
        query = query.filter(Customer.is_vip == is_vip)
    
    if phone:
        query = query.filter(Customer.phone.like(f"%{phone}%"))
    
    customers = query.order_by(desc(Customer.last_order_date)).offset(skip).limit(limit).all()
    return customers


@router.get("/{customer_id}")
def read_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Get customer by ID
    """
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return customer


@router.get("/frequent/")
def get_frequent_customers(
    limit: int = Query(default=50, description="Number of customers to return"),
    min_orders: int = Query(default=5, description="Minimum number of orders"),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Get frequent customers based on order count and spending
    """
    # Base query for customers with minimum orders
    query = db.query(Customer).filter(Customer.total_orders >= min_orders)
    
    # If date range specified, filter by customers who ordered in that period
    if start_date or end_date:
        order_query = db.query(Order.customer_phone).distinct()
        
        if start_date:
            order_query = order_query.filter(Order.created_at >= start_date)
        
        if end_date:
            order_query = order_query.filter(Order.created_at <= end_date)
        
        phones_in_period = [phone for phone, in order_query.all()]
        query = query.filter(Customer.phone.in_(phones_in_period))
    
    # Order by total spent and loyalty score
    customers = query.order_by(
        desc(Customer.total_spent),
        desc(Customer.loyalty_score),
        desc(Customer.total_orders)
    ).limit(limit).all()
    
    # Enhance with recent order information
    result = []
    for customer in customers:
        # Get recent orders
        recent_orders = db.query(Order).filter(
            Order.customer_phone == customer.phone
        ).order_by(desc(Order.created_at)).limit(3).all()
        
        customer_data = {
            "id": customer.id,
            "name": customer.name,
            "phone": customer.phone,
            "email": customer.email,
            "total_orders": customer.total_orders,
            "total_spent": float(customer.total_spent),
            "average_order_value": float(customer.average_order_value),
            "loyalty_score": float(customer.loyalty_score),
            "is_vip": customer.is_vip,
            "order_frequency": customer.order_frequency,
            "favorite_items": customer.favorite_items,
            "last_order_date": customer.last_order_date,
            "recent_orders": [
                {
                    "order_number": order.order_number,
                    "total": float(order.total),
                    "platform": order.platform,
                    "created_at": order.created_at
                }
                for order in recent_orders
            ]
        }
        result.append(customer_data)
    
    return result


@router.get("/analytics/segmentation")
def get_customer_segmentation(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Get customer segmentation analytics
    """
    total_customers = db.query(Customer).count()
    
    # Segment by order frequency
    segments = {
        "high_value": db.query(Customer).filter(Customer.total_spent > 100).count(),
        "medium_value": db.query(Customer).filter(
            and_(Customer.total_spent >= 50, Customer.total_spent <= 100)
        ).count(),
        "low_value": db.query(Customer).filter(Customer.total_spent < 50).count(),
        "frequent": db.query(Customer).filter(Customer.total_orders >= 10).count(),
        "occasional": db.query(Customer).filter(
            and_(Customer.total_orders >= 3, Customer.total_orders < 10)
        ).count(),
        "new": db.query(Customer).filter(Customer.total_orders < 3).count(),
        "vip": db.query(Customer).filter(Customer.is_vip == True).count()
    }
    
    # Calculate percentages
    segmentation = {}
    for segment, count in segments.items():
        segmentation[segment] = {
            "count": count,
            "percentage": round((count / total_customers * 100) if total_customers > 0 else 0, 2)
        }
    
    return {
        "total_customers": total_customers,
        "segments": segmentation
    }


@router.get("/analytics/retention")
def get_customer_retention(
    period_days: int = Query(default=30, description="Period in days for retention analysis"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Calculate customer retention metrics
    """
    cutoff_date = datetime.now() - timedelta(days=period_days)
    
    # Customers who made their first order before the cutoff
    first_time_customers = db.query(Customer).filter(Customer.first_order_date < cutoff_date).all()
    
    # Customers who have ordered since the cutoff (retained customers)
    retained_customers = db.query(Customer).filter(
        and_(
            Customer.first_order_date < cutoff_date,
            Customer.last_order_date >= cutoff_date
        )
    ).all()
    
    total_eligible = len(first_time_customers)
    retained_count = len(retained_customers)
    retention_rate = (retained_count / total_eligible * 100) if total_eligible > 0 else 0
    
    # Calculate average time between orders for retained customers
    avg_order_interval = 0
    if retained_customers:
        intervals = []
        for customer in retained_customers:
            if customer.total_orders > 1:
                days_since_first = (customer.last_order_date - customer.first_order_date).days
                interval = days_since_first / (customer.total_orders - 1)
                intervals.append(interval)
        
        avg_order_interval = sum(intervals) / len(intervals) if intervals else 0
    
    return {
        "period_days": period_days,
        "total_eligible_customers": total_eligible,
        "retained_customers": retained_count,
        "retention_rate": round(retention_rate, 2),
        "average_order_interval_days": round(avg_order_interval, 1),
        "churn_rate": round(100 - retention_rate, 2)
    }


@router.get("/feedback/")
def get_customer_feedback(
    skip: int = 0,
    limit: int = 100,
    rating: Optional[int] = Query(None, ge=1, le=5),
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Retrieve customer feedback
    """
    query = db.query(CustomerFeedback)
    
    if rating:
        query = query.filter(CustomerFeedback.rating == rating)
    
    if category:
        query = query.filter(CustomerFeedback.category == category)
    
    feedback = query.order_by(desc(CustomerFeedback.created_at)).offset(skip).limit(limit).all()
    return feedback


@router.get("/analytics/satisfaction")
def get_customer_satisfaction_metrics(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Get customer satisfaction metrics from feedback
    """
    query = db.query(CustomerFeedback)
    
    if start_date:
        query = query.filter(CustomerFeedback.created_at >= start_date)
    
    if end_date:
        query = query.filter(CustomerFeedback.created_at <= end_date)
    
    feedback_data = query.all()
    
    if not feedback_data:
        return {
            "total_reviews": 0,
            "average_rating": 0,
            "rating_distribution": {},
            "category_ratings": {},
            "satisfaction_trends": {}
        }
    
    total_reviews = len(feedback_data)
    average_rating = sum(f.rating for f in feedback_data) / total_reviews
    
    # Rating distribution
    rating_dist = {}
    for i in range(1, 6):
        count = len([f for f in feedback_data if f.rating == i])
        rating_dist[str(i)] = {
            "count": count,
            "percentage": round((count / total_reviews * 100), 2)
        }
    
    # Category ratings
    category_ratings = {}
    for feedback in feedback_data:
        category = feedback.category
        if category not in category_ratings:
            category_ratings[category] = {"ratings": [], "count": 0}
        category_ratings[category]["ratings"].append(feedback.rating)
        category_ratings[category]["count"] += 1
    
    for category, data in category_ratings.items():
        avg_rating = sum(data["ratings"]) / len(data["ratings"])
        category_ratings[category] = {
            "average_rating": round(avg_rating, 2),
            "count": data["count"]
        }
    
    return {
        "total_reviews": total_reviews,
        "average_rating": round(average_rating, 2),
        "rating_distribution": rating_dist,
        "category_ratings": category_ratings,
        "nps_score": calculate_nps_score(feedback_data)  # Net Promoter Score
    }


def calculate_nps_score(feedback_data) -> float:
    """
    Calculate Net Promoter Score (NPS) from feedback ratings
    Ratings 4-5 = Promoters, 3 = Passive, 1-2 = Detractors
    """
    if not feedback_data:
        return 0
    
    promoters = len([f for f in feedback_data if f.rating >= 4])
    detractors = len([f for f in feedback_data if f.rating <= 2])
    total = len(feedback_data)
    
    nps = ((promoters - detractors) / total) * 100
    return round(nps, 2)