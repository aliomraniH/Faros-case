# Orchestration

The loop that keeps the system deterministic and human-supervised. One human gate (approval); two
agents that never blur roles.

```
   fetch (Cowork/Desktop)                         ┌─────────── human gate ───────────┐
   faros.ai ──► fetch/raw/*.json                  │  review agents/review-queue.md    │
        │                                          │  edit · set status: approved      │
        ▼                                          └───────────────┬───────────────────┘
   ┌──────────┐   proposes (status: proposed)                      │ approves
   │ CURATOR  │ ─────────────────────────────────────────────────►│
   └──────────┘                                                    ▼
                                                          knowledge-tree (approved nodes)
                                                                   │ traverse (read-only)
                                                                   ▼
   user question ──────────────────────────────────────────► ┌──────────┐
                                                              │ ADVISOR  │ ──► structured answer
                                                              └────┬─────┘
                                                                   │ gap? (no approved node)
                                                                   ▼
                                                          emit curator task ──► (loop)
```

## Steps
1. **Fetch.** Cowork/Desktop runs `fetch/INSTRUCTIONS.md` → `fetch/raw/*.json`. Records a `claim` in
   MCP_Assist (`fetch/batch-N`).
2. **Curate.** Curator proposes `faros`/`mapping` nodes (`status: proposed`), appends to
   `agents/review-queue.md`.
3. **Approve (human gate).** Ali reviews the queue, edits, sets `status: approved` + `approved_by`.
4. **Advise.** Advisor answers persona questions from approved nodes only, with provenance + honesty
   labels.
5. **Close gaps.** Where the Advisor finds no approved node, it emits a curator task; loop to step 2.

## When MCP_Assist is up
- Each surface bootstraps with `coord_health(dev/faros-case)` before trusting stored state.
- Fetch/commit claims are reconciled with `coord_reconcile` against `aliomraniH/Faros-case`.
- The web→Cowork baton is the handoff `handoff/web-to-cowork` (see `memory/README.md`).

## The simulation (later)
Once the approved tree has real fetched nodes, run the Advisor against the persona as a Q&A
simulation: feed it the buyer's likely questions (these can come from the panel-simulator question
set), score each answer for (a) correct node citations, (b) honest shipped/roadmap labelling, and
(c) positioning discipline (door/room, empower-not-police). That score is the system's eval.
