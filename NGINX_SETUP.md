# Nginx 설정 가이드

EC2에서 HTTPS를 통해 백엔드 API에 접근하도록 Nginx 리버스 프록시를 설정합니다.

> **참고**: GitHub Actions 배포 시 자동으로 Nginx가 설정되므로, 이 가이드는 수동 설정이 필요한 경우에만 참고하세요.

## Nginx 설치 (Amazon Linux)

```bash
sudo yum update -y
sudo amazon-linux-extras install -y nginx1
# 또는 Amazon Linux 2023:
# sudo yum install -y nginx

sudo yum install -y certbot python3-certbot-nginx
```

## 백엔드 설정

### /etc/nginx/conf.d/portfolio-backend.conf

> Amazon Linux는 `sites-available/sites-enabled` 대신 `conf.d/` 디렉토리를 사용합니다.

```nginx
server {
    listen 80;
    server_name api.joohoonkim.site;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # 정적 파일
    location /static {
        proxy_pass http://localhost:8000/static;
    }
}
```

## 설정 활성화 (수동 설정 시)

```bash
# Amazon Linux는 conf.d/ 디렉토리의 .conf 파일을 자동으로 로드합니다
# 별도의 심볼릭 링크 불필요

# 설정 테스트
sudo nginx -t

# Nginx 재시작
sudo systemctl restart nginx
```

## SSL 인증서 설정 (Let's Encrypt)

> **참고**: GitHub Actions 배포 시 자동으로 SSL이 설정됩니다.

```bash
# 자동 인증서 발급
sudo certbot --nginx -d api.joohoonkim.site

# 또는 수동 설정
sudo certbot --nginx -d api.joohoonkim.site --non-interactive --agree-tos -m your-email@example.com
```

## 자동 갱신 설정

```bash
# 인증서 자동 갱신 테스트
sudo certbot renew --dry-run

# Cron 작업으로 자동 갱신 (이미 설정되어 있을 수 있음)
sudo crontab -e
# 다음 줄 추가:
0 12 * * * /usr/bin/certbot renew --quiet
```

## DNS 설정

도메인이 EC2 IP를 가리키도록 DNS 레코드를 설정해야 합니다:

```
Type: A
Name: api (또는 @)
Value: 13.209.8.80
TTL: 300
```

예시:
- `api.joohoonkim.site` → `13.209.8.80`

## 방화벽 설정

```bash
# Amazon Linux는 AWS 보안 그룹으로 방화벽을 관리합니다
# AWS 콘솔에서 보안 그룹 인바운드 규칙 설정:
# - SSH (22): 내 IP
# - HTTP (80): 0.0.0.0/0
# - HTTPS (443): 0.0.0.0/0

# (선택사항) firewalld를 사용하는 경우:
# sudo firewall-cmd --permanent --add-service=http
# sudo firewall-cmd --permanent --add-service=https
# sudo firewall-cmd --reload
```

**참고**: Docker Compose에서 포트를 127.0.0.1:8000으로 바인딩했기 때문에 외부에서 직접 8000 포트로 접근할 수 없습니다. Nginx를 통해서만 접근 가능합니다.

## 트러블슈팅

### Nginx 상태 확인
```bash
sudo systemctl status nginx
```

### Nginx 로그 확인
```bash
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### 설정 파일 문법 검사
```bash
sudo nginx -t
```

