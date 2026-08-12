from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.core.security import create_access_token
from app.database.db import get_db
from app.database.schema.auth_schema import User
from app.models.auth import Login, Register, Token, UserProfile
from app.service.auth import AuthService
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["auth"])
auth_service = AuthService()


@router.post("/register", response_model=UserProfile, status_code=status.HTTP_201_CREATED)
async def register(request: Register, db: Session = Depends(get_db)):
    try:
        return auth_service.create_user(db, request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    login_request = Login(username=form_data.username, password=form_data.password)
    user = auth_service.login(db, login_request)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    access_token = create_access_token(data={"sub": str(user.id)})
    return Token(access_token=access_token)

@router.get("/me", response_model=UserProfile)
async def get_profile(current_user: User = Depends(get_current_user)):
    return current_user
