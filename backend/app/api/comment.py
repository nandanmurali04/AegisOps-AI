from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.comment import (
    CommentCreate,
    CommentResponse,
    CommentUpdate,
)
from app.services.comment import (
    create_comment,
    get_comments_by_incident,
    update_comment,
    delete_comment,
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
# ---------------------------------
# Add Comment
# ---------------------------------
@router.post(
    "/{incident_id}/comments",
    response_model=CommentResponse
)
def add_comment(
    incident_id: int,
    comment: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Check if incident exists
    incident = get_incident_by_id(
        db,
        incident_id
    )

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return create_comment(
        db=db,
        incident_id=incident_id,
        user_id=current_user.id,
        comment=comment.comment,
    )
# ---------------------------------
# Get Comments
# ---------------------------------
@router.get(
    "/{incident_id}/comments",
    response_model=list[CommentResponse]
)
def get_comments(
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

    return get_comments_by_incident(
        db,
        incident_id
    )
# ---------------------------------
# Update Comment
# ---------------------------------
@router.put(
    "/comments/{comment_id}",
    response_model=CommentResponse
)
def edit_comment(
    comment_id: int,
    updated_comment: CommentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    from app.models.comment import Comment

    comment = (
        db.query(Comment)
        .filter(Comment.id == comment_id)
        .first()
    )

    if comment is None:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )

    # Only the comment owner or an admin can edit
    if (
        comment.user_id != current_user.id
        and current_user.role != "admin"
    ):
        raise HTTPException(
            status_code=403,
            detail="Not authorized to edit this comment"
        )

    return update_comment(
        db,
        comment,
        updated_comment.comment
    )
# ---------------------------------
# Delete Comment
# ---------------------------------
@router.delete("/comments/{comment_id}")
def remove_comment(
    comment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    from app.models.comment import Comment

    comment = (
        db.query(Comment)
        .filter(Comment.id == comment_id)
        .first()
    )

    if comment is None:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )

    # Only the owner or an admin can delete
    if (
        comment.user_id != current_user.id
        and current_user.role != "admin"
    ):
        raise HTTPException(
            status_code=403,
            detail="Not authorized to delete this comment"
        )

    delete_comment(
        db,
        comment
    )

    return {
        "message": "Comment deleted successfully"
    }