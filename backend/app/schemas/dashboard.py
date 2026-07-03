from pydantic import BaseModel
from datetime import datetime


class DashboardResponse(BaseModel):
    total_incidents: int
    open_incidents: int
    resolved_incidents: int
    critical_incidents: int


class SeverityStats(BaseModel):
    Critical: int
    High: int
    Medium: int
    Low: int

class StatusStats(BaseModel):
    Open: int
    Resolved: int
    In_Progress: int

class UserIncidentStats(BaseModel):
    user: str
    incident_count: int

class ActivityResponse(BaseModel):
    incident_id: int
    performed_by: int
    action: str
    timestamp: datetime