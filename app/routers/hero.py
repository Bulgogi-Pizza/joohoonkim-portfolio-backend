from datetime import datetime
from typing import List

from app.database import get_db
from app.models import HeroContent
from app.security.security import require_admin
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/hero", tags=["hero"])


@router.get("", response_model=HeroContent)
def get_active_hero(db: Session = Depends(get_db)):
    """Get the active hero content for the homepage"""
    hero = db.query(HeroContent).filter(HeroContent.is_active == True).first()
    if not hero:
        # Return default content if none exists
        return HeroContent(
            id=0,
            title="Innovating",
            title_highlight="Nanophotonics",
            description="Ph.D. student at POSTECH, specializing in nanofabrication and metasurfaces for next-gen optical applications like VR/AR and optical computing.",
            cta_primary_text="Explore Research",
            cta_primary_link="/research",
            cta_secondary_text="View CV",
            cta_secondary_link="/cv",
            is_active=True
        )
    return hero


@router.get("/all", response_model=List[HeroContent])
def get_all_hero_contents(
    db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):
    """Get all hero contents (admin only)"""
    return db.query(HeroContent).order_by(HeroContent.id.desc()).all()


@router.post("", response_model=HeroContent)
def create_hero_content(
    hero_data: HeroContent,
    db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):
    """Create new hero content (admin only)"""
    # If this is set to active, deactivate all others
    if hero_data.is_active:
        db.query(HeroContent).update({HeroContent.is_active: False})
    
    hero_data.created_at = datetime.utcnow()
    hero_data.updated_at = datetime.utcnow()
    db.add(hero_data)
    db.commit()
    db.refresh(hero_data)
    return hero_data


@router.put("/{hero_id}", response_model=HeroContent)
def update_hero_content(
    hero_id: int,
    hero_data: HeroContent,
    db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):
    """Update hero content (admin only)"""
    hero = db.query(HeroContent).filter(HeroContent.id == hero_id).first()
    if not hero:
        raise HTTPException(status_code=404, detail="Hero content not found")

    # If this is being set to active, deactivate all others
    if hero_data.is_active and not hero.is_active:
        db.query(HeroContent).filter(HeroContent.id != hero_id).update({HeroContent.is_active: False})

    for key, value in hero_data.dict(exclude_unset=True).items():
        if key not in ["id", "created_at"]:
            setattr(hero, key, value)

    hero.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(hero)
    return hero


@router.delete("/{hero_id}")
def delete_hero_content(
    hero_id: int,
    db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):
    """Delete hero content (admin only)"""
    hero = db.query(HeroContent).filter(HeroContent.id == hero_id).first()
    if not hero:
        raise HTTPException(status_code=404, detail="Hero content not found")

    db.delete(hero)
    db.commit()
    return {"message": "Hero content deleted successfully"}


@router.post("/{hero_id}/activate")
def activate_hero_content(
    hero_id: int,
    db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):
    """Set a specific hero content as active (admin only)"""
    hero = db.query(HeroContent).filter(HeroContent.id == hero_id).first()
    if not hero:
        raise HTTPException(status_code=404, detail="Hero content not found")

    # Deactivate all others
    db.query(HeroContent).update({HeroContent.is_active: False})
    
    # Activate this one
    hero.is_active = True
    hero.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(hero)
    return {"message": "Hero content activated successfully", "hero": hero}

