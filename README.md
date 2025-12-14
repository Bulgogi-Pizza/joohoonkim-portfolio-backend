# JoohoonKim Portfolio Backend

FastAPI 기반 포트폴리오 웹사이트 백엔드 API

## 기술 스택

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLModel (SQLAlchemy 기반)
- **Deployment**: Docker, GitHub Actions
- **Cloud**: AWS (S3), EC2

## 로컬 개발 환경 설정

### 1. 저장소 클론
```bash
git clone https://github.com/your-username/joohoonkim-portfolio-backend.git
cd joohoonkim-portfolio-backend
```

### 2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정
```bash
cp .env.local.example .env.local
# .env.local 파일을 열어서 실제 값으로 수정
```

### 5. 애플리케이션 실행
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API 문서: http://localhost:8000/docs

## Docker로 실행

```bash
# 이미지 빌드 및 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 중지
docker-compose down
```

## 배포

이 프로젝트는 GitHub Actions를 통해 자동으로 EC2에 배포됩니다.

- **Production**: `main` 브랜치에 push → EC2에 자동 배포 (HTTPS 지원)
- **Backend URL**: https://api.joohoonkim.site

배포 시 자동으로 설정되는 항목:
- Docker 컨테이너 빌드 및 실행
- Nginx 리버스 프록시 설정
- Let's Encrypt SSL 인증서 발급
- HTTPS 자동 리다이렉트

자세한 배포 설정 방법은 [QUICK_START.md](./QUICK_START.md) 또는 [DEPLOYMENT.md](./DEPLOYMENT.md)를 참고하세요.

## 프로젝트 구조

```
.
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 앱 진입점
│   ├── database.py          # 데이터베이스 연결 설정
│   ├── models.py            # SQLModel 모델 정의
│   ├── routers/             # API 라우터
│   │   ├── auth.py
│   │   ├── publications.py
│   │   └── ...
│   ├── security/            # 보안 관련 모듈
│   └── utils/               # 유틸리티 함수
├── alembic/                 # 데이터베이스 마이그레이션
├── scripts/                 # 데이터 초기화 스크립트
├── static/                  # 정적 파일
├── .env.example             # 환경 변수 템플릿
├── docker-compose.yml       # Docker Compose 설정
├── Dockerfile               # Docker 이미지 정의
└── requirements.txt         # Python 의존성

```

## API 엔드포인트

- `GET /` - API 상태 확인
- `GET /health` - 헬스 체크
- `GET /docs` - Swagger API 문서
- `GET /api/publications` - 논문 목록
- `GET /api/education` - 학력 정보
- `POST /api/auth/login` - 관리자 로그인
- ... (자세한 내용은 `/docs` 참고)

## 데이터베이스 마이그레이션

```bash
# 새 마이그레이션 생성
alembic revision --autogenerate -m "description"

# 마이그레이션 적용
alembic upgrade head

# 마이그레이션 롤백
alembic downgrade -1
```

## 환경 변수

주요 환경 변수는 `.env.example` 파일을 참고하세요.

## 라이선스

MIT License

