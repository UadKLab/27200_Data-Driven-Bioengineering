# Hypoxia knowledge base

A small, linked set of study cards about how cells respond to low oxygen. It is built from
published papers and from a table of **differential proteomics results** (yours, or the reference table). Every claim on a card points
to the sentence in a paper that supports it, and a script checks that the sentence is really
there.

Start with [[INDEX]].


## What is in this folder

| | |
|---|---|
| `INDEX.md` | every card, one line each - start here |
| `concepts/` | one card per process, mechanism or method (for example, how cells sense oxygen) |
| `genes/` | one card per gene from the results table |
| `sources/` | the papers, as plain text. `SOURCES.md` has the full citations |
| `my_results.csv` | the results table used: gene, log2FC, p, q |
| `CHECK_REPORT.md` | what the checking script found, the last time it ran |
| `CHANGELOG.md` | every change made after the first version, and why |
| `tools/check_kb.py` | the checking script |


## How to open it

- **Obsidian** (free, obsidian.md): *Open folder as vault* and pick this folder. Click a
  `[[link]]` to follow it; open the *Graph view* to see how the cards connect.
- **Any text editor** works too. The cards are plain markdown files.


## How to read a card

```
---
type: gene                         concept or gene
sources: [Hofner2025]              the papers this card uses
my_log2FC: 3.53                    gene cards only: your own numbers
my_q: 0.0061
---
# NDRG1

## In one sentence                 a plain definition
## My result                       gene cards only: what the results table shows
## What the papers say             claims, each with its source and a quote:
- NDRG1 is more abundant in KGN cells in hypoxia. (Hofner2025, Results)
  > "The more abundantly expressed proteins included AK4 ..., and NDRG1 ..."
## Do my result and the papers agree?   gene cards only
## Open questions                  what the papers leave open, or disagree on
## Related                         links to other cards, each with a reason
```

- `(Hofner2025, Results)` - the paper and the section the claim comes from.
- `> "..."` - the exact sentence from that paper. `...` means words were left out.
- `(not from these sources)` - general knowledge, not from these papers. Treat it as
  unchecked.


## The rules for adding to it

1. **One card per thing.** Search the cards before making a new one. If it exists, update it.
2. **Every claim cites a paper in `sources/` and quotes it.** Otherwise mark it
   *(not from these sources)*.
3. **Never invent a source.** A paper that is not in `sources/` cannot be cited.
4. **Link each card to at least two others**, and say why in a few words.
5. **Say where papers disagree**, under *Open questions*. Do not quietly pick one.
6. **Record every change** in `CHANGELOG.md`: the date, the card, what changed, and why.
7. **Run the check after every change**, and fix what it reports:

       python tools/check_kb.py

   (from inside this folder; it needs only Python 3).


## What the check can and cannot tell you

It can tell you that a quoted sentence exists in the cited paper, that links work, that
every claim has a source, and that the gene numbers match `my_results.csv`.

It **cannot** tell you whether the quote actually supports the claim, whether general
knowledge is right, or whether two cards describe the same thing under different names.
That part is yours.
