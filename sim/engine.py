#!/usr/bin/env python3
"""
engine.py — the deterministic Advisor simulation core for Faros-case.

It loads the APPROVED knowledge tree from disk, matches a buyer question to the
right flow + mapping node, drafts an answer from that node ONLY, runs the
positioning check, attaches the honesty label, and scores the result. No API key,
no network — fully offline and reviewable. This is the source of truth; the HTML
UI mirrors this logic in JS for interactivity.

Design guarantees (the whole point):
  - Answers are composed only from APPROVED nodes; if nothing matches → gap (no improvising).
  - Every answer cites the exact node IDs it used.
  - Honesty label (shipped|roadmap|inference) is carried from the node and surfaced.
  - Positioning check flags any drift to "spend less" or surveillance framing.
"""
import os, re, glob, json

try:
    import yaml
except ImportError:
    raise SystemExit("pyyaml required: pip install pyyaml")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TREE = os.path.join(ROOT, "knowledge-tree")

# Tunables (mirrored in web/index.html so the UI matches the engine)
MATCH_THRESHOLD = 0.30
STOPWORDS = set("a an the of to and or is are was were be been being do does did "
                "how what why when who which can could would should we i my our your "
                "you it this that with for from on in at as by me us them they help "
                "about into out have has had will just so if not no yes".split())
SYNONYMS = {
    "incident": {"incident", "outage", "p1", "p0", "sev", "down", "broke", "broken", "failure", "bug", "production"},
    "spend": {"spend", "cost", "budget", "bill", "roi", "dollar", "money", "wasteful", "wasted"},
    "learn": {"learn", "learning", "learned", "repeat", "repeating", "memory", "remember", "mistake", "again", "knowledge"},
    "surveil": {"surveil", "surveillance", "monitor", "monitoring", "rank", "ranking", "track", "tracking", "police", "policing", "watch", "spy", "individual", "keystroke"},
    "outcome": {"outcome", "quality", "produced", "produce", "ship", "shipped", "shipping", "value", "impact", "delivered"},
    "trace": {"trace", "traceable", "cause", "caused", "root", "attribute", "attribution", "session", "which", "where"},
    "govern": {"govern", "governance", "policy", "guardrail", "block", "blocked", "review", "merge", "flag", "control", "slow", "slowing", "velocity"},
    "tool": {"tool", "tooling", "model", "copilot", "cursor", "claude", "keep", "scope", "cut", "standardize", "worth"},
}
# reverse: token -> canonical bucket
_SYN_REV = {}
for canon, words in SYNONYMS.items():
    for w in words:
        _SYN_REV[w] = canon


def _depluralize(t):
    # strip a single trailing 's' (not 'ss'); helps incidents->incident, costs->cost
    if len(t) > 4 and t.endswith("s") and not t.endswith("ss"):
        return t[:-1]
    return t


def tokenize(s):
    toks = re.findall(r"[a-z0-9]+", (s or "").lower())
    out = set()
    for t in toks:
        if t in STOPWORDS:
            continue
        t = _depluralize(t)
        out.add(_SYN_REV.get(t, t))
    return out


def raw_tokens(s):
    """Depluralized tokens WITHOUT synonym mapping — used to detect specific intents."""
    return {_depluralize(t) for t in re.findall(r"[a-z0-9]+", (s or "").lower()) if t not in STOPWORDS}


# Open commercial/strategic questions the tree intentionally does NOT answer from a
# capability node — they get a human-authored stance instead of a false mapping or a bare gap.
OPEN_INTENTS = [
    {
        "id": "open:pricing",
        "triggers": {"price", "priced", "pricing", "charge", "license", "subscription"},
        "title": "How Faros itself is priced (open commercial question)",
        "answer": ("That's the one open commercial question — and the cleanest FinOps-vs-platform "
                   "tell. The call I'd make: price on the platform/outcome layer (seats or a "
                   "connected-org tier), not on tokens or a percentage of savings — because "
                   "consumption/savings pricing structurally bends the product toward 'spend less' "
                   "and collapses the positioning. Public anchor seen: about $29/contributor/month. "
                   "The signal that would flip me: if pricing proves consumption- or savings-based "
                   "and Finance owns the buy, the FinOps read wins."),
        "honesty": "inference",
        "cite": "open:pricing",
    },
]


