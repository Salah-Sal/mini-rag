from .minirag_base import SQLAlchemyBase
from sqlalchemy import Column, Integer, DateTime, func, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy import Index
from pydantic import BaseModel
import uuid

class DataChunk(SQLAlchemyBase):
    """SQLAlchemy model representing a text chunk derived from an asset.

    Chunks are the primary units of text processed and embedded for RAG.

    Attributes:
        chunk_id: Primary key, auto-incrementing integer.
        chunk_uuid: Unique UUID identifier for the chunk.
        chunk_text: The actual text content of the chunk.
        chunk_metadata: Optional JSON field for chunk-specific metadata.
        chunk_order: The sequential order of the chunk within its source asset.
        chunk_project_id: Foreign key linking to the parent project.
        chunk_asset_id: Foreign key linking to the source asset.
        created_at: Timestamp when the chunk was created.
        updated_at: Timestamp when the chunk was last updated.
        project: Relationship to the parent Project object.
        asset: Relationship to the source Asset object.
    """

    __tablename__ = "chunks"

    chunk_id = Column(Integer, primary_key=True, autoincrement=True)
    chunk_uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)

    chunk_text = Column(String, nullable=False)
    chunk_metadata = Column(JSONB, nullable=True)
    chunk_order = Column(Integer, nullable=False)

    chunk_project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)
    chunk_asset_id = Column(Integer, ForeignKey("assets.asset_id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    project = relationship("Project", back_populates="chunks")
    asset = relationship("Asset", back_populates="chunks")

    __table_args__ = (
        Index('ix_chunk_project_id', chunk_project_id),
        Index('ix_chunk_asset_id', chunk_asset_id),
    )

class RetrievedDocument(BaseModel):
    text: str
    score: float
