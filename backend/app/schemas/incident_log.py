from datetime import datetime
from pydantic import BaseModel


class IncidentLogResponse(BaseModel):
    id: int
    incident_id: int
    performed_by: int
    action: str
    timestamp: datetime

    class Config:
        from_attributes = True