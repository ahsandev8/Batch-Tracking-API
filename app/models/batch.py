from pydantic import BaseModel
import uuid
from enum import Enum
from datetime import datetime
from pydantic import ConfigDict

class BatchStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class BatchCreate(BaseModel):
    sample_id: str
    batch_type: str
    submitted_by: str

class BatchResponse(BaseModel):
    id: uuid.UUID
    sample_id: str
    batch_type: str
    submitted_by: str
    status: BatchStatus
    result: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class BatchStatusUpdate(BaseModel):
    status: BatchStatus
