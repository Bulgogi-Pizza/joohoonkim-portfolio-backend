import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import List

from app.database import get_db
from app.models import ResearchArea
from app.security.security import require_admin
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/research-areas", tags=["research-areas"])

# 업로드 디렉토리 설정
UPLOAD_DIR = Path("../frontend/static/uploads/icons")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# NEW: 본문 이미지 업로드 디렉토리
CONTENT_UPLOAD_DIR = Path("../frontend/static/uploads/research-areas")
CONTENT_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.get("/", response_model=List[ResearchArea])
def get_research_areas(
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    query = db.query(ResearchArea)
    if active_only:
        query = query.filter(ResearchArea.is_active == True)
    return query.order_by(ResearchArea.order_index.asc()).all()


@router.get("/{slug}", response_model=ResearchArea)
def get_research_area(slug: str, db: Session = Depends(get_db)):
    area = db.query(ResearchArea).filter(ResearchArea.slug == slug).first()
    if not area:
        raise HTTPException(status_code=404, detail="Research area not found")
    return area


@router.post("/", response_model=ResearchArea)
def create_research_area(area_data: ResearchArea,
    db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):
    area_data.updated_at = datetime.utcnow()
    db.add(area_data)
    db.commit()
    db.refresh(area_data)
    return area_data


@router.put("/{area_id}", response_model=ResearchArea)
def update_research_area(
    area_id: int,
    area_data: ResearchArea,
    db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):
    area = db.query(ResearchArea).filter(ResearchArea.id == area_id).first()
    if not area:
        raise HTTPException(status_code=404, detail="Research area not found")

    for key, value in area_data.dict(exclude_unset=True).items():
        if key != "id":
            setattr(area, key, value)

    area.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(area)
    return area


@router.delete("/{area_id}")
def delete_research_area(
    area_id: int,
    db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):
    area = db.query(ResearchArea).filter(ResearchArea.id == area_id).first()
    if not area:
        raise HTTPException(status_code=404, detail="Research area not found")

    db.delete(area)
    db.commit()
    return {"message": "Research area deleted successfully"}


@router.post("/upload-icon")
async def upload_icon(file: UploadFile = File(...),
    admin: bool = Depends(require_admin)

):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe = re.sub(r'[^A-Za-z0-9_.-]', '_', file.filename)
    filename = f"{timestamp}_{safe}"
    file_path = UPLOAD_DIR / filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"icon_path": f"/static/uploads/icons/{filename}"}


# NEW: 본문 이미지 업로드
@router.post("/upload-content-image")
async def upload_content_image(file: UploadFile = File(...),
    admin: bool = Depends(require_admin)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    safe = re.sub(r'[^A-Za-z0-9_.-]', '_', file.filename)
    filename = f"{timestamp}_{safe}"
    file_path = CONTENT_UPLOAD_DIR / filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 프론트에서 Markdown으로 바로 삽입하기 좋은 절대 경로 반환
    return {"image_path": f"/static/uploads/research-areas/{filename}"}
