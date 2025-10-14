from __future__ import annotations

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.asset import Asset, Tag
from ..schemas.assets import AssetBase, AssetRead, TagRead
from ..security.auth import require_roles

router = APIRouter()


@router.get("/", response_model=List[AssetRead])
def list_assets(db: Session = Depends(get_db)):
    assets = db.query(Asset).all()
    return assets


@router.post("/", response_model=AssetRead)
def create_asset(asset: AssetBase, db: Session = Depends(get_db), user=Depends(require_roles("developer", "analyst", "manager", "admin"))):
    # ensure tags
    tag_objs: list[Tag] = []
    for tag_name in asset.tags:
        tag = db.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            db.add(tag)
            db.flush()
        tag_objs.append(tag)

    obj = Asset(
        identifier=asset.identifier,
        type=asset.type,  # type: ignore[arg-type]
        name=asset.name,
        business_criticality=asset.business_criticality,
        tags=tag_objs,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{asset_id}")
def delete_asset(asset_id: int, db: Session = Depends(get_db), user=Depends(require_roles("admin"))):
    obj = db.query(Asset).get(asset_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Asset not found")
    db.delete(obj)
    db.commit()
    return {"ok": True}
