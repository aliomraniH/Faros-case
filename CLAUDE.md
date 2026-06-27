# CLAUDE.md — project guide for Claude Code

You are working in **Faros-case**: a deterministic, human-supervised knowledge tree that maps Faros
AI's offering to a buyer persona, with two agents (Curator, Advisor) that operate over it.

## The one rule you must never break
**Agents propose; humans approve.** You may create or edit knowledge-tree nodes only with
`status: proposed`. You must **never** set `status: approved` or write `approved_by` — only the
human (Ali) does that. `tools/validate_nodes.py` and CI enforce this; a PR that sets `approved`
without `approved_by` will fail.

## Layout (where things live)
- `knowledge-tree/` — typed nodes (`organization|faros|persona|flow|principle|mapping`), YAML
  frontmatter + Markdown body. Schema: `schemas/knowledge-node.schema.json`.
- `schemas/` — node, fetched-page, and offering schemas.
- `agents/` — Curator + Advisor specs and the orchestration loop. `agents/HUMAN-GATE.md` = how Ali
  approves.
- `fetch/` — instructions + targets to pull faros.ai pages as JSON into `fetch/raw/`.
- `memory/` — assist-memory key map + staged replay payloads.
- `tools/` — `validate_nodes.py`, `mcp_health.py`, `replay_memory.py`.

## Conventions
- Node IDs: `<type>:<slug>` (e.g. `faros:token-intelligence`). Unique. `parent` must resolve.
- Provenance: `sourced` (cite a page + retrieved_at), `inferred` (label it), `user-intent` (Ali's want).
- Honesty label on faros/mapping nodes: `shipped | roadmap | inference` — never present roadmap as shipped.
- Keep verbatim quotes from any source **under 15 words**; paraphrase the rest.
- Run `python3 tools/validate_nodes.py` before every commit. It must exit 0.

## assist-memory (coordination memory)
- Connector configured in `.mcp.json` under the name **`assist-memory`** (pin this name everywhere).
- Namespace: **`dev/faros-case`**.
- At the start of a work session: `coord_health("dev/faros-case")`, then load `insight/*` + `arch/*`.
- If the endpoint errors with "Session terminated", the Replit app is asleep — open its URL once to
  wake it, then retry. That error is a server state, not a name mismatch.
- Seeding memory: replay `memory/replay/all-payloads.json` (see `prompts/claude-code-seed-memory.md`).

## Positioning discipline (carry into any generated content)
Money is the door, quality is the room. Use "spend" to frame the entry; never argue "spend less" —
argue "see and improve what the spend produced." Never frame Faros as engineer surveillance:
decisions land at repo/system level, never individual keystrokes.

## Typical tasks you'll be asked to do
1. **Seed memory** — replay payloads into assist-memory (`dev/faros-case`).
2. **Fetch** — pull faros.ai Platform/Capabilities/Solutions pages to `fetch/raw/*.json` (conform to
   `schemas/faros-page.schema.json`). Use WebFetch.
3. **Curate** — read `fetch/raw/*.json`, propose `faros`/`mapping` nodes (`status: proposed`), append
   to `agents/review-queue.md`. Never approve.
4. **Advise (sim)** — answer persona questions from APPROVED nodes only, returning the advisor
   contract in `agents/advisor-agent.md`.

## Running the simulation (sim/)
- `python3 sim/run.py --interactive` — REPL; `--batch sim/questions.seed.json` — scorecard;
  `--export` — regenerate `sim/web/tree.js` then open `sim/web/index.html`.
- The engine answers ONLY from approved nodes; unmatched → gap (curator task); open commercial
  questions (pricing) hit a human-authored stance. Source of truth: `sim/engine.py`.
- To drive it from here, use `prompts/run-simulation.md`. Produce polished answers only from cited
  nodes; never invent facts; never change a node's status/approved_by.
