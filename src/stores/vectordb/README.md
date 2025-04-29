# Vector DB Store

The Vector DB Store module provides a unified interface to different vector database backends, enabling semantic search through vector similarity. This is a critical component of the RAG pipeline, allowing efficient retrieval of context-relevant documents.

## Overview

This module follows a provider-based architecture with:

1. **Common Interface**: Abstract base class defining required vector operations
2. **Factory**: Creates appropriate provider instance based on configuration
3. **Providers**: Concrete implementations for specific vector databases
4. **Enums**: Constants and types for providers and operations

## Core Components

### VectorDBInterface

The abstract base class (`VectorDBInterface.py`) defines all operations required for a vector database provider:

- **Connection Management**: `connect()`, `disconnect()`
- **Collection Management**: `create_collection()`, `delete_collection()`, `list_all_collections()`, `get_collection_info()`
- **Data Operations**: `insert_one()`, `insert_many()`
- **Search**: `search_by_vector()` for similarity search

This interface ensures all providers support the necessary operations regardless of the underlying implementation.

### VectorDBProviderFactory

Factory class (`VectorDBProviderFactory.py`) that creates provider instances based on configuration:

- **Providers**:
  - `QDRANT`: Creates a QdrantDBProvider
  - `PGVECTOR`: Creates a PGVectorProvider

The factory handles passing configuration to the appropriate provider and ensures consistent initialization.

### Providers

Concrete implementations of the VectorDBInterface:

- **PGVectorProvider**: Uses PostgreSQL with the pgvector extension

  - Embeds vector operations directly in PostgreSQL
  - Creates and manages tables with vector columns
  - Handles index creation (HNSW, IVFFlat) for efficient search
  - Uses SQL for all operations (create, insert, search)
  - Fully integrated with the application's PostgreSQL database

- **QdrantDBProvider**: Uses the Qdrant vector database
  - Can run as a separate service or embedded
  - Provides specialized vector indexing and search

### Enums

Constants and type definitions:

- **VectorDBEnums**: Vector database providers (`QDRANT`, `PGVECTOR`)
- **DistanceMethodEnums**: Similarity metrics (`COSINE`, `DOT`)
- **PgVectorTableSchemeEnums**: Column names for pgvector tables
- **PgVectorDistanceMethodEnums**: PostgreSQL-specific distance operators
- **PgVectorIndexTypeEnums**: Index types (`HNSW`, `IVFFLAT`)

## Usage Pattern

The module is typically used through dependency injection:

```python
# In app startup
app.vectordb_client = vectordb_provider_factory.create(
    provider=settings.VECTOR_DB_BACKEND
)
await app.vectordb_client.connect()

# In controllers
collection_name = self.create_collection_name(project_id=project.project_id)
await self.vectordb_client.create_collection(
    collection_name=collection_name,
    embedding_size=self.embedding_client.embedding_size
)

# For search
results = await self.vectordb_client.search_by_vector(
    collection_name=collection_name,
    vector=query_vector,
    limit=limit
)
```

## PGVector Implementation

The primary implementation uses PostgreSQL with pgvector, which:

- Creates tables with vector columns for each collection
- Stores both the original text and its vector representation
- Links vectors to their source chunks via foreign keys
- Creates optimized vector indexes after reaching a threshold
- Uses native SQL functions for vector similarity search (`<=>` operator)
- Returns search results as `RetrievedDocument` objects with text and relevance score

## Future Extensibility

Additional vector database providers can be added by:

1. Creating a new class that implements `VectorDBInterface`
2. Adding the provider to `VectorDBEnums`
3. Updating the factory to instantiate the new provider
