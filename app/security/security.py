from fastapi import HTTPException, Request


def require_admin(request: Request):
    if not request.session.get("admin", False):
        raise HTTPException(status_code=401, detail="Admin required")
    return True
