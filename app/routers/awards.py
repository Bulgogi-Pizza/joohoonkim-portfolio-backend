from typing import List, Optional, get_args

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import nullslast
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Award, AwardCategory
from ..security.security import require_admin

router = APIRouter(prefix="/api/awards", tags=["awards"])


# table=True 모델은 요청 본문 검증을 건너뛰므로 Literal 타입이 강제되지 않는다
def check_category(category: str) -> None:
    allowed = get_args(AwardCategory)
    if category not in allowed:
        raise HTTPException(status_code=422, detail=f"category must be one of {list(allowed)}")


@router.get("", response_model=List[Award])
def get_awards(
    show_in_cv: Optional[bool] = Query(None),
    category: Optional[AwardCategory] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Award)
    if category is not None:
        query = query.filter(Award.category == category)
    if show_in_cv is not None:
        query = query.filter(Award.show_in_cv == show_in_cv)
        return query.order_by(nullslast(Award.cv_order.asc())).all()
    return query.order_by(nullslast(Award.order_index.desc())).all()


@router.post("", response_model=Award)
def create_award(
    award: Award,
    db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):
    check_category(award.category)
    db.add(award)
    db.flush()
    if award.order_index is None:
        award.order_index = award.id
    db.commit()
    db.refresh(award)
    return award


@router.put("/{award_id}", response_model=Award)
def update_award(
    award_id: int,
    award: Award,
    db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):
    check_category(award.category)
    db_award = db.query(Award).filter(Award.id == award_id).first()
    if not db_award:
        raise HTTPException(status_code=404, detail="Award not found")

    for key, value in award.dict(exclude_unset=True).items():
        setattr(db_award, key, value)

    db.commit()
    db.refresh(db_award)
    return db_award


@router.delete("/{award_id}")
def delete_award(
    award_id: int,
    db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):
    award = db.query(Award).filter(Award.id == award_id).first()
    if not award:
        raise HTTPException(status_code=404, detail="Award not found")

    db.delete(award)
    db.commit()
    return {"message": "Award deleted successfully"}
