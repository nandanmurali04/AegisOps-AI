from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String, nullable=False)

    email = Column(String, unique=True, index=True, nullable=False)

    hashed_password = Column(String, nullable=False)

    role = Column(String, default="user")

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # Incidents created by this user
    incidents = relationship(
        "Incident",
        foreign_keys="Incident.created_by",
        back_populates="owner"
    )

    # Incidents assigned to this user
    assigned_incidents = relationship(
        "Incident",
        foreign_keys="Incident.assigned_to",
        back_populates="assignee"
    )

    # Audit logs performed by this user
    incident_logs = relationship(
        "IncidentLog",
        back_populates="user"
    )