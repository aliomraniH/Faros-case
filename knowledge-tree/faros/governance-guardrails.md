---
id: faros:governance-guardrails
type: faros
title: Governance & Guardrails — policy, flags, code tagging
parent: faros:govern
provenance: sourced
status: proposed
proposed_by: cowork-curator
honesty: inference
source:
  kind: faros-website
  url: https://www.faros.ai/platform/ai-transformation
  retrieved_at: "2026-06-26T23:57:50Z"
  quote_or_derivation: "Enforce governance and guardrails at scale."
fields:
  layer: sub-capability
  pillar: govern
tags: [faros, govern, guardrails, proposed, conflict-flag]
---

The AI Transformation page describes IDE-level governance: flag PRs needing extra scrutiny,
real-time code-quality checks, policy orchestration for risk mitigation, distinguish human vs.
machine-generated code. **Conflict flag:** the seed `faros:govern` node is `honesty: roadmap` and
offering.json marks policy/compensating-controls `partial`; the live page reads more shipped.
Proposed `honesty: inference` and flagged for Ali. The seed's key distinction — *compensating
controls over hard blocks*, with a human still merging — is the design choice to preserve when
approving, and keeps this consistent with `principle:empower-not-police`.
