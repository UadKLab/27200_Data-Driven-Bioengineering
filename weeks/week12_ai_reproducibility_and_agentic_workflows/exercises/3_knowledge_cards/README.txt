A SMALL KNOWLEDGE BASE                                          Start here - about 45 min

WHAT YOU WILL DO
Turn two papers and a table of proteomics results into a set of linked study cards: a small
knowledge base you can download and keep. Every claim on a card must quote the sentence in
the paper that supports it, and a script checks that the sentence is really there.

The script can check that a quote exists. Only you can check that it supports the claim.
That split - the machine checks what it can, you check the rest - is the point.


WHAT IS IN THIS FOLDER
  hypoxia_kb/            the knowledge base. This is what you download at the end.
    README.md            what the knowledge base is, the card format, the rules - read it
    sources/             the two papers, as plain text, and their citations
    tools/check_kb.py    the checking script
    concepts/  genes/    empty - the agent fills them
  PROMPT.txt             paste this into Gemini
  PROMPT_chat.txt        use this instead if you work in a chat assistant
  PROMPT_update.txt      if you finish early
  make_zip.py            packs hypoxia_kb/ into hypoxia_kb.zip for download
  new_paper/             a third paper, for PROMPT_update.txt
  pdf/                   the review as a PDF, if you want to see its figures

THE PAPERS
  Hofner2025   the study behind the proteomics exercise: KGN cells, 10 days at 1% O2      CC BY-NC 4.0
  Luo2022      a review of how cells respond to low oxygen                    CC BY 4.0
  Full citations are in hypoxia_kb/sources/SOURCES.md.


BEFORE YOU START
  The agent needs a table of differential proteomics results. This is the first exercise, so
  it uses results_reference.csv in this folder: our analysis of the same experiment. If you
  have already done the proteomics exercise, it uses your ../1_proteomics/results.csv.
  After the proteomics exercise, you can rebuild the gene cards from your own results.


STEPS
  1. In the Colab terminal:
         cd /content/exercise/3_knowledge_cards
         gemini
  2. Paste the whole of PROMPT.txt.
  3. The agent proposes 5 concept cards and 6 gene cards, and stops. Look at the gene list:
     are these really among your significant proteins? Then type:
         continue
  4. The agent writes the cards, runs the check, fixes what it reports, and makes
     hypoxia_kb.zip.
  5. Download it: Files panel on the left > 3_knowledge_cards > right-click hypoxia_kb.zip >
     Download. (Or use the "Download your work" cell in the notebook.)
  6. Unzip it. Open the hypoxia_kb folder in Obsidian (free, obsidian.md, "Open folder as
     vault"), or read the files in any text editor. Start with INDEX.md.


YOUR CHECKS
  Open hypoxia_kb/CHECK_REPORT.md and hypoxia_kb/CHANGELOG.md first.
  1. How many quotes did the script find word for word? What did the agent have to fix or
     delete (CHANGELOG.md)? Those are claims it would have given you unchecked.
  2. Pick three claims the script passed. Read each quote. Does it really support the
     claim - or does it only mention the same words?
  3. Your gene cards: does your result match what the papers say? If not, give a reason
     that is not "the agent was wrong".
  4. The two genes "neither paper mentions": search the papers yourself for the protein's
     other names. Is that really true? What did the agent write on those cards?
  5. Find everything marked (not from these sources). Is it right? How would you check?


IF YOU FINISH EARLY
  - Keep the knowledge base up to date: paste PROMPT_update.txt. It adds a 2025 paper on
    HIF-1α and NDRG1 in the human ovary. Then: did the agent update cards, or duplicate
    them? Under what oxygen level were the new paper's experiments done - and does that
    matter when you compare them with the KGN hypoxia results?
  - Open the graph view in Obsidian. Which card is the most connected? Does that make sense?


ESTIMATED QUOTA: 40 to 60 requests, plus about 20 for PROMPT_update.txt.


IF YOU USE A CHAT ASSISTANT INSTEAD
  Follow PROMPT_chat.txt. Paste the chat's answers, one after the other, into a new text
  file called cards.txt and upload it to this folder in Colab. Then, in a notebook cell:
      !cd /content/exercise/3_knowledge_cards && python make_zip.py --from-chat cards.txt
  That unpacks the cards, runs the check and makes hypoxia_kb.zip.
