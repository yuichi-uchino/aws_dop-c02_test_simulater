---
name: dop-c02-quiz
description: Run an interactive DOP-C02 practice quiz from this repository's question bank when the user asks to practice or answer questions.
---

# DOP-C02 quiz

Use this skill to conduct a quiz in the Codex CLI conversation. Work from the repository root. The question bank is `questions/questions.json`; the helper is `scripts/quiz.py`.

1. Run `python3 scripts/quiz.py validate`. If it reports `0 問` or fails, explain what needs to be added or fixed and stop.
2. Run `python3 scripts/quiz.py draw` to select a question. For an explicit request for AWS official samples only, add `--source official`. The external HTML questions have a strong answer-length cue. After drawing, look up only the selected `id` in `questions/questions.json` to inspect its stored answers and explanation privately. Do not expose the answer before the user responds.
3. For external HTML questions, rewrite the displayed choices to remove answer-length and obviously absurd distractor cues. Keep the question, choice labels, number of correct answers, and intended correct set unchanged. Give every choice a similarly detailed, plausible AWS configuration or action; aim for comparable lengths without filler. Verify technical claims against current official AWS documentation when needed. Check every rewritten choice against the stored answer and explanation: each correct choice must remain correct, each distractor must remain incorrect, and no choice may introduce an additional valid answer. If a safe rewrite is not possible, skip that question and draw another, excluding the skipped `id` for this session. Clearly label rewritten choices as AI-adjusted; they are not verbatim source text. For official sample questions, preserve the original choices.
4. Show the selected `question` and displayed `choices` only. If the current client provides a selectable user-input tool, present the choices with it so the user can select an option in the UI. Otherwise, number them in their original order as `1. (A) ...`, `2. (B) ...` and wait for a text answer. Keep the `id` and displayed choice-to-label mapping for grading.
5. Accept one number such as `1`, or multiple comma-separated numbers such as `1,3`. Choice letters such as `A,C` also work. Run `python3 scripts/quiz.py grade <id> <answer>`. If the answer format is invalid, request a valid choice without grading it.
6. Report correct or incorrect, the correct choice labels, and the explanation returned by the helper. For rewritten choices, explain why the displayed distractors are wrong if the stored explanation does not address their new wording. Distinguish this added explanation from the question bank.
7. Ask whether to continue. For another question, run `draw` again with the same source option and `--exclude <id>` for every question already shown or skipped in this session. When none remain, report completion. Do not repeat a question in the same session.

The helper performs random selection and exact-set grading against the stored choice labels. Do not select a question or judge an answer from memory. The standalone Python `play` mode is deprecated because it does not rewrite choices; recommend this Codex skill for practice.
