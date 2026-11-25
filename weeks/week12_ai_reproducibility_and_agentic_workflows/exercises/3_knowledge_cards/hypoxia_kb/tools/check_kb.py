"""Check the knowledge base, and write CHECK_REPORT.md.

Run from anywhere:   python hypoxia_kb/tools/check_kb.py

What it checks
  - every quote on a card appears, word for word, in the paper the claim cites
  - every claim either cites a paper and quotes it, or is marked (not from these sources)
  - every [[link]] points to a card that exists, and every card links to at least two others
  - every card has the required parts, and is listed in INDEX.md
  - gene cards: the numbers match my_results.csv, and "not in the papers" is really true

What it cannot check - that is your job
  - whether a quote that exists actually supports the claim next to it
  - whether anything marked (not from these sources) is true
  - whether two cards describe the same thing under different names

Only the Python standard library is used, so it runs anywhere Python 3 does.
"""
import csv
import difflib
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

KB = Path(__file__).resolve().parent.parent
MIN_WORDS = 6
CARD_DIRS = {"concept": "concepts", "gene": "genes"}
REQUIRED = {
    "concept": ["In one sentence", "What the papers say", "Open questions", "Related"],
    "gene": ["In one sentence", "My result", "What the papers say",
             "Do my result and the papers agree?", "Open questions", "Related"],
}
GREEK = {"α": "alpha", "β": "beta", "γ": "gamma", "δ": "delta", "ε": "epsilon", "κ": "kappa",
         "λ": "lambda", "μ": "mu", "µ": "mu", "σ": "sigma", "τ": "tau", "ω": "omega"}
TAG = re.compile(r"\(\s*([A-Z][A-Za-z]+\d{4}[a-z]?)\s*(?:,\s*([^)]*))?\)")
GENERAL = re.compile(r"\(\s*not from these sources\s*\)", re.I)
LINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")


# ---------------------------------------------------------------- text matching
def norm(s):
    """Lower-case, one kind of quote and dash, Greek spelled out, no markdown emphasis."""
    s = unicodedata.normalize("NFKC", s)
    for g, name in GREEK.items():
        s = s.replace(g, name)
    s = re.sub(r"[‘’‚‛′`]", "'", s)
    s = re.sub(r"[“”„″]", '"', s)
    s = re.sub(r"[‐‑‒–—−]", "-", s)
    s = s.replace("…", "...").replace("*", "")
    return re.sub(r"\s+", " ", s).strip().lower()


def letters(s):
    """Only the letters: ignores numbers, punctuation, spaces and citation markers."""
    return re.sub(r"[^a-z]", "", norm(s))


def letters_with_index(text):
    """The letters of an already normalised text, and where each one sits in it."""
    idx = [i for i, ch in enumerate(text) if "a" <= ch <= "z"]
    return "".join(text[i] for i in idx), idx


NUMBER = re.compile(r"\d+(?:[.,]\d+)?")


def found_in_order(parts, text):
    return span_in_order(parts, text) is not None


def span_in_order(parts, text):
    pos, start = 0, None
    for p in parts:
        i = text.find(p, pos)
        if i < 0:
            return None
        start = i if start is None else start
        pos = i + len(p)
    return start, pos


def fragments(quote):
    """A quote may skip words with '...'; each piece must then appear, in order."""
    q = norm(quote).strip(" \"'")
    q = q.replace("[...]", "...")
    return [p.strip(" \"',;") for p in q.split("...") if p.strip(" \"',;")]


class Source:
    def __init__(self, path):
        self.id = path.stem.split("_")[0]
        self.name = path.name
        self.raw = path.read_text(encoding="utf-8")
        self.text = norm(self.raw)
        self.loose, self.loose_idx = letters_with_index(self.text)
        self.sentences = [s for s in re.split(r"(?<=[.!?])\s+", self.text) if len(s) > 30]

    def closest(self, quote):
        q = norm(quote).strip(" \"'")
        best, best_s = 0.0, ""
        for s in self.sentences:
            m = difflib.SequenceMatcher(None, q, s, autojunk=False)
            if m.real_quick_ratio() < best or m.quick_ratio() < best:
                continue
            r = m.ratio()
            if r > best:
                best, best_s = r, s
        return best, best_s


