# GitHub Actions Secrets 설정 가이드

GitHub Actions 배포를 위해 다음 Secrets를 GitHub 저장소에 설정해야 합니다.

## 설정 방법
1. GitHub 저장소 페이지로 이동
2. Settings → Secrets and variables → Actions
3. "New repository secret" 버튼 클릭
4. 아래 Secrets를 하나씩 추가

## 필수 Secrets 목록

### EC2 접속 정보
- **EC2_PROD_KEY**: EC2 SSH 개인키 (전체 내용)
  ```
  -----BEGIN RSA PRIVATE KEY-----
  [개인키 내용]
  -----END RSA PRIVATE KEY-----
  ```

### 데이터베이스 정보
- **DATABASE_URL**: PostgreSQL 연결 URL
- **DB_NAME**: 데이터베이스 이름
- **DB_USER**: 데이터베이스 사용자명
- **DB_PASSWORD**: 데이터베이스 비밀번호

### 도메인 및 인증 정보
- **CERTBOT_EMAIL**: Let's Encrypt SSL 인증서용 이메일
- **SECRET_KEY**: FastAPI 세션 암호화 키
- **ADMIN_USERNAME**: 관리자 사용자명
- **ADMIN_PASSWORD_HASH**: 관리자 비밀번호 해시

### AWS 정보
- **AWS_ACCESS_KEY**: AWS 액세스 키
- **AWS_SECRET_ACCESS_KEY**: AWS 시크릿 키
- **AWS_REGION**: AWS 리전 (예: ap-northeast-2)

## 환경 설정

### Production 환경 (main 브랜치)
- **EC2 IP**: 13.209.8.80
- **Backend URL**: https://api.joohoonkim.site
- **Frontend**: https://main.d1jx5u7u0ebuxt.amplifyapp.com, https://dev.d1jx5u7u0ebuxt.amplifyapp.com (모두 허용)
- **SSH Key**: EC2_PROD_KEY
- **배포 디렉토리**: /home/ec2-user/portfolio-backend
- **SSH 사용자**: ec2-user (Amazon Linux)

**참고**: 
- FRONTEND_ORIGIN은 쉼표로 구분된 여러 URL을 지원합니다.
- Nginx + Let's Encrypt를 통해 자동으로 HTTPS가 설정됩니다.
- 백엔드 API는 https://api.joohoonkim.site로 접근 가능합니다.

## 배포 방법

### 자동 배포
- `main` 브랜치에 push → EC2에 자동 배포 및 HTTPS 설정

```bash
git add .
git commit -m "Deploy to production"
git push origin main
```

### 수동 실행
1. GitHub 저장소 → Actions 탭
2. "Deploy to EC2" 워크플로우 선택
3. "Run workflow" 버튼 클릭
4. main 브랜치 선택 후 실행

## EC2 서버 사전 설정 필요사항

EC2 인스턴스에 다음 항목들이 설치되어 있어야 합니다:

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

# Docker Compose 설치
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Nginx 설치
sudo amazon-linux-extras install -y nginx1
# 또는 Amazon Linux 2023:
# sudo yum install -y nginx

# Certbot 설치 (HTTPS 지원)
sudo yum install -y certbot python3-certbot-nginx

# Nginx 서비스 시작
sudo systemctl start nginx
sudo systemctl enable nginx

# AWS 보안 그룹 인바운드 규칙 설정 (AWS 콘솔에서):
# - SSH (22): 내 IP
# - HTTP (80): 0.0.0.0/0
# - HTTPS (443): 0.0.0.0/0
```

### DNS 설정 필수!
도메인이 EC2 IP를 가리키도록 DNS A 레코드를 설정해야 합니다:
```
Type: A
Name: api
Value: 13.209.8.80
TTL: 300
```

이렇게 하면 `api.joohoonkim.site`가 EC2를 가리킵니다.

## 보안 주의사항

⚠️ **중요**: `.env` 파일과 SSH 개인키는 절대 Git에 커밋하지 마세요!
- `.env` 파일은 이미 `.gitignore`에 포함되어 있어야 합니다
- SSH 개인키는 GitHub Secrets에만 저장하세요
- 배포 후에는 서버의 `.env` 파일 권한을 600으로 설정하세요
  ```bash
  chmod 600 /home/ubuntu/portfolio-backend-*/\.env.local
  ```

## 트러블슈팅

### 배포 실패 시 확인사항
1. GitHub Secrets가 모두 올바르게 설정되었는지 확인
2. EC2 인스턴스가 실행 중인지 확인
3. EC2 보안 그룹에서 SSH 포트(22), HTTP(80), HTTPS(443)가 열려있는지 확인
4. SSH 키가 올바른 형식인지 확인 (개행 문자 포함)
5. DNS 설정이 올바른지 확인 (`api.joohoonkim.site` → `13.209.8.80`)

### 로그 확인
```bash
# EC2 서버에 접속 후
cd /home/ec2-user/portfolio-backend
docker-compose logs -f

# Nginx 로그
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### 컨테이너 재시작
```bash
cd /home/ec2-user/portfolio-backend
docker-compose restart
```

### SSL 인증서 수동 갱신
```bash
sudo certbot renew
sudo systemctl reload nginx
```

### 컨테이너 상태 확인
```bash
docker-compose ps
docker-compose logs
docker ps
```

### Nginx 상태 확인
```bash
sudo systemctl status nginx
sudo nginx -t  # 설정 파일 테스트
```

