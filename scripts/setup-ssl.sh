#!/bin/bash
# SSL 인증서 수동 발급 스크립트

echo "🔐 SSL 인증서 수동 발급을 시작합니다..."
echo ""

# 색상 정의
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 도메인 설정
DOMAIN="api.joohoonkim.site"
EMAIL="quitendexit@gmail.com"

echo "📋 체크리스트를 확인합니다..."
echo ""

# 1. DNS 확인
echo "1️⃣  DNS 설정 확인 중..."
DNS_IP=$(nslookup $DOMAIN | grep -A1 "Name:" | tail -1 | awk '{print $2}')
if [ "$DNS_IP" == "13.209.8.80" ]; then
    echo -e "${GREEN}✅ DNS 설정 정상: $DOMAIN → $DNS_IP${NC}"
else
    echo -e "${RED}❌ DNS 설정 오류: $DOMAIN → $DNS_IP (예상: 13.209.8.80)${NC}"
    exit 1
fi
echo ""

# 2. Nginx 상태 확인
echo "2️⃣  Nginx 상태 확인 중..."
if systemctl is-active --quiet nginx; then
    echo -e "${GREEN}✅ Nginx 실행 중${NC}"
else
    echo -e "${RED}❌ Nginx가 실행되지 않음${NC}"
    echo "   sudo systemctl start nginx 를 실행하세요"
    exit 1
fi
echo ""

# 3. Docker 컨테이너 확인
echo "3️⃣  Docker 컨테이너 상태 확인 중..."
if docker ps | grep -q "portfolio-backend"; then
    echo -e "${GREEN}✅ Docker 컨테이너 실행 중${NC}"
else
    echo -e "${RED}❌ Docker 컨테이너가 실행되지 않음${NC}"
    echo "   cd /home/ec2-user/portfolio-backend && docker-compose up -d"
    exit 1
fi
echo ""

# 4. 로컬 API 테스트
echo "4️⃣  로컬 API 테스트 중..."
if curl -sf http://localhost:8000/health > /dev/null; then
    echo -e "${GREEN}✅ API 정상 응답${NC}"
else
    echo -e "${RED}❌ API 응답 없음${NC}"
    exit 1
fi
echo ""

# 5. 외부 HTTP 접근 테스트
echo "5️⃣  외부 HTTP 접근 테스트 중..."
if curl -sf http://$DOMAIN/health > /dev/null; then
    echo -e "${GREEN}✅ 외부에서 HTTP 접근 가능${NC}"
else
    echo -e "${YELLOW}⚠️  외부에서 HTTP 접근 불가${NC}"
    echo "   AWS 보안 그룹에서 포트 80(HTTP)를 0.0.0.0/0으로 열어주세요"
    echo ""
    echo "   AWS 콘솔 → EC2 → 보안 그룹 → 인바운드 규칙 편집:"
    echo "   - 유형: HTTP"
    echo "   - 포트: 80"
    echo "   - 소스: 0.0.0.0/0"
    echo ""
    read -p "보안 그룹을 수정했으면 엔터를 눌러 계속하세요..."
fi
echo ""

# 6. SSL 인증서 발급
echo "6️⃣  SSL 인증서 발급 중..."
echo ""

# 기존 인증서 확인
if [ -f "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" ]; then
    echo -e "${YELLOW}⚠️  기존 SSL 인증서가 존재합니다${NC}"
    read -p "기존 인증서를 갱신하시겠습니까? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "SSL 인증서 발급을 취소했습니다."
        exit 0
    fi
    sudo certbot renew --nginx
else
    # 새 인증서 발급
    sudo certbot --nginx -d $DOMAIN --non-interactive --agree-tos -m $EMAIL
fi

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ SSL 인증서 발급 성공!${NC}"
    echo ""
    echo "🎉 배포 완료!"
    echo ""
    echo "📍 접근 URL:"
    echo "   - HTTPS: https://$DOMAIN"
    echo "   - Docs:  https://$DOMAIN/docs"
    echo ""
    echo "🔍 테스트:"
    echo "   curl https://$DOMAIN/health"
    echo ""
else
    echo ""
    echo -e "${RED}❌ SSL 인증서 발급 실패${NC}"
    echo ""
    echo "문제 해결 방법:"
    echo "1. AWS 보안 그룹에서 포트 80, 443이 열려있는지 확인"
    echo "2. DNS 전파 대기 (최대 24시간)"
    echo "3. Nginx 로그 확인: sudo tail -f /var/log/nginx/error.log"
    echo "4. Certbot 로그 확인: sudo tail -f /var/log/letsencrypt/letsencrypt.log"
    echo ""
    exit 1
fi

