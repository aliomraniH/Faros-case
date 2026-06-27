# Prompt — Claude Cowork · fetch + curate + sync faros.ai (batch-1)

Run this in **Claude Cowork** with the `Faros-case` repo connected (clone or GitHub). It is one job
in three parts: crawl the site, propose nodes, sync to git + assist-memory. Do the work; do NOT approve
anything — approval is Ali's gate.

## Bootstrap (do first)
Read `CLAUDE.md`, `fetch/INSTRUCTIONS.md`, `fetch/targets.json`, and `agents/curator-agent.md`.
Then bootstrap context from **assist-memory** namespace `dev/faros-case`: read the `insight/*` and
`arch/*` entries and the `handoff/web-to-cowork` baton. The repo is live at
`github.com/aliomraniH/Faros-case` (branch `main`).

## PART 1 — CRAWL
- Fetch every page in `fetch/targets.json` — the **Platform**, **Capabilities**, and **Solutions**
  tabs first (primary list), then secondary. Follow in-page nav to the real sub-pages and include
  any you find.
- Write one file per page to `fetch/raw/<tab>__<slug>.json`, conforming to
  `schemas/faros-page.schema.json`: hero headline/subhead/CTA, ordered sections, `named_capabilities`,
  `named_solutions`, `stats` (e.g. "10x", "100+"), customer logos, links.
- Verbatim quotes **under 15 words**; paraphrase the rest; honest `notes`; real `retrieved_at`.
- Update `fetch/raw/_manifest.md`. If a page is JS-gated or returns nothing, list it as
  **"needs Chrome"** and move on — don't fabricate content.

## PART 2 — CURATE (propose only)
For each fetched page, propose tree nodes:
- a `faros` node per distinct **named capability/solution** — `provenance: sourced`, with the page
  `url` + `retrieved_at` + a **<15-word paraphrase**, and an honest `shipped | roadmap | inference`
  label;
- candidate `mapping` nodes linking **`persona:maya`'s pains/flows** to those capabilities
  (`honesty: inference` until Ali confirms evidence).

Every node MUST be `status: proposed`, `proposed_by: cowork-curator`. **Never** set `status: approved`
or `approved_by`. Append each (id, source page, honesty) to `agents/review-queue.md`. If a fetched
fact **conflicts** with an approved node (e.g. connectors 70+ → 100+), do NOT overwrite — propose an
update node and flag the conflict in the queue.

## PART 3 — SYNC
1. Run `python3 tools/validate_nodes.py` — it MUST exit 0; fix only schema/format issues.
2. Commit the raw JSON + proposed nodes and open a PR (or push a branch) for Ali to review.
3. In **assist-memory** `dev/faros-case`:
   - save a **claim** keyed `fetch/batch-1` with `meta.repo=aliomraniH/Faros-case`, `meta.branch=main`,
     and the list of files written, then run `coord_reconcile`;
   - save a **knowledge** entry `insight/offering-live` summarizing the real Platform / Capabilities /
     Solutions offering you found (readable from Claude web + Desktop).

## Finish
List every proposed node ID and which page it came from, the files written to `fetch/raw/`, any
"needs Chrome" pages, and any conflicts flagged.
