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

You work on your own computer, with a coding agent. All three exercises are optional: go as far
as time allows, in class or at home, in this order.

| Order | Exercise | Folder | Time |
|---|---|---|---|
| Start here | A small knowledge base | [exercises/3_knowledge_cards](exercises/3_knowledge_cards) | ~15 min |
| Then | Differential proteomics | [exercises/1_proteomics](exercises/1_proteomics) | ~30 min |
| Then | Your own explorer | [exercises/2_visualization](exercises/2_visualization) | ~20 min |

The full instructions are in [exercises/START_HERE.txt](exercises/START_HERE.txt). Each folder has a
`README.txt` with what to do and what to check, and a `PROMPT.txt` for the agent.

### 1. Install one agent (before class)

Pick the one you have an account for.

| Agent | Account | Install | Start |
|---|---|---|---|
| [Codex app](https://developers.openai.com/codex/quickstart) (OpenAI) | ChatGPT, free plan included | download the app from the page; no terminal needed (or `npm install -g @openai/codex` for the CLI) | open the app |
| [GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/set-up/install-copilot-cli) | GitHub, free plan included; more on the student plan | `npm install -g @github/copilot` | `copilot` |
| [Antigravity CLI](https://antigravity.google) (Google) | personal Google account, free tier | macOS/Linux: `curl -fsSL https://antigravity.google/cli/install.sh \| bash` · Windows (PowerShell): `irm https://antigravity.google/cli/install.ps1 \| iex` | `agy` |
| [Claude Code](https://claude.com/download) (Anthropic) | paid Claude plan | download the Claude app from the page; no terminal needed | open the app's **Code** tab |

You also need:

- [Node.js](https://nodejs.org) (the LTS version) for the `npm` commands (Copilot CLI, or Codex in the terminal)
- [Python 3](https://www.python.org/downloads/), because the agents write and run Python

Sign in with your account the first time you start the agent. The free tiers are small: read what
the agent prints before you ask again, and keep prompts specific.

### 2. Download the exercises

Click **[27200_Week12_exercises.zip](27200_Week12_exercises.zip)**, then the download button
(*Download raw file*). The same zip is on DTU Learn under Week 12. Unzip it.

### 3. Start an exercise

**Codex app, or the Claude app (Code tab):** open the exercise folder as your project (choose a folder when you start).

**In a terminal:** go into an exercise folder and start your agent there:

```bash
cd path/to/exercises/3_knowledge_cards
copilot      # or: agy
```

The agent can read and write the files in that folder. Then type *Read PROMPT.txt and follow it*,
or paste the whole of `PROMPT.txt`.

### Giving the agent files

The agent already sees every file in the folder you started it in. To point at one file in your
message, type `@` and the file name:

| Agent | How |
|---|---|
| Codex app | Type `@` and pick the file, or drag the file into the message box |
| Copilot CLI | `Explain @README.txt`, or drag a file from your file browser into the terminal |
| Antigravity CLI | `Summarise @sources/SOURCES.md`; if your version does not complete it, just write the file name |
| Claude app (Code tab) | Type `@` and pick the file, e.g. `@PROMPT.txt` |

Do **not** attach the data files (`proteinGroups.txt`, `umap_spectra_25k.csv`): they are far bigger
than the context window. Name them, and let the agent read them with code.

The agent asks before it runs a command or changes a file. Read what it wants to do, then approve.
Do not switch on "approve everything" modes on your own computer.

### If a session stops

Every prompt asks the agent to keep a `NOTES.md`. Start a new session in the same folder and type:
*Read NOTES.md and continue from the next step.*

All data in these exercises is public. Do not use free tiers like this for confidential or
unpublished data.
