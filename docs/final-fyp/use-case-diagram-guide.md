# CrackInt — Use case diagram: how to build it yourself

This guide explains **how to draw** a clean UML use case diagram in **draw.io (diagrams.net)**, what **flows** each core use case represents, and **which extra use cases** you may add based on **implemented backend and product features** (see `IMPLEMENTED-VS-PENDING-FINAL.md` in this folder).

**Sources of truth for features:** `docs/final-fyp/IMPLEMENTED-VS-PENDING-FINAL.md`, backend `app/api/router.py`, and Swagger at `/api/v1/docs`.

---

## 1. What tool to use

| Tool | Best for |
|------|-----------|
| **draw.io (diagrams.net)** | Free, UML shapes, export PNG/SVG for Word — **recommended** |
| **Astah UML** | Stricter UML if you already use it |
| **PlantUML** (`@startuml` … `@enduml`) | Text-first; good if you like version-controlled diagrams |

**Export for thesis:** PNG at **2×** scale or **SVG**, then insert into Word. Use one **font** and **line weight** for all figures.

---

## 2. Diagram rules (keep the viva simple)

1. **One system boundary** — Label it **CrackInt** (or “CrackInt System”).
2. **Primary actor** — For the **main** figure, use **one** actor: **Job seeker** (your §4.9 table). Add a caption note if personas include students and early-career users — they are the same *role*, not three actors.
3. **Use cases = user goals**, not every button. Put step-by-step detail in **Appendix B** or §4.9.1 text.
4. **Secondary actors** — Only **external** systems or people: e.g. **Email provider**, **AI/LLM API**, **Object storage (S3)**. Do **not** draw **BiLSTM-CRF NER** as an actor if it runs **inside** your backend; it is part of CrackInt.
5. **Relationships** — Solid lines from primary actor to use cases; **dashed** lines to secondary actors. Add **`<<include>>`** / **`<<extend>>`** only where the behaviour is always true or optional (see §5).

---

## 3. Baseline use cases (match §4.9, Table 1)

These six are enough for a **clear** “core” diagram.

| ID | Use case name (short) | What “flow” means (high level) |
|----|------------------------|--------------------------------|
| **UC-01** | Register and create profile | User registers → optional email verification path → profile exists → JWT session for later calls. **Implemented:** `POST /api/v1/auth/register`, login, `GET /me`; Google OAuth if configured. |
| **UC-02** | Upload and parse résumé | User uploads PDF/text → text extraction → **in-platform** NER (`parse_resume_hybrid`) → structured entities → persisted. User may **review/edit** entities. **Implemented:** extract, list, get, `PATCH /resumes/{id}`. **Partial:** DOCX — verify in `text_extraction` before claiming in SRS. |
| **UC-03** | Generate role-specific questions | Preconditions: résumé (and typically **job context**) available → session created → questions emitted **via** `POST /sessions/{id}/chat` (unified turn), not a separate “get next question” call from the UI. **Partial:** needs `OPENAI_API_KEY` for LLM; question count is agent behaviour — document in Ch 7. |
| **UC-04** | Practice with semantic feedback | Chat session → each user send → **`POST .../chat`** persists the turn and runs classification, evaluation, and next-question logic server-side → FEEDBACK messages (with scores in `meta` when applicable). **Partial:** follow-ups and rubric depend on agent implementation. |
| **UC-05** | View progress analytics | Dashboard / readiness / trend / home summary. **Partial:** “charts” are frontend; backend supplies summary/trend APIs. |
| **UC-06** | Manage account settings | Profile, multiple résumés, preferences as implemented. **Partial:** full preferences UI — verify before claiming. |

### 3.1 Narrative flows (for your prose, not every arrow on the diagram)

**Flow A — Onboarding:** UC-01 → (authenticated) → UC-02.

**Flow B — Target role context:** After UC-02, user adds job text or **job posting** (see §4) → data available for UC-03.

