from typing import Any, List, Optional
from datetime import datetime, date, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_

from ..core.database import get_db
from ..core.auth import get_current_active_user_or_owner, get_current_active_owner
from ..models.users import User
from ..models.staff import Staff, WorkSchedule, StaffPerformance


router = APIRouter()


@router.get("/")
def read_staff(
    skip: int = 0,
    limit: int = 100,
    employment_status: Optional[str] = None,
    position: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Retrieve staff members
    """
    query = db.query(Staff)
    
    if employment_status:
        query = query.filter(Staff.employment_status == employment_status)
    
    if position:
        query = query.filter(Staff.position == position)
    
    staff = query.order_by(Staff.first_name, Staff.last_name).offset(skip).limit(limit).all()
    return staff


@router.get("/{staff_id}")
def read_staff_member(
    staff_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Get staff member by ID
    """
    staff = db.query(Staff).filter(Staff.id == staff_id).first()
    if not staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Staff member not found"
        )
    return staff


@router.get("/schedules/weekly")
def get_weekly_staff_schedule(
    week_start: Optional[date] = Query(default=None, description="Start of week (Monday)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Get weekly staff schedule
    """
    if not week_start:
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
    
    week_end = week_start + timedelta(days=6)
    
    # Get schedules for the week
    schedules = db.query(WorkSchedule).join(Staff).filter(
        and_(
            WorkSchedule.schedule_date >= week_start,
            WorkSchedule.schedule_date <= week_end,
            Staff.employment_status == "active"
        )
    ).order_by(WorkSchedule.schedule_date, WorkSchedule.start_time).all()
    
    # Group by date
    weekly_schedule = {}
    current_date = week_start
    while current_date <= week_end:
        date_str = current_date.strftime('%Y-%m-%d')
        daily_schedules = [s for s in schedules if s.schedule_date == current_date]
        
        weekly_schedule[date_str] = [
            {
                "staff_id": schedule.staff_id,
                "staff_name": f"{schedule.staff_member.first_name} {schedule.staff_member.last_name}",
                "position": schedule.staff_member.position,
                "start_time": schedule.start_time.strftime('%H:%M'),
                "end_time": schedule.end_time.strftime('%H:%M'),
                "status": schedule.status
            }
            for schedule in daily_schedules
        ]
        
        current_date += timedelta(days=1)
    
    return weekly_schedule


@router.get("/performance/summary")
def get_staff_performance_summary(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_owner)
) -> Any:
    """
    Get staff performance summary
    """
    if not start_date:
        start_date = date.today() - timedelta(days=30)
    
    if not end_date:
        end_date = date.today()
    
    # Get performance data
    performance_data = db.query(StaffPerformance).join(Staff).filter(
        and_(
            StaffPerformance.period_start >= start_date,
            StaffPerformance.period_end <= end_date,
            Staff.employment_status == "active"
        )
    ).all()
    
    summary = []
    for perf in performance_data:
        summary.append({
            "staff_id": perf.staff_id,
            "staff_name": f"{perf.staff_member.first_name} {perf.staff_member.last_name}",
            "position": perf.staff_member.position,
            "overall_score": float(perf.overall_score) if perf.overall_score else None,
            "orders_handled": perf.orders_handled,
            "hours_worked": float(perf.hours_worked),
            "order_accuracy": float(perf.order_accuracy) if perf.order_accuracy else None
        })
    
    return summary


@router.get("/analytics/utilization")
def get_staff_utilization(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_or_owner)
) -> Any:
    """
    Get staff utilization analytics
    """
    if not start_date:
        start_date = date.today() - timedelta(days=30)
    
    if not end_date:
        end_date = date.today()
    
    # Get active staff
    staff_members = db.query(Staff).filter(Staff.employment_status == "active").all()
    
    utilization_data = []
    for staff in staff_members:
        # Get schedules for the period
        schedules = db.query(WorkSchedule).filter(
            and_(
                WorkSchedule.staff_id == staff.id,
                WorkSchedule.schedule_date >= start_date,
                WorkSchedule.schedule_date <= end_date
            )
        ).all()
        
        total_scheduled_hours = 0
        total_worked_hours = 0
        
        for schedule in schedules:
            # Calculate scheduled hours
            start_datetime = datetime.combine(schedule.schedule_date, schedule.start_time)
            end_datetime = datetime.combine(schedule.schedule_date, schedule.end_time)
            scheduled_hours = (end_datetime - start_datetime).total_seconds() / 3600
            total_scheduled_hours += scheduled_hours
            
            # Calculate actual worked hours if available
            if schedule.actual_start_time and schedule.actual_end_time:
                worked_hours = (schedule.actual_end_time - schedule.actual_start_time).total_seconds() / 3600
                total_worked_hours += worked_hours
        
        utilization_rate = (total_worked_hours / total_scheduled_hours * 100) if total_scheduled_hours > 0 else 0
        
        utilization_data.append({
            "staff_id": staff.id,
            "staff_name": f"{staff.first_name} {staff.last_name}",
            "position": staff.position,
            "scheduled_hours": total_scheduled_hours,
            "worked_hours": total_worked_hours,
            "utilization_rate": round(utilization_rate, 2)
        })
    
    return utilization_data