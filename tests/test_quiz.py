import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "quiz.py"
QUESTIONS = [
    {
        "id": "one",
        "question": "単一選択の問題",
        "choices": {"A": "正解", "B": "不正解"},
        "answers": ["A"],
        "explanation": "A が正解です。",
    },
    {
        "id": "two",
        "question": "複数選択の問題",
        "choices": {"A": "正解1", "B": "不正解", "C": "正解2"},
        "answers": ["A", "C"],
        "explanation": "A と C が正解です。",
    },
]


class QuizCliTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.bank = Path(self.temp.name) / "questions.json"
        self.bank.write_text(json.dumps(QUESTIONS, ensure_ascii=False), encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def run_cli(self, *args, input_text=None):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--bank", str(self.bank), *args],
            input=input_text,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_draw_hides_answer_and_excludes_previous_question(self):
        result = self.run_cli("draw", "--exclude", "one")
        self.assertEqual(result.returncode, 0, result.stderr)
        question = json.loads(result.stdout)
        self.assertEqual(question["id"], "two")
        self.assertNotIn("answers", question)
        self.assertNotIn("explanation", question)

    def test_draw_official_source_excludes_other_questions(self):
        questions = [
            {**QUESTIONS[0], "source": "questions/upload/AWS-Certified-DevOps-Engineer-Professional_Sample-Questions.pdf"},
            {**QUESTIONS[1], "source": "questions/upload/sakitoo.com_dop-c02-mondaishu.html"},
        ]
        self.bank.write_text(json.dumps(questions, ensure_ascii=False), encoding="utf-8")
        result = self.run_cli("draw", "--source", "official")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["id"], "one")

    def test_multiple_answers_are_order_independent_and_exact(self):
        correct = self.run_cli("grade", "two", "C,A")
        numbered = self.run_cli("grade", "two", "3,1")
        partial = self.run_cli("grade", "two", "A")
        self.assertTrue(json.loads(correct.stdout)["correct"])
        self.assertTrue(json.loads(numbered.stdout)["correct"])
        self.assertFalse(json.loads(partial.stdout)["correct"])

    def test_invalid_bank_and_answer_fail(self):
        self.assertNotEqual(self.run_cli("grade", "one", "Z").returncode, 0)
        self.bank.write_text(json.dumps([QUESTIONS[0], QUESTIONS[0]]), encoding="utf-8")
        self.assertNotEqual(self.run_cli("validate").returncode, 0)

    def test_interactive_quiz_accepts_input_and_reports_score(self):
        result = self.run_cli("play", input_text="1\n\n1\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("非推奨", result.stderr)
        self.assertIn("正解:", result.stdout)
        self.assertIn("解説:", result.stdout)
        self.assertIn("結果:", result.stdout)


if __name__ == "__main__":
    unittest.main()
