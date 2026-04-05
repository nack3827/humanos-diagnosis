# HumanOS診断API

人間の状態をOSのように分析し、構造、バグ、改善提案を生成するAPIです。

## 概要

このAPIは、生年月日、出生地、身体ログ、心の状態、思考パターンなどの情報を入力として受け取り、人間の状態をコンピュータOSのように分析します。システム構造の評価、バグの特定、改善提案の生成を行い、構造的で感情にも刺さる文章で診断結果を返します。

## 特徴

- **構造的分析**: 人間をコアシステム、認知システム、感情システム、身体システム、社会システムの5つの構成要素で分析
- **バグ検出**: ストレス応答システム、不安検出システム、報酬システムなどの具体的な問題を特定
- **改善提案**: 優先度付きの具体的なアクションプランを提示
- **日本語対応**: 感情に響く自然な日本語で診断結果を生成
- **REST API**: FastAPIベースのモダンなAPI設計

## セットアップ

### 環境要件

- Python 3.8以上

### インストール

```bash
# リポジトリをクローン
git clone <repository-url>
cd humanos-diagnosis-api

# 仮想環境を作成
python -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate  # Windows

# 依存パッケージをインストール
pip install -r requirements.txt
```

### 起動

```bash
# 開発サーバーで起動
python main.py

# またはuvicornを直接使用
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

サーバーが起動したら、以下のURLでアクセスできます：

- APIドキュメント: http://localhost:8000/docs
- ReDocドキュメント: http://localhost:8000/redoc

## APIエンドポイント

### POST `/diagnose`

完全なHumanOS診断を実行します。

#### リクエスト例

```json
{
  "birth_date": "1990-01-01T00:00:00",
  "birth_location": "東京都",
  "birth_time": "09:30",
  "condition": "stressed",
  "body_logs": [
    {
      "timestamp": "2024-01-01T10:00:00",
      "heart_rate": 75,
      "stress_level": 7,
      "sleep_hours": 6.5
    }
  ],
  "mental_state": {
    "mood": 4,
    "energy_level": 3,
    "anxiety_level": 8,
    "focus_level": 5,
    "motivation": 4
  },
  "thought_patterns": ["analytical", "logical"],
  "additional_notes": "最近仕事が忙しい"
}
```

#### レスポンス例

```json
{
  "analysis": {
    "overall_score": 52.3,
    "system_structure": {
      "core_system": "コアシステムは正常に機能していますが、若干の最適化余地があります...",
      "cognitive_system": "認知システムは最適化されており、安定した稼働を維持しています...",
      "emotional_system": "感情システムに軽度の不具合が見られます...",
      "physical_system": "身体システムは正常に機能していますが、若干の最適化余地があります...",
      "social_system": "社会システムは正常に機能していますが、若干の最適化余地があります..."
    },
    "strengths": ["論理的思考能力が高く、複雑な問題解決に適しています"],
    "weaknesses": ["ストレス応答システムに過負荷がかかっており、リセットが必要です"],
    "patterns": ["分析的思考パターンが強く、詳細な分析を得意としています"]
  },
  "bugs": [
    {
      "category": "ストレス応答システム",
      "severity": "medium",
      "description": "コルチゾール・リズムの異常検出...",
      "impact": "パフォーマンス低下、免疫システムの抑制",
      "potential_cause": "長期的なストレス暴露、睡眠不足"
    }
  ],
  "improvement_proposals": [
    {
      "category": "システム最適化",
      "priority": "high",
      "action": "睡眠サイクルの正規化...",
      "expected_outcome": "メモリConsolidationの向上、認知パフォーマンスの20-30%向上",
      "implementation_difficulty": "medium"
    }
  ],
  "summary": "HumanOS診断レポート - 総合評価：要注意（52.3/100点）...",
  "recommendations": ["専門家への相談を推奨します"],
  "created_at": "2024-01-01T10:00:00"
}
```

### POST `/diagnose/simple`

シンプルなパラメータで手軽に診断を実行します。

#### リクエスト例

```json
{
  "birth_date": "1990-01-01T00:00:00",
  "birth_location": "東京都",
  "condition": "stressed",
  "mood": 4,
  "energy_level": 3,
  "anxiety_level": 8,
  "thought_patterns": ["analytical", "logical"]
}
```

### GET `/conditions`

利用可能な状態タイプの一覧を取得します。

### GET `/thought-patterns`

利用可能な思考パターンの一覧を取得します。

### GET `/health`

APIのヘルスチェックを行います。

## データモデル

### 状態タイプ (ConditionType)

- `healthy`: 健康的で安定した状態
- `balanced`: バランスの取れた状態
- `stressed`: ストレスを感じている状態
- `anxious`: 不安を感じている状態
- `depressed`: 抑うつ的な状態
- `exhausted`: 疲労困憊の状態
- `confused`: 混乱している状態

### 思考パターン (ThoughtPattern)

- `analytical`: 論理的・分析的な思考
- `creative`: 創造的・発想的な思考
- `intuitive`: 直感的な思考
- `logical`: 論理的な思考
- `emotional`: 感情的な思考
- `systematic`: 体系的・組織的な思考
- `chaotic`: 混沌とした思考

## 診断アルゴリズム

### スコア計算

診断エンジンは以下の要素を考慮して総合スコアを計算します：

1. **状態の重み付け (30%)**: 現在の状態の深刻度
2. **身体的状態 (20%)**: 身体ログから得られる健康指標
3. **精神的状態 (25%)**: 気分、エネルギー、不安レベルなど
4. **年齢要因 (10%)**: 年齢に応じた特性
5. **安定性 (15%)**: 全体的なシステムの安定性

### バグ検出ロジック

入力データに基づいて、以下のようなシステムバグを検出：

- ストレス応答システムの異常
- 不安検出システムの過作動
- 報酬システムの機能不全
- エネルギー管理システムの低下
- 自律神経システムの不均衡

### 改善提案生成

検出されたバグと状態に基づいて、優先度付きの具体的な改善提案を生成：

- システム最適化
- 栄養システム改善
- ストレス管理
- 運動プログラム
- 認知トレーニング

## 使用例

### Pythonクライアント

```python
import requests
import json

