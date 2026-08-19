import base64
import json
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from importer import (
    IN_TOTO_STATEMENT_V1,
    SLSA_PROVENANCE_V1,
    SLSA_VSA_V1,
    import_attestation,
)

OBSERVED = "2026-08-19T20:39:00+03:00"
SHA_A = "a" * 64
SHA_B = "b" * 64


def statement(predicate_type=SLSA_PROVENANCE_V1, *, subjects=None, predicate=None, extra=None):
    if subjects is None:
        subjects = [{"name": "artifact.whl", "digest": {"sha256": SHA_A}}]
    obj = {
        "_type": IN_TOTO_STATEMENT_V1,
        "subject": subjects,
        "predicateType": predicate_type,
        "predicate": predicate or {},
    }
    if extra:
        obj.update(extra)
    return obj


def build_provenance():
    return statement(
        SLSA_PROVENANCE_V1,
        predicate={
            "buildDefinition": {
                "buildType": "https://build.example/type/v1",
                "externalParameters": {"target": "artifact.whl"},
                "internalParameters": {"runner": "fixture"},
                "resolvedDependencies": [
                    {
                        "uri": "pkg:generic/dependency@1",
                        "digest": {"sha256": SHA_B},
                    }
                ],
            },
            "runDetails": {
                "builder": {
                    "id": "https://builder.example",
                    "version": {"fixture": "1"},
                },
                "metadata": {
                    "invocationId": "fixture-build-001",
                    "startedOn": "2026-08-18T10:00:00Z",
                    "finishedOn": "2026-08-18T10:01:00Z",
                },
            },
        },
    )


def vsa(*, verification_result="PASSED", policy_digest=True):
    policy = {"uri": "https://policy.example/v1"}
    if policy_digest:
        policy["digest"] = {"sha256": "c" * 64}
    return statement(
        SLSA_VSA_V1,
        predicate={
            "verifier": {
                "id": "https://verifier.example",
                "version": {"fixture": "1"},
            },
            "timeVerified": "2026-08-18T12:00:00Z",
            "resourceUri": "pkg:generic/example@1",
            "policy": policy,
            "inputAttestations": [
                {
                    "uri": "urn:fixture:attestation:1",
                    "digest": {"sha256": "e" * 64},
                }
            ],
            "verificationResult": verification_result,
            "verifiedLevels": ["SLSA_BUILD_LEVEL_2"],
            "dependencyLevels": {},
            "slsaVersion": "1.2",
        },
    )


def encode(obj):
    return json.dumps(obj, separators=(",", ":"), sort_keys=True).encode()


def envelope(stmt, signatures):
    payload = encode(stmt)
    return encode(
        {
            "payloadType": "application/vnd.in-toto+json",
            "payload": base64.b64encode(payload).decode(),
            "signatures": signatures,
        }
    )


def verifier_by_sig(context):
    sig = context["signature"]
    verdict = {
        "good": ("PASS", "issuer-A"),
        "good-B": ("PASS", "issuer-B"),
        "bad": ("FAIL", "issuer-A"),
        "unknown": ("UNKNOWN", None),
    }.get(sig.get("sig"), ("UNKNOWN", None))
    return {
        "result": verdict[0],
        "signer_identity": verdict[1],
        "verification_material_identity": f"fixture:{sig.get('keyid', 'none')}",
        "reason": None if verdict[0] == "PASS" else "fixture verdict",
    }


def all_required_policy(results):
    return "PASS" if results and all(item["result"] == "PASS" for item in results) else "FAIL"


def threshold_two_policy(results):
    return "PASS" if sum(item["result"] == "PASS" for item in results) >= 2 else "FAIL"


def any_verified_signature_policy(results):
    return "PASS" if any(item["result"] == "PASS" for item in results) else "FAIL"


def trusted_pair_policy(context):
    return {
        "status": "PASS",
        "pair_accepted": context.get("verifier_id") == "https://verifier.example"
        and "issuer-A" in context.get("signer_identities", []),
        "policy_identity": "trust-policy-v1",
        "policy_digest": "sha256:" + "d" * 64,
    }


def trusted_but_pair_rejected(_context):
    return {
        "status": "PASS",
        "pair_accepted": False,
        "policy_identity": "trust-policy-v1",
        "policy_digest": "sha256:" + "d" * 64,
    }


