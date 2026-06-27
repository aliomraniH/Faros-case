---
id: faros:historical-replay
type: faros
title: Historical Replay — learn context from past PRs
parent: faros:optimize
provenance: sourced
status: proposed
proposed_by: cowork-curator
honesty: inference
source:
  kind: faros-website
  url: https://www.faros.ai/platform/context-engineering
  retrieved_at: "2026-06-26T23:57:50Z"
  quote_or_derivation: "Context derived from past PRs and tickets until success rates soar."
fields:
  layer: sub-capability
  pillar: optimize
tags: [faros, historical-replay, optimize, proposed, conflict-flag]
---

Replays past tasks/PRs to extract per-repo context (patterns, dependencies, failure modes) and to
battle-test rules in simulation. **Conflict flag for human review:** the live Clara page presents
historical replay as a current product feature, but seed `offering.json` marks "Historical Replay"
as `shipped_status: partial`. Per curator rules, not silently resolving — proposed with
`honesty: inference` so the advisor can't over-claim, and flagged for Ali to set the true status.
