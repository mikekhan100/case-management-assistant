from pathlib import Path
from sqlalchemy.orm import Session
from src.models import CaseModel, DocumentModel
from src.services.file_storage import FileStorageService


class SummaryService:
    def __init__(self, file_storage: FileStorageService | None = None):
        self.file_storage = file_storage or FileStorageService()

    def generate_case_summary(self, case: CaseModel, db: Session) -> str:
        """Reads all uploaded documents for a case and generates a baseline executive summary."""
        documents = db.query(DocumentModel).filter(DocumentModel.case_id == case.id).all()

        if not documents:
            return f"Summary for case {case.reference_number}: No evidence documents uploaded yet."

        extracted_texts: list[str] = []
        for doc in documents:
            try:
                raw_bytes = self.file_storage.read_file(doc.file_path)
                # Attempt standard UTF-8 decoding for plain text files
                text_content = raw_bytes.decode("utf-8", errors="replace")
                extracted_texts.append(f"--- Document: {doc.filename} ---\n{text_content.strip()}")
            except Exception as exc:
                extracted_texts.append(f"--- Document: {doc.filename} ---\n[Error reading file: {exc}]")

        combined_evidence = "\n\n".join(extracted_texts)

        # Baseline rule-based summary (to be replaced by external LLM provider call in Phase 2)
        summary_content = (
            f"Executive Summary for Case {case.reference_number} ({case.title})\n"
            f"Total Documents Ingested: {len(documents)}\n\n"
            f"Key Extracted Evidence:\n{combined_evidence[:2000]}"  # Truncate for MVP display limits
        )
        if len(combined_evidence) > 2000:
            summary_content += "\n\n[Truncated for length...]"

        return summary_content