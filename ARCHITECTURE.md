# ARCHITECTURE

The design principle, stated precisely, and the contracts that hold it together.

## 1. Why deterministic-with-human-supervision

The failure mode we are designing against is the one MIT NANDA named for enterprise AI: systems
that **don't learn, don't retain context, and improvise** — producing plausible output with no
traceable link to a human-approved intent. An advisor agent that free-associates over marketing
copy reproduces exactly that failure inside a sales conversation.

So the org's picture is not a prompt; it is a **tree of typed, approved nodes**. Determinism comes
from three places:

- **Structure is fixed.** Node types and their required fields are defined by
  `schemas/knowledge-node.schema.json`. An agent cannot create a node that doesn't validate.
- **Authority is gated.** Agents may write nodes only in `status: proposed`. Only a human moves a
  node to `status: approved`. Advisors answer **only** from approved nodes.
- **Lineage is explicit.** Every node names its `parent`, its `provenance`, and (for sourced nodes)
  the exact Faros page + retrieval timestamp it came from.

This is the same shape as Faros's own governance pitch — *"policies set centrally, full provenance,
a human still reviews and merges"* — turned inward on the knowledge that drives the demo.

## 2. The tree

A single rooted tree. The root is the **organization-in-question** (the buyer's company as the
advisor models it). Five node types hang beneath it:

```
root: organization
├── faros        — what Faros offers (platform / capability / solution / offering-leaf)
├── persona      — who in the org we're advising (buyer, influencers, users)
├── flow         — the work the org does, and where AI touches it
├── principle    — the team's engineering principles & culture to protect/amplify
└── mapping      — edges that connect a persona's flow/pain to a faros node (the answer substrate)
```

`mapping` nodes are the important ones: a mapping says *"persona P, doing flow F, feels pain X →
Faros capability C addresses it, with evidence E and honesty-label H."* An advisor answer is a
walk from a persona pain to one or more mapping nodes.

### Node types (summary — full schema in `/schemas`)

| type | answers the question | key fields |
|---|---|---|
| `faros` | "what does Faros do?" | `layer` (platform/capability/solution), `claim`, `shipped_status`, `source` |
| `persona` | "who are we advising?" | `role`, `org_context`, `pressures`, `success_criteria` |
| `flow` | "what work happens here?" | `stage`, `actors`, `ai_touchpoints`, `current_tools` |
| `principle` | "what must we protect?" | `statement`, `why_it_matters`, `risk_if_lost` |
| `mapping` | "how does Faros help *this*?" | `persona_ref`, `flow_ref`, `pain`, `faros_ref`, `evidence`, `honesty` |

### Provenance (every node)

```
provenance: sourced | inferred | user-intent
```

- `sourced` — derived from a specific Faros page (or the press release / Field Guide). Must carry
  `source.url` and `source.retrieved_at`.
- `inferred` — our analytical reasoning. Allowed, but must be labelled so an advisor can flag it.
- `user-intent` — a want Ali stated. The deterministic gate: agents build *toward* these.

### Honesty label (mapping nodes especially)

```
honesty: shipped | roadmap | inference
```

Carries forward the discipline from the demo: never present a roadmap capability as shipped. An
advisor must surface this label when it answers (e.g. "Faros traces this today" vs. "this is on the
roadmap").

## 3. The agents (Claude-managed, run separately)

Two roles, deliberately split so that writing and answering never blur:

- **Curator** — reads fetched website JSON (`fetch/raw/*.json`), proposes `faros` and `mapping`
  nodes in `status: proposed`, never approves its own work. Its job is breadth + accurate sourcing.
- **Advisor** — answers a user's "how can Faros help with X?" by traversing **approved** nodes
  only. Returns a structured answer: the matched pain, the Faros node(s), the evidence, the honesty
  label, and the node IDs it used. If no approved node matches, it says so and emits a curator task.

Orchestration (`agents/orchestration.md`) defines the loop: fetch → curator proposes → human
approves → advisor answers → gaps found → curator proposes again. The human is in the loop at
exactly one place — approval — and that single gate is what makes the whole thing deterministic.

## 4. Memory & coordination (assist-memory)

The tree lives in git (durable, reviewable, diff-able). **assist-memory** holds the *coordination*
layer that git doesn't:

- the **architecture decisions** (`kind: decision`) and **website insights** (`kind: knowledge`),
  so any surface can bootstrap without re-reading the whole repo;
- **handoffs** (`kind: handoff`) — the baton from Claude web to Cowork/Desktop;
- **claims** (`kind: claim`) about repo state (e.g. "fetch/raw/platform.json committed on `main`")
  that `coord_reconcile` can verify against GitHub.

Namespace: **`dev/faros-case`**. See `memory/README.md` for the full key map and replay payloads.

## 5. Why this is defensible in the room

If a panelist asks *"isn't your advisor just a chatbot over marketing copy?"* the answer is the
architecture: typed nodes, human-gated approval, provenance and honesty labels on every answer,
and a git history that shows exactly which human approved which claim when. It is the product's own
governance philosophy, applied to itself.
