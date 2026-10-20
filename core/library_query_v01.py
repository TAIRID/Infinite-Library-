"""Infinite Library v0.1: source-checked, deliberately bounded question -> source -> answer.

This is a deterministic adapter, NOT general language reasoning or independent
truth verification. It will not return a curated response if any referenced
original-source passage is unavailable or does not match the pinned archive.
Run from repo root with -m, after checking out the public TAIRID REU source.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re

CORE = Path(__file__).resolve().parent
DEFAULT_ORIGINAL_REPO = CORE.parent / "original-reu"
PINNED_ORIGIN = "e535ab3dddeb98460a7aff5f5d70ce7ae5c5b093"
BASE_URL = "https://github.com/TAIRID/Reverse-Engineering-Unknown/blob/" + PINNED_ORIGIN


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class NoTrustedAnswer(Exception):
    pass


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text.casefold()).strip()


def choose_case(question: str, cases: list[dict]) -> dict | None:
    text = normalized(question)
    choices = []
    for item in cases:
        matched = [p for p in item["match"] if normalized(p) in text]
        if matched:
            choices.append((max(map(len, matched)), item))
    if not choices:
        return None
    choices.sort(key=lambda x: (-x[0], x[1]["id"]))
    # Overlapping weak matches should NOT silently select a subject.
    if len(choices) > 1 and choices[0][0] == choices[1][0]:
        return None
    return choices[0][1]


def checked_path(root: Path, relative: str) -> Path:
    if relative.startswith("/") or "\\" in relative:
        raise NoTrustedAnswer("Untrusted absolute/path-escape source path")
    root = root.resolve()
    p = (root / relative).resolve()
    if not p.is_relative_to(root) or not p.is_file():
        raise NoTrustedAnswer("Original source missing or out of allowed root")
    return p


def fetch_evidence(case: dict, source_repo: Path, registry: dict) -> list[dict]:
    if registry["origin_commit"] != PINNED_ORIGIN:
        raise NoTrustedAnswer("Original source version not pinned to this runnable adapter")
    index = {entry["id"]: entry for entry in registry["source_documents"]}
    if len(index) != len(registry["source_documents"]):
        raise NoTrustedAnswer("Original document registry contains duplicate IDs")
    all_proofs = []
    for e in case["evidence"]:
        if e["kind"] == "original_text":
            doc = index.get(e["source_id"])
            if not doc:
                raise NoTrustedAnswer("Required original source ID missing")
            suffix = "/" + e["part"]
            matches = [path for path in doc["source_text_parts"] if path.endswith(suffix)]
            if len(matches) != 1:
                raise NoTrustedAnswer("Ambiguous or absent original source text part")
            path = matches[0]
            lines = checked_path(source_repo, path).read_text(encoding="utf-8").splitlines()
            needle = e["needle"]
            hits = [(i+1, line) for i, line in enumerate(lines) if needle in line]
            if len(hits) != 1:
                raise NoTrustedAnswer(f"Original source phrase missing or ambiguous: {e['source_id']}")
            lineno, full_line = hits[0]
            # Only the matched fragment is given to output, not the private/original whole work.
            all_proofs.append({
                "id": e["source_id"],
                "kind": "source_original_text",
                "required_passage": needle,
                "source_locator": f"{path}#L{lineno}",
                "source_url": f"{BASE_URL}/{path}#L{lineno}",
                "original_source_sha256_recorded": doc["source_original_sha256"],
                "passage_match": "EXACT_SUBSTRING_FOUND_IN_PINNED_ORIGINAL_EXTRACT"
            })
        elif e["kind"] == "reference_entry":
            path = "reference_library/v0.1/" + e["reference_filename"]
            j = read_json(checked_path(source_repo, path))
            refs = [r for r in j.get("records", []) if r["id"] == e["ref_id"]]
            if len(refs) != 1 or e["needle"] not in refs[0]["title"]:
                raise NoTrustedAnswer("Required native reference catalog item is absent or changed")
            ref = refs[0]
            all_proofs.append({
                "id": e["ref_id"], "kind": "provisional_native_reference",
                "required_passage": e["needle"], "native_equation": ref["equation"],
                "native_validity": ref["validity_conditions"],
                "catalog_review_status": ref["review_status"],
                "primary_external_source": ref["primary_reference"],
                "source_url": f"{BASE_URL}/{path}",
                "passage_match": "EXACT_RECORD_ID_AND_TITLE_FOUND_IN_PINNED_REFERENCE_CATALOG"
            })
        else:
            raise NoTrustedAnswer("Undeclared original source kind")
    return all_proofs


def answer(question: str, original_repo: Path, core: Path = CORE) -> dict:
    q = read_json(core / "grounded-question-cases-v01.json")
    registry = read_json(core / "source-registry.json")
    cases = q["cases"]
    candidate = choose_case(question, cases)
    if candidate is None:
        return {
            "status":"ABSTAIN_NO_CURATED_SOURCE_ROUTE",
            "question":question,
            "answer":None,
            "reason":"Unknown or ambiguous query. Not a negative result about the full original corpus.",
            "supported_case_ids":[c["id"] for c in cases],
        }
    try:
        evidence = fetch_evidence(candidate, original_repo, registry)
    except (NoTrustedAnswer, OSError, ValueError, KeyError) as exc:
        return {
            "status":"ABSTAIN_ORIGINAL_SOURCE_GATE_FAILED",
            "question":question,"case_id":candidate["id"],"answer":None,
            "reason":str(exc), "evidence":[],
        }
    return {
        "status":"CURATED_ANSWER_FROM_VERIFIED_SOURCE_MATCHES",
        "question":question, "case_id":candidate["id"],
        "answer":candidate["answer"],"scientific_gate":candidate["gate"],
        "evidence":evidence,
        "route":"question -> matched curated intent -> pinned public original source -> exact line/record check -> scoped authored explanation",
        "automatic_causal_or_semantic_promotion":False,
        "is_general_librarian":False,
        "is_independent_empirical_verification":False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", required=True)
    parser.add_argument("--origin", default=str(DEFAULT_ORIGINAL_REPO))
    args = parser.parse_args()
    result = answer(args.question, Path(args.origin))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if result["status"] == "ABSTAIN_ORIGINAL_SOURCE_GATE_FAILED":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
