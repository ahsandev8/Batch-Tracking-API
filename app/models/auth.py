from pydantic import BaseModel, Field, EmailStr ,ConfigDict
from uuid import UUID
from datetime import datetime

class Login(BaseModel):
    username: str = Field(..., json_schema_extra={"example": "john_doe"})
    password: str = Field(..., json_schema_extra={"example": "password123"})


class Register(BaseModel):
    username: str = Field(..., json_schema_extra={"example": "john_doe"})
    email: EmailStr = Field(..., json_schema_extra={"example": "zDd2G@example.com"})
    password: str = Field(..., json_schema_extra={"example": "password123"})

class UserProfile(BaseModel):
    id: UUID
    username: str
    email: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
