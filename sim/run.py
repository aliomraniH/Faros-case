#!/usr/bin/env python3
"""
run.py — drive the Faros-case advisor simulation.

Modes:
  python3 sim/run.py --interactive            # REPL: type buyer questions, get scored answers
  python3 sim/run.py --batch sim/questions.seed.json   # run a question set, print a scorecard
  python3 sim/run.py --export                 # write sim/web/tree.js for the local HTML UI
  python3 sim/run.py --once "your question"   # single question, JSON out

Options:
  --persona persona:maya       # default persona
  --json                       # machine-readable output (interactive prints JSON too)

Runs fully offline. Intended to be driven by Claude Desktop coding (local file access),
but works as a plain CLI.
"""
import sys, os, json, argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine  # noqa: E402

C = {
    "dim": "\033[2m", "b": "\033[1m", "grn": "\033[32m", "yel": "\033[33m",
    "red": "\033[31m", "cya": "\033[36m", "mag": "\033[35m", "x": "\033[0m",
}
def col(s, c): return f"{C[c]}{s}{C['x']}"


def badge_honesty(h):
    return {"shipped": col("● shipped", "grn"),
            "roadmap": col("◐ roadmap", "yel"),
            "inference": col("○ inference", "mag")}.get(h, h or "")


def render(res, as_json=False):
    if as_json:
        print(json.dumps(res, indent=2)); return
    print()
    if res.get("gap"):
        print(col("  ✗ GAP — no approved node", "red"))
        print("   " + res["answer"])
        print(col(f"   match_score={res['match_score']} (below threshold)", "dim"))
        return
    print(col("  ▸ " + res["answer"], "b"))
    print()
    print(f"   {col('matched pain','dim')}  {res['matched_pain']}")
    print(f"   {col('honesty','dim')}      {badge_honesty(res['honesty'])}")
    pc = res["positioning_check"]
    print(f"   {col('positioning','dim')}  " +
          (col("passed", "grn") if pc == "passed" else col("FLAGGED", "red")))
    print(f"   {col('cites','dim')}        " + ", ".join(col(c, "cya") for c in res["citations"]))
    s = res["score"]
    bar = "".join("✓" if s[k] else "✗" for k in ("citations_ok", "honesty_ok", "positioning_ok"))
    print(f"   {col('score','dim')}        {bar}  ({s['total']}/3)   "
          + col(f"match={res['match_score']}", "dim"))


def run_batch(tree, path, persona, as_json):
    qs = json.load(open(path))
    items = qs["questions"] if isinstance(qs, dict) else qs
    results, totals = [], {"answered": 0, "gaps": 0, "perfect": 0, "score_sum": 0, "max": 0}
    for q in items:
        question = q["q"] if isinstance(q, dict) else q
        p = (q.get("persona") if isinstance(q, dict) else None) or persona
        res = engine.advise(tree, question, p)
        results.append(res)
        if res.get("gap"):
            totals["gaps"] += 1
        else:
            totals["answered"] += 1
            totals["score_sum"] += res["score"]["total"]; totals["max"] += 3
            if res["score"]["total"] == 3:
                totals["perfect"] += 1
        if not as_json:
            print(col(f"\nQ: {question}", "b"))
            render(res)
    if as_json:
        print(json.dumps({"results": results, "totals": totals}, indent=2)); return
    print(col("\n" + "─" * 60, "dim"))
    print(col("SCORECARD", "b"))
    print(f"  answered: {totals['answered']}   gaps: {totals['gaps']}   "
          f"perfect (3/3): {totals['perfect']}")
    if totals["max"]:
        pct = 100 * totals["score_sum"] / totals["max"]
        print(f"  quality:  {totals['score_sum']}/{totals['max']} ({pct:.0f}%) "
              "across citations · honesty · positioning")
    print(col("  gaps are not failures — they're curator tasks (questions the tree doesn't cover yet).", "dim"))


def repl(tree, persona):
    print(col("Faros-case advisor simulation", "b") + col("  (deterministic, offline)", "dim"))
    print(col(f"persona: {persona}   ", "cya") +
          col("commands: :persona <id>  :personas  :seed  :json  :help  :quit", "dim"))
    as_json = False
    seed_path = os.path.join(os.path.dirname(__file__), "questions.seed.json")
    while True:
        try:
            line = input(col("\nask> ", "grn")).strip()
        except (EOFError, KeyboardInterrupt):
            print(); break
        if not line:
            continue
        if line in (":q", ":quit", ":exit"):
            break
        if line == ":help":
            print("  type a buyer question, or:")
            print("   :persona <id>   switch persona (e.g. :persona persona:maya)")
            print("   :personas       list approved personas")
            print("   :seed           list seed questions")
            print("   :json           toggle JSON output")
            print("   :quit")
            continue
        if line == ":json":
            as_json = not as_json; print(col(f"  json output: {as_json}", "dim")); continue
        if line == ":personas":
            for p in tree.personas():
                print(f"   {col(p['id'],'cya')}  {p['title']}")
            continue
        if line == ":seed":
            if os.path.exists(seed_path):
                for q in json.load(open(seed_path))["questions"]:
                    print("   • " + (q["q"] if isinstance(q, dict) else q))
            continue
        if line.startswith(":persona "):
            pid = line.split(" ", 1)[1].strip()
            if tree.get(pid):
                persona = pid; print(col(f"  persona → {persona}", "dim"))
            else:
                print(col(f"  no approved persona '{pid}'", "red"))
            continue
        res = engine.advise(tree, line, persona)
        render(res, as_json)


def main():
    ap = argparse.ArgumentParser(description="Faros-case advisor simulation")
    ap.add_argument("--interactive", "-i", action="store_true")
    ap.add_argument("--batch", metavar="FILE")
    ap.add_argument("--once", metavar="QUESTION")
    ap.add_argument("--export", action="store_true")
    ap.add_argument("--persona", default="persona:maya")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.export:
        path, n = engine.export_web()
        print(f"exported {n} approved nodes → {path}")
        return

    tree = engine.Tree()
    if not tree.mappings():
        print(col("No approved mapping nodes found — nothing to advise from yet.", "yel"))
        print("Approve some mapping nodes (agents/HUMAN-GATE.md) and retry.")
        # still allow REPL to show gaps

    if args.once:
        render(engine.advise(tree, args.once, args.persona), args.json); return
    if args.batch:
        run_batch(tree, args.batch, args.persona, args.json); return
    if args.interactive:
        repl(tree, args.persona); return
    ap.print_help()


if __name__ == "__main__":
    main()
