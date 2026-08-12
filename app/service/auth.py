from sqlalchemy import select, or_
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.database.schema.auth_schema import User
from app.models.auth import Login, Register


class AuthService:
    def create_user(self, db: Session, request: Register) -> User:
        existing_user = db.scalar(
            select(User).where(
                or_(User.username == request.username, User.email == request.email)
            )
        )
        if existing_user:
            field = "Username" if existing_user.username == request.username else "Email"
            raise ValueError(f"{field} already registered")

        user = User(
            username=request.username,
            email=request.email,
            password=hash_password(request.password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def login(self, db: Session, request: Login) -> User | None:
        user = db.scalar(select(User).where(User.username == request.username))
        if not user or not verify_password(request.password, user.password):
            return None
        return user

    def get_user_by_id(self, db: Session, user_id: str) -> User | None:
        return db.scalar(select(User).where(User.id == user_id))
