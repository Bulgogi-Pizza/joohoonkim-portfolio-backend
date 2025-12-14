# 🔧 Docker 및 SSL 트러블슈팅 가이드

## 현재 발생한 문제들

### 1. ❌ Docker Buildx 버전 문제
```
compose build requires buildx 0.17 or later
```

**해결 방법:**
- `DOCKER_BUILDKIT=0` 환경 변수로 레거시 빌더 사용
- GitHub Actions 워크플로우에 이미 적용됨

### 2. ❌ SSL 인증서 발급 실패
```
Certbot failed to authenticate some domains
Detail: Timeout during connect (likely firewall problem)
```

**원인:**
1. DNS가 아직 전파되지 않음
2. AWS 보안 그룹에서 포트 80/443이 열려있지 않음
3. Docker 컨테이너가 시작되기 전에 SSL을 발급하려고 함

## 🔍 진단 체크리스트

### 1. DNS 확인
```bash
nslookup api.joohoonkim.site
# 결과가 13.209.8.80이어야 함

dig api.joohoonkim.site
# ANSWER SECTION에 13.209.8.80이 있어야 함
```

### 2. AWS 보안 그룹 확인
EC2 인스턴스의 보안 그룹 인바운드 규칙에 다음이 있어야 함:

| 유형 | 프로토콜 | 포트 범위 | 소스 |
|------|----------|-----------|------|
| SSH | TCP | 22 | 내 IP |
| HTTP | TCP | 80 | 0.0.0.0/0 |
| HTTPS | TCP | 443 | 0.0.0.0/0 |

### 3. Docker 컨테이너 상태 확인
```bash
ssh -i joohoonkim-portfolio-backend-main-key.pem ec2-user@13.209.8.80

# 컨테이너 확인
docker ps

# 로그 확인
cd /home/ec2-user/portfolio-backend
docker-compose logs

# API 테스트
curl http://localhost:8000/health
```

## 🛠️ 해결 방법

### 방법 1: DNS 전파 대기 후 수동 SSL 발급

1. **DNS 전파 확인** (5-30분 소요)
   ```bash
   nslookup api.joohoonkim.site
   ```

2. **AWS 보안 그룹 확인**
   - AWS 콘솔 → EC2 → 보안 그룹
   - HTTP(80), HTTPS(443) 포트가 0.0.0.0/0에서 접근 가능한지 확인

3. **Docker 컨테이너 확인**
   ```bash
   ssh -i joohoonkim-portfolio-backend-main-key.pem ec2-user@13.209.8.80
   cd /home/ec2-user/portfolio-backend
   
   # 컨테이너 재시작
   docker-compose down
   docker-compose up -d
   
   # 로그 확인
   docker-compose logs -f
   ```

4. **수동으로 SSL 인증서 발급**
   ```bash
   # DNS가 전파되고 Docker가 실행 중일 때
   sudo certbot --nginx -d api.joohoonkim.site
   ```

### 방법 2: 임시로 HTTP로 테스트

SSL 없이 먼저 HTTP로 작동하는지 확인:

```bash
# 브라우저에서
http://13.209.8.80:8000/health
http://13.209.8.80:8000/docs

# 또는 curl로
curl http://13.209.8.80:8000/health
```

**참고:** docker-compose.yml에서 포트를 `127.0.0.1:8000:8000`에서 `8000:8000`으로 임시 변경해야 외부 접근 가능

### 방법 3: 로컬에서 테스트

```bash
# EC2 서버에서
cd /home/ec2-user/portfolio-backend

# 환경 변수 확인
cat .env

# Docker 재빌드
DOCKER_BUILDKIT=0 docker-compose build --no-cache
docker-compose up -d

# 로컬 API 테스트
curl http://localhost:8000/health
```

## 📝 현재 적용된 수정사항

1. ✅ `DOCKER_BUILDKIT=0`로 레거시 빌더 사용
2. ✅ `--no-cache` 플래그로 깨끗한 빌드
3. ✅ docker-compose.yml에서 `version` 필드 제거
4. ✅ healthcheck를 Python 기반으로 변경 (curl 불필요)
5. ✅ SSL 발급 전 컨테이너 헬스체크 대기
6. ✅ SSL 발급 실패 시 에러 대신 경고 표시

## 🚀 다음 배포 시도

```bash
git add .
git commit -m "fix: improve Docker build and SSL certificate process"
git push origin main
```

배포 후 GitHub Actions 로그에서 다음을 확인:
- ✅ Docker 이미지 빌드 성공
- ✅ 컨테이너 시작 성공
- ✅ `curl http://localhost:8000/health` 성공
- ⚠️  SSL 발급은 실패할 수 있음 (DNS/방화벽 문제)

## 🔐 SSL 인증서 수동 발급 (배포 후)

DNS와 방화벽이 준비되면:

```bash
ssh -i joohoonkim-portfolio-backend-main-key.pem ec2-user@13.209.8.80

# SSL 인증서 발급
sudo certbot --nginx -d api.joohoonkim.site

# Nginx 재시작
sudo systemctl reload nginx
```

## 📊 성공 확인

모든 것이 정상 작동하면:

```bash
# HTTPS 테스트
curl https://api.joohoonkim.site/health

# 브라우저에서
https://api.joohoonkim.site/docs
```

## ⚠️ 주의사항

1. **DNS 설정이 가장 중요합니다**
   - `api.joohoonkim.site` → `13.209.8.80` A 레코드
   - 전파 시간: 5분 ~ 24시간

2. **AWS 보안 그룹 필수 포트**
   - 80 (HTTP)
   - 443 (HTTPS)
   - 22 (SSH)

3. **Docker 컨테이너가 먼저 실행되어야 SSL 발급 가능**
   - Nginx가 80 포트를 리스닝해야 Let's Encrypt 검증 가능

4. **첫 배포 시 SSL은 실패할 수 있음**
   - 정상입니다! HTTP로 먼저 확인 후 수동으로 SSL 발급

