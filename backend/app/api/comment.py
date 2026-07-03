from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.comment import (
    CommentCreate,
    CommentResponse,
)

from app.services.comment import (
    create_comment,
    get_comments_by_incident,
)

from app.services.incident import get_incident_by_id

router = APIRouter(
    prefix="/incidents",
    tags=["Comments"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()