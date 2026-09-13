import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "score_profile.py"
SPEC = importlib.util.spec_from_file_location("score_profile", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def payload(axis_value=5, risk_value=0):
    return {
        "axes": {key: axis_value for key in MODULE.AXES},
        "risks": {key: risk_value for key in MODULE.RISKS},
    }


class ScoreProfileTests(unittest.TestCase):
    def test_full_profile_scores_100(self):
        result = MODULE.score_profile(payload())
        self.assertEqual(result["score"], 100.0)
        self.assertEqual(result["stage"], "复利")
        self.assertEqual(result["stage_en"], "Compound")

    def test_maximum_risks_deduct_20(self):
        result = MODULE.score_profile(payload(risk_value=5))
        self.assertEqual(result["risk_deduction"], 20.0)
        self.assertEqual(result["score"], 80.0)

    def test_low_profile_is_floor_stage(self):
        result = MODULE.score_profile(payload(axis_value=0))
        self.assertEqual(result["score"], 0.0)
        self.assertEqual(result["stage"], "打底")
        self.assertEqual(result["stage_en"], "Foundation")

    def test_rejects_out_of_range_values(self):
        data = payload()
        data["axes"]["global_demand"] = 6
        with self.assertRaisesRegex(ValueError, "between 0 and 5"):
            MODULE.score_profile(data)

    def test_rejects_missing_fields(self):
        data = payload()
        del data["risks"]["capacity_burnout"]
        with self.assertRaisesRegex(ValueError, "missing required fields"):
            MODULE.score_profile(data)


if __name__ == "__main__":
    unittest.main()
