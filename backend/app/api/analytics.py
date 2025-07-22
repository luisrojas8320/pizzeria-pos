from typing import Any, List, Optional, Dict
from datetime import datetime, date, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, func, extract
from decimal import Decimal
import calendar

from ..core.database import get_db
from ..core.auth import get_current_active_user_or_owner
from ..models.users import User
from ..models.orders import Order
from ..models.customers import Customer
from ..models.staff import Staff, StaffPerformance
from ..models.menu import MenuItem
from ..utils.predictions import DemandPredictor
from ..utils.optimization import BusinessOptimizer


router = APIRouter()


@router.get("/trends/demand")
def get_demand_trends(
    period: str = Query(default="monthly", description="daily, weekly, monthly"),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Analyze demand trends for Ibarra market context
    """
    if not start_date:
        start_date = datetime.now() - timedelta(days=90)
    
    if not end_date:
        end_date = datetime.now()
    
    # Get orders in the period
    orders = db.query(Order).filter(
        and_(
            Order.created_at >= start_date,
            Order.created_at <= end_date,
            Order.status != "cancelled"
        )
    ).all()
    
    # Analyze trends based on period
    trends = {}
    
    if period == "monthly":
        trends = _analyze_monthly_trends(orders)
    elif period == "weekly":
        trends = _analyze_weekly_trends(orders)
    elif period == "daily":
        trends = _analyze_daily_trends(orders)
    
    # Add Ibarra-specific context
    ibarra_context = {
        "local_events": _get_local_events_impact(orders),
        "weather_correlation": _analyze_weather_impact(orders),
        "economic_cycles": _analyze_economic_cycles(orders)
    }
    
    return {
        "period": period,
        "trends": trends,
        "ibarra_context": ibarra_context,
        "predictions": DemandPredictor.predict_next_period(orders, period)
    }


@router.get("/optimization/pricing")
def get_pricing_optimization(
    item_id: Optional[int] = None,
    target_margin: float = Query(default=0.30, description="Target profit margin (0.30 = 30%)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Optimize pricing based on costs, demand, and competition
    """
    query = db.query(MenuItem)
    
    if item_id:
        query = query.filter(MenuItem.id == item_id)
    
    menu_items = query.all()
    
    optimization_results = []
    
    for item in menu_items:
        # Get order data for this item (simplified)
        # In real implementation, you'd need to parse order items JSON or have separate table
        
        current_margin = (item.price - item.cost) / item.price if item.price > 0 else 0
        optimal_price = BusinessOptimizer.calculate_optimal_price(
            cost=item.cost,
            current_price=item.price,
            target_margin=target_margin
        )
        
        optimization_results.append({
            "item_id": item.id,
            "item_name": item.name,
            "current_price": float(item.price),
            "current_cost": float(item.cost),
            "current_margin": round(current_margin * 100, 2),
            "optimal_price": float(optimal_price),
            "potential_margin": round(target_margin * 100, 2),
            "price_change_needed": float(optimal_price - item.price),
            "recommendations": BusinessOptimizer.get_pricing_recommendations(item.cost, item.price, target_margin)
        })
    
    return optimization_results


@router.get("/optimization/inventory")
def get_inventory_optimization(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Optimize inventory levels based on demand patterns
    """
    # This would require integration with inventory models
    # For now, return a placeholder structure
    
    return {
        "recommended_stock_levels": [],
        "reorder_points": [],
        "seasonal_adjustments": [],
        "cost_saving_opportunities": []
    }


@router.get("/optimization/staff")
def get_staff_optimization(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Optimize staff scheduling based on demand patterns
    """
    if not start_date:
        start_date = date.today() - timedelta(days=30)
    
    if not end_date:
        end_date = date.today()
    
    # Analyze order patterns by hour and day
    orders = db.query(Order).filter(
        and_(
            func.date(Order.created_at) >= start_date,
            func.date(Order.created_at) <= end_date,
            Order.status != "cancelled"
        )
    ).all()
    
    # Analyze demand by hour and day
    hourly_demand = {}
    daily_demand = {}
    
    for order in orders:
        hour = order.created_at.hour
        day_name = order.created_at.strftime('%A')
        
        if hour not in hourly_demand:
            hourly_demand[hour] = 0
        hourly_demand[hour] += 1
        
        if day_name not in daily_demand:
            daily_demand[day_name] = 0
        daily_demand[day_name] += 1
    
    # Get current staff performance
    staff_performance = db.query(StaffPerformance).join(Staff).filter(
        and_(
            StaffPerformance.period_start >= start_date,
            StaffPerformance.period_end <= end_date
        )
    ).all()
    
    optimization = BusinessOptimizer.optimize_staff_schedule(
        hourly_demand,
        daily_demand,
        staff_performance
    )
    
    return {
        "current_demand_patterns": {
            "hourly": hourly_demand,
            "daily": daily_demand
        },
        "optimization_recommendations": optimization,
        "cost_impact": _calculate_staff_cost_impact(optimization)
    }


@router.get("/predictions/sales")
def get_sales_predictions(
    prediction_days: int = Query(default=30, description="Days to predict ahead"),
    model_type: str = Query(default="trend", description="trend, seasonal, ml"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Predict future sales using various models
    """
    # Get historical data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)  # Use 90 days of history
    
    orders = db.query(Order).filter(
        and_(
            Order.created_at >= start_date,
            Order.created_at <= end_date,
            Order.status != "cancelled"
        )
    ).order_by(Order.created_at).all()
    
    predictions = DemandPredictor.predict_sales(
        orders=orders,
        prediction_days=prediction_days,
        model_type=model_type
    )
    
    return {
        "prediction_period": f"{prediction_days} days",
        "model_type": model_type,
        "historical_data_points": len(orders),
        "predictions": predictions,
        "confidence_intervals": DemandPredictor.calculate_confidence_intervals(orders, predictions),
        "business_insights": _generate_business_insights(predictions)
    }


@router.get("/kpis/dashboard")
def get_kpi_dashboard(
    period: str = Query(default="monthly", description="daily, weekly, monthly"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Get key performance indicators for dashboard
    """
    # Define period dates
    end_date = datetime.now()
    if period == "daily":
        start_date = end_date - timedelta(days=1)
    elif period == "weekly":
        start_date = end_date - timedelta(days=7)
    else:  # monthly
        start_date = end_date - timedelta(days=30)
    
    # Calculate KPIs
    orders = db.query(Order).filter(
        and_(
            Order.created_at >= start_date,
            Order.created_at <= end_date,
            Order.status != "cancelled"
        )
    ).all()
    
    if not orders:
        return _empty_kpi_dashboard()
    
    total_revenue = sum(order.total for order in orders)
    total_orders = len(orders)
    avg_order_value = total_revenue / total_orders
    total_costs = sum(order.ingredient_cost + order.packaging_cost + order.commission_amount for order in orders)
    net_profit = sum(order.net_profit for order in orders)
    
    # Platform breakdown
    platform_stats = {}
    for order in orders:
        platform = order.platform
        if platform not in platform_stats:
            platform_stats[platform] = {"orders": 0, "revenue": Decimal('0')}
        platform_stats[platform]["orders"] += 1
        platform_stats[platform]["revenue"] += order.total
    
    return {
        "period": period,
        "period_start": start_date,
        "period_end": end_date,
        "kpis": {
            "total_revenue": float(total_revenue),
            "total_orders": total_orders,
            "average_order_value": float(avg_order_value),
            "total_costs": float(total_costs),
            "net_profit": float(net_profit),
            "profit_margin": float(net_profit / total_revenue * 100) if total_revenue > 0 else 0,
            "cost_percentage": float(total_costs / total_revenue * 100) if total_revenue > 0 else 0
        },
        "platform_performance": {
            platform: {
                "orders": stats["orders"],
                "revenue": float(stats["revenue"]),
                "avg_order_value": float(stats["revenue"] / stats["orders"]) if stats["orders"] > 0 else 0
            }
            for platform, stats in platform_stats.items()
        },
        "growth_metrics": _calculate_growth_metrics(orders, period)
    }


# Helper functions
def _analyze_monthly_trends(orders: List[Order]) -> Dict:
    """Analyze monthly trends"""
    monthly_data = {}
    for order in orders:
        month_key = order.created_at.strftime('%Y-%m')
        if month_key not in monthly_data:
            monthly_data[month_key] = {"orders": 0, "revenue": Decimal('0')}
        monthly_data[month_key]["orders"] += 1
        monthly_data[month_key]["revenue"] += order.total
    
    return monthly_data


def _analyze_weekly_trends(orders: List[Order]) -> Dict:
    """Analyze weekly trends"""
    weekly_data = {}
    for order in orders:
        week_key = order.created_at.strftime('%Y-W%U')
        if week_key not in weekly_data:
            weekly_data[week_key] = {"orders": 0, "revenue": Decimal('0')}
        weekly_data[week_key]["orders"] += 1
        weekly_data[week_key]["revenue"] += order.total
    
    return weekly_data


def _analyze_daily_trends(orders: List[Order]) -> Dict:
    """Analyze daily trends"""
    daily_data = {}
    for order in orders:
        day_key = order.created_at.strftime('%Y-%m-%d')
        if day_key not in daily_data:
            daily_data[day_key] = {"orders": 0, "revenue": Decimal('0')}
        daily_data[day_key]["orders"] += 1
        daily_data[day_key]["revenue"] += order.total
    
    return daily_data


def _get_local_events_impact(orders: List[Order]) -> Dict:
    """Analyze impact of local events in Ibarra"""
    # This would integrate with local calendar data
    return {
        "festivals": "Analyze impact during Inti Raymi, Fiesta de los Lagos",
        "university_calendar": "University student patterns (UTN)",
        "payday_patterns": "15th and 30th salary patterns"
    }


def _analyze_weather_impact(orders: List[Order]) -> Dict:
    """Analyze weather correlation with orders"""
    # Would integrate with weather API
    return {
        "rainy_days": "Increased delivery orders during rain",
        "cold_weather": "Higher hot food demand"
    }


def _analyze_economic_cycles(orders: List[Order]) -> Dict:
    """Analyze economic cycle impact"""
    return {
        "monthly_cycles": "Payday impact on orders",
        "seasonal_spending": "Holiday and vacation patterns"
    }


def _calculate_staff_cost_impact(optimization: Dict) -> Dict:
    """Calculate cost impact of staff optimization"""
    return {
        "current_labor_cost": 0,
        "optimized_labor_cost": 0,
        "potential_savings": 0,
        "efficiency_gain": 0
    }


def _generate_business_insights(predictions: Dict) -> List[str]:
    """Generate actionable business insights from predictions"""
    insights = [
        "Consider increasing inventory for predicted high-demand periods",
        "Schedule additional staff during peak predicted times",
        "Prepare marketing campaigns for low-demand periods"
    ]
    return insights


def _empty_kpi_dashboard() -> Dict:
    """Return empty KPI dashboard structure"""
    return {
        "kpis": {
            "total_revenue": 0,
            "total_orders": 0,
            "average_order_value": 0,
            "total_costs": 0,
            "net_profit": 0,
            "profit_margin": 0,
            "cost_percentage": 0
        },
        "platform_performance": {},
        "growth_metrics": {}
    }


def _calculate_growth_metrics(orders: List[Order], period: str) -> Dict:
    """Calculate growth metrics compared to previous period"""
    # Simplified implementation - would compare with previous period
    return {
        "revenue_growth": 0,
        "order_growth": 0,
        "customer_growth": 0
    }