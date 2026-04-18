import os

from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine, SQLModel, Session

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL 환경 변수가 설정되지 않았습니다.")

# SQLModel/SQLAlchemy 엔진 생성
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=1800,   # 30분마다 연결 재활용 (idle 연결 만료 방지)
    pool_size=5,
    max_overflow=10,
)

# 세션 팩토리 생성
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session  # SQLModel의 Session 사용
)


# 테이블 생성 함수
def create_db_and_tables():
    """데이터베이스 테이블을 생성합니다."""
    SQLModel.metadata.create_all(engine)


# 데이터베이스 세션 의존성
def get_db():
    """FastAPI 의존성으로 사용할 데이터베이스 세션을 제공합니다."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 데이터베이스 연결 테스트 함수
def test_db_connection():
    """데이터베이스 연결을 테스트합니다."""
    try:
        with engine.connect() as connection:
            print("✅ 데이터베이스 연결 성공!")
            return True
    except Exception as e:
        print(f"❌ 데이터베이스 연결 실패: {e}")
        return False
