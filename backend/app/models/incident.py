from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    description = Column(Text, nullable=False)

    severity = Column(String, nullable=False)

    status = Column(String, default="Open")

    # User who created the incident
    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    # User assigned to handle the incident
    assigned_to = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # Relationship to creator
    owner = relationship(
        "User",
        foreign_keys=[created_by],
        back_populates="incidents"
    )

    # Relationship to assignee
    assignee = relationship(
        "User",
        foreign_keys=[assigned_to],
        back_populates="assigned_incidents"
    )

    # Audit Logs
    logs = relationship(
        "IncidentLog",
        back_populates="incident",
        cascade="all, delete-orphan"
    )