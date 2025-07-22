from typing import Any, List, Optional, Dict
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, func
from decimal import Decimal

from ..core.database import get_db
from ..core.auth import get_current_active_user_or_owner
from ..models.users import User
from ..models.orders import Order
from ..core.config import settings


router = APIRouter()


@router.get("/performance/")
def get_platform_performance(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    platform: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Analyze platform performance (Uber Eats, Pedidos Ya, Bis, etc.)
    """
    if not start_date:
        start_date = datetime.now() - timedelta(days=30)
    
    if not end_date:
        end_date = datetime.now()
    
    query = db.query(Order).filter(
        and_(
            Order.created_at >= start_date,
            Order.created_at <= end_date,
            Order.status != "cancelled"
        )
    )
    
    if platform:
        query = query.filter(Order.platform == platform)
    
    orders = query.all()
    
    # Group by platform
    platform_stats = {}
    for order in orders:
        platform_name = order.platform
        
        if platform_name not in platform_stats:
            platform_stats[platform_name] = {
                "orders": 0,
                "total_revenue": Decimal('0'),
                "total_commission": Decimal('0'),
                "net_revenue": Decimal('0'),
                "average_order_value": Decimal('0'),
                "commission_rate": settings.COMMISSION_RATES.get(platform_name, 0),
                "delivery_times": [],
                "customer_ratings": []
            }
        
        stats = platform_stats[platform_name]
        stats["orders"] += 1
        stats["total_revenue"] += order.total
        stats["total_commission"] += order.commission_amount
        stats["net_revenue"] += order.net_revenue
    
    # Calculate averages and additional metrics
    for platform_name, stats in platform_stats.items():
        if stats["orders"] > 0:
            stats["average_order_value"] = stats["total_revenue"] / stats["orders"]
            stats["commission_percentage"] = (stats["total_commission"] / stats["total_revenue"] * 100) if stats["total_revenue"] > 0 else 0
        
        # Convert Decimal to float for JSON serialization
        for key in ["total_revenue", "total_commission", "net_revenue", "average_order_value", "commission_percentage"]:
            if key in stats:
                stats[key] = float(stats[key])
    
    # Calculate overall performance metrics
    total_orders = sum(stats["orders"] for stats in platform_stats.values())
    total_revenue = sum(Decimal(str(stats["total_revenue"])) for stats in platform_stats.values())
    total_commission = sum(Decimal(str(stats["total_commission"])) for stats in platform_stats.values())
    
    performance_summary = {
        "period_start": start_date,
        "period_end": end_date,
        "total_orders": total_orders,
        "total_revenue": float(total_revenue),
        "total_commission_paid": float(total_commission),
        "overall_commission_rate": float(total_commission / total_revenue * 100) if total_revenue > 0 else 0,
        "platform_breakdown": platform_stats,
        "recommendations": _generate_platform_recommendations(platform_stats)
    }
    
    return performance_summary


@router.get("/commission/analysis")
def get_commission_analysis(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Detailed commission analysis across all platforms
    """
    if not start_date:
        start_date = datetime.now() - timedelta(days=30)
    
    if not end_date:
        end_date = datetime.now()
    
    orders = db.query(Order).filter(
        and_(
            Order.created_at >= start_date,
            Order.created_at <= end_date,
            Order.status != "cancelled"
        )
    ).all()
    
    commission_analysis = {}
    total_revenue = Decimal('0')
    total_commission = Decimal('0')
    
    for order in orders:
        platform = order.platform
        
        if platform not in commission_analysis:
            commission_analysis[platform] = {
                "orders": 0,
                "gross_revenue": Decimal('0'),
                "commission_paid": Decimal('0'),
                "net_revenue": Decimal('0'),
                "commission_rate": settings.COMMISSION_RATES.get(platform, 0),
                "potential_savings": Decimal('0')
            }
        
        stats = commission_analysis[platform]
        stats["orders"] += 1
        stats["gross_revenue"] += order.total
        stats["commission_paid"] += order.commission_amount
        stats["net_revenue"] += order.net_revenue
        
        total_revenue += order.total
        total_commission += order.commission_amount
    
    # Calculate potential savings if we could reduce commission rates
    for platform, stats in commission_analysis.items():
        current_rate = stats["commission_rate"]
        # Simulate 5% reduction in commission rate
        target_rate = max(0, current_rate - 0.05)
        potential_savings = stats["gross_revenue"] * (current_rate - target_rate)
        stats["potential_savings"] = potential_savings
        
        # Convert to float for JSON
        for key in ["gross_revenue", "commission_paid", "net_revenue", "potential_savings"]:
            stats[key] = float(stats[key])
    
    return {
        "period_start": start_date,
        "period_end": end_date,
        "total_gross_revenue": float(total_revenue),
        "total_commission_paid": float(total_commission),
        "overall_commission_rate": float(total_commission / total_revenue * 100) if total_revenue > 0 else 0,
        "platform_analysis": commission_analysis,
        "cost_optimization": {
            "total_potential_savings": float(sum(Decimal(str(stats["potential_savings"])) for stats in commission_analysis.values())),
            "recommendations": _generate_commission_optimization_recommendations(commission_analysis)
        }
    }


@router.get("/visibility/recommendations")
def get_visibility_recommendations(
    platform: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Get recommendations to improve platform visibility and performance
    """
    # Get recent performance data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    query = db.query(Order).filter(
        and_(
            Order.created_at >= start_date,
            Order.created_at <= end_date,
            Order.status != "cancelled"
        )
    )
    
    if platform:
        query = query.filter(Order.platform == platform)
    
    orders = query.all()
    
    # Analyze performance patterns
    platform_recommendations = {}
    
    platforms_to_analyze = [platform] if platform else ["uber_eats", "pedidos_ya", "bis", "phone", "whatsapp"]
    
    for platform_name in platforms_to_analyze:
        platform_orders = [o for o in orders if o.platform == platform_name]
        
        recommendations = []
        
        if not platform_orders:
            recommendations.append({
                "priority": "high",
                "category": "activation",
                "title": f"Activate {platform_name.replace('_', ' ').title()} presence",
                "description": "No orders found on this platform. Consider setting up or promoting your presence.",
                "expected_impact": "New revenue stream"
            })
        else:
            # Analyze order patterns
            avg_orders_per_day = len(platform_orders) / 30
            
            if avg_orders_per_day < 1:
                recommendations.append({
                    "priority": "medium",
                    "category": "promotion",
                    "title": "Increase marketing efforts",
                    "description": f"Low order frequency ({avg_orders_per_day:.1f} orders/day). Consider promotions or improved listings.",
                    "expected_impact": "Increased order volume"
                })
            
            # Check order value
            if platform_orders:
                avg_order_value = sum(order.total for order in platform_orders) / len(platform_orders)
                overall_avg = sum(order.total for order in orders) / len(orders) if orders else 0
                
                if avg_order_value < overall_avg * 0.9:
                    recommendations.append({
                        "priority": "medium",
                        "category": "upselling",
                        "title": "Improve order value",
                        "description": f"Average order value (${avg_order_value:.2f}) is below overall average. Consider bundle offers.",
                        "expected_impact": "Higher revenue per order"
                    })
            
            # Platform-specific recommendations
            if platform_name == "uber_eats":
                recommendations.extend(_get_uber_eats_recommendations(platform_orders))
            elif platform_name == "pedidos_ya":
                recommendations.extend(_get_pedidos_ya_recommendations(platform_orders))
            elif platform_name == "bis":
                recommendations.extend(_get_bis_recommendations(platform_orders))
            elif platform_name in ["phone", "whatsapp"]:
                recommendations.extend(_get_direct_channel_recommendations(platform_orders))
        
        platform_recommendations[platform_name] = {
            "total_orders": len(platform_orders),
            "recommendations": recommendations,
            "priority_actions": [r for r in recommendations if r["priority"] == "high"]
        }
    
    return {
        "analysis_period": f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
        "platform_recommendations": platform_recommendations,
        "general_recommendations": _get_general_visibility_recommendations(orders)
    }


@router.get("/integration/status")
def get_integration_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Check integration status with delivery platforms
    """
    # This would check API connections and data sync status
    # For now, return mock data
    
    integrations = {
        "uber_eats": {
            "status": "connected",
            "last_sync": datetime.now() - timedelta(minutes=5),
            "orders_today": _count_platform_orders("uber_eats", db),
            "issues": []
        },
        "pedidos_ya": {
            "status": "connected",
            "last_sync": datetime.now() - timedelta(minutes=3),
            "orders_today": _count_platform_orders("pedidos_ya", db),
            "issues": []
        },
        "bis": {
            "status": "connected",
            "last_sync": datetime.now() - timedelta(minutes=7),
            "orders_today": _count_platform_orders("bis", db),
            "issues": []
        },
        "phone_system": {
            "status": "connected",
            "last_sync": datetime.now() - timedelta(minutes=1),
            "orders_today": _count_platform_orders("phone", db),
            "issues": []
        }
    }
    
    return {
        "overall_status": "healthy",
        "integrations": integrations,
        "recommendations": [
            "All integrations are functioning properly",
            "Consider setting up automated alerts for integration failures"
        ]
    }


# Helper functions
def _generate_platform_recommendations(platform_stats: Dict) -> List[str]:
    """Generate recommendations based on platform performance"""
    recommendations = []
    
    # Find best and worst performing platforms
    if platform_stats:
        sorted_platforms = sorted(
            platform_stats.items(),
            key=lambda x: x[1]["net_revenue"],
            reverse=True
        )
        
        best_platform = sorted_platforms[0]
        worst_platform = sorted_platforms[-1]
        
        recommendations.append(f"Focus marketing efforts on {best_platform[0]} - your highest performing platform")
        
        if len(sorted_platforms) > 1:
            recommendations.append(f"Consider strategies to improve performance on {worst_platform[0]}")
        
        # Check for high commission platforms
        high_commission_platforms = [
            platform for platform, stats in platform_stats.items()
            if stats["commission_percentage"] > 25
        ]
        
        if high_commission_platforms:
            recommendations.append(f"High commission rates on {', '.join(high_commission_platforms)} - consider promoting direct orders")
    
    return recommendations


def _generate_commission_optimization_recommendations(commission_analysis: Dict) -> List[str]:
    """Generate recommendations for commission optimization"""
    recommendations = []
    
    # Find platforms with highest commission impact
    high_commission_platforms = [
        platform for platform, stats in commission_analysis.items()
        if stats["commission_rate"] > 0.25
    ]
    
    if high_commission_platforms:
        recommendations.append(f"Negotiate better rates with {', '.join(high_commission_platforms)}")
        recommendations.append("Promote direct ordering (WhatsApp/Phone) to reduce commission costs")
    
    recommendations.append("Consider implementing customer loyalty programs for direct orders")
    recommendations.append("Optimize menu pricing to account for platform commission differences")
    
    return recommendations


def _get_uber_eats_recommendations(orders: List[Order]) -> List[Dict]:
    """Get Uber Eats specific recommendations"""
    return [
        {
            "priority": "medium",
            "category": "optimization",
            "title": "Optimize Uber Eats listing",
            "description": "Update photos, descriptions, and ensure competitive pricing",
            "expected_impact": "Improved visibility and conversion"
        }
    ]


def _get_pedidos_ya_recommendations(orders: List[Order]) -> List[Dict]:
    """Get Pedidos Ya specific recommendations"""
    return [
        {
            "priority": "medium",
            "category": "promotion",
            "title": "Pedidos Ya promotions",
            "description": "Consider running targeted promotions during peak hours",
            "expected_impact": "Increased order frequency"
        }
    ]


def _get_bis_recommendations(orders: List[Order]) -> List[Dict]:
    """Get Bis specific recommendations"""
    return [
        {
            "priority": "low",
            "category": "expansion",
            "title": "Expand Bis presence",
            "description": "Bis is growing in Ecuador - consider increasing menu variety",
            "expected_impact": "Market share growth"
        }
    ]


def _get_direct_channel_recommendations(orders: List[Order]) -> List[Dict]:
    """Get recommendations for direct channels (phone/WhatsApp)"""
    return [
        {
            "priority": "high",
            "category": "promotion",
            "title": "Promote direct ordering",
            "description": "No commission fees on direct orders - offer incentives for WhatsApp/phone orders",
            "expected_impact": "Reduced commission costs"
        }
    ]


def _get_general_visibility_recommendations(orders: List[Order]) -> List[str]:
    """Get general recommendations for platform visibility"""
    return [
        "Maintain consistent branding across all platforms",
        "Respond quickly to customer reviews and feedback",
        "Update menu items and prices regularly",
        "Monitor competitor pricing and adjust accordingly",
        "Use high-quality food photography",
        "Optimize delivery times to improve platform rankings"
    ]


def _count_platform_orders(platform: str, db: Session) -> int:
    """Count orders for a platform today"""
    today = datetime.now().date()
    return db.query(Order).filter(
        and_(
            func.date(Order.created_at) == today,
            Order.platform == platform,
            Order.status != "cancelled"
        )
    ).count()