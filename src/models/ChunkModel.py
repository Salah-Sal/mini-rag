"""Data access model for text chunks.

This module provides methods for creating, retrieving, and managing
text chunks stored in the database. These chunks are the core data
units for vector embedding and retrieval in the RAG pipeline.
"""
from .BaseDataModel import BaseDataModel
from .db_schemes import DataChunk
from .enums.DataBaseEnum import DataBaseEnum
from bson.objectid import ObjectId
from pymongo import InsertOne
from sqlalchemy.future import select
from sqlalchemy import func, delete
from typing import List, Optional, Any, Union

class ChunkModel(BaseDataModel):
    """Data access model for text chunks.
    
    This class provides methods to interact with the chunks table in the database,
    handling CRUD operations and pagination for text chunks.
    
    Chunks are segments of text extracted from uploaded files, which are
    embedded and indexed for semantic search in the RAG pipeline.
    
    Attributes:
        db_client: SQLAlchemy async session maker for database access
    """

    def __init__(self, db_client: Any):
        """Initialize the ChunkModel.
        
        Args:
            db_client: SQLAlchemy async session maker
        """
        super().__init__(db_client=db_client)
        self.db_client = db_client

    @classmethod
    async def create_instance(cls, db_client: Any) -> 'ChunkModel':
        """Create an instance of ChunkModel asynchronously.
        
        This factory method provides a standard way to create model instances.
        
        Args:
            db_client: SQLAlchemy async session maker
            
        Returns:
            Initialized ChunkModel instance
        """
        instance = cls(db_client)
        return instance

    async def create_chunk(self, chunk: DataChunk) -> DataChunk:
        """Create a single chunk record in the database.
        
        Args:
            chunk: DataChunk object to insert
            
        Returns:
            The inserted DataChunk with updated attributes (e.g., ID)
        """
        async with self.db_client() as session:
            async with session.begin():
                session.add(chunk)
            await session.commit()
            await session.refresh(chunk)
        return chunk

    async def get_chunk(self, chunk_id: str) -> Optional[DataChunk]:
        """Retrieve a specific chunk by ID.
        
        Args:
            chunk_id: ID of the chunk to retrieve
            
        Returns:
            DataChunk object if found, None otherwise
        """
        async with self.db_client() as session:
            result = await session.execute(select(DataChunk).where(DataChunk.chunk_id == chunk_id))
            chunk = result.scalar_one_or_none()
        return chunk

    async def insert_many_chunks(self, chunks: List[DataChunk], batch_size: int=100) -> int:
        """Insert multiple chunks in batches.
        
        Efficiently inserts multiple chunks by breaking them into batches
        to avoid overwhelming the database.
        
        Args:
            chunks: List of DataChunk objects to insert
            batch_size: Number of chunks to insert in each transaction
            
        Returns:
            Number of chunks inserted
        """
        async with self.db_client() as session:
            async with session.begin():
                for i in range(0, len(chunks), batch_size):
                    batch = chunks[i:i+batch_size]
                    session.add_all(batch)
            await session.commit()
        return len(chunks)

    async def delete_chunks_by_project_id(self, project_id: Any) -> int:
        """Delete all chunks associated with a project.
        
        Args:
            project_id: ID of the project whose chunks should be deleted
            
        Returns:
            Number of chunks deleted
        """
        async with self.db_client() as session:
            stmt = delete(DataChunk).where(DataChunk.chunk_project_id == project_id)
            result = await session.execute(stmt)
            await session.commit()
        return result.rowcount
    
    async def get_poject_chunks(self, project_id: Any, page_no: int=1, page_size: int=50) -> List[DataChunk]:
        """Retrieve chunks for a project with pagination.
        
        Args:
            project_id: ID of the project to retrieve chunks for
            page_no: Page number (1-indexed)
            page_size: Number of chunks per page
            
        Returns:
            List of DataChunk objects for the requested page
        """
        async with self.db_client() as session:
            stmt = select(DataChunk).where(DataChunk.chunk_project_id == project_id).offset((page_no - 1) * page_size).limit(page_size)
            result = await session.execute(stmt)
            records = result.scalars().all()
        return records
    
    async def get_total_chunks_count(self, project_id: Any) -> int:
        """Count the total number of chunks for a project.
        
        Used for pagination and progress tracking.
        
        Args:
            project_id: ID of the project to count chunks for
            
        Returns:
            Total number of chunks in the project
        """
        total_count = 0
        async with self.db_client() as session:
            count_sql = select(func.count(DataChunk.chunk_id)).where(DataChunk.chunk_project_id == project_id)
            records_count = await session.execute(count_sql)
            total_count = records_count.scalar()
        
        return total_count


