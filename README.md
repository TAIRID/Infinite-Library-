# Infinite Library — GitHub-backed Librarian entrypoint (bootstrap v0.1)

**Status: usable for limited, manual source-grounded navigation through a connected ChatGPT GitHub tool. NOT a finished knowledge base, automated Librarian, independent scientific validator, or general deployed query service.**

## Start here
Read [`core/library-index.json`](core/library-index.json) and [`core/author-math-intent-crosswalk.json`](core/author-math-intent-crosswalk.json). They record exactly where the existing working source graph, experiments, original author texts, 24 reference entries, 15 future source providers, 139 historical author source records and known failures can be found in the **existing** public `TAIRID/Reverse-Engineering-Unknown` repository. The new repository owns only the *navigation/read-only index*, not replacements of the scientific corpus or the original frozen equations.

### What can already be done in a connected ChatGPT session
A user can say: **"Use the Infinite Library GitHub index; begin at the Dayton Air Force Museum, go into the B-2 structural-test airframe, then explain how the Spirit of Ohio panel connects to Eglin and what the source actually proves."** The Librarian can open the linked source graph and original museum reference, give contextual paths, clarify that two separate aircraft are involved, and return the source. A connected ChatGPT can also follow original author source IDs, inspect selected lines, and distinguish proposed mathematical ideas from demonstrated library code.

The interface is still **manual retrieval by the assistant**: this repository is currently not a networked search API or a permanently loaded model context. It cannot force every fresh conversation to discover and read all links unless the user directs the assistant to this root. GitHub-connected ChatGPT can fetch/review/update permitted files; GitHub CI can execute specific committed tests; neither proves unlimited automatic code execution or self-updating intelligence.

### Exact boundaries
- Original source manuscripts and math authority stay in `TAIRID/Reverse-Engineering-Unknown`; **do not replace frozen ledger or science with an AI synopsis**.
- Private *Space Robot Five* timelines and personal source evidence stay in private `TAIRID/Space-Robot-Five`; none is mirrored here.
- Existing scientific reference set is 24 **provisional** source-anchored entries; original author corpus includes 139 source records, **not 139 validated scientific laws**.
- Historical pilot graph is 13 public museum nodes + 15 evidence-typed edges; 24 scientific catalog nodes were added to the navigation engine (mostly isolated).
- Preserve experiments that failed, and block concept analogies from becoming physically validated equations without measurable mappings and held-out tests.
- Gemini is reserved for occasional independent math/programming audits, not general history or manuscript review.
- The only test evidence so far is the source-typed [context navigation CI run](https://github.com/TAIRID/Reverse-Engineering-Unknown/actions/runs/39432358248), 14 tests passed, **not** a speed test or whole-corpus review.

## Examples of question commands to use in ChatGPT
- "Open the Infinite Library root, show the current core contents and their evidence statuses."
- "From the Air Force Museum node, follow the component-provenance link to Florida and return the full source trail."
- "Compare the original author meanings of recursion depth across SRC-136 and SRC-137; do not turn the equation into executable numerical powers without a source-level reconciliation."
- "Find whether the Library can evaluate overload with a physically or cognitively validated law; distinguish enzyme kinetics from a work-backlog model."
- "Show the failed heldout stage-boundary pilot and what specifically remained unidentified."

## What must happen next
1. Reconcile source-level mathematical definitions and author-version conflicts, with exact locators in **all** original manuscript parts before claiming a complete author mathematical core; then locate and verify all frozen 114 equation rows.
2. Implement source-provenance preserving typed components, relational compatibility, reversible composition, and time/location/experimental validity in one query engine—not solely the small museum graph.
3. Import and screen a much wider educational, history, art and science corpus as **individual licensed, cited items**, rather than treating 15 provider links as ingested books.
4. Add persisted, invalidatable knowledge assemblies, simple natural-language-to-typed-query routing, failure/abstention and source mutation guards.
5. Test against ordinary keyword/document retrieval and strong source/accuracy baselines, report time/steps, errors, cost and false transferred analogies.
6. Demonstrate one genuine end-to-end ChatGPT → GitHub core → source → answer → reversible navigation and correct updates across sessions. The limited manual example above demonstrates *some* of that path but not the integrated backend.
7. Only then expand neurotype-inspired optional processing strategies based on actual user-selected preferences and task results, without implying proof of neuropsychological generality.

**Truthfulness rule:** Nothing in the core gains scientific authority from being in this repository. The Library's organizational machinery is a hypothesis to test; sources and exact versioned experiment results control the factual content.
