import os
import shutil

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.attachment import Attachment


UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def save_attachment(
    db: Session,
    incident_id: int,
    user_id: int,
    file: UploadFile,
):
    filepath = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    attachment = Attachment(
        incident_id=incident_id,
        uploaded_by=user_id,
        filename=file.filename,
        filepath=filepath,
    )

    db.add(attachment)
    db.commit()
    db.refresh(attachment)

    return attachment


def get_attachments(
    db: Session,
    incident_id: int,
):
    return (
        db.query(Attachment)
        .filter(
            Attachment.incident_id == incident_id
        )
        .all()
    )