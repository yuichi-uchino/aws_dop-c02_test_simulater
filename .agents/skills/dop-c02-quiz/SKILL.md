---
name: dop-c02-quiz
description: Run an interactive DOP-C02 practice quiz from this repository's question bank when the user asks to practice or answer questions.
---

# DOP-C02 quiz

Use this skill to conduct a quiz in the Codex CLI conversation. Work from the repository root. The question bank is `questions/questions.json`; the helper is `scripts/quiz.py`.

1. Run `python3 scripts/quiz.py validate`. If it reports `0 問` or fails, explain what needs to be added or fixed and stop.
2. Run `python3 scripts/quiz.py draw`. Show only its `question` and `choices`. If the current client provides a selectable user-input tool, present the choices with it so the user can select an option in the UI. Otherwise, number them in their original order as `1. (A) ...`, `2. (B) ...` and wait for a text answer. Keep the `id` for grading; do not read or reveal the answer before the user responds.
3. Accept one number such as `1`, or multiple comma-separated numbers such as `1,3`. Choice letters such as `A,C` also work. Run `python3 scripts/quiz.py grade <id> <answer>`. If the answer format is invalid, request a valid choice without grading it.
4. Report correct or incorrect, the correct choice labels, and the explanation returned by the helper. Base the explanation on the stored answer; if adding context, clearly distinguish it from the question bank.
5. Ask whether to continue. For another question, run `draw` again with `--exclude <id>` for every question already shown in this session. When none remain, report completion. Do not repeat a question in the same session.

The helper performs random selection and exact-set grading. Do not select a question or judge an answer from memory. If the user asks for a standalone terminal quiz, point them to `python3 scripts/quiz.py play`.
