from typing import List

from app.security.security import require_admin
from app.utils.s3 import upload_file_to_s3
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Media

router = APIRouter(prefix="/api/media", tags=["media"])


@router.get("", response_model=List[Media])
def get_media(db: Session = Depends(get_db)):
    return db.query(Media).order_by(Media.date.desc()).all()


@router.post("", response_model=Media)
def create_media(media: Media, db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):
    db.add(media)
    db.commit()
    db.refresh(media)
    return media


@router.put("/{media_id}", response_model=Media)
def update_media(media_id: int, media: Media, db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):
    db_media = db.query(Media).filter(Media.id == media_id).first()
    if not db_media:
        raise HTTPException(status_code=404, detail="Media item not found")

    for key, value in media.dict(exclude_unset=True).items():
        setattr(db_media, key, value)

    db.commit()
    db.refresh(db_media)
    return db_media


@router.delete("/{media_id}")
def delete_media(media_id: int, db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):
    media = db.query(Media).filter(Media.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="Media item not found")

    db.delete(media)
    db.commit()
    return {"message": "Media item deleted successfully"}


@router.post("/upload-image")
async def upload_media_image(file: UploadFile = File(...),
    admin: bool = Depends(require_admin)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        # Upload to S3 (media folder)
        s3_url = await upload_file_to_s3(file, folder="media")
        return {"image_path": s3_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