def check_quote(quote, cited, sources):
    """Return (result, detail): verbatim | close | wrong number | wrong source | not found | too short."""
    parts = fragments(quote)
    if sum(len(p.split()) for p in parts) < MIN_WORDS:
        return "too short", f"quotes need at least {MIN_WORDS} words to be checkable"
    order = [sources[c] for c in cited if c in sources]
    others = [s for s in sources.values() if s.id not in cited]
    for s in order:
        if found_in_order(parts, s.text):
            return "verbatim", s.id
    for s in order:
        span = span_in_order([letters(p) for p in parts], s.loose)
        if span:
            a, b = s.loose_idx[span[0]], s.loose_idx[span[1] - 1] + 1
            # widen to whole sentences, so numbers at either end are included
            a = max(s.text.rfind(". ", 0, a) + 2, 0) if s.text.rfind(". ", 0, a) >= 0 else 0
            end = re.search(r"[.!?](\s|$)", s.text[b:])
            b = b + end.end() if end else len(s.text)
            passage = s.text[a:b].strip()
            missing = [n for n in NUMBER.findall(" ".join(parts)) if n not in NUMBER.findall(passage)]
            if missing:
                return "wrong number", (f"the words are in {s.id}, but these numbers are not in that "
                                        f"sentence: {', '.join(missing)}. The paper says: \"{passage[:220]}\"")
            return "close", (f"in {s.id} the words and numbers match, but punctuation or citation "
                             "markers differ - fine if nothing else changed")
    for s in others:
        if found_in_order(parts, s.text):
            return "wrong source", f"this sentence is in {s.id}, not in {', '.join(cited)}"
    pool = order or list(sources.values())
    score, sent = max((s.closest(quote) for s in pool), key=lambda t: t[0])
    return "not found", f"closest sentence ({score:.0%} similar): \"{sent[:220]}\""


# ---------------------------------------------------------------- reading cards
def parse_frontmatter(text):
    meta, body = {}, text
    m = re.match(r"\s*---\s*\n(.*?)\n---\s*\n(.*)", text, re.S)
    if m:
        body = m.group(2)
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                v = v.split("#")[0].strip()
                if v.startswith("[") and v.endswith("]"):
                    v = [x.strip().strip("'\"") for x in v[1:-1].split(",") if x.strip()]
                meta[k.strip()] = v
    return meta, body, bool(m)


def sections(body):
    out, cur = {}, None
    for line in body.splitlines():
        h = re.match(r"##\s+(.*?)\s*$", line)
        if h and not line.startswith("###"):
            cur = h.group(1)
            out[cur] = []
        elif cur is not None:
            out[cur].append(line)
    return out


def claims(lines):
    """Top-level bullets are claims; '>' lines under a bullet are its quotes."""
    out = []
    for line in lines:
        s = line.strip()
        if re.match(r"^[-*]\s+", line):
            out.append({"text": re.sub(r"^[-*]\s+", "", line).strip(), "quotes": []})
        elif s.startswith(">") and out:
            q = s.lstrip(">").strip()
            if q:
                out[-1]["quotes"].append(q)
        elif s and out and not out[-1]["quotes"]:
            out[-1]["text"] += " " + s
    return out


def section(secs, name):
    for k, v in secs.items():
        if k.lower().startswith(name.lower().rstrip("?")):
            return v
    return None


def read_results(path):
    if not path.exists():
        return None
    with path.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return {}
    cols = {c.lower().replace(" ", "").replace("_", ""): c for c in rows[0]}

    def pick(*names):
        for n in names:
            if n in cols:
                return cols[n]
    g = pick("gene", "genename", "genenames", "symbol")
    fc = pick("log2fc", "logfc", "log2foldchange", "foldchange")
    q = pick("q", "qvalue", "padj", "fdr", "adjp")
    if not (g and fc and q):
        return {"__bad__": f"my_results.csv needs columns for gene, log2FC and q (found: {', '.join(rows[0])})"}
    out = {}
    for r in rows:
        for name in re.split(r"[;,]", r[g] or ""):
            if name.strip():
                out.setdefault(name.strip().upper(), (float(r[fc]), float(r[q])))
    return out


def num(v):
    try:
        return float(str(v).replace("×10^", "e").replace("x10^", "e"))
    except ValueError:
        return None


