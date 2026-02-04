# IPD: Current State Audit

**Purpose:** Plan Phase 1, Step 1 — list what is done vs not done for the CrackInt prototype and IPD submission.

---

## Done

### NER and data (model-traning-1:30)

- **Resume NER:** Training pipeline, BERT-BiLSTM-CRF model; data in `resume_ner_pipeline/` (annotations, merged JSON); notebooks in `fyp/BERT_BiLSTM_CRF_Resume_NER_FYP.ipynb`, `resume_ner_pipeline/`. Model published to Hugging Face `dinalUdagedara/resume-entity-extractor`.
- **Job poster NER:** Training pipeline and model in `job_poster_ner_pipeline/`, `fyp/job-poster-ner/`; data (e.g. `merged_job_poster_ner.json`, skillspan).

### Prototype app (PROJECT)

- **Backend (crackint-backend):**
  - FastAPI; resume extract (PDF + text) → text extraction (PyMuPDF) → resume NER (`app/ml/resume_ner.py`) → persist to PostgreSQL; list/get/update/PATCH/delete resumes.
  - Job extract API: `POST /api/v1/jobs/extract` (PDF or text) → job poster NER when `JOB_POSTER_NER_LOAD_DIR` set, else resume NER fallback; no persistence.
  - Health check; OpenAPI docs at `/api/v1/docs`; Alembic migrations; config (e.g. `RESUME_NER_LOAD_DIR`, `JOB_POSTER_NER_LOAD_DIR`).
- **Frontend (crackint-frontend):**
  - Next.js; CV Upload page: file drop + paste → call `POST /api/v1/resumes/extract` → display entities → Edit dialog (PATCH); resume list (admin); sidebar, breadcrumbs; `resume-uploader.service.ts` and API proxy.

### IPD documentation

- **docs/ipd/requirements-analysis.md** — submission rules, marking criteria, slide structure, checklist.
- **docs/project/proposal-summary.md** — PPRS summary (stakeholders, FR/NFR, use cases, Gantt).
- **docs/ipd/requirements-implemented-vs-pending.md** — FR/NFR table with Implemented / Partial / Pending and locations.

---

## Not done (for IPD / post-IPD)

- **User auth:** No registration or login (FR01, FR02); optional `user_id` in backend only.
- **Job description UI:** Backend job extract exists; no frontend page or form to paste/upload job and show entities (FR06/FR07 partial on FE).
- **Question generation:** No LLM integration for role-specific questions (FR08).
- **Chat / practice session:** No interview Q&A flow, no semantic feedback (FR09–FR13).
- **Session history and analytics:** Resumes saved; no practice sessions, scores, or dashboards (FR14–FR16).
- **Profile, preferences, export, fallbacks, email:** FR17–FR24 not implemented.
- **Security and privacy:** No bcrypt, S3, GDPR flows, or JWT (NFR01, NFR14–NFR16).
- **Hosting:** No deployed frontend/backend; no public or supervisor-facing runnable link.
- **Google Drive submission:** Source (and optional dataset) not yet in a shared folder with public link and README for IPD.
- **Slides and videos:** Presentation deck and recording/upload/submit not done.

---

## Summary

| Area              | Done                                                                 | Not done                                              |
|-------------------|----------------------------------------------------------------------|-------------------------------------------------------|
| Resume NER        | Training, model, Hugging Face; backend + frontend flow              | —                                                     |
| Job NER           | Training, model; backend API only                                    | Frontend job input + display                          |
| Question gen      | —                                                                    | LLM integration, chat UI                              |
| Semantic feedback | —                                                                    | Evaluation and feedback pipeline                     |
| Auth / security   | —                                                                    | Registration, bcrypt, JWT, S3, GDPR                   |
| Hosting / submit  | —                                                                    | Deploy FE/BE; Google Drive link; README               |
| IPD docs          | Requirements analysis, PPRS summary, implemented vs pending, audit, scope, architecture | Slides, videos                                        |