# 診断リクエスト
data = {
    "birth_date": "1990-01-01T00:00:00",
    "birth_location": "東京都",
    "condition": "stressed",
    "mental_state": {
        "mood": 4,
        "energy_level": 3,
        "anxiety_level": 8
    },
    "thought_patterns": ["analytical"]
}

response = requests.post("http://localhost:8000/diagnose", json=data)
result = response.json()

print(f"総合スコア: {result['analysis']['overall_score']}")
print(f"要約: {result['summary']}")
```

### curlコマンド

```bash
curl -X POST "http://localhost:8000/diagnose" \
-H "Content-Type: application/json" \
-d '{
  "birth_date": "1990-01-01T00:00:00",
  "birth_location": "東京都",
  "condition": "stressed",
  "mental_state": {
    "mood": 4,
    "energy_level": 3,
    "anxiety_level": 8
  },
  "thought_patterns": ["analytical"]
}'
```

## 開発

### テスト実行

```bash
# テストを実行
python -m pytest tests/

# カバレッジを表示
python -m pytest --cov=. tests/
```

### コードフォーマット

```bash
# blackでフォーマット
black .

# flake8で linting
flake8 .
```

## 注意事項

- このAPIは教育的・娯楽的目的で提供されています
- 実際の医療診断に代わるものではありません
- 深刻な健康上の懸念がある場合は、必ず医療専門家に相談してください
- 個人情報の取り扱いには十分注意してください

## ライセンス

MIT License

## 貢献

バグレポートや機能リクエスト、プルリクエストを歓迎します。

---

*HumanOS診断API - あなたの内なるOSを理解するためのツール*
