from __future__ import annotations

from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base
import enum


class ScanStatus(str, enum.Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"


class Scan(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True)
    target = Column(String, index=True, nullable=False)
    tools = Column(String, nullable=True)  # comma-separated
    status = Column(Enum(ScanStatus), default=ScanStatus.pending, index=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    error = Column(String, nullable=True)

    # Raw outputs per tool
    raw_results = Column(JSON, nullable=True)

    findings = relationship("Finding", back_populates="scan", cascade="all, delete-orphan")
