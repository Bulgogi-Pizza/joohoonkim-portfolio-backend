from typing import List

from app.security.security import require_admin
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Conference

router = APIRouter(prefix="/api/conferences", tags=["conferences"])


@router.get("", response_model=List[Conference])
def get_conferences(db: Session = Depends(get_db)):
    return db.query(Conference).order_by(Conference.date.desc()).all()


@router.post("/", response_model=Conference)
def create_conference(conference: Conference, db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)):
    db.add(conference)
    db.commit()
    db.refresh(conference)
    return conference


@router.put("/{conference_id}", response_model=Conference)
def update_conference(conference_id: int, conference: Conference,
    db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):
    db_conference = db.query(Conference).filter(
        Conference.id == conference_id).first()
    if not db_conference:
        raise HTTPException(status_code=404, detail="Conference not found")

    for key, value in conference.dict(exclude_unset=True).items():
        setattr(db_conference, key, value)

    db.commit()
    db.refresh(db_conference)
    return db_conference


@router.delete("/{conference_id}")
def delete_conference(conference_id: int, db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):
    conference = db.query(Conference).filter(
        Conference.id == conference_id).first()
    if not conference:
        raise HTTPException(status_code=404, detail="Conference not found")

    db.delete(conference)
    db.commit()
    return {"message": "Conference deleted successfully"}
