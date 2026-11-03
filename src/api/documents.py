from typing import List
from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.models import CaseModel, DocumentModel
from src.schemas import DocumentResponse
from src.services.file_storage import FileStorageService

router = APIRouter(prefix="/cases/{case_id}/documents", tags=["Documents"])
file_storage = FileStorageService()


@router.post("", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    case_id: UUID, file: UploadFile = File(...), db: Session = Depends(get_db)
) -> DocumentResponse:
    case = db.get(CaseModel, case_id)
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Case with ID {case_id} not found",
        )

    content = await file.read()
    doc_id = uuid4()
    filename = file.filename or "unnamed_file.txt"

    # Save binary file content to disk
    saved_path = file_storage.save_file(
        case_id=case_id,
        document_id=doc_id,
        filename=filename,
        content=content,
    )

    document = DocumentModel(
        id=doc_id,
        case_id=case_id,
        filename=filename,
        file_path=str(saved_path),
        file_size=len(content),
        mime_type=file.content_type or "text/plain",
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return DocumentResponse.model_validate(document)


@router.get("", response_model=List[DocumentResponse])
async def list_documents(
    case_id: UUID, db: Session = Depends(get_db)
) -> List[DocumentResponse]:
    case = db.get(CaseModel, case_id)
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Case with ID {case_id} not found",
        )

    stmt = select(DocumentModel).where(DocumentModel.case_id == case_id)
    documents = db.scalars(stmt).all()
    return [DocumentResponse.model_validate(d) for d in documents]