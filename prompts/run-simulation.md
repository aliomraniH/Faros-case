# Prompt — Claude Desktop coding · run the Advisor simulation

You have local file access to this repo. Read `sim/README.md` and `agents/advisor-agent.md` first.

1. Ensure deps: `pip install pyyaml jsonschema` (quiet is fine).
2. Validate the tree: `python3 tools/validate_nodes.py` (must exit 0).
3. Run the batch: `python3 sim/run.py --batch sim/questions.seed.json`. Show me the scorecard.
4. For EACH answered result, produce a `polished_answer`: rewrite the engine's draft in Maya's voice
   using ONLY the matched node's evidence — introduce NO new facts, capabilities, customers, or
   numbers. Preserve the citations and the honesty label exactly. If polishing would require a fact
   that isn't in the cited nodes, stop and say so instead.
5. For each GAP, write the one-line curator task it implies (what mapping would need to exist) and
   append it to `agents/review-queue.md` under a "## Gaps found by simulation" heading.
6. For any result where `positioning_check` is flagged or `score.total < 3`, call it out and propose
   the fix (usually: tighten the node's evidence, or correct its honesty label) — but DO NOT change
   any node's `status` or `approved_by` (that's Ali's gate).
7. Optional: refresh the web UI with `python3 sim/run.py --export` so `sim/web/index.html` reflects
   the current approved tree.

Then let me drive it live: I'll give you buyer questions one at a time; run
`python3 sim/run.py --once "<question>"` (or reason over the approved nodes directly) and return the
contract + your polished_answer. Never answer from a node that isn't `status: approved`.
