# Final FYP — writing hub

One place to **orient yourself**, **link official assets**, and **point to code** while you write the thesis.

---

## Where you are now

| Area | Status |
|------|--------|
| **Interim (IPD)** | Done — see [IPD PDF](../ipd/w1998730_20221214_IPD.pdf) |
| **Product (CrackInt)** | Implemented and working — see **Application code** below |
| **ML / NER** | Training pipelines + metrics in **Training repo** (this workspace) |
| **Final thesis (Word)** | **To write** using the official template — start from template sections + IPD where still true, then align to current app + measured results |

---

## What we are doing

- Writing the **final FYP** in the **2025/26 Word template** (not starting from zero: reuse IPD + chapter drafts where valid).
- Keeping **facts** aligned with:
  - **Application:** `FYP/PROJECT` (frontend + backend + `API_OVERVIEW.md`).
  - **NER / datasets / metrics:** this repo (`model-traning-1:30`) + notebooks / evaluation outputs.

---

## Next steps (recommended order)

1. **Copy** the template to a working file (e.g. `CrackInt_Final_Thesis_W1998730.docx`) so the original template stays clean.
2. Fill **[THESIS-FACTS-SHEET.md](./THESIS-FACTS-SHEET.md)** (freeze endpoints, metrics, env flags — update as you go).
3. **Write first:** Ch 7 → 8 → 9 → 10 → Abstract; then update Ch 4–6 and Ch 1–3 to match the built system. **Ch 8:** [plan](./chapter-08-testing-PLAN.md) · [draft](./chapter-08-testing-DRAFT.md). **Ch 9:** [draft](./chapter-09-critical-evaluation-DRAFT.md). **Ch 10:** [draft](./chapter-10-conclusion-DRAFT.md).
4. Cross-check against **[thesis final checklist](../thesis-final-submission-checklist-from-template.md)**.

---

## How to do it (short workflow)

| Step | Action |
|------|--------|
| 1 | Open your **working** `.docx` (from template). |
| 2 | For any **feature** claim → check **PROJECT** + [API_OVERVIEW](../../../PROJECT/crackint-backend/API_OVERVIEW.md) (path below). |
| 3 | For any **ML number** → check **model-traning-1:30** notebooks / saved results / `THESIS-FACTS-SHEET.md`. |
| 4 | Paste **screenshots** from the running app into Design / Implementation / Testing. |
| 5 | Run **tests** (backend + manual checklist) and put **pass rate / metrics** in Ch 8. |
| 6 | Write **Abstract last** (≤300 words, 3 paragraphs, include **quantitative** results). |

See **[WORKFLOW.md](./WORKFLOW.md)** for a slightly longer version of the same flow.

---

## Official & reference documents (in this repo)

| Asset | Path |
|--------|------|
| **Final thesis template (Word)** | [`../[Template FYP -2025_26] Final Thesis .docx`](../%5BTemplate%20FYP%20-2025_26%5D%20Final%20Thesis%20.docx) |
| **Template plain-text export** (search / quick ref) | [`../thesis-template-2025-26-export.md`](../thesis-template-2025-26-export.md) |
| **Submission checklist (from template)** | [`../thesis-final-submission-checklist-from-template.md`](../thesis-final-submission-checklist-from-template.md) |
| **Sample “good” FYP (reference only)** | [`../sample-project/Pansilu_Ashinshana_Wijesiri_w19127880_20210021_FPR.pdf`](../sample-project/Pansilu_Ashinshana_Wijesiri_w19127880_20210021_FPR.pdf) — see [SAMPLE-FPR-REFERENCE-NOTES.md](./SAMPLE-FPR-REFERENCE-NOTES.md) (sample vs **2025/26** template) |
| **IPD submission (your interim PDF)** | [`../ipd/w1998730_20221214_IPD.pdf`](../ipd/w1998730_20221214_IPD.pdf) |
| **PPRS (proposal PDF, repo root)** | [`../../20221214_w1998730.pdf`](../../20221214_w1998730.pdf) |
| **Research gaps / novelty notes** | [`../ipd/research-gaps-and-novelty-reference.md`](../ipd/research-gaps-and-novelty-reference.md) |

> **Note:** The Word template and sample PDF are **not duplicated** here — this folder **links** to them so you maintain a single copy.

---

## Application code — CrackInt (frontend & backend)

Repo root: **`FYP/PROJECT`** (sibling of `model-traning-1:30`).

From the **`model-traning-1:30` repo root**, `PROJECT` is the **sibling folder** under `FYP/` (not inside this repo). Use:

| Part | Relative path (from `model-traning-1:30/`) | What it is |
|------|----------------|------------|
| **Backend** | `../PROJECT/crackint-backend/` | FastAPI, agents, ML, API routes |
| **Backend API reference** | `../PROJECT/crackint-backend/API_OVERVIEW.md` | Endpoints, payloads, env requirements |
| **Backend README** | `../PROJECT/crackint-backend/README.md` | Features, setup, NER paths |
| **Frontend** | `../PROJECT/crackint-frontend/` | Next.js App Router UI |
| **Frontend app routes** | `../PROJECT/crackint-frontend/app/` | `login`, `register`, `(dashboard)/…` |

From **`docs/final-fyp/`** (this README), the same folders are:

| Part | Relative path |
|------|----------------|
| **Backend** | `../../../PROJECT/crackint-backend/` |
| **API overview** | `../../../PROJECT/crackint-backend/API_OVERVIEW.md` |
| **Frontend** | `../../../PROJECT/crackint-frontend/` |

**Absolute paths (if you use Finder / Cursor “Open”):**

- `/Users/dinalbandara/Desktop/IIT/4th year/FYP/PROJECT/crackint-backend`
- `/Users/dinalbandara/Desktop/IIT/4th year/FYP/PROJECT/crackint-frontend`

---

## Training / ML repo (this workspace)

| Part | Path |
|------|------|
From **repository root** `model-traning-1:30/`:

| Folder | Path |
|--------|------|
| **Résumé NER pipeline** | `resume_ner_pipeline/` |
| **Job poster NER pipeline** | `job_poster_ner_pipeline/` |
| **Notebooks / FYP** | `fyp/` |
| **Root tests** (e.g. session QA) | `test_session_qa_*.py`, etc. |

From **`docs/final-fyp/`**, same as: `../../resume_ner_pipeline/`, `../../job_poster_ner_pipeline/`, `../../fyp/`.

---

## Files in this folder

| File | Purpose |
|------|---------|
| **README.md** (this file) | Hub: status, links, paths, next steps |
| **[WORKFLOW.md](./WORKFLOW.md)** | Expanded writing order + tips |
| **[THESIS-FACTS-SHEET.md](./THESIS-FACTS-SHEET.md)** | Fill in: frozen metrics, key endpoints, env flags (your single fact sheet) |
| **[SUGGESTIONS-BEFORE-FINAL-RUN.md](./SUGGESTIONS-BEFORE-FINAL-RUN.md)** | Checklist: backups, integrity, examiner view |
| **[IMPLEMENTED-VS-PENDING-FINAL.md](./IMPLEMENTED-VS-PENDING-FINAL.md)** | **FR/NFR vs backend API** — use for SRS + evaluation chapters |
| **[chapter-07-implementation-DRAFT.md](./chapter-07-implementation-DRAFT.md)** | **Chapter 7 (Implementation) — thesis draft** — paste into Word; includes sample-FPR structure notes |
| **[chapter-08-testing-PLAN.md](./chapter-08-testing-PLAN.md)** | **Chapter 8 (Testing) — IIT §8.1–8.11 mapped to CrackInt** |
| **[chapter-08-testing-DRAFT.md](./chapter-08-testing-DRAFT.md)** | **Chapter 8 (Testing) — thesis draft** — NER tables, functional/NFR outline, placeholders for pass rate |
| **[chapter-09-critical-evaluation-DRAFT.md](./chapter-09-critical-evaluation-DRAFT.md)** | **Chapter 9 (Critical evaluation) — thesis draft** — criteria, self-eval, FR/NFR tables 9.1–9.2, honest expert scope |
| **[chapter-10-conclusion-DRAFT.md](./chapter-10-conclusion-DRAFT.md)** | **Chapter 10 (Conclusion) — thesis draft** — **Table 10.1** (R02–R22 from IPD), **Table 10.2** (LO1–LO9 mapping), deviations, limitations |
| **[WORD-THESIS-STRUCTURE-ALIGNMENT.md](./WORD-THESIS-STRUCTURE-ALIGNMENT.md)** | **Fix Word TOC/chapters** — Ch 8 = Testing only; Gantt belongs in Ch 3 (2025/26 template) |
| **[FINAL-FYP-MARKING-SCHEME-SUMMARY.md](./FINAL-FYP-MARKING-SCHEME-SUMMARY.md)** | **Official final FYP rubric** (from `6COSC023W_...xlsx`) — weights, chapter expectations, grade bands |

---

*Last updated: created for final FYP writing phase.*
