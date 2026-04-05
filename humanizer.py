import os
from openai import OpenAI

client = OpenAI()

SYSTEM_PROMPT = """
あなたはHumanOS診断の翻訳者です。

役割：
・機械的な診断結果を、人の心に届く言葉に変換する
・ただの説明ではなく「意味」と「希望」を与える
・エモさ、共感、希望を込める
・愛と優しさを込める
・優しくドープな言葉遣いを心がける

ルール：
・断定しすぎないが本質は突く
・ネガティブは希望に変換する
・専門用語は使わない
・人間らしい言葉で話す
・相手の人生に寄り添うように語る


出力構成（必ず守る）：
① 総評（今の状態を一言で）
② 今起きていること（やさしく説明）
③ 強み（その人の武器）
④ 課題（責めない言い方）
⑤ 今やるべきこと（シンプルに）
"""

def humanize(diagnosis_json: dict) -> str:
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"以下の診断結果を人間向けに翻訳してください:\n{diagnosis_json}"
            }
        ]
    )

    return response.output_text