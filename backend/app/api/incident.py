from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.incident import (
    IncidentCreate,
    IncidentResponse,
    IncidentUpdate,
)
from app.services.incident import (
    create_incident,
    get_all_incidents,
    get_incident_by_id,
    update_incident,
    delete_incident,
)

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

    updated_data = incident_data.model_dump(
        exclude_unset=True
    )

    return update_incident(
        db,
        incident,
        updated_data
    )


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