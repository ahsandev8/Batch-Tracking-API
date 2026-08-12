
from sqlalchemy import text
from app.database.db import Base, engine

from app.database.schema import auth_schema, batch_schema  # noqa: F401


def reset_database():
    confirm = input(
        "This will DROP ALL TABLES AND TYPES and recreate them. Type 'yes' to continue: "
    )
    if confirm.strip().lower() != "yes":
        print("Aborted.")
        return

    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)

    print("Dropping leftover enum types...")
    with engine.connect() as conn:
        conn.execute(text("DROP TYPE IF EXISTS batchstatus CASCADE"))
        conn.commit()

    print("Creating all tables and types...")
    Base.metadata.create_all(bind=engine)

    print("Done.")


if __name__ == "__main__":
    reset_database()
