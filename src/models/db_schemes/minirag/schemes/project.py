from .minirag_base import SQLAlchemyBase
from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

class Project(SQLAlchemyBase):
    """SQLAlchemy model representing a project.

    A project acts as a container for related assets (files) and chunks (text segments).

    Attributes:
        project_id: Primary key, auto-incrementing integer.
        project_uuid: Unique UUID identifier for the project.
        created_at: Timestamp when the project was created.
        updated_at: Timestamp when the project was last updated.
        chunks: Relationship to associated DataChunk objects.
        assets: Relationship to associated Asset objects.
    """
    __tablename__ = "projects"
    
    project_id = Column(Integer, primary_key=True, autoincrement=True)
    project_uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    chunks = relationship("DataChunk", back_populates="project")
    assets = relationship("Asset", back_populates="project")
