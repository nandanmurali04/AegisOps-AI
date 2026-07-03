from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.attachment import AttachmentResponse

from app.services.attachment import (
    save_attachment,
    get_attachments,
)

from app.services.incident import get_incident_by_id

router = APIRouter(
    prefix="/incidents",
    tags=["Attachments"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------
# Upload Attachment
# ---------------------------------
@router.post(
    "/{incident_id}/attachments",
    response_model=AttachmentResponse
)
def upload_attachment(
    incident_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    incident = get_incident_by_id(
        db,
        incident_id
    )

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return save_attachment(
        db=db,
        incident_id=incident_id,
        user_id=current_user.id,
        file=file,
    )


# ---------------------------------
# Get Attachments
# ---------------------------------
@router.get(
    "/{incident_id}/attachments",
    response_model=list[AttachmentResponse]
)
def list_attachments(
    incident_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    incident = get_incident_by_id(
        db,
        incident_id
    )

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return get_attachments(
        db,
        incident_id
    )