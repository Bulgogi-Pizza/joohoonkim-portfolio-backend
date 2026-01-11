from typing import List

from app.security.security import require_admin
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Experience

router = APIRouter(prefix="/api/experience", tags=["experience"])


@router.get("", response_model=List[Experience])
def get_experience(db: Session = Depends(get_db)):
    return db.query(Experience).all()


@router.post("", response_model=Experience)
def create_experience(experience: Experience, db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)):
    db.add(experience)
    db.commit()
    db.refresh(experience)
    return experience


@router.put("/{experience_id}", response_model=Experience)
def update_experience(experience_id: int, experience: Experience,
    db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):
    db_experience = db.query(Experience).filter(
        Experience.id == experience_id).first()
    if not db_experience:
        raise HTTPException(status_code=404, detail="Experience item not found")

    for key, value in experience.dict(exclude_unset=True).items():
        setattr(db_experience, key, value)

    db.commit()
    db.refresh(db_experience)
    return db_experience


@router.delete("/{experience_id}")
def delete_experience(experience_id: int, db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):
    experience = db.query(Experience).filter(
        Experience.id == experience_id).first()
    if not experience:
        raise HTTPException(status_code=404, detail="Experience item not found")

    db.delete(experience)
    db.commit()
    return {"message": "Experience item deleted successfully"}
