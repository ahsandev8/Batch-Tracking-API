from uuid import UUID
from app.models.batch import BatchResponse
from app.database.db import Session
from app.database.schema.batch_schema import Batch
from app.models.batch import BatchCreate, BatchStatusUpdate,BatchStatus

from datetime import datetime
from fastapi import HTTPException, status

class BatchService:

  VALID_TRANSITIONS = {
        BatchStatus.QUEUED: [BatchStatus.PROCESSING],
        BatchStatus.PROCESSING: [BatchStatus.COMPLETED],
        BatchStatus.COMPLETED: [],
    }

  def create_batch(self, db: Session, batch: BatchCreate) -> BatchResponse:
    new_batch = Batch(**batch.dict())
    db.add(new_batch)
    db.commit()
    db.refresh(new_batch)
    return new_batch

  def get_batch_by_id(self, db: Session, batch_id: UUID) -> BatchResponse:
    batch = db.get(Batch, batch_id)
    if batch is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Batch not found")
    return batch

  def update_batch_status(self, db: Session, batch_id: UUID, status_update: BatchStatusUpdate):
    batch = db.get(Batch, batch_id)
    if batch is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Batch not found")
    if status_update.status not in self.VALID_TRANSITIONS[batch.status]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid batch status transition")
    batch.status = status_update.status
    batch.updated_at = datetime.now()
    db.commit()
    db.refresh(batch)
    return batch
