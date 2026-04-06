from pydantic import BaseModel, Field
from typing import List, Optional


class SimpleDiagnosisRequest(BaseModel):
    birth_date: str = Field(..., description="生年月日")
    birth_location: str = Field(..., description="出生地")
    condition: str = Field(..., description="状態")
    mood: int = Field(..., ge=1, le=10, description="気分")
    energy_level: int = Field(..., ge=1, le=10, description="エネルギーレベル")
    anxiety_level: int = Field(..., ge=1, le=10, description="不安レベル")
    thought_patterns: List[str] = Field(..., description="思考パターン")
