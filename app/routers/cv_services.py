from datetime import datetime
from typing import List

from app.security.security import require_admin
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import CVService

router = APIRouter(prefix="/api/cv-services", tags=["cv-services"])


@router.get("", response_model=List[CVService])
def get_cv_services(db: Session = Depends(get_db)):
    return db.query(CVService).order_by(CVService.order_index.asc()).all()


@router.get("/{service_id}", response_model=CVService)
def get_cv_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(CVService).filter(CVService.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="CV service not found")
    return service


@router.post("", response_model=CVService)
def create_cv_service(
    service: CVService,
    db: Session = Depends(get_db),
    admin: bool = Depends(require_admin),
):
    db.add(service)
    db.commit()
    db.refresh(service)
    return service


@router.put("/{service_id}", response_model=CVService)
def update_cv_service(
    service_id: int,
    service: CVService,
    db: Session = Depends(get_db),
    admin: bool = Depends(require_admin),
):
    db_service = db.query(CVService).filter(CVService.id == service_id).first()
    if not db_service:
        raise HTTPException(status_code=404, detail="CV service not found")

    for key, value in service.dict(exclude_unset=True).items():
        setattr(db_service, key, value)
    db_service.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(db_service)
    return db_service


@router.delete("/{service_id}")
def delete_cv_service(
    service_id: int,
    db: Session = Depends(get_db),
    admin: bool = Depends(require_admin),
):
    service = db.query(CVService).filter(CVService.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="CV service not found")

    db.delete(service)
    db.commit()
    return {"message": "CV service deleted successfully"}
