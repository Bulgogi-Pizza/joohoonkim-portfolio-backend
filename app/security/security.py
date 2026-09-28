import os
import secrets
from typing import Optional

from fastapi import HTTPException, Request, Security
from fastapi.security import APIKeyHeader
from passlib.context import CryptContext

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Swagger UI의 Authorize 버튼에 X-API-Key 입력란이 노출된다
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def verify_admin_credentials(username: str, password: str) -> bool:
    admin_user = os.getenv("ADMIN_USERNAME", "admin")
    admin_hash = os.getenv("ADMIN_PASSWORD_HASH", "")
    if not admin_hash or not secrets.compare_digest(username.encode(), admin_user.encode()):
        return False
    return pwd.verify(password, admin_hash)


def is_valid_api_key(api_key: Optional[str]) -> bool:
    # API_KEYS는 쉼표로 구분된 여러 키를 허용 (키 교체 시 신/구 키 병행 가능)
    if not api_key:
        return False
    keys = [k.strip() for k in os.getenv("API_KEYS", "").split(",") if k.strip()]
    return any(secrets.compare_digest(api_key.encode(), k.encode()) for k in keys)


def is_admin(request: Request, api_key: Optional[str] = None) -> bool:
    return bool(request.session.get("admin", False)) or is_valid_api_key(api_key)


def require_admin(request: Request,
    api_key: Optional[str] = Security(api_key_header)):
    """세션 쿠키(관리자 로그인) 또는 X-API-Key 헤더로 인증"""
    if not is_admin(request, api_key):
        raise HTTPException(status_code=401, detail="Admin required")
    return True
