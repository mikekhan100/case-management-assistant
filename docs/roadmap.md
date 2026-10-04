# Product Roadmap & Future Capabilities

This roadmap outlines the planned versions for the Case Management Assistant, moving from the MVP baseline to advanced AI-assisted decision support.

---

## Version 1: MVP Baseline
* Core case creation and metadata tracking
* Plain text and PDF document upload and file storage
* Document viewing and metadata retrieval
* Single-prompt document summarisation

---

## Version 2: Timeline & Entity Intelligence
* **Timeline Extraction:** Automatic extraction of chronological events, dates and milestones from uploaded case files.
* **Entity Extraction:** Identification and categorisation of key stakeholders (investigators, whistleblowers, witnesses, employers and pension schemes).
* **Risk & Flag Identification:** Automated flagging of statutory deadline risks, missing documentation or high-risk indicators.

---

## Version 3: Deep Search & Semantic Retrieval (RAG)
* **Vector Store Integration:** Chunking and embedding case documents using `pgvector` or dedicated vector database.
* **Semantic Search:** Natural language search across complex multi-document case history.
* **Grounded Question Answering:** Targeted QA interface with precise page-level citations and source snippets to preserve evidence provenance.

---

## Version 4: Decision Support & Consistency Analysis
* **Suggested Next Actions:** Rule and LLM-assisted recommendations for proportionate regulatory next steps (e.g. issuing statutory notices or fines).
* **Contradiction Detection:** Automatic cross-referencing of statements, emails and meeting notes to highlight factual inconsistencies across documents.
* **Audit Trail Engine:** Comprehensive logging of AI reasoning, prompt versions, retrieved context and investigator overrides for legal accountability.

---

## Version 5: Multi-Case Analytics & Intelligence
* **Cross-Case Entity Matching:** Detect recurring subjects, employers or advisers across separate cases.
* **Macro Trend Dashboard:** Aggregated insights into regulatory breach types, resolution times and enforcement outcomes.