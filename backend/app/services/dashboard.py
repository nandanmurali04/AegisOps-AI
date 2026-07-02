from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.incident import Incident
from app.models.user import User


def get_dashboard_stats(db: Session):
    total_incidents = db.query(func.count(Incident.id)).scalar()

    open_incidents = (
        db.query(func.count(Incident.id))
        .filter(Incident.status == "Open")
        .scalar()
    )

    resolved_incidents = (
        db.query(func.count(Incident.id))
        .filter(Incident.status == "Resolved")
        .scalar()
    )

    critical_incidents = (
        db.query(func.count(Incident.id))
        .filter(Incident.severity == "Critical")
        .scalar()
    )

    return {
        "total_incidents": total_incidents,
        "open_incidents": open_incidents,
        "resolved_incidents": resolved_incidents,
        "critical_incidents": critical_incidents,
    }
def get_severity_stats(db: Session):
    result = (
        db.query(
            Incident.severity,
            func.count(Incident.id)
        )
        .group_by(Incident.severity)
        .all()
    )

    stats = {
        "Critical": 0,
        "High": 0,
        "Medium": 0,
        "Low": 0,
    }

    for severity, count in result:
        stats[severity] = count

    return stats

def get_status_stats(db: Session):
    result = (
        db.query(
            Incident.status,
            func.count(Incident.id)
        )
        .group_by(Incident.status)
        .all()
    )

    stats = {
        "Open": 0,
        "Resolved": 0,
        "In_Progress": 0,
    }

    for status, count in result:
        if status == "In Progress":
            stats["In_Progress"] = count
        else:
            stats[status] = count

    return stats

def get_user_incident_stats(db: Session):
    result = (
        db.query(
            User.full_name,
            func.count(Incident.id)
        )
        .join(
            Incident,
            Incident.created_by == User.id
        )
        .group_by(User.full_name)
        .all()
    )

    return [
        {
            "user": name,
            "incident_count": count
        }
        for name, count in result
    ]