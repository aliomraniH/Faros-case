#!/usr/bin/env bash
# Push this seed to your GitHub repo. Run from inside the Faros-case/ folder.
set -euo pipefail
REPO="https://github.com/aliomraniH/Faros-case.git"
git remote remove origin 2>/dev/null || true
git remote add origin "$REPO"
git branch -M main
# If the GitHub repo was created with a README, pull/rebase first:
git pull --rebase origin main 2>/dev/null || true
git push -u origin main
echo "Pushed to $REPO"
