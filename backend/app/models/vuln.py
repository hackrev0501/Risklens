from __future__ import annotations

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base


class Vulnerability(Base):
    __tablename__ = "vulnerabilities"

    id = Column(Integer, primary_key=True)
    cve_id = Column(String, index=True, nullable=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    cvss = Column(Float, nullable=True)
    exploit_available = Column(Boolean, default=False)
    source = Column(String, nullable=True)  # scanner source


class Finding(Base):
    __tablename__ = "findings"

    id = Column(Integer, primary_key=True)
    scan_id = Column(Integer, ForeignKey("scans.id", ondelete="CASCADE"))
    asset_id = Column(Integer, ForeignKey("assets.id", ondelete="CASCADE"))
    vuln_id = Column(Integer, ForeignKey("vulnerabilities.id", ondelete="CASCADE"))

    port = Column(Integer, nullable=True)
    service = Column(String, nullable=True)

    scan = relationship("Scan", back_populates="findings")
    asset = relationship("Asset")
    vuln = relationship("Vulnerability")
