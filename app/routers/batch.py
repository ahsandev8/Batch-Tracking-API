from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.service.batch import BatchService
from app.database.db import get_db
from app.models.batch import BatchCreate, BatchStatusUpdate,BatchStatus
from app.models.batch import BatchResponse
from app.core.dependencies import get_current_user
from app.database.schema.auth_schema import User

router = APIRouter(prefix="/batch", tags=["batch"])
batch_service = BatchService()


@router.post("/", response_model=BatchResponse, status_code=status.HTTP_201_CREATED)
async def create_batch(
    batch: BatchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return batch_service.create_batch(db, batch)

@router.get("/{batch_id}", response_model=BatchResponse)
async def get_batch_by_id(
    batch_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    batch = batch_service.get_batch_by_id(db, batch_id)
    if not batch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Batch not found",
        )
    return batch

@router.put("/{batch_id}", response_model=BatchResponse)
async def update_batch_status(
    batch_id: UUID,
    status_update: BatchStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    batch = batch_service.update_batch_status(db, batch_id, status_update)
    if not batch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Batch not found",
        )
    return batch
