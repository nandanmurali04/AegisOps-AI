from datetime import datetime
from pydantic import BaseModel


class IncidentCreate(BaseModel):
    title: str
    description: str
    severity: str


class IncidentUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    severity: str | None = None
    status: str | None = None


class IncidentResponse(BaseModel):
    id: int
    title: str
    description: str
    severity: str
    status: str
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True