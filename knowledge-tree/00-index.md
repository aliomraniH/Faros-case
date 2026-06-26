# Knowledge Tree — Index

Auto-generated list of nodes. Every node validates against `schemas/knowledge-node.schema.json`.

| id | type | status | provenance | file |
|---|---|---|---|---|
| `faros:govern` | faros | approved | sourced | [govern.md](faros/govern.md) |
| `faros:observe` | faros | approved | sourced | [observe.md](faros/observe.md) |
| `faros:optimize` | faros | approved | sourced | [optimize.md](faros/optimize.md) |
| `faros:root` | faros | approved | sourced | [00-faros.md](faros/00-faros.md) |
| `flow:board-asks-roi` | flow | approved | inferred | [board-asks-roi.md](flows/board-asks-roi.md) |
| `flow:incident-to-cause` | flow | approved | inferred | [incident-to-cause.md](flows/incident-to-cause.md) |
| `mapping:maya-incident-observe` | mapping | approved | inferred | [maya-incident-to-observe.md](mapping/maya-incident-to-observe.md) |
| `mapping:maya-learning-negmem` | mapping | approved | inferred | [maya-learning-to-negative-memory.md](mapping/maya-learning-to-negative-memory.md) |
| `mapping:maya-roi-ledger` | mapping | approved | sourced | [maya-roi-to-ledger.md](mapping/maya-roi-to-ledger.md) |
| `organization:root` | organization | approved | user-intent | [00-root.md](00-root.md) |
| `persona:maya` | persona | approved | inferred | [maya.md](personas/maya.md) |
| `principle:empower-not-police` | principle | approved | user-intent | [empower-not-police.md](principles/empower-not-police.md) |
| `principle:transfer-of-mastery` | principle | approved | user-intent | [transfer-of-mastery.md](principles/transfer-of-mastery.md) |

## Edges (parent → child)

- `faros:root` → `faros:govern`
- `faros:root` → `faros:observe`
- `faros:root` → `faros:optimize`
- `null` → `organization:root`
- `organization:root` → `faros:root`
- `organization:root` → `flow:board-asks-roi`
- `organization:root` → `flow:incident-to-cause`
- `organization:root` → `mapping:maya-incident-observe`
- `organization:root` → `mapping:maya-learning-negmem`
- `organization:root` → `mapping:maya-roi-ledger`
- `organization:root` → `persona:maya`
- `organization:root` → `principle:empower-not-police`
- `organization:root` → `principle:transfer-of-mastery`
