from sqlalchemy.orm import Session

from app.models.incident_log import IncidentLog


# ----------------------------
# Create Audit Log
# ----------------------------
def create_log(
    db: Session,
    incident_id: int,
    user_id: int,
    action: str
):
    log = IncidentLog(
        incident_id=incident_id,
        performed_by=user_id,
        action=action
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log


# ----------------------------
# Get Logs for an Incident
# ----------------------------
def get_incident_logs(
    db: Session,
    incident_id: int
):
    return (
        db.query(IncidentLog)
        .filter(IncidentLog.incident_id == incident_id)
        .order_by(IncidentLog.timestamp.desc())
        .all()
    )