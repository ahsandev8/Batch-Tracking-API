import uuid
from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.models.batch import BatchStatus

from app.database.db import Base


class Batch(Base):
    __tablename__ = "batches"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    sample_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    batch_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    submitted_by: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    status: Mapped[BatchStatus] = mapped_column(
        Enum(
            BatchStatus,
            name="batchstatus",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        default=BatchStatus.QUEUED,
        nullable=False,
    )

    result: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
