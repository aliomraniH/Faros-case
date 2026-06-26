---
id: mapping:maya-incident-observe
type: mapping
title: Mapping — Maya's incident-to-cause pain → Observe
parent: organization:root
provenance: inferred
status: approved
approved_by: ali
proposed_by: claude-web
honesty: shipped
fields:
  persona_ref: persona:maya
  flow_ref: flow:incident-to-cause
  pain: "When a P1 hits, the trail goes cold at every tool boundary; can't reach the session or the missing context that caused it."
  faros_ref: faros:observe
  evidence: "Operational graph joins ticket→session→PR→deploy→incident→spend; traces to the one missing repo rule."
tags: [mapping, signature, shipped]
---

**The strongest mapping — and it's shipped.** Maya's hardest unanswerable question ('which
session, missing what context, caused this incident?') is exactly what the Observe graph answers.
An advisor asked 'how does Faros help when we have a production incident from AI code?' walks from
`persona:maya` + `flow:incident-to-cause` to this node and answers with the trace, labelled
`shipped`.
