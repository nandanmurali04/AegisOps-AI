from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.incident import (
    IncidentCreate,
    IncidentResponse,
    IncidentUpdate,
    AssignIncident,
)

from app.schemas.incident_log import IncidentLogResponse

from app.services.incident import (
    create_incident,
    get_all_incidents,
    get_incident_by_id,
    update_incident,
    assign_incident,
    delete_incident,
)

from app.services.incident_log import get_incident_logs

router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------
# Create Incident
# -------------------------
@router.post("/", response_model=IncidentResponse)
def create_new_incident(
    incident: IncidentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_incident(
        db=db,
        incident=incident,
        user_id=current_user.id
    )


# -------------------------
# Get All Incidents
# -------------------------
@router.get("/", response_model=list[IncidentResponse])
def get_incidents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_all_incidents(db)


# -------------------------
# Get One Incident
# -------------------------
@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident(
    incident_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    incident = get_incident_by_id(db, incident_id)

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return incident


# -------------------------
# Get Incident Logs
# -------------------------
@router.get(
    "/{incident_id}/logs",
    response_model=list[IncidentLogResponse]
)
def get_logs(
    incident_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    incident = get_incident_by_id(db, incident_id)

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return get_incident_logs(
        db,
        incident_id
    )


# -------------------------
# Update Incident
# -------------------------
@router.put("/{incident_id}", response_model=IncidentResponse)
def edit_incident(
    incident_id: int,
    incident_data: IncidentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    incident = get_incident_by_id(db, incident_id)

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    updated_data = incident_data.model_dump(exclude_unset=True)

    return update_incident(
        db,
        incident,
        updated_data
    )


# -------------------------
# Assign Incident
# -------------------------
@router.put("/{incident_id}/assign", response_model=IncidentResponse)
def assign_incident_to_user(
    incident_id: int,
    assignment: AssignIncident,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Only admins can assign incidents
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admins can assign incidents."
        )

    incident = get_incident_by_id(db, incident_id)

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    updated = assign_incident(
        db,
        incident,
        assignment.assigned_to
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Assigned user not found"
        )

    return updated


# -------------------------
# Delete Incident
# -------------------------
@router.delete("/{incident_id}")
def remove_incident(
    incident_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    incident = get_incident_by_id(db, incident_id)

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    delete_incident(db, incident)

    return {
        "message": "Incident deleted successfully"
    }