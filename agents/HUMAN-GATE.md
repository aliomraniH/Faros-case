# The Human Gate (how to approve a node)

Agents can only ever propose. You (Ali) are the single approval gate. To approve a proposed node:

1. Open the node file under `knowledge-tree/`.
2. Read it; edit freely (fix the claim, tighten the evidence, correct the honesty label).
3. In the frontmatter, set:
   ```yaml
   status: approved
   approved_by: ali
   approved_at: 2026-06-26T00:00:00Z   # real timestamp
   ```
4. Remove the node's line from `agents/review-queue.md`.

Only nodes with `status: approved` are visible to the Advisor. If you reject one, set
`status: rejected` and leave a one-line reason in the body — history is preserved in git.