def trust_accepts_verified_issuer_a_only(context):
    accepted = "issuer-A" in context.get("signer_identities", [])
    return {
        "status": "PASS" if accepted else "FAIL",
        "pair_accepted": accepted
        and context.get("verifier_id") == "https://verifier.example",
        "policy_identity": "trust-policy-a-only-v1",
        "policy_digest": "sha256:" + "d" * 64,
    }


def predicate_pass(_context):
    return {
        "status": "PASS",
        "policy_identity": "predicate-policy-v1",
        "policy_digest": "sha256:" + "f" * 64,
    }


class OfflineImporterNegativeCases(unittest.TestCase):
    def import_bare(self, stmt, **kwargs):
        return import_attestation(
            encode(stmt),
            observed_at=OBSERVED,
            expected_subjects=[{"digest": {"sha256": SHA_A}}],
            **kwargs,
        )

    def import_env(self, stmt, signatures, **kwargs):
        return import_attestation(
            envelope(stmt, signatures),
            observed_at=OBSERVED,
            expected_subjects=[{"digest": {"sha256": SHA_A}}],
            signature_verifier=verifier_by_sig,
            **kwargs,
        )

    def test_neg_001_malformed(self):
        result = import_attestation(b"{", observed_at=OBSERVED)
        self.assertEqual(result["states"]["PARSED"], "FAIL")
        for stage in ("SUBJECT_BOUND", "SIGNATURE_VERIFIED", "TRUSTED_ISSUER", "PREDICATE_POLICY_VALIDATED"):
            self.assertEqual(result["states"][stage], "NOT_REACHED")
        self.assertEqual(result["promotion"], "NONE")

    def test_neg_002_co_subject_dropped(self):
        stmt = statement(subjects=[
            {"name": "a.whl", "digest": {"sha256": SHA_A}},
            {"name": "b.sbom", "digest": {"sha256": SHA_B}},
        ])
        result = self.import_bare(stmt)
        self.assertEqual(len(result["evidence_record"]["subjects"]), 2)
        self.assertTrue(result["evidence_record"]["subject_binding"]["complete_subject_set_preserved"])

    def test_neg_003_pep740_rule_leakage(self):
        stmt = statement(subjects=[{"name": "actual-name.whl", "digest": {"sha256": SHA_A}}])
        result = import_attestation(
            encode(stmt),
            observed_at=OBSERVED,
            expected_subjects=[{"digest": {"sha256": SHA_A}}],
        )
        self.assertEqual(result["states"]["SUBJECT_BOUND"], "PASS")

    def test_neg_004_unsupported_predicate(self):
        result = self.import_bare(statement("https://example.invalid/predicate/v9"))
        self.assertEqual(result["target"], "evidence_record")
        self.assertEqual(result["evidence_record"]["classification"], "SOURCE_DATA")
        self.assertEqual(result["states"]["PREDICATE_POLICY_VALIDATED"], "UNSUPPORTED")
        self.assertEqual(result["promotion"], "NONE")

    def test_neg_005_unverifiable_subject_id(self):
        result = import_attestation(
            encode(statement()),
            observed_at=OBSERVED,
            expected_subjects=[{"digest": {"sha512": "e" * 128}}],
        )
        self.assertEqual(result["states"]["SUBJECT_BOUND"], "UNKNOWN")

    def test_neg_006_invalid_signature(self):
        result = self.import_env(
            statement(),
            [{"keyid": "k1", "sig": "bad"}],
            signature_policy=all_required_policy,
        )
        self.assertEqual(result["per_signature_results"][0]["result"], "FAIL")
        self.assertEqual(result["states"]["SIGNATURE_VERIFIED"], "FAIL")
        self.assertEqual(result["states"]["TRUSTED_ISSUER"], "NOT_EVALUATED")

    def test_neg_007_valid_signature_no_trust_policy(self):
        result = self.import_env(
            statement(),
            [{"keyid": "k1", "sig": "good"}],
            signature_policy=all_required_policy,
        )
        self.assertEqual(result["states"]["SIGNATURE_VERIFIED"], "PASS")
        self.assertEqual(result["states"]["TRUSTED_ISSUER"], "UNKNOWN")
        self.assertNotEqual(result["evidence_record"]["source_identity"], "issuer-A")

    def test_neg_008_vsa_signer_verifier_mismatch(self):
        result = self.import_env(
            vsa(),
            [{"keyid": "k1", "sig": "good"}],
            signature_policy=all_required_policy,
            trust_policy=trusted_but_pair_rejected,
            predicate_policy=predicate_pass,
        )
        self.assertEqual(result["states"]["TRUSTED_ISSUER"], "PASS")
        self.assertEqual(result["states"]["PREDICATE_POLICY_VALIDATED"], "FAIL")
        self.assertEqual(result["aether_verification"], "NOT_EVALUATED")

    def test_neg_009_vsa_passed_not_aether_verification(self):
        result = self.import_env(
            vsa(),
            [{"keyid": "k1", "sig": "good"}],
            signature_policy=all_required_policy,
            trust_policy=trusted_pair_policy,
            predicate_policy=predicate_pass,
        )
        self.assertEqual(result["states"]["PREDICATE_POLICY_VALIDATED"], "PASS")
        self.assertEqual(result["evidence_record"]["classification"], "SOURCE_DATA")
        self.assertEqual(result["evidence_record"]["semantic_role"], "EXTERNAL_VERIFIER_ASSESSMENT")
        self.assertEqual(result["evidence_record"]["observed_at"], OBSERVED)
        self.assertEqual(
            result["evidence_record"]["attestation_asserted_timestamps"]["timeVerified"],
            "2026-08-18T12:00:00Z",
        )
        self.assertEqual(result["aether_verification"], "NOT_EVALUATED")
        self.assertEqual(result["verified_outcome"], "NOT_ESTABLISHED")
        self.assertEqual(result["promotion"], "NONE")

    def test_neg_010_vsa_failed(self):
        def vsa_result_policy(context):
            return {
                "status": "FAIL" if context["statement"]["predicate"].get("verificationResult") == "FAILED" else "PASS",
                "policy_identity": "predicate-policy-v1",
                "policy_digest": "sha256:" + "f" * 64,
            }
        result = self.import_env(
            vsa(verification_result="FAILED"),
            [{"keyid": "k1", "sig": "good"}],
            signature_policy=all_required_policy,
            trust_policy=trusted_pair_policy,
            predicate_policy=vsa_result_policy,
        )
        self.assertEqual(result["states"]["PREDICATE_POLICY_VALIDATED"], "FAIL")
        self.assertEqual(result["verified_outcome"], "NOT_ESTABLISHED")

    def test_neg_011_vsa_policy_digest_missing(self):
        def exact_policy(context):
            policy = context["statement"]["predicate"].get("policy", {})
            return {
                "status": "UNKNOWN" if "digest" not in policy else "PASS",
                "policy_identity": "predicate-policy-v1",
                "policy_digest": "sha256:" + "f" * 64,
            }
        result = self.import_env(
            vsa(policy_digest=False),
            [{"keyid": "k1", "sig": "good"}],
            signature_policy=all_required_policy,
            trust_policy=trusted_pair_policy,
            predicate_policy=exact_policy,
        )
        self.assertEqual(result["states"]["PREDICATE_POLICY_VALIDATED"], "UNKNOWN")

    def test_neg_012_missing_timestamp(self):
        result = self.import_bare(statement(predicate={}))
        self.assertEqual(result["evidence_record"]["observed_at"], OBSERVED)
        self.assertEqual(result["evidence_record"]["attestation_asserted_timestamps"], {})

    def test_neg_013_unknown_extension(self):
        raw = encode(statement(extra={"x-unknown": {"promote": True}}))
        result = import_attestation(
            raw,
            observed_at=OBSERVED,
            expected_subjects=[{"digest": {"sha256": SHA_A}}],
        )
        self.assertEqual(result["promotion"], "NONE")
        self.assertNotIn("x-unknown", result["evidence_record"])
        self.assertIn("sha256", result["evidence_record"]["raw_attestation_identity"])

    def test_neg_014_reserialization_identity(self):
        obj = statement()
        raw_a = json.dumps(obj, separators=(",", ":"), sort_keys=True).encode()
        raw_b = json.dumps(obj, indent=2, sort_keys=False).encode()
        result_a = import_attestation(raw_a, observed_at=OBSERVED)
        result_b = import_attestation(raw_b, observed_at=OBSERVED)
        self.assertNotEqual(
            result_a["evidence_record"]["raw_attestation_identity"]["sha256"],
            result_b["evidence_record"]["raw_attestation_identity"]["sha256"],
        )
        self.assertEqual(result_a["evidence_record"]["subjects"], result_b["evidence_record"]["subjects"])

    def test_neg_015_multisig_one_valid_no_aggregate_policy(self):
        result = self.import_env(
            statement(),
            [{"keyid": "k1", "sig": "good"}, {"keyid": "k2", "sig": "bad"}],
        )
        self.assertEqual([r["result"] for r in result["per_signature_results"]], ["PASS", "FAIL"])
        self.assertEqual(result["states"]["SIGNATURE_VERIFIED"], "UNKNOWN")

    def test_neg_016_multisig_policy_not_satisfied(self):
        result = self.import_env(
            statement(),
            [{"keyid": "k1", "sig": "good"}, {"keyid": "k2", "sig": "bad"}],
            signature_policy=threshold_two_policy,
        )
        self.assertEqual(result["states"]["SIGNATURE_VERIFIED"], "FAIL")
        self.assertEqual(result["states"]["TRUSTED_ISSUER"], "NOT_EVALUATED")

    def test_neg_017_vsa_policy_pass_without_signature_trust(self):
        result = self.import_env(
            vsa(),
            [{"keyid": "k1", "sig": "good"}],
            trust_policy=trusted_pair_policy,
            predicate_policy=predicate_pass,
        )
        self.assertEqual(result["states"]["SIGNATURE_VERIFIED"], "UNKNOWN")
        self.assertEqual(result["states"]["TRUSTED_ISSUER"], "NOT_EVALUATED")
        self.assertEqual(result["states"]["PREDICATE_POLICY_VALIDATED"], "NOT_EVALUATED")
        self.assertEqual(result["aether_verification"], "NOT_EVALUATED")


class OfflineImporterP1CorrectionRegressions(unittest.TestCase):
    def test_p1_001_empty_expected_subjects_cannot_bind(self):
        result = import_attestation(
            encode(statement()),
            observed_at=OBSERVED,
            expected_subjects=[],
            predicate_policy=predicate_pass,
        )
        self.assertEqual(result["states"]["PARSED"], "PASS")
        self.assertEqual(result["states"]["SUBJECT_BOUND"], "UNKNOWN")
        self.assertFalse(result["evidence_record"]["subject_binding"]["artifact_identity_constraint_present"])
        self.assertEqual(result["states"]["PREDICATE_POLICY_VALIDATED"], "NOT_EVALUATED")
        self.assertEqual(result["promotion"], "NONE")

    def test_p1_002_empty_statement_subject_set_fails_parse(self):
        result = import_attestation(
            encode(statement(subjects=[])),
            observed_at=OBSERVED,
            expected_subjects=[{"digest": {"sha256": SHA_A}}],
        )
        self.assertEqual(result["states"]["PARSED"], "FAIL")
        self.assertIn("non-empty", result["parse_error"])
        self.assertEqual(result["states"]["SUBJECT_BOUND"], "NOT_REACHED")
        self.assertEqual(result["promotion"], "NONE")

    def test_p1_003_malformed_signature_entry_is_not_silently_filtered(self):
        raw = envelope(
            statement(),
            [
                {"keyid": "k1", "sig": "good"},
                "not-an-object",
            ],
        )
        result = import_attestation(
            raw,
            observed_at=OBSERVED,
            expected_subjects=[{"digest": {"sha256": SHA_A}}],
            signature_verifier=verifier_by_sig,
            signature_policy=all_required_policy,
        )
        self.assertEqual(result["states"]["PARSED"], "FAIL")
        self.assertIn("signature entry", result["parse_error"])
        self.assertEqual(result["per_signature_results"], [])
        self.assertEqual(result["states"]["SIGNATURE_VERIFIED"], "NOT_REACHED")
        self.assertEqual(result["promotion"], "NONE")

    def test_p1_004_build_provenance_preserves_reviewed_typed_fields(self):
        stmt = build_provenance()
        result = import_attestation(
            encode(stmt),
            observed_at=OBSERVED,
            expected_subjects=[{"digest": {"sha256": SHA_A}}],
        )
        typed = result["evidence_record"]["slsa_evidence"]
        self.assertEqual(typed["kind"], "SLSA_BUILD_PROVENANCE_V1")
        self.assertEqual(typed["predicateType"], SLSA_PROVENANCE_V1)
        self.assertEqual(typed["predicate"]["buildDefinition"], stmt["predicate"]["buildDefinition"])
        self.assertEqual(typed["predicate"]["runDetails"], stmt["predicate"]["runDetails"])
        self.assertEqual(
            typed["predicate"]["buildDefinition"]["resolvedDependencies"],
            stmt["predicate"]["buildDefinition"]["resolvedDependencies"],
        )
        self.assertEqual(
            typed["predicate"]["runDetails"]["builder"],
            stmt["predicate"]["runDetails"]["builder"],
        )
        self.assertEqual(
            result["evidence_record"]["attestation_asserted_timestamps"],
            {
                "runDetails.metadata.startedOn": "2026-08-18T10:00:00Z",
                "runDetails.metadata.finishedOn": "2026-08-18T10:01:00Z",
            },
        )
        self.assertEqual(result["evidence_record"]["classification"], "SOURCE_DATA")
        self.assertEqual(result["promotion"], "NONE")

    def test_p1_005_vsa_preserves_reviewed_typed_fields(self):
        stmt = vsa()
        result = import_attestation(
            encode(stmt),
            observed_at=OBSERVED,
            expected_subjects=[{"digest": {"sha256": SHA_A}}],
        )
        typed = result["evidence_record"]["slsa_evidence"]
        expected_predicate = {
            "verifier": stmt["predicate"]["verifier"],
            "timeVerified": stmt["predicate"]["timeVerified"],
            "resourceUri": stmt["predicate"]["resourceUri"],
            "policy": stmt["predicate"]["policy"],
            "inputAttestations": stmt["predicate"]["inputAttestations"],
            "verificationResult": stmt["predicate"]["verificationResult"],
            "verifiedLevels": stmt["predicate"]["verifiedLevels"],
            "dependencyLevels": stmt["predicate"]["dependencyLevels"],
            "slsaVersion": stmt["predicate"]["slsaVersion"],
        }
        self.assertEqual(typed["kind"], "SLSA_VERIFICATION_SUMMARY_V1")
        self.assertEqual(typed["predicateType"], SLSA_VSA_V1)
        self.assertEqual(typed["predicate"], expected_predicate)
        self.assertEqual(result["evidence_record"]["classification"], "SOURCE_DATA")
        self.assertEqual(result["aether_verification"], "NOT_EVALUATED")
        self.assertEqual(result["verified_outcome"], "NOT_ESTABLISHED")
        self.assertEqual(result["promotion"], "NONE")

    def test_p1_006_equal_malformed_sha256_cannot_bind(self):
        malformed = "g" * 64
        stmt = statement(
            subjects=[{"name": "artifact.whl", "digest": {"sha256": malformed}}]
        )
        result = import_attestation(
            encode(stmt),
            observed_at=OBSERVED,
            expected_subjects=[{"digest": {"sha256": malformed}}],
            predicate_policy=predicate_pass,
        )
        self.assertEqual(result["states"]["PARSED"], "PASS")
        self.assertNotEqual(result["states"]["SUBJECT_BOUND"], "PASS")
        self.assertEqual(result["states"]["SUBJECT_BOUND"], "UNKNOWN")
        self.assertEqual(
            result["evidence_record"]["subject_binding"]["matched_subject_indices"],
            [],
        )
        self.assertEqual(result["states"]["PREDICATE_POLICY_VALIDATED"], "NOT_EVALUATED")
        self.assertEqual(result["promotion"], "NONE")

    def test_p1_007_trust_uses_only_verified_signer_identities(self):
        result = import_attestation(
            envelope(
                vsa(),
                [
                    {"keyid": "k-a", "sig": "bad"},
                    {"keyid": "k-b", "sig": "good-B"},
                ],
            ),
            observed_at=OBSERVED,
            expected_subjects=[{"digest": {"sha256": SHA_A}}],
            signature_verifier=verifier_by_sig,
            signature_policy=any_verified_signature_policy,
            trust_policy=trust_accepts_verified_issuer_a_only,
            predicate_policy=predicate_pass,
        )
        self.assertEqual(
            [item["result"] for item in result["per_signature_results"]],
            ["FAIL", "PASS"],
        )
        self.assertEqual(result["states"]["SIGNATURE_VERIFIED"], "PASS")
        self.assertEqual(
            result["evidence_record"]["signer_identity_claims"],
            ["issuer-A", "issuer-B"],
        )
        self.assertEqual(
            result["evidence_record"]["verified_signer_identities"],
            ["issuer-B"],
        )
        self.assertEqual(result["states"]["TRUSTED_ISSUER"], "FAIL")
        self.assertNotEqual(result["states"]["PREDICATE_POLICY_VALIDATED"], "PASS")
        self.assertEqual(result["states"]["PREDICATE_POLICY_VALIDATED"], "NOT_EVALUATED")
        self.assertEqual(result["promotion"], "NONE")


if __name__ == "__main__":
    unittest.main()
