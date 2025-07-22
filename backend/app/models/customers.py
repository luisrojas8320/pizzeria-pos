from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, Text, Boolean, JSON, Date
from sqlalchemy.sql import func
from ..core.database import Base


class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Customer identification (unified across platforms)
    phone = Column(String(20), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    
    # Address information
    addresses = Column(JSON, nullable=True)  # Array of address objects with delivery instructions
    
    # Platform presence
    platforms = Column(JSON, nullable=True)  # Object with platform IDs {uber_eats: "id123", whatsapp: "phone"}
    
    # Order statistics
    total_orders = Column(Integer, default=0)
    total_spent = Column(DECIMAL(10, 2), default=0)
    average_order_value = Column(DECIMAL(10, 2), default=0)
    
    # Preferences
    favorite_items = Column(JSON, nullable=True)  # Array of menu item IDs with frequency
    dietary_restrictions = Column(JSON, nullable=True)  # Array of restrictions
    preferred_platforms = Column(JSON, nullable=True)  # Array of platform preferences
    
    # Behavioral data
    order_frequency = Column(String(20), nullable=True)  # daily, weekly, monthly, occasional
    preferred_order_times = Column(JSON, nullable=True)  # Array of hour ranges
    loyalty_score = Column(DECIMAL(5, 2), default=0)  # 0-100 scale
    
    # Customer service
    notes = Column(Text, nullable=True)
    is_vip = Column(Boolean, default=False)
    complaints_count = Column(Integer, default=0)
    
    # Marketing
    marketing_consent = Column(Boolean, default=False)
    last_promotion_sent = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    first_order_date = Column(DateTime(timezone=True), nullable=True)
    last_order_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class CustomerFeedback(Base):
    __tablename__ = "customer_feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=True)  # Can be null for anonymous feedback
    order_id = Column(Integer, nullable=True)  # Related order if applicable
    
    # Feedback details
    rating = Column(Integer, nullable=False)  # 1-5 scale
    category = Column(String(50), nullable=False)  # food_quality, delivery_time, service, etc.
    feedback_text = Column(Text, nullable=True)
    
    # Response
    response_text = Column(Text, nullable=True)
    responded_by = Column(String(100), nullable=True)
    response_date = Column(DateTime(timezone=True), nullable=True)
    
    # Platform information
    platform = Column(String(50), nullable=True)
    platform_feedback_id = Column(String(100), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class MarketingCampaign(Base):
    __tablename__ = "marketing_campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    
    # Campaign details
    campaign_type = Column(String(50), nullable=False)  # promotion, retention, acquisition
    channels = Column(JSON, nullable=False)  # Array of channels: whatsapp, email, sms
    
    # Target audience
    target_criteria = Column(JSON, nullable=False)  # Criteria for targeting customers
    estimated_reach = Column(Integer, nullable=True)
    
    # Campaign content
    message_template = Column(Text, nullable=False)
    offer_details = Column(JSON, nullable=True)  # Discount, free item, etc.
    
    # Schedule
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    
    # Performance metrics
    sent_count = Column(Integer, default=0)
    opened_count = Column(Integer, default=0)
    clicked_count = Column(Integer, default=0)
    converted_count = Column(Integer, default=0)
    revenue_generated = Column(DECIMAL(10, 2), default=0)
    
    # Status
    status = Column(String(20), default="draft")  # draft, active, completed, cancelled
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())