from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.models import CaseModel, SummaryModel
from src.schemas import SummaryResponse

router = APIRouter(prefix="/cases/{case_id}/summary", tags=["Summaries"])


@router.post("", response_model=SummaryResponse, status_code=status.HTTP_201_CREATED)
async def generate_summary(
    case_id: UUID, db: Session = Depends(get_db)
) -> SummaryResponse:
    case = db.get(CaseModel, case_id)
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Case with ID {case_id} not found",
        )

    # Check if a summary already exists
    stmt = select(SummaryModel).where(SummaryModel.case_id == case_id)
    existing_summary = db.scalars(stmt).first()

    if existing_summary:
        existing_summary.content = (
            f"Updated baseline summary for case {case.reference_number}: Under review."
        )
        db.commit()
        db.refresh(existing_summary)
        return SummaryResponse.model_validate(existing_summary)

    summary = SummaryModel(
        case_id=case_id,
        content=f"Baseline summary for case {case.reference_number}: Under review.",
        model_version="baseline-v1",
    )
    db.add(summary)
    db.commit()
    db.refresh(summary)
    return SummaryResponse.model_validate(summary)


@router.get("", response_model=SummaryResponse)
async def get_summary(
    case_id: UUID, db: Session = Depends(get_db)
) -> SummaryResponse:
    case = db.get(CaseModel, case_id)
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Case with ID {case_id} not found",
        )

    stmt = select(SummaryModel).where(SummaryModel.case_id == case_id)
    summary = db.scalars(stmt).first()
    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No summary generated yet for case {case_id}",
        )
    return SummaryResponse.model_validate(summary)