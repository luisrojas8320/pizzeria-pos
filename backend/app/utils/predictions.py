from typing import List, Dict, Any
from datetime import datetime, timedelta
from decimal import Decimal
import statistics
from ..models.orders import Order


class DemandPredictor:
    """
    Demand prediction algorithms for Delizzia POS
    """
    
    @staticmethod
    def predict_sales(
        orders: List[Order], 
        prediction_days: int = 30, 
        model_type: str = "trend"
    ) -> Dict[str, Any]:
        """
        Predict future sales using various models
        """
        if not orders:
            return DemandPredictor._empty_prediction(prediction_days)
        
        if model_type == "trend":
            return DemandPredictor._trend_based_prediction(orders, prediction_days)
        elif model_type == "seasonal":
            return DemandPredictor._seasonal_prediction(orders, prediction_days)
        elif model_type == "ml":
            return DemandPredictor._ml_based_prediction(orders, prediction_days)
        else:
            return DemandPredictor._simple_average_prediction(orders, prediction_days)
    
    @staticmethod
    def _trend_based_prediction(orders: List[Order], prediction_days: int) -> Dict[str, Any]:
        """
        Predict based on historical trend analysis
        """
        # Group orders by day
        daily_sales = {}
        for order in orders:
            date_key = order.created_at.date()
            if date_key not in daily_sales:
                daily_sales[date_key] = {"orders": 0, "revenue": Decimal('0')}
            daily_sales[date_key]["orders"] += 1
            daily_sales[date_key]["revenue"] += order.total
        
        # Calculate trend
        sorted_dates = sorted(daily_sales.keys())
        if len(sorted_dates) < 2:
            return DemandPredictor._simple_average_prediction(orders, prediction_days)
        
        # Simple linear trend calculation
        revenues = [float(daily_sales[date]["revenue"]) for date in sorted_dates]
        order_counts = [daily_sales[date]["orders"] for date in sorted_dates]
        
        # Calculate trend slope
        n = len(revenues)
        x_values = list(range(n))
        
        # Linear regression for revenue trend
        revenue_slope = DemandPredictor._calculate_slope(x_values, revenues)
        revenue_intercept = statistics.mean(revenues) - revenue_slope * statistics.mean(x_values)
        
        # Linear regression for order count trend  
        order_slope = DemandPredictor._calculate_slope(x_values, order_counts)
        order_intercept = statistics.mean(order_counts) - order_slope * statistics.mean(x_values)
        
        # Generate predictions
        predictions = []
        last_date = sorted_dates[-1]
        
        for i in range(1, prediction_days + 1):
            prediction_date = last_date + timedelta(days=i)
            
            # Project trend
            predicted_revenue = revenue_intercept + revenue_slope * (n + i - 1)
            predicted_orders = int(max(0, order_intercept + order_slope * (n + i - 1)))
            
            # Apply business context adjustments
            adjusted_revenue, adjusted_orders = DemandPredictor._apply_business_context(
                prediction_date, predicted_revenue, predicted_orders
            )
            
            predictions.append({
                "date": prediction_date,
                "predicted_revenue": round(adjusted_revenue, 2),
                "predicted_orders": adjusted_orders,
                "confidence": DemandPredictor._calculate_confidence(i, prediction_days)
            })
        
        return {
            "model": "trend_based",
            "historical_days": len(sorted_dates),
            "trend_slope_revenue": round(revenue_slope, 2),
            "trend_slope_orders": round(order_slope, 2),
            "predictions": predictions
        }
    
    @staticmethod
    def _seasonal_prediction(orders: List[Order], prediction_days: int) -> Dict[str, Any]:
        """
        Predict based on seasonal patterns
        """
        # Group by day of week and hour
        weekly_patterns = {}
        hourly_patterns = {}
        
        for order in orders:
            day_of_week = order.created_at.weekday()  # 0=Monday, 6=Sunday
            hour = order.created_at.hour
            
            if day_of_week not in weekly_patterns:
                weekly_patterns[day_of_week] = {"orders": 0, "revenue": Decimal('0')}
            weekly_patterns[day_of_week]["orders"] += 1
            weekly_patterns[day_of_week]["revenue"] += order.total
            
            if hour not in hourly_patterns:
                hourly_patterns[hour] = {"orders": 0, "revenue": Decimal('0')}
            hourly_patterns[hour]["orders"] += 1
            hourly_patterns[hour]["revenue"] += order.total
        
        # Calculate averages
        total_weeks = len(orders) / 7 if len(orders) > 7 else 1
        
        for day_pattern in weekly_patterns.values():
            day_pattern["avg_orders"] = day_pattern["orders"] / total_weeks
            day_pattern["avg_revenue"] = day_pattern["revenue"] / total_weeks
        
        # Generate seasonal predictions
        predictions = []
        base_date = datetime.now().date()
        
        for i in range(prediction_days):
            prediction_date = base_date + timedelta(days=i + 1)
            day_of_week = prediction_date.weekday()
            
            if day_of_week in weekly_patterns:
                pattern = weekly_patterns[day_of_week]
                predicted_orders = int(pattern["avg_orders"])
                predicted_revenue = float(pattern["avg_revenue"])
            else:
                # Use overall average if no pattern data
                avg_orders = sum(p["orders"] for p in weekly_patterns.values()) / len(weekly_patterns)
                avg_revenue = sum(float(p["revenue"]) for p in weekly_patterns.values()) / len(weekly_patterns)
                predicted_orders = int(avg_orders)
                predicted_revenue = avg_revenue
            
            # Apply business context
            adjusted_revenue, adjusted_orders = DemandPredictor._apply_business_context(
                prediction_date, predicted_revenue, predicted_orders
            )
            
            predictions.append({
                "date": prediction_date,
                "predicted_revenue": round(adjusted_revenue, 2),
                "predicted_orders": adjusted_orders,
                "day_of_week": prediction_date.strftime('%A'),
                "confidence": DemandPredictor._calculate_confidence(i + 1, prediction_days)
            })
        
        return {
            "model": "seasonal",
            "weekly_patterns": {str(k): {"avg_orders": round(v["avg_orders"], 1), "avg_revenue": round(float(v["avg_revenue"]), 2)} for k, v in weekly_patterns.items()},
            "predictions": predictions
        }
    
    @staticmethod
    def _ml_based_prediction(orders: List[Order], prediction_days: int) -> Dict[str, Any]:
        """
        Machine learning based prediction (simplified)
        In production, this would use scikit-learn or similar
        """
        # For now, combine trend and seasonal approaches
        trend_pred = DemandPredictor._trend_based_prediction(orders, prediction_days)
        seasonal_pred = DemandPredictor._seasonal_prediction(orders, prediction_days)
        
        # Ensemble prediction (weighted average)
        predictions = []
        for i in range(prediction_days):
            trend_day = trend_pred["predictions"][i]
            seasonal_day = seasonal_pred["predictions"][i]
            
            # Weight: 60% trend, 40% seasonal
            combined_revenue = trend_day["predicted_revenue"] * 0.6 + seasonal_day["predicted_revenue"] * 0.4
            combined_orders = int(trend_day["predicted_orders"] * 0.6 + seasonal_day["predicted_orders"] * 0.4)
            
            predictions.append({
                "date": trend_day["date"],
                "predicted_revenue": round(combined_revenue, 2),
                "predicted_orders": combined_orders,
                "confidence": (trend_day["confidence"] + seasonal_day["confidence"]) / 2
            })
        
        return {
            "model": "ml_ensemble",
            "components": ["trend", "seasonal"],
            "weights": {"trend": 0.6, "seasonal": 0.4},
            "predictions": predictions
        }
    
    @staticmethod
    def _simple_average_prediction(orders: List[Order], prediction_days: int) -> Dict[str, Any]:
        """
        Simple average-based prediction
        """
        if not orders:
            return DemandPredictor._empty_prediction(prediction_days)
        
        total_revenue = sum(order.total for order in orders)
        total_orders = len(orders)
        days_with_data = len(set(order.created_at.date() for order in orders))
        
        avg_daily_revenue = float(total_revenue) / days_with_data if days_with_data > 0 else 0
        avg_daily_orders = total_orders / days_with_data if days_with_data > 0 else 0
        
        predictions = []
        base_date = datetime.now().date()
        
        for i in range(prediction_days):
            prediction_date = base_date + timedelta(days=i + 1)
            
            predictions.append({
                "date": prediction_date,
                "predicted_revenue": round(avg_daily_revenue, 2),
                "predicted_orders": int(avg_daily_orders),
                "confidence": 0.5  # Medium confidence for simple average
            })
        
        return {
            "model": "simple_average",
            "avg_daily_revenue": round(avg_daily_revenue, 2),
            "avg_daily_orders": int(avg_daily_orders),
            "predictions": predictions
        }
    
    @staticmethod
    def predict_next_period(orders: List[Order], period: str) -> Dict[str, Any]:
        """
        Predict the next period based on historical patterns
        """
        if period == "daily":
            return DemandPredictor.predict_sales(orders, 7, "seasonal")
        elif period == "weekly":
            return DemandPredictor.predict_sales(orders, 30, "trend")
        elif period == "monthly":
            return DemandPredictor.predict_sales(orders, 90, "ml")
        else:
            return DemandPredictor.predict_sales(orders, 30, "trend")
    
    @staticmethod
    def calculate_confidence_intervals(orders: List[Order], predictions: Dict) -> Dict[str, Any]:
        """
        Calculate confidence intervals for predictions
        """
        if not orders or not predictions.get("predictions"):
            return {"lower_bound": [], "upper_bound": []}
        
        # Calculate historical variance
        daily_revenues = {}
        for order in orders:
            date_key = order.created_at.date()
            if date_key not in daily_revenues:
                daily_revenues[date_key] = 0
            daily_revenues[date_key] += float(order.total)
        
        revenues = list(daily_revenues.values())
        if len(revenues) < 2:
            return {"lower_bound": [], "upper_bound": []}
        
        variance = statistics.variance(revenues)
        std_dev = variance ** 0.5
        
        confidence_intervals = {
            "lower_bound": [],
            "upper_bound": []
        }
        
        for pred in predictions["predictions"]:
            predicted_value = pred["predicted_revenue"]
            confidence = pred.get("confidence", 0.8)
            
            # Adjust interval based on confidence
            interval_width = std_dev * (2 - confidence)  # Wider intervals for lower confidence
            
            confidence_intervals["lower_bound"].append(max(0, predicted_value - interval_width))
            confidence_intervals["upper_bound"].append(predicted_value + interval_width)
        
        return confidence_intervals
    
    @staticmethod
    def _calculate_slope(x_values: List[float], y_values: List[float]) -> float:
        """Calculate slope for linear regression"""
        n = len(x_values)
        if n < 2:
            return 0
        
        x_mean = statistics.mean(x_values)
        y_mean = statistics.mean(y_values)
        
        numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, y_values))
        denominator = sum((x - x_mean) ** 2 for x in x_values)
        
        return numerator / denominator if denominator != 0 else 0
    
    @staticmethod
    def _apply_business_context(date, revenue: float, orders: int) -> tuple:
        """
        Apply Ibarra-specific business context to predictions
        """
        # Day of week adjustments
        weekday = date.weekday()
        if weekday in [4, 5]:  # Friday, Saturday
            revenue *= 1.3  # Higher weekend demand
            orders = int(orders * 1.3)
        elif weekday == 6:  # Sunday
            revenue *= 0.8  # Lower Sunday demand
            orders = int(orders * 0.8)
        
        # Monthly cycles (payday effect)
        day_of_month = date.day
        if day_of_month in [15, 30, 31]:  # Payday periods
            revenue *= 1.2
            orders = int(orders * 1.2)
        
        # University calendar effects (UTN students)
        # This would be more sophisticated with actual calendar integration
        
        return revenue, orders
    
    @staticmethod
    def _calculate_confidence(days_ahead: int, total_days: int) -> float:
        """
        Calculate confidence level based on prediction distance
        """
        # Confidence decreases with prediction distance
        base_confidence = 0.9
        decay_factor = 0.02
        confidence = base_confidence * (1 - decay_factor * days_ahead)
        return max(0.1, confidence)  # Minimum 10% confidence
    
    @staticmethod
    def _empty_prediction(prediction_days: int) -> Dict[str, Any]:
        """Return empty prediction structure"""
        base_date = datetime.now().date()
        predictions = []
        
        for i in range(prediction_days):
            predictions.append({
                "date": base_date + timedelta(days=i + 1),
                "predicted_revenue": 0,
                "predicted_orders": 0,
                "confidence": 0
            })
        
        return {
            "model": "empty",
            "predictions": predictions
        }