import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import json

from main import app
from models import HumanOSDiagnosisInput, MentalState, BodyLog, ConditionType, ThoughtPattern

client = TestClient(app)


class TestHumanOSDiagnosisAPI:
    """HumanOS診断APIのテスト"""
    
    def test_root_endpoint(self):
        """ルートエンドポイントのテスト"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert data["message"] == "HumanOS診断APIへようこそ"
    
    def test_health_check(self):
        """ヘルスチェックエンドポイントのテスト"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert data["service"] == "HumanOS診断API"
    
    def test_get_conditions(self):
        """状態タイプ一覧取得のテスト"""
        response = client.get("/conditions")
        assert response.status_code == 200
        data = response.json()
        assert "conditions" in data
        assert len(data["conditions"]) > 0
        # すべての状態タイプが含まれていることを確認
        condition_values = [c["value"] for c in data["conditions"]]
        expected_conditions = ["healthy", "balanced", "stressed", "anxious", "depressed", "exhausted", "confused"]
        for condition in expected_conditions:
            assert condition in condition_values
    
    def test_get_thought_patterns(self):
        """思考パターン一覧取得のテスト"""
        response = client.get("/thought-patterns")
        assert response.status_code == 200
        data = response.json()
        assert "thought_patterns" in data
        assert len(data["thought_patterns"]) > 0
        # すべての思考パターンが含まれていることを確認
        pattern_values = [p["value"] for p in data["thought_patterns"]]
        expected_patterns = ["analytical", "creative", "intuitive", "logical", "emotional", "systematic", "chaotic"]
        for pattern in expected_patterns:
            assert pattern in pattern_values
    
    def test_diagnose_complete(self):
        """完全な診断のテスト"""
        test_data = {
            "birth_date": "1990-01-01T00:00:00",
            "birth_location": "東京都",
            "birth_time": "09:30",
            "condition": "stressed",
            "body_logs": [
                {
                    "timestamp": "2024-01-01T10:00:00",
                    "heart_rate": 75,
                    "blood_pressure_systolic": 120,
                    "blood_pressure_diastolic": 80,
                    "temperature": 36.5,
                    "sleep_hours": 6.5,
                    "exercise_minutes": 30,
                    "stress_level": 7,
                    "symptoms": ["頭痛", "肩こり"]
                }
            ],
            "mental_state": {
                "mood": 4,
                "energy_level": 3,
                "focus_level": 5,
                "anxiety_level": 8,
                "motivation": 4,
                "social_connection": 6,
                "emotional_stability": 4,
                "self_esteem": 5
            },
            "thought_patterns": ["analytical", "logical"],
            "additional_notes": "最近仕事が忙しい"
        }
        
        response = client.post("/diagnose", json=test_data)
        assert response.status_code == 200
        
        data = response.json()
        
        # レスポンス構造の確認
        assert "analysis" in data
        assert "bugs" in data
        assert "improvement_proposals" in data
        assert "summary" in data
        assert "recommendations" in data
        assert "created_at" in data
        
        # 分析データの確認
        analysis = data["analysis"]
        assert "overall_score" in analysis
        assert "system_structure" in analysis
        assert "strengths" in analysis
        assert "weaknesses" in analysis
        assert "patterns" in analysis
        
        # スコアの範囲確認
        assert 0 <= analysis["overall_score"] <= 100
        
        # システム構造の確認
        structure = analysis["system_structure"]
        assert "core_system" in structure
        assert "cognitive_system" in structure
        assert "emotional_system" in structure
        assert "physical_system" in structure
        assert "social_system" in structure
        
        # バグの確認
        bugs = data["bugs"]
        assert isinstance(bugs, list)
        for bug in bugs:
            assert "category" in bug
            assert "severity" in bug
            assert "description" in bug
            assert "impact" in bug
            assert "potential_cause" in bug
            assert bug["severity"] in ["low", "medium", "high", "critical"]
        
        # 改善提案の確認
        proposals = data["improvement_proposals"]
        assert isinstance(proposals, list)
        for proposal in proposals:
            assert "category" in proposal
            assert "priority" in proposal
            assert "action" in proposal
            assert "expected_outcome" in proposal
            assert "implementation_difficulty" in proposal
            assert proposal["priority"] in ["low", "medium", "high", "urgent"]
            assert proposal["implementation_difficulty"] in ["easy", "medium", "hard"]
    
    def test_diagnose_simple(self):
        """シンプル診断のテスト"""
        test_data = {
            "birth_date": "1990-01-01T00:00:00",
            "birth_location": "東京都",
            "condition": "stressed",
            "mood": 4,
            "energy_level": 3,
            "anxiety_level": 8,
            "thought_patterns": ["analytical", "logical"]
        }
        
        response = client.post("/diagnose/simple", json=test_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "analysis" in data
        assert "overall_score" in data["analysis"]
        assert 0 <= data["analysis"]["overall_score"] <= 100
    
    def test_diagnose_missing_required_fields(self):
        """必須フィールド欠如時のテスト"""
        # birth_date欠如
        test_data = {
            "birth_location": "東京都",
            "condition": "stressed",
            "mental_state": {"mood": 5},
            "thought_patterns": ["analytical"]
        }
        
        response = client.post("/diagnose", json=test_data)
        assert response.status_code == 400
        assert "生年月日は必須です" in response.json()["detail"]
        
        # birth_location欠如
        test_data = {
            "birth_date": "1990-01-01T00:00:00",
            "condition": "stressed",
            "mental_state": {"mood": 5},
            "thought_patterns": ["analytical"]
        }
        
        response = client.post("/diagnose", json=test_data)
        assert response.status_code == 400
        assert "出生地は必須です" in response.json()["detail"]
    
    def test_diagnose_invalid_date_format(self):
        """無効な日付形式のテスト"""
        test_data = {
            "birth_date": "invalid-date",
            "birth_location": "東京都",
            "condition": "stressed",
            "mood": 4,
            "energy_level": 3,
            "anxiety_level": 8,
            "thought_patterns": ["analytical"]
        }
        
        response = client.post("/diagnose/simple", json=test_data)
        assert response.status_code == 400
        assert "日付形式が正しくありません" in response.json()["detail"]
    
    def test_diagnose_different_conditions(self):
        """異なる状態での診断テスト"""
        base_data = {
            "birth_date": "1990-01-01T00:00:00",
            "birth_location": "東京都",
            "mental_state": {"mood": 5, "energy_level": 5, "anxiety_level": 5},
            "thought_patterns": ["analytical"]
        }
        
        conditions = ["healthy", "stressed", "anxious", "depressed", "exhausted", "confused"]
        
        for condition in conditions:
            test_data = base_data.copy()
            test_data["condition"] = condition
            
            response = client.post("/diagnose", json=test_data)
            assert response.status_code == 200
            
            data = response.json()
            assert "analysis" in data
            assert "bugs" in data
            assert "improvement_proposals" in data
    
    def test_diagnose_different_thought_patterns(self):
        """異なる思考パターンでの診断テスト"""
        base_data = {
            "birth_date": "1990-01-01T00:00:00",
            "birth_location": "東京都",
            "condition": "balanced",
            "mental_state": {"mood": 7, "energy_level": 7, "anxiety_level": 3}
        }
        
        patterns = ["analytical", "creative", "intuitive", "logical", "emotional", "systematic", "chaotic"]
        
        for pattern in patterns:
            test_data = base_data.copy()
            test_data["thought_patterns"] = [pattern]
            
            response = client.post("/diagnose", json=test_data)
            assert response.status_code == 200
            
            data = response.json()
            assert "analysis" in data
            assert len(data["analysis"]["patterns"]) > 0
    
    def test_diagnose_with_body_logs(self):
        """身体ログ付き診断のテスト"""
        test_data = {
            "birth_date": "1990-01-01T00:00:00",
            "birth_location": "東京都",
            "condition": "healthy",
            "mental_state": {"mood": 8, "energy_level": 8, "anxiety_level": 2},
            "thought_patterns": ["analytical"],
            "body_logs": [
                {
                    "timestamp": "2024-01-01T10:00:00",
                    "heart_rate": 65,
                    "stress_level": 2,
                    "sleep_hours": 8.0
                },
                {
                    "timestamp": "2024-01-02T10:00:00",
                    "heart_rate": 68,
                    "stress_level": 3,
                    "sleep_hours": 7.5
                }
            ]
        }
        
        response = client.post("/diagnose", json=test_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "analysis" in data
        # 健康的な状態なのでスコアは高いはず
        assert data["analysis"]["overall_score"] >= 60
    
    def test_diagnose_edge_cases(self):
        """エッジケースのテスト"""
        # 最小限のデータ
        minimal_data = {
            "birth_date": "1990-01-01T00:00:00",
            "birth_location": "東京都",
            "condition": "balanced",
            "mental_state": {"mood": 5},
            "thought_patterns": ["analytical"]
        }
        
        response = client.post("/diagnose", json=minimal_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "analysis" in data
        assert isinstance(data["analysis"]["overall_score"], (int, float))
    
    def test_diagnose_consistency(self):
        """診断結果の一貫性テスト"""
        test_data = {
            "birth_date": "1990-01-01T00:00:00",
            "birth_location": "東京都",
            "condition": "stressed",
            "mental_state": {"mood": 4, "energy_level": 3, "anxiety_level": 8},
            "thought_patterns": ["analytical", "logical"]
        }
        
        # 同じ入力で複数回診断を実行
        results = []
        for _ in range(3):
            response = client.post("/diagnose", json=test_data)
            assert response.status_code == 200
            results.append(response.json())
        
        # 結果が一貫していることを確認（若干の誤差は許容）
        scores = [r["analysis"]["overall_score"] for r in results]
        for i in range(1, len(scores)):
            assert abs(scores[i] - scores[0]) < 0.1  # 小数点以下の誤差のみ許容


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
