#!/usr/bin/env python3
"""CLI quiz and deterministic grading for the DOP-C02 question bank."""

import argparse
import json
import random
import sys
from pathlib import Path


DEFAULT_BANK = Path(__file__).resolve().parents[1] / "questions" / "questions.json"
OFFICIAL_SAMPLE_SOURCE = "questions/upload/AWS-Certified-DevOps-Engineer-Professional_Sample-Questions.pdf"


def load_questions(path):
    try:
        questions = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"問題集を読み込めません: {exc}") from exc
    if not isinstance(questions, list):
        raise ValueError("問題集の最上位は配列にしてください")
    seen = set()
    for number, item in enumerate(questions, 1):
        if not isinstance(item, dict):
            raise ValueError(f"{number}問目はオブジェクトにしてください")
        qid = item.get("id")
        choices = item.get("choices")
        answers = item.get("answers")
        if not isinstance(qid, str) or not qid.strip() or qid in seen:
            raise ValueError(f"{number}問目の id が空または重複しています")
        seen.add(qid)
        if not isinstance(item.get("question"), str) or not item["question"].strip():
            raise ValueError(f"{qid}: question が必要です")
        if not isinstance(choices, dict) or len(choices) < 2 or any(
            not isinstance(k, str) or len(k) != 1 or k not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            or not isinstance(v, str) or not v.strip() for k, v in choices.items()
        ):
            raise ValueError(f"{qid}: choices に A, B などの選択肢を2つ以上指定してください")
        if not isinstance(answers, list) or not answers or any(
            not isinstance(a, str) or a not in choices for a in answers
        ) or len(set(answers)) != len(answers):
            raise ValueError(f"{qid}: answers に重複のない正解記号を指定してください")
        if not isinstance(item.get("explanation"), str) or not item["explanation"].strip():
            raise ValueError(f"{qid}: explanation が必要です")
    return questions


def grade(question, raw_answer):
    labels = list(question["choices"])
    answer = []
    for part in raw_answer.split(","):
        token = part.strip().upper()
        if token.isdecimal() and 1 <= int(token) <= len(labels):
            token = labels[int(token) - 1]
        answer.append(token)
    if len(set(answer)) != len(answer) or any(part not in question["choices"] for part in answer):
        raise ValueError("回答は 1 または 1,3 の形式で入力してください（A などの記号も可）")
    return {
        "id": question["id"],
        "correct": set(answer) == set(question["answers"]),
        "answers": question["answers"],
        "explanation": question["explanation"],
    }


def play(questions):
    remaining = questions[:]
    random.SystemRandom().shuffle(remaining)
    score = 0
    total = 0
    while remaining:
        item = remaining.pop()
        print(f"\n問題 {total + 1}: {item['question']}")
        for number, (label, choice) in enumerate(item["choices"].items(), 1):
            print(f"  {number}. ({label}) {choice}")
        while True:
            try:
                raw = input("回答（1 または 1,3 / q で終了）> ").strip()
                if raw.lower() == "q":
                    print(f"結果: {score}/{total} 問正解")
                    return
                result = grade(item, raw)
                break
            except ValueError as exc:
                print(exc)
            except EOFError:
                print()
                return
        total += 1
        score += result["correct"]
        print("正解です。" if result["correct"] else "不正解です。")
        print(f"正解: {', '.join(result['answers'])}")
        print(f"解説: {result['explanation']}")
        if remaining:
            try:
                if input("次の問題へ？ [Enter: 続ける / q: 終了] > ").strip().lower() == "q":
                    break
            except EOFError:
                print()
                break
    print(f"結果: {score}/{total} 問正解")


def select_source(questions, source):
    if source == "official":
        return [item for item in questions if item.get("source") == OFFICIAL_SAMPLE_SOURCE]
    return questions


def main():
    parser = argparse.ArgumentParser(description="DOP-C02 問題集 CLI")
    parser.add_argument("--bank", type=Path, default=DEFAULT_BANK, help="問題集 JSON ファイル")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("validate", help="問題集を検証")
    play_command = commands.add_parser("play", help="非推奨: 元の選択肢で対話形式の出題")
    play_command.add_argument("--source", choices=("all", "official"), default="all")
    draw = commands.add_parser("draw", help="ランダムな問題を JSON で出力")
    draw.add_argument("--source", choices=("all", "official"), default="all")
    draw.add_argument("--exclude", action="append", default=[], help="出題済み ID")
    check = commands.add_parser("grade", help="回答を採点して JSON で出力")
    check.add_argument("id", help="問題 ID")
    check.add_argument("answer", help="回答番号または記号。複数は 1,3 または A,C")
    args = parser.parse_args()
    try:
        questions = load_questions(args.bank)
        if args.command == "validate":
            print(f"{len(questions)} 問を検証しました")
        elif not questions:
            raise ValueError("問題がありません。questions/questions.json に問題を追加してください")
        elif args.command == "play":
            selected = select_source(questions, args.source)
            if not selected:
                raise ValueError("指定した出典の問題がありません")
            print(
                "注意: Python の play モードは非推奨です。選択肢を調整できないため、"
                "Codex の $dop-c02-quiz を使用してください。",
                file=sys.stderr,
            )
            play(selected)
        elif args.command == "draw":
            available = [q for q in select_source(questions, args.source) if q["id"] not in args.exclude]
            if not available:
                raise ValueError("未出題の問題がありません")
            item = random.SystemRandom().choice(available)
            print(json.dumps({k: item[k] for k in ("id", "question", "choices")}, ensure_ascii=False))
        else:
            item = next((q for q in questions if q["id"] == args.id), None)
            if item is None:
                raise ValueError(f"問題 ID が見つかりません: {args.id}")
            print(json.dumps(grade(item, args.answer), ensure_ascii=False))
    except ValueError as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
