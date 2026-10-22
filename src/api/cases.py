from typing import List
from uuid import UUID, uuid4
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, status

from src.schemas import CaseCreate, CaseResponse, CaseStatus

router = APIRouter(prefix="/cases", tags=["Cases"])

# In-memory storage placeholder for initial endpoint verification
cases_db: dict[UUID, dict] = {}


@router.post("", response_model=CaseResponse, status_code=status.HTTP_201_CREATED)
async def create_case(payload: CaseCreate) -> CaseResponse:
    case_id = uuid4()
    now = datetime.now(timezone.utc)
    
    # Generate human-readable reference number
    ref_num = f"CAS-2026-{(len(cases_db) + 1):04d}"

    case_record = {
        "id": case_id,
        "reference_number": ref_num,
        "title": payload.title,
        "description": payload.description,
        "status": CaseStatus.NEW,
        "created_at": now,
        "updated_at": now,
    }
    
    cases_db[case_id] = case_record
    return CaseResponse.model_validate(case_record)


@router.get("", response_model=List[CaseResponse])
async def list_cases() -> List[CaseResponse]:
    return [CaseResponse.model_validate(c) for c in cases_db.values()]


@router.get("/{case_id}", response_model=CaseResponse)
async def get_case(case_id: UUID) -> CaseResponse:
    if case_id not in cases_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Case with ID {case_id} not found",
        )
    return CaseResponse.model_validate(cases_db[case_id])