# FYP demo video — outline and shot list (CrackInt)

**Purpose:** Plan your **unlisted YouTube** submission (max **30 minutes**, **one link**). Align with IIT mandatory structure: **(1) Problem & research gap → (2) Solution & technical design + code walkthrough → (3) System demonstration** with **positive** and **negative** test cases.

**Read-aloud script (end-to-end):** see **`DEMO-VIDEO-FULL-SCRIPT.md`** in this folder — speak the main text; use **bold [SCREEN:] / [ACTION:]** lines as cues only. That file includes a **table of exact paths** (`app/ml/resume_ner.py`, `app/api/deps.py`, notebook `fyp/BiLSTM_CRF_Resume_NER_Path2_FYP.ipynb` sections) for the code walkthrough.

**Tips:** Script a loose talk track; record in **1080p**; use **clear audio**; **redact** API keys and personal emails in code/browser; keep a **timer** so part 3 does not swallow the whole video.

---

## Suggested time budget (adjust to your pace)

| Block | Target time | Notes |
|--------|-------------|--------|
| Part 1 — Problem & gap | 3–5 min | Mostly you + optional 1–2 slides |
| Part 2 — Design & code | 8–12 min | Architecture + short IDE/Swagger/notebook |
| Part 3 — Live demo | 12–18 min | Browser + optional API tool; show pass **and** fail paths |
| Buffer / recap | 1–2 min | Optional “thank you / links” (no secrets) |

**Total:** stay under **30 minutes**. If long, use a **playlist** (one link) per module instructions.

---

## Part 1 — Problem & research gap (what to say & show)

### What to say (talking points)

1. **Problem (30–60 s)**  
   - Graduates and job seekers need **personalised interview preparation** tied to their **CV** and **target roles**.  
   - Manual prep is **time-consuming** and not always **structured** or **feedback-rich**.

2. **Who it affects (20–40 s)**  
   - e.g. final-year students, career switchers, high-volume applicants.

3. **Research / practice gap (60–90 s)**  
   - Generic chat tools are **not** grounded in **your** résumé and **a specific job description**.  
   - You justify **your** approach: **structured entity extraction (NER)** for résumé + job text, **skill-gap** analysis, **prep sessions** with **optional LLM** coaching — integrated in **one** product (**CrackInt**).  
   - Mention **one or two** limitations of “CV parsers only” or “Q&A apps only” that your system combines (keep it examinable, not marketing).

### Where to demonstrate

- **Optional:** 1–2 slides (title, problem diagram) **or** full-screen **browser on project landing/login** while you voiceover.  
- **No code yet** unless you flash a **high-level diagram** (browser, Next.js → FastAPI → DB / NER / LLM).

---

## Part 2 — Solution & technical design + code walkthrough (what to say & show)

### What to say (talking points)

1. **Solution in one sentence**  
   - CrackInt: **full-stack** app — **résumé & job understanding** (NER), **matching / skill-gap**, **authenticated** **practice sessions**, **readiness** views; **LLM** features when configured.

2. **Architecture (2–4 min)**  
   - **Frontend:** Next.js (App Router), calls REST API with **JWT**.  
   - **Backend:** FastAPI, **PostgreSQL**, **NER** checkpoints (**Appendix G** paths / env names only — **do not** show secret values).  
   - **ML:** **Word2Vec + BiLSTM + CRF** for résumé and job-poster NER (point to **Chapter 7 / frozen run** in speech).  
   - Optional: **one diagram** (from thesis Design chapter) on screen.

3. **Code walkthrough (mandatory — 4–8 min)**  
   Pick **two short** locations (10–40 lines each), paste or scroll slowly:

   | Location | Why show it |
   |----------|-------------|
   | **Hybrid résumé extraction** (e.g. rules + model) | Shows **novel integration**, not only “we called an API”. |
   | **JWT / protected route** or **session chat → LLM** | Shows **security** and **agent** flow. |
   | **Training notebook** — `BiLSTMCRF` **or** training loop **or** `parse_resume_path2` | Links **implementation** to **report tables** (splits, F1). |

   Say **what** the snippet does, **not** every line.

