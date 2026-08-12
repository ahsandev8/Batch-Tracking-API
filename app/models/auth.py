from pydantic import BaseModel, Field, EmailStr


class Login(BaseModel):
    username: str = Field(..., json_schema_extra={"example": "john_doe"})
    password: str = Field(..., json_schema_extra={"example": "password123"})


class Register(BaseModel):
    username: str = Field(..., json_schema_extra={"example": "john_doe"})
    email: EmailStr = Field(..., json_schema_extra={"example": "zDd2G@example.com"})
    password: str = Field(..., json_schema_extra={"example": "password123"})
