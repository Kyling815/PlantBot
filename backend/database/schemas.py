"""
Pydantic schemas for database records.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class DiagnosisRecordCreate(BaseModel):
    raw_label: str
    label: str
    confidence: float
    status: str
    plant: Optional[str] = None
    disease: Optional[str] = None
    severity: Optional[str] = None
    agent_response: Optional[str] = None


class DiagnosisRecordRead(DiagnosisRecordCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
