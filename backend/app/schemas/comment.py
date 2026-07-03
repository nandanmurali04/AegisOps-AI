from datetime import datetime

from pydantic import BaseModel


# -------------------------
# Create Comment
# -------------------------
class CommentCreate(BaseModel):
    comment: str


# -------------------------
# Response
# -------------------------
class CommentResponse(BaseModel):
    id: int
    incident_id: int
    user_id: int
    comment: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }