from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class SummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    case_id: UUID
    content: str
    model_version: str
    created_at: datetime