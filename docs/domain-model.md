# Domain Model & Entity Boundaries

This document defines the core business entities, their attributes, domain boundaries and relationships for the Case Management Assistant system.

---

## Entity Relationship Overview

```text
Case (1) ───────< Document (N)
  │                  │
  ├─< Summary (N)    └─< DocumentChunk (N)
  │                          │
  ├─< TimelineEvent (N) <────┘ (via Citation)
  │
  └─< ActionItem (N)
```

## 1. Core Entities

### Case
The primary administrative container representing a regulatory investigation or enquiry.

Attributes:

- id (UUID, Primary Key): Unique case identifier.

- reference_number (String, Unique): Human-readable reference (e.g. CAS-2026-8841).

- title (String): Concise title of the case or enquiry.

- description (Text, Optional): Initial summary or scope notes.

- status (Enum): Current state (NEW, UNDER_REVIEW, ACTION_REQUIRED, CLOSED).

- created_at (Timestamp): Record creation date.

- updated_at (Timestamp): Last modification date.

### Document
An uploaded evidence asset or piece of correspondence linked to a specific case.

Attributes:

- id (UUID, Primary Key): Unique document identifier.

- case_id (UUID, Foreign Key): Reference to parent Case.

- filename (String): Original filename (e.g. 01_complaint_letter.txt).

- file_path (String): Storage location path (S3 or local disk).

- file_size (Integer): File size in bytes.

- mime_type (String): File media type (e.g. text/plain, application/pdf).

- uploaded_at (Timestamp): Date and time of upload.

### Summary
An AI-generated or case owner generated summary of case evidence.

Attributes:

- id (UUID, Primary Key): Unique summary identifier.

- case_id (UUID, Foreign Key): Reference to parent Case.

- content (Text): The generated executive summary text.

- model_version (String): AI model or prompt version used (e.g. gpt-4o-2026-05).

- created_at (Timestamp): Generation timestamp.

## 2. Future Evolutionary Entities (v2+)

### DocumentChunk
Sub-sections of extracted text generated for vector search and citation grounding.

Attributes:

- id (UUID, Primary Key): Unique chunk identifier.

- document_id (UUID, Foreign Key): Reference to parent Document.

- chunk_index (Integer): Sequential position within the parent document.

- content (Text): Text snippet content.

- embedding (Vector, Optional): High-dimensional vector embedding.

### TimelineEvent
Chronological key events extracted from case evidence.

Attributes:

- id (UUID, Primary Key): Unique event identifier.

- case_id (UUID, Foreign Key): Reference to parent Case.

- event_date (Date/Timestamp): Extracted date of the event.

- description (Text): Summary of what occurred.

- source_document_id (UUID, Foreign Key): Source document establishing the event.

### ActionItem
Suggested or assigned regulatory next steps derived from case analysis.

Attributes:

- id (UUID, Primary Key): Unique action item identifier.

- case_id (UUID, Foreign Key): Reference to parent Case.

- title (String): Action title (e.g. "Issue Section 72 Notice").

- rationale (Text): Justification derived from evidence analysis.

- status (Enum): Action state (PROPOSED, APPROVED, COMPLETED, DISMISSED).