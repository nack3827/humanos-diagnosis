from datetime import datetime, timedelta
from typing import List, Dict, Any
import math
import random
from models import (
    HumanOSDiagnosisInput, 
    HumanOSDiagnosisOutput, 
    HumanOSAnalysis,
    SystemStructure,
    SystemBug,
    ImprovementProposal,
    ConditionType,
    ThoughtPattern
)


class HumanOSDiagnosisEngine:
    """
    HumanOS診断エンジン
    人間の状態をOSのように分析し、構造、バグ、改善提案を生成する
    """
    
    def __init__(self):
        self.condition_weights = {
            ConditionType.HEALTHY: 0.9,
            ConditionType.BALANCED: 0.85,
            ConditionType.STRESSED: 0.6,
            ConditionType.ANXIOUS: 0.5,
            ConditionType.DEPRESSED: 0.4,
            ConditionType.EXHAUSTED: 0.3,
            ConditionType.CONFUSED: 0.45
        }
        
        self.thought_pattern_impacts = {
            ThoughtPattern.ANALYTICAL: {"cognitive": 0.8, "emotional": 0.6},
            ThoughtPattern.CREATIVE: {"cognitive": 0.7, "emotional": 0.8},
            ThoughtPattern.INTUITIVE: {"cognitive": 0.6, "emotional": 0.9},
            ThoughtPattern.LOGICAL: {"cognitive": 0.9, "emotional": 0.5},
            ThoughtPattern.EMOTIONAL: {"cognitive": 0.5, "emotional": 0.9},
            ThoughtPattern.SYSTEMATIC: {"cognitive": 0.8, "emotional": 0.7},
            ThoughtPattern.CHAOTIC: {"cognitive": 0.4, "emotional": 0.6}
        }

    def calculate_age_factor(self, birth_date: datetime) -> float:
        """年齢要因を計算"""
        today = datetime.now()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        
        if age < 25:
            return 0.8  # 若さのエネルギー
        elif age < 35:
            return 0.9  # ピーク性能
        elif age < 50:
            return 0.85  # 安定期
        elif age < 65:
            return 0.75  # 経験と知恵
        else:
            return 0.7  # 円熟期

    def analyze_body_logs(self, body_logs: List) -> Dict[str, float]:
        """身体ログを分析"""
        if not body_logs:
            return {"physical": 0.7, "stability": 0.7}
        
        recent_logs = body_logs[-5:] if len(body_logs) > 5 else body_logs
        
        heart_rates = [log.heart_rate for log in recent_logs if log.heart_rate]
        stress_levels = [log.stress_level for log in recent_logs if log.stress_level]
        sleep_hours = [log.sleep_hours for log in recent_logs if log.sleep_hours]
        
        physical_score = 0.7
        stability_score = 0.7
        
        if heart_rates:
            avg_hr = sum(heart_rates) / len(heart_rates)
            if 60 <= avg_hr <= 80:
                physical_score += 0.1
            elif avg_hr > 90:
                stability_score -= 0.2
        
        if stress_levels:
            avg_stress = sum(stress_levels) / len(stress_levels)
            if avg_stress <= 3:
                stability_score += 0.2
            elif avg_stress >= 7:
                stability_score -= 0.3
        
        if sleep_hours:
            avg_sleep = sum(sleep_hours) / len(sleep_hours)
            if 7 <= avg_sleep <= 9:
                physical_score += 0.2
            elif avg_sleep < 6:
                physical_score -= 0.2
        
        return {
            "physical": max(0.0, min(1.0, physical_score)),
            "stability": max(0.0, min(1.0, stability_score))
        }

    def analyze_mental_state(self, mental_state) -> Dict[str, float]:
        """精神状態を分析"""
        scores = []
        
        if mental_state.mood is not None:
            scores.append(mental_state.mood / 10.0)
        if mental_state.energy_level is not None:
            scores.append(mental_state.energy_level / 10.0)
        if mental_state.focus_level is not None:
            scores.append(mental_state.focus_level / 10.0)
        if mental_state.emotional_stability is not None:
            scores.append(mental_state.emotional_stability / 10.0)
        if mental_state.self_esteem is not None:
            scores.append(mental_state.self_esteem / 10.0)
        
        if mental_state.anxiety_level is not None:
            scores.append((10 - mental_state.anxiety_level) / 10.0)
        
        avg_score = sum(scores) / len(scores) if scores else 0.7
        
        return {
            "mental": avg_score,
            "emotional": (mental_state.mood or 7) / 10.0 if mental_state.mood else 0.7
        }

    def generate_system_structure(self, input_data: HumanOSDiagnosisInput, scores: Dict[str, float]) -> SystemStructure:
        """システム構造を生成"""
        age_factor = self.calculate_age_factor(input_data.birth_date)
        condition_score = self.condition_weights.get(input_data.condition, 0.7)
        
        # 思考パターンの影響を計算
        cognitive_impact = 0.7
        emotional_impact = 0.7
        for pattern in input_data.thought_patterns:
            impacts = self.thought_pattern_impacts.get(pattern, {"cognitive": 0.7, "emotional": 0.7})
            cognitive_impact = (cognitive_impact + impacts["cognitive"]) / 2
            emotional_impact = (emotional_impact + impacts["emotional"]) / 2
        
        core_score = (condition_score * age_factor * 0.8 + scores.get("physical", 0.7) * 0.2)
        
        return SystemStructure(
            core_system=self._describe_system_state(core_score, "コア"),
            cognitive_system=self._describe_system_state(cognitive_impact * core_score, "認知"),
            emotional_system=self._describe_system_state(emotional_impact * scores.get("emotional", 0.7), "感情"),
            physical_system=self._describe_system_state(scores.get("physical", 0.7) * age_factor, "身体"),
            social_system=self._describe_system_state(0.7, "社会")
        )

    def _describe_system_state(self, score: float, system_type: str) -> str:
        """システム状態を記述"""
        if score >= 0.8:
            return f"{system_type}システムは最適化されており、安定した稼働を維持しています。リソース配分が効率的で、パフォーマンスが高い状態です。"
        elif score >= 0.6:
            return f"{system_type}システムは正常に機能していますが、若干の最適化余地があります。全体的には安定していますが、ピーク性能を発揮するには調整が必要です。"
        elif score >= 0.4:
            return f"{system_type}システムに軽度の不具合が見られます。動作は続いていますが、パフォーマンスの低下や不安定性が確認されます。早急なメンテナンスが推奨されます。"
        else:
            return f"{system_type}システムは深刻な状態です。システム障害のリスクが高く、全面的な診断と修復が必要です。機能不全に陥る可能性があります。"

    def identify_bugs(self, input_data: HumanOSDiagnosisInput, scores: Dict[str, float]) -> List[SystemBug]:
        """システムバグを特定"""
        bugs = []
        
        # 状態に基づくバグ
        if input_data.condition == ConditionType.STRESSED:
            bugs.append(SystemBug(
                category="ストレス応答システム",
                severity="medium",
                description="コルチゾール・リズムの異常検出。ストレス応答が過剰に作動し、リソースを過剰消費しています。",
                impact="パフォーマンス低下、免疫システムの抑制、記憶機能の障害",
                potential_cause="長期的なストレス暴露、睡眠不足、ワークライフバランスの崩壊"
            ))
        
        if input_data.condition == ConditionType.ANXIOUS:
            bugs.append(SystemBug(
                category="不安検出システム",
                severity="high",
                description="扁桃体の過剰作動。危険予測アルゴリズムが誤作動し、過剰な警報を発しています。",
                impact="意思決定の麻痺、社会的回避、睡眠障害",
                potential_cause="過去のトラウマ、認知の歪み、神経伝達物質の不均衡"
            ))
        
        if input_data.condition == ConditionType.DEPRESSED:
            bugs.append(SystemBug(
                category="報酬システム",
                severity="critical",
                description="ドーパミン受容体の感受性低下。報酬予測エラーが頻発し、モチベーションシステムが機能不全に陥っています。",
                impact="意欲低下、快感消失症、社会機能の障害",
                potential_cause="慢性的なストレス、遺伝的要因、神経炎症"
            ))
        
        if input_data.condition == ConditionType.EXHAUSTED:
            bugs.append(SystemBug(
                category="エネルギー管理システム",
                severity="high",
                description="ミトコンドリア効率の大幅な低下。ATP生成が最適レベルの40%程度にまで落ち込んでいます。",
                impact="全身的な倦怠感、認知機能の低下、免疫機能の抑制",
                potential_cause="慢性的な睡眠不足、栄養不足、過度な精神的・身体的負荷"
            ))
        
        # 身体ログに基づくバグ
        if input_data.body_logs:
            recent_logs = input_data.body_logs[-3:]
            high_stress_count = sum(1 for log in recent_logs if log.stress_level and log.stress_level >= 7)
            
            if high_stress_count >= 2:
                bugs.append(SystemBug(
                    category="自律神経システム",
                    severity="medium",
                    description="交感神経と副交感神経のバランス崩壊。恒常性維持メカニズムに異常が検出されました。",
                    impact="心拍数の不安定化、消化機能の低下、睡眠の質の悪化",
                    potential_cause="慢性的なストレス、不規則な生活リズム、運動不足"
                ))
        
        # 精神状態に基づくバグ
        mental = input_data.mental_state
        if mental.anxiety_level and mental.anxiety_level >= 8:
            bugs.append(SystemBug(
                category="認知制御システム",
                severity="medium",
                description="前頭前野の実行機能が低下。感情制御と認知柔軟性に問題が検出されています。",
                impact="集中力の低下、衝動制御の困難、問題解決能力の低下",
                potential_cause="過度な不安、睡眠不足、栄養不均衡"
            ))
        
        return bugs

    def generate_improvements(self, input_data: HumanOSDiagnosisInput, bugs: List[SystemBug]) -> List[ImprovementProposal]:
        """改善提案を生成"""
        proposals = []
        
        # 基本的な改善提案
        proposals.append(ImprovementProposal(
            category="システム最適化",
            priority="high",
            action="睡眠サイクルの正規化：毎日7-9時間の質の高い睡眠を確保し、就寝・起床時間を一定に保つ",
            expected_outcome="メモリ Consolidation の向上、免疫システムの強化、認知パフォーマンスの20-30%向上",
            implementation_difficulty="medium"
        ))
        
        proposals.append(ImprovementProposal(
            category="栄養システム",
            priority="high",
            action="抗炎症食の導入：オメガ3脂肪酸、抗酸化物質、複合炭水化物をバランス良く摂取",
            expected_outcome="神経炎症の抑制、エネルギー生産効率の向上、気分安定性の改善",
            implementation_difficulty="easy"
        ))
        
        # 状態特異的改善提案
        if input_data.condition in [ConditionType.STRESSED, ConditionType.ANXIOUS]:
            proposals.append(ImprovementProposal(
                category="ストレス管理システム",
                priority="urgent",
                action="マインドフルネス瞑想の実践：毎日10-20分の呼吸瞑想を継続的に行う",
                expected_outcome="扁桃体の過剰作動の抑制、コルチゾールレベルの正常化、感情制御能力の向上",
                implementation_difficulty="easy"
            ))
            
            proposals.append(ImprovementProposal(
                category="運動システム",
                priority="medium",
                action="有酸素運動の定期的実施：週3回、30分の中強度有酸素運動（ウォーキング、ジョギング等）",
                expected_outcome="エンドルフィン分泌の促進、神経新生の促進、ストレス耐性の向上",
                implementation_difficulty="medium"
            ))
        
        if input_data.condition == ConditionType.DEPRESSED:
            proposals.append(ImprovementProposal(
                category="報酬システム再構築",
                priority="urgent",
                action="行動活性化療法：小さな達成可能な目標を設定し、成功体験を積み重ねる",
                expected_outcome="ドーパミン受容体の感受性回復、報酬システムの再 calibration、意欲の回復",
                implementation_difficulty="medium"
            ))
        
        if input_data.condition == ConditionType.EXHAUSTED:
            proposals.append(ImprovementProposal(
                category="エネルギー最適化",
                priority="critical",
                action="デジタルデトックス：情報入力を制限し、脳の休息時間を確保する",
                expected_outcome="認知リソースの回復、注意力の向上、創造性の回復",
                implementation_difficulty="medium"
            ))
        
        # 思考パターンに基づく提案
        if ThoughtPattern.ANALYTICAL in input_data.thought_patterns:
            proposals.append(ImprovementProposal(
                category="認知柔軟性向上",
                priority="medium",
                action="創造的活動の導入：論理的思考以外の活動（芸術、音楽、自然散策等）を取り入れる",
                expected_outcome="脳の多様な領域の活性化、創造的問題解決能力の向上、バランスの取れた思考",
                implementation_difficulty="easy"
            ))
        
        return proposals

    def calculate_overall_score(self, input_data: HumanOSDiagnosisInput, scores: Dict[str, float]) -> float:
        """総合スコアを計算"""
        age_factor = self.calculate_age_factor(input_data.birth_date)
        condition_score = self.condition_weights.get(input_data.condition, 0.7)
        
        # 各要素の重み付け
        weights = {
            "condition": 0.3,
            "physical": 0.2,
            "mental": 0.25,
            "age": 0.1,
            "stability": 0.15
        }
        
        weighted_score = (
            condition_score * weights["condition"] +
            scores.get("physical", 0.7) * weights["physical"] +
            scores.get("mental", 0.7) * weights["mental"] +
            age_factor * weights["age"] +
            scores.get("stability", 0.7) * weights["stability"]
        )
        
        return round(weighted_score * 100, 1)

    def generate_analysis(self, input_data: HumanOSDiagnosisInput, scores: Dict[str, float]) -> HumanOSAnalysis:
        """分析を生成"""
        overall_score = self.calculate_overall_score(input_data, scores)
        system_structure = self.generate_system_structure(input_data, scores)
        
        # 強みの特定
        strengths = []
        if scores.get("physical", 0) >= 0.7:
            strengths.append("身体システムが安定しており、高い身体的耐性を維持しています")
        if scores.get("mental", 0) >= 0.7:
            strengths.append("精神的回復力が高く、ストレスへの適応能力に優れています")
        if input_data.condition == ConditionType.HEALTHY:
            strengths.append("全体的なシステムバランスが取れており、最適な状態にあります")
        
        if not strengths:
            strengths.append("改善のポテンシャルが高く、適切な介入による回復可能性が大きいです")
        
        # 弱みの特定
        weaknesses = []
        if input_data.condition in [ConditionType.STRESSED, ConditionType.ANXIOUS, ConditionType.DEPRESSED]:
            weaknesses.append("ストレス応答システムに過負荷がかかっており、リセットが必要です")
        if scores.get("stability", 0) < 0.6:
            weaknesses.append("システムの安定性が低下しており、外部要因による影響を受けやすい状態です")
        if input_data.condition == ConditionType.EXHAUSTED:
            weaknesses.append("エネルギーリソースが枯渇しており、システム全体のパフォーマンスが低下しています")
        
        # パターンの特定
        patterns = []
        if ThoughtPattern.ANALYTICAL in input_data.thought_patterns:
            patterns.append("論理的・分析的思考パターンが強く、複雑な問題解決に適しています")
        if ThoughtPattern.EMOTIONAL in input_data.thought_patterns:
            patterns.append("感情的知性が高く、他者との共感や社会的つながりを重視する傾向があります")
        if len(input_data.thought_patterns) > 2:
            patterns.append("多様な思考パターンを持ち合わせており、状況に応じた柔軟な対応が可能です")
        
        return HumanOSAnalysis(
            overall_score=overall_score,
            system_structure=system_structure,
            strengths=strengths,
            weaknesses=weaknesses,
            patterns=patterns
        )

    def generate_summary(self, analysis: HumanOSAnalysis, bugs: List[SystemBug]) -> str:
        """要約を生成"""
        score = analysis.overall_score
        
        if score >= 80:
            status = "優秀"
            status_desc = "あなたのHumanOSは非常に良好な状態です。システム全体が効率的に稼働しており、高いパフォーマンスを維持しています。"
        elif score >= 60:
            status = "良好"
            status_desc = "あなたのHumanOSは安定した状態にありますが、いくつかの最適化ポイントが見つかりました。"
        elif score >= 40:
            status = "要注意"
            status_desc = "あなたのHumanOSにはいくつかの懸念事項があります。早めの対処が推奨されます。"
        else:
            status = "要介入"
            status_desc = "あなたのHumanOSは支援が必要な状態です。専門的なサポートと集中的なケアが必要です。"
        
        critical_bugs = [bug for bug in bugs if bug.severity == "critical"]
        high_bugs = [bug for bug in bugs if bug.severity == "high"]
        
        bug_summary = ""
        if critical_bugs:
            bug_summary = f"特に{len(critical_bugs)}件の深刻なシステム障害が検出されており、緊急の対応が必要です。"
        elif high_bugs:
            bug_summary = f"{len(high_bugs)}件の高優先度の問題が確認されました。"
        
        summary = f"""
HumanOS診断レポート - 総合評価：{status}（{score:.1f}/100点）

{status_desc}{bug_summary}

システム構造の面では、{analysis.system_structure.core_system.lower()}また、{len(analysis.strengths)}つの強みと{len(analysis.weaknesses)}つの改善分野が特定されました。

今回の診断で検出された{len(bugs)}件のシステムバグに対して、具体的な修復プランと{len(analysis.patterns)}つの行動パターンの最適化提案を提示します。
        """.strip()
        
        return summary

    def generate_recommendations(self, analysis: HumanOSAnalysis, bugs: List[SystemBug]) -> List[str]:
        """推奨事項を生成"""
        recommendations = []
        
        # スコアに基づく推奨
        if analysis.overall_score < 50:
            recommendations.append("専門家（医療機関、カウンセラー等）への相談を強く推奨します")
            recommendations.append("日常生活の負担を軽減し、回復に専念できる環境を整えてください")
        
        # バグに基づく推奨
        critical_bugs = [bug for bug in bugs if bug.severity == "critical"]
        if critical_bugs:
            recommendations.append("深刻なシステム障害が検出されたため、直ちに対処が必要です")
        
        # 一般的推奨
        recommendations.extend([
            "定期的なシステムチェック（自己観察）を習慣化してください",
            "小さな成功体験を積み重ね、報酬システムを再活性化してください",
            "信頼できる人との対話を通じて、社会システムのメンテナンスを行ってください"
        ])
        
        return recommendations

    def diagnose(self, input_data: HumanOSDiagnosisInput) -> HumanOSDiagnosisOutput:
        """HumanOS診断を実行"""
        # 各種スコアを計算
        body_scores = self.analyze_body_logs(input_data.body_logs)
        mental_scores = self.analyze_mental_state(input_data.mental_state)
        
        scores = {
            "physical": body_scores.get("physical", 0.7),
            "stability": body_scores.get("stability", 0.7),
            "mental": mental_scores.get("mental", 0.7),
            "emotional": mental_scores.get("emotional", 0.7)
        }
        
        # 分析を生成
        analysis = self.generate_analysis(input_data, scores)
        
        # バグを特定
        bugs = self.identify_bugs(input_data, scores)
        
        # 改善提案を生成
        improvements = self.generate_improvements(input_data, bugs)
        
        # 要約と推奨事項を生成
        summary = self.generate_summary(analysis, bugs)
        recommendations = self.generate_recommendations(analysis, bugs)
        
        return HumanOSDiagnosisOutput(
       analysis=analysis,
        bugs=bugs,
        improvement_proposals=improvements,
        summary=summary,
        recommendations=recommendations,
        created_at=datetime.now()
)
