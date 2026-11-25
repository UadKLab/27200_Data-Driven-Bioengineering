# Week 12 — AI, Reproducibility, Data Management and Agentic Workflows

**Date:** 26 November 2026  
**Instructors:** Kostas & Ajuna  
**Theme:** How to work productively and critically with AI-enabled computational workflows.

---

## Lecture: AI in biology and agentic workflows

The slides are on DTU Learn, under Week 12: one HTML file that opens in any browser, and a PDF.
Press ↓ on a slide to open its study note.

---

## Exercises

All three are optional: go as far as time allows, in class or at home, in this order.

| Order | Exercise | Folder | Time |
|---|---|---|---|
| Start here | A small knowledge base | [exercises/3_knowledge_cards](exercises/3_knowledge_cards) | ~45 min |
| Then | Differential proteomics | [exercises/1_proteomics](exercises/1_proteomics) | ~2 h |
| Then | Your own explorer | [exercises/2_visualization](exercises/2_visualization) | ~1 h 15 |

The full instructions are in [exercises/START_HERE.txt](exercises/START_HERE.txt). Each folder has a
`README.txt` with what to do and what to check, and a `PROMPT.txt` to paste into the agent.

### Download the exercises

Click **[27200_Week12_exercises.zip](27200_Week12_exercises.zip)**, then the download button
(*Download raw file*). The same zip is on DTU Learn under Week 12.

### Option A: Google Colab and Gemini CLI (free, nothing to install)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/UadKLab/27200_Data-Driven-Bioengineering/blob/main/weeks/week12_ai_reproducibility_and_agentic_workflows/exercises/exercise_setup.ipynb)

1. Get a free API key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey).
2. Open the set-up notebook with the badge above.
3. Click the key icon on the left, add a secret called `GEMINI_API_KEY`, paste the key, and switch
   on *Notebook access*.
4. Run the cells from top to bottom. Upload the zip when asked (not unzipped) and wait for `Ready.`
5. Open Colab's **Terminal** and start the first exercise:

   ```bash
   cd /content/exercise/3_knowledge_cards
   gemini
   ```

   If it asks how to sign in, choose *Use Gemini API key*. Then paste all of `PROMPT.txt`.

### Option B: already using Claude Code, Codex or the ChatGPT desktop app?

Then you can skip Colab and the API key, and work on your own computer.

1. Download the zip (above) and unzip it.
2. Open the exercise folder in your agent. In a terminal:

   ```bash
   cd exercises/3_knowledge_cards
   claude      # Claude Code
   codex       # Codex
   ```

   In a desktop app, choose that folder as the project or working folder.
3. Paste all of `PROMPT.txt`. The prompts are written for Gemini CLI but work in any agent.

To install one (both need an account, usually a paid plan):

| Tool | Install |
|---|---|
| Claude Code | macOS/Linux: `curl -fsSL https://claude.ai/install.sh \| bash` · Windows (PowerShell): `irm https://claude.ai/install.ps1 \| iex` · or the Claude desktop app, Code tab ([claude.com/download](https://claude.com/download)). [Docs](https://code.claude.com/docs/en/setup) |
| Codex | `npm install -g @openai/codex`, or the Codex app. [Docs](https://developers.openai.com/codex/quickstart) |

Sign in with your Claude or ChatGPT account the first time you start it.

### If something does not work

- Out of quota, or the agent will not start? Use any free chat assistant (Gemini, Claude, ChatGPT)
  with `PROMPT_chat.txt`: upload the data file, never paste the data itself.
- Keep a `NOTES.md` (every prompt asks for one). If a session stops, start a new one and type:
  *Read NOTES.md and continue from the next step.*
- Colab deletes everything when you close the session. The last cell of the notebook downloads
  your work as a zip.

All data in these exercises is public. Do not use free tiers like this for confidential or
unpublished data.
