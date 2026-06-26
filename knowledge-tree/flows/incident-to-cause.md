---
id: flow:incident-to-cause
type: flow
title: Flow — from production incident to root cause
parent: organization:root
provenance: inferred
status: approved
approved_by: ali
proposed_by: claude-web
fields:
  stage: post-delivery
  actors: [on-call, staff engineer, the AI agent that wrote the change]
  ai_touchpoints: ["AI session generated the PR", "context the session did/didn't have"]
  current_tools: [incident tool, delivery dashboard, cost tool, catalog]
tags: [flow, incident, signature]
---

The signature flow. A P1 fires (checkout down). Today the trail goes cold the moment it crosses
a tool boundary — the incident tool knows the incident, the dashboard knows the PR, the cost tool
knows the session spend, but **nothing joins them**, so 'which session, missing which context,
caused this?' is unanswerable. This is the flow the Observe pillar lights up, and the one the demo's
Beat 3 walks live.
