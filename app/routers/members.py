from datetime import datetime
from typing import List, Optional, get_args

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy import nullslast
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Member, MemberCategory
from ..security.security import require_admin
from ..utils.s3 import upload_file_to_s3

router = APIRouter(prefix="/api/members", tags=["members"])


# table=True 모델은 요청 본문 검증을 건너뛰므로 Literal 타입이 강제되지 않는다
def check_category(category: str) -> None:
    allowed = get_args(MemberCategory)
    if category not in allowed:
        raise HTTPException(status_code=422, detail=f"category must be one of {list(allowed)}")


@router.get("", response_model=List[Member])
def get_members(
    category: Optional[MemberCategory] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Member)
    if category is not None:
        query = query.filter(Member.category == category)
    return query.order_by(nullslast(Member.order_index.desc())).all()


@router.post("", response_model=Member)
def create_member(
    member: Member,
    db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):
    check_category(member.category)
    db.add(member)
    db.flush()
    if member.order_index is None:
        member.order_index = member.id
    db.commit()
    db.refresh(member)
    return member


@router.put("/{member_id}", response_model=Member)
def update_member(
    member_id: int,
    member: Member,
    db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):
    check_category(member.category)
    db_member = db.query(Member).filter(Member.id == member_id).first()
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")

    for key, value in member.dict(exclude_unset=True).items():
        if key not in ["id", "created_at"]:
            setattr(db_member, key, value)
    db_member.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(db_member)
    return db_member


@router.delete("/{member_id}")
def delete_member(
    member_id: int,
    db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    db.delete(member)
    db.commit()
    return {"message": "Member deleted successfully"}


@router.post("/upload-image")
async def upload_member_image(
    file: UploadFile = File(...),
    admin: bool = Depends(require_admin)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        s3_url = await upload_file_to_s3(file, folder="members")
        return {"image_path": s3_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
