"""Interface for vector database operations.

This module defines the abstract base class that all vector database providers
must implement. It standardizes the operations for connection management,
collection (table) handling, vector insertion, and similarity search.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, Union
from models.db_schemes import RetrievedDocument

class VectorDBInterface(ABC):
    """Abstract base class for vector database providers.
    
    This interface defines the required operations for any vector database implementation,
    providing a consistent API regardless of the underlying technology. Providers must
    implement all methods to ensure full compatibility with the application.
    
    Vector databases store high-dimensional vectors (embeddings) and provide efficient
    similarity search, which is a core component of the RAG pipeline.
    """

    @abstractmethod
    async def connect(self) -> None:
        """Connect to the vector database.
        
        Establishes a connection to the underlying database/service
        and performs any necessary setup operations (e.g., creating extensions).
        
        Should be called during application startup.
        """
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Disconnect from the vector database.
        
        Closes connections and performs any necessary cleanup.
        
        Should be called during application shutdown.
        """
        pass

    @abstractmethod
    async def is_collection_existed(self, collection_name: str) -> bool:
        """Check if a collection exists in the vector database.
        
        Args:
            collection_name: Name of the collection to check
            
        Returns:
            True if the collection exists, False otherwise
        """
        pass

    @abstractmethod
    async def list_all_collections(self) -> List[str]:
        """List all collections in the vector database.
        
        Returns:
            List of collection names
        """
        pass

    @abstractmethod
    async def get_collection_info(self, collection_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific collection.
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            Dictionary with collection metadata (structure depends on provider),
            or None if the collection doesn't exist
        """
        pass

    @abstractmethod
    async def delete_collection(self, collection_name: str) -> bool:
        """Delete a collection from the vector database.
        
        Args:
            collection_name: Name of the collection to delete
            
        Returns:
            True if deletion was successful, False otherwise
        """
        pass

    @abstractmethod
    async def create_collection(self, collection_name: str, 
                                embedding_size: int,
                                do_reset: bool = False) -> bool:
        """Create a new collection in the vector database.
        
        Args:
            collection_name: Name of the collection to create
            embedding_size: Dimension of the vectors to be stored
            do_reset: Whether to delete and recreate if the collection already exists
            
        Returns:
            True if collection was created (or already existed), False otherwise
        """
        pass

    @abstractmethod
    async def insert_one(self, collection_name: str, text: str, vector: List[float],
                         metadata: Optional[Dict[str, Any]] = None, 
                         record_id: Optional[str] = None) -> bool:
        """Insert a single vector into a collection.
        
        Args:
            collection_name: Name of the collection
            text: Original text corresponding to the vector
            vector: The embedding vector as a list of floats
            metadata: Optional metadata to store with the vector
            record_id: Optional identifier to associate with the vector
            
        Returns:
            True if insertion was successful, False otherwise
        """
        pass

    @abstractmethod
    async def insert_many(self, collection_name: str, texts: List[str], 
                          vectors: List[List[float]], metadata: Optional[List[Dict]] = None, 
                          record_ids: Optional[List[str]] = None, batch_size: int = 50) -> bool:
        """Insert multiple vectors into a collection in batches.
        
        Args:
            collection_name: Name of the collection
            texts: List of original texts corresponding to the vectors
            vectors: List of embedding vectors
            metadata: Optional list of metadata dictionaries
            record_ids: Optional list of record identifiers
            batch_size: Number of vectors to insert in each batch
            
        Returns:
            True if all insertions were successful, False otherwise
        """
        pass

    @abstractmethod
    async def search_by_vector(self, collection_name: str, vector: List[float], 
                               limit: int) -> List[RetrievedDocument]:
        """Search for similar vectors in a collection.
        
        This is the core operation for semantic search in the RAG pipeline,
        finding the most similar documents to a query vector.
        
        Args:
            collection_name: Name of the collection to search
            vector: Query vector to search for
            limit: Maximum number of results to return
            
        Returns:
            List of RetrievedDocument objects containing the text and similarity score,
            sorted by decreasing similarity (most similar first)
        """
        pass
    