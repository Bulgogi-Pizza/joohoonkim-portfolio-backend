from app.database import get_db
from app.models import ResearchArea
from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/api/search"
)


@router.get("/sitemap.xml")
def sitemap(db: Session = Depends(get_db)):
    base = "https://joohoonkim.site"
    areas = db.query(ResearchArea).filter(ResearchArea.is_active == True).all()
    urls = [
        f"{base}/",
        f"{base}/research",
        f"{base}/publications",
        f"{base}/awards",
        f"{base}/conferences",
        f"{base}/cv",
        *[f"{base}/research/{a.slug}" for a in areas],
    ]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    xml += [f"<url><loc>{u}</loc></url>" for u in urls]
    xml.append("</urlset>")
    return Response("".join(xml), media_type="application/xml")
