from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.models import CaseModel
from src.schemas import CaseCreate, CaseResponse, CaseStatus

router = APIRouter(prefix="/cases", tags=["Cases"])


@router.post("", response_model=CaseResponse, status_code=status.HTTP_201_CREATED)
async def create_case(
    payload: CaseCreate, db: Session = Depends(get_db)
) -> CaseResponse:
    # Calculate next sequence number for reference number
    case_count = db.scalar(select(func.count(CaseModel.id))) or 0
    ref_num = f"CAS-2026-{(case_count + 1):04d}"

    case = CaseModel(
        reference_number=ref_num,
        title=payload.title,
        description=payload.description,
        status=CaseStatus.NEW,
    )
    db.add(case)
    db.commit()
    db.refresh(case)
    return CaseResponse.model_validate(case)


@router.get("", response_model=List[CaseResponse])
async def list_cases(db: Session = Depends(get_db)) -> List[CaseResponse]:
    stmt = select(CaseModel).order_by(CaseModel.created_at.desc())
    cases = db.scalars(stmt).all()
    return [CaseResponse.model_validate(c) for c in cases]


@router.get("/{case_id}", response_model=CaseResponse)
async def get_case(case_id: UUID, db: Session = Depends(get_db)) -> CaseResponse:
    case = db.get(CaseModel, case_id)
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Case with ID {case_id} not found",
        )
    return CaseResponse.model_validate(case)