# ---------------------------------------------------------------- the check
def main():
    sources = {}
    for p in sorted((KB / "sources").glob("*.md")):
        if p.stem.upper() != "SOURCES":
            s = Source(p)
            sources[s.id] = s
    cards = {}
    for kind, d in CARD_DIRS.items():
        for p in sorted((KB / d).glob("*.md")):
            cards[p.stem] = (kind, p)
    lower = {}
    for name in cards:
        lower.setdefault(name.lower(), []).append(name)
    results = read_results(KB / "my_results.csv")

    problems = {}          # card -> list of (level, message)
    quote_rows = []
    tally = {k: 0 for k in ["verbatim", "close", "wrong number", "wrong source", "not found", "too short",
                            "no quote", "no source", "general"]}

    def add(card, level, msg):
        problems.setdefault(card, []).append((level, msg))

    if not sources:
        add("(knowledge base)", "ERROR", "no papers found in sources/")
    if not cards:
        add("(knowledge base)", "ERROR", "no cards found in concepts/ or genes/")
    for name, same in lower.items():
        if len(same) > 1:
            add("(knowledge base)", "ERROR", f"two cards differ only in capitals: {', '.join(same)}")
    if isinstance(results, dict) and "__bad__" in results:
        add("(knowledge base)", "ERROR", results.pop("__bad__"))
    if results is None and any(k == "gene" for k, _ in cards.values()):
        add("(knowledge base)", "WARNING",
            "my_results.csv not found - copy ../1_proteomics/results.csv or ../results_reference.csv here, named my_results.csv")

    for name, (kind, path) in cards.items():
        text = path.read_text(encoding="utf-8")
        meta, body, has_fm = parse_frontmatter(text)
        if re.search(r"[\[\]#^|:\\/]", name):
            add(name, "WARNING", "file name contains a character Obsidian cannot link to ([ ] # ^ | : \\ /)")
        if not has_fm:
            add(name, "ERROR", "no front matter (the block between --- lines at the top)")
        if meta.get("type") != kind:
            add(name, "ERROR", f"type should be '{kind}' because the card is in {CARD_DIRS[kind]}/ (found: {meta.get('type')!r})")
        listed = meta.get("sources") or []
        if isinstance(listed, str):
            listed = [listed]
        for sid in listed:
            if sid not in sources:
                add(name, "ERROR", f"sources lists '{sid}', but there is no paper with that name in sources/")
        title = re.search(r"^#\s+(.+?)\s*$", body, re.M)
        if not title:
            add(name, "ERROR", "no title line (# Card name)")
        elif title.group(1) != name:
            add(name, "WARNING", f"title '{title.group(1)}' differs from the file name '{name}' - links use the file name")
        secs = sections(body)
        for req in REQUIRED[kind]:
            if section(secs, req) is None:
                add(name, "ERROR", f"missing section: ## {req}")

        # claims and quotes
        cited_ids = set()
        for c in claims(section(secs, "What the papers say") or []):
            tags = [m.group(1) for m in TAG.finditer(c["text"])]
            short = c["text"][:70] + ("..." if len(c["text"]) > 70 else "")
            if GENERAL.search(c["text"]):
                tally["general"] += 1
                quote_rows.append((name, short, "-", "general knowledge", "check it yourself"))
                continue
            if not tags:
                tally["no source"] += 1
                add(name, "ERROR", f"claim with no source and not marked (not from these sources): \"{short}\"")
                quote_rows.append((name, short, "-", "no source", ""))
                continue
            cited_ids.update(tags)
            for t in tags:
                if t not in sources:
                    add(name, "ERROR", f"cites '{t}', which is not a paper in sources/ - an invented source?")
            if not c["quotes"]:
                tally["no quote"] += 1
                add(name, "ERROR", f"claim with no quote under it: \"{short}\"")
                quote_rows.append((name, short, ", ".join(tags), "no quote", ""))
                continue
            for q in c["quotes"]:
                res, detail = check_quote(q, tags, sources)
                tally[res] += 1
                quote_rows.append((name, short, ", ".join(tags), res, "" if res == "verbatim" else detail))
                if res == "close":
                    add(name, "WARNING", f"quote nearly matches - {detail}: \"{q[:120]}\"")
                elif res != "verbatim":
                    add(name, "ERROR", f"quote {res} - {detail}. Quote: \"{q[:160]}\"")
        missing = cited_ids - set(listed)
        if missing:
            add(name, "WARNING", f"claims cite {', '.join(sorted(missing))}, but the front matter 'sources' does not list it")

        # links
        targets = []
        for m in LINK.finditer(body):
            t = m.group(1).strip()
            if t in cards or t.lower() in lower:
                if t not in cards:
                    add(name, "WARNING", f"link [[{t}]] only matches '{lower[t.lower()][0]}' if capitals are ignored")
                if t.lower() != name.lower():
                    targets.append(t.lower())
            elif (KB / f"{t}.md").exists() or (KB / "sources" / f"{t}.md").exists():
                pass
            else:
                add(name, "ERROR", f"broken link [[{t}]] - no card with that name")
        if len(set(targets)) < 2:
            add(name, "ERROR", f"links to {len(set(targets))} other card(s); needs at least 2")

        # gene cards against my own results, and against the papers
        if kind == "gene":
            sym = name.upper()
            if results is not None:
                if sym not in results:
                    add(name, "ERROR", f"{name} is not in my_results.csv - gene cards must come from your own results")
                else:
                    fc, q = results[sym]
                    mfc, mq = num(meta.get("my_log2FC")), num(meta.get("my_q"))
                    if mfc is None or mq is None:
                        add(name, "ERROR", "front matter needs my_log2FC and my_q as numbers")
                    else:
                        if abs(mfc - fc) > max(0.02, 0.02 * abs(fc)):
                            add(name, "ERROR", f"my_log2FC is {mfc}, but my_results.csv says {fc:.3g}")
                        if q > 0 and mq > 0 and abs(_log10(mq) - _log10(q)) > 0.05:
                            add(name, "ERROR", f"my_q is {mq}, but my_results.csv says {q:.3g}")
            pat = re.compile(r"(?<![A-Za-z0-9])" + re.escape(name) + r"(?![A-Za-z0-9])", re.I)
            where = {s.id: len(pat.findall(s.raw)) for s in sources.values()}
            where = {k: v for k, v in where.items() if v}
            if not cited_ids and where:
                add(name, "WARNING", "no claims from the papers, but the symbol appears in "
                    + ", ".join(f"{k} ({v}x)" for k, v in where.items()) + " - look again")
            if cited_ids and not where:
                add(name, "NOTE", f"the symbol {name} does not appear in any paper - the quotes must use "
                    "another name for it. Check that they really are about this gene")

    # the index
    index = KB / "INDEX.md"
    if not index.exists():
        add("INDEX.md", "ERROR", "INDEX.md is missing")
    else:
        linked = {m.group(1).strip().lower() for m in LINK.finditer(index.read_text(encoding="utf-8"))}
        for name in cards:
            if name.lower() not in linked:
                add("INDEX.md", "WARNING", f"card '{name}' is not listed")
        for t in linked:
            if t not in lower:
                add("INDEX.md", "ERROR", f"broken link [[{t}]]")

    write_report(cards, sources, problems, quote_rows, tally, results)
    n_err = sum(1 for v in problems.values() for lvl, _ in v if lvl == "ERROR")
    n_warn = sum(1 for v in problems.values() for lvl, _ in v if lvl == "WARNING")
    print(f"Checked {len(cards)} cards against {len(sources)} papers.")
    print(f"Quotes: {tally['verbatim']} verbatim, {tally['close']} close, {tally['wrong number']} wrong number, "
          f"{tally['wrong source']} wrong source, "
          f"{tally['not found']} not found, {tally['too short']} too short.")
    print(f"Claims without a quote: {tally['no quote']}. Without a source: {tally['no source']}. "
          f"Marked general knowledge: {tally['general']}.")
    print(f"{n_err} errors, {n_warn} warnings. Details in {KB.name}/CHECK_REPORT.md")
    for card, items in problems.items():
        for lvl, msg in items:
            if lvl == "ERROR":
                print(f"  ERROR  {card}: {msg}")
    return 1 if n_err else 0


