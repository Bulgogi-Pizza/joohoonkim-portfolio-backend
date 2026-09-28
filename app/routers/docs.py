# app/routers/docs.py
# /docs, /redoc, /openapi.json 을 관리자 로그인 뒤로 숨긴다.
# 로그인은 관리자 페이지와 같은 세션(admin_sess)을 쓰므로, 한쪽에서 로그인하면 양쪽 모두 접근 가능하다.
from datetime import timedelta
from html import escape
from typing import Optional

from app.security.security import api_key_header, is_admin, \
    verify_admin_credentials
from fastapi import APIRouter, Form, Request, Security
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

router = APIRouter(include_in_schema=False)

# 로그인 후 이동 가능한 경로 (open redirect 방지)
ALLOWED_NEXT = {"/docs", "/redoc"}

LOGIN_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>API Docs Login</title>
  <style>
    body {{ font-family: system-ui, sans-serif; background: #f5f5f5; display: flex;
           align-items: center; justify-content: center; min-height: 100vh; margin: 0; }}
    form {{ background: #fff; padding: 32px; border-radius: 8px; width: 100%; max-width: 320px;
           box-shadow: 0 2px 8px rgba(0,0,0,.08); }}
    h1 {{ font-size: 18px; margin: 0 0 20px; }}
    label {{ display: block; font-size: 13px; margin-bottom: 4px; color: #444; }}
    input {{ width: 100%; box-sizing: border-box; padding: 8px 10px; margin-bottom: 14px;
            border: 1px solid #ccc; border-radius: 4px; font-size: 14px; }}
    button {{ width: 100%; padding: 10px; border: 0; border-radius: 4px; background: #111;
             color: #fff; font-size: 14px; cursor: pointer; }}
    .error {{ color: #c62828; font-size: 13px; margin: 0 0 14px; }}
  </style>
</head>
<body>
  <form method="post" action="/docs/login">
    <h1>API Docs Login</h1>
    {error}
    <input type="hidden" name="next" value="{next}">
    <label for="username">Username</label>
    <input id="username" name="username" autocomplete="username" required autofocus>
    <label for="password">Password</label>
    <input id="password" name="password" type="password" autocomplete="current-password" required>
    <button type="submit">Log in</button>
  </form>
</body>
</html>"""


def _safe_next(next_path: Optional[str]) -> str:
    return next_path if next_path in ALLOWED_NEXT else "/docs"


def _login_redirect(next_path: str) -> RedirectResponse:
    return RedirectResponse(f"/docs/login?next={next_path}", status_code=303)


@router.get("/docs/login")
def docs_login_page(request: Request, next: Optional[str] = None):
    next_path = _safe_next(next)
    if is_admin(request):
        return RedirectResponse(next_path, status_code=303)
    return HTMLResponse(LOGIN_PAGE.format(error="", next=escape(next_path)))


@router.post("/docs/login")
def docs_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    next: Optional[str] = Form(None),
):
    next_path = _safe_next(next)
    if not verify_admin_credentials(username, password):
        error = '<p class="error">Invalid username or password</p>'
        return HTMLResponse(LOGIN_PAGE.format(error=error, next=escape(next_path)),
                            status_code=401)
    request.session["admin"] = True
    request.session["exp"] = (timedelta(hours=12)).total_seconds()
    return RedirectResponse(next_path, status_code=303)


@router.get("/docs/logout")
def docs_logout(request: Request):
    request.session.clear()
    return _login_redirect("/docs")


@router.get("/docs")
def swagger_ui(request: Request):
    if not is_admin(request):
        return _login_redirect("/docs")
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=f"{request.app.title} - Swagger UI",
        # Try it out 요청에 세션 쿠키를 함께 보낸다
        swagger_ui_parameters={"withCredentials": True},
    )


@router.get("/redoc")
def redoc(request: Request):
    if not is_admin(request):
        return _login_redirect("/redoc")
    return get_redoc_html(openapi_url="/openapi.json",
                          title=f"{request.app.title} - ReDoc")


@router.get("/openapi.json")
def openapi_schema(request: Request,
    api_key: Optional[str] = Security(api_key_header)):
    # 스크립트/코드 생성기에서는 X-API-Key 헤더로도 스키마를 받을 수 있다
    if not is_admin(request, api_key):
        return JSONResponse({"detail": "Admin required"}, status_code=401)
    return JSONResponse(request.app.openapi())
