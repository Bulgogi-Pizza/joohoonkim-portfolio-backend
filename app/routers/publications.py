from datetime import datetime
from typing import List, Optional

from app.database import get_db
from app.models import Publication
from app.security.security import require_admin
from app.utils.s3 import upload_file_to_s3
from fastapi import APIRouter, Depends, HTTPException, Query, File, UploadFile
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/publications", tags=["publications"])


@router.get("", response_model=List[Publication])
def get_publications(
    year: Optional[str] = Query(None, description="Filter by year"),
    contribution: Optional[str] = Query(None,
                                        description="Filter by contribution type: first-author, corresponding, co-author"),
    status: Optional[str] = Query(None,
                                  description="Filter by status: published, under-submission, in-press, in-review"),
    db: Session = Depends(get_db)
):
    query = db.query(Publication)

    if year:
        query = query.filter(Publication.year == year)

    if contribution:
        if contribution == "first-author":
            query = query.filter(Publication.is_first_author == True)
        elif contribution == "corresponding":
            query = query.filter(Publication.is_corresponding_author == True)
        elif contribution == "equal-contribution":
            query = query.filter(Publication.is_equal_contribution == True)
        else:  # co-author
            query = query.filter(
                Publication.is_first_author == False,
                Publication.is_corresponding_author == False,
                Publication.is_equal_contribution == False
            )

    if status:
        query = query.filter(Publication.status == status)

    return query.order_by(Publication.number.desc()).all()


@router.get("/years")
def get_available_years(db: Session = Depends(get_db)):
    """사용 가능한 연도 목록 반환"""
    years = db.query(Publication.year).distinct().all()
    return {"years": sorted([year[0] for year in years], reverse=True)}


@router.get("/stats")
def get_publication_stats(db: Session = Depends(get_db)):
    """출판물 통계 정보 반환"""
    total = db.query(Publication).count()
    first_author = db.query(Publication).filter(
        Publication.is_first_author == True).count()
    corresponding = db.query(Publication).filter(
        Publication.is_corresponding_author == True).count()
    under_submission = db.query(Publication).filter(
        Publication.status == "under-submission").count()

    return {
        "total": total,
        "first_author": first_author,
        "corresponding": corresponding,
        "under_submission": under_submission
    }


@router.get("/{publication_id}", response_model=Publication)
def get_publication(publication_id: int, db: Session = Depends(get_db)):
    publication = db.query(Publication).filter(
        Publication.id == publication_id).first()
    if not publication:
        raise HTTPException(status_code=404, detail="Publication not found")
    return publication


# Admin CRUD operations
@router.post("/", response_model=Publication)
def create_publication(publication: Publication, db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):
    publication.updated_at = datetime.utcnow()
    db.add(publication)
    db.commit()
    db.refresh(publication)
    return publication


@router.put("/{publication_id}", response_model=Publication)
def update_publication(publication_id: int, publication: Publication,
    db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):
    db_publication = db.query(Publication).filter(
        Publication.id == publication_id).first()
    if not db_publication:
        raise HTTPException(status_code=404, detail="Publication not found")

    for key, value in publication.dict(exclude_unset=True).items():
        if key != "id":  # ID는 업데이트하지 않음
            setattr(db_publication, key, value)

    db_publication.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_publication)
    return db_publication


@router.delete("/{publication_id}")
def delete_publication(publication_id: int, db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):
    publication = db.query(Publication).filter(
        Publication.id == publication_id).first()
    if not publication:
        raise HTTPException(status_code=404, detail="Publication not found")

    db.delete(publication)
    db.commit()
    return {"message": "Publication deleted successfully"}


@router.post("/upload-image")
async def upload_publication_image(
    file: UploadFile = File(...),
    admin: bool = Depends(require_admin)
):
    """
    논문 커버 이미지 또는 그래픽 업로드

    - S3 publications 폴더에 업로드
    - 업로드된 이미지 URL 반환
    """
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        # Upload to S3 (publications folder)
        s3_url = await upload_file_to_s3(file, folder="publications")
        return {"image_path": s3_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

