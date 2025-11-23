import os
from contextlib import asynccontextmanager

from app import models  # 모든 모델을 import하여 테이블이 생성되도록 함
# 데이터베이스 및 모델 import
from app.database import create_db_and_tables, test_db_connection
# 라우터 import
from app.routers import publications, education, experience, awards, \
    conferences, media, representative_works, research_areas, cv_markdown, cv, \
    research_highlights, cover_arts, auth, sitemap
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

load_dotenv()
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN")
SECRET_KEY = os.getenv("SECRET_KEY")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 시작/종료 시 실행될 작업들"""
    # 시작 시 실행
    print("🚀 애플리케이션 시작 중...")

    # 데이터베이스 연결 테스트
    if test_db_connection():
        # 테이블 생성
        create_db_and_tables()
        print("📊 데이터베이스 테이블 생성/확인 완료")

    yield  # 애플리케이션 실행

    # 종료 시 실행 (필요한 경우)
    print("🛑 애플리케이션 종료 중...")


# FastAPI 앱 생성
app = FastAPI(
    title="JoohoonKim Portfolio API",
    description="Portfolio API for JoohoonKim's academic website",
    version="1.0.0",
    lifespan=lifespan
)

# 쿠키 세션
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    same_site="lax",
    https_only=True,
    session_cookie="admin_sess"
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(publications.router)
app.include_router(awards.router)
app.include_router(conferences.router)
app.include_router(representative_works.router)
app.include_router(research_areas.router)
app.include_router(research_highlights.router)
app.include_router(cover_arts.router)
app.include_router(auth.router)
app.include_router(sitemap.router)

# 정적 파일 서빙
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_root():
    return {"message": "JoohoonKim Portfolio API is running!"}


@app.get("/health")
def health_check():
    """API 상태 확인 엔드포인트"""
    return {
        "status": "healthy",
        "message": "API is running successfully"
    }
