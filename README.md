# 🚀 Venture Quest — Build & Validate

An interactive classroom game for teaching **venture creation, ideation and validation**
to business students. Students take one startup idea from a hunch to a tested opportunity
across five decision rounds, scored out of 100 with coaching feedback after every choice.

Built with [Streamlit](https://streamlit.io) — deploy once, share a single link, and the
whole class can play in the browser (laptop or phone). No installs for students.

---

## What it teaches

Each playthrough runs one venture through the lean-startup / customer-development loop:

| Round | Focus | Concept practised |
|------|-------|-------------------|
| 1 | Frame the opportunity | Narrow beachhead customer + **jobs-to-be-done** (problem-first, not solution-first) |
| 2 | Riskiest assumption | **Desirability / Feasibility / Viability**; test the fatal assumption first |
| 3 | Customer interview | **The Mom Test** — ask about past behaviour, never pitch |
| 4 | Design an experiment | **MVP as a test** (concierge, Wizard-of-Oz, pre-sale) + a falsifiable success metric |
| 5 | Read the evidence | **Pivot / Persevere / Kill** against a pre-set threshold |

Three built-in ventures — a **consumer app** (CampusEats), a **marketplace** (FitMates), and a
**B2B tool** (LedgerLite) — so students can replay and see the same validation logic apply
across very different business models.

---

## Run it locally (optional)

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Then open http://localhost:8501.

---

## Deploy it for your class (free) — 3 steps

### 1. Put it on GitHub
- Create a new **public** repository (e.g. `venture-quest`).
- Upload these three files to the repo root: `streamlit_app.py`, `requirements.txt`, `README.md`
  (drag-and-drop works: *Add file → Upload files* on GitHub).

### 2. Deploy on Streamlit Community Cloud
- Go to **https://share.streamlit.io** and sign in with your GitHub account.
- Click **Create app → Deploy a public app from GitHub**.
- Select your repo, set **Main file path** to `streamlit_app.py`, and click **Deploy**.
- First build takes ~1–2 minutes.

### 3. Share the link
- You'll get a URL like `https://your-app-name.streamlit.app`.
- Drop it in your LMS / slides. Students click and play — no login or install needed.

> **Tip for class:** have students play once individually (5–8 min), then run one venture
> together on the projector and debate each choice before revealing the feedback. The
> in-app *"Why this round matters"* expanders double as discussion prompts.

---

## Customising the game

All content lives in plain Python dictionaries near the top of `streamlit_app.py`:

- **`SCENARIOS`** — add your own venture: copy one block and edit the customer segments,
  problems, assumptions, MVP options and results. Give exactly **one** assumption
  `"riskiest": True`.
- **`INTERVIEW_QUESTIONS`** — add good/weak interview questions (tag each `"good"` or `"bad"`).

The game auto-includes any scenario you add to the list — no other code changes needed.

Scoring: five rounds × 20 points = **100**. Feedback colour-codes each answer
(green = strong, amber = partial, red = weak).

---

*Classroom activity by Dr Ash Najmaei.*
