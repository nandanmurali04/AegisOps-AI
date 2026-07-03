from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.incident import Incident
from app.models.user import User
from app.schemas.incident import IncidentCreate
from app.services.incident_log import create_log


# ---------------------------------
# Create Incident
# ---------------------------------
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

    # Create Audit Log
    create_log(
        db=db,
        incident_id=db_incident.id,
        user_id=user_id,
        action="Created"
    )

    return db_incident


# ---------------------------------
# Get All Incidents
# ---------------------------------
def get_all_incidents(
    db: Session,
    status: str = None,
    severity: str = None,
    search: str = None,
    page: int = 1,
    limit: int = 10,
):
    query = db.query(Incident)

    if status:
        query = query.filter(
            Incident.status.ilike(status)
        )

    if severity:
        query = query.filter(
            Incident.severity.ilike(severity)
        )

    if search:
        query = query.filter(
            or_(
                Incident.title.ilike(f"%{search}%"),
                Incident.description.ilike(f"%{search}%")
            )
        )

    offset = (page - 1) * limit

    return (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

# ---------------------------------
# Get Incident By ID
# ---------------------------------
def get_incident_by_id(
    db: Session,
    incident_id: int
):
    return (
        db.query(Incident)
        .filter(Incident.id == incident_id)
        .first()
    )


# ---------------------------------
# Update Incident
# ---------------------------------
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


# ---------------------------------
# Assign Incident
# ---------------------------------
def assign_incident(
    db: Session,
    incident: Incident,
    user_id: int
):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        return None

    incident.assigned_to = user_id

    db.commit()
    db.refresh(incident)

    # Create Audit Log
    create_log(
        db=db,
        incident_id=incident.id,
        user_id=user_id,
        action="Assigned"
    )

    return incident


# ---------------------------------
# Delete Incident
# ---------------------------------
def delete_incident(
    db: Session,
    incident: Incident
):
    db.delete(incident)
    db.commit()