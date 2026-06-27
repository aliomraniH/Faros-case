# RUNBOOK — how to run Faros-case end to end

Two surfaces, one human gate. **Claude Code** (the CLI, has your GitHub token) does git + memory +
optional fetch. **Claude Cowork** does the heavier multi-step fetch + curation when you'd rather
hand off a whole task. You (Ali) are the approval gate in the middle.

```
  Claude Code ──push──► GitHub ──┐
       │  seed memory            │
       ▼                         ▼
   assist-memory            Claude Cowork ──fetch faros.ai──► fetch/raw/*.json
   (dev/faros-case)             │ curate (propose nodes)
       ▲                        ▼
       └──── you approve ◄── agents/review-queue.md ──► Advisor answers (simulation)
```

---

## §1 · One-time setup (Claude Code)

You have the seed on disk (extracted `Faros-case/`). In a terminal:

```bash
cd Faros-case
chmod +x bootstrap.sh
./bootstrap.sh
```

Or drive it through Claude Code so it can react to anything that goes wrong:

> **Prompt (paste into Claude Code, run from the Faros-case folder):**
> "Read CLAUDE.md, then run ./bootstrap.sh. If validation fails, show me the failing nodes and fix
> only schema/format issues (never change a node's `status` or `approved_by`). If the push fails
> because the repo doesn't exist, create it with `gh repo create aliomraniH/Faros-case --private
> --source=. --remote=origin --push`. Report what you did."

`bootstrap.sh` validates the tree, commits, pushes to `github.com/aliomraniH/Faros-case`, and tries a
memory health check. Full prompt also in `prompts/claude-code-bootstrap.md`.

**GitHub token:** the script uses, in order, an authenticated `gh` CLI → `$GH_TOKEN` → `$GITHUB_TOKEN`.
For a token, it needs `repo` scope. If you use a fine-grained token, grant Contents: read/write on
this repo.

---

## §2 · Fetch faros.ai (choose Cowork **or** Claude Code)

The Claude **web** session that built the seed couldn't reach faros.ai; these surfaces can.

### Option A — Claude Cowork (recommended for the full batch)
Cowork is built for multi-step jobs with many tool calls and files — ideal here.

1. Open Claude Cowork (desktop app → Cowork tab; or the Claude mobile app → Cowork).
2. Connect the repo: point Cowork at your local clone of `Faros-case`, or connect GitHub so it can
   read/write the repo.
3. Paste the prompt from `prompts/cowork-fetch.md`. It tells Cowork to read `fetch/targets.json`,
   fetch each Platform/Capabilities/Solutions page, and write conformant JSON to `fetch/raw/*.json`
   plus update `_manifest.md`.
4. Let it run; review the `fetch/raw/*.json` it produced.

### Option B — Claude Code (if you'd rather stay in the CLI)
Claude Code has a WebFetch tool. Paste `prompts/claude-code-fetch.md`. Same output contract.

**Output contract (both):** one file per page, `fetch/raw/<tab>__<slug>.json`, validating against
`schemas/faros-page.schema.json`; verbatim quotes < 15 words; honest `notes` per page.

---

## §3 · Curate fetched JSON into proposed nodes (Cowork or Claude Code)

Run the **Curator**. Paste `prompts/curate.md` into whichever surface holds the repo. It reads
`fetch/raw/*.json` and creates `faros`/`mapping` nodes with `status: proposed`, citing each source
page, and appends them to `agents/review-queue.md`. **It never approves.**

Then run the validator:
```bash
python3 tools/validate_nodes.py    # must exit 0
```

---

## §4 · Seed / update assist-memory memory (Claude Code)

The architecture + website insights belong in assist-memory so any surface can bootstrap. Two ways:

**Preferred — native tool calls via Claude Code** (the connector is in `.mcp.json`):
> Paste `prompts/claude-code-seed-memory.md`. It checks health, then replays
> `memory/replay/all-payloads.json` as `memory_save`/`handoff_save` calls into `dev/faros-case`,
> saving the `repo/seed-commit` claim **after** the push and running `coord_reconcile`.

**Fallback — raw HTTP, no Claude in the loop:**
```bash
python3 tools/mcp_health.py            # is the endpoint awake?
python3 tools/replay_memory.py         # replays everything except the claim
python3 tools/replay_memory.py --include-claim   # after the push
```

**If you see "Session terminated" / unreachable:** the server is a Replit app that sleeps. Open
`https://mcp-assist-memory.replit.app/mcp` (or its dashboard) once to wake it, then retry. This is a
server state — **not** a connector-name mismatch (the name `assist-memory` is correct; a real mismatch
would say "tool not found").

---

## §5 · Approve (the human gate — you)

Open `agents/review-queue.md`. For each proposed node you accept, edit its file and set:
```yaml
status: approved
approved_by: ali
approved_at: <ISO timestamp>
```
Remove its line from the queue. CI blocks any `approved` node missing `approved_by`. See
`agents/HUMAN-GATE.md`.

---

## §6 · Run the advisor simulation (Claude Desktop coding)

The simulation is built and runnable in `sim/`. It answers buyer questions **only** from approved
nodes, cites them, labels honesty, runs a positioning check, and scores each answer.

```bash
python3 sim/run.py --interactive                  # REPL — type questions, get scored answers
python3 sim/run.py --batch sim/questions.seed.json # scorecard across a question set
python3 sim/run.py --export && open sim/web/index.html   # standalone local UI (no server)
```

To drive it from **Claude Desktop coding** (local file access): open the repo in the Code tab and
paste `prompts/run-simulation.md`. It runs the batch, produces a polished answer per result drawn
**only** from the cited nodes (no new facts), turns each gap into a curator task, and flags any
answer that fails a score check — without ever changing a node's `status`/`approved_by`.

**The eval:** each answer scores on citations_ok · honesty_ok · positioning_ok. The batch quality %
is the number to watch as the tree grows with real fetched nodes. See `sim/README.md`.

---

## What you need installed
- **Claude Code** (the CLI / desktop Code tab) with your GitHub token (`gh auth login` or a `repo`
  scoped token in `GH_TOKEN`). The `.mcp.json` here auto-connects assist-memory.
- **Claude Cowork** (desktop app's Cowork tab, or mobile) — for the fetch/curate batch.
- **python3** with `pyyaml`, `jsonschema` (the bootstrap installs these).
- Optional: `gh` CLI for the easiest auth + repo creation.
