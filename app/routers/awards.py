from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Award
from ..security.security import require_admin

router = APIRouter(prefix="/api/awards", tags=["awards"])


@router.get("", response_model=List[Award])
def get_awards(db: Session = Depends(get_db)):
    return db.query(Award).order_by(Award.year.desc()).all()


@router.post("", response_model=Award)
def create_award(
    award: Award,
    db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):
    db.add(award)
    db.commit()
    db.refresh(award)
    return award


@router.put("/{award_id}", response_model=Award)
def update_award(
    award_id: int,
    award: Award,
    db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):
    db_award = db.query(Award).filter(Award.id == award_id).first()
    if not db_award:
        raise HTTPException(status_code=404, detail="Award not found")

    for key, value in award.dict(exclude_unset=True).items():
        setattr(db_award, key, value)

    db.commit()
    db.refresh(db_award)
    return db_award


@router.delete("/{award_id}")
def delete_award(
    award_id: int,
    db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):
    award = db.query(Award).filter(Award.id == award_id).first()
    if not award:
        raise HTTPException(status_code=404, detail="Award not found")

    db.delete(award)
    db.commit()
    return {"message": "Award deleted successfully"}
