# Week 3 — Regulation and network logic

**27200 · 17 September 2026 · Thursday, 08:00–12:00**

Alon, *An Introduction to Systems Biology*, chapters 1–4. Two short lectures, two Colab exercises and
one in Cytoscape. Nothing needs the HPC.

> **Install Cytoscape before Thursday.** Exercise 2 ends in Cytoscape and there is no time to
> download a 200 MB installer in the room. Get 3.10 or later from [cytoscape.org](https://cytoscape.org)
> — free, runs on macOS, Windows and Linux — and open it once to check it starts.

| Block | Time | Content |
|---|---|---|
| Housekeeping | 08:00 – 08:10 | |
| Recap | 08:10 – 08:40 | Week 2 exercises, live |
| PyMOL | 08:40 – 09:00 | Working with structures |
| Break | 09:00 – 09:10 | ☕ |
| Lecture 1 | 09:10 – 09:30 | Gene regulation and circuits |
| Exercise 1 | 09:30 – 10:10 | `notebooks/01_gene_circuits.ipynb` |
| Break | 10:10 – 10:20 | ☕ |
| Lecture 2 | 10:20 – 10:50 | Biological networks |
| Exercise 2 | 10:50 – 11:30 | `notebooks/02_networks.ipynb`, then `exercises/cytoscape_exercise.md` |
| Hand-in feedback | 11:30 – 11:50 | On the Week 2 reports and peer reviews |
| Hand-in 2 | 11:50 – 11:55 | Introduction to this week's group assignment |
| Wrap-up | 11:55 – 12:00 | Muddy points |

---

## What you'll do today

- Simulate the simplest gene circuit and see why its response speed is fixed by degradation alone.
- Build **negative autoregulation** and watch it reach the same steady state eight times faster, and
  shrug off a doubling of its production rate.
- Build the **coherent feed-forward loop** and show it ignores a signal that does not last; build the
  **incoherent** one and turn a step into a pulse.
- Compute **degree, clustering and path length** on a real yeast protein network and show it is not
  random: scale-free, clustered, hierarchical.
- **Reproduce Milo et al. 2002**: count feed-forward loops in the yeast transcription network,
  randomise it fifty times keeping every node's degree, and get Z ≈ 14.
- Open the same network in **Cytoscape** and make the picture say something.

---

## Open the exercises in Colab

Both notebooks are complete and commented, with every output saved — run them, read the plots, and
answer the questions in the text. There is nothing to fill in.

### Exercise 1 — Gene circuits

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/UadKLab/27200_Data-Driven-Bioengineering/blob/main/weeks/week03_regulation_and_network_logic/notebooks/01_gene_circuits.ipynb)

Simple regulation, negative and positive autoregulation, the coherent and incoherent feed-forward
loops, and — if you have time — the repressilator. Every model is a few lines of explicit
time-stepping you can read. Runs instantly on the free CPU runtime; no installs.

### Exercise 2 — Biological networks

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/UadKLab/27200_Data-Driven-Bioengineering/blob/main/weeks/week03_regulation_and_network_logic/notebooks/02_networks.ipynb)

A seven-node graph you can check by hand, then a real yeast protein network measured against its
random twin, then the feed-forward-loop motif count on the Alon lab's yeast transcription network.
Ends by exporting the network for Cytoscape — **the download starts automatically when you run the
last cell**. Free CPU; the randomisation cell takes ~20 s. Installs `networkx`.

### Exercise 2, part B — Cytoscape

**[exercises/cytoscape_exercise.md](exercises/cytoscape_exercise.md)** — about 20 minutes. Import the
network, attach the attributes you computed, try layouts, find a hub's neighbourhood, map degree to
size and a knock-out's expression to colour, and check Cytoscape's statistics against the notebook's.
Answers at the bottom for the plenary. Also on DTU Learn as a PDF.

> If a notebook has trouble loading, *File → Save a copy in Drive*. Restart the runtime after any
> `pip install` cell.

---

## Data

Everything the notebooks use is fetched live from public URLs. The two files the Cytoscape exercise
needs are also here, in case the notebook download did not reach you:

| File | Description |
|---|---|
| `data/galFiltered.sif` | Yeast galactose-pathway network, 331 proteins, 361 interactions (`pp` protein–protein, `pd` protein–DNA). Cytoscape's standard sample network, from the [Cytoscape tutorials](https://github.com/cytoscape/cytoscape-tutorials). |
| `data/galFiltered_node_attributes.csv` | Gene name, degree and clustering coefficient per node, as computed in Exercise 2. |

The yeast transcription network in Exercise 2 is the Alon lab's
[2002 dataset](https://www.weizmann.ac.il/mcb/UriAlon/download/collection-complex-networks), fetched
by the notebook.

---

## Reading

Alon, *An Introduction to Systems Biology*, 2nd ed., chapters 1–4. Chapter 6 if the repressilator
caught your interest. The group assignment for this week is introduced at 11:50 and posted on DTU
Learn afterwards.

## Slides

Released on DTU Learn shortly before the session.

## Acknowledgements

The circuit exercises rework the 27641 Systems Biology R exercises. Network data: Cytoscape
tutorials (GAL network); Alon lab (yeast transcription network). Milo R. et al., *Science* 298,
824–827 (2002).
