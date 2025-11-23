from typing import List

from app.security.security import require_admin
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Education

router = APIRouter(prefix="/api/education", tags=["education"])


@router.get("/", response_model=List[Education])
def get_education(db: Session = Depends(get_db)):
    return db.query(Education).all()


@router.get("/{education_id}", response_model=Education)
def get_education_item(education_id: int, db: Session = Depends(get_db)):
    education = db.query(Education).filter(Education.id == education_id).first()
    if not education:
        raise HTTPException(status_code=404, detail="Education item not found")
    return education


# Admin CRUD operations
@router.post("/", response_model=Education)
def create_education(education: Education, db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):
    db.add(education)
    db.commit()
    db.refresh(education)
    return education


@router.put("/{education_id}", response_model=Education)
def update_education(education_id: int, education: Education,
    db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):
    db_education = db.query(Education).filter(
        Education.id == education_id).first()
    if not db_education:
        raise HTTPException(status_code=404, detail="Education item not found")

    for key, value in education.dict(exclude_unset=True).items():
        setattr(db_education, key, value)

    db.commit()
    db.refresh(db_education)
    return db_education


@router.delete("/{education_id}")
def delete_education(education_id: int, db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)):
    education = db.query(Education).filter(Education.id == education_id).first()
    if not education:
        raise HTTPException(status_code=404, detail="Education item not found")

    db.delete(education)
    db.commit()
    return {"message": "Education item deleted successfully"}