def _log10(x):
    import math
    return math.log10(x)


def write_report(cards, sources, problems, quote_rows, tally, results):
    n_c = sum(1 for k, _ in cards.values() if k == "concept")
    n_g = len(cards) - n_c
    L = [f"# Check report", "",
         f"Made by `tools/check_kb.py` on {datetime.now():%Y-%m-%d %H:%M}. "
         f"{n_c} concept cards, {n_g} gene cards, {len(sources)} papers "
         f"({', '.join(sources)}). Run the script again after every change.", "",
         "## Summary", "",
         "| What | Count | Meaning |", "|---|---:|---|",
         f"| Quotes found word for word | {tally['verbatim']} | the sentence is in the cited paper |",
         f"| Quotes that nearly match | {tally['close']} | same words and numbers; punctuation or citation markers differ |",
         f"| Quotes with a changed number | {tally['wrong number']} | the sentence exists, but a number in the quote does not |",
         f"| Quotes from the wrong paper | {tally['wrong source']} | the sentence exists, but in another paper |",
         f"| Quotes not found | {tally['not found']} | not in the cited paper - paraphrased or invented |",
         f"| Quotes too short to check | {tally['too short']} | fewer than {MIN_WORDS} words |",
         f"| Claims with no quote | {tally['no quote']} | cannot be checked |",
         f"| Claims with no source | {tally['no source']} | not allowed |",
         f"| Claims marked general knowledge | {tally['general']} | not from these papers - check them yourself |",
         "", "## What this script cannot check", "",
         "- Whether a quote that exists actually **supports** the claim next to it.",
         "- Whether a claim marked *(not from these sources)* is true.",
         "- Whether two cards describe the same thing under different names.",
         "- Whether a gene the papers do not mention appears under another name (for example a protein name).",
         "", "## Problems, card by card", ""]
    if not problems:
        L.append("None found.")
    for card, items in problems.items():
        L.append(f"### {card}")
        for lvl, msg in items:
            L.append(f"- **{lvl}** {msg}")
        L.append("")
    L += ["", "## Every claim", "", "| Card | Claim | Cites | Result | Detail |", "|---|---|---|---|---|"]
    for row in quote_rows:
        L.append("| " + " | ".join(str(x).replace("|", "/") for x in row) + " |")
    (KB / "CHECK_REPORT.md").write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
