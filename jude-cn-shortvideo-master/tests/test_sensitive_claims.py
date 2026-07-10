import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SCANNER = SKILL_DIR / "scripts" / "audit_sensitive_claims.py"


class SensitiveClaimsAuditTest(unittest.TestCase):
    def run_scan(self, content: str):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.md"
            path.write_text(content, encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(SCANNER), str(path)],
                capture_output=True,
                text=True,
                check=False,
            )

    def test_safeguard_lists_do_not_fail_the_scan(self):
        result = self.run_scan(
            "- 不说保证、绝对、永久、无痕、零风险。\n"
            "- 不展示患者、病历、聊天记录、付款信息。\n"
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Safeguard-only lines: 2", result.stdout)
        self.assertIn("Total findings: 0", result.stdout)

    def test_real_promises_and_privacy_exposure_still_fail(self):
        result = self.run_scan("保证一次修好，恢复快。这里展示患者病历和付款信息。\n")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("[absolute_or_promise]", result.stdout)
        self.assertIn("[privacy]", result.stdout)

    def test_unrelated_negative_word_does_not_hide_a_promise(self):
        result = self.run_scan("不要担心，保证恢复快。\n")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("[absolute_or_promise]", result.stdout)


if __name__ == "__main__":
    unittest.main()
