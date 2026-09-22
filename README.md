# DOP-C02 Test Simulator

AWS Certified DevOps Engineer – Professional（DOP-C02）の問題集を使って、CLI で練習するためのリポジトリです。`questions/questions.json` には、AWS のサンプル PDF から10問、`questions/upload/sakitoo.com_dop-c02-mondaishu.html` から120問の計130問を登録しています。各問題の `source` に元ファイルを記録しています。

外部HTML由来の単一選択120問では、119問で正解が唯一の最長選択肢です。Codexの対話クイズでは出題時に選択肢の長さや明らかに誤りと分かる表現を調整して表示します。調整後の選択肢はAIによる改変であり、元ファイルの原文ではありません。AWS公式サンプルだけで練習したい場合はその旨を指定してください。

## 問題を登録する

`questions/questions.json` に問題の配列を追加します。1問の形式は次のとおりです。正解が複数ある場合は `answers` にすべて指定します。

```json
[
  {
    "id": "dop-c02-001",
    "question": "ここに問題文を入力",
    "choices": {
      "A": "選択肢 A",
      "B": "選択肢 B"
    },
    "answers": ["A"],
    "explanation": "ここに正解の理由を入力"
  }
]
```

問題集の原文を別の形式で受け取った場合は、内容を確認してからこの JSON 形式に変換してください。問題文、選択肢、正解、解説を推測で補わないでください。

## AI と対話して練習する

このリポジトリで Codex CLI を起動し、`$dop-c02-quiz` と入力してください。AI がランダムに問題を出し、回答を待ってから採点・解説します。外部HTML由来の問題は、正誤を維持したまま選択肢を調整して出題します。利用中のクライアントに選択 UI がある場合はそれを使い、ない場合は番号付きで表示して `1` や `1,3` のように回答を受け付けます。出題と採点には `scripts/quiz.py` を内部で使用します。スキルの手順は `.agents/skills/dop-c02-quiz/SKILL.md` にあります。

## CLI ヘルパー

Python 3 の標準ライブラリだけで動くヘルパーは、問題集の検証とCodexスキルからの出題・採点に使用します。`play` は選択肢の偏りを調整できないため非推奨です。練習には `$dop-c02-quiz` を使用してください。

```bash
python3 scripts/quiz.py validate  # 問題集を検証
python3 -m unittest discover -s tests  # CLI のテスト
```
