# Prompt — paste this into Claude Code (the Claude CLI) FIRST

Run from inside the `Faros-case/` folder. This is the only prompt you need to get everything running.

---

You are working in the `Faros-case` repo. Read `START_HERE.md` and `CLAUDE.md` first so you know the
rules — most importantly: you may NEVER set a knowledge-tree node's `status: approved` or write
`approved_by`; only the human does that.

Then do the following, reporting what you did at each step and stopping to ask me only if something
truly blocks you:

1. Make `bootstrap.sh` executable and run it: `chmod +x bootstrap.sh && ./bootstrap.sh`.
2. If dependency install fails, install `pyyaml` and `jsonschema` however works in this environment,
   then continue.
3. If `tools/validate_nodes.py` reports problems, show me the failing nodes and fix ONLY
   schema/format issues — never change any node's `status` or `approved_by`.
4. If the push fails because the GitHub repo doesn't exist yet, create it and push:
   `gh repo create aliomraniH/Faros-case --private --source=. --remote=origin --push`
   (use `--public` instead of `--private` if I tell you to).
5. Run `python3 tools/mcp_health.py`. If assist-memory is reachable, seed memory by following
   `prompts/claude-code-seed-memory.md` (replay `memory/replay/all-payloads.json` into namespace
   `dev/faros-case`, skipping the `repo/seed-commit` claim until after the push, then run
   `coord_reconcile`). If it's NOT reachable, tell me — it's a sleeping Replit app, not a name
   mismatch — and skip memory for now; the payloads stay staged.
6. Run the simulation smoke test: `python3 sim/run.py --batch sim/questions.seed.json` and show me
   the scorecard.

Finish with a short summary: commit SHA, remote URL (or that the repo still needs creating),
whether memory seeded, and the simulation quality %. Then tell me the single best next action.
