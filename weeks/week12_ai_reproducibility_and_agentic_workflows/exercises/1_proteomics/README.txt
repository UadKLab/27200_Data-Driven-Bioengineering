DIFFERENTIAL PROTEOMICS                                          Start here - about 30 min

WHAT YOU WILL DO
Take real output from a published proteomics experiment and use an agent to find the
proteins that change between two conditions. Running the analysis is the easy part.
The point of the exercise is checking it.


THE DATA
  proteinGroups.txt     MaxQuant protein table (some columns removed, otherwise unchanged)
  sample_metadata.csv   one row per sample: condition, replicate, batch

  Source:   PRIDE PXD056016
  Paper:    Höfner et al., Reproduction and Fertility 6(4): e250017, 2025
            doi:10.1530/raf-25-0017
  Licence:  CC BY-NC 4.0. Public data, so a free AI tier is fine.


STEPS
  1. In a terminal, start your agent in this folder (see START_HERE.txt):
         cd path/to/exercises/1_proteomics
         copilot      (or: agy)
     In the Codex app or the Claude app (Code tab): open this folder as your project instead.
  2. Type:  Read PROMPT.txt and follow it.   (or paste the whole of PROMPT.txt)
     Do not @-attach proteinGroups.txt: it is far bigger than the context window.
  3. After step 1 the agent stops. Read what it found. Does the sample mapping look right?
     Then type:  continue
  4. When it finishes, open volcano.png and read RESULTS.md (both in this folder).
     Keep results.csv: the knowledge-base exercise (the last one) builds its gene cards from it.


YOUR CHECKS  -  answer these yourself before comparing with anyone else
  1. Before you look at the results: what is the experiment? Which proteins or pathways
     would you expect to change, and in which direction? Write your list down.
  2. Did they change as you expected? If not, is the biology surprising - or is the
     pipeline broken? How would you tell the difference?
  3. In the shuffled data, how many proteins passed FDR? What should that number be?
  4. Did the agent notice how the samples were processed? Did it do anything about it?
  5. The paper reports 132 proteins that changed. How many did you find? Give two reasons
     why the numbers could differ.
  6. Could you re-run analysis.py without the agent? Try it in a new terminal, in this folder:
         python3 analysis.py      (on Windows: python analysis.py)


IF YOU FINISH EARLY
  - "Refit this as a linear model with batch as a covariate. Which proteins change status?"
  - "I do not believe protein X. Show me its raw intensity in every sample."
  - "Make the volcano plot interactive, so hovering a point shows the gene and its values."

