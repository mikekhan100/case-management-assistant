from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class CaseStatus(str, Enum):
    NEW = "NEW"
    UNDER_REVIEW = "UNDER_REVIEW"
    ACTION_REQUIRED = "ACTION_REQUIRED"
    CLOSED = "CLOSED"


class CaseCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Title of the case or enquiry")
    description: Optional[str] = Field(None, description="Initial summary or background notes")


class CaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    reference_number: str
    title: str
    description: Optional[str] = None
    status: CaseStatus
    created_at: datetime
    updated_at: datetime