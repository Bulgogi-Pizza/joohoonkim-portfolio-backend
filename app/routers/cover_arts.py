import shutil
from datetime import datetime
from pathlib import Path
from typing import List

from app.database import get_db
from app.models import CoverArt
from app.security.security import require_admin
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi import File, UploadFile
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/cover-arts", tags=["cover-arts"])

UPLOAD_DIR_CA = Path("../frontend/static/uploads/cover-arts")
UPLOAD_DIR_CA.mkdir(parents=True, exist_ok=True)


@router.get("/", response_model=List[CoverArt])
def list_cover_arts(
    active_only: bool = Query(False, description="True면 is_active 항목만"),
    db: Session = Depends(get_db)
):
    query = db.query(CoverArt)
    if active_only:
        query = query.filter(CoverArt.is_active == True)
    return query.order_by(
        CoverArt.order_index.asc(),
        CoverArt.id.desc()
    ).all()


@router.get("/{item_id}", response_model=CoverArt)
def get_cover_art(item_id: int, db: Session = Depends(get_db)):
    item = db.query(CoverArt).filter(CoverArt.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="CoverArt not found")
    return item


@router.post("/", response_model=CoverArt)
def create_cover_art(item: CoverArt, db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)):
    item.updated_at = datetime.utcnow()
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/{item_id}", response_model=CoverArt)
def update_cover_art(
    item_id: int,
    patch: CoverArt,
    db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):
    db_item = db.query(CoverArt).filter(CoverArt.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="CoverArt not found")

    for k, v in patch.dict(exclude_unset=True).items():
        if k != "id":
            setattr(db_item, k, v)
    db_item.updated_at = datetime.utcnow()

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.delete("/{item_id}")
def delete_cover_art(item_id: int, db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)):
    item = db.query(CoverArt).filter(CoverArt.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="CoverArt not found")
    db.delete(item)
    db.commit()
    return {"message": "CoverArt deleted successfully"}


@router.post("/upload-image")
async def upload_cover_art_image(file: UploadFile = File(...),
    admin: bool = Depends(require_admin)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = UPLOAD_DIR_CA / filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"image_path": f"/static/uploads/cover-arts/{filename}"}
