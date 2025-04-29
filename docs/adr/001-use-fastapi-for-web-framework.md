# ADR-001: Use FastAPI for Web Framework

**Status:** Accepted

**Context:**

The `mini-rag` project requires a backend web framework to serve its API endpoints for managing projects, uploading data, processing files, indexing vectors, and performing RAG-based question answering. Key requirements for the framework include:

- Asynchronous support: Essential for handling potentially long-running I/O operations like database interactions, vector store operations, and calls to external LLM APIs efficiently without blocking the server.
- Performance: The framework should be performant to handle concurrent requests effectively.
- Automatic API Documentation: Built-in support for generating interactive API documentation (like Swagger UI/OpenAPI) is highly desirable to simplify API usage and testing for developers.
- Data Validation: Strong support for request/response data validation using modern Python features (like type hints) is needed for robustness.
- Ease of Use: The framework should be relatively easy for Python developers to learn and use.

**Decision:**

We decided to use **FastAPI** as the web framework for this project.

**Consequences:**

- **Positive:**
  - **Native Async:** FastAPI is built on Starlette and Pydantic, providing native `async`/`await` support, making it ideal for I/O-bound applications.
  - **High Performance:** Benchmarks often show FastAPI as one of the fastest Python frameworks available, thanks to Starlette and `uvicorn`.
  - **Automatic Docs:** Automatically generates OpenAPI and Swagger UI documentation from route definitions and Pydantic models, significantly reducing documentation effort.
  - **Data Validation:** Leverages Pydantic for robust data validation and serialization using Python type hints, improving code clarity and reducing runtime errors.
  - **Developer Experience:** Generally considered easy to learn, especially for those familiar with Flask. Enforces type hints, leading to better code quality.
  - **Dependency Injection:** Has a simple yet powerful dependency injection system.
- **Negative:**
  - **Maturity/Ecosystem:** While rapidly growing, it's newer than frameworks like Django or Flask, which might mean a smaller ecosystem for certain highly specific plugins (though core needs are well-covered).
  - **Async Learning Curve:** Developers unfamiliar with Python's `asyncio` might face a slight learning curve.
