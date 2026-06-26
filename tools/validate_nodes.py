#!/usr/bin/env python3
"""
validate_nodes.py — schema + human-gate validation for the Faros-case knowledge tree.

Exit code 0 = all good; 1 = violations found (used by CI to block bad merges).

Checks:
  1. Every knowledge-tree/**/*.md node has valid YAML frontmatter and validates
     against schemas/knowledge-node.schema.json.
  2. IDs are unique.
  3. Every parent reference resolves to a real node (except the single root,
     whose parent is the literal "null").
  4. HUMAN GATE: a node with status == "approved" MUST have approved_by set.
     This is the mechanical enforcement of "agents propose, humans approve."
  5. provenance == "sourced" MUST carry a source block (schema also enforces).
"""
import sys, glob, os, json

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. pip install pyyaml", file=sys.stderr); sys.exit(2)
try:
    from jsonschema import Draft202012Validator
except ImportError:
    print("ERROR: jsonschema not installed. pip install jsonschema", file=sys.stderr); sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA = os.path.join(ROOT, "schemas", "knowledge-node.schema.json")
TREE = os.path.join(ROOT, "knowledge-tree")

def load_frontmatter(path):
    txt = open(path, encoding="utf-8").read()
    if not txt.startswith("---"):
        return None
    parts = txt.split("---", 2)
    if len(parts) < 3:
        return None
    return yaml.safe_load(parts[1])

def main():
    schema = json.load(open(SCHEMA))
    validator = Draft202012Validator(schema)

    errors = []
    nodes = {}
    files = sorted(glob.glob(os.path.join(TREE, "**", "*.md"), recursive=True))
    if not files:
        print("No node files found under knowledge-tree/", file=sys.stderr)
        return 1

    for path in files:
        rel = os.path.relpath(path, ROOT)
        data = load_frontmatter(path)
        if data is None:
            # index files and prose-only docs are allowed if they have no 'id'
            head = open(path, encoding="utf-8").read(40)
            if "id:" in head:
                errors.append(f"{rel}: could not parse frontmatter")
            continue
        if "id" not in data:
            continue  # not a node (e.g. index)

        # schema
        for e in validator.iter_errors(data):
            errors.append(f"{rel}: schema: {e.message}")

        nid = data.get("id")
        if nid in nodes:
            errors.append(f"{rel}: duplicate id '{nid}' (also in {nodes[nid]['_file']})")
        data["_file"] = rel
        nodes[nid] = data

        # HUMAN GATE
        if data.get("status") == "approved" and not data.get("approved_by"):
            errors.append(f"{rel}: HUMAN-GATE violation — status=approved but approved_by is empty. "
                          f"Agents may only set status=proposed; a human must approve.")

        # sourced needs a source block (belt-and-suspenders beyond schema)
        if data.get("provenance") == "sourced" and not data.get("source"):
            errors.append(f"{rel}: provenance=sourced but no source block.")

    # parent integrity
    for nid, data in nodes.items():
        parent = data.get("parent")
        if parent in (None, "null", "None"):
            continue
        if parent not in nodes:
            errors.append(f"{data['_file']}: parent '{parent}' does not resolve to a known node.")

    # report
    if errors:
        print(f"\n✗ {len(errors)} violation(s):\n")
        for e in errors:
            print("  -", e)
        print()
        return 1

    by_status = {}
    for d in nodes.values():
        by_status[d.get("status")] = by_status.get(d.get("status"), 0) + 1
    print(f"✓ {len(nodes)} nodes valid. status breakdown: {by_status}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
