from __future__ import annotations

from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base
import enum


asset_tag_table = Table(
    "asset_tags",
    Base.metadata,
    Column("asset_id", Integer, ForeignKey("assets.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class AssetType(str, enum.Enum):
    host = "host"
    domain = "domain"


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True)
    identifier = Column(String, index=True, nullable=False)  # ip, cidr, domain
    type = Column(Enum(AssetType), nullable=False, default=AssetType.host)
    name = Column(String, nullable=True)
    business_criticality = Column(Integer, default=1)  # 1-5
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    tags = relationship("Tag", secondary=asset_tag_table, back_populates="assets", lazy="joined")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)

    assets = relationship("Asset", secondary=asset_tag_table, back_populates="tags")
