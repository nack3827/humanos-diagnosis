from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import logging
from typing import List, Optional
import traceback

from models import (
    HumanOSDiagnosisInput, 
    HumanOSDiagnosisOutput,
    ConditionType,
    ThoughtPattern
)
from diagnosis_engine import HumanOSDiagnosisEngine
from simple_request import SimpleDiagnosisRequest
from humanizer import humanize

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FastAPIアプリケーションの初期化
app = FastAPI(
    title="HumanOS診断API",
    description="人間の状態をOSのように分析し、構造、バグ、改善提案を生成するAPI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切に制限すること
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 診断エンジンのインスタンス
diagnosis_engine = HumanOSDiagnosisEngine()


@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "message": "HumanOS診断APIへようこそ",
        "version": "1.0.0",
        "description": "人間の状態をOSのように分析するAPI",
        "endpoints": {
            "diagnosis": "/diagnose",
            "health_check": "/health",
            "conditions": "/conditions",
            "thought_patterns": "/thought-patterns"
        }
    }


@app.get("/health")
async def health_check():
    """ヘルスチェックエンドポイント"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "HumanOS診断API"
    }


@app.get("/conditions")
async def get_conditions():
    """利用可能な状態タイプの一覧を取得"""
    return {
        "conditions": [
            {"value": condition.value, "description": _get_condition_description(condition)}
            for condition in ConditionType
        ]
    }


@app.get("/thought-patterns")
async def get_thought_patterns():
    """利用可能な思考パターンの一覧を取得"""
    return {
        "thought_patterns": [
            {"value": pattern.value, "description": _get_thought_pattern_description(pattern)}
            for pattern in ThoughtPattern
        ]
    }


@app.post("/diagnose", response_model=HumanOSDiagnosisOutput)
async def diagnose_human_os(input_data: HumanOSDiagnosisInput):
    """
    HumanOS診断を実行
    
    - **birth_date**: 生年月日
    - **birth_location**: 出生地
    - **birth_time**: 出生時間（任意）
    - **condition**: 現在の状態
    - **body_logs**: 身体ログ（任意）
    - **mental_state**: 心の状態
    - **thought_patterns**: 思考パターン
    - **additional_notes**: 追加メモ（任意）
    """
    try:
        logger.info(f"診断リクエスト受信: {input_data.birth_date}, 状態: {input_data.condition}")
        
        # 入力データのバリデーション
        if not input_data.birth_date:
            raise HTTPException(status_code=400, detail="生年月日は必須です")
        
        if not input_data.birth_location:
            raise HTTPException(status_code=400, detail="出生地は必須です")
        
        if not input_data.mental_state:
            raise HTTPException(status_code=400, detail="心の状態は必須です")
        
        if not input_data.thought_patterns:
            raise HTTPException(status_code=400, detail="思考パターンは必須です")
        
        # 診断を実行
        result = diagnosis_engine.diagnose(input_data)
        
        logger.info(f"診断完了: 総合スコア {result.analysis.overall_score}")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"診断中にエラーが発生しました: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500, 
            detail=f"診断中に内部エラーが発生しました: {str(e)}"
        )


@app.post("/diagnose/simple", response_model=HumanOSDiagnosisOutput)
async def diagnose_simple(request: SimpleDiagnosisRequest):
    """
    シンプルなHumanOS診断を実行
    
    より少ないパラメータで手軽に診断を実行するエンドポイント
    """
    try:
        # 日付文字列をdatetimeオブジェクトに変換
        birth_datetime = datetime.fromisoformat(request.birth_date.replace('Z', '+00:00'))
        
        # 状態タイプを変換
        condition = ConditionType(request.condition)
        
        # 思考パターンを変換
        thought_patterns = [ThoughtPattern(pattern) for pattern in request.thought_patterns]
        
        # MentalStateを作成
        from models import MentalState
        mental_state = MentalState(
            mood=request.mood,
            energy_level=request.energy_level,
            anxiety_level=request.anxiety_level
        )
        
        # 診断入力を作成
        input_data = HumanOSDiagnosisInput(
            birth_date=birth_datetime,
            birth_location=request.birth_location,
            condition=condition,
            mental_state=mental_state,
            thought_patterns=thought_patterns
        )
        
        # 診断を実行
        result = diagnosis_engine.diagnose(input_data)
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"入力データの形式が正しくありません: {str(e)}")
    except Exception as e:
        logger.error(f"シンプル診断中にエラーが発生しました: {str(e)}")
        raise HTTPException(status_code=500, detail=f"診断中にエラーが発生しました: {str(e)}")


def _get_condition_description(condition: ConditionType) -> str:
    """状態タイプの説明を取得"""
    descriptions = {
        ConditionType.HEALTHY: "健康的で安定した状態",
        ConditionType.BALANCED: "バランスの取れた状態",
        ConditionType.STRESSED: "ストレスを感じている状態",
        ConditionType.ANXIOUS: "不安を感じている状態",
        ConditionType.DEPRESSED: "抑うつ的な状態",
        ConditionType.EXHAUSTED: "疲労困憊の状態",
        ConditionType.CONFUSED: "混乱している状態"
    }
    return descriptions.get(condition, "")


def _get_thought_pattern_description(pattern: ThoughtPattern) -> str:
    """思考パターンの説明を取得"""
    descriptions = {
        ThoughtPattern.ANALYTICAL: "論理的・分析的な思考",
        ThoughtPattern.CREATIVE: "創造的・発想的な思考",
        ThoughtPattern.INTUITIVE: "直感的な思考",
        ThoughtPattern.LOGICAL: "論理的な思考",
        ThoughtPattern.EMOTIONAL: "感情的な思考",
        ThoughtPattern.SYSTEMATIC: "体系的・組織的な思考",
        ThoughtPattern.CHAOTIC: "混沌とした思考"
    }
    return descriptions.get(pattern, "")


# エラーハンドラー
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"未処理の例外: {str(exc)}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={"error": "内部サーバーエラーが発生しました", "status_code": 500}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

@app.post("/full")
def full_diagnosis(input_data: HumanOSDiagnosisInput):
    
    # ① 診断
    result = diagnosis_engine.diagnose(input_data)
    
    # ② 人間化
    human_text = humanize(result)
    
    import json

    return {
        "raw": json.loads(json.dumps(result, default=str)),
        "human": human_text
    }