from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    case_id: UUID
    filename: str
    file_size: int
    mime_type: str
    uploaded_at: datetime