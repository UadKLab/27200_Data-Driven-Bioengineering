YOUR OWN EXPLORER                                                Third - about 20 min

WHAT YOU WILL DO
Build an interactive tool for a large embedding. Then use a statistic to decide whether a
cluster you can see is real, or a covariate in disguise.


THE DATA
  umap_spectra_25k.csv   25,000 mass spectra, embedded by a spectrum foundation model
                         (InstaNovo-FM) and projected with UMAP (random_state = 42),
                         with 26 columns of metadata: instrument, organism, project, ...

  Source:   Nieuwoudt et al., bioRxiv 2026, doi:10.64898/2026.09.03.747733
            The spectra come from 77 public PRIDE projects.
  Licence:  CC BY-NC 4.0. Public data, so a free AI tier is fine.


STEPS
  1. In a terminal, start your agent in this folder (see START_HERE.txt):
         cd path/to/exercises/2_visualization
         copilot      (or: agy, claude, codex)
     In the Codex app: open this folder as your project instead.
  2. Paste PART 1 of PROMPT.txt. Read the data profile, then type:  continue
     Do not @-attach umap_spectra_25k.csv: it is far bigger than the context window.
  3. Open explorer.html in your browser (double-click it in this folder). Try it: colour by
     instrument, then by organism. Select a region.
  4. Only now, paste PART 2. Then read covariates.md.

  Do the parts in this order. Part 1 gives you a picture; Part 2 tells you whether the
  picture means anything.


YOUR CHECKS
  1. The agent could not open explorer.html. What did you have to check by eye that it
     could not check itself?
  2. Colour by organism. Does it look as if the spectra cluster by organism?
  3. What did the covariate test say about organism within project? And instrument?
  4. How many project groups could actually test organism? Is that enough to trust it?
  5. In one sentence: why is "enriched in this region" not the same as "causes this region"?


IF YOU FINISH EARLY
  - "Add a 3-D view using umap3d_1, umap3d_2 and umap3d_3. Keep the 2-D view: they are
    separate fits, so the axes are not interchangeable."
  - "Which region would make the cleanest figure panel? Score regions by purity and by how
    much of the category they capture."

