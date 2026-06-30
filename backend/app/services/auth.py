from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.security import hash_password


def create_user(db: Session, user: UserCreate):

    hashed = hash_password(user.password)

    db_user = User(
    full_name=user.full_name,
    email=user.email,
    hashed_password=hashed
)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user