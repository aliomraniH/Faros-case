# Prompt — Claude Code · seed MCP_Assist memory

The MCP_Assist connector is configured in `.mcp.json` (server name `MCP_Assist`, namespace
`dev/faros-case`).

1. Call `mcp__MCP_Assist__coord_health` for namespace `dev/faros-case`. If it errors with "Session
   terminated"/unreachable, tell me — the Replit app is asleep; I'll wake it and we retry. Do not
   fake success.
2. If healthy, read `memory/replay/all-payloads.json`. For each entry, call the named tool
   (`memory_save` or `handoff_save`) with its exact `args` (namespace, key, kind, value, tags, meta,
   source_surface). Preserve keys verbatim.
3. **Skip** the `repo/seed-commit` entry (kind=claim) for now — replay it only AFTER the repo is
   pushed, so it can be verified.
4. After the push exists, save the `repo/seed-commit` claim, then run
   `mcp__MCP_Assist__coord_reconcile` for `dev/faros-case` and report each verdict
   (current/stale/unverifiable). If the backend has no GitHub token, expect `unverifiable`.
5. Confirm with `mcp__MCP_Assist__memory_list` that the `insight/*`, `arch/*`, and `open/pricing`
   keys are present. List what you wrote.
