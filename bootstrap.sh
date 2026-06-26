#!/usr/bin/env bash
###############################################################################
# Faros-case · bootstrap.sh
#
# Run this from INSIDE the extracted Faros-case/ folder. It is written to be run
# by Claude Code (the Claude CLI), which has a GitHub token available, but a human
# can run it too.
#
# What it does, in order:
#   1. Checks prerequisites (git, python3, and a GitHub credential).
#   2. Validates the seed knowledge tree (schema + human-gate rules).
#   3. Initializes git (if needed) and pushes to github.com/aliomraniH/Faros-case.
#   4. Optionally seeds MCP_Assist memory (if the server is awake).
#   5. Prints the next steps (fetch → curate → approve → advise).
#
# Safe to re-run. Each step is idempotent and guarded.
###############################################################################
set -euo pipefail

REPO_OWNER="aliomraniH"
REPO_NAME="Faros-case"
REPO_SLUG="${REPO_OWNER}/${REPO_NAME}"
REPO_URL="https://github.com/${REPO_SLUG}.git"
BRANCH="main"

c_grn(){ printf "\033[32m%s\033[0m\n" "$*"; }
c_yel(){ printf "\033[33m%s\033[0m\n" "$*"; }
c_red(){ printf "\033[31m%s\033[0m\n" "$*"; }
c_cya(){ printf "\033[36m%s\033[0m\n" "$*"; }
step(){ printf "\n\033[1;36m== %s ==\033[0m\n" "$*"; }

# ---------------------------------------------------------------------------
step "0 · Sanity: are we in the repo root?"
if [[ ! -f "README.md" || ! -d "knowledge-tree" || ! -d "schemas" ]]; then
  c_red "This doesn't look like the Faros-case root (no knowledge-tree/ + schemas/)."
  c_red "cd into the extracted Faros-case/ folder and re-run."
  exit 1
fi
c_grn "OK — in $(pwd)"

# ---------------------------------------------------------------------------
step "1 · Prerequisites"
command -v git >/dev/null     || { c_red "git not found"; exit 1; }
command -v python3 >/dev/null || { c_red "python3 not found"; exit 1; }
python3 -m pip install --quiet --break-system-packages pyyaml jsonschema 2>/dev/null \
  || pip3 install --quiet pyyaml jsonschema 2>/dev/null || c_yel "(could not pre-install pyyaml/jsonschema; validator may need them)"

# Resolve a GitHub credential. Prefer gh CLI; fall back to a token env var.
GH_MODE=""
if command -v gh >/dev/null && gh auth status >/dev/null 2>&1; then
  GH_MODE="gh"
  c_grn "GitHub auth: gh CLI is authenticated."
elif [[ -n "${GH_TOKEN:-}" ]]; then
  GH_MODE="token"; TOKEN="${GH_TOKEN}"
  c_grn "GitHub auth: using \$GH_TOKEN."
elif [[ -n "${GITHUB_TOKEN:-}" ]]; then
  GH_MODE="token"; TOKEN="${GITHUB_TOKEN}"
  c_grn "GitHub auth: using \$GITHUB_TOKEN."
else
  c_yel "No GitHub credential found (no authenticated gh, no GH_TOKEN/GITHUB_TOKEN)."
  c_yel "Set one of these, or run: gh auth login   — then re-run."
  GH_MODE="none"
fi

# ---------------------------------------------------------------------------
step "2 · Validate the seed (schema + human gate)"
if python3 tools/validate_nodes.py; then
  c_grn "Validation passed."
else
  c_red "Validation failed — fix the nodes above before pushing."
  exit 1
fi

# ---------------------------------------------------------------------------
step "3 · Git init + commit (if needed)"
if [[ ! -d ".git" ]]; then
  git init -q
  git add -A
  git -c commit.gpgsign=false commit -q -m "Seed Faros-case (deterministic human-supervised knowledge tree)"
  c_grn "Initialized git and made the seed commit."
else
  # commit any local additions (e.g. this kit) so the push is complete
  if ! git diff --quiet || ! git diff --cached --quiet || [[ -n "$(git status --porcelain)" ]]; then
    git add -A
    git -c commit.gpgsign=false commit -q -m "Add Claude Code bootstrap kit (scripts, CI, runbook, prompts)" || true
    c_grn "Committed local changes."
  else
    c_grn "Working tree clean."
  fi
fi
git branch -M "$BRANCH"

# ---------------------------------------------------------------------------
step "4 · Push to ${REPO_SLUG}"
if [[ "$GH_MODE" == "none" ]]; then
  c_yel "Skipping push — no credential. Add a token and re-run, or push manually:"
  echo   "    git remote add origin ${REPO_URL} && git push -u origin ${BRANCH}"
else
  git remote remove origin >/dev/null 2>&1 || true
  if [[ "$GH_MODE" == "token" ]]; then
    git remote add origin "https://x-access-token:${TOKEN}@github.com/${REPO_SLUG}.git"
  else
    git remote add origin "$REPO_URL"   # gh credential helper handles auth
  fi
  # If the GitHub repo was created with an initial commit (README/license), reconcile first.
  git pull --rebase origin "$BRANCH" 2>/dev/null || true
  if git push -u origin "$BRANCH"; then
    c_grn "Pushed to ${REPO_URL}"
  else
    c_red "Push failed. Common causes: repo not created yet, or token lacks 'repo' scope."
    c_yel "Create it (gh): gh repo create ${REPO_SLUG} --private --source=. --remote=origin --push"
  fi
  # scrub token from the stored remote URL
  if [[ "$GH_MODE" == "token" ]]; then
    git remote set-url origin "$REPO_URL"
  fi
fi

# ---------------------------------------------------------------------------
step "5 · (Optional) Seed MCP_Assist memory if the server is awake"
if [[ -f "tools/mcp_health.py" ]]; then
  if python3 tools/mcp_health.py; then
    c_grn "MCP_Assist looks reachable."
    c_cya "To seed memory, run Claude Code with the prompt in prompts/claude-code-seed-memory.md,"
    c_cya "or: python3 tools/replay_memory.py   (raw HTTP fallback)."
  else
    c_yel "MCP_Assist endpoint not reachable right now (Replit app may be asleep)."
    c_yel "It will seed later — the payloads are staged in memory/replay/. See RUNBOOK.md §4."
  fi
fi

# ---------------------------------------------------------------------------
step "Done"
c_grn  "Repo seeded and (if credentialed) pushed."
echo
c_cya  "Next:"
echo   "  • Fetch faros.ai pages  → see RUNBOOK.md §2  (Claude Cowork or Claude Code WebFetch)"
echo   "  • Curate into nodes     → RUNBOOK.md §3  (curator agent, status: proposed)"
echo   "  • Approve (human gate)  → agents/HUMAN-GATE.md"
echo   "  • Seed/replay memory    → RUNBOOK.md §4"
echo
c_cya  "Copy-paste prompts for each surface are in prompts/."
