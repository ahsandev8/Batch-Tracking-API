import uuid
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from main import app

from app.routers import auth as auth_router_module
from app.routers import batch as batch_router_module
from app.core.dependencies import get_current_user


client = TestClient(app)


def make_iso_now():
    return datetime.now(timezone.utc).isoformat()


@pytest.fixture(autouse=True)
def override_deps(monkeypatch):
    # Provide a fake current user for endpoints that require authentication
    fake_user = {
        "id": str(uuid.uuid4()),
        "username": "testuser",
        "email": "test@example.com",
        "created_at": make_iso_now(),
        "updated_at": make_iso_now(),
    }

    monkeypatch.setattr(auth_router_module, "auth_service", auth_router_module.auth_service)
    monkeypatch.setattr(batch_router_module, "batch_service", batch_router_module.batch_service)

    app.dependency_overrides[get_current_user] = lambda: fake_user

    yield

    app.dependency_overrides.clear()


def test_auth_register_and_login_and_me(monkeypatch):
    now = make_iso_now()
    created = {
        "id": str(uuid.uuid4()),
        "username": "testuser",
        "email": "test@example.com",
        "created_at": now,
        "updated_at": now,
    }

    # Patch create_user
    monkeypatch.setattr(auth_router_module.auth_service, "create_user", lambda db, req: created)

    resp = client.post("/auth/register", json={"username": "testuser", "email": "test@example.com", "password": "password123"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"

    # Patch login to return a user-like object and patch token creation
    monkeypatch.setattr(auth_router_module.auth_service, "login", lambda db, req: created)
    monkeypatch.setattr(auth_router_module, "create_access_token", lambda data: "fake-token")

    resp = client.post("/auth/login", data={"username": "testuser", "password": "password123"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["access_token"] == "fake-token"

    # GET /auth/me uses dependency override
    resp = client.get("/auth/me")
    assert resp.status_code == 200
    data = resp.json()
    assert data["username"] == "testuser"


def test_batch_crud_and_list(monkeypatch):
    now = make_iso_now()
    batch_id = str(uuid.uuid4())
    sample = {
        "id": batch_id,
        "sample_id": "SAMPLE123",
        "batch_type": "typeA",
        "submitted_by": "tester",
        "status": "queued",
        "result": None,
        "created_at": now,
        "updated_at": now,
    }

    # Patch batch service methods
    monkeypatch.setattr(batch_router_module.batch_service, "create_batch", lambda db, b: sample)
    monkeypatch.setattr(batch_router_module.batch_service, "get_batch_by_id", lambda db, bid: sample)
    monkeypatch.setattr(batch_router_module.batch_service, "update_batch_status", lambda db, bid, su: {**sample, "status": su.status})
    monkeypatch.setattr(batch_router_module.batch_service, "list_batches", lambda db, status, batch_type, page, page_size: ([sample], 1))

    # Create
    resp = client.post("/batch/", json={"sample_id": "SAMPLE123", "batch_type": "typeA", "submitted_by": "tester"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["sample_id"] == "SAMPLE123"

    # Get by id
    resp = client.get(f"/batch/{batch_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == batch_id

    # Update status
    resp = client.put(f"/batch/{batch_id}", json={"status": "processing"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "processing"

    # List
    resp = client.get("/batch/?page=1&page_size=10")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert isinstance(data["items"], list)
