# Batch Tracking API

This repository provides a small FastAPI application for tracking batches.

Running the app

- Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

- Start the server:

```bash
uvicorn main:app --reload
```

API endpoints

- `POST /auth/register` — register a new user. Body: `username`, `email`, `password`.
- `POST /auth/login` — login with form data `username` and `password`. Returns access token.
- `GET /auth/me` — get current user profile (requires authentication).
- `POST /batch/` — create a new batch. Body: `sample_id`, `batch_type`, `submitted_by`.
- `GET /batch/{batch_id}` — get batch by id.
- `PUT /batch/{batch_id}` — update batch status. Body: `status` (queued, processing, completed, failed).
- `GET /batch/` — list batches with optional query params `status`, `type`, `page`, `page_size`.

Testing

Tests are written using `pytest` and FastAPI's `TestClient` and are designed to run without a real database by monkeypatching services and dependencies.

Run tests:

```bash
pytest -q
```

# Batch-Tracking-API
