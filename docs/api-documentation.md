# API Documentation

This document provides detailed information about the mini-rag API endpoints, request/response formats, and usage examples.

## Base URL

All API endpoints are accessible via the base URL: `http://localhost:5000/api/v1`

## Authentication

The API currently does not implement authentication. In production environments, consider implementing an authentication mechanism.

## Error Handling

All API endpoints return standard HTTP status codes:

- `200 OK`: Successful request
- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server-side error

Error responses follow this format:

```json
{
  "status": "error",
  "message": "Detailed error message"
}
```

## Projects API

### Create Project

```
POST /projects
```

Creates a new document project.

**Request Body:**

```json
{
  "name": "Project Name",
  "description": "Project Description"
}
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "id": "uuid",
    "name": "Project Name",
    "description": "Project Description",
    "created_at": "ISO-8601 timestamp",
    "updated_at": "ISO-8601 timestamp"
  }
}
```

### List Projects

```
GET /projects
```

Returns a list of all projects.

**Response:**

```json
{
  "status": "success",
  "data": [
    {
      "id": "uuid",
      "name": "Project Name",
      "description": "Project Description",
      "created_at": "ISO-8601 timestamp",
      "updated_at": "ISO-8601 timestamp"
    }
  ]
}
```

## Data API

### Upload File

```
POST /data/upload
```

Uploads a document file to be processed.

**Request Body:**

- `project_id`: UUID of the project
- `file`: The file to upload (multipart/form-data)

**Response:**

```json
{
  "status": "success",
  "data": {
    "asset_id": "uuid",
    "filename": "filename.ext",
    "size": 1024,
    "created_at": "ISO-8601 timestamp"
  }
}
```

### Process File

```
POST /data/process
```

Processes an uploaded file, extracting and embedding its content.

**Request Body:**

```json
{
  "asset_id": "uuid"
}
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "processed": true,
    "chunks_count": 10,
    "processing_time": 3.5
  }
}
```

### List Assets

```
GET /data/list
```

Lists all uploaded assets for a project.

**Query Parameters:**

- `project_id`: UUID of the project

**Response:**

```json
{
  "status": "success",
  "data": [
    {
      "id": "uuid",
      "filename": "filename.ext",
      "size": 1024,
      "status": "processed",
      "created_at": "ISO-8601 timestamp"
    }
  ]
}
```

## NLP API

### Answer RAG Question

```
POST /index/answer
```

Answers a question using RAG (Retrieval-Augmented Generation).

**Request Body:**

```json
{
  "project_id": "uuid",
  "query": "What is mini-rag?",
  "top_k": 3
}
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "answer": "Mini-rag is a minimal implementation of the RAG model for question answering.",
    "sources": [
      {
        "chunk_id": "uuid",
        "text": "Chunk text...",
        "score": 0.95,
        "asset_id": "uuid",
        "filename": "filename.ext"
      }
    ],
    "processing_time": 2.3
  }
}
```

### Semantic Search

```
POST /index/search
```

Performs semantic search on document chunks.

**Request Body:**

```json
{
  "project_id": "uuid",
  "query": "Search query",
  "top_k": 5
}
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "results": [
      {
        "chunk_id": "uuid",
        "text": "Chunk text...",
        "score": 0.92,
        "asset_id": "uuid",
        "filename": "filename.ext"
      }
    ],
    "processing_time": 0.5
  }
}
```

## OpenAPI Specification

The complete OpenAPI specification is available at `/docs` or `/redoc` when the server is running. These endpoints provide interactive documentation for all API endpoints, including request/response schemas and examples.

## Usage Examples

### Complete RAG Workflow

1. Create a project:

```bash
curl -X POST http://localhost:5000/api/v1/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Documentation Project", "description": "Technical documentation for mini-rag"}'
```

2. Upload a file:

```bash
curl -X POST http://localhost:5000/api/v1/data/upload \
  -F "project_id=your_project_id" \
  -F "file=@/path/to/document.pdf"
```

3. Process the file:

```bash
curl -X POST http://localhost:5000/api/v1/data/process \
  -H "Content-Type: application/json" \
  -d '{"asset_id": "your_asset_id"}'
```

4. Ask a question:

```bash
curl -X POST http://localhost:5000/api/v1/index/answer \
  -H "Content-Type: application/json" \
  -d '{"project_id": "your_project_id", "query": "What is mini-rag?", "top_k": 3}'
```
