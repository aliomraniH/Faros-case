# Prompt — Curator (Claude Code or Cowork) · propose nodes from fetched JSON

Read `agents/curator-agent.md` and the existing `knowledge-tree/00-index.md` (to avoid duplicates).
Then read every `fetch/raw/*.json` (ignore `_example.json`).

Produce proposed nodes:
- One `faros` node per distinct named capability/solution not already in the tree. Set
  `provenance: sourced` with a `source` block (the page url + retrieved_at + a <15-word
  paraphrase/quote), an honest `shipped|roadmap|inference` label, `status: proposed`,
  `proposed_by: curator-agent`.
- Candidate `mapping` nodes linking `persona:maya` flows/pains to the new capabilities,
  `honesty: inference`, `status: proposed`.
- If a fetched fact conflicts with an existing approved node (e.g. connector count changed), do NOT
  overwrite — propose an update and flag the conflict in `agents/review-queue.md`.

Append every proposed node to `agents/review-queue.md`. Run `python3 tools/validate_nodes.py` (exit
0). Never approve anything. List what you proposed and from which page.
