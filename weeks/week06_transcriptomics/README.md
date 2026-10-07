# Week 6 - Transcriptomics

**27200 · 08 October 2026 · Thursday, 08:00–12:00**

**Teaching:** Juliana Assis (Senior Data Scientist, BRIGHT) and Lasse Ebdrup Pedersen
(Senior Researcher, DTU Bioengineering)

**Theme:** transcript abundance as a dynamic, but incomplete, regulatory readout.

Two lectures and two hands-on blocks. Nothing needs to be installed and nothing needs
the HPC: the exercises run in GitHub Codespaces, which starts a ready-made environment
with R, all packages, Nextflow and Docker already in it.

All material lives in its own repository:

[**→ Material and exercises**](https://github.com/biosustain/dsp_transcriptomics_27200-Data-driven-bioengineering)
· [**→ Course book**](https://biosustain.github.io/dsp_transcriptomics_27200-Data-driven-bioengineering/)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/biosustain/dsp_transcriptomics_27200-Data-driven-bioengineering)

> **When you create the Codespace, set the Machine type to 4-core.** The default is
> too small for the pipeline step. A `START_HERE` page opens by itself and tells you
> what to do first.

| Block | Time | Content |
|---|---|---|
| Welcome | 08:00 – 08:15 | Setup and Codespaces |
| Lecture 1 | 08:15 – 09:00 | Illumina sequencing, the RNA-seq workflow, nf-core/rnaseq |
| Lecture 2 | 09:00 – 09:45 | Count matrices, normalisation, PCA, differential expression |
| Break | 09:45 – 10:00 | ☕ |
| Exercise 1 | 10:00 – 10:55 | Quality control and exploratory analysis |
| Exercise 2 | 10:55 – 11:50 | Differential expression and functional enrichment |
| Wrap-up | 11:50 – 12:00 | Key insight and muddy point |

---

## What you'll do today

- **Make a count matrix yourself.** Run the nf-core/rnaseq pipeline on two sub-sampled
  samples and watch reads turn into a table of numbers. It is a small demonstration,
  not the data you analyse afterwards, and that distinction is part of the point.
- **Read a count matrix critically.** Library sizes, filtering, normalisation, and what
  a PCA is and is not telling you about your samples.
- **Test a hypothesis with DESeq2.** Build a design formula, see what changes when you
  account for a known confounder, and learn why the direction of a fold change depends
  on a choice you made earlier.
- **Get from a gene list to biology** with gene set enrichment analysis, including what
  to do when nothing comes out significant.
- **Say what transcriptomics cannot tell you.** The molecule whose activity changes most
  in this experiment barely moves in the data.

The dataset is human airway smooth muscle cells treated with dexamethasone
([Himes *et al.*, 2014](https://doi.org/10.1371/journal.pone.0099625)), four donors,
paired design. Groups that finish early continue with a bacterial time course
(*Staphylococcus aureus*, biofilm versus planktonic, two strains) in the advanced part
of the book.

## How the exercises work

You work in groups of four, in Jupyter notebooks with an R kernel. The code is written
for you: the exercise is reading the output and arguing about what it means. Each
notebook ends with **interpretation questions**, and those are the point of the
session. Nobody expects a complete answer to them.

AI assistants are allowed and encouraged, as long as you check what they tell you.
Copilot Chat is available in the Codespace, and the book has a section on using it
sensibly.

## Before the session

**You need a GitHub account.** If you do not have one already, create a free account at
[github.com/signup](https://github.com/signup) before Thursday. Sign up with your DTU
address if you can: that also gets you the free
[Student Developer Pack](https://education.github.com/pack), which includes GitHub
Copilot.

Nothing else to install. If you want to look ahead, the
[course book](https://biosustain.github.io/dsp_transcriptomics_27200-Data-driven-bioengineering/)
has every chapter in full, with the code and the outputs.

Questions beforehand: Juliana Assis (jasge@dtu.dk)
