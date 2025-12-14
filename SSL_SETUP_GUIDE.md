# 🔐 SSL 인증서 수동 발급 가이드

## 현재 상태 ✅

- ✅ Docker 컨테이너 정상 실행
- ✅ DNS 설정 완료 (`api.joohoonkim.site` → `13.209.8.80`)
- ✅ HTTP로 API 접근 가능
- ❌ SSL 인증서 미발급 (Let's Encrypt 접근 불가)

## SSL 발급 실패 원인

Let's Encrypt가 `http://api.joohoonkim.site/.well-known/acme-challenge/`에 접근할 수 없습니다.

**가능한 원인:**
1. ⚠️  **AWS 보안 그룹에서 포트 80이 차단됨** (가장 가능성 높음)
2. DNS 전파가 완전히 완료되지 않음
3. 방화벽 또는 네트워크 정책

## 🔧 해결 방법

### 1단계: AWS 보안 그룹 설정 확인 (필수!)

1. **AWS 콘솔에 로그인**
   - https://console.aws.amazon.com/ec2/

2. **EC2 인스턴스 확인**
   - EC2 대시보드 → 인스턴스
   - IP `13.209.8.80`인 인스턴스 선택

3. **보안 그룹 확인**
   - 하단 "보안" 탭 → "보안 그룹" 링크 클릭

4. **인바운드 규칙 확인 및 추가**
   
   현재 필요한 규칙:
   
   | 유형 | 프로토콜 | 포트 범위 | 소스 | 설명 |
   |------|----------|-----------|------|------|
   | SSH | TCP | 22 | 내 IP | SSH 접속 |
   | HTTP | TCP | 80 | 0.0.0.0/0, ::/0 | Let's Encrypt 검증 + HTTP 접근 |
   | HTTPS | TCP | 443 | 0.0.0.0/0, ::/0 | HTTPS 접근 |

   **중요:** 
   - HTTP (80) 포트가 **0.0.0.0/0 (모든 IPv4)** 와 **::/0 (모든 IPv6)** 에서 접근 가능해야 합니다
   - "내 IP"로만 설정하면 Let's Encrypt 서버에서 접근할 수 없습니다!

5. **규칙 추가 방법**
   ```
   인바운드 규칙 편집 → 규칙 추가
   
   - 유형: HTTP
   - 포트 범위: 80
   - 소스: 0.0.0.0/0
   - 설명: Allow HTTP for Let's Encrypt
   
   규칙 추가 (IPv6용)
   - 유형: HTTP
   - 포트 범위: 80
   - 소스: ::/0
   - 설명: Allow HTTP for Let's Encrypt (IPv6)
   
   동일하게 HTTPS (443)도 추가
   ```

### 2단계: 보안 그룹 설정 확인

보안 그룹을 수정한 후 외부에서 접근 테스트:

```bash
# 로컬 컴퓨터에서 실행
curl -I http://api.joohoonkim.site

# 결과에 "HTTP/1.1 405 Method Not Allowed" 또는 "HTTP/1.1 200 OK"가 나오면 성공
# 타임아웃이나 연결 거부가 나오면 보안 그룹 재확인 필요
```

### 3단계: EC2 서버에서 SSL 인증서 발급

보안 그룹이 올바르게 설정되었다면:

#### 방법 1: 자동 스크립트 사용 (권장)

```bash
# EC2 서버에 접속
ssh -i joohoonkim-portfolio-backend-main-key.pem ec2-user@13.209.8.80

# 배포 디렉토리로 이동
cd /home/ec2-user/portfolio-backend

# SSL 설정 스크립트 실행 권한 부여
chmod +x scripts/setup-ssl.sh

# 스크립트 실행
sudo ./scripts/setup-ssl.sh
```

스크립트가 자동으로:
- DNS 설정 확인
- Nginx 상태 확인
- Docker 컨테이너 확인
- API 응답 확인
- SSL 인증서 발급

#### 방법 2: 수동 발급

```bash
# EC2 서버에 접속
ssh -i joohoonkim-portfolio-backend-main-key.pem ec2-user@13.209.8.80

# 1. Docker 컨테이너 확인
docker ps
# "portfolio-backend" 컨테이너가 "Up" 상태여야 함

# 2. API 테스트
curl http://localhost:8000/health
# {"status":"healthy","message":"API is running successfully"} 응답 확인

# 3. Nginx 상태 확인
sudo systemctl status nginx
# active (running) 확인

# 4. SSL 인증서 발급
sudo certbot --nginx -d api.joohoonkim.site

# 프롬프트가 나오면:
# - 이메일 확인: Enter
# - 약관 동의: Y
# - Redirect HTTP to HTTPS: 2 (권장)
```

### 4단계: SSL 인증서 발급 성공 확인

```bash
# SSL 인증서 확인
sudo certbot certificates

# HTTPS 테스트
curl https://api.joohoonkim.site/health

# 브라우저에서 접속
https://api.joohoonkim.site/docs
```

## 🚨 트러블슈팅

### 문제 1: "Timeout during connect"
```
Detail: 13.209.8.80: Fetching http://api.joohoonkim.site/.well-known/acme-challenge/xxx: Timeout during connect
```

**원인:** AWS 보안 그룹에서 포트 80이 차단됨

**해결:**
1. AWS 콘솔 → EC2 → 보안 그룹
2. HTTP (80) 포트를 0.0.0.0/0으로 오픈
3. 5분 대기 후 다시 시도

### 문제 2: "Connection refused"
```
curl: (7) Failed to connect to api.joohoonkim.site port 80: Connection refused
```

**원인:** Nginx가 실행되지 않음

**해결:**
```bash
sudo systemctl start nginx
sudo systemctl status nginx
```

### 문제 3: "404 Not Found" on /.well-known/acme-challenge/
```
Detail: Fetching http://api.joohoonkim.site/.well-known/acme-challenge/xxx: 404
```

**원인:** Nginx 설정 문제

**해결:**
```bash
# Nginx 설정 확인
sudo nginx -t

# Nginx 재시작
sudo systemctl restart nginx
```

### 문제 4: 기존 인증서와 충돌
```
Certificate already exists
```

**해결:**
```bash
# 기존 인증서 삭제
sudo certbot delete --cert-name api.joohoonkim.site

# 다시 발급
sudo certbot --nginx -d api.joohoonkim.site
```

## 📊 AWS 보안 그룹 최종 설정 (참고)

```
인바운드 규칙:
┌──────────┬──────────┬───────────┬─────────────┬────────────────────────────┐
│ 유형     │ 프로토콜 │ 포트 범위 │ 소스        │ 설명                       │
├──────────┼──────────┼───────────┼─────────────┼────────────────────────────┤
│ SSH      │ TCP      │ 22        │ 내 IP       │ SSH 접속                   │
│ HTTP     │ TCP      │ 80        │ 0.0.0.0/0   │ Let's Encrypt + HTTP       │
│ HTTP     │ TCP      │ 80        │ ::/0        │ Let's Encrypt + HTTP (IPv6)│
│ HTTPS    │ TCP      │ 443       │ 0.0.0.0/0   │ HTTPS                      │
│ HTTPS    │ TCP      │ 443       │ ::/0        │ HTTPS (IPv6)               │
└──────────┴──────────┴───────────┴─────────────┴────────────────────────────┘
```

## ✅ 성공 후 확인사항

SSL 인증서 발급에 성공하면:

```bash
# 1. HTTPS 접근 테스트
curl https://api.joohoonkim.site/health

# 2. HTTP → HTTPS 리다이렉트 확인
curl -I http://api.joohoonkim.site
# 결과: 301 Moved Permanently
# Location: https://api.joohoonkim.site/

# 3. 브라우저에서 확인
https://api.joohoonkim.site/docs

# 4. SSL 인증서 정보
sudo certbot certificates
```

## 🔄 SSL 인증서 자동 갱신

Let's Encrypt 인증서는 90일마다 갱신해야 합니다.

```bash
# 자동 갱신 테스트
sudo certbot renew --dry-run

# Cron job 확인 (이미 설정되어 있어야 함)
sudo systemctl status certbot.timer

# 수동 갱신 (필요 시)
sudo certbot renew
sudo systemctl reload nginx
```

## 📱 Amplify Frontend 연결

SSL 인증서 발급 후 Amplify에서 백엔드 호출:

```javascript
// Frontend 환경 변수
const API_URL = 'https://api.joohoonkim.site';

// API 호출
fetch(`${API_URL}/api/publications`)
  .then(res => res.json())
  .then(data => console.log(data));
```

## 🎯 다음 단계

SSL 인증서 발급 후:

1. ✅ Amplify Frontend에서 백엔드 URL을 `https://api.joohoonkim.site`로 설정
2. ✅ CORS 설정 확인 (이미 설정됨)
3. ✅ API 테스트
4. ✅ 프로덕션 배포

## 📞 도움이 필요하면

1. AWS 보안 그룹 설정 스크린샷 확인
2. EC2 서버 로그:
   ```bash
   sudo tail -f /var/log/nginx/error.log
   sudo tail -f /var/log/letsencrypt/letsencrypt.log
   ```
3. Docker 로그:
   ```bash
   cd /home/ec2-user/portfolio-backend
   docker-compose logs -f
   ```

