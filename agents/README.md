# agents/ — Claude-managed advisor & curator

Two agents, deliberately split so that **writing knowledge** and **answering from knowledge** never
blur. Both are "managed separately by Claude" — they run as distinct Claude instances/sessions with
distinct system prompts and distinct permissions over the tree.

| agent | reads | writes | the one rule |
|---|---|---|---|
| **Curator** (`curator-agent.md`) | `fetch/raw/*.json`, existing tree | new nodes as `status: proposed` only | never approves its own work |
| **Advisor** (`advisor-agent.md`) | **approved** tree nodes only | nothing in the tree (may emit curator tasks) | if it isn't in an approved node, say so — don't improvise |

The human (Ali) sits at exactly one gate: **approval**. That single deterministic gate is what makes
the whole system trustworthy. See `orchestration.md` for the loop.

> Design echo: this is Faros's own "policy + provenance + a human still reviews and merges" applied
> to the knowledge that powers the demo. The advisor can defend itself with its own architecture.
