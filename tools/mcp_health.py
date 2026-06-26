#!/usr/bin/env python3
"""
mcp_health.py — quick reachability check for the MCP_Assist memory server.

Exit 0 if the endpoint answers an MCP initialize handshake; 1 otherwise.
This is a *transport* check, not a name check: if it fails with the server
returning errors (e.g. "Session terminated"), the connector name is fine and
the server itself is asleep/crashing (the Replit app cold-starts).

Usage: python3 tools/mcp_health.py [endpoint_url]
Default endpoint: env MCP_ASSIST_URL or the known Replit URL.
"""
import sys, os, json, urllib.request, urllib.error

URL = (len(sys.argv) > 1 and sys.argv[1]) or os.environ.get(
    "MCP_ASSIST_URL", "https://mcp-assist-memory.replit.app/mcp"
)

def post(method, params=None, _id=1):
    body = json.dumps({"jsonrpc": "2.0", "id": _id, "method": method,
                       "params": params or {}}).encode()
    req = urllib.request.Request(
        URL, data=body, method="POST",
        headers={"Content-Type": "application/json",
                 "Accept": "application/json, text/event-stream"})
    with urllib.request.urlopen(req, timeout=15) as r:
        raw = r.read().decode(errors="replace")
        # streamable-http may return SSE framing; grab the first JSON object
        if raw.lstrip().startswith("data:"):
            for line in raw.splitlines():
                if line.startswith("data:"):
                    return json.loads(line[5:].strip())
        return json.loads(raw)

def main():
    try:
        resp = post("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "faros-case-health", "version": "1.0"},
        })
        if "result" in resp:
            print(f"✓ MCP_Assist reachable at {URL}")
            return 0
        print(f"✗ MCP_Assist responded with an error: {resp.get('error')}")
        return 1
    except urllib.error.URLError as e:
        print(f"✗ MCP_Assist unreachable at {URL}: {e}")
        return 1
    except Exception as e:
        print(f"✗ MCP_Assist check failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
