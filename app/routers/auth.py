# app/routers/auth.py
from datetime import timedelta
from typing import Optional

from app.security.security import api_key_header, is_admin, \
    verify_admin_credentials
from fastapi import APIRouter, HTTPException, Request, Security
from pydantic import BaseModel

router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginReq(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(data: LoginReq, request: Request):
    if not verify_admin_credentials(data.username, data.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    request.session["admin"] = True
    request.session["exp"] = (timedelta(hours=12)).total_seconds()
    return {"ok": True}


@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return {"ok": True}


@router.get("/me")
def me(request: Request, api_key: Optional[str] = Security(api_key_header)):
    return {"admin": is_admin(request, api_key)}
