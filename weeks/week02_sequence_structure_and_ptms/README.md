# Week 2 — Sequence, Structure and PTMs

**27200 · 10 September 2026 · Thursday, 08:00–12:00**

Three short lectures and three hands-on Colab exercises. Nothing needs to be installed locally and
nothing needs the HPC — click the badges below.

| Block | Time | Content |
|---|---|---|
| Programming | 08:00 – 08:30 | Continued from Week 1 |
| Housekeeping | 08:30 – 08:40 | Groups and hand-in information |
| Break | 08:40 – 08:50 | ☕ |
| Lecture 1 | 08:50 – 09:20 | Representations |
| Exercise 1 | 09:20 – 09:50 | `notebooks/01_representations.ipynb` |
| Break | 09:50 – 10:00 | ☕ |
| Lecture 2 | 10:00 – 10:20 | Sequence similarity — *Kristian* |
| Exercise 2 | 10:20 – 10:50 | `notebooks/02_gh_sequence_space.ipynb` |
| Break | 10:50 – 11:00 | ☕ |
| Lecture 3 | 11:00 – 11:20 | Protein structure — *Kristian* |
| Exercise 3 | 11:20 – 11:50 | `notebooks/03_structure_prediction_chai1.ipynb` |
| Wrap-up | 11:50 – 12:00 | Expectations survey and muddy points |

Each exercise slot is **30 minutes**. Exercises 2 and 3 have individual steps that take longer than
that, so you are not expected to finish them in the room — get as far as you can and come back to
them afterwards. The notebooks say where to stop.

---

## What you'll do today

- Encode a protein as a **one-hot matrix** and find out what that encoding silently assumes.
- Use **BLOSUM62 rows** as an encoding and see similarity become part of the representation.
- Build a **profile HMM** from a real histone H3 family, search with it, and discover that it misses
  a genuine family member because of what you trained it on.
- Extend an encoding with **PTM channels**, and show that H3K4me3 and H3K9me3 are indistinguishable
  in a 20-letter alphabet.
- Pull a **CAZy glycoside hydrolase family** from the database, cluster it with **MMseqs2**, and map
  it as a **sequence similarity network**.
- Predict protein **structures, enzyme–substrate complexes, glycosylation and metal cofactors** with
  **Chai-1**, and judge the predictions using pLDDT, pTM and PAE.

---

## Open the exercises in Colab

### Exercise 1 — Representations: from letters to models

One-hot and BLOSUM encodings, a profile HMM built from a live UniProt query, and PTM channels. Runs
on **free CPU** in about two minutes of compute. There are two versions — take the one that suits you.

**Exercise version** — three `# YOUR CODE HERE` blanks to fill in.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/UadKLab/27200_Data-Driven-Bioengineering/blob/main/weeks/week02_sequence_structure_and_ptms/notebooks/01_representations.ipynb)

**Worked version** — every cell completed, with the outputs already saved, so it reads straight
through even before you run anything.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/UadKLab/27200_Data-Driven-Bioengineering/blob/main/weeks/week02_sequence_structure_and_ptms/notebooks/01_representations_solved.ipynb)

**If you don't write code, start from the worked version.** Run the cells, read what comes out, and
spend your time on the questions in the text between them. What is being assessed this week is the
reasoning, not the syntax — you are not expected to arrive already knowing Python.

### Exercise 2 — GH sequence space

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/UadKLab/27200_Data-Driven-Bioengineering/blob/main/weeks/week02_sequence_structure_and_ptms/notebooks/02_gh_sequence_space.ipynb)

Fetch a glycoside hydrolase family (GH26) from CAZy and its sequences from NCBI, cluster them with
MMseqs2, then build a sequence similarity network and threshold it. You answer set questions at each
stage: how many clusters, how large, and where the characterised enzymes sit. Optional Cytoscape
visualisation at the end. **Free CPU.**

### Exercise 3 — Structure prediction with Chai-1

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/UadKLab/27200_Data-Driven-Bioengineering/blob/main/weeks/week02_sequence_structure_and_ptms/notebooks/03_structure_prediction_chai1.ipynb)

Three parts. **B** predicts the fold of a GH26 sequence and asks you to read pLDDT, pTM and PAE.
**C** models a GH26 catalytic domain bound to a carbohydrate substrate, after checking whether the
signal peptide needs removing. **D** predicts a copper cofactor and an N-glycosylation site on an
LPMO using covalent-bond restraints. **Needs a GPU runtime.**

> If a notebook has trouble loading, save it to your Drive: *File → Save a copy in Drive*. Restart
> the runtime (*Runtime → Restart session*) after any `pip install` cell.

---

## Environment notes

| | |
|---|---|
| Exercise 1 | CPU. Installs `pyhmmer`, `pyfamsa`, `biopython` (~30 s). Fetches live from the UniProt REST API. |
| Exercise 2 | CPU. Installs `biopython` and `networkx`; downloads MMseqs2 and seqkit binaries. Needs an email address for NCBI Entrez — use your DTU one. |
| Exercise 3 | **GPU required** — *Runtime → Change runtime type → T4 GPU*. Installs `chai_lab` and `py3Dmol`. Restart the session between parts B, C and D to free RAM. |

Exercise 2 pulls `data/GH26_characterized.html` from this repository automatically — there is
nothing to upload.

## Data

| File | Description |
|---|---|
| `data/GH26_characterized.html` | CAZy listing of characterised GH26 entries, used in Exercise 2 to mark which clusters contain a functionally characterised enzyme. |

---

## Hand-in

The Week 2 group assignment — **find the homologs of a human protein by sequence and by structure** —
is on DTU Learn, with the protein allocation per group.

| | |
|---|---|
| Report due | **Wednesday 16 September, 17:00** — one PDF per group, in FeedbackFruits |
| Peer feedback due | **Friday 18 September, 17:00** — one review per person |

---

## Slides

Released on DTU Learn shortly before the session.

## Acknowledgements

Exercises 2 and 3 were written by **Kristian Barrett**. Chai-1 is from Chai Discovery; MMseqs2 from
Steinegger & Söding; the histone annotation in Exercise 1 comes from UniProt.
