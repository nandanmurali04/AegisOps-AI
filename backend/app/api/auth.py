from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserResponse,
    LoginRequest,
    Token,
)
from app.services.auth import create_user, login_user

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------------------------
# Register
# ------------------------------------
@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


# ------------------------------------
# Login
# ------------------------------------
@router.post("/login", response_model=Token)
def login(user: LoginRequest, db: Session = Depends(get_db)):
    token = login_user(db, user.email, user.password)

    if token is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return token


# ------------------------------------
# User Profile (Protected)
# ------------------------------------
@router.get("/profile")
def profile(
    current_user: User = Depends(get_current_user)
):
    return {
        "message": "Welcome!",
        "user": {
            "id": current_user.id,
            "full_name": current_user.full_name,
            "email": current_user.email,
            "role": current_user.role,
        },
    }


# ------------------------------------
# Admin Dashboard (Admin Only)
# ------------------------------------
@router.get("/admin/dashboard")
def admin_dashboard(
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Access denied. Admins only."
        )

    return {
        "message": "Welcome Admin!",
        "user": {
            "id": current_user.id,
            "full_name": current_user.full_name,
            "email": current_user.email,
            "role": current_user.role,
        },
    }