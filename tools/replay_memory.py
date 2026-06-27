#!/usr/bin/env python3
"""
replay_memory.py — replay the staged assist-memory payloads over raw HTTP.

This is a FALLBACK. The preferred path is to let Claude Code (which has the
assist-memory connector loaded) replay them as native tool calls — see
prompts/claude-code-seed-memory.md. Use this only if you want to seed memory
from a plain shell without Claude in the loop.

Reads memory/replay/all-payloads.json (a list of {tool, args}) and issues a
tools/call for each over the MCP streamable-HTTP endpoint.

Usage:
  python3 tools/replay_memory.py [endpoint_url]
Env:
  MCP_ASSIST_URL  override endpoint (default: known Replit URL)

Note: the 'repo/seed-commit' claim is best replayed AFTER the push, so
coord_reconcile can verify it. This script skips it unless --include-claim is set.
"""
import sys, os, json, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAYLOADS = os.path.join(ROOT, "memory", "replay", "all-payloads.json")
URL = os.environ.get("MCP_ASSIST_URL", "https://mcp-assist-memory.replit.app/mcp")
INCLUDE_CLAIM = "--include-claim" in sys.argv
args_pos = [a for a in sys.argv[1:] if not a.startswith("--")]
if args_pos:
    URL = args_pos[0]

_session = {"id": None}

def _post(method, params=None, _id=1):
    headers = {"Content-Type": "application/json",
               "Accept": "application/json, text/event-stream"}
    if _session["id"]:
        headers["Mcp-Session-Id"] = _session["id"]
    body = json.dumps({"jsonrpc": "2.0", "id": _id, "method": method,
                       "params": params or {}}).encode()
    req = urllib.request.Request(URL, data=body, method="POST", headers=headers)
    with urllib.request.urlopen(req, timeout=20) as r:
        sid = r.headers.get("Mcp-Session-Id")
        if sid:
            _session["id"] = sid
        raw = r.read().decode(errors="replace")
        if raw.lstrip().startswith("data:"):
            for line in raw.splitlines():
                if line.startswith("data:"):
                    return json.loads(line[5:].strip())
        return json.loads(raw) if raw.strip() else {}

def call_tool(name, arguments, _id):
    return _post("tools/call", {"name": name, "arguments": arguments}, _id)

def main():
    if not os.path.exists(PAYLOADS):
        print(f"No payloads at {PAYLOADS}", file=sys.stderr); return 1
    payloads = json.load(open(PAYLOADS))

    print(f"Initializing MCP session at {URL} …")
    try:
        init = _post("initialize", {
            "protocolVersion": "2024-11-05", "capabilities": {},
            "clientInfo": {"name": "faros-case-replay", "version": "1.0"}}, _id=0)
        if "error" in init:
            print(f"✗ initialize failed: {init['error']}"); return 1
        try:
            _post("notifications/initialized", {})  # best effort
        except Exception:
            pass
    except urllib.error.URLError as e:
        print(f"✗ endpoint unreachable: {e}\n  The Replit app is likely asleep. "
              f"Open the URL once in a browser to wake it, then retry."); return 1

    ok = fail = skipped = 0
    for i, p in enumerate(payloads, 1):
        tool = p["tool"].split(":", 1)[-1]  # 'assist-memory:memory_save' -> 'memory_save'
        args = p["args"]
        key = args.get("key", "?")
        if args.get("kind") == "claim" and not INCLUDE_CLAIM:
            print(f"  · skip claim '{key}' (replay after push, or pass --include-claim)")
            skipped += 1; continue
        try:
            resp = call_tool(tool, args, _id=i)
            if "error" in resp:
                print(f"  ✗ {tool} {key}: {resp['error']}"); fail += 1
            else:
                print(f"  ✓ {tool} {key}"); ok += 1
        except Exception as e:
            print(f"  ✗ {tool} {key}: {e}"); fail += 1

    print(f"\nDone: {ok} ok, {fail} failed, {skipped} skipped.")
    return 0 if fail == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
