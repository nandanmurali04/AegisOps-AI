from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.schemas.user import UserCreate, UserResponse, LoginRequest, Token
from app.services.auth import create_user, login_user
from app.utils.security import verify_access_token

router = APIRouter()

security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------------------------
# Get Current User from JWT
# ------------------------------------
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    payload = verify_access_token(credentials.credentials)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return payload


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
    current_user=Depends(get_current_user)
):
    return {
        "message": "Welcome!",
        "user": current_user
    }


# ------------------------------------
# Admin Dashboard (Admin Only)
# ------------------------------------
@router.get("/admin/dashboard")
def admin_dashboard(
    current_user=Depends(get_current_user)
):
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Access denied. Admins only."
        )

    return {
        "message": "Welcome Admin!",
        "user": current_user
    }