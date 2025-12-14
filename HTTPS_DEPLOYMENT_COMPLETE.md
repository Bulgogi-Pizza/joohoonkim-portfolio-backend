# 🎉 HTTPS 배포 설정 완료!

## 변경 사항 요약

### ✅ 주요 변경사항

1. **단일 브랜치 배포**: `main` 브랜치만 사용 (dev 브랜치 제거)
2. **HTTPS 지원**: Nginx + Let's Encrypt를 통한 자동 SSL 인증서 발급
3. **도메인 접근**: https://api.joohoonkim.site 로 백엔드 API 접근
4. **보안 강화**: Docker 포트를 localhost에만 바인딩하여 Nginx를 통해서만 접근 가능

### 📝 수정된 파일들

1. **`.github/workflows/deploy.yml`**
   - main 브랜치만 트리거
   - EC2 IP를 13.209.8.80으로 고정
   - Nginx 자동 설정 추가
   - Let's Encrypt SSL 자동 발급 추가

2. **`docker-compose.yml`**
   - 포트를 `127.0.0.1:8000:8000`으로 변경 (외부 직접 접근 차단)

3. **문서 파일들**
   - `QUICK_START.md` - HTTPS 배포 가이드로 업데이트
   - `DEPLOYMENT.md` - 단일 환경 설정으로 업데이트
   - `NGINX_SETUP.md` - 자동 설정 가이드로 업데이트
   - `README.md` - HTTPS 배포 정보 추가

## 🚀 배포 프로세스

### 자동화된 배포 단계:

```
Git Push (main 브랜치)
    ↓
GitHub Actions 트리거
    ↓
EC2 접속 (SSH)
    ↓
코드 업데이트 (Git Pull)
    ↓
환경 변수 설정 (.env)
    ↓
Nginx 설정 파일 생성
    ↓
Docker Compose 빌드 & 실행
    ↓
SSL 인증서 발급 (첫 배포 시)
    ↓
배포 완료! ✅
```

## 📋 배포 전 체크리스트

### 1. GitHub Secrets 설정 ✅
- [ ] `EC2_PROD_KEY` - SSH 개인키
- [ ] `DATABASE_URL` - PostgreSQL 연결 URL
- [ ] `DB_NAME`, `DB_USER`, `DB_PASSWORD`
- [ ] `CERTBOT_EMAIL` - SSL 인증서용 이메일
- [ ] `SECRET_KEY` - FastAPI 세션 키
- [ ] `ADMIN_USERNAME`, `ADMIN_PASSWORD_HASH`
- [ ] `AWS_ACCESS_KEY`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`

### 2. DNS 설정 ✅ (중요!)
```
Type: A
Name: api
Value: 13.209.8.80
TTL: 300
```

DNS 전파 확인:
```bash
nslookup api.joohoonkim.site
```

### 3. EC2 서버 준비 ✅
```bash
# Docker 설치
sudo yum update -y
sudo yum install -y docker git

# Docker 시작
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ec2-user

# Docker Compose 설치
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Nginx 및 Certbot 설치
sudo amazon-linux-extras install -y nginx1
sudo yum install -y certbot python3-certbot-nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# AWS 보안 그룹에서 방화벽 설정
# - SSH (22): 내 IP
# - HTTP (80): 0.0.0.0/0
# - HTTPS (443): 0.0.0.0/0
```

### 4. EC2 보안 그룹 설정 ✅
- [ ] SSH (22) - 내 IP에서만 접근
- [ ] HTTP (80) - 모든 곳에서 접근
- [ ] HTTPS (443) - 모든 곳에서 접근

## 🎯 배포 방법

### 코드 배포
```bash
git add .
git commit -m "Deploy to production"
git push origin main
```

### GitHub Actions에서 진행 상황 확인
1. GitHub 저장소 → Actions 탭
2. 실행 중인 워크플로우 클릭
3. 각 단계별 로그 확인

## ✅ 배포 확인

### 1. DNS 확인
```bash
nslookup api.joohoonkim.site
# 결과: 13.209.8.80
```

### 2. HTTP → HTTPS 리다이렉트 확인
```bash
curl -I http://api.joohoonkim.site
# 결과: 301 Moved Permanently
# Location: https://api.joohoonkim.site/
```

### 3. HTTPS API 접근
```bash
curl https://api.joohoonkim.site/health
# 결과: {"status":"healthy","message":"API is running successfully"}
```

### 4. Swagger 문서 확인
브라우저에서: https://api.joohoonkim.site/docs

## 🔧 트러블슈팅

### SSL 인증서 발급 실패
**원인**: DNS가 아직 전파되지 않음

**해결책**:
1. DNS 전파 확인: `nslookup api.joohoonkim.site`
2. DNS 전파 대기 (최대 24시간, 보통 5-30분)
3. 수동으로 SSL 재발급:
   ```bash
   sudo certbot --nginx -d api.joohoonkim.site
   ```

### Docker 컨테이너가 시작되지 않음
```bash
cd /home/ubuntu/portfolio-backend
docker compose logs -f
# 에러 로그 확인 후 환경 변수 또는 코드 수정
```

### Nginx 502 Bad Gateway
**원인**: Docker 컨테이너가 실행되지 않음

**해결책**:
```bash
docker compose ps  # 컨테이너 상태 확인
docker compose up -d  # 컨테이너 재시작
```

### CORS 에러
**원인**: Frontend URL이 CORS에 허용되지 않음

**해결책**: GitHub Actions 워크플로우의 `FRONTEND_ORIGIN`에 URL 추가됨 (이미 설정됨)

## 🌐 접근 URL

### Backend API
- **Production**: https://api.joohoonkim.site
- **Swagger Docs**: https://api.joohoonkim.site/docs
- **Health Check**: https://api.joohoonkim.site/health

### Frontend (CORS 허용됨)
- **Main**: https://main.d1jx5u7u0ebuxt.amplifyapp.com
- **Dev**: https://dev.d1jx5u7u0ebuxt.amplifyapp.com

## 📚 추가 문서

- **빠른 시작**: [QUICK_START.md](./QUICK_START.md)
- **상세 배포 가이드**: [DEPLOYMENT.md](./DEPLOYMENT.md)
- **Nginx 설정**: [NGINX_SETUP.md](./NGINX_SETUP.md)
- **프로젝트 README**: [README.md](./README.md)

## 🎊 완료!

이제 `main` 브랜치에 push하면 자동으로 HTTPS가 설정된 프로덕션 환경에 배포됩니다!

Amplify Frontend에서 다음과 같이 백엔드 API를 호출할 수 있습니다:
```javascript
const API_URL = 'https://api.joohoonkim.site';

// 예시
fetch(`${API_URL}/api/publications`)
  .then(res => res.json())
  .then(data => console.log(data));
```

## 🔒 보안 참고사항

1. ✅ HTTPS로 모든 통신 암호화
2. ✅ Docker 컨테이너는 localhost에만 바인딩
3. ✅ Nginx를 통해서만 API 접근 가능
4. ✅ 민감한 정보는 GitHub Secrets로 관리
5. ✅ SSH 키는 Git에 커밋되지 않음
6. ✅ CORS는 특정 Frontend URL만 허용

