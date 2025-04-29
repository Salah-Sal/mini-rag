# ADR-002: Use PostgreSQL + pgvector for Database and Vector Storage

**Status:** Accepted

**Context:**

The `mini-rag` application needs to store:

1.  Relational/structured data: Project information, uploaded file metadata (Assets), and text chunks derived from files.
2.  Vector embeddings: Dense vector representations of the text chunks for efficient semantic search.

The project initially used MongoDB (as mentioned in the README history), but requires a solution that handles both structured data and vector search effectively and preferably within a single system to simplify infrastructure.

Requirements:

- Persistence for structured project/asset/chunk metadata.
- Ability to store and efficiently query high-dimensional vectors (similarity search).
- Standard SQL interface for relational data is preferred for familiarity and tooling.
- Mature and reliable database technology.
- Integration with Python (specifically with async support).

**Decision:**

We decided to use **PostgreSQL** as the primary database, extended with the **pgvector** extension for handling vector embeddings and similarity search.

**Consequences:**

- **Positive:**
  - **Unified System:** Stores both relational data and vector embeddings within the same mature, ACID-compliant database system, simplifying deployment and data management.
  - **Mature Technology:** PostgreSQL is a highly reliable, feature-rich, and widely used open-source relational database.
  - **SQL Interface:** Allows leveraging standard SQL for querying structured data alongside vector search capabilities.
  - **pgvector Efficiency:** `pgvector` provides indexed similarity search (using HNSW, IVFFlat) directly within PostgreSQL.
  - **Ecosystem:** Benefits from the extensive PostgreSQL ecosystem, including robust Python clients (like `asyncpg` for async operations) and ORMs (like SQLAlchemy).
  - **Transactional Integrity:** Ensures consistency between metadata and vectors if managed within the same transaction.
- **Negative:**
  - **Scalability Limits (Compared to Dedicated):** While `pgvector` is efficient, extremely large-scale vector search requirements (billions of vectors) might eventually perform better in specialized vector databases. However, this is sufficient for the project's current and foreseeable scale.
  - **Extension Management:** Requires ensuring the `pgvector` extension is installed and managed in the PostgreSQL instance.
  - **Potential Resource Contention:** High load on both relational queries and vector search could potentially lead to resource contention on the same database instance, requiring appropriate monitoring and scaling.

**Alternatives Considered:**

- **MongoDB + Dedicated Vector DB (e.g., Qdrant, Weaviate):** Used previously. Separates concerns but increases infrastructure complexity (managing two databases) and potential data consistency challenges between them.
- **Standalone Vector Databases:** Excellent for vector search but require a separate relational database for metadata, leading to the same complexity as the previous point.
