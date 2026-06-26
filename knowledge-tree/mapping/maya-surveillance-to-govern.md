---
id: mapping:maya-surveillance-govern
type: mapping
title: Mapping — 'is this surveillance?' → repo/system-level governance
parent: organization:root
provenance: inferred
status: approved
approved_by: ali
proposed_by: claude-web
honesty: shipped
fields:
  persona_ref: persona:maya
  flow_ref: flow:incident-to-cause
  pain: "Worried this becomes engineer surveillance — ranking, monitoring, individual keystroke tracking."
  faros_ref: faros:govern
  evidence: "Everything lands at the repo/system level — context rules, feature flags, traces, policy — never individual keystrokes. A human still reviews and merges. Built to empower the team, not police it."
tags: [mapping, surveillance, empower, govern, shipped]
---

Answers the developers'-fear question. Pairs with `principle:empower-not-police`. The advisor must
say 'a human still reviews and merges' and keep the grain at repo/system level. Honest tension to
hold if pushed: Faros does support org/team/individual views with RBAC — so the governance story
matters more, not less.
