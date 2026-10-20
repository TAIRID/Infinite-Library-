# Infinite Library — public navigation entrypoint

**Current status (20 October 2026): early tested private-core prototype, not a complete or general autonomous knowledge engine.**

The user's original TAIRID corpus, precise unpublished terminology reviews, source manifests, experiment history, mathematical support matrix, and actual source-grounded query code reside in the **private** `TAIRID/Reverse-Engineering-Unknown` repository. This public repository is an entrypoint, **not** a mirror of those materials. It grants no public access to the private originals.

## How to use this with ChatGPT

With GitHub connected and access to the private research repository, ask ChatGPT:

> Open `TAIRID/Reverse-Engineering-Unknown/core/library-index.json` as my Infinite Library root. Follow the relevant source ID into the exact original document, report the original meaning and evidence status, and keep experimental limitations and failures visible.

You can also request a narrowly supported original-source query, for example:

> In the Infinite Library, compare what the original TAIRID documents actually say about `O = Tᵃ · Iᵇ` and explain why the numeric interpretation is not yet settled.

The working private engine is `core/library_query_v01.py`, and its original-source proofs are in `core/grounded-question-cases-v01.json`. The **GitHub Actions test in the private research repository** passed: https://github.com/TAIRID/Reverse-Engineering-Unknown/actions/runs/39439138375 (requires private repo access).

## Measured scope

- 139 original source pointers and 288 extracted text parts remain in the **private** archive; the mechanical scan did not constitute a full semantic review.
- Terminology v0.5: of 28 preliminary assigned senses, 10 have direct wording support, 7 partial support, and 11 have insufficient original source support. Zero cross-sense translations were approved.
- A new private source-review table documents 12 high-priority term families, without changing the historical 114-equation baseline.
- A new private math matrix classifies 20 proposed/native method links by their evidence and blocks unsupported transfers.
- A private original-source query prototype supports **six curated question cases**, eight regression tests and demonstrated abstention when evidence is missing or altered.
- The museum/structural-context navigation prototype has 14 passing unit tests but no measured advantage over standard document search.
- Most of established science, cultural history, school curricula and the broader original research corpus have **not** been integrated as verified, executable knowledge items.

## Required boundaries

- **Private source content is not available to unauthenticated public GitHub Actions**. A GitHub Action in this public repository cannot read a separate private repository using the standard default runner token. Do not insert a personal GitHub token into public workflow code.
- The core is source-linked and revisable; it is not a proof of TAIRID's proposed universal physical claims.
- Natural-language understanding of arbitrary questions, cross-field equation translation, automatic source acquisition and reliable ranking remain incomplete.
- Gemini remains reserved for occasional independent checks of mathematics/programming, not general document interpretation.
- Personal timeline data remain in the user's separate private repository.

**Important publication/history note:** An earlier build mistakenly treated the REU research repository as public and briefly committed detailed private archive *filenames, checksums, and interpretation metadata* into this public repository's history. Those files have been withdrawn from the current branch and retained in the private research repository. **Deleting files from the current branch does not erase them from earlier Git history**. Review the public repository visibility and history before treating its past commits as private. Full original manuscript text and private timeline files were not bulk copied in that entrypoint.

For a complete private-first Library, it is safer to keep source files and executable source-backed retrieval inside the authorized private repository and expose only limited, intentionally public interfaces.
