#!/usr/bin/env python3
"""
HumanOS診断APIの使用例
"""

import requests
import json
from datetime import datetime

# APIのベースURL
BASE_URL = "http://localhost:8000"

def example_diagnosis_complete():
    """完全な診断の例"""
    print("=== 完全なHumanOS診断の例 ===")
    
    data = {
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
            },
            {
                "timestamp": "2024-01-02T10:00:00",
                "heart_rate": 78,
                "stress_level": 6,
                "sleep_hours": 6.0
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
        "additional_notes": "最近仕事が忙しく、睡眠不足が続いている"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/diagnose", json=data)
        response.raise_for_status()
        
        result = response.json()
        
        print(f"総合スコア: {result['analysis']['overall_score']:.1f}/100")
        print(f"\n要約:")
        print(result['summary'])
        
        print(f"\nシステム構造:")
        structure = result['analysis']['system_structure']
        for system, description in structure.items():
            print(f"• {system}: {description[:50]}...")
        
        print(f"\n検出されたバグ ({len(result['bugs'])}件):")
        for i, bug in enumerate(result['bugs'], 1):
            print(f"{i}. {bug['category']} ({bug['severity']})")
            print(f"   {bug['description']}")
        
        print(f"\n改善提案 ({len(result['improvement_proposals'])}件):")
        for i, proposal in enumerate(result['improvement_proposals'], 1):
            print(f"{i}. {proposal['category']} ({proposal['priority']})")
            print(f"   {proposal['action']}")
        
        print(f"\n推奨事項:")
        for i, rec in enumerate(result['recommendations'], 1):
            print(f"{i}. {rec}")
            
    except requests.exceptions.RequestException as e:
        print(f"エラー: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON解析エラー: {e}")

def example_diagnosis_simple():
    """シンプル診断の例"""
    print("\n=== シンプルHumanOS診断の例 ===")
    
    data = {
        "birth_date": "1985-05-15T00:00:00",
        "birth_location": "大阪府",
        "condition": "anxious",
        "mood": 3,
        "energy_level": 4,
        "anxiety_level": 9,
        "thought_patterns": ["emotional", "intuitive"]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/diagnose/simple", json=data)
        response.raise_for_status()
        
        result = response.json()
        
        print(f"総合スコア: {result['analysis']['overall_score']:.1f}/100")
        print(f"\n強み:")
        for strength in result['analysis']['strengths']:
            print(f"• {strength}")
        
        print(f"\n弱み:")
        for weakness in result['analysis']['weaknesses']:
            print(f"• {weakness}")
        
        print(f"\n思考パターン:")
        for pattern in result['analysis']['patterns']:
            print(f"• {pattern}")
            
    except requests.exceptions.RequestException as e:
        print(f"エラー: {e}")

def example_multiple_conditions():
    """複数の状態での診断比較"""
    print("\n=== 異なる状態での診断比較 ===")
    
    base_data = {
        "birth_date": "1992-03-10T00:00:00",
        "birth_location": "京都府",
        "mental_state": {"mood": 5, "energy_level": 6, "anxiety_level": 4},
        "thought_patterns": ["analytical", "creative"]
    }
    
    conditions = ["healthy", "stressed", "anxious", "depressed", "exhausted"]
    
    for condition in conditions:
        data = base_data.copy()
        data["condition"] = condition
        
        try:
            response = requests.post(f"{BASE_URL}/diagnose", json=data)
            response.raise_for_status()
            
            result = response.json()
            score = result['analysis']['overall_score']
            bug_count = len(result['bugs'])
            proposal_count = len(result['improvement_proposals'])
            
            print(f"{condition:12}: スコア {score:5.1f} | バグ {bug_count:2}件 | 提案 {proposal_count:2}件")
            
        except requests.exceptions.RequestException as e:
            print(f"{condition:12}: エラー - {e}")

def example_get_info():
    """情報取得エンドポイントの例"""
    print("\n=== 利用可能なオプション ===")
    
    try:
        # 状態タイプを取得
        response = requests.get(f"{BASE_URL}/conditions")
        response.raise_for_status()
        conditions = response.json()['conditions']
        
        print("状態タイプ:")
        for condition in conditions:
            print(f"• {condition['value']}: {condition['description']}")
        
        print("\n思考パターン:")
        # 思考パターンを取得
        response = requests.get(f"{BASE_URL}/thought-patterns")
        response.raise_for_status()
        patterns = response.json()['thought_patterns']
        
        for pattern in patterns:
            print(f"• {pattern['value']}: {pattern['description']}")
            
    except requests.exceptions.RequestException as e:
        print(f"エラー: {e}")

def main():
    """メイン実行関数"""
    print("HumanOS診断API 使用例")
    print("=" * 50)
    
    # APIが利用可能か確認
    try:
        response = requests.get(f"{BASE_URL}/health")
        response.raise_for_status()
        print("✓ APIサーバーが利用可能です")
    except requests.exceptions.RequestException:
        print("✗ APIサーバーが利用できません")
        print("まず 'python main.py' でサーバーを起動してください")
        return
    
    # 各種例を実行
    example_get_info()
    example_diagnosis_simple()
    example_diagnosis_complete()
    example_multiple_conditions()
    
    print("\n" + "=" * 50)
    print("例の実行完了！")
    print("APIドキュメント: http://localhost:8000/docs")
    print("ReDocドキュメント: http://localhost:8000/redoc")

if __name__ == "__main__":
    main()
