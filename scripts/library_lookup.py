"""A genuinely runnable, bounded Infinite Library GitHub source-pointer resolver.

Does not fetch entire research corpus or claim natural language understanding.
The connected ChatGPT model supplies language interpretation and fetches cited
GitHub source files through its available connector, after inspecting this index.

Commands:
  python scripts/library_lookup.py source SRC-136
  python scripts/library_lookup.py track IL05
  python scripts/library_lookup.py question dayton
  python scripts/library_lookup.py integrity
"""
import argparse
import json
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "core"
ORIGINAL_REPO = "TAIRID/Reverse-Engineering-Unknown"


def load(file):
    return json.loads((CORE / file).read_text(encoding="utf-8"))


def to_source_url(path, commit):
    return (f"https://github.com/{ORIGINAL_REPO}/blob/{commit}/"
            + quote(path, safe="/.-_"))


def source(ref):
    library = load("library-index.json")
    registry = load("source-registry.json")
    record = next((s for s in registry["source_documents"] if s["id"] == ref), None)
    if record is None:
        return {"status": "NOT_FOUND_IN_ORIGINAL_139_SOURCE_MANIFEST", "source_id": ref}
    return {
        "status": "ORIGINAL_SOURCE_POINTER_NO_EVIDENCE_PROMOTION",
        "source_id": record["id"],
        "original_repo": ORIGINAL_REPO,
        "original_source": to_source_url(record["source_original_path"],
                                         library["origin_research_commit"]),
        "original_sha256_manifest_reported": record["source_original_sha256"],
        "extracted_text": [to_source_url(p, library["origin_research_commit"])
                           for p in record["source_text_parts"]],
        "extraction_scope": record["extraction_scope"],
        "not_promoted": record["reference_status"],
    }


def track(ref):
    library = load("library-index.json")
    found = next((r for r in library["existing_work_tracks"] if r["id"] == ref), None)
    if found is None:
        return {"status": "TRACK_NOT_FOUND", "track_id": ref}
    return {
        "status": found["status"],
        "id": found["id"], "title": found["label"],
        "source_path": found["source"],
        "source_url": to_source_url(found["source"], library["origin_research_commit"]),
        "evidence_boundary": found["explanation"],
        "test": found.get("test"),
    }


def question(name):
    index = load("library-index.json")
    hits = [q for q in index["sample_queries"]
            if name.lower() in q["id"].lower() or
               name.lower() in q["title"].lower()]
    if not hits:
        return {"status": "NO_CURATED_SAMPLE_QUERY_MATCH",
                "message": "This is NOT evidence that an item is absent from original research.",
                "question": name}
    return {
        "status": "CURATED_SAMPLE_ROUTE_NOT_GENERAL_LANGUAGE_SEARCH",
        "routes": [{
            **hit,
            "source_url": to_source_url(hit["path"],
                                        index["origin_research_commit"]),
        } for hit in hits]
    }


def integrity():
    index = load("library-index.json")
    manifest = load("source-registry.json")
    math = load("author-math-intent-crosswalk.json")
    week = load("last-week-correction-audit.json")
    gates = load("readiness-gates.json")
    docs = manifest["source_documents"]
    source_ids = [d["id"] for d in docs]
    part_count = sum(len(d["source_text_parts"]) for d in docs)
    assert index["repo"] == "TAIRID/Infinite-Library-"
    assert index["original_research_authority"] == ORIGINAL_REPO
    assert manifest["origin_repository"] == ORIGINAL_REPO
    assert manifest["origin_commit"] == index["origin_research_commit"]
    assert manifest["original_source_count"] == len(source_ids) == 139
    assert len(source_ids) == len(set(source_ids))
    assert manifest["original_text_parts"] == part_count == 288
    assert all(len(x["source_original_sha256"]) == 64 for x in docs)
    assert all(x["reference_status"] ==
               "ORIGINAL_SOURCE_PRESERVED_NOT_SCIENTIFICALLY_VALIDATED" for x in docs)
    assert {x["id"] for x in index["existing_work_tracks"]} >= {
        "IL01", "IL02", "IL03", "IL04", "IL05", "IL12", "IL16",
        "IL38", "ILNAV", "ILMATH", "ILPROV", "ILNEG",
    }
    assert len({x["id"] for x in index["existing_work_tracks"]}) == len(
        index["existing_work_tracks"])
    assert len(math["entry_sources"]) >= 10
    assert len(week["events"]) == 8
    assert len(gates["six_beta_engineering_gates"]) == 6
    assert not index["capabilities"]["automatically_load_every_source_into_model_context"]
    assert not index["capabilities"]["automatically_find_every_true_scientific_mechanism"]
    return {
        "status": "LOCAL_POINTER_REGISTRY_CONSISTENCY_PASS",
        "source_ids": len(source_ids),
        "extracted_text_pointers": part_count,
        "author_math_sense_examples": len(math["entry_sources"]),
        "prior_work_tracks": len(index["existing_work_tracks"]),
        "correction_dates": len(week["events"]),
        "beta_engineering_gates": len(gates["six_beta_engineering_gates"]),
        "scope": "Locally validates this index; does NOT re-open or hash remote REU source bytes.",
    }


def main():
    parser = argparse.ArgumentParser()
    cmd = parser.add_subparsers(dest="command", required=True)
    for operation in ("source", "track", "question"):
        sub = cmd.add_parser(operation)
        sub.add_argument("id")
    cmd.add_parser("integrity")
    args = parser.parse_args()
    if args.command == "source":
        result = source(args.id)
    elif args.command == "track":
        result = track(args.id)
    elif args.command == "question":
        result = question(args.id)
    else:
        result = integrity()
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
