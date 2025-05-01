----------------------------------------------------
1. Layered / Component View
----------------------------------------------------
```mermaid
graph LR
  subgraph Presentation-Layer
      FAPI[FastAPI routes\n(base.py, data.py, nlp.py)]
  end
  subgraph Application-Layer
      Ctrls[Controllers\n(Data, Process, NLP, Project, …)]
  end
  subgraph Domain-Layer
      Models[Domain Models\n(ProjectModel, AssetModel, ChunkModel)]
  end
  subgraph Infrastructure-Layer
      Stores[Stores\n(VectorDB, LLM, DB)]
  end
  subgraph External-Services
      PG[(PostgreSQL)]
      PGVec[(PGVector)]
      Qdrant[(Qdrant)]
      OpenAI[(OpenAI)]
      CoHere[(CoHere)]
  end

  FAPI --> Ctrls
  Ctrls --> Models
  Ctrls --> Stores
  Models --> PG
  Stores --> PGVec & Qdrant
  Stores --> OpenAI & CoHere
```

----------------------------------------------------
2. Sequence – File Upload (`/api/v1/data/upload/{project_id}`)
----------------------------------------------------
```mermaid
sequenceDiagram
    participant Client
    participant Route as Data Route
    participant ProjM as ProjectModel
    participant DC as DataController
    participant FS as FileSystem
    participant AssetM as AssetModel
    participant DB as PostgreSQL

    Client->>Route: POST upload(file)
    Route->>ProjM: get_project_or_create_one()
    ProjM-->>DB: SELECT/INSERT project
    Route->>DC: validate_uploaded_file()
    alt invalid
        Route-->>Client: 400 FILE_VALIDATION_ERROR
    else valid
        Route->>FS: write file (chunks)
        Route->>AssetM: create_asset()
        AssetM-->>DB: INSERT asset
        Route-->>Client: 200 FILE_UPLOAD_SUCCESS + file_id
    end
```

----------------------------------------------------
3. Sequence – File Processing (`/api/v1/data/process/{project_id}`)
----------------------------------------------------
```mermaid
sequenceDiagram
    participant Client
    participant Route as Data Route
    participant ProjM as ProjectModel
    participant AssetM as AssetModel
    participant PC as ProcessController
    participant ChunkM as ChunkModel
    participant VDB as VectorDB(Client)  %% only touched when do_reset =1
    participant DB as PostgreSQL
    participant FS as FileSystem

    Client->>Route: POST process(params)
    Route->>ProjM: get_project_or_create_one()
    Route->>AssetM: get_all_project_assets()
    loop each selected file
        Route->>PC: get_file_content()
        PC->>FS: read file
        PC-->>Route: content
        Route->>PC: process_file_content()
        PC-->>Route: chunks[]
        Route->>ChunkM: insert_many_chunks()
        ChunkM-->>DB: INSERT
    end
    Route-->>Client: PROCESSING_SUCCESS (records, files)
```

----------------------------------------------------
4. Sequence – Vector Index Push (`/api/v1/nlp/index/push/{project_id}`)
----------------------------------------------------
```mermaid
sequenceDiagram
    participant Client
    participant Route as NLP Route
    participant ProjM as ProjectModel
    participant ChunkM as ChunkModel
    participant NLP as NLPController
    participant VDB as VectorDB Client
    participant DB as PostgreSQL

    Client->>Route: POST index/push
    Route->>ProjM: get_project_or_create_one()
    loop batches
        Route->>ChunkM: get_poject_chunks()
        ChunkM-->>DB: SELECT
        Route->>NLP: index_into_vector_db(chunks)
        NLP->>VDB: create_collection()
        NLP->>VDB: insert_many()
    end
    Route-->>Client: INSERT_INTO_VECTORDB_SUCCESS
```

----------------------------------------------------
5. Sequence – RAG Answer (`/api/v1/nlp/index/answer/{project_id}`)
----------------------------------------------------
```mermaid
sequenceDiagram
    participant Client
    participant Route as NLP Route
    participant ProjM as ProjectModel
    participant NLP as NLPController
    participant Emb as EmbeddingClient
    participant VDB as VectorDB Client
    participant LLM as GenerationClient
    participant DB as PostgreSQL

    Client->>Route: POST answer(query)
    Route->>ProjM: get_project_or_create_one()
    Route->>NLP: answer_rag_question(query)
    NLP->>Emb: embed_text(query)
    Emb-->>NLP: vector
    NLP->>VDB: search_by_vector()
    VDB-->>NLP: top docs[]
    NLP->>LLM: generate_text(prompt)
    LLM-->>NLP: answer
    NLP-->>Route: answer
    Route-->>Client: RAG_ANSWER_SUCCESS
```

----------------------------------------------------
6. Class Diagram – Controllers Hierarchy
----------------------------------------------------
```mermaid
classDiagram
    class BaseController {
        +Settings app_settings
        +generate_random_string()
        +get_database_path()
    }
    class DataController
    class ProcessController
    class NLPController
    class ProjectController

    BaseController <|-- DataController
    BaseController <|-- ProcessController
    BaseController <|-- NLPController
    BaseController <|-- ProjectController
```

----------------------------------------------------
7. Class Diagram – Vector DB Abstraction
----------------------------------------------------
```mermaid
classDiagram
    class VectorDBInterface {
        <<interface>>
        +connect()
        +disconnect()
        +create_collection()
        +insert_many()
        +delete_collection()
        +search_by_vector()
    }

    class PGVectorProvider
    class QdrantDBProvider
    VectorDBInterface <|.. PGVectorProvider
    VectorDBInterface <|.. QdrantDBProvider

    class VectorDBProviderFactory {
        +create(provider) VectorDBInterface
    }
    VectorDBProviderFactory ..> VectorDBInterface
```

----------------------------------------------------
8. Class Diagram – LLM Abstraction
----------------------------------------------------
```mermaid
classDiagram
    class LLMInterface {
        <<interface>>
        +set_generation_model()
        +set_embedding_model()
        +generate_text()
        +embed_text()
    }
    class OpenAIProvider
    class CoHereProvider
    LLMInterface <|.. OpenAIProvider
    LLMInterface <|.. CoHereProvider

    class LLMProviderFactory {
        +create(provider) LLMInterface
    }
    LLMProviderFactory ..> LLMInterface
```

----------------------------------------------------
9. ER Diagram – Database Schemes
----------------------------------------------------
```mermaid
erDiagram
    project ||--o{ asset : has
    project ||--o{ datachunk : has
    asset ||--o{ datachunk : contains

    project {
        int project_id PK
        string project_name
        datetime created_at
    }
    asset {
        int asset_id PK
        int asset_project_id FK
        int asset_type
        string asset_name
        int asset_size
        datetime created_at
    }
    datachunk {
        int chunk_id PK
        int chunk_project_id FK
        int chunk_asset_id FK
        text chunk_text
        json chunk_metadata
        int chunk_order
    }
```

----------------------------------------------------
10. Activity Diagram – Simple Chunk Splitter
----------------------------------------------------
```mermaid
flowchart TD
    A[process_simpler_splitter()] --> B{Join all texts}
    B --> C[Split by delimiter]
    C --> D[Accumulate lines\n until >= chunk_size]
    D -->|yes| E[Push chunk to list]
    D -->|no| C
    E --> C
    C -->|EOF| F[Push last chunk]
    F --> G[Return chunks[]]

