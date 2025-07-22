from typing import List, Dict, Any, Tuple
from decimal import Decimal
from datetime import datetime, timedelta


class BusinessOptimizer:
    """
    Business optimization algorithms for Delizzia POS
    """
    
    @staticmethod
    def calculate_optimal_price(
        cost: Decimal, 
        current_price: Decimal, 
        target_margin: float,
        demand_elasticity: float = -0.5
    ) -> Decimal:
        """
        Calculate optimal price based on cost and target margin
        Considers demand elasticity for price sensitivity
        """
        # Basic optimal price calculation
        optimal_price = cost / (1 - target_margin)
        
        # Adjust for demand elasticity
        if current_price > 0:
            price_change_ratio = optimal_price / current_price
            demand_impact = 1 + (demand_elasticity * (price_change_ratio - 1))
            
            # If demand impact is too negative, moderate the price increase
            if demand_impact < 0.7:  # If demand would drop more than 30%
                optimal_price = current_price * 1.1  # Max 10% increase
        
        return optimal_price.quantize(Decimal('0.01'))
    
    @staticmethod
    def get_pricing_recommendations(
        cost: Decimal, 
        current_price: Decimal, 
        target_margin: float
    ) -> List[str]:
        """
        Get pricing recommendations based on current vs optimal pricing
        """
        recommendations = []
        current_margin = (current_price - cost) / current_price if current_price > 0 else 0
        optimal_price = BusinessOptimizer.calculate_optimal_price(cost, current_price, target_margin)
        
        if optimal_price > current_price:
            increase_percent = ((optimal_price - current_price) / current_price * 100) if current_price > 0 else 0
            if increase_percent > 20:
                recommendations.append(f"Consider gradual price increases over time instead of immediate {increase_percent:.1f}% increase")
            else:
                recommendations.append(f"Price increase of {increase_percent:.1f}% recommended to reach target margin")
        
        elif optimal_price < current_price:
            decrease_percent = ((current_price - optimal_price) / current_price * 100) if current_price > 0 else 0
            recommendations.append(f"Current price may be too high - consider {decrease_percent:.1f}% reduction")
        
        if current_margin < 0.15:  # Less than 15% margin
            recommendations.append("Very low margin - review cost structure or increase price")
        elif current_margin > 0.5:  # More than 50% margin
            recommendations.append("High margin - consider competitive pricing or promotions")
        
        return recommendations
    
    @staticmethod
    def optimize_staff_schedule(
        hourly_demand: Dict[int, int],
        daily_demand: Dict[str, int],
        staff_performance: List[Any]
    ) -> Dict[str, Any]:
        """
        Optimize staff scheduling based on demand patterns
        """
        # Find peak hours
        peak_hours = sorted(hourly_demand.items(), key=lambda x: x[1], reverse=True)[:3]
        low_hours = sorted(hourly_demand.items(), key=lambda x: x[1])[:3]
        
        # Find peak days
        peak_days = sorted(daily_demand.items(), key=lambda x: x[1], reverse=True)[:2]
        low_days = sorted(daily_demand.items(), key=lambda x: x[1])[:2]
        
        recommendations = []
        
        # Peak hour staffing
        for hour, orders in peak_hours:
            hour_str = f"{hour:02d}:00"
            recommendations.append({
                "type": "staffing",
                "time": hour_str,
                "action": "increase",
                "reason": f"Peak hour with {orders} orders",
                "impact": "Improved service speed and customer satisfaction"
            })
        
        # Low hour optimization
        for hour, orders in low_hours:
            hour_str = f"{hour:02d}:00"
            if orders < 2:  # Very low demand
                recommendations.append({
                    "type": "staffing",
                    "time": hour_str,
                    "action": "reduce",
                    "reason": f"Low demand with only {orders} orders",
                    "impact": "Reduced labor costs"
                })
        
        # Day-based recommendations
        for day, orders in peak_days:
            recommendations.append({
                "type": "scheduling",
                "time": day,
                "action": "increase",
                "reason": f"High demand day with {orders} orders",
                "impact": "Better coverage during busy periods"
            })
        
        # Staff performance optimization
        if staff_performance:
            high_performers = [sp for sp in staff_performance if sp.overall_score and sp.overall_score > 4.0]
            recommendations.append({
                "type": "performance",
                "action": "utilize_top_performers",
                "reason": f"{len(high_performers)} high-performing staff members identified",
                "impact": "Schedule top performers during peak times"
            })
        
        return {
            "peak_hours": [f"{h:02d}:00" for h, _ in peak_hours],
            "low_hours": [f"{h:02d}:00" for h, _ in low_hours],
            "peak_days": [day for day, _ in peak_days],
            "recommendations": recommendations,
            "estimated_efficiency_gain": BusinessOptimizer._calculate_efficiency_gain(recommendations)
        }
    
    @staticmethod
    def optimize_menu_mix(
        item_performance: List[Dict[str, Any]],
        target_food_cost_percentage: float = 0.30
    ) -> Dict[str, Any]:
        """
        Optimize menu mix based on profitability and popularity
        """
        if not item_performance:
            return {"recommendations": [], "categories": {}}
        
        # Categorize items based on popularity and profitability
        categories = {
            "stars": [],      # High popularity, high profit
            "plowhorses": [], # High popularity, low profit
            "puzzles": [],    # Low popularity, high profit
            "dogs": []        # Low popularity, low profit
        }
        
        # Calculate median values for categorization
        popularities = [item.get("order_count", 0) for item in item_performance]
        profits = [item.get("profit_margin", 0) for item in item_performance]
        
        if popularities and profits:
            median_popularity = sorted(popularities)[len(popularities) // 2]
            median_profit = sorted(profits)[len(profits) // 2]
            
            for item in item_performance:
                popularity = item.get("order_count", 0)
                profit = item.get("profit_margin", 0)
                
                if popularity >= median_popularity and profit >= median_profit:
                    categories["stars"].append(item)
                elif popularity >= median_popularity and profit < median_profit:
                    categories["plowhorses"].append(item)
                elif popularity < median_popularity and profit >= median_profit:
                    categories["puzzles"].append(item)
                else:
                    categories["dogs"].append(item)
        
        recommendations = []
        
        # Stars: Promote and maintain
        for item in categories["stars"]:
            recommendations.append({
                "item": item["name"],
                "category": "star",
                "action": "promote",
                "reason": "High profit and popularity",
                "suggestion": "Feature prominently, consider upselling"
            })
        
        # Plowhorses: Improve profitability
        for item in categories["plowhorses"]:
            recommendations.append({
                "item": item["name"],
                "category": "plowhorse",
                "action": "optimize_cost",
                "reason": "Popular but low profit",
                "suggestion": "Reduce costs or increase price carefully"
            })
        
        # Puzzles: Increase popularity
        for item in categories["puzzles"]:
            recommendations.append({
                "item": item["name"],
                "category": "puzzle",
                "action": "promote",
                "reason": "Profitable but unpopular",
                "suggestion": "Market more aggressively, improve description/photo"
            })
        
        # Dogs: Consider removal or major changes
        for item in categories["dogs"]:
            recommendations.append({
                "item": item["name"],
                "category": "dog",
                "action": "evaluate_removal",
                "reason": "Low profit and popularity",
                "suggestion": "Consider removing or major recipe/price revision"
            })
        
        return {
            "categories": {
                "stars": len(categories["stars"]),
                "plowhorses": len(categories["plowhorses"]),
                "puzzles": len(categories["puzzles"]),
                "dogs": len(categories["dogs"])
            },
            "recommendations": recommendations,
            "menu_optimization_score": BusinessOptimizer._calculate_menu_score(categories)
        }
    
    @staticmethod
    def optimize_inventory_levels(
        inventory_data: List[Dict[str, Any]],
        demand_forecast: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Optimize inventory levels based on demand patterns and costs
        """
        recommendations = []
        
        for item in inventory_data:
            current_stock = item.get("current_stock", 0)
            min_threshold = item.get("min_threshold", 0)
            usage_rate = item.get("daily_usage", 0)
            lead_time_days = item.get("supplier_lead_time", 3)
            
            # Calculate optimal stock levels
            safety_stock = usage_rate * lead_time_days * 1.5  # 50% safety buffer
            reorder_point = usage_rate * lead_time_days + safety_stock
            optimal_order_quantity = BusinessOptimizer._calculate_eoq(
                annual_demand=usage_rate * 365,
                order_cost=item.get("order_cost", 10),
                holding_cost=item.get("holding_cost", 2)
            )
            
            if current_stock < reorder_point:
                recommendations.append({
                    "item": item["name"],
                    "action": "reorder",
                    "current_stock": current_stock,
                    "reorder_point": reorder_point,
                    "suggested_quantity": optimal_order_quantity,
                    "urgency": "high" if current_stock < min_threshold else "medium"
                })
        
        return {
            "recommendations": recommendations,
            "total_items_to_reorder": len([r for r in recommendations if r["action"] == "reorder"]),
            "high_priority_items": len([r for r in recommendations if r.get("urgency") == "high"])
        }
    
    @staticmethod
    def optimize_delivery_zones(
        delivery_data: List[Dict[str, Any]],
        driver_capacity: int = 5
    ) -> Dict[str, Any]:
        """
        Optimize delivery zones and routing for Ibarra
        """
        # Group deliveries by zone/neighborhood
        zones = {}
        for delivery in delivery_data:
            zone = delivery.get("zone", "unknown")
            if zone not in zones:
                zones[zone] = {
                    "orders": 0,
                    "avg_delivery_time": 0,
                    "total_distance": 0,
                    "revenue": 0
                }
            
            zones[zone]["orders"] += 1
            zones[zone]["avg_delivery_time"] += delivery.get("delivery_time", 30)
            zones[zone]["total_distance"] += delivery.get("distance", 5)
            zones[zone]["revenue"] += delivery.get("order_value", 20)
        
        # Calculate zone efficiency metrics
        zone_analysis = []
        for zone, data in zones.items():
            if data["orders"] > 0:
                avg_time = data["avg_delivery_time"] / data["orders"]
                avg_distance = data["total_distance"] / data["orders"]
                avg_revenue = data["revenue"] / data["orders"]
                
                efficiency_score = avg_revenue / (avg_time + avg_distance)
                
                zone_analysis.append({
                    "zone": zone,
                    "orders": data["orders"],
                    "avg_delivery_time": round(avg_time, 1),
                    "avg_distance": round(avg_distance, 1),
                    "avg_revenue": round(avg_revenue, 2),
                    "efficiency_score": round(efficiency_score, 3)
                })
        
        # Sort by efficiency
        zone_analysis.sort(key=lambda x: x["efficiency_score"], reverse=True)
        
        recommendations = []
        
        # High efficiency zones
        for zone in zone_analysis[:3]:
            recommendations.append({
                "zone": zone["zone"],
                "action": "prioritize",
                "reason": f"High efficiency score: {zone['efficiency_score']}",
                "suggestion": "Allocate more delivery capacity, consider delivery fee reduction"
            })
        
        # Low efficiency zones
        for zone in zone_analysis[-2:]:
            if zone["efficiency_score"] < 0.5:
                recommendations.append({
                    "zone": zone["zone"],
                    "action": "optimize",
                    "reason": f"Low efficiency score: {zone['efficiency_score']}",
                    "suggestion": "Increase delivery fee, batch orders, or limit delivery times"
                })
        
        return {
            "zone_analysis": zone_analysis,
            "recommendations": recommendations,
            "optimal_zones": len([z for z in zone_analysis if z["efficiency_score"] > 1.0])
        }
    
    @staticmethod
    def _calculate_eoq(annual_demand: float, order_cost: float, holding_cost: float) -> int:
        """
        Calculate Economic Order Quantity (EOQ)
        """
        if holding_cost <= 0:
            return int(annual_demand / 12)  # Monthly supply as fallback
        
        eoq = ((2 * annual_demand * order_cost) / holding_cost) ** 0.5
        return max(1, int(eoq))
    
    @staticmethod
    def _calculate_efficiency_gain(recommendations: List[Dict[str, Any]]) -> float:
        """
        Estimate efficiency gain from staff optimization recommendations
        """
        # Simplified calculation - in reality would be more complex
        base_score = 0.0
        
        for rec in recommendations:
            if rec["type"] == "staffing":
                if rec["action"] == "increase":
                    base_score += 5.0  # 5% efficiency gain
                elif rec["action"] == "reduce":
                    base_score += 3.0  # 3% cost savings
            elif rec["type"] == "performance":
                base_score += 10.0  # 10% gain from using top performers
        
        return min(base_score, 30.0)  # Cap at 30% maximum gain
    
    @staticmethod
    def _calculate_menu_score(categories: Dict[str, List]) -> float:
        """
        Calculate overall menu optimization score
        """
        total_items = sum(len(items) for items in categories.values())
        if total_items == 0:
            return 0
        
        # Ideal distribution: 25% stars, 35% plowhorses, 20% puzzles, 20% dogs
        stars_pct = len(categories["stars"]) / total_items
        score = stars_pct * 100  # Higher percentage of stars = better score
        
        return min(score, 100.0)