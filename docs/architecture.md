# System Architecture & Technical Evolution

This document outlines the high-level system architecture for the Case Management Assistant, detailing both the initial MVP setup and its planned evolution into an AI-driven investigation platform.

---

## 1. Phase 1 Architecture: MVP

The initial MVP uses a monolithic synchronous pattern focused on core data persistence and basic HTTP API endpoints.

### Topology

```
+-------------------+
|   Client / UI     |
| (Browser / Postman)
+-------------------+
          |
          v
+-------------------+
|   FastAPI App     |
| (Web API Layer)   |
+-------------------+
     |         |
     v         v
+----------+ +--------------------+
| SQLite / | |  Local File Store  |
| Postgres | | (Document Storage) |
+----------+ +--------------------+
```

## 2. Phase 2 Architecture: AI Pipeline & RAG Evolution

As features like semantic search, entity extraction and automated citations are added, the system introduces decoupled services, a vector indexing pipeline and an external LLM integration layer.

### Topology

```
+-------------------+
                            |   Client / UI     |
                            | (Browser / Postman)
                            +-------------------+
                                      |
                                      v
                            +-------------------+
                            |   FastAPI App     |
                            | (API Gateway/Web) |
                            +-------------------+
                                      |
         +----------------------------+----------------------------+
         |                            |                            |
         v                            v                            v
+-------------------+        +-------------------+        +-------------------+
|   Case Service    |        | Document Service  |        |    AI Service     |
| (Core Management) |        | (Parsing/Storage) |        | (RAG/Summaries)   |
+-------------------+        +-------------------+        +-------------------+
         |                            |                            |
         |                            v                            v
         |                   +-------------------+        +-------------------+
         |                   |  Document Store   |        |   LLM Provider    |
         |                   | (S3 / Local Disk) |        | (OpenAI/Anthropic)|
         |                   +-------------------+        +-------------------+
         |                            |                            |
         +----------------------------+----------------------------+
                                      |
                                      v
                            +-------------------+
                            | PostgreSQL DB     |
                            |  (+ pgvector)     |
                            +-------------------+
```

### Key Architectural Boundaries

1. Case Service: Manages domain logic around case statuses, lifecycle transitions, and record associations.

2. Document Service: Handles file upload ingestion, text extraction, document chunking, and file storage retrieval.

3. AI Service: Orchestrates prompt templates, calls external LLM providers, manages vector embeddings and formats citations.

4. pgvector Store: Extends the relational database to store high-dimensional text embeddings for fast vector similarity search across case evidence.


## 3. Data Flow: Document Ingestion & Summary Generation

1. Upload: Client sends a multipart document payload via POST /cases/{id}/documents.

2. Storage: Document Service stores raw bytes on disk/S3 and records file metadata in the relational database.

3. Indexing (Phase 2): Text is extracted, split into manageable chunks, embedded via the AI Service, and written to pgvector.

4. Summarisation: Client invokes POST /cases/{id}/summary. The AI Service pulls case documents (or retrieved context chunks), executes the prompt template against the LLM, and persists the generated response.