**Flow C — Practice loop:** UC-03 (question) ↔ UC-04 (answer + feedback) until session ends; persistence satisfies FR14-style behaviour.

**Flow D — Insight:** UC-05 reads historical sessions / readiness (depends on UC-04 data existing).

**Flow E — Analyse résumé and receive CV feedback (strength / scoring):**  
After **UC-02** (parsed résumé stored and entities available), the user runs **CV analysis / feedback** — a **separate goal** from “parse entities” (NER) and from **UC-04** (interview answer feedback).

1. Preconditions: authenticated user; at least one **saved résumé** with extracted content (from UC-02).  
2. User requests **résumé strength score / written feedback** (narrative strengths, gaps — whatever your UI exposes).  
3. Backend: **`POST` / `GET` … `/resumes/score`** (LLM-based when enabled). Requires **`CV_SCORING_ENABLED`** and **`OPENAI_API_KEY`** — treat as **partial** in the thesis if flags or keys can be off.  
4. Output: score and/or text feedback shown in UI; user may use it before job matching or practice.

**Diagram hint:** Add an optional oval **“Analyse résumé strength (CV feedback)”** (maps to **UC-11** in §4). Link **Job seeker** → that oval. **Dashed** line from **AI service** → that oval (not to NER-only parsing). **Do not** merge this with UC-04 unless your product literally uses the same screen for both — interview feedback and CV scoring are different *goals*.

**Flow F — Check job poster against CV (fit / skill gap):**  
This is the **résumé ↔ job** alignment flow — different from parsing the job alone (**UC-07**) or parsing the CV alone (**UC-02**).

1. Preconditions: **stored résumé** (UC-02) **and** a **job description or saved job posting** (UC-07) the user wants to compare against.  
2. User opens **match / skill gap** (or equivalent screen) and triggers analysis.  
3. Backend: **`POST /match/skill-gap`** — **implemented** (compares résumé entities vs job posting / JD). Optional extras such as LLM “fit” may be gated — check `config.py` / agent flags and document honestly.  
4. Output: gaps, matched skills, alerts — feeds user decisions before **UC-03** (questions) or **UC-04** (practice).

**Diagram hint:** Add an oval **“View skill gap / job match”** (maps to **UC-09** in §4). Link **Job seeker** → UC-09. **Include** relationships on the diagram are optional; in text, state **«precedes»** UC-03: user often checks match **before** starting a targeted session.

**How E and F sit next to the core six:** You can keep **UC-01–UC-06** on the main diagram and add **UC-09** and **UC-11** on the same page *if there is space*, or on a **second diagram** titled e.g. *“CrackInt — résumé analysis and job fit”* to avoid clutter.

---

## 4. Optional extra use cases (only if implemented or honestly “partial”)

Add **separate ovals** only when they represent a **distinct goal** you will describe in SRS and test in Ch 8. Map to current implementation status.

| Suggested UC ID | Use case (name) | Status | Notes |
|-------------------|-----------------|--------|--------|
| UC-07 | Provide job description / job posting | **Implemented** | `POST /jobs/extract`; job postings CRUD `/job-postings` |
| UC-08 | Confirm or edit extracted entities | **Implemented** | `PATCH /resumes/{id}` |
| UC-09 | View skill gap (résumé vs job) | **Implemented** | `POST /match/skill-gap` — see **Flow F** in §3.1 |
| UC-10 | Generate or manage cover letter | **Partial** (LLM) | `/cover-letter/*`, feature flags + API key |
| UC-11 | Analyse résumé / CV feedback (strength score) | **Partial** (LLM) | `/resumes/score`, `CV_SCORING_ENABLED` — see **Flow E** in §3.1 |
| UC-12 | Upload image to cloud storage | **Partial** | `/uploads/image`, S3 when configured |
| UC-13 | Use speech input in session | **Partial** | STT + Socket.IO — only if you demo it |
| UC-14 | Export progress as PDF | **Pending** | **Do not draw** as delivered unless you implement FR17 |

