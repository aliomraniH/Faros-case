# Review Queue (human gate)

The Curator appends one line per **proposed** node here. Ali reviews, edits the node file if needed,
then sets `status: approved` (+ `approved_by`, `approved_at`) in the node's frontmatter. Only
approved nodes are visible to the Advisor.

| proposed node id | from source | honesty | proposed_at | reviewed? |
|---|---|---|---|---|
| `faros:token-intelligence` | /platform/token-intelligence | shipped | 2026-06-26 | ☐ |
| `faros:ai-transformation` | /platform/ai-transformation | shipped | 2026-06-26 | ☐ |
| `faros:clara-context-engine` | /platform/context-engineering | shipped | 2026-06-26 | ☐ |
| `faros:developer-productivity` | /platform/engineering-efficiency | shipped | 2026-06-26 | ☐ |
| `faros:delivery-excellence` | /platform/delivery-excellence | shipped | 2026-06-26 | ☐ ⚑ taxonomy |
| `faros:engineering-world-model` | /platform/token-intelligence | shipped | 2026-06-26 | ☐ |
| `faros:token-attribution-ledger` | /platform/token-intelligence | shipped | 2026-06-26 | ☐ |
| `faros:historical-replay` | /platform/context-engineering | inference | 2026-06-26 | ☐ ⚑ conflict |
| `faros:model-routing` | /platform/token-intelligence | inference | 2026-06-26 | ☐ ⚑ conflict |
| `faros:governance-guardrails` | /platform/ai-transformation | inference | 2026-06-26 | ☐ ⚑ conflict |
| `faros:provenance-audit-trail` | /platform/ai-transformation | shipped | 2026-06-26 | ☐ |
| `mapping:maya-adoption-aitransformation` | inferred (Maya × AI Transformation) | inference | 2026-06-26 | ☐ |
| `mapping:maya-rework-context` | inferred (Maya × Clara) | inference | 2026-06-26 | ☐ |
| `mapping:maya-predictability-delivery` | inferred (Maya × Delivery) | inference | 2026-06-26 | ☐ ⚑ taxonomy |

### Conflict / corroboration flags for Ali (curator does not resolve — rule 5)

- **Connector count 70+ → 100+:** the live `/platform/delivery-excellence` FAQ states "100+ tools".
  offering.json already notes "70+ (press-release) → 100+ (current marketing)". No node sets a hard
  number, so nothing to overwrite — recorded as corroboration of the 100+ figure.
- **Optimize pillar status (`faros:historical-replay`, `faros:model-routing`):** live pages present
  these as available; offering.json marks them `partial`. Proposed `honesty: inference` + flagged.
- **Govern pillar status (`faros:governance-guardrails`):** live page reads more shipped than the
  seed `faros:govern` (`roadmap`). Proposed `honesty: inference` + flagged. Preserve the seed's
  "compensating controls over hard blocks, human still merges" distinction when approving.
- **Taxonomy (`faros:delivery-excellence`, `mapping:maya-predictability-delivery`):** a 5th named
  capability (predictable delivery / PMO) sits outside the Observe/Optimize/Govern thesis. Decide
  fold-under-pillar vs. sibling-pillar vs. out-of-scope before approving.
- **Corroborations (no new node needed):** Token Intelligence page corroborates
  `mapping:maya-roi-ledger` (Token Attribution Ledger) and `mapping:maya-tool-rationalization`
  (task-to-tool routing); homepage hero corroborates the "money is the door, never spend-less"
  positioning ("smarter—not smaller—budgets").
- **Negative memory (`mapping:maya-learning-negmem`):** the Clara page's "feedback becomes reusable
  context so agents don't ask twice" is the closest public analog, but frames forward learning, not
  explicit failure write-back. Left as-is (still roadmap/inference); no overwrite.

## Seed nodes (authored by claude-web, pre-approved by Ali for the seed commit)
These 13 nodes were authored directly in the seed and set to `approved` because Ali authored/owns
the interpretation they encode. Everything the **Curator** adds from live fetches must pass through
this queue.

See `knowledge-tree/00-index.md` for the current approved set.
