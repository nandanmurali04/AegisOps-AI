from sqlalchemy.orm import Session

from app.models.comment import Comment
from app.services.incident_log import create_log


# ---------------------------------
# Create Comment
# ---------------------------------
def create_comment(
    db: Session,
    incident_id: int,
    user_id: int,
    comment: str,
):
    db_comment = Comment(
        incident_id=incident_id,
        user_id=user_id,
        comment=comment,
    )

    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)

    # Create Audit Log
    create_log(
        db=db,
        incident_id=incident_id,
        user_id=user_id,
        action="Comment Added"
    )

    return db_comment


# ---------------------------------
# Get Comments By Incident
# ---------------------------------
def get_comments_by_incident(
    db: Session,
    incident_id: int,
):
    return (
        db.query(Comment)
        .filter(Comment.incident_id == incident_id)
        .order_by(Comment.created_at.asc())
        .all()
    )


# ---------------------------------
# Update Comment
# ---------------------------------
def update_comment(
    db: Session,
    comment: Comment,
    new_text: str,
    user_id: int,
):
    comment.comment = new_text

    db.commit()
    db.refresh(comment)

    # Create Audit Log
    create_log(
        db=db,
        incident_id=comment.incident_id,
        user_id=user_id,
        action="Comment Updated"
    )

    return comment


# ---------------------------------
# Delete Comment
# ---------------------------------
def delete_comment(
    db: Session,
    comment: Comment,
    user_id: int,
):
    # Create Audit Log
    create_log(
        db=db,
        incident_id=comment.incident_id,
        user_id=user_id,
        action="Comment Deleted"
    )

    db.delete(comment)
    db.commit()