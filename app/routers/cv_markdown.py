from datetime import datetime
from typing import List, Optional

from app.database import get_db
from app.models import MarkdownCV
from app.security.security import require_admin
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/cv-markdown", tags=["cv-markdown"])


class CVMarkdownCreate(BaseModel):
    title: str
    content: str
    description: Optional[str] = None


class CVMarkdownUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    description: Optional[str] = None


@router.get("/documents", response_model=List[MarkdownCV])
def get_cv_documents(db: Session = Depends(get_db)):
    """모든 마크다운 CV 문서 목록 조회"""
    return db.query(MarkdownCV).order_by(MarkdownCV.updated_at.desc()).all()


@router.get("/documents/active", response_model=Optional[MarkdownCV])
def get_active_cv_document(db: Session = Depends(get_db)):
    """현재 활성화된 CV 문서 조회"""
    return db.query(MarkdownCV).filter(MarkdownCV.is_active == True).first()


@router.get("/documents/{doc_id}", response_model=MarkdownCV)
def get_cv_document(doc_id: int, db: Session = Depends(get_db)):
    """특정 CV 문서 조회"""
    cv_doc = db.query(MarkdownCV).filter(MarkdownCV.id == doc_id).first()
    if not cv_doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return cv_doc


@router.post("/documents", response_model=MarkdownCV)
def create_cv_document(cv_data: CVMarkdownCreate,
    db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):
    """새 마크다운 CV 문서 생성"""
    try:
        cv_doc = MarkdownCV(
            title=cv_data.title,
            content=cv_data.content,
            description=cv_data.description,
            is_active=False
        )

        db.add(cv_doc)
        db.commit()
        db.refresh(cv_doc)

        return cv_doc

    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Failed to create document: {str(e)}")


@router.put("/documents/{doc_id}", response_model=MarkdownCV)
def update_cv_document(
    doc_id: int,
    cv_data: CVMarkdownUpdate,
    db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):
    """CV 문서 수정"""
    cv_doc = db.query(MarkdownCV).filter(MarkdownCV.id == doc_id).first()
    if not cv_doc:
        raise HTTPException(status_code=404, detail="Document not found")

    try:
        # 수정된 필드만 업데이트
        if cv_data.title is not None:
            cv_doc.title = cv_data.title
        if cv_data.content is not None:
            cv_doc.content = cv_data.content
            cv_doc.version += 1  # 내용이 변경되면 버전 증가
        if cv_data.description is not None:
            cv_doc.description = cv_data.description

        cv_doc.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(cv_doc)

        return cv_doc

    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Failed to update document: {str(e)}")


@router.post("/documents/{doc_id}/set-active")
def set_active_cv_document(doc_id: int, db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):
    """CV 문서를 활성화 (다른 모든 문서는 비활성화)"""
    try:
        # 모든 문서를 비활성화
        db.query(MarkdownCV).update({MarkdownCV.is_active: False})

        # 선택된 문서만 활성화
        cv_doc = db.query(MarkdownCV).filter(MarkdownCV.id == doc_id).first()
        if not cv_doc:
            raise HTTPException(status_code=404, detail="Document not found")

        cv_doc.is_active = True
        cv_doc.updated_at = datetime.utcnow()
        db.commit()

        return {"message": f"Document '{cv_doc.title}' is now active"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Failed to set active document: {str(e)}")


@router.delete("/documents/{doc_id}")
def delete_cv_document(doc_id: int, db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):
    """CV 문서 삭제"""
    cv_doc = db.query(MarkdownCV).filter(MarkdownCV.id == doc_id).first()
    if not cv_doc:
        raise HTTPException(status_code=404, detail="Document not found")

    try:
        db.delete(cv_doc)
        db.commit()

        return {"message": "Document deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Failed to delete document: {str(e)}")


@router.get("/documents/{doc_id}/export")
def export_cv_markdown(doc_id: int, db: Session = Depends(get_db)):
    """마크다운 파일로 다운로드"""
    cv_doc = db.query(MarkdownCV).filter(MarkdownCV.id == doc_id).first()
    if not cv_doc:
        raise HTTPException(status_code=404, detail="Document not found")

    from fastapi.responses import Response

    filename = f"{cv_doc.title.replace(' ', '_')}.md"

    return Response(
        content=cv_doc.content,
        media_type="text/markdown",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