def _frontmatter(path):
    txt = open(path, encoding="utf-8").read()
    if not txt.startswith("---"):
        return None, ""
    _, fm, body = txt.split("---", 2)
    return yaml.safe_load(fm), body.strip()


class Tree:
    def __init__(self):
        self.nodes = {}       # id -> dict (incl _body)
        self.load()

    def load(self):
        for path in sorted(glob.glob(os.path.join(TREE, "**", "*.md"), recursive=True)):
            data, body = _frontmatter(path)
            if not data or "id" not in data:
                continue
            data["_body"] = body
            data["_file"] = os.path.relpath(path, ROOT)
            self.nodes[data["id"]] = data

    def approved(self, *types):
        out = [n for n in self.nodes.values() if n.get("status") == "approved"]
        if types:
            out = [n for n in out if n.get("type") in types]
        return out

    def get(self, nid):
        return self.nodes.get(nid)

    def personas(self):
        return self.approved("persona")

    def mappings(self):
        return self.approved("mapping")


# ---- the advisor ----

BANNED_POSITIONING = [
    "spend less", "cut cost", "cut costs", "reduce spend", "reduce cost",
    "lower the bill", "save money", "cost-cutting", "spend down",
    "rank engineers", "rank developers", "monitor keystrokes", "surveil",
]


def _node_bag(tree, m):
    """Weighted keyword bag for a mapping node. The mapping's OWN pain/title/tags
    dominate; the linked faros/flow add a little. The shared persona is deliberately
    excluded — it's identical across a persona's mappings, so it can't discriminate."""
    from collections import Counter
    bag = Counter()
    f = (m.get("fields") or {})
    for tok in tokenize(f.get("pain", "")):
        bag[tok] += 3
    for tok in tokenize(m.get("title", "")):
        bag[tok] += 2
    for t in (m.get("tags") or []):
        for tok in tokenize(t):
            bag[tok] += 2
    faros = tree.get(f.get("faros_ref"))
    if faros:
        for tok in tokenize(faros.get("title", "")):
            bag[tok] += 2
    flow = tree.get(f.get("flow_ref"))
    if flow:
        for tok in tokenize(flow.get("title", "")):
            bag[tok] += 1
        ff = flow.get("fields") or {}
        for v in (ff.get("ai_touchpoints") or []):
            for tok in tokenize(str(v)):
                bag[tok] += 1
    return bag


def _score(qtokens, bag):
    if not qtokens or not bag:
        return 0.0
    hit = sum(w for tok, w in bag.items() if tok in qtokens)
    if hit == 0:
        return 0.0
    total = sum(bag.values())
    # reward matched weight; normalize by question size and bag size so a big bag
    # can't win by sheer volume
    return hit / ((len(qtokens) ** 0.5) * (total ** 0.5))


def positioning_check(text):
    low = text.lower()
    for phrase in BANNED_POSITIONING:
        if phrase in low:
            return "flagged", phrase
    return "passed", None


def _draft(tree, m, persona):
    f = m.get("fields") or {}
    faros = tree.get(f.get("faros_ref"))
    honesty = m.get("honesty", "inference")
    evidence = f.get("pain") and (f.get("evidence") or "")
    cap = faros.get("title") if faros else "Faros"
    if honesty == "shipped":
        lead = "Yes — and this part is live today."
    elif honesty == "roadmap":
        lead = "Yes — the foundation is live, and this specific capability is on the roadmap (flagging that honestly)."
    else:
        lead = "Here's how Faros approaches it (this read is our inference, not a shipped claim)."
    answer = f"{lead} {f.get('evidence','').strip()}"
    return answer.strip(), honesty, cap


