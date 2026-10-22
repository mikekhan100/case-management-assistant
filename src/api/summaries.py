from uuid import UUID, uuid4
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, status

from src.api.cases import cases_db
from src.schemas import SummaryResponse

router = APIRouter(prefix="/cases/{case_id}/summary", tags=["Summaries"])

summaries_db: dict[UUID, dict] = {}


@router.post("", response_model=SummaryResponse, status_code=status.HTTP_201_CREATED)
async def generate_summary(case_id: UUID) -> SummaryResponse:
    if case_id not in cases_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Case with ID {case_id} not found",
        )

    summary_id = uuid4()
    now = datetime.now(timezone.utc)

    summary_record = {
        "id": summary_id,
        "case_id": case_id,
        "content": f"Baseline summary for case {cases_db[case_id]['reference_number']}: Under review.",
        "model_version": "baseline-v1",
        "created_at": now,
    }

    summaries_db[case_id] = summary_record
    return SummaryResponse.model_validate(summary_record)


@router.get("", response_model=SummaryResponse)
async def get_summary(case_id: UUID) -> SummaryResponse:
    if case_id not in cases_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Case with ID {case_id} not found",
        )
    if case_id not in summaries_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No summary generated yet for case {case_id}",
        )
    return SummaryResponse.model_validate(summaries_db[case_id])