# Prompt — Claude Code · bootstrap & push

Run from inside the `Faros-case/` folder.

---
Read `CLAUDE.md` first so you know the rules (especially: you may NEVER set a node's `status:
approved` or write `approved_by` — only the human does).

Then:
1. Run `python3 tools/validate_nodes.py`. If it fails, show me the failing nodes and fix only
   schema/format problems — never change `status` or `approved_by`.
2. Run `./bootstrap.sh`. It commits and pushes to `github.com/aliomraniH/Faros-case` using my
   GitHub token (gh auth or $GH_TOKEN/$GITHUB_TOKEN).
3. If the push fails because the repo doesn't exist yet, create it:
   `gh repo create aliomraniH/Faros-case --private --source=. --remote=origin --push`
4. Run `python3 tools/mcp_health.py` and tell me whether assist-memory is reachable.
5. Summarize: what was committed, the commit SHA, the remote URL, and the next step.

Do not modify the knowledge tree's content in this task — bootstrap only.
