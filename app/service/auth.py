from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.database.schema.auth_schema import User
from app.models.auth import Login, Register


class AuthService:
    def create_user(self, db: Session, request: Register) -> User:
        if not request.email:
            raise ValueError("Email is required")

        if not request.password:
            raise ValueError("Password is required")

        if not request.username:
            raise ValueError("Username is required")

        existing_user = (
            db.query(User)
            .filter((User.username == request.username) | (User.email == request.email))
            .first()
        )
        if existing_user:
            raise ValueError("User already exists")

        hashed = hash_password(request.password)
        user = User(username=request.username, email=request.email, password=hashed)

        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def login(self, db: Session, request: Login):
        user = db.query(User).filter(User.username == request.username).first()
        if not user:
            return None

        if not verify_password(request.password, user.password):
            return None

        return user

    def get_user(self, db: Session, username: str):
        return db.query(User).filter(User.username == username).first()
