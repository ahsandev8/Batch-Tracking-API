from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.database.db import get_db
from app.database.schema.auth_schema import User
from app.service.auth import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
auth_service = AuthService()

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    payload = decode_access_token(token)
    if payload is None or (user_id := payload.get("sub")) is None:
        raise CREDENTIALS_EXCEPTION

    user = auth_service.get_user_by_id(db, user_id)
    if user is None:
        raise CREDENTIALS_EXCEPTION

    return user
