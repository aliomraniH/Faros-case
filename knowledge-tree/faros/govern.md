---
id: faros:govern
type: faros
title: Govern — policy, distributed context, provenance
parent: faros:root
provenance: sourced
status: approved
approved_by: ali
proposed_by: claude-web
honesty: roadmap
source:
  kind: press-release
  quote_or_derivation: "Policies set centrally; banned model or missing context shows up; audit trail from ticket to shipped change."
fields:
  layer: capability
  pillar: govern
tags: [faros, govern, partial]
---

Central policy, distributed context kept in sync across repos, full provenance. The design
choice that matters for the demo: **compensating controls over hard blocks** — instead of blocking
an unreviewed merge and killing velocity, require shipping behind a feature flag. Guardrails, not
gates. **A human still reviews and merges** — this is the line that defuses the surveillance fear.
Negative-memory write-back (a failed session's lesson written into repo context) is the roadmap
edge here.
