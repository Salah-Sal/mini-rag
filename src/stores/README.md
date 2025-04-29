# Stores Module

The `stores` package abstracts all **external service integrations** so the core
business logic can remain agnostic of concrete back-ends. Two service families
are currently supported:

1. **Large-Language-Model (LLM) Providers** – text generation & embeddings
2. **Vector Database Providers** – high-dimensional similarity search

Both families follow the same design philosophy:

• A **common interface** that defines the required operations.
• A **provider enum** that lists concrete back-ends.
• A **factory** that instantiates the correct provider based on configuration.

This pattern lets us swap back-ends (e.g. OpenAI → Ollama, PGVector → Qdrant)
with _zero_ changes to controllers.

---

## Directory Layout

```
stores/
├── llm/               # LLM integration layer
│   ├── LLMInterface.py
│   ├── LLMProviderFactory.py
│   ├── LLMEnums.py
│   ├── providers/     # Concrete providers (OpenAI, Ollama, etc.)
│   └── templates/     # Prompt template system (see README there)
└── vectordb/          # Vector DB integration layer
    ├── VectorDBInterface.py
    ├── VectorDBProviderFactory.py
    ├── VectorDBEnums.py
    └── providers/     # Concrete providers (PGVector, Qdrant, …)
```

---

## LLM Sub-module (`stores/llm`)

| File                    | Purpose                                                                                                              |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `LLMInterface.py`       | Async interface specifying generation, embedding and model-selection calls                                           |
| `LLMProviderFactory.py` | Reads `settings.GENERATION_BACKEND` / `EMBEDDING_BACKEND` and returns a provider instance implementing the interface |
| `providers/`            | One sub-package per back-end (e.g., `openai_provider.py`)                                                            |
| `templates/`            | Localised prompt templates + parser – see dedicated README                                                           |

Usage example (from `src/main.py`):

```python
llm_factory = LLMProviderFactory(settings)
app.generation_client = llm_factory.create(provider=settings.GENERATION_BACKEND)
app.embedding_client  = llm_factory.create(provider=settings.EMBEDDING_BACKEND)
```

---

## Vector DB Sub-module (`stores/vectordb`)

Similar layout and intent:

| File                         | Purpose                                                                                 |
| ---------------------------- | --------------------------------------------------------------------------------------- |
| `VectorDBInterface.py`       | Async CRUD + search methods (`create_collection`, `insert_many`, `search_by_vector`, …) |
| `VectorDBProviderFactory.py` | Instantiates provider based on `settings.VECTOR_DB_BACKEND`                             |
| `VectorDBEnums.py`           | Provider & distance-metric enums                                                        |

Example (see `NLPController.index_into_vector_db`):

```python
collection_name = self.create_collection_name(project_id)
await self.vectordb_client.create_collection(collection_name, embedding_size)
await self.vectordb_client.insert_many(collection_name, texts, metadata, vectors)
```

---

## Adding a New Provider

1. Implement the relevant interface.
2. Add an entry to the corresponding enum.
3. Extend the factory to return your new class.
4. Document configuration flags in `README.md` and `.env.example`.

---

## See Also

- `src/stores/llm/templates/README.md` – prompt template localisation.
- `docs/adr/004-template-engine-for-llm-prompts.md` – decision record.
- `src/stores/vectordb/README.md` – deeper dive into vector-store layer.
