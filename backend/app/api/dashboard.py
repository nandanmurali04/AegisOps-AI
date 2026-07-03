from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.dashboard import (
    DashboardResponse,
    SeverityStats,
    StatusStats,
    UserIncidentStats,
    ActivityResponse,
)

from app.services.dashboard import (
    get_dashboard_stats,
    get_severity_stats,
    get_status_stats,
    get_user_incident_stats,
    get_recent_activity,
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------
# Dashboard Statistics
# ---------------------------------
@router.get("/", response_model=DashboardResponse)
def dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_dashboard_stats(db)
# ---------------------------------
# Severity Analytics
# ---------------------------------
@router.get("/severity", response_model=SeverityStats)
def severity_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_severity_stats(db)
# ---------------------------------
# Status Analytics
# ---------------------------------
@router.get("/status", response_model=StatusStats)
def status_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_status_stats(db)

# ---------------------------------
# User Incident Analytics
# ---------------------------------
@router.get("/users", response_model=list[UserIncidentStats])
def user_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_user_incident_stats(db)

# ---------------------------------
# Recent Activity
# ---------------------------------
@router.get("/activity", response_model=list[ActivityResponse])
def recent_activity(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_recent_activity(db)