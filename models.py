from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


class ConditionType(str, Enum):
    HEALTHY = "healthy"
    STRESSED = "stressed"
    ANXIOUS = "anxious"
    DEPRESSED = "depressed"
    EXHAUSTED = "exhausted"
    CONFUSED = "confused"
    BALANCED = "balanced"


class ThoughtPattern(str, Enum):
    ANALYTICAL = "analytical"
    CREATIVE = "creative"
    INTUITIVE = "intuitive"
    LOGICAL = "logical"
    EMOTIONAL = "emotional"
    SYSTEMATIC = "systematic"
    CHAOTIC = "chaotic"


class BodyLog(BaseModel):
    timestamp: datetime
    heart_rate: Optional[int] = Field(None, ge=40, le=200, description="心拍数")
    blood_pressure_systolic: Optional[int] = Field(None, ge=80, le=200, description="収縮期血圧")
    blood_pressure_diastolic: Optional[int] = Field(None, ge=40, le=120, description="拡張期血圧")
    temperature: Optional[float] = Field(None, ge=35.0, le=42.0, description="体温")
    sleep_hours: Optional[float] = Field(None, ge=0.0, le=24.0, description="睡眠時間")
    exercise_minutes: Optional[int] = Field(None, ge=0, description="運動時間（分）")
    weight: Optional[float] = Field(None, ge=20.0, le=300.0, description="体重（kg）")
    stress_level: Optional[int] = Field(None, ge=1, le=10, description="ストレスレベル（1-10）")
    symptoms: Optional[List[str]] = Field(default_factory=list, description="症状リスト")


class MentalState(BaseModel):
    mood: Optional[int] = Field(None, ge=1, le=10, description="現在の気分（1-10）")
    energy_level: Optional[int] = Field(None, ge=1, le=10, description="エネルギーレベル（1-10）")
    focus_level: Optional[int] = Field(None, ge=1, le=10, description="集中力レベル（1-10）")
    anxiety_level: Optional[int] = Field(None, ge=1, le=10, description="不安レベル（1-10）")
    motivation: Optional[int] = Field(None, ge=1, le=10, description="モチベーション（1-10）")
    social_connection: Optional[int] = Field(None, ge=1, le=10, description="社会的つながり（1-10）")
    emotional_stability: Optional[int] = Field(None, ge=1, le=10, description="感情的安定性（1-10）")
    self_esteem: Optional[int] = Field(None, ge=1, le=10, description="自己肯定感（1-10）")


class HumanOSDiagnosisInput(BaseModel):
    birth_date: datetime = Field(..., description="生年月日")
    birth_location: str = Field(..., description="出生地")
    birth_time: Optional[str] = Field(None, description="出生時間（HH:MM形式）")
    condition: ConditionType = Field(..., description="現在の状態")
    body_logs: List[BodyLog] = Field(default_factory=list, description="身体ログ")
    mental_state: MentalState = Field(..., description="心の状態")
    thought_patterns: List[ThoughtPattern] = Field(..., description="思考パターン")
    additional_notes: Optional[str] = Field(None, description="追加メモ")


class SystemStructure(BaseModel):
    core_system: str = Field(..., description="コアシステムの状態")
    emotional_system: str = Field(..., description="感情システムの状態")
    cognitive_system: str = Field(..., description="認知システムの状態")
    physical_system: str = Field(..., description="身体システムの状態")
    social_system: str = Field(..., description="社会システムの状態")


class SystemBug(BaseModel):
    category: str = Field(..., description="バグのカテゴリ")
    severity: str = Field(..., description="深刻度（low/medium/high/critical）")
    description: str = Field(..., description="バグの説明")
    impact: str = Field(..., description="影響範囲")
    potential_cause: str = Field(..., description="潜在的な原因")


class ImprovementProposal(BaseModel):
    category: str = Field(..., description="改善提案のカテゴリ")
    priority: str = Field(..., description="優先度（low/medium/high/urgent）")
    action: str = Field(..., description="具体的なアクション")
    expected_outcome: str = Field(..., description="期待される効果")
    implementation_difficulty: str = Field(..., description="実装難易度（easy/medium/hard）")


class HumanOSAnalysis(BaseModel):
    overall_score: float = Field(..., ge=0.0, le=100.0, description="総合スコア")
    system_structure: SystemStructure = Field(..., description="システム構造分析")
    strengths: List[str] = Field(..., description="強み")
    weaknesses: List[str] = Field(..., description="弱み")
    patterns: List[str] = Field(..., description="観察されるパターン")
    
    class Config:
        arbitrary_types_allowed = True


class HumanOSDiagnosisOutput(BaseModel):
    analysis: HumanOSAnalysis = Field(..., description="人間OS分析")
    bugs: List[SystemBug] = Field(..., description="システムバグ")
    improvement_proposals: List[ImprovementProposal] = Field(..., description="改善提案")
    summary: str = Field(..., description="要約")
    recommendations: List[str] = Field(..., description="推奨事項")
    created_at: datetime = Field(default_factory=datetime.now, description="診断作成日時")
    
    class Config:
        arbitrary_types_allowed = True
