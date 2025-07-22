from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.security import create_access_token, verify_password, get_password_hash
from ..core.auth import get_user_by_username, get_current_user, get_current_active_owner
from ..core.config import settings
from ..models.users import User
from ..schemas.users import Token, UserCreate, User as UserSchema, LoginRequest


router = APIRouter()


@router.post("/login", response_model=Token)
def login_for_access_token(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = get_user_by_username(db, username=login_data.username)
    
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            subject=user.username, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/register", response_model=UserSchema)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_owner)
) -> Any:
    """
    Create new user. Only owners can create new users.
    """
    # Check if user already exists
    existing_user = get_user_by_username(db, username=user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        role=user_data.role,
        is_active=user_data.is_active
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


@router.get("/me", response_model=UserSchema)
def read_users_me(current_user: User = Depends(get_current_user)) -> Any:
    """
    Get current user information
    """
    return current_user


@router.post("/test-token", response_model=UserSchema)
def test_token(current_user: User = Depends(get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user