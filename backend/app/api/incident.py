from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
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
from app.utils.security import verify_access_token

router = APIRouter(prefix="/incidents", tags=["Incidents"])

security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=IncidentResponse)
def create_new_incident(
    incident: IncidentCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    payload = verify_access_token(credentials.credentials)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = payload.get("id")

    return create_incident(db, incident, user_id)


@router.get("/", response_model=list[IncidentResponse])
def get_incidents(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    payload = verify_access_token(credentials.credentials)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return get_all_incidents(db)


@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident(
    incident_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    payload = verify_access_token(credentials.credentials)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    incident = get_incident_by_id(db, incident_id)

    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")

    return incident


@router.put("/{incident_id}", response_model=IncidentResponse)
def edit_incident(
    incident_id: int,
    incident_data: IncidentUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    payload = verify_access_token(credentials.credentials)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    incident = get_incident_by_id(db, incident_id)

    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")

    updated_data = incident_data.model_dump(exclude_unset=True)

    return update_incident(db, incident, updated_data)


@router.delete("/{incident_id}")
def remove_incident(
    incident_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    payload = verify_access_token(credentials.credentials)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    incident = get_incident_by_id(db, incident_id)

    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")

    delete_incident(db, incident)

    return {"message": "Incident deleted successfully"}