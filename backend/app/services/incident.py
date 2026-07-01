from sqlalchemy.orm import Session

from app.models.incident import Incident
from app.schemas.incident import IncidentCreate


def create_incident(
    db: Session,
    incident: IncidentCreate,
    user_id: int
):
    db_incident = Incident(
        title=incident.title,
        description=incident.description,
        severity=incident.severity,
        created_by=user_id
    )

    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)

    return db_incident


def get_all_incidents(db: Session):
    return db.query(Incident).all()


def get_incident_by_id(
    db: Session,
    incident_id: int
):
    return (
        db.query(Incident)
        .filter(Incident.id == incident_id)
        .first()
    )


def update_incident(
    db: Session,
    incident: Incident,
    data: dict
):
    for key, value in data.items():
        setattr(incident, key, value)

    db.commit()
    db.refresh(incident)

    return incident


def delete_incident(
    db: Session,
    incident: Incident
):
    db.delete(incident)
    db.commit()