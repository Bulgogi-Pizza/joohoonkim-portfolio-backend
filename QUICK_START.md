# 빠른 시작 가이드 (Quick Start)

## 🚀 1단계: GitHub Secrets 설정

GitHub 저장소에서 Settings → Secrets and variables → Actions로 이동하여 다음 Secrets를 추가하세요:

### 필수 Secrets

```plaintext
EC2_PROD_KEY=<joohoonkim-portfolio-backend-main-key.pem 파일 내용>

DATABASE_URL=<PostgreSQL 연결 URL>
DB_NAME=<데이터베이스 이름>
DB_USER=<DB 사용자명>
DB_PASSWORD=<DB 비밀번호>

CERTBOT_EMAIL=<이메일 주소>
SECRET_KEY=<랜덤 문자열>
ADMIN_USERNAME=<관리자 ID>
ADMIN_PASSWORD_HASH=<bcrypt 해시>

AWS_ACCESS_KEY=<AWS 액세스 키>
AWS_SECRET_ACCESS_KEY=<AWS 시크릿 키>
AWS_REGION=ap-northeast-2
```

### SSH 키 파일 읽기
```bash
cat joohoonkim-portfolio-backend-main-key.pem
```
전체 내용을 복사하여 `EC2_PROD_KEY`에 붙여넣기

## 🌐 2단계: DNS 설정 (중요!)

도메인 제공업체에서 DNS A 레코드를 추가하세요:

```
Type: A
Name: api
Value: 13.209.8.80
TTL: 300
```

결과: `api.joohoonkim.site` → `13.209.8.80`

DNS 전파 확인:
```bash
nslookup api.joohoonkim.site
# 또는
dig api.joohoonkim.site
```

## 🖥️ 3단계: EC2 서버 준비

EC2 인스턴스(13.209.8.80)에 SSH로 접속하여 다음 명령어를 실행하세요:

```bash
# 시스템 업데이트
sudo yum update -y

# Docker 설치
sudo yum install -y docker git

# Docker 서비스 시작
sudo systemctl start docker
sudo systemctl enable docker

# ec2-user를 docker 그룹에 추가
sudo usermod -aG docker ec2-user

# Docker Compose 설치 (최신 버전)
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Nginx 설치
sudo amazon-linux-extras install -y nginx1
# 또는 Amazon Linux 2023의 경우:
# sudo yum install -y nginx

# Certbot 설치 (HTTPS 지원)
sudo yum install -y certbot python3-certbot-nginx

# Nginx 서비스 시작
sudo systemctl start nginx
sudo systemctl enable nginx

# 로그아웃 후 재로그인 또는
newgrp docker

# 방화벽 설정은 AWS 보안 그룹에서 관리
# AWS 콘솔에서 보안 그룹 인바운드 규칙 설정:
# - SSH (22): 내 IP
# - HTTP (80): 0.0.0.0/0
# - HTTPS (443): 0.0.0.0/0
```

## 📦 4단계: 배포

### 자동 배포
```bash
# Production 배포
git checkout main
git add .
git commit -m "Deploy to production"
git push origin main
```

배포가 완료되면 자동으로:
1. Docker 컨테이너 빌드 및 실행
2. Nginx 리버스 프록시 설정
3. Let's Encrypt SSL 인증서 발급
4. HTTPS 자동 설정

### 수동 배포 (GitHub Actions 재실행)
1. GitHub 저장소 → Actions 탭
2. "Deploy to EC2" 워크플로우 선택
3. "Run workflow" 버튼 클릭
4. main 브랜치 선택 후 실행

## ✅ 5단계: 배포 확인

### API 상태 확인
```bash
# HTTPS로 접근 (DNS 전파 후)
curl https://api.joohoonkim.site/health

# 또는 브라우저에서
https://api.joohoonkim.site/docs
```

### Swagger 문서 접근
- **API 문서**: https://api.joohoonkim.site/docs
- **Health Check**: https://api.joohoonkim.site/health

## 🔧 트러블슈팅

### EC2에서 로그 확인
```bash
# EC2 서버 접속 (Amazon Linux는 ec2-user 사용)
ssh -i joohoonkim-portfolio-backend-main-key.pem ec2-user@13.209.8.80

# 배포 디렉토리로 이동
cd /home/ec2-user/portfolio-backend

# Docker 로그
docker compose logs -f

# Nginx 로그
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### DNS 전파 확인
```bash
# DNS 설정 확인
nslookup api.joohoonkim.site

# 예상 결과:
# Server: ...
# Address: ...
# 
# Non-authoritative answer:
# Name: api.joohoonkim.site
# Address: 13.209.8.80
```

### SSL 인증서 확인
```bash
# 인증서 상태 확인
sudo certbot certificates

# 수동 갱신
sudo certbot renew
sudo systemctl reload nginx
```

### 컨테이너 재시작
```bash
cd /home/ec2-user/portfolio-backend
docker compose restart
```

### 완전히 재배포
```bash
cd /home/ec2-user/portfolio-backend
docker compose down
docker compose up -d --build
```

### Docker 상태 확인
```bash
docker compose ps
docker ps
docker images
```

### Nginx 상태 확인
```bash
sudo systemctl status nginx
sudo nginx -t  # 설정 파일 테스트
```

## 📝 주의사항

1. ⚠️ `.env` 파일은 Git에 커밋하지 마세요 (이미 .gitignore에 포함됨)
2. 🔐 SSH 키는 GitHub Secrets에만 저장하세요
3. 🌐 DNS 설정이 필수입니다 (`api.joohoonkim.site` → `13.209.8.80`)
4. 🔒 SSL 인증서는 자동으로 발급되지만 DNS가 먼저 설정되어야 합니다
5. 🐳 EC2 서버에 Docker와 Nginx가 설치되어 있어야 합니다
6. 🔑 EC2 보안 그룹에서 포트 22(SSH), 80(HTTP), 443(HTTPS)이 열려있어야 합니다

## 🎯 환경 정보

### Production 환경
- **EC2 IP**: 13.209.8.80
- **Backend URL**: https://api.joohoonkim.site
- **Frontend (Main)**: https://main.d1jx5u7u0ebuxt.amplifyapp.com
- **Frontend (Dev)**: https://dev.d1jx5u7u0ebuxt.amplifyapp.com
- **배포 디렉토리**: /home/ec2-user/portfolio-backend
- **프로토콜**: HTTPS (Let's Encrypt SSL)

두 Frontend URL 모두 CORS에서 허용되므로 상호 테스트가 가능합니다.

## 📚 추가 문서

- [DEPLOYMENT.md](./DEPLOYMENT.md) - 상세 배포 가이드
- [NGINX_SETUP.md](./NGINX_SETUP.md) - Nginx 리버스 프록시 설정
- [README.md](./README.md) - 프로젝트 전체 문서

## 🆘 도움이 필요하신가요?

GitHub Actions 워크플로우 실행 로그를 확인하세요:
1. GitHub 저장소 → Actions 탭
2. 실패한 워크플로우 클릭
3. 각 단계의 로그 확인

