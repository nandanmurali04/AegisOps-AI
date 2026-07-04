import os
import shutil

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.attachment import Attachment
from app.services.incident_log import create_log


UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------------------------
# Upload Attachment
# ---------------------------------
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

    # Create Audit Log
    create_log(
        db=db,
        incident_id=incident_id,
        user_id=user_id,
        action="Attachment Uploaded"
    )

    return attachment


# ---------------------------------
# Get Attachments
# ---------------------------------
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


# ---------------------------------
# Get Attachment By ID
# ---------------------------------
def get_attachment_by_id(
    db: Session,
    attachment_id: int,
):
    return (
        db.query(Attachment)
        .filter(Attachment.id == attachment_id)
        .first()
    )


# ---------------------------------
# Delete Attachment
# ---------------------------------
def delete_attachment(
    db: Session,
    attachment: Attachment,
    user_id: int,
):
    if os.path.exists(attachment.filepath):
        os.remove(attachment.filepath)

    # Create Audit Log
    create_log(
        db=db,
        incident_id=attachment.incident_id,
        user_id=user_id,
        action="Attachment Deleted"
    )

    db.delete(attachment)
    db.commit()