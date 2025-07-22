from typing import List, Dict, Any
from decimal import Decimal
from ..core.config import settings
from ..schemas.orders import OrderItemCreate


class FinancialCalculator:
    """
    Financial calculations for the POS system
    """
    
    @staticmethod
    def calculate_packaging_cost(items: List[OrderItemCreate]) -> Decimal:
        """
        Calculate packaging cost based on order items
        This is a simplified calculation - in reality you'd need more complex logic
        """
        total_quantity = sum(item.quantity for item in items)
        
        # Assume basic packaging cost per item
        if total_quantity <= 2:
            return Decimal(str(settings.PACKAGING_COSTS["small_box"]))
        elif total_quantity <= 4:
            return Decimal(str(settings.PACKAGING_COSTS["medium_box"]))
        else:
            return Decimal(str(settings.PACKAGING_COSTS["large_box"]))
    
    @staticmethod
    def calculate_commission(total: Decimal, platform: str) -> Dict[str, Decimal]:
        """
        Calculate commission based on platform
        """
        commission_rate = Decimal(str(settings.COMMISSION_RATES.get(platform, 0)))
        commission_amount = total * commission_rate
        
        return {
            "rate": commission_rate,
            "amount": commission_amount,
            "net_amount": total - commission_amount
        }
    
    @staticmethod
    def calculate_ingredient_cost(recipe: List[Dict[str, Any]], quantity: int) -> Decimal:
        """
        Calculate ingredient cost based on recipe and quantity
        """
        # This would need to query the inventory table for current ingredient costs
        # For now, return a placeholder
        return Decimal('0')
    
    @staticmethod
    def calculate_profit_margin(revenue: Decimal, costs: Decimal) -> Decimal:
        """
        Calculate profit margin percentage
        """
        if revenue == 0:
            return Decimal('0')
        
        profit = revenue - costs
        margin = (profit / revenue) * 100
        return margin.quantize(Decimal('0.01'))
    
    @staticmethod
    def calculate_food_cost_percentage(ingredient_cost: Decimal, revenue: Decimal) -> Decimal:
        """
        Calculate food cost as percentage of revenue
        """
        if revenue == 0:
            return Decimal('0')
        
        percentage = (ingredient_cost / revenue) * 100
        return percentage.quantize(Decimal('0.01'))
    
    @staticmethod
    def optimize_pricing(current_price: Decimal, cost: Decimal, target_margin: Decimal) -> Decimal:
        """
        Calculate optimal price based on cost and target margin
        Target margin should be in decimal form (e.g., 0.30 for 30%)
        """
        optimal_price = cost / (1 - target_margin)
        return optimal_price.quantize(Decimal('0.01'))
    
    @staticmethod
    def calculate_break_even_quantity(fixed_costs: Decimal, unit_price: Decimal, variable_cost: Decimal) -> int:
        """
        Calculate break-even quantity for a product
        """
        if unit_price <= variable_cost:
            return 0  # Cannot break even
        
        contribution_margin = unit_price - variable_cost
        break_even_qty = fixed_costs / contribution_margin
        return int(break_even_qty.to_integral_value())
    
    @staticmethod
    def analyze_order_profitability(order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive order profitability analysis
        """
        total_revenue = Decimal(str(order_data.get('total', 0)))
        ingredient_cost = Decimal(str(order_data.get('ingredient_cost', 0)))
        packaging_cost = Decimal(str(order_data.get('packaging_cost', 0)))
        commission_amount = Decimal(str(order_data.get('commission_amount', 0)))
        
        total_costs = ingredient_cost + packaging_cost + commission_amount
        gross_profit = total_revenue - total_costs
        
        # Calculate various metrics
        profit_margin = FinancialCalculator.calculate_profit_margin(total_revenue, total_costs)
        food_cost_percentage = FinancialCalculator.calculate_food_cost_percentage(ingredient_cost, total_revenue)
        
        return {
            "total_revenue": total_revenue,
            "total_costs": total_costs,
            "gross_profit": gross_profit,
            "profit_margin_percentage": profit_margin,
            "food_cost_percentage": food_cost_percentage,
            "commission_percentage": (commission_amount / total_revenue * 100) if total_revenue > 0 else Decimal('0'),
            "packaging_cost_percentage": (packaging_cost / total_revenue * 100) if total_revenue > 0 else Decimal('0')
        }
    
    @staticmethod
    def calculate_customer_lifetime_value(
        average_order_value: Decimal,
        order_frequency_per_month: Decimal,
        customer_lifespan_months: int,
        profit_margin: Decimal
    ) -> Decimal:
        """
        Calculate Customer Lifetime Value (CLV)
        """
        monthly_value = average_order_value * order_frequency_per_month * profit_margin
        clv = monthly_value * customer_lifespan_months
        return clv.quantize(Decimal('0.01'))
    
    @staticmethod
    def calculate_inventory_turnover(
        cost_of_goods_sold: Decimal,
        average_inventory_value: Decimal
    ) -> Decimal:
        """
        Calculate inventory turnover ratio
        """
        if average_inventory_value == 0:
            return Decimal('0')
        
        turnover = cost_of_goods_sold / average_inventory_value
        return turnover.quantize(Decimal('0.01'))