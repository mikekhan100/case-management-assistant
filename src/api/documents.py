from typing import List
from uuid import UUID, uuid4
from datetime import datetime, timezone
from fastapi import APIRouter, File, HTTPException, UploadFile, status

from src.api.cases import cases_db
from src.schemas import DocumentResponse

router = APIRouter(prefix="/cases/{case_id}/documents", tags=["Documents"])

documents_db: dict[UUID, dict] = {}


@router.post("", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(case_id: UUID, file: UploadFile = File(...)) -> DocumentResponse:
    if case_id not in cases_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Case with ID {case_id} not found",
        )

    doc_id = uuid4()
    now = datetime.now(timezone.utc)
    content = await file.read()

    doc_record = {
        "id": doc_id,
        "case_id": case_id,
        "filename": file.filename or "unnamed_file.txt",
        "file_size": len(content),
        "mime_type": file.content_type or "text/plain",
        "uploaded_at": now,
    }

    documents_db[doc_id] = doc_record
    return DocumentResponse.model_validate(doc_record)


@router.get("", response_model=List[DocumentResponse])
async def list_documents(case_id: UUID) -> List[DocumentResponse]:
    if case_id not in cases_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Case with ID {case_id} not found",
        )
    return [
        DocumentResponse.model_validate(doc)
        for doc in documents_db.values()
        if doc["case_id"] == case_id
    ]