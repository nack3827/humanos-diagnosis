from pydantic import BaseModel
from typing import List


class SimpleDiagnosisRequest(BaseModel):
    birth_date: str
    birth_location: str
    condition: str
    mood: int
    energy_level: int
    anxiety_level: int
    thought_patterns: List[str]
