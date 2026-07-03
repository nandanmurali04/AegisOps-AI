from sqlalchemy.orm import Session

from app.models.comment import Comment


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
    comment,
    new_text: str
):
    comment.comment = new_text

    db.commit()
    db.refresh(comment)

    return comment
# ---------------------------------
# Delete Comment
# ---------------------------------
def delete_comment(
    db: Session,
    comment
):
    db.delete(comment)
    db.commit()