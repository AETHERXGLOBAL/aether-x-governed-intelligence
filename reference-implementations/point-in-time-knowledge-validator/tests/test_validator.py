import copy
import importlib.util
import json
import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("ptk_validator", ROOT / "validator.py")
validator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)


def valid_envelope():
    with (ROOT / "examples" / "valid_envelope.json").open("r", encoding="utf-8") as handle:
        return json.load(handle)


class PointInTimeValidatorTests(unittest.TestCase):
    def codes(self, envelope):
        return {finding.code for finding in validator.validate_envelope(envelope)}

    def test_valid_envelope_passes(self):
        self.assertEqual(validator.validate_envelope(valid_envelope()), [])

    def test_source_retrieved_after_cutoff_is_rejected(self):
        envelope = valid_envelope()
        envelope["source_records"][0]["retrieved_at"] = "2026-08-17T20:16:00Z"
        self.assertIn("AX-PTK-FUTURE-SOURCE-RETRIEVAL", self.codes(envelope))

    def test_assertion_observed_after_cutoff_is_rejected(self):
        envelope = valid_envelope()
        envelope["knowledge_assertions"][0]["observed_at"] = "2026-08-17T20:16:00Z"
        self.assertIn("AX-PTK-FUTURE-ASSERTION-OBSERVED", self.codes(envelope))

    def test_unknown_source_reference_is_rejected(self):
        envelope = valid_envelope()
        envelope["knowledge_assertions"][0]["source_record_id"] = "src-missing"
        self.assertIn("AX-PTK-SOURCE-REFERENCE", self.codes(envelope))

    def test_null_value_requires_missing_state(self):
        envelope = valid_envelope()
        envelope["knowledge_assertions"][0]["value"] = None
        self.assertIn("AX-PTK-MISSING-STATE-REQUIRED", self.codes(envelope))

    def test_correction_requires_prior_assertion(self):
        envelope = valid_envelope()
        assertion = envelope["knowledge_assertions"][0]
        assertion["revision_kind"] = "CORRECTION"
        assertion.pop("supersedes", None)
        self.assertIn("AX-PTK-REVISION-SUPERSEDES-REQUIRED", self.codes(envelope))

    def test_unknown_supersedes_reference_is_rejected(self):
        envelope = valid_envelope()
        assertion = envelope["knowledge_assertions"][0]
        assertion["revision_kind"] = "CORRECTION"
        assertion["supersedes"] = "ka-missing"
        self.assertIn("AX-PTK-SUPERSEDES-REFERENCE", self.codes(envelope))

    def test_unknown_transformation_reference_is_rejected(self):
        envelope = valid_envelope()
        envelope["knowledge_assertions"][0]["transformation_references"] = ["tx-missing"]
        self.assertIn("AX-PTK-TRANSFORMATION-REFERENCE", self.codes(envelope))

    def test_reproducibility_cutoff_must_match_query_cutoff(self):
        envelope = valid_envelope()
        envelope["reproducibility_package"]["point_in_time_cutoff"] = "2026-08-17T20:14:00Z"
        self.assertIn("AX-PTK-REPRODUCIBILITY-CUTOFF", self.codes(envelope))


if __name__ == "__main__":
    unittest.main()
