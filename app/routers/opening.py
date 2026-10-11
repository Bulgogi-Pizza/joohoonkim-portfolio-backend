from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Opening
from ..security.security import require_admin

router = APIRouter(prefix="/api/opening", tags=["opening"])


class OpeningUpdate(BaseModel):
    content: str


def get_opening_row(db: Session) -> Opening:
    opening = db.query(Opening).first()
    if not opening:
        raise HTTPException(status_code=404, detail="Opening not found")
    return opening


@router.get("", response_model=Opening)
def get_opening(db: Session = Depends(get_db)):
    return get_opening_row(db)


@router.put("", response_model=Opening)
def update_opening(
    data: OpeningUpdate,
    db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):
    opening = get_opening_row(db)
    opening.content = data.content
    opening.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(opening)
    return opening