**Pending / not recommended on the main diagram unless you build them:** email notifications (FR23), full-text session search (FR22), dedicated admin error dashboard (FR25).

---

## 5. Includes, extends, and secondary actors (minimal pattern)

- **`<<include>>`** — Child use case is **always** part of the parent (e.g. “Authenticate” included by “Upload résumé” **only if** every upload strictly requires a fresh login — usually **omit** and state preconditions in text).
- **`<<extend>>`** — Optional extension (e.g. “Get hint” extends “Practice” **only if** hints exist — FR20 was pending/TBC).
- **Email service** — Associate with **UC-01** if verification emails are real; otherwise mention in narrative only.
- **AI service (e.g. OpenAI)** — Associate with **UC-03**, **UC-04**, **UC-11** (CV scoring/feedback), and optionally **UC-10** when flags + keys are required — **not** with pure NER parsing if NER is local. **UC-09** (skill gap) may be mostly **in-platform** matching; only add an AI actor here if your implementation calls an LLM for fit narrative — verify in code before drawing.

---

## 6. Ready-made diagrams (HTML + SVG)

| File | What it shows |
|------|----------------|
| **`docs/final-fyp/diagrams/crackint-use-case-diagram.html`** | **Simplified thesis view:** one **Job seeker** actor, UC-01–UC-06 plus UC-09 / UC-11, optional AI actor. Easier to align with §4.9 Table 1. |
| **`docs/final-fyp/diagrams/crackint-use-case-diagram-full.html`** | **Entire CrackInt-style view** in **horizontal swimlanes** (rows): documents and practice flows read **left → right**; **Job seeker, Student, Early career** → **Primary user**, **Career service**, **System administrator**; **blue `<<include>>`** in the top two rows; **grey associations** from **Primary user** (one line per oval). External AI/S3 as dashed lines. |

Open either file in a browser. Export via **Print → Save as PDF** or a **screenshot** for Word. Edit the SVG in the same file to tweak labels or actors. The **full** diagram is dense — use draw.io if you need pixel-perfect layout.

---

## 7. Step-by-step in draw.io

1. Open [https://app.diagrams.net](https://app.diagrams.net) → **Create new diagram**.
2. **More shapes** → enable **UML** (search “use case”).
3. Drag a **large rectangle** → title: **CrackInt**.
4. Add **one stick figure** left: **Job seeker**.
5. Add **six ellipses** inside the box: UC-01 … UC-06 (use short names from §3).
6. **Connect** Job seeker to each ellipse with straight lines.
7. Optional: add **secondary actors** (cloud/database icons or stick figures) **outside** the box; **dashed** lines to UC-01 (email), UC-02/UC-12 (S3 if used), UC-03/UC-04/UC-10/UC-11 (AI).
8. Optional second page: **“Extended use cases”** with UC-07–UC-13 so the first page stays readable — or add **UC-09** (Flow F) and **UC-11** (Flow E) to a dedicated **“Résumé analysis & job fit”** diagram.
9. **Align** ellipses to a grid; keep **parallel** text; export **PNG (2×)** or **SVG**.

---

## 8. Caption text you can paste under the figure

> **Figure X.Y** — Use case diagram for CrackInt showing the primary actor (job seeker) and core use cases for registration, résumé parsing, role-aware practice, feedback, analytics, and account management. Optional use cases for **résumé strength / CV feedback** and **skill-gap / job match** may be included as separate goals (see Flows E and F). Secondary actors (e.g. email, LLM API, object storage) are shown only where the system delegates to an external service. Résumé entity extraction is performed by in-platform NER (BiLSTM-CRF) unless otherwise stated in Chapter 7.

Adjust the last sentence to match your exact thesis claims.

---

## 9. When you change the code

Re-run through **Swagger** and update **`IMPLEMENTED-VS-PENDING-FINAL.md`**, then **add/remove ovals** so the diagram never claims **pending** features as shipped.

---

*This guide is a thesis helper for CrackInt; it does not replace your supervisor’s UML preferences.*
