

import os
import shutil
from datetime import datetime
from typing import List, Optional

from app.security.security import require_admin
from app.utils.s3 import upload_file_to_s3
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlmodel import Session, select, SQLModel

from ..database import get_db
from ..models import CVProfile, ContactInfo, CVSection, MarkdownCV

router = APIRouter(prefix="/api/cv", tags=["CV"])


# Pydantic 스키마
class ContactInfoCreate(SQLModel):
    label: str
    value: str
    data_type: str = "text"
    order_index: int = 0


class CVSectionCreate(SQLModel):
    title: str
    content: str
    order_index: int = 0


class CVProfileCreate(SQLModel):
    name: str
    title: Optional[str] = None
    bio: Optional[str] = None
    profile_image: Optional[str] = None
    contact_info: List[ContactInfoCreate] = []
    cv_sections: List[CVSectionCreate] = []


class CVProfileResponse(SQLModel):
    id: int
    name: str
    title: Optional[str] = None
    bio: Optional[str] = None
    profile_image: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    contact_info: List[ContactInfo] = []
    cv_sections: List[CVSection] = []


# 활성 CV 프로필 조회 (공개용)
@router.get("/profile", response_model=CVProfileResponse)
async def get_active_cv_profile(session: Session = Depends(get_db)):
    # 활성 프로필 조회
    statement = select(CVProfile).where(CVProfile.is_active == True)
    profile = session.exec(statement).first()

    if not profile:
        raise HTTPException(status_code=404,
                            detail="No active CV profile found")

    # 연락처 정보 조회
    contact_statement = select(ContactInfo).where(
        ContactInfo.profile_id == profile.id
    ).order_by(ContactInfo.order_index)
    contact_info = session.exec(contact_statement).all()

    # CV 섹션 조회
    section_statement = select(CVSection).where(
        CVSection.profile_id == profile.id
    ).order_by(CVSection.order_index)
    cv_sections = session.exec(section_statement).all()

    # 응답 생성
    response = CVProfileResponse(
        id=profile.id,
        name=profile.name,
        title=profile.title,
        bio=profile.bio,
        profile_image=profile.profile_image,
        is_active=profile.is_active,
        created_at=profile.created_at,
        updated_at=profile.updated_at,
        contact_info=list(contact_info),
        cv_sections=list(cv_sections)
    )

    return response


# CV 프로필 생성/업데이트 (관리자용)
@router.post("/profile", response_model=CVProfileResponse)
async def create_or_update_cv_profile(
    profile_data: CVProfileCreate,
    session: Session = Depends(get_db),
    admin: bool = Depends(require_admin)

):
    # 기존 활성 프로필 비활성화
    existing_profiles = session.exec(
        select(CVProfile).where(CVProfile.is_active == True)).all()
    for existing in existing_profiles:
        existing.is_active = False
        session.add(existing)

    # 새 프로필 생성
    new_profile = CVProfile(
        name=profile_data.name,
        title=profile_data.title,
        bio=profile_data.bio,
        profile_image=profile_data.profile_image,
        is_active=True,
        updated_at=datetime.utcnow()
    )
    session.add(new_profile)
    session.commit()
    session.refresh(new_profile)

    # 연락처 정보 추가
    for contact_data in profile_data.contact_info:
        contact = ContactInfo(
            profile_id=new_profile.id,
            label=contact_data.label,
            value=contact_data.value,
            data_type=contact_data.data_type,
            order_index=contact_data.order_index
        )
        session.add(contact)

    # CV 섹션 추가
    for section_data in profile_data.cv_sections:
        section = CVSection(
            profile_id=new_profile.id,
            title=section_data.title,
            content=section_data.content,
            order_index=section_data.order_index
        )
        session.add(section)

    session.commit()

    # 응답을 위해 다시 조회
    return await get_active_cv_profile(session)


# 프로필 이미지 업로드
@router.post("/upload-image")
async def upload_profile_image(file: UploadFile = File(...),
    admin: bool = Depends(require_admin)):
    
    try:
        # Upload to S3 (profiles folder)
        s3_url = await upload_file_to_s3(file, folder="profiles")
        # Return path relative to what frontend expects or full URL
        # Frontend might expect /static/... but with S3 we return full URL
        return {"image_path": s3_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 기존 마크다운 CV와의 호환성 유지
@router.get("/markdown/active")
async def get_active_markdown_cv(session: Session = Depends(get_db)
):
    statement = select(MarkdownCV).where(MarkdownCV.is_active == True).order_by(
        MarkdownCV.version.desc())
    cv = session.exec(statement).first()

    if not cv:
        raise HTTPException(status_code=404,
                            detail="No active markdown CV found")

    return cv


# 마크다운 CV 생성/업데이트
@router.post("/markdown")
async def create_markdown_cv(
    title: str,
    content: str,
    description: Optional[str] = None,
    session: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):
    # 기존 활성 CV 비활성화
    existing_cvs = session.exec(
        select(MarkdownCV).where(MarkdownCV.is_active == True)).all()
    for existing in existing_cvs:
        existing.is_active = False
        session.add(existing)

    # 새 버전 번호 계산
    latest_version = session.exec(
        select(MarkdownCV).order_by(MarkdownCV.version.desc())).first()
    new_version = (latest_version.version + 1) if latest_version else 1

    # 새 CV 생성
    new_cv = MarkdownCV(
        title=title,
        content=content,
        description=description,
        is_active=True,
        version=new_version
    )
    session.add(new_cv)
    session.commit()
    session.refresh(new_cv)

    return new_cv
