import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "learning_ledger.py"
SPEC = importlib.util.spec_from_file_location("learning_ledger", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def event(**overrides):
    payload = {
        "date": "2026-09-13",
        "experiment": "Test a bilingual audit offer",
        "hypothesis": "Buyers value evidence before strategy",
        "expected_signal": "Three qualified replies",
        "observed_signal": 1,
        "evidence": "Four replies and two discovery calls",
        "decision": "continue",
        "lesson": "Lead with the audit",
        "tags": ["Bilingual", "audit"],
    }
    payload.update(overrides)
    return payload


class LearningLedgerTests(unittest.TestCase):
    def test_append_is_deterministic_and_preserves_raw_event(self):
        updated = MODULE.append_event(MODULE.new_ledger(), event())
        self.assertEqual(len(updated["events"]), 1)
        self.assertEqual(updated["events"][0]["observed_signal"], 1)
        self.assertEqual(updated["events"][0]["tags"], ["audit", "bilingual"])
        self.assertEqual(len(updated["events"][0]["event_id"]), 16)

    def test_duplicate_event_is_rejected(self):
        updated = MODULE.append_event(MODULE.new_ledger(), event())
        with self.assertRaisesRegex(ValueError, "duplicate event"):
            MODULE.append_event(updated, event())

    def test_invalid_signal_and_decision_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "-2 to 2"):
            MODULE.validate_event(event(observed_signal=3))
        with self.assertRaisesRegex(ValueError, "continue, adjust, or stop"):
            MODULE.validate_event(event(decision="scale"))

    def test_summary_keeps_only_recurring_tags(self):
        ledger = MODULE.append_event(MODULE.new_ledger(), event())
        ledger = MODULE.append_event(
            ledger,
            event(
                date="2026-09-14",
                experiment="Test the same offer with educators",
                evidence="Two qualified replies",
                lesson="Educators asked for examples",
                tags=["audit", "education"],
            ),
        )
        result = MODULE.summarize(ledger)
        self.assertEqual(result["event_count"], 2)
        self.assertEqual(result["net_observed_signal"], 2)
        self.assertEqual(result["recurring_tags"], [{"tag": "audit", "events": 2}])


if __name__ == "__main__":
    unittest.main()
