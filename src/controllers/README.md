# Controllers Module

The Controllers module contains business logic classes that handle specific application operations, decoupling the API routes from implementation details.

## Overview

Controllers act as intermediaries between the API routes and the data models/stores. They orchestrate operations involving multiple components, handle file operations, process data, and manage application state. Controllers inherit from BaseController to share common functionality.

## Core Controllers

### BaseController

The foundation controller class that provides:

- Access to application settings and configuration
- Standard file paths for assets and database
- Utility methods (e.g., random string generation)
- Path management methods

### ProjectController

Manages project-specific operations:

- Creates and manages project directories
- Ensures unique project paths exist
- Provides standardized paths for project assets

### DataController

Handles file upload and validation operations:

- Validates uploaded files (type, size)
- Generates unique file paths with random identifiers
- Sanitizes filenames for storage
- Manages file metadata

### ProcessController

Processes uploaded files into text chunks for RAG:

- Detects file types and selects appropriate loaders
- Loads content from different file formats (TXT, PDF)
- Splits content into chunks with configurable parameters
- Manages chunk metadata and ordering
- Implements text splitting algorithms

### NLPController

Manages NLP operations including vector operations and RAG:

- Handles vector collection management
- Coordinates text embedding generation
- Performs semantic search against vector database
- Orchestrates the RAG pipeline
- Manages prompt templates and LLM interactions

## Controller Dependencies

Controllers may depend on:

- Other controllers (e.g., ProcessController uses ProjectController)
- External services (e.g., NLPController uses vectordb_client and generation_client)
- Helper utilities (e.g., template_parser, config)

## Design Patterns

The controllers implement several design patterns:

- **Inheritance** from BaseController for shared functionality
- **Dependency Injection** to receive external services
- **Factory** pattern to create instances of domain objects
- **Strategy** pattern for processing different file types

## Error Handling

Controllers handle errors through:

- Well-defined return values (e.g., boolean success flags)
- Error signals (ResponseSignal enum values)
- Exception handling with appropriate logging
