# Review Queue (human gate)

The Curator appends one line per **proposed** node here. Ali reviews, edits the node file if needed,
then sets `status: approved` (+ `approved_by`, `approved_at`) in the node's frontmatter. Only
approved nodes are visible to the Advisor.

> **Decisions applied 2026-06-27 (Ali, via Claude Code).** The flagged conflicts/taxonomy/overlap
> below are now resolved in the node files (honesty markings kept, delivery family folded under
> Observe, GAINS/Executive-Scorecards overlap merged, project framing kept over website where they
> disagreed). **Status is still `proposed` on every node** — the approval flip remains Ali's gate.

| proposed node id | from source | honesty | proposed_at | status / resolution |
|---|---|---|---|---|
| `faros:token-intelligence` | /platform/token-intelligence | shipped | 2026-06-26 | ☐ website-confirmed |
| `faros:ai-transformation` | /platform/ai-transformation | shipped | 2026-06-26 | ☐ website-confirmed |
| `faros:clara-context-engine` | /platform/context-engineering | shipped | 2026-06-26 | ☐ website-confirmed |
| `faros:developer-productivity` | /platform/engineering-efficiency | shipped | 2026-06-26 | ☐ website-confirmed |
| `faros:delivery-excellence` | /platform/delivery-excellence | shipped | 2026-06-26 | ☐ ✓ folded under Observe |
| `faros:engineering-world-model` | /platform/token-intelligence | shipped | 2026-06-26 | ☐ website-confirmed |
| `faros:token-attribution-ledger` | /platform/token-intelligence | shipped | 2026-06-26 | ☐ website-confirmed |
| `faros:historical-replay` | /platform/context-engineering | inference | 2026-06-26 | ☐ ✓ keep project framing (Optimize partial) |
| `faros:model-routing` | /platform/token-intelligence | inference | 2026-06-26 | ☐ ✓ keep project framing (Optimize partial) |
| `faros:governance-guardrails` | /platform/ai-transformation | inference | 2026-06-26 | ☐ ✓ keep project framing (Govern roadmap) |
| `faros:provenance-audit-trail` | /platform/ai-transformation | shipped | 2026-06-26 | ☐ website-confirmed |
| `mapping:maya-adoption-aitransformation` | inferred (Maya × AI Transformation) | inference | 2026-06-26 | ☐ proposed (unconfirmed) |
| `mapping:maya-rework-context` | inferred (Maya × Clara) | inference | 2026-06-26 | ☐ proposed (unconfirmed) |
| `mapping:maya-predictability-delivery` | inferred (Maya × Delivery) | inference | 2026-06-26 | ☐ ✓ in scope (Observe) |
| `faros:gains` | /platform/ai-transformation/gains | shipped | 2026-06-27 | ☐ ✓ now owns Transformation Roadmaps |
| `faros:dora-metrics` | /dora-metrics | shipped | 2026-06-27 | ☐ website-confirmed |
| `faros:executive-scorecards` | /engineering-executives | shipped | 2026-06-27 | ☐ ✓ merged: roadmaps → gains |
| `faros:initiative-tracking` | /initiative-tracking | shipped | 2026-06-27 | ☐ ✓ Observe (sub of delivery) |
| `faros:software-capitalization` | /software-capitalization | shipped | 2026-06-27 | ☐ ✓ Observe (sub of delivery) |
| `mapping:maya-devex-friction` | inferred (Maya × Developer Experience) | inference | 2026-06-27 | ☐ proposed (unconfirmed) |

### Resolved decisions (Ali, 2026-06-27)

- **Honesty markings.** Website-confirmed capabilities keep `honesty: shipped` (provenance `sourced`).
  Our proposals that the live pages don't fully support keep `honesty: inference`. No labels changed —
  the curator's markings already matched this rule.
- **Conflicts — `faros:historical-replay`, `faros:model-routing`, `faros:governance-guardrails`:**
  keep the **project framing** (it's newer and authoritative). Live pages read more shipped than the
  seed's Optimize (`partial`) and Govern (`roadmap`); honesty stays `inference`, and the Govern node
  preserves "compensating controls over hard blocks, a human still merges" per
  `principle:empower-not-police`.
- **Taxonomy — Predictable Delivery family:** `faros:delivery-excellence` folded under **`faros:observe`**
  (delivery analytics computed on the same operational graph); its sub-caps `faros:initiative-tracking`
  and `faros:software-capitalization` inherit the Observe pillar; `mapping:maya-predictability-delivery`
  is now in scope. All report at org/initiative level, never individual keystrokes.
- **Overlap — `faros:gains` × `faros:executive-scorecards`:** **merged.** The recurring "Transformation
  Roadmaps" engagement (quarterly maturity + 90-day plan) is consolidated into `faros:gains`;
  `faros:executive-scorecards` keeps only the distinct boardroom KPI dashboards so the picture stays
  clear.
- **Corroborations (no new node, unchanged):** connector 70+→100+; Token Intelligence ↔
  `mapping:maya-roi-ledger` + `mapping:maya-tool-rationalization`; homepage "smarter—not smaller—budgets"
  ↔ positioning; `/ai-impact` ↔ `faros:ai-transformation`; `/developer-experience` ↔
  `faros:developer-productivity` + `principle:empower-not-police`; role pages recombine existing
  capabilities (captured as raw JSON, no duplicate nodes).
- **Negative memory (`mapping:maya-learning-negmem`):** unchanged — Clara's forward-learning is the
  closest public analog but not explicit failure write-back; stays roadmap/inference.

## Seed nodes (authored by claude-web, pre-approved by Ali for the seed commit)
These 16 nodes were authored directly in the seed and set to `approved` because Ali authored/owns
the interpretation they encode. Everything the **Curator** adds from live fetches must pass through
this queue.

See `knowledge-tree/00-index.md` for the current approved set.
