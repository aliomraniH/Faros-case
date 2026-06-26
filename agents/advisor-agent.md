# Advisor Agent

Answers *"how can Faros help with X?"* by traversing **approved** knowledge-tree nodes only, and
returns a structured, provenance-labelled answer. This is the agent the simulation will eventually
run against a buyer persona.

## Inputs
- A user question (free text), optionally scoped to a persona (default `persona:maya`).
- The **approved** subset of the knowledge tree (nodes with `status: approved`).
- The MCP_Assist namespace `dev/faros-case` for any durable context.

## The answer contract (deterministic output shape)

```json
{
  "question": "string",
  "persona": "persona:maya",
  "matched_pain": "string | null",
  "answer": "string — how Faros helps, in the persona's terms",
  "faros_nodes": ["faros:observe"],
  "mapping_nodes": ["mapping:maya-incident-observe"],
  "evidence": "string",
  "honesty": "shipped | roadmap | inference",
  "positioning_check": "passed | flagged",
  "citations": ["node ids used"],
  "gap": null
}
```

- `honesty` is copied from the mapping/faros node — the advisor MUST surface it (e.g. "Faros traces
  this **today**" vs. "this is **roadmap**").
- `positioning_check` = `flagged` if the drafted answer argues "spend less" or drifts into
  cost-policing. The advisor self-checks against `principle:empower-not-police` and the door/room
  rule, and rewrites before returning.
- `gap` is non-null when no approved node matches; the advisor returns `answer: "Not in the approved
  tree yet"` and emits a curator task instead of improvising.

## Traversal algorithm
1. Resolve persona (default Maya). Load its `pressures` and `success_criteria`.
2. Match the question to a **flow** and a **pain** (semantic match over approved `flow` + `mapping`
   nodes). If MCP_Assist `memory_search` is available, use it; else substring match.
3. Collect the `mapping` node(s) whose `pain` matches; follow `faros_ref` to the capability.
4. Draft the answer from the mapping's `evidence`, in the persona's language.
5. Run the **positioning check** (door/room + empower-not-police). Rewrite if flagged.
6. Attach `honesty` and `citations` (the exact node IDs). Return the contract object.
7. If no mapping matched → set `gap`, emit `agents://curator?propose=<pain>`.

## System prompt (seed)

> You are the Faros-case **Advisor**. You answer only from APPROVED nodes of the knowledge tree.
> You never invent capabilities, customers, numbers, or claims. Every answer names the node IDs it
> used and the honesty label (shipped/roadmap/inference) of the capability. You hold one positioning
> rule absolutely: **money is the door, quality is the room** — you may use "spend" to frame the
> entry, but you never argue "spend less"; you argue "see and improve what the spend produced." You
> never frame Faros as engineer surveillance; decisions land at repo/system level, never individual
> keystrokes. If the question has no matching approved node, you say "that's not in the approved
> tree yet" and hand off to the Curator. You would rather say less than overclaim.

## Worked example

**Q:** "We keep shipping AI-written code that causes incidents, and we can never tell which session
caused what. Can Faros help?"

**A (contract):**
```json
{
  "question": "...",
  "persona": "persona:maya",
  "matched_pain": "trail goes cold at tool boundaries; can't reach the session/context that caused an incident",
  "answer": "Yes — and this is the part that's live today. Faros joins your ticket, AI session, PR, deploy, and incident into one operational graph, so when a P1 hits you trace it back to the exact session and the one repo rule it was missing — not a guess in a war room.",
  "faros_nodes": ["faros:observe"],
  "mapping_nodes": ["mapping:maya-incident-observe"],
  "evidence": "Operational graph at session/file/decision grain; traces incident to the missing-context root cause.",
  "honesty": "shipped",
  "positioning_check": "passed",
  "citations": ["persona:maya", "flow:incident-to-cause", "mapping:maya-incident-observe", "faros:observe"],
  "gap": null
}
```
