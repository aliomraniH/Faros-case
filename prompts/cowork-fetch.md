# Prompt — Claude Cowork · fetch + curate faros.ai

Context: this repo (`Faros-case`) is a deterministic, human-supervised knowledge tree about Faros
AI. I want you to do two things as one job: fetch the marketing pages, then propose knowledge nodes
from them. Read `CLAUDE.md`, `fetch/INSTRUCTIONS.md`, and `agents/curator-agent.md` first.

PART 1 — FETCH
- Read `fetch/targets.json`. Fetch each Platform / Capabilities / Solutions page (primary list
  first, then secondary). Follow in-page nav to find real sub-pages and include them.
- Write one file per page to `fetch/raw/<tab>__<slug>.json`, conforming to
  `schemas/faros-page.schema.json`. Verbatim quotes < 15 words; paraphrase the rest; honest `notes`;
  real `retrieved_at`. Update `fetch/raw/_manifest.md`.

PART 2 — CURATE (propose only)
- For each fetched page, propose knowledge-tree nodes:
  - a `faros` node per distinct named capability/solution (provenance: sourced, with the page url +
    retrieved_at, an honest shipped/roadmap/inference label),
  - candidate `mapping` nodes linking `persona:maya`'s pains/flows to those capabilities
    (honesty: inference until I confirm evidence).
- Every node you create MUST have `status: proposed` and `proposed_by: cowork-curator`. You must
  NEVER set `status: approved` or `approved_by` — that's my gate.
- Append each proposed node (id, source page, honesty) to `agents/review-queue.md`.
- Run `python3 tools/validate_nodes.py` — it must exit 0 — and fix any schema/format issues.

Finish by listing the proposed node IDs and the pages each came from. Open a PR (or commit to a
branch) so I can review and approve.
