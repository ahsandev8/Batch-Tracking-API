"""
Seed script for populating the batches table with sample data.

Usage:
    python -m app.database.seed
    python -m app.database.seed --clear
    python -m app.database.seed --count 50
"""

import argparse
import random
import uuid
from datetime import datetime, timedelta, timezone

from app.database.db import SessionLocal
from app.database.schema.batch_schema import Batch
from app.models.batch import BatchStatus

BATCH_TYPES = ["PCR", "Sequencing", "Extraction", "QC", "Library Prep"]
SUBMITTERS = ["ahsan", "john_doe", "jane_smith", "lab_tech_01", "qa_reviewer"]

STATUS_WEIGHTS = {
    BatchStatus.QUEUED: 0.15,
    BatchStatus.PROCESSING: 0.15,
    BatchStatus.COMPLETED: 0.55,
    BatchStatus.FAILED: 0.15,
}

FAILURE_REASONS = [
    "Sample degraded beyond usable threshold",
    "Instrument calibration error during run",
    "Contamination detected in control well",
    "Insufficient sample volume for processing",
    "Reagent lot failed QC checks",
]

DEFAULT_SEED_COUNT = 25


def random_recent_datetime(days_back: int = 30) -> datetime:
    offset = timedelta(
        days=random.randint(0, days_back),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
    )
    return datetime.now(timezone.utc) - offset


def weighted_status() -> BatchStatus:
    statuses = list(STATUS_WEIGHTS.keys())
    weights = list(STATUS_WEIGHTS.values())
    return random.choices(statuses, weights=weights, k=1)[0]


def build_result(status: BatchStatus, sample_id: str) -> str | None:
    if status == BatchStatus.COMPLETED:
        return f"{sample_id} processed successfully — all QC checks passed"
    if status == BatchStatus.FAILED:
        return f"{sample_id} failed: {random.choice(FAILURE_REASONS)}"
    return None


def build_batches(count: int) -> list[Batch]:
    batches = []

    for i in range(count):
        status = weighted_status()
        created = random_recent_datetime()

        if status == BatchStatus.QUEUED:
            updated = created
        else:
            updated = created + timedelta(minutes=random.randint(5, 240))

        sample_id = f"SMP-{1000 + i}"

        batch = Batch(
            id=uuid.uuid4(),
            sample_id=sample_id,
            batch_type=random.choice(BATCH_TYPES),
            submitted_by=random.choice(SUBMITTERS),
            status=status,
            result=build_result(status, sample_id),
            created_at=created,
            updated_at=updated,
        )
        batches.append(batch)

    return batches


def seed_batches(count: int, clear_existing: bool = False) -> None:
    db = SessionLocal()
    try:
        if clear_existing:
            deleted = db.query(Batch).delete()
            print(f"Deleted {deleted} existing batch(es).")

        batches = build_batches(count)
        db.add_all(batches)
        db.commit()

        counts = {status: 0 for status in BatchStatus}
        for b in batches:
            counts[b.status] += 1

        print(f"Seeded {len(batches)} batch(es):")
        for status, n in counts.items():
            print(f"  {status.value:<12} {n}")

    except Exception as e:
        db.rollback()
        print(f"Seeding failed: {e}")
        raise
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description="Seed the batches table with sample data.")
    parser.add_argument(
        "--count",
        type=int,
        default=DEFAULT_SEED_COUNT,
        help=f"Number of batches to create (default: {DEFAULT_SEED_COUNT})",
    )
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Delete all existing batches before seeding",
    )
    args = parser.parse_args()

    if args.count < 1:
        parser.error("--count must be at least 1")

    seed_batches(count=args.count, clear_existing=args.clear)


if __name__ == "__main__":
    main()
