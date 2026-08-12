from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.service.auth import AuthService
from app.models.auth import Login, Register, UserProfile
from app.core.security import create_access_token
from app.database.db import get_db

router = APIRouter(prefix="/auth")
auth_service = AuthService()


@router.post("/login")
async def login(request: Login, db: Session = Depends(get_db)):
    user = auth_service.login(db, request)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    access_token = create_access_token(data={"sub": str(user.id), "username": user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }



@router.post("/register")
async def register(request: Register, db: Session = Depends(get_db)):
    try:
        user = auth_service.create_user(db, request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return {"message": "User created", "username": user.username}


@router.get("/me", response_model=UserProfile)
async def get_profile( ):
    return current_user
