from datetime import datetime

from pydantic import BaseModel


class AttachmentResponse(BaseModel):
    id: int
    incident_id: int
    uploaded_by: int
    filename: str
    filepath: str
    uploaded_at: datetime

    model_config = {
        "from_attributes": True
    }