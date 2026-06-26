# Review Queue (human gate)

The Curator appends one line per **proposed** node here. Ali reviews, edits the node file if needed,
then sets `status: approved` (+ `approved_by`, `approved_at`) in the node's frontmatter. Only
approved nodes are visible to the Advisor.

| proposed node id | from source | honesty | proposed_at | reviewed? |
|---|---|---|---|---|
| _(none yet — curator runs after the first fetch batch)_ | | | | |

## Seed nodes (authored by claude-web, pre-approved by Ali for the seed commit)
These 13 nodes were authored directly in the seed and set to `approved` because Ali authored/owns
the interpretation they encode. Everything the **Curator** adds from live fetches must pass through
this queue.

See `knowledge-tree/00-index.md` for the current approved set.
