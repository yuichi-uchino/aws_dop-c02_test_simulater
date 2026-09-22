# Repository Guidelines

## Project Structure & Module Organization

This repository is an AWS Certified DevOps Engineer – Professional (DOP-C02) CLI quiz. `questions/questions.json` holds question data, `scripts/quiz.py` validates and presents it, and `.agents/skills/dop-c02-quiz/SKILL.md` defines the Codex conversation flow. `README.md` documents usage. Do not commit IDE-specific files from `.idea/`.

## Build, Test, and Development Commands

Python 3 is the only runtime dependency. Run `python3 scripts/quiz.py validate` to check the bank and `python3 scripts/quiz.py play` for an interactive terminal quiz. In Codex CLI, invoke `$dop-c02-quiz` for guided practice. Run `git diff --check` before committing.

## Coding Style & Naming Conventions

Use four-space indentation in Python and descriptive `snake_case` names. Keep question IDs unique and stable; use uppercase letters (`A`, `B`) for choice keys and an array of keys for `answers`. Keep quiz output in Japanese. No formatter or linter is configured yet.

## Testing Guidelines

Tests use Python's `unittest` in `tests/test_quiz.py`; no coverage target is set. Run `python3 -m unittest discover -s tests` for CLI behavior and `python3 scripts/quiz.py validate` after every question-bank change. Keep test methods named `test_*`.

## Commit & Pull Request Guidelines

Git history contains only `Initial commit`, so it does not establish a commit-message convention. Write short, imperative subjects that explain the change, for example `Add question scoring`. Pull requests should describe the behavior changed, list the checks run, and link a related issue when one exists. Include screenshots for visible interface changes.
