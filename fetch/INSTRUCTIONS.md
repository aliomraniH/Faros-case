# fetch/ — pull faros.ai pages as JSON (Cowork / Desktop task)

This is the task for **Claude Cowork** or **Claude Desktop**. The Claude web session that seeded
this repo does **not** have network access to `faros.ai`, so the live fetch is deliberately handed
to a surface that does.

## What to do

1. Read `fetch/targets.json` — the list of pages to fetch, grouped by tab (Platform, Capabilities,
   Solutions; Company/reports are optional extras).
2. For **each** target URL, fetch the page and normalize it into a JSON file that conforms to
   `schemas/faros-page.schema.json`. One file per page:
   `fetch/raw/<tab>__<slug>.json` (e.g. `fetch/raw/platform__overview.json`).
3. Keep verbatim quotes **under 15 words**; paraphrase the rest. Capture structure faithfully:
   hero headline/subhead, section headings, named capabilities, named solutions, stats (e.g.
   "10x", "100+"), customer logos, and links worth following.
4. Record honest `notes` per page: anything gated, ambiguous, or that needed a judgment call.
5. Do **not** edit the knowledge tree directly. The **curator agent** (see `agents/curator-agent.md`)
   reads `fetch/raw/*.json` and proposes tree nodes in `status: proposed` for a human to approve.

## Targets (also in targets.json)

Primary (the three tabs Ali named):
- Platform: `https://www.faros.ai/platform` and its sub-pages (AI Transformation, Delivery
  Excellence, etc. — follow the in-page links).
- Capabilities: the capabilities/product pages (Token Intelligence, Engineering World Model, the
  observe/optimize/govern surfaces). Start from the top nav "Capabilities" / "Product".
- Solutions: the solutions / use-case / "for AI leaders" pages.

Secondary (optional, high-value for the tree):
- Company / about (`https://www.faros.ai/company`) — founders, vision.
- The AI Engineering Report 2026 ("Acceleration Whiplash") landing page — the independent-ish
  research anchor.
- Customer stories (Vimeo, SmartBear) — to verify proof points already in `offering.json`.

## Output contract

- Every file in `fetch/raw/` MUST validate against `schemas/faros-page.schema.json`.
- Set `retrieved_at` to the actual fetch time (ISO-8601).
- After fetching, append a one-line entry per page to `fetch/raw/_manifest.md` (url, tab, time).

## Coordination

When the fetch batch is done, record it in MCP_Assist so the curator (any surface) knows the raw
JSON is ready:

```
MCP_Assist:memory_save(
  namespace="dev/faros-case",
  key="fetch/batch-1",
  kind="claim",
  value="Fetched Platform/Capabilities/Solutions pages to fetch/raw/*.json; N files.",
  meta={ "repo": "aliomraniH/Faros-case", "branch": "main" },
  source_surface="claude-cowork"
)
```

Then run `coord_reconcile` so the claim can be verified against the repo once committed.
See `memory/README.md` and the handoff under key `handoff/web-to-cowork`.
