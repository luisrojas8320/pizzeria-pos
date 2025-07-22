from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, Text, Boolean, JSON, ForeignKey, Date, Time
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base


class Staff(Base):
    __tablename__ = "staff"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_number = Column(String(20), unique=True, index=True, nullable=False)
    
    # Personal information
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    address = Column(Text, nullable=True)
    
    # Employment details
    position = Column(String(50), nullable=False)  # cook, assistant, delivery, cashier
    department = Column(String(50), nullable=False)  # kitchen, delivery, front
    hire_date = Column(Date, nullable=False)
    employment_status = Column(String(20), nullable=False, default="active")  # active, inactive, terminated
    
    # Schedule preferences
    preferred_days = Column(JSON, nullable=True)  # Array of day numbers [1,2,3] = Mon,Tue,Wed
    max_hours_per_week = Column(Integer, nullable=False, default=40)
    hourly_rate = Column(DECIMAL(8, 2), nullable=True)
    
    # Performance tracking
    performance_score = Column(DECIMAL(3, 2), nullable=True)  # 0.00-5.00
    total_orders_handled = Column(Integer, default=0)
    total_hours_worked = Column(DECIMAL(8, 2), default=0)
    
    # Skills and certifications
    skills = Column(JSON, nullable=True)  # Array of skill strings
    certifications = Column(JSON, nullable=True)  # Array of certification objects
    
    # Emergency contact
    emergency_contact_name = Column(String(100), nullable=True)
    emergency_contact_phone = Column(String(20), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class WorkSchedule(Base):
    __tablename__ = "work_schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    staff_id = Column(Integer, ForeignKey("staff.id"), nullable=False)
    
    # Schedule details
    schedule_date = Column(Date, nullable=False, index=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    
    # Break times
    break_start = Column(Time, nullable=True)
    break_end = Column(Time, nullable=True)
    
    # Schedule status
    status = Column(String(20), nullable=False, default="scheduled")  # scheduled, confirmed, completed, cancelled
    is_overtime = Column(Boolean, default=False)
    
    # Actual times (for time tracking)
    actual_start_time = Column(DateTime(timezone=True), nullable=True)
    actual_end_time = Column(DateTime(timezone=True), nullable=True)
    
    # Notes
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    staff_member = relationship("Staff", backref="schedules")


class StaffPerformance(Base):
    __tablename__ = "staff_performance"
    
    id = Column(Integer, primary_key=True, index=True)
    staff_id = Column(Integer, ForeignKey("staff.id"), nullable=False)
    
    # Performance period
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    
    # Metrics
    orders_handled = Column(Integer, default=0)
    hours_worked = Column(DECIMAL(8, 2), default=0)
    tardiness_count = Column(Integer, default=0)
    customer_ratings = Column(JSON, nullable=True)  # Array of rating objects
    
    # Quality metrics
    order_accuracy = Column(DECIMAL(5, 4), nullable=True)  # Percentage
    speed_score = Column(DECIMAL(3, 2), nullable=True)  # 1-5 scale
    teamwork_score = Column(DECIMAL(3, 2), nullable=True)  # 1-5 scale
    
    # Overall rating
    overall_score = Column(DECIMAL(3, 2), nullable=True)
    
    # Notes and feedback
    supervisor_notes = Column(Text, nullable=True)
    improvement_areas = Column(JSON, nullable=True)
    achievements = Column(JSON, nullable=True)
    
    # Review information
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    review_date = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    staff_member = relationship("Staff", backref="performance_reviews")
    reviewer = relationship("User")