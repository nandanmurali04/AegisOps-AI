from sqlalchemy.orm import Session

from app.models.incident_log import IncidentLog
from app.schemas.activity import ActivityResponse


def get_activity_timeline(
    db: Session,
    incident_id: int,
):
    logs = (
        db.query(IncidentLog)
        .filter(IncidentLog.incident_id == incident_id)
        .order_by(IncidentLog.timestamp.asc())
        .all()
    )

    activity = []

    for log in logs:
        activity.append(
            ActivityResponse(
                action=log.action,
                performed_by=log.user.full_name,
                timestamp=log.timestamp
            )
        )

    return activity