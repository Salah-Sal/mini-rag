# Models Module

The Models module defines the database schemas and data access models for the mini-rag application, providing structured data persistence and retrieval.

## Overview

This module follows a layered approach to database interaction:

1. **Database Schemes (SQLAlchemy)**: Define the database tables and relationships
2. **Data Models**: Provide high-level methods to interact with specific entities
3. **Enums**: Define constants and types used throughout the models

## Core Components

### Database Schemes (`db_schemes/minirag/schemes/`)

SQLAlchemy-based database schema definitions:

- **`Project`**: Represents a project in the system

  - Primary entity that groups assets and chunks
  - Contains unique ID, UUID, and timestamps

- **`Asset`**: Represents uploaded files

  - References `Project` (many-to-one)
  - Stores metadata (type, name, size) about uploaded files

- **`DataChunk`**: Represents text chunks derived from assets
  - References both `Project` and `Asset` (many-to-one)
  - Contains the actual content for vector embedding
  - Includes metadata and ordering information

These schemas define PostgreSQL tables with appropriate indexes and relationships. Alembic is used for database migrations (managed in `db_schemes/minirag/alembic/`).

### Data Access Models

Object-oriented interfaces for database interaction:

- **`BaseDataModel`**: Abstract base class for data models

  - Provides common database access utilities
  - Stores database client and app settings

- **`ProjectModel`**: Operations for projects

  - Create, retrieve, and list projects
  - Handles pagination for listing

- **`AssetModel`**: Operations for uploaded file assets

  - Create and retrieve assets by project/name
  - List all assets for a project

- **`ChunkModel`**: Operations for text chunks
  - Create/insert individual chunks and batches
  - Delete chunks by project
  - Retrieve chunks with pagination
  - Count chunks by project

### Enums & Constants

- **`AssetTypeEnum`**: Types of assets (e.g., FILE)
- **`DataBaseEnum`**: Collection/table names
- **`ProcessingEnum`**: Supported file types for processing
- **`ResponseSignal`**: API response status codes

## Usage Patterns

### Creating and Using Models

Models are created asynchronously using the classmethod `create_instance`:

```python
# Create a model instance
project_model = await ProjectModel.create_instance(db_client=request.app.db_client)

# Use the model to interact with the database
project = await project_model.get_project_or_create_one(project_id=project_id)
```

### Inserting and Retrieving Data

Models handle complex database operations like batch insertion:

```python
# Insert many chunks in batches
chunks_count = await chunk_model.insert_many_chunks(chunks=file_chunks_records)

# Retrieve chunks with pagination
page_chunks = await chunk_model.get_poject_chunks(
    project_id=project.project_id,
    page_no=page_no
)
```

## SQLAlchemy and Async

The models use SQLAlchemy's async features with PostgreSQL:

- **Async Session**: `async with` for session and transaction management
- **Future API**: Modern SQLAlchemy syntax with `select()`, `delete()`, etc.
- **Scalars/Results**: Proper handling of query results with `.scalar_one()`, `.all()`, etc.

## Database Schema Evolution

Database schema changes are managed through Alembic migrations:

1. Models define the target schema state
2. Alembic generates migration scripts between states
3. Migrations are applied with `alembic upgrade head`
