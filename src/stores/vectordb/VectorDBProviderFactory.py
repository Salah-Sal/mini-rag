"""Factory for creating vector database provider instances.

This module implements the Factory pattern for vector database providers,
creating the appropriate provider instance based on configuration.
"""
from .providers import QdrantDBProvider, PGVectorProvider
from .VectorDBEnums import VectorDBEnums
from controllers.BaseController import BaseController
from sqlalchemy.orm import sessionmaker
from typing import Optional, Any, Union

class VectorDBProviderFactory:
    """Factory class for vector database providers.
    
    This class creates the appropriate vector database provider based on configuration.
    It abstracts the provider instantiation details and ensures consistent initialization.
    
    Attributes:
        config: Application configuration containing provider settings
        base_controller: BaseController instance for utility functions
        db_client: SQLAlchemy sessionmaker for database access
    """
    
    def __init__(self, config: Any, db_client: Optional[sessionmaker]=None):
        """Initialize the vector database provider factory.
        
        Args:
            config: Application configuration object containing settings
                   (e.g., VECTOR_DB_PATH, VECTOR_DB_DISTANCE_METHOD)
            db_client: SQLAlchemy sessionmaker for PostgreSQL access (for pgvector)
        """
        self.config = config
        self.base_controller = BaseController()
        self.db_client = db_client

    def create(self, provider: str) -> Optional[Union[QdrantDBProvider, PGVectorProvider]]:
        """Create a vector database provider instance.
        
        Creates the appropriate provider based on the provider name,
        passing necessary configuration parameters.
        
        Args:
            provider: Provider name from VectorDBEnums (e.g., "QDRANT", "PGVECTOR")
            
        Returns:
            Initialized provider instance, or None if the provider is not supported
            
        Examples:
            ```python
            factory = VectorDBProviderFactory(config, db_client)
            pgvector = factory.create(VectorDBEnums.PGVECTOR.value)
            ```
        """
        if provider == VectorDBEnums.QDRANT.value:
            qdrant_db_client = self.base_controller.get_database_path(db_name=self.config.VECTOR_DB_PATH)

            return QdrantDBProvider(
                db_client=qdrant_db_client,
                distance_method=self.config.VECTOR_DB_DISTANCE_METHOD,
                default_vector_size=self.config.EMBEDDING_MODEL_SIZE,
                index_threshold=self.config.VECTOR_DB_PGVEC_INDEX_THRESHOLD,
            )
        
        if provider == VectorDBEnums.PGVECTOR.value:
            return PGVectorProvider(
                db_client=self.db_client,
                distance_method=self.config.VECTOR_DB_DISTANCE_METHOD,
                default_vector_size=self.config.EMBEDDING_MODEL_SIZE,
                index_threshold=self.config.VECTOR_DB_PGVEC_INDEX_THRESHOLD,
            )
        
        return None