4. **Data / models (1–2 min)**  
   - Entity types for **résumé** vs **job**; **test F1** at high level (**~0.83** résumé, **~0.85** job-poster — match thesis).  
   - **Do not** claim numbers that are not in the report.

### Where to demonstrate

- **VS Code / Cursor** or **Jupyter** (zoomed, large font).  
- **Swagger UI** (`/api/v1/docs`): show **2–3** key endpoints exist (auth, résumé extract, session) — quick, not a full tour.  
- **Thesis PDF** (optional): flash **Table 7.1 / 7.2** or architecture figure for **5–10 seconds** if it helps.

---

## Part 3 — System demonstration (positive & negative cases)

### Setup before recording

- **Backend + DB + frontend** running (or deployed URL).  
- **Test user** created; **sample PDF/text** résumé and **job** text ready.  
- **NER** directories loaded if you claim extraction in demo.  
- Decide whether **LLM** is **on** (full path) or **off** (show **graceful** behaviour for “negative” or partial).

### Positive test cases (show **at least 3–4**)

Record **screen + short narration** for each: what you click, what you expect.

| # | Flow | What examiners should see |
|---|------|----------------------------|
| P1 | **Register → Login** | Account works; JWT protects pages. |
| P2 | **Upload / extract résumé** | Entities populated (NAME, SKILL, …) or sensible structure. |
| P3 | **Edit / save entities** (if in UI) | Persistence after refresh. |
| P4 | **Job extract** or **job posting** | Job-side entities or clear fallback. |
| P5 | **Skill-gap / match** | Structured output (skills missing / match view). |
| P6 | **Prep session** — message or chat turn | History visible; if LLM on, question or feedback appears. |
| P7 | **Dashboard / readiness / home-summary** | Non-empty or valid empty state. |

You do **not** need every row — pick what best matches **your** final build.

### Negative / edge test cases (show **at least 2–3**)

| # | Flow | Expected behaviour to **narrate** |
|---|------|-------------------------------------|
| N1 | **Protected page or API without token** | **401** / redirect to login — **security**. |
| N2 | **Invalid login** | Clear error, no crash. |
| N3 | **Empty file / corrupt upload / oversize** (if safe) | Validation or error message (**4xx**), not stack trace to user. |
| N4 | **LLM off or no API key** | **503** or message: feature unavailable — **documented** partial behaviour (tie to **Appendix D / Ch 8**). |
| N5 | **Job extract with minimal text** | Degraded but stable response. |

### Where to demonstrate

- **Primary:** **Browser** — full CrackInt UI.  
- **Optional:** **Swagger** or **curl** for one **401** response (negative case) if faster than UI.  
- **Zoom** the important panel; **pause** 2–3 seconds on key JSON or UI state.

---

## Closing (optional, 30–60 s)

- One line: what you **delivered** vs **future work** (short).  
- **No** live secrets; **no** private repo URLs unless they are **submission** links examiners may use.

---

## Pre-submission checklist

- [ ] Video has **all three** compulsory blocks in order (even if part 1 is short).  
- [ ] **Code walkthrough** appears in part 2 (not only screenshots).  
- [ ] Part 3 includes **positive** and **negative** cases, **visible** on screen.  
- [ ] Length **≤ 30 min** (or **playlist** + one link).  
- [ ] YouTube **Unlisted**; link opens in **incognito** / logged-out browser.  
- [ ] Audio levels OK; cursor visible; text readable.

---

## File location

Save this plan next to your thesis drafts: `docs/final-fyp/DEMO-VIDEO-OUTLINE.md`. Update the **P/N** rows to match your **actual** routes and UI labels before you record.
