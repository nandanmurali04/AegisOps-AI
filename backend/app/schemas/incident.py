from datetime import datetime
from pydantic import BaseModel


# -----------------------------
# Create Incident
# -----------------------------
class IncidentCreate(BaseModel):
    title: str
    description: str
    severity: str


# -----------------------------
# Update Incident
# -----------------------------
class IncidentUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    severity: str | None = None
    status: str | None = None
    assigned_to: int | None = None


# -----------------------------
# Assign Incident
# -----------------------------
class AssignIncident(BaseModel):
    assigned_to: int


# -----------------------------
# Response Model
# -----------------------------
class IncidentResponse(BaseModel):
    id: int
    title: str
    description: str
    severity: str
    status: str

    created_by: int
    assigned_to: int | None = None

    created_at: datetime

    class Config:
        from_attributes = True