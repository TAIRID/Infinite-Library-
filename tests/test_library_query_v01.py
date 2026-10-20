"""Tests for a genuinely source-reading, bounded question → source → answer route.

A passing result confirms original public files were read at their PINNED commit.
It does not prove general semantic understanding, full corpus correctness,
citation validity in linked external scholarship, or scientific law.
"""
import json
from pathlib import Path
import tempfile
import unittest
from core.library_query_v01 import answer, choose_case, fetch_evidence, read_json

REPO = Path(__file__).resolve().parents[1]
ORIGINAL = REPO / "original-reu"
CORE = REPO / "core"

PROMPTS = [
    ("What do T^a and the exponents mean in the observation equation?", "Q-TIO", "BLOCK_NUMERIC_TAIRID_EQUATION"),
    ("Can SDR act as a universal truth detector?", "Q-SDR", "BLOCK_UNIVERSAL_TRUTH_SCORE"),
    ("What does the Kernel show about retained form and reuse?", "Q-REUSE", "KEEP_TESTED_MODEL_SCOPE"),
    ("Do three gates and the approach window prove a physical merge?", "Q-GATES", "ALLOW_SCOPED_ATTEMPT_GATE_ONLY"),
    ("Is golden ratio a universal Fibonacci branching attractor?", "Q-PHI", "BLOCK_UNIVERSAL_PHI"),
    ("How does Shannon information entropy in bits work?", "Q-SHANNON", "READY_NATIVE_MATH_NO_CROSS_SENSE_REPLACEMENT"),
]


class SourceToAnswerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not (ORIGINAL / "sources/corpus-2026-10-11/manifest.json").is_file():
            raise AssertionError("Tests REQUIRE an actual checkout of original REU, not mocked quotations")

    def test_all_six_real_source_queries(self):
        for question, case_id, gate in PROMPTS:
            with self.subTest(case_id=case_id):
                result = answer(question, ORIGINAL)
                self.assertEqual(result["status"], "CURATED_ANSWER_FROM_VERIFIED_SOURCE_MATCHES", result)
                self.assertEqual(result["case_id"], case_id)
                self.assertEqual(result["scientific_gate"], gate)
                self.assertGreater(len(result["evidence"]), 0)
                self.assertTrue(all(e["source_url"].startswith("https://github.com/TAIRID/Reverse-Engineering-Unknown/blob/") for e in result["evidence"]))
                self.assertTrue(all("PINNED_" in e["passage_match"] for e in result["evidence"]))
                self.assertFalse(result["automatic_causal_or_semantic_promotion"])

    def test_catalog_and_original_do_not_have_same_evidence_class(self):
        result = answer(PROMPTS[-1][0], ORIGINAL)
        kinds = {x["kind"] for x in result["evidence"]}
        self.assertEqual(kinds, {"source_original_text", "provisional_native_reference"})
        original = next(x for x in result["evidence"] if x["kind"] == "source_original_text")
        self.assertEqual(original["id"], "SRC-136")
        native = next(x for x in result["evidence"] if x["kind"] == "provisional_native_reference")
        self.assertEqual(native["id"], "REF-MATH-002")
        self.assertIn("requires source-level verification", native["catalog_review_status"])

    def test_unknown_question_refuses_to_invent_answer(self):
        result = answer("How long until a nearby supermarket stocks blue oranges?", ORIGINAL)
        self.assertEqual(result["status"], "ABSTAIN_NO_CURATED_SOURCE_ROUTE")
        self.assertIsNone(result["answer"])

    def test_missing_original_checkout_does_not_answer_from_template(self):
        with tempfile.TemporaryDirectory() as temp:
            result = answer(PROMPTS[0][0], Path(temp))
            self.assertEqual(result["status"], "ABSTAIN_ORIGINAL_SOURCE_GATE_FAILED")
            self.assertIsNone(result["answer"])

    def test_tampered_source_quote_does_not_answer_from_template(self):
        registry = read_json(CORE / "source-registry.json")
        case = next(c for c in read_json(CORE / "grounded-question-cases-v01.json")["cases"] if c["id"] == "Q-TIO")
        original = next(x for x in registry["source_documents"] if x["id"] == "SRC-136")
        source = next(p for p in original["source_text_parts"] if p.endswith("/part-001.md"))
        with tempfile.TemporaryDirectory() as temp:
            fake = Path(temp) / source
            fake.parent.mkdir(parents=True)
            native = (ORIGINAL / source).read_text(encoding="utf-8")
            self.assertIn(case["evidence"][1]["needle"], native)
            fake.write_text(native.replace(case["evidence"][1]["needle"],
                                           "UNAUTHORIZED_SOURCE_REPLACEMENT"),
                            encoding="utf-8")
            result = answer(PROMPTS[0][0], Path(temp))
            self.assertEqual(result["status"], "ABSTAIN_ORIGINAL_SOURCE_GATE_FAILED")
            self.assertIsNone(result["answer"])

    def test_original_math_source_identity_and_all_139_registry_entries(self):
        r = read_json(CORE / "source-registry.json")
        self.assertEqual(len(r["source_documents"]), 139)
        self.assertEqual(sum(len(x["source_text_parts"]) for x in r["source_documents"]), 288)
        self.assertEqual(len({x["id"] for x in r["source_documents"]}), 139)
        self.assertTrue(all(x["source_original_sha256"] for x in r["source_documents"]))

    def test_frozen_math_and_wrong_hypothesis_are_blocked_in_matrix(self):
        j = read_json(CORE / "math-connection-support-v01.json")
        lookup = {x["id"]: x for x in j["entries"]}
        self.assertEqual(len(lookup), 20)
        for ident in ("M12", "M13", "M14", "M15", "M16", "M18", "M19"):
            self.assertTrue(lookup[ident]["operational_decision"].startswith("BLOCK")
                            or lookup[ident]["operational_decision"] == "BENCHMARK_REQUIRED")

    def test_still_unapproved_author_senses(self):
        j = read_json(CORE / "terminology-source-review-v06.json")
        self.assertEqual(j["older_review"]["unsupported"], 11)
        self.assertEqual(j["older_review"]["approved_translations"], 0)
        self.assertEqual(len(j["data"]), 12)


if __name__ == "__main__":
    unittest.main()