def advise(tree, question, persona_id="persona:maya"):
    persona = tree.get(persona_id) or (tree.personas()[0] if tree.personas() else None)
    qtokens = tokenize(question)
    qraw = raw_tokens(question)

    # 1) open commercial/strategic intents get a human-authored stance, not a false mapping
    for oi in OPEN_INTENTS:
        if qraw & oi["triggers"]:
            pcheck, _ = positioning_check(oi["answer"])
            citations = [c for c in [persona_id, oi["cite"]] if c]
            return {
                "question": question, "persona": persona_id,
                "kind": "open-question",
                "matched_pain": oi["title"], "answer": oi["answer"],
                "faros_nodes": [], "mapping_nodes": [],
                "evidence": "Human-authored stance on an open question (see memory open/pricing).",
                "honesty": oi["honesty"], "positioning_check": pcheck,
                "citations": citations, "gap": None, "match_score": 1.0,
                "score": {"citations_ok": len(citations) >= 2, "honesty_ok": True,
                          "positioning_ok": pcheck == "passed",
                          "total": sum([len(citations) >= 2, True, pcheck == "passed"])},
            }

    ranked = []
    for m in tree.mappings():
        ranked.append((_score(qtokens, _node_bag(tree, m)), m))
    ranked.sort(key=lambda x: x[0], reverse=True)

    best_score, best = (ranked[0] if ranked else (0.0, None))
    result = {
        "question": question,
        "persona": persona_id,
        "kind": "answer",
        "matched_pain": None,
        "answer": None,
        "faros_nodes": [],
        "mapping_nodes": [],
        "evidence": None,
        "honesty": None,
        "positioning_check": "passed",
        "citations": [],
        "gap": None,
        "match_score": round(best_score, 3),
    }

    if not best or best_score < MATCH_THRESHOLD:
        result["gap"] = "no_approved_node"
        result["answer"] = ("That's not covered by an approved node yet. Routing to the curator to "
                            "propose a mapping rather than improvising an answer.")
        result["score"] = {"citations_ok": False, "honesty_ok": False, "positioning_ok": True, "total": 0}
        return result

    f = best.get("fields") or {}
    answer, honesty, cap = _draft(tree, best, persona)
    pcheck, _phrase = positioning_check(answer + " " + (f.get("evidence") or ""))

    faros_ref = f.get("faros_ref")
    citations = [c for c in [persona_id, f.get("flow_ref"), best.get("id"), faros_ref] if c]

    result.update({
        "matched_pain": f.get("pain"),
        "answer": answer,
        "faros_nodes": [faros_ref] if faros_ref else [],
        "mapping_nodes": [best.get("id")],
        "evidence": f.get("evidence"),
        "honesty": honesty,
        "positioning_check": pcheck,
        "citations": citations,
    })
    result["score"] = {
        "citations_ok": len(citations) >= 2,
        "honesty_ok": honesty in ("shipped", "roadmap", "inference"),
        "positioning_ok": pcheck == "passed",
        "total": sum([len(citations) >= 2, honesty in ("shipped", "roadmap", "inference"), pcheck == "passed"]),
    }
    return result


# ---- export for the web UI ----

def export_web(out_path=None):
    tree = Tree()
    out_path = out_path or os.path.join(os.path.dirname(__file__), "web", "tree.js")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    payload = {
        "nodes": [
            {k: v for k, v in n.items() if not k.startswith("_")}
            for n in tree.approved()
        ],
        "threshold": MATCH_THRESHOLD,
        "synonyms": SYNONYMS_SERIALIZABLE(),
        "stopwords": sorted(STOPWORDS),
        "banned_positioning": BANNED_POSITIONING,
        "open_intents": [
            {"id": oi["id"], "triggers": sorted(oi["triggers"]), "title": oi["title"],
             "answer": oi["answer"], "honesty": oi["honesty"], "cite": oi["cite"]}
            for oi in OPEN_INTENTS
        ],
    }
    with open(out_path, "w", encoding="utf-8") as fp:
        fp.write("// auto-generated by sim/engine.py export_web — do not edit by hand\n")
        fp.write("window.TREE = ")
        json.dump(payload, fp, indent=2)
        fp.write(";\n")
    return out_path, len(payload["nodes"])


def SYNONYMS_SERIALIZABLE():
    return {k: sorted(v) for k, v in SYNONYMS.items()}


if __name__ == "__main__":
    t = Tree()
    print(f"loaded {len(t.nodes)} nodes; {len(t.approved())} approved; {len(t.mappings())} mappings.")
