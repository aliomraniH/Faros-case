# sim/ — the Advisor simulation (run it locally)

An interactive, **deterministic** simulation of the Advisor answering buyer questions from the
**approved** knowledge tree. Built to be driven by **Claude Desktop coding** (it has local file
access), but every piece also runs as a plain CLI with no API key and no network.

## Three ways to run it

### 1) Interactive terminal (REPL)
```bash
python3 sim/run.py --interactive
```
Type a buyer question; get a scored answer with citations, honesty label, and positioning check.
Commands inside: `:persona persona:maya`, `:personas`, `:seed`, `:json`, `:quit`.

### 2) Batch scorecard
```bash
python3 sim/run.py --batch sim/questions.seed.json
```
Runs a question set and prints a scorecard (answered / gaps / quality %). Add your own questions to
`sim/questions.seed.json` (or any JSON list).

### 3) Local web UI (open in a browser / Claude Desktop)
```bash
python3 sim/run.py --export          # writes sim/web/tree.js from the approved tree
# then open sim/web/index.html
```
A standalone page (no server) that mirrors the engine in JS: pick a persona, ask questions, watch a
running scorecard. Re-run `--export` whenever you approve new nodes.

## What "deterministic" means here
- `sim/engine.py` is the source of truth. It loads only `status: approved` nodes, matches a question
  to a mapping (weighted keyword overlap, threshold `MATCH_THRESHOLD`), drafts the answer **from that
  node only**, runs the positioning check, and scores it.
- No approved node above threshold → **gap** (routes to the curator). The advisor never invents an
  answer.
- Open commercial questions (e.g. *how is Faros priced?*) hit a human-authored stance in
  `OPEN_INTENTS`, not a false capability match.

## The score (your eval)
Each answer is scored on three booleans: **citations_ok** (≥2 node IDs cited), **honesty_ok** (a
valid shipped/roadmap/inference label), **positioning_ok** (no drift to "spend less" / surveillance).
The batch quality % is the aggregate — that's the number to watch as the tree grows.

## Driving it from Claude Desktop coding
Open the repo in Claude Desktop (Code tab) and paste `prompts/run-simulation.md`. It will run the
batch, then optionally produce a **polished_answer** for each result drawn only from the matched
nodes (no new facts), preserving citations + honesty — the "Claude-in-the-loop" layer on top of the
deterministic core. It will also flag any answer that fails a score check and suggest the curator
task for each gap.

## Files
- `engine.py` — deterministic core (load, match, gate, score, export).
- `run.py` — CLI: `--interactive | --batch FILE | --once "q" | --export`.
- `questions.seed.json` — starter buyer questions (mix of in-scope, an open question, and an out-of-scope gap).
- `web/index.html` + `web/tree.js` — standalone local UI (tree.js is generated).
