from datetime import datetime
from pydantic import BaseModel


class ActivityResponse(BaseModel):
    action: str
    performed_by: str
    timestamp: datetime

    class Config:
        from_attributes = True