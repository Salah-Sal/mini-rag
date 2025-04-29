# Routes Module

The Routes module defines the API endpoints of the mini-rag application, handling HTTP requests and delegating business logic to controllers.

## Overview

This module follows REST principles with a versioned API structure (`/api/v1/`). All endpoints use asynchronous handlers to efficiently handle I/O operations. The routes are organized in routers by functional domain:

- `base_router`: Basic application information
- `data_router`: Data upload and processing
- `nlp_router`: Vector indexing and RAG functionality

## Core Routers

### Base Router (`base.py`)

Provides basic application info:

- `GET /api/v1/`: Returns application name and version.

### Data Router (`data.py`)

Manages data upload and processing:

- `POST /api/v1/data/upload/{project_id}`: Uploads a file to a specific project

  - Validates file type and size
  - Saves file to project directory
  - Creates Asset record in database
  - Returns unique file_id

- `POST /api/v1/data/process/{project_id}`: Processes uploaded files into chunks
  - Accepts parameters for chunk size and overlap
  - Can process a specific file or all files in a project
  - Loads file content using appropriate loader (Text, PDF)
  - Splits content into chunks with metadata
  - Stores chunks in database
  - Returns count of chunks created

### NLP Router (`nlp.py`)

Handles NLP operations including vector operations and RAG:

- `POST /api/v1/nlp/index/push/{project_id}`: Indexes chunks into vector DB

  - Embeds text chunks
  - Stores vectors with metadata
  - Supports batch processing for large datasets

- `GET /api/v1/nlp/index/info/{project_id}`: Gets vector collection info

  - Collection statistics
  - Vector count, dimensions

- `POST /api/v1/nlp/index/search/{project_id}`: Performs semantic search

  - Searches by text query
  - Configurable result limit
  - Returns semantically similar chunks with scores

- `POST /api/v1/nlp/index/answer/{project_id}`: Performs RAG to answer questions
  - Retrieves relevant chunks via semantic search
  - Constructs prompts with retrieved context
  - Generates answers via LLM
  - Returns answer, prompt details, and chat history

## Request/Response Patterns

All routes follow consistent patterns:

- Request validation using Pydantic models (`schemes/`)
- HTTP responses use JSONResponse with appropriate status codes
- API responses include a `signal` field for client-side handling
- Error responses use appropriate HTTP status codes (4xx)

## Dependencies

The routes use FastAPI's dependency injection system for:

- Configuration (`get_settings`)
- Controller initialization
- Database client access

A detailed sequence diagram for the RAG flow is available at `/docs/diagrams/rag_sequence.md`.
