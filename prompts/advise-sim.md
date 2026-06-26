# Prompt — Advisor simulation (Claude Code or Cowork)

Read `agents/advisor-agent.md`. Load only nodes with `status: approved` from `knowledge-tree/`.

I will give you buyer questions (persona default `persona:maya`). For each:
1. Match it to an approved `flow` + `mapping` node(s).
2. Return the advisor contract JSON exactly as specified (matched_pain, answer, faros_nodes,
   mapping_nodes, evidence, honesty, positioning_check, citations, gap).
3. Surface the honesty label in the answer ("today" vs "roadmap"). Run the positioning check
   (door/room; empower-not-police) and rewrite if it would drift to "spend less" or surveillance.
4. If no approved node matches, set `gap` and emit a curator task — do NOT improvise an answer.

After all questions, give me a scorecard: for each answer, did it (a) cite correct nodes, (b) label
shipped/roadmap honestly, (c) hold positioning discipline? That scorecard is the eval.

First question set (paste yours, or start with these):
- "We keep shipping AI-written code that causes incidents and can't tell which session caused what. Can Faros help?"
- "My board wants to know what our AI spend bought. What can Faros show them?"
- "How do you stop the same AI mistake from happening again next week?"
- "Is this going to surveil my engineers?"
