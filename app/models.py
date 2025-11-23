from datetime import datetime
from typing import Optional

from pydantic import ConfigDict
from sqlmodel import SQLModel, Field


class Education(SQLModel, table=True):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: Optional[int] = Field(default=None, primary_key=True)
    degree: str
    institution: str
    location: str
    start_year: str
    end_year: str
    advisor: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Experience(SQLModel, table=True):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: Optional[int] = Field(default=None, primary_key=True)
    position: str
    organization: str
    location: str
    start_year: str
    end_year: str
    description: Optional[str] = None
    host_advisor: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Award(SQLModel, table=True):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    organization: str
    location: str
    year: str
    rank: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Publication(SQLModel, table=True):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: Optional[int] = Field(default=None, primary_key=True)
    number: int  # 논문 번호 (내림차순)
    title: str
    authors: str  # 전체 저자 리스트
    journal: str
    volume: Optional[str] = None
    pages: Optional[str] = None
    year: str
    month: Optional[str] = None
    doi: Optional[str] = None
    arxiv: Optional[str] = None

    # 기여도 분류
    is_first_author: bool = Field(default=False)
    is_corresponding_author: bool = Field(default=False)
    is_equal_contribution: bool = Field(default=False)
    contribution_type: str = Field(
        default="co-author")  # first-author, corresponding, co-author

    # 상태
    status: str = Field(
        default="published")  # published, under-submission, in-press, in-review

    # 추가 정보
    impact_factor: Optional[float] = None
    featured_info: Optional[str] = None  # Cover article, News & Views 등

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Conference(SQLModel, table=True):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    conference_name: str
    location: str
    date: str
    presentation_type: str
    award: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Media(SQLModel, table=True):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    source: str
    date: str
    url: Optional[str] = None
    description: Optional[str] = None
    category: str = Field(default="news")
    image_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class RepresentativeWork(SQLModel, table=True):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    journal: str
    volume: Optional[str] = None
    is_in_revision: bool = Field(default=False)
    pages: Optional[str] = None  # 예: "474-481"
    year: Optional[str] = None  # 예: "2023"
    image_path: str  # 이미지 파일 경로
    order_index: int = Field(default=0)  # 슬라이드 순서
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class GalleryImage(SQLModel, table=True):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    image_path: str
    alt_text: Optional[str] = None
    category: str  # manufacturing, design, applications
    order_index: int = Field(default=0)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ResearchArea(SQLModel, table=True):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    slug: str = Field(unique=True)  # URL용 (design, manufacturing, applications)
    description: str
    icon_path: Optional[str] = None
    order_index: int = Field(default=0)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class MarkdownCV(SQLModel, table=True):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str  # 마크다운 텍스트
    description: Optional[str] = None
    is_active: bool = Field(default=False)
    version: int = Field(default=1)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class CVProfile(SQLModel, table=True):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    title: Optional[str] = None  # "Director of the Center for..."
    bio: Optional[str] = None
    profile_image: Optional[str] = None
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ContactInfo(SQLModel, table=True):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: Optional[int] = Field(default=None, primary_key=True)
    profile_id: int = Field(foreign_key="cvprofile.id")
    label: str  # "E-mail", "Office", "Phone" 등
    value: str  # 실제 값
    data_type: str = Field(default="text")  # "email", "phone", "link", "text"
    order_index: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class CVSection(SQLModel, table=True):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: Optional[int] = Field(default=None, primary_key=True)
    profile_id: int = Field(foreign_key="cvprofile.id")
    title: str  # "Biography", "Education" 등
    content: str
    order_index: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ResearchHighlight(SQLModel, table=True):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: Optional[int] = Field(default=None, primary_key=True)
    image_path: str
    link: Optional[str] = None
    description: Optional[str] = None
    alt_text: Optional[str] = None
    order_index: int = Field(default=0)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class CoverArt(SQLModel, table=True):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: Optional[int] = Field(default=None, primary_key=True)
    image_path: str
    link: Optional[str] = None
    journal: str
    volume: Optional[str] = None
    year: Optional[str] = None
    description: Optional[str] = None
    alt_text: Optional[str] = None
    order_index: int = Field(default=0)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
