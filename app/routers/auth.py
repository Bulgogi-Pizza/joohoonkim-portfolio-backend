# app/routers/auth.py
import os
from datetime import timedelta

from fastapi import APIRouter, HTTPException, Request
from passlib.context import CryptContext
from pydantic import BaseModel

router = APIRouter(prefix="/api/auth", tags=["auth"])
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
ADMIN_USER = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_HASH = os.getenv("ADMIN_PASSWORD_HASH", "")


class LoginReq(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(data: LoginReq, request: Request):
    if data.username != ADMIN_USER or not pwd.verify(data.password, ADMIN_HASH):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    request.session["admin"] = True
    request.session["exp"] = (timedelta(hours=12)).total_seconds()
    return {"ok": True}


@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return {"ok": True}


@router.get("/me")
def me(request: Request):
    return {"admin": bool(request.session.get("admin", False))}
