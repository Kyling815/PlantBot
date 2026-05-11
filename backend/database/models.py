"""
SQLAlchemy ORM models.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from backend.database.db import Base


class DiagnosisRecord(Base):
    """Stores each diagnosis result for history / audit purposes."""
    __tablename__ = "diagnosis_records"

    id = Column(Integer, primary_key=True, index=True)
    raw_label = Column(String(120), nullable=False)
    label = Column(String(120), nullable=False)
    confidence = Column(Float, nullable=False)
    status = Column(String(30), nullable=False)
    plant = Column(String(60))
    disease = Column(String(60))
    severity = Column(String(20))
    agent_response = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
