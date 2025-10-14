from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..security.auth import require_roles

router = APIRouter()


@router.get("/users")
def list_users(db: Session = Depends(get_db), user=Depends(require_roles("admin"))):
    users = db.query(User).all()
    return users
