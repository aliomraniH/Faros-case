# memory/ — assist-memory coordination layer

The knowledge tree lives in git (durable, diff-able, reviewable). **assist-memory** holds the
*coordination* layer git can't: architecture decisions and website insights any surface can
bootstrap from, the web→Cowork handoff baton, and reconcilable claims about repo state.

- **Namespace:** `dev/faros-case`
- **Server name to call:** `assist-memory` (tools as `assist-memory:memory_save`, etc.)

## Key map (intended contents)

| key | kind | what |
|---|---|---|
| `project/charter` | decision | The project's goal + surfaces + endstate. |
| `arch/determinism-rule` | decision | The three rules (traverse vs author, typed+provenance, tree-is-contract). |
| `arch/node-schema` | knowledge | Node schema summary; 13 seed nodes validate. |
| `arch/agents` | knowledge | Curator/Advisor split and contracts. |
| `insight/thesis` | knowledge | Faros thesis (door/room, outcome-maxxing), validated vs. Jun 2026 site. |
| `insight/pillars` | knowledge | Observe (shipped) / Optimize (partial) / Govern (partial). |
| `insight/proof` | knowledge | Vimeo, SmartBear (vendor), MIT NANDA (independent), company facts. |
| `insight/market-corrections` | knowledge | EU AI Act deferral + 18-month-window-is-inference + causal-ML method. |
| `insight/persona-maya` | knowledge | The buyer persona + the squeeze. |
| `open/pricing` | todo | The open commercial question + Ali's intended pricing call. |
| `repo/seed-commit` | claim | Repo state — reconcilable against GitHub once pushed. |
| `handoff/web-to-cowork` | handoff | The baton: fetch → curate → approve → advise → simulate. |

## ⚠ Server was unreachable at seed time

Every assist-memory call from the seeding session returned `{"code":32600,"message":"Session
terminated"}`. Per the skill's degradation rule, nothing was assumed written. The intended writes are
**staged verbatim** in `memory/replay/`:

- `memory/replay/all-payloads.json` — all 12 calls as one array.
- `memory/replay/NN_<key>.json` — one file per call.

Each is the exact `{tool, args}` shape. To apply once the server is back, from any surface with
assist-memory loaded, replay them in order (the `repo/seed-commit` claim should be saved *after* the
push so `coord_reconcile` can verify it).

## Bootstrap sequence (for any surface picking this up)
1. `assist-memory:coord_health("dev/faros-case")` — see what's there / what's stale.
2. `assist-memory:memory_list` (or `memory_search`) to load the `insight/*` and `arch/*` entries.
3. `assist-memory:handoff_load("handoff/web-to-cowork", "dev/faros-case")` — get the next steps.
4. If relying on `repo/seed-commit`, `coord_reconcile` first (don't trust a claim at face value).
