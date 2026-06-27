# START HERE

You have the `Faros-case` folder (extracted from the download). Three ways to begin — pick one.

## A · Let Claude Code do it (recommended)
Open this folder in **Claude Code** (the Claude CLI / the Desktop "Code" tab — it has your GitHub
token) and paste the prompt in **`prompts/claude-cli-first-prompt.md`**. It runs the first script,
fixes anything that breaks, creates/pushes the GitHub repo, and shows you the simulation working.

## B · Run the first script yourself
```bash
cd Faros-case
chmod +x bootstrap.sh
./bootstrap.sh
```
`bootstrap.sh` is the full first-run script. It: installs deps → validates the tree → commits →
pushes to `github.com/aliomraniH/Faros-case` (using `gh` or `$GH_TOKEN`/`$GITHUB_TOKEN`) → checks
assist-memory → exports the local sim UI → runs a simulation smoke test. Safe to re-run.

## C · Just try the simulation (no GitHub, no network)
```bash
cd Faros-case
pip install pyyaml jsonschema --break-system-packages
python3 sim/run.py --interactive          # type buyer questions
# or
python3 sim/run.py --export && open sim/web/index.html   # local UI
```

---

### What this project is
A deterministic, human-supervised **knowledge tree** mapping Faros AI's offering to a buyer persona
(Maya), with Claude-managed **advisor + curator agents** that answer "how can Faros help?" from
approved nodes only. Full picture: `README.md` → `ARCHITECTURE.md` → `RUNBOOK.md`.

### What you need installed
- **Claude Code** (CLI or Desktop Code tab) with a GitHub token (`gh auth login`, or a `repo`-scoped
  token in `GH_TOKEN`). `.mcp.json` auto-connects assist-memory.
- **Claude Cowork** (Desktop Cowork tab or mobile) — for the faros.ai fetch + curate batch.
- **python3** with `pyyaml` + `jsonschema` (the script installs these).
- Optional: `gh` CLI (easiest auth + repo creation).

### The one rule
Agents **propose** (`status: proposed`); only you **approve** (`status: approved` + `approved_by`).
CI enforces it. See `agents/HUMAN-GATE.md`.
