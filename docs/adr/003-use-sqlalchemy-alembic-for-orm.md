# ADR-003: Use SQLAlchemy and Alembic for ORM and Migrations

**Status:** Accepted

**Context:**

With the decision to use PostgreSQL (ADR-002), the project needs a way to interact with the relational database from Python code and manage database schema changes over time. Requirements include:

- Object-Relational Mapper (ORM): To map Python objects to database tables, reducing the need to write raw SQL for common operations.
- Asynchronous Support: The ORM must integrate with Python's `asyncio` for non-blocking database calls, compatible with FastAPI (ADR-001).
- Schema Migrations: A tool is needed to reliably manage changes to the database schema (e.g., adding tables, columns, indexes) as the application evolves, keeping the schema definition version-controlled.

**Decision:**

We decided to use:

1.  **SQLAlchemy:** As the ORM toolkit.
2.  **Alembic:** For handling database schema migrations, which integrates well with SQLAlchemy.

**Consequences:**

- **Positive:**
  - **Powerful ORM:** SQLAlchemy is a mature, flexible, and powerful ORM for Python, offering both high-level ORM features and the ability to drop down to SQL expressions or raw SQL when needed.
  - **Async Support:** SQLAlchemy provides excellent support for `asyncio` operations, integrating smoothly with FastAPI and `asyncpg`.
  - **Alembic Integration:** Alembic is designed specifically for SQLAlchemy, making schema migrations straightforward. Migration scripts can be auto-generated and manually edited.
  - **Decoupling:** Helps decouple application logic from raw database queries.
  - **Mature and Well-Supported:** Both SQLAlchemy and Alembic are widely used and have extensive documentation and community support.
- **Negative:**
  - **Learning Curve:** SQLAlchemy has a reputation for being powerful but can have a steeper learning curve compared to some simpler ORMs, especially regarding session management and advanced features.
  - **Verbosity:** Can sometimes be more verbose than other ORMs for simple operations.
  - **Migration Script Management:** Requires developers to learn Alembic commands and manage migration script generation and application.

**Alternatives Considered:**

- **Django ORM:** Tightly coupled with the Django framework; not suitable for FastAPI.
- **Peewee:** A simpler ORM, potentially easier to learn but less feature-rich than SQLAlchemy. Async support might be less mature.
- **SQLModel:** Built on top of Pydantic and SQLAlchemy by the creator of FastAPI. Offers closer integration with FastAPI's Pydantic models but is newer and might be considered less battle-tested than pure SQLAlchemy for complex scenarios.
- **Manual SQL + Migration Tool:** Writing raw SQL (e.g., via `asyncpg`) provides maximum control but is more verbose, error-prone, and couples logic tightly to the specific SQL dialect. Would still need a separate migration tool (like Alembic or others).
