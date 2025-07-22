from typing import List, Dict, Any, Optional
from datetime import datetime, date, timedelta
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc

from ..models.orders import Order, OrderItem
from ..models.menu import MenuItem
from ..schemas.orders import OrderCreate, DailySalesReport, WeeklySalesReport, MonthlySalesReport
from ..core.config import settings
from ..services.calculations import FinancialCalculator


class OrderService:
    
    @staticmethod
    def create_order(db: Session, order_data: OrderCreate, user_id: int) -> Order:
        """
        Create a new order with financial calculations
        """
        # Generate order number
        order_count = db.query(func.count(Order.id)).scalar()
        order_number = f"ORD{datetime.now().strftime('%Y%m%d')}{order_count + 1:04d}"
        
        # Calculate order totals
        subtotal = Decimal('0')
        total_ingredient_cost = Decimal('0')
        
        # Get menu items and calculate costs
        for item_data in order_data.items:
            menu_item = db.query(MenuItem).filter(MenuItem.id == item_data.menu_item_id).first()
            if not menu_item:
                raise ValueError(f"Menu item {item_data.menu_item_id} not found")
            
            if not menu_item.is_available:
                raise ValueError(f"Menu item {menu_item.name} is not available")
            
            item_total = item_data.unit_price * item_data.quantity
            subtotal += item_total
            total_ingredient_cost += menu_item.cost * item_data.quantity
        
        # Calculate packaging cost (simplified calculation)
        packaging_cost = FinancialCalculator.calculate_packaging_cost(order_data.items)
        
        # Calculate tax (if applicable)
        tax_amount = Decimal('0')  # Ecuador doesn't typically charge tax on food delivery
        
        # Calculate total
        total = subtotal + tax_amount + order_data.delivery_fee
        
        # Calculate commission based on platform
        commission_rate = Decimal(str(settings.COMMISSION_RATES.get(order_data.platform.value, 0)))
        commission_amount = total * commission_rate
        
        # Calculate net revenue and profit
        net_revenue = total - commission_amount
        net_profit = net_revenue - total_ingredient_cost - packaging_cost
        
        # Create order
        db_order = Order(
            order_number=order_number,
            customer_name=order_data.customer_name,
            customer_phone=order_data.customer_phone,
            customer_address=order_data.customer_address,
            platform=order_data.platform,
            platform_order_id=order_data.platform_order_id,
            payment_method=order_data.payment_method,
            items=[item.dict() for item in order_data.items],  # Store as JSON
            subtotal=subtotal,
            tax_amount=tax_amount,
            delivery_fee=order_data.delivery_fee,
            total=total,
            ingredient_cost=total_ingredient_cost,
            packaging_cost=packaging_cost,
            commission_rate=commission_rate,
            commission_amount=commission_amount,
            net_revenue=net_revenue,
            net_profit=net_profit,
            created_by=user_id
        )
        
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        
        return db_order
    
    @staticmethod
    def get_daily_sales_report(db: Session, report_date: date) -> DailySalesReport:
        """
        Generate daily sales report
        """
        start_datetime = datetime.combine(report_date, datetime.min.time())
        end_datetime = datetime.combine(report_date, datetime.max.time())
        
        # Get orders for the day
        orders = db.query(Order).filter(
            and_(
                Order.created_at >= start_datetime,
                Order.created_at <= end_datetime,
                Order.status != "cancelled"
            )
        ).all()
        
        if not orders:
            return DailySalesReport(
                period_start=start_datetime,
                period_end=end_datetime,
                total_orders=0,
                total_revenue=Decimal('0'),
                total_costs=Decimal('0'),
                total_profit=Decimal('0'),
                average_order_value=Decimal('0'),
                platform_breakdown={},
                top_items=[],
                hourly_breakdown={}
            )
        
        # Calculate totals
        total_orders = len(orders)
        total_revenue = sum(order.total for order in orders)
        total_costs = sum(order.ingredient_cost + order.packaging_cost + order.commission_amount for order in orders)
        total_profit = sum(order.net_profit for order in orders)
        average_order_value = total_revenue / total_orders if total_orders > 0 else Decimal('0')
        
        # Platform breakdown
        platform_breakdown = {}
        for order in orders:
            platform = order.platform
            if platform not in platform_breakdown:
                platform_breakdown[platform] = {
                    'orders': 0,
                    'revenue': Decimal('0'),
                    'commission': Decimal('0')
                }
            platform_breakdown[platform]['orders'] += 1
            platform_breakdown[platform]['revenue'] += order.total
            platform_breakdown[platform]['commission'] += order.commission_amount
        
        # Hourly breakdown
        hourly_breakdown = {}
        for order in orders:
            hour = order.created_at.hour
            hour_key = f"{hour:02d}:00"
            if hour_key not in hourly_breakdown:
                hourly_breakdown[hour_key] = {
                    'orders': 0,
                    'revenue': Decimal('0')
                }
            hourly_breakdown[hour_key]['orders'] += 1
            hourly_breakdown[hour_key]['revenue'] += order.total
        
        # Top items (simplified - would need proper item tracking)
        top_items = OrderService._get_top_items_for_period(db, start_datetime, end_datetime)
        
        return DailySalesReport(
            period_start=start_datetime,
            period_end=end_datetime,
            total_orders=total_orders,
            total_revenue=total_revenue,
            total_costs=total_costs,
            total_profit=total_profit,
            average_order_value=average_order_value,
            platform_breakdown=platform_breakdown,
            top_items=top_items,
            hourly_breakdown=hourly_breakdown
        )
    
    @staticmethod
    def get_weekly_sales_report(db: Session, start_date: date) -> WeeklySalesReport:
        """
        Generate weekly sales report
        """
        end_date = start_date + timedelta(days=6)
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())
        
        # Get orders for the week
        orders = db.query(Order).filter(
            and_(
                Order.created_at >= start_datetime,
                Order.created_at <= end_datetime,
                Order.status != "cancelled"
            )
        ).all()
        
        # Calculate similar to daily report but with daily breakdown
        total_orders = len(orders)
        total_revenue = sum(order.total for order in orders) if orders else Decimal('0')
        total_costs = sum(order.ingredient_cost + order.packaging_cost + order.commission_amount for order in orders) if orders else Decimal('0')
        total_profit = sum(order.net_profit for order in orders) if orders else Decimal('0')
        average_order_value = total_revenue / total_orders if total_orders > 0 else Decimal('0')
        
        # Daily breakdown
        daily_breakdown = {}
        current_date = start_date
        while current_date <= end_date:
            day_key = current_date.strftime('%Y-%m-%d')
            day_orders = [o for o in orders if o.created_at.date() == current_date]
            daily_breakdown[day_key] = {
                'orders': len(day_orders),
                'revenue': sum(order.total for order in day_orders) if day_orders else Decimal('0')
            }
            current_date += timedelta(days=1)
        
        platform_breakdown = {}
        for order in orders:
            platform = order.platform
            if platform not in platform_breakdown:
                platform_breakdown[platform] = {
                    'orders': 0,
                    'revenue': Decimal('0'),
                    'commission': Decimal('0')
                }
            platform_breakdown[platform]['orders'] += 1
            platform_breakdown[platform]['revenue'] += order.total
            platform_breakdown[platform]['commission'] += order.commission_amount
        
        top_items = OrderService._get_top_items_for_period(db, start_datetime, end_datetime)
        
        return WeeklySalesReport(
            period_start=start_datetime,
            period_end=end_datetime,
            total_orders=total_orders,
            total_revenue=total_revenue,
            total_costs=total_costs,
            total_profit=total_profit,
            average_order_value=average_order_value,
            platform_breakdown=platform_breakdown,
            top_items=top_items,
            daily_breakdown=daily_breakdown
        )
    
    @staticmethod
    def get_monthly_sales_report(db: Session, year: int, month: int) -> MonthlySalesReport:
        """
        Generate monthly sales report
        """
        from calendar import monthrange
        
        start_date = date(year, month, 1)
        end_date = date(year, month, monthrange(year, month)[1])
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())
        
        # Get orders for the month
        orders = db.query(Order).filter(
            and_(
                Order.created_at >= start_datetime,
                Order.created_at <= end_datetime,
                Order.status != "cancelled"
            )
        ).all()
        
        total_orders = len(orders)
        total_revenue = sum(order.total for order in orders) if orders else Decimal('0')
        total_costs = sum(order.ingredient_cost + order.packaging_cost + order.commission_amount for order in orders) if orders else Decimal('0')
        total_profit = sum(order.net_profit for order in orders) if orders else Decimal('0')
        average_order_value = total_revenue / total_orders if total_orders > 0 else Decimal('0')
        
        # Weekly breakdown
        weekly_breakdown = {}
        current_date = start_date
        week_num = 1
        while current_date <= end_date:
            week_start = current_date
            week_end = min(current_date + timedelta(days=6), end_date)
            week_key = f"Week {week_num}"
            
            week_orders = [o for o in orders if week_start <= o.created_at.date() <= week_end]
            weekly_breakdown[week_key] = {
                'orders': len(week_orders),
                'revenue': sum(order.total for order in week_orders) if week_orders else Decimal('0')
            }
            
            current_date = week_end + timedelta(days=1)
            week_num += 1
        
        platform_breakdown = {}
        for order in orders:
            platform = order.platform
            if platform not in platform_breakdown:
                platform_breakdown[platform] = {
                    'orders': 0,
                    'revenue': Decimal('0'),
                    'commission': Decimal('0')
                }
            platform_breakdown[platform]['orders'] += 1
            platform_breakdown[platform]['revenue'] += order.total
            platform_breakdown[platform]['commission'] += order.commission_amount
        
        top_items = OrderService._get_top_items_for_period(db, start_datetime, end_datetime)
        
        return MonthlySalesReport(
            period_start=start_datetime,
            period_end=end_datetime,
            total_orders=total_orders,
            total_revenue=total_revenue,
            total_costs=total_costs,
            total_profit=total_profit,
            average_order_value=average_order_value,
            platform_breakdown=platform_breakdown,
            top_items=top_items,
            weekly_breakdown=weekly_breakdown
        )
    
    @staticmethod
    def _get_top_items_for_period(db: Session, start_datetime: datetime, end_datetime: datetime) -> List[Dict[str, Any]]:
        """
        Get top items for a given period
        """
        # This is a simplified implementation
        # In a real implementation, you'd need to parse the JSON items field
        # or have a separate order_items table
        return []
    
    @staticmethod
    def get_popular_items(db: Session, limit: int, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        Get most popular menu items
        """
        # Simplified implementation - would need proper item tracking
        return []
    
    @staticmethod
    def get_platform_performance(db: Session, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Get platform performance analytics
        """
        query = db.query(Order).filter(Order.status != "cancelled")
        
        if start_date:
            query = query.filter(Order.created_at >= start_date)
        
        if end_date:
            query = query.filter(Order.created_at <= end_date)
        
        orders = query.all()
        
        platform_stats = {}
        for order in orders:
            platform = order.platform
            if platform not in platform_stats:
                platform_stats[platform] = {
                    'orders': 0,
                    'revenue': Decimal('0'),
                    'commission_paid': Decimal('0'),
                    'net_revenue': Decimal('0'),
                    'average_order_value': Decimal('0')
                }
            
            stats = platform_stats[platform]
            stats['orders'] += 1
            stats['revenue'] += order.total
            stats['commission_paid'] += order.commission_amount
            stats['net_revenue'] += order.net_revenue
        
        # Calculate averages
        for platform, stats in platform_stats.items():
            if stats['orders'] > 0:
                stats['average_order_value'] = stats['revenue'] / stats['orders']
        
        return platform_stats