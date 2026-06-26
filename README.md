# Faros-case

A **deterministic, human-supervised knowledge tree** that maps Faros AI's offering to a
specific buyer persona, plus **Claude-managed advisor agents** that answer *"how can Faros
help me?"* through structured question-and-answer — grounded only in approved nodes of the tree.

> Repo: `github.com/aliomraniH/Faros-case`
> Status: **seed** (this commit establishes structure, schemas, and the initial knowledge tree).

---

## The idea in one paragraph

Most "AI advisor" demos let an agent free-associate over a pile of marketing copy. This project
does the opposite. We build the organization's picture — Faros's offering, the buyer's flows,
the team's principles and culture — as an **explicit tree of typed nodes**. Agents do **not**
invent that tree; they **propose** additions and **traverse** an already-approved tree. The tree
is the deterministic substrate; **a human approves every node before an agent may rely on it.**
The result is an advisor whose every answer is traceable to a node a human signed off on — the
same "observe → attribute → govern with provenance" discipline Faros itself sells, applied to the
sales conversation about Faros.

## Architecture at a glance

```
        ┌───────────────────────────────────────────────────────────────┐
        │  HUMAN (Ali)  — author of intent, approver of every node       │
        └───────────────┬───────────────────────────────────────────────┘
                        │ wants / approvals (deterministic gate)
                        ▼
   ┌────────────────────────────────────────────────────────────────────┐
   │  KNOWLEDGE TREE  (this repo, /knowledge-tree)                       │
   │  typed nodes: faros · persona · flow · principle · mapping         │
   │  every node carries provenance: sourced | inferred | user-intent   │
   └───────┬──────────────────────────────────────────────┬─────────────┘
           │ traverse (read-only)                          │ propose (write, needs approval)
           ▼                                               ▼
   ┌───────────────────────┐                     ┌──────────────────────────┐
   │  ADVISOR AGENTS        │                     │  CURATOR AGENT            │
   │  (Claude-managed)      │                     │  proposes new nodes from  │
   │  Q&A: "how can Faros    │                    │  fetched website JSON,    │
   │  help with X?"          │                    │  flags for human review   │
   └───────────────────────┘                     └──────────────────────────┘
           ▲                                               ▲
           │ structured answers                            │ raw JSON
           │                                               │
   ┌───────┴───────────────┐                     ┌─────────┴────────────────┐
   │  MCP_Assist memory     │                    │  FETCH (Cowork/Desktop)   │
   │  architecture + insights│                   │  faros.ai → JSON          │
   │  cross-surface handoffs │                   │  /fetch/raw/*.json        │
   └────────────────────────┘                    └──────────────────────────┘
```

Three rules make it deterministic, not vibes:

1. **Agents traverse; humans author.** An agent may *propose* a node (`status: proposed`) but may
   only *answer from* nodes a human has set to `status: approved`. (Mirrors Faros's "policy +
   human review" governance.)
2. **Every node is typed and has provenance.** No untyped free text. Provenance is one of
   `sourced` (verbatim/derived from a cited Faros page), `inferred` (our reasoning, labelled), or
   `user-intent` (Ali's stated want). An advisor must show provenance when it answers.
3. **The tree is the contract.** Answers cite node IDs. If the answer isn't in the tree, the agent
   says "not in the approved tree" and routes to the curator to propose it — it does not improvise.

## Layout

| Path | What lives here |
|---|---|
| `knowledge-tree/` | The tree itself — typed Markdown+frontmatter nodes (see `schemas/knowledge-node.schema.json`). |
| `knowledge-tree/faros/` | What Faros is: platform, capabilities, solutions, offering (`offering.json`). |
| `knowledge-tree/personas/` | Buyer personas. `maya.md` is the seed persona. |
| `knowledge-tree/flows/` | Mapping of the buyer's flows (the work that happens, where AI touches it). |
| `knowledge-tree/principles/` | Team principles & engineering culture the org wants to protect/amplify. |
| `knowledge-tree/mapping/` | The simplest-version deliverable: persona ↔ offering mapping. |
| `schemas/` | JSON schemas: the node schema, the fetched-page schema, the offering schema. |
| `agents/` | Agent specifications (advisor, curator, orchestration) — what Claude runs, separately. |
| `fetch/` | Instructions + targets for Cowork/Desktop to pull faros.ai pages as JSON into `fetch/raw/`. |
| `memory/` | What's mirrored into MCP_Assist, and replay payloads to (re)seed it. |

## How the surfaces divide the work

- **Claude web (here):** authored this seed — structure, schemas, initial tree, persona mapping,
  agent specs, and the MCP_Assist replay payloads. Insight source: the press release, the Field
  Guide, and a June 2026 market-research pass.
- **Claude Cowork / Claude Desktop:** run `fetch/INSTRUCTIONS.md` — fetch the Platform,
  Capabilities, and Solutions pages from faros.ai as JSON into `fetch/raw/`, then let the curator
  agent propose tree nodes from them for human approval.
- **MCP_Assist:** durable, cross-surface memory of the architecture and website insights, plus the
  handoff baton between web and Cowork/Desktop. See `memory/README.md`.

## Current state & honest gaps

- The knowledge tree is seeded from **already-gathered** material (press release, Field Guide,
  market research). Nodes derived from a **live fetch** of faros.ai are *not yet present* — that's
  the Cowork/Desktop step.
- The MCP_Assist server was **unreachable** when this seed was authored (every call returned
  "Session terminated"). The intended memory writes are staged as **replay payloads** in
  `memory/replay/` so they can be applied verbatim once the server is back. Nothing was silently
  assumed to have been written.
- Pricing of Faros is the one open commercial question carried forward (see persona/mapping notes).

## License / use

Private working artifact for an interview exercise. Not affiliated with Faros AI. All Faros-sourced
content is attributed and used for analysis; treat `fetch/raw/*` as third-party content under
Faros's terms.
