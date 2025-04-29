# ADR 005: Main Application Initialization and Lifecycle

## Status

Accepted

## Context

The FastAPI application in `src/main.py` serves as the entry point for the mini-rag system. This module initializes essential components, configures middleware, establishes connections, and manages the application lifecycle. A clear understanding of this initialization process is crucial for maintaining and extending the application.

## Decision

We've structured the main application initialization to follow a clear, sequential process:

1. **Configuration Loading**: Using the `helpers.config` module to load environment variables
2. **Database Initialization**: Setting up the PostgreSQL connection with SQLAlchemy async engine
3. **Service Providers**: Initializing LLM and VectorDB clients via factory patterns
4. **Middleware Setup**: Configuring Prometheus metrics middleware for monitoring
5. **Event Handlers**: Defining startup and shutdown procedures for resource management
6. **Router Registration**: Including modular routers from the routes package

This structure provides separation of concerns and clearly defined initialization steps, making the system easier to maintain and extend.

## Details

### Component Initialization

The main application initializes these key components:

1. **Database Connection**:

   - Uses SQLAlchemy's async engine
   - Creates a session factory for dependency injection

2. **LLM Providers**:

   - Initializes generation and embedding clients
   - Uses factory pattern for provider flexibility

3. **Vector Database**:

   - Connects to the configured vector database
   - Handles indexing and similarity search

4. **Template Parser**:
   - Sets up multilingual prompt templates

### Lifecycle Management

The application uses FastAPI's event handlers:

- **`startup_span()`**: Initializes connections and services
- **`shutdown_span()`**: Properly releases resources and connections

### Error Handling

The application uses FastAPI's built-in exception handling mechanisms, with custom exception handlers defined in specific routes.

## Consequences

### Positive

- **Clean Separation**: Clear division between initialization and business logic
- **Resource Management**: Proper lifecycle management through event handlers
- **Modularity**: Easy to add or replace components due to factory patterns
- **Monitoring**: Built-in metrics for performance monitoring

### Negative

- **Complexity**: Several interconnected components create a complex startup sequence
- **Dependency Chain**: Changes to one component may affect others due to interdependencies

## Related

- ADR 001: Use FastAPI for Web Framework
- ADR 002: Use PostgreSQL/pgvector for Database
- ADR 003: Use SQLAlchemy/Alembic for ORM
