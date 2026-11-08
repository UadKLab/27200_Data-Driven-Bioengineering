# Week 11 — Protein Language Models and Generative Protein Design

**Date:** 19 November 2026  
**Instructors:** Jonathan Funk & Kostas  
**Theme:** Modern representation learning and generative models for biological sequences.

---

## Lecture: Protein language models

Lecture recording | [Panopto](https://panopto.dtu.dk/Panopto/Pages/Viewer.aspx?id=4c973ae9-841d-40b4-9d1b-b467006cdc6d). Log in with your DTU credentials.

---

## Exercise: pLM playground

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/UadKLab/27200_Data-Driven-Bioengineering/blob/main/weeks/week11_protein_language_models_and_generative_design/notebooks/01_plm_playground_student.ipynb)

**[notebooks/01_plm_playground_student.ipynb](notebooks/01_plm_playground_student.ipynb)** — by the end you will have:

- loaded the **ESM-2** protein language model in Colab and used it to embed sequences
- seen pLM embeddings cluster nanobodies, human heavy-chain antibodies and shuffled controls, and trained a small classifier on top
- used ESM-2 in **zero-shot mode** to score amino-acid preferences across a nanobody CDR3
- predicted the optimal pH of enzymes from sequence with ESM-2 embeddings and ridge regression, and compared this against a hand-crafted baseline

> If the notebook has trouble loading on Colab, save it to your Drive: *File → Save a copy in Drive*.
> Restart the runtime (*Runtime → Restart session*) after any `pip install` cell.

### How the notebook is set up

The exercise contains **8 fill-in-the-blank `TODO_N` markers**. Each blank is a real design choice a
researcher makes, not a trick question. The markdown above the cell, and the hint inside the comment,
usually contain the answer. The first markdown cell lists every blank with the section it lives in,
so you can use it as a checklist.

If a cell crashes with `SyntaxError` or `NameError`, check that every `___` and `____` placeholder has
been filled in.

A solved version, [notebooks/01_plm_playground_solved.ipynb](notebooks/01_plm_playground_solved.ipynb),
is in the same folder. Try to resist looking at it!

### Environment

The notebook runs end-to-end on **free-tier Google Colab CPU** in about 10–15 minutes. A GPU is faster
(especially for the pH-prediction section) but is not required. It installs only `transformers`,
`umap-learn` and the standard ML stack (~30 s), and downloads the enzyme pH data itself.

---

## Going further

If you finish early or want to keep exploring pLMs on your own time, take a look at the
**[Multiomics Analytics Group's `course_protein_language_modeling`](https://github.com/Multiomics-Analytics-Group/course_protein_language_modeling/tree/main)**.
It is a fuller short course on pLMs by Alberto Santos and colleagues at DTU Biosustain, with hands-on
Colab notebooks that go beyond what we cover here: fine-tuning ESM on a downstream task, per-residue
embeddings, the `bio-embeddings` library, and *de novo* protein design with a pLM.

---

## Acknowledgements

The lecture and exercise come from the
[27666 Protein Design course](https://github.com/DigBioLab/27666_Protein_Design/tree/main/Day_5/morning)
(DigBioLab, DTU). Many figures in the lecture are adapted from Sarah Gurev's protein language models
tutorial at MLCB 2024 (with credit to Aaron Kollasch, Noor Youssef, John Ingraham and Adam Riesselman).
The enzyme optimal-pH dataset is distributed via the
[ESM2-Tutorial](https://github.com/ProteinVision/ESM2-Tutorial) repository. The nanobody sequences
are from the InstaNexus study (Reverenna M. *et al.*, *Mol Cell Proteomics* 25:4, 2026).

- **ESM-2** — Lin Z. *et al.*, *Science* 379, 1123–1130 (2023).
