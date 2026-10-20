"""Honest first-stage test suite: index integrity and inspectable source pointers.

This validates *retrieval metadata*, NOT scientific source claims, assistant
semantic understanding, mathematical correctness, actual historical availability,
or speed advantages over ordinary search.
"""
import unittest
from scripts.library_lookup import (
    load, source, track, question, integrity, to_source_url
)


class LibraryBootstrapTests(unittest.TestCase):
    def test_integrity_self_check(self):
        result = integrity()
        self.assertEqual(result["status"], "LOCAL_POINTER_REGISTRY_CONSISTENCY_PASS")
        self.assertEqual(result["source_ids"], 139)
        self.assertEqual(result["extracted_text_pointers"], 288)

    def test_source_originals_preserved(self):
        src = source("SRC-136")
        self.assertEqual(src["source_id"], "SRC-136")
        self.assertIn("/blob/", src["original_source"])
        self.assertIn("sources/corpus-2026-10-11/", src["original_source"])
        self.assertTrue(src["extracted_text"])
        self.assertEqual(src["not_promoted"],
                         "ORIGINAL_SOURCE_PRESERVED_NOT_SCIENTIFICALLY_VALIDATED")

    def test_missing_source_does_not_make_science_claim(self):
        src = source("SRC-999")
        self.assertEqual(src["status"], "NOT_FOUND_IN_ORIGINAL_139_SOURCE_MANIFEST")

    def test_distinct_original_library_versions(self):
        a, b = source("SRC-046"), source("SRC-117")
        self.assertNotEqual(a["original_sha256_manifest_reported"],
                            b["original_sha256_manifest_reported"])
        self.assertNotEqual(a["original_source"], b["original_source"])

    def test_frozen_math_is_still_unreconciled(self):
        index = load("library-index.json")
        self.assertEqual(index["science"]["canonical_row_mapping"],
                         "NOT_FULLY_RECONCILED_IN_THIS_INDEX")

    def test_older_5_library_versions_retained(self):
        for key in ("IL01", "IL02", "IL03", "IL04", "IL05"):
            self.assertNotEqual(track(key)["status"], "TRACK_NOT_FOUND")

    def test_recorded_negative_results_retrievable(self):
        bad = track("IL38")
        self.assertEqual(bad["status"], "EXECUTED_SOURCE_TEST_NOT_SUPPORTED")
        self.assertIn("failed 2 of 3", bad["evidence_boundary"].lower())

    def test_unsupported_original_definitions_preserved(self):
        x = load("author-math-intent-crosswalk.json")
        match = next(y for y in x["entry_sources"] if y["id"] == "RECURSIVE-EXPONENTS")
        self.assertFalse(match["computable"])
        self.assertIn("NOT ordinary numeric powers", match["original_usage"])

    def test_three_gate_physical_validation_is_not_claimed(self):
        x = load("author-math-intent-crosswalk.json")
        gate = next(y for y in x["entry_sources"] if y["id"] == "THREE-GATES")
        self.assertIn("synthetic", gate["computable_scope"])
        self.assertNotEqual(gate["status"], "UNIVERSAL_PHYSICS_PROVEN")

    def test_sample_context_route_keeps_specific_identity(self):
        x = question("dayton")
        self.assertEqual(len(x["routes"]), 1)
        route = x["routes"][0]
        self.assertEqual(route["anchor"], "place:nmusaf")
        self.assertIn("e01, e08, e09, e10", route["syntax"])
        self.assertIn("two aircraft are different", route["syntax"])

    def test_unknown_question_is_not_a_negative_corpus_result(self):
        x = question("unlisted field qwerty")
        self.assertEqual(x["status"], "NO_CURATED_SAMPLE_QUERY_MATCH")
        self.assertIn("NOT evidence", x["message"])

    def test_tool_capability_limit_is_explicit(self):
        cap = load("library-index.json")["capabilities"]
        self.assertFalse(cap["answer_every_arbitrary_domain_query_from_this_root_without_tools"])
        self.assertFalse(cap["automatically_load_every_source_into_model_context"])

    def test_no_private_docx_contents_mirrored(self):
        src = load("source-registry.json")
        self.assertIn("NOT import private timeline", src["privacy"])
        self.assertTrue(all(set(d).issuperset(
            {"id","source_original_path","source_original_sha256","source_text_parts"}
        ) for d in src["source_documents"]))

    def test_prior_week_corrections_are_indexed(self):
        audit = load("last-week-correction-audit.json")
        years = [e["date"] for e in audit["events"]]
        self.assertEqual(years[0], "2026-10-13")
        self.assertEqual(years[-1], "2026-10-20")
        self.assertTrue(any("Gemini only" in v for v in audit["nonnegotiable_corrections"]))

    def test_compositional_gate_is_not_pretended_done(self):
        gates = load("readiness-gates.json")["six_beta_engineering_gates"]
        self.assertEqual(len(gates), 6)
        bond = next(g for g in gates if g["id"] == "B2")
        self.assertEqual(bond["status"], "PARTIAL")

    def test_pinned_url_encoding(self):
        u = to_source_url("sources/file name.docx", "abc123")
        self.assertIn("file%20name.docx", u)
        self.assertIn("abc123", u)


if __name__ == "__main__":
    unittest.main()
