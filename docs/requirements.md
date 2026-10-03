# Functional Requirements & Scope Boundaries

## Version 1: Minimal Viable Product (MVP)

The objective of Version 1 is to establish a working end-to-end baseline for case creation, document upload and text summarisation without complex AI orchestration at this stage.

### Core Capabilities

#### 1. Case Management
* **Create Case:** An investigator can create a new case with a title and optional description.
* **List Cases:** An investigator can view a list of all active cases with their creation date and status.
* **View Case Details:** An investigator can inspect a single case to see its metadata and attached documents.

#### 2. Document Management
* **Upload Document:** An investigator can upload plain text (`.txt`) or PDF (`.pdf`) files to a specific case.
* **Store Document Metadata:** The system tracks filename, file size, upload timestamp and content type for each document.
* **View Documents:** An investigator can fetch and view the raw content or metadata of any uploaded document attached to a case.

#### 3. Baseline Case Summarisation
* **Generate Summary:** An investigator can trigger a summary generation request for a case.
* **Display Summary:** The system displays an aggregated summary combining the uploaded case documents.

---

## Technical Constraints for MVP

* **Synchronous Processing:** Document uploads and initial summaries execute synchronously over standard HTTP endpoints.
* **Storage Layer:** Metadata is persisted in a local relational database (PostgreSQL or SQLite during initial setup); files are stored on local disk.
* **Simple Integration:** Baseline AI summarisation interacts directly with an LLM API provider without additional retrieval layers (RAG) or vector databases.

---

## Out of Scope for Version 1

To preserve focus, the following capabilities are deferred to future releases:
* Timeline extraction and visualisation
* Entity extraction (people, organisations, amounts)
* Multi-document semantic search (Vector / RAG pipeline)
* Asynchronous background workers (Celery / Redis)
* Role-based access control (RBAC) and multi-tenancy