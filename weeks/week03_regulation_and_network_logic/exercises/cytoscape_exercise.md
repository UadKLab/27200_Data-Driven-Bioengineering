# Week 3 — Exercise 2, part B: the same network in Cytoscape

**27200 Data-driven Bioengineering · about 20 minutes**

You have just computed degree, clustering and paths on the yeast GAL network in Python. Now look at
it. Cytoscape is where you *see* a network; the notebook is where you *compute* on it. You need both,
and this exercise is about learning what the picture adds.

**Before you start:** install Cytoscape (3.10 or later) from [cytoscape.org](https://cytoscape.org).
It is free and runs on everything. You also need two small files, `galFiltered.sif` and
`galFiltered_node_attributes.csv`. Part 4 of the notebook downloads them to your computer when you
run it; they are also on **DTU Learn** and in the course repository under
`weeks/week03_regulation_and_network_logic/data/`. Or use the copy of the same network that ships
inside Cytoscape (step 1 explains both).

> **Terms**
> **SIF** — the simplest network file format: one line per edge, `source  type  target`.
> **Node table** — a spreadsheet where each row is a node and each column an attribute (name,
> degree, expression…). Cytoscape shows it at the bottom of the window.
> **Style** — the rules that map attributes to appearance: node size from degree, colour from
> expression. This is the whole point of Cytoscape.
> **First neighbours** — the nodes directly connected to a selected node.

---

## 1 · Get the network in

**Either** import the file you exported: *File → Import → Network from File…* → `galFiltered.sif`.
Cytoscape recognises SIF; just click OK.

**Or** use Cytoscape's own copy: on the welcome screen choose *Open Session*, or *File → Open
Session…*, and open `galFiltered.cys` from the `sampleData` folder inside your Cytoscape installation.
The session version already has expression data attached, which you need in step 5.

You should see 331 nodes and 361 edges (bottom-right of the network view). If the view is empty,
*Layout → Apply Preferred Layout* or press **F5**.

## 2 · Add the attributes you computed

*File → Import → Table from File…* → `galFiltered_node_attributes.csv`. In the dialog, make sure
**Key column for network** is `shared name` and the CSV's key column is `id`, then OK. The node
table at the bottom now has `name`, `degree` and `clustering` columns.

Click a few nodes. Compare the `degree` column with what the notebook printed for the hubs.

## 3 · Layouts — same network, different pictures

*Layout* menu. Try **Prefuse Force Directed**, **Circular** and **Grid**. Then *Layout → yFiles
Layouts* if the app is installed (it prompts you).

**Question 3.1** — The force-directed layout pulls tightly connected groups together and pushes hubs
to the middle of their neighbourhoods. The circular layout puts every node on a ring. Which one lets
you *see* the clustering you computed? Which one is honest about the fact that node positions carry
no information?

## 4 · Find a hub and its neighbourhood

In the search box (top right of the toolbar) type `GAL4` and press Enter. The node is selected
(yellow). Then *Select → Nodes → First Neighbours of Selected Nodes → Undirected*.

**Question 4.1** — How many nodes are now selected? Subtract one for GAL4 itself. Does it match the
degree in your table?

**Question 4.2** — Do the same for `MCM1`, the highest-degree node. Its neighbours light up all over
the network rather than in one place. Relate that to its clustering coefficient of 0.06.

## 5 · Make the picture say something: map attributes to appearance

Open the **Style** tab in the left panel.

- **Size from degree.** Click the *Size* row → set *Column* to `degree`, *Mapping Type* to
  *Continuous*. Hubs become large.
- **Colour from expression.** The `galFiltered.cys` session, and `galExpData.csv` if you imported the
  SIF, carry three knock-out experiments: `gal1RGexp`, `gal4RGexp`, `gal80Rexp` — the log-ratio of
  expression in the mutant versus wild type. Click *Fill Color* → *Column* `gal80Rexp` → *Continuous*.
  Set the low end blue, the midpoint white, the high end red.

**Question 5.1** — A negative value in `gal80Rexp` means the gene is *lower* in the mutant than in
wild type. Why do we work with the log of the ratio rather than the ratio itself? (Hint: what does
"halved" look like next to "doubled" on each scale?)

**Question 5.2** — Sort the node table by `gal80Rexp`. Which gene is most up-regulated when GAL80 is
deleted?

**Question 5.3** — GAL80 is deleted, and most genes connected to GAL4 go *up*. GAL4 is a
transcriptional activator. What does that tell you about what Gal80 protein normally does to Gal4?
Now find the GAL4–GAL80 edge in the network: is it `pp` or `pd`? Does that fit your answer?

## 6 · Network statistics inside Cytoscape

*Tools → Analyze Network* → treat as undirected. Compare the numbers to the notebook: average
degree, clustering coefficient, diameter. The *Node Degree Distribution* button opens the same
log-log plot you drew in Python.

**Question 6.1** — The numbers should match. If any do not, the likeliest reason is that Cytoscape
counts a self-loop twice when reporting degree. Can you find a self-loop in the network?

---

## What Cytoscape adds — and does not

The notebook computed every number here in a second and could do it for ten thousand networks in a
loop. What it cannot do is let you notice that MCM1's neighbours are scattered across the whole
network while GAL4's form a clump, or that the up-regulated genes in the gal80 knock-out all sit in
one region. **Compute in code, look in Cytoscape, and go back to code once you know what to compute.**

For the group assignment you may find Cytoscape useful for one of your two figures.

---

## Answers (for the plenary)

- **3.1** Force-directed shows clustering; circular is honest that position is arbitrary.
- **4.1** GAL4 has 10 neighbours in this subset. **4.2** MCM1's neighbours barely interact with each
  other (C = 0.06) — it is a hub between modules, not inside one.
- **5.1** Ratios are asymmetric (½ vs 2); logs make equal fold-changes equal and opposite (−1 vs +1).
- **5.2** GAL7 is the most up-regulated in the gal80 knock-out (sort the column to confirm).
- **5.3** Gal80 inhibits Gal4: remove the inhibitor and Gal4's targets rise. The GAL4–GAL80 edge is a
  protein–protein (`pp`) interaction, consistent with Gal80 binding Gal4 protein rather than
  regulating the GAL4 gene.
- **6.1** Yes — a protein that interacts with itself appears as a self-loop and is counted twice in
  Cytoscape's degree.
