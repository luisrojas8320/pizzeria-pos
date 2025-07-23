from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    OWNER = "owner"
    STAFF = "staff"


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.STAFF
    is_active: bool = True
    
    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'Username must be alphanumeric'
        assert len(v) >= 3, 'Username must be at least 3 characters'
        return v


class UserCreate(UserBase):
    password: str
    
    @field_validator('password')
    @classmethod
    @classmethod
    def validate_password(cls, v):
        assert len(v) >= 8, 'Password must be at least 8 characters'
        assert any(c.isupper() for c in v), 'Password must contain uppercase letter'
        assert any(c.islower() for c in v), 'Password must contain lowercase letter'
        assert any(c.isdigit() for c in v), 'Password must contain digit'
        return v


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class UserInDB(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class User(UserInDB):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str