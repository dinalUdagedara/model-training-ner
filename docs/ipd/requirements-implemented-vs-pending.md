# IPD: Formal Requirements — Implemented vs Pending

**Purpose:** Single source for the IPD "Formal requirements specification" slide and for progress-since-PPRS.  
**Prototype location:** PROJECT — `crackint-frontend` + `crackint-backend`.  
**NER training / data:** Repository root — `resume_ner_pipeline/`, `job_poster_ner_pipeline/`, `fyp/`.

---

## Functional requirements (FR)

| ID | Requirement (one-line) | Status | Where / notes |
|----|-------------------------|--------|----------------|
| FR01 | Register with email, password, basic profile | **Pending** | Not implemented; optional `user_id` in backend for testing only. |
| FR02 | Secure auth, encrypted password storage | **Pending** | No auth layer yet. |
| FR03 | Accept resume uploads PDF/DOCX (max 5MB) | **Implemented** | PROJECT: backend `app/api/resume/route.py` (PDF; DOCX not in backend); frontend `CVFileDropZone`, `CVPasteArea` → `POST /api/v1/resumes/extract`. |
| FR04 | Parse resumes; extract NAME, EMAIL, SKILL, OCCUPATION, EDUCATION, EXPERIENCE (NER) | **Implemented** | PROJECT: `app/ml/resume_ner.py` (BERT-BiLSTM-CRF + hybrid rules), `app/api/resume/service.py`; model from Hugging Face or `RESUME_NER_LOAD_DIR`. |
| FR05 | Allow users to review and manually edit extracted resume info | **Implemented** | PROJECT: frontend `EditEntitiesDialog`; backend `PATCH /api/v1/resumes/{id}`. |
| FR06 | Accept job description via text paste or job title entry | **Partial** | Backend: `POST /api/v1/jobs/extract` (file or form `text`). No frontend UI yet; no job title entry. |
| FR07 | Analyze job descriptions: extract required skills, qualifications, responsibilities | **Partial** | PROJECT: `app/ml/job_poster_ner.py`, `app/api/job/service.py` when `JOB_POSTER_NER_LOAD_DIR` set; else resume NER fallback. |
| FR08 | Generate 10–15 personalized, role-specific questions (LLM from resume + job) | **Pending** | Not in PROJECT. |
| FR09 | Present questions in chat-based, conversational interface | **Pending** | Frontend has chat-related components (e.g. `ChatInputView`) but no interview Q&A flow. |
| FR10 | Allow users to submit text-based responses to interview questions | **Pending** | Not implemented. |
| FR11 | Evaluate responses using semantic analysis (depth, relevance, structure, clarity) | **Pending** | Not implemented. |
| FR12 | Real-time feedback: score 0–100, strengths, areas for improvement, actionable suggestions | **Pending** | Not implemented. |
| FR13 | Conversational follow-up questions (e.g. "Why was this weak?") | **Pending** | Not implemented. |
| FR14 | Save all practice sessions (questions, answers, feedback, scores) to user history | **Partial** | Resume records (and extracted entities) are saved in DB; no "practice session" or Q&A history yet. |
| FR15 | Progress analytics dashboard: session history, average scores, performance by category | **Pending** | Not implemented. |
| FR16 | Visual charts (line/bar) for performance trends | **Pending** | Not implemented. |
| FR17 | Export progress reports in PDF | **Pending** | Not implemented. |
| FR18 | Update profile, multiple resume versions, session preferences | **Pending** | No profile/preferences; multiple resumes via list + upload (no explicit "versions" per user). |
| FR19 | Pause and resume practice sessions with auto-save | **Pending** | Not implemented. |
| FR20 | Hints or guidance when user requests assistance during practice | **Pending** | Not implemented. |
| FR21 | Adapt question difficulty based on experience level (from resume) | **Pending** | Not implemented. |
| FR22 | Keyword search within session history | **Pending** | Not implemented. |
| FR23 | Email notifications (verification, session summary, weekly progress) | **Pending** | Not implemented. |
| FR24 | Fallback: LLM fail → question bank; semantic evaluator fail → rule-based | **Pending** | Not implemented. |
| FR25 | Log all errors and system failures for administrator review | **Partial** | Standard FastAPI/uvicorn logging; no dedicated admin error log. |

---

## Non-functional requirements (NFR)

| ID | Requirement (one-line) | Status | Where / notes |
|----|-------------------------|--------|----------------|
| NFR01 | Passwords bcrypt (≥10 rounds); resume/personal data AES-256 at rest (e.g. S3) | **Pending** | No auth; no S3; resume stored in DB. |
| NFR02 | Resume parsing ≤10 s (95%); job analysis ≤5 s | **Partial** | Depends on model load and hardware; not formally measured. |
| NFR03 | Question generation ≤15 s; fallback ≤3 s | **Pending** | No QG yet. |
| NFR04 | Semantic feedback ≤5 s (95%) | **Pending** | No semantic feedback yet. |
| NFR05 | Support 500 concurrent users; auto-scale | **Pending** | No load testing or auto-scaling. |
| NFR06 | PostgreSQL 50k+ sessions; query &lt;2 s | **Partial** | PostgreSQL in use; scale not validated. |
| NFR07 | 99.5% uptime (business hours) | **Pending** | Not deployed/monitored. |
| NFR08 | Zero data loss; auto-save every 2 min and on answer submit | **Partial** | Resume create/update persisted; no practice-session auto-save. |
| NFR09 | Mobile-responsive (320px–2560px); keyboard navigation | **Partial** | Next.js + Tailwind; responsiveness and a11y not formally verified. |
| NFR10 | Homepage/dashboard load ≤3 s; analytics ≤5 s | **Pending** | Not measured. |
| NFR11 | WCAG 2.1 Level AA | **Pending** | Not assessed. |
| NFR12 | Latest Chrome, Firefox, Safari, Edge; iOS Safari, Android Chrome | **Partial** | Standard web stack; not formally tested. |
| NFR13 | Modular architecture; OpenAPI/Swagger API docs | **Implemented** | PROJECT: FastAPI with routers; `/api/v1/docs`; clear split frontend/backend/ML. |
| NFR14 | GDPR: consent, right to deletion, data portability, privacy policy | **Pending** | Not implemented. |
| NFR15 | Data anonymization for training; resumes separate from analytics | **Pending** | Not implemented. |
| NFR16 | Session expire 30 min inactivity; JWT over HTTPS | **Pending** | No auth/sessions. |
| NFR17 | Daily backups, 30-day retention; restore within 4 h | **Pending** | Not implemented. |
| NFR18 | Logging (actions, API errors, metrics); retention 90 days; monitoring | **Partial** | Application logs only; no structured audit or monitoring. |

---

## Summary for IPD slides

**Implemented (done in prototype):**

- **FR03** – Resume upload (PDF + paste).
- **FR04** – Resume NER extraction (BERT-BiLSTM-CRF + rules).
- **FR05** – Review and edit extracted entities.
- **NFR13** – Modular architecture and OpenAPI docs.

**Partial (backend or part of flow only):**

- **FR06–FR07** – Job description input and analysis (API only; no frontend).
- **FR14** – Persist resume/entities (no practice-session history yet).
- **FR25** – Basic application logging.
- **NFR02, NFR06, NFR08, NFR09, NFR12, NFR18** – Partially addressed by current stack; not fully validated.

**Pending (for post-IPD / April):**

- **FR01–FR02** – Registration and auth.
- **FR08–FR13** – Question generation, chat interface, semantic feedback, follow-ups.
- **FR15–FR24** – Analytics, export, profile, fallbacks, etc.
- **NFR01, NFR03–NFR05, NFR07, NFR10–NFR12, NFR14–NFR17** – Security, performance, privacy, backup, accessibility.

---

## Where things live (quick reference)

| What | Location |
|------|----------|
| **Frontend (Next.js)** | PROJECT `crackint-frontend/` — `app/cv-upload/`, `components/cv-upload/`, `services/resume-uploader.service.ts` |
| **Backend (FastAPI)** | PROJECT `crackint-backend/` — `app/api/resume/`, `app/api/job/`, `app/ml/resume_ner.py`, `app/ml/job_poster_ner.py`, `app/services/text_extraction.py` |
| **Resume NER model** | Hugging Face `dinalUdagedara/resume-entity-extractor` or PROJECT `RESUME_NER_LOAD_DIR`; training in repo `resume_ner_pipeline/`, `fyp/BERT_BiLSTM_CRF_Resume_NER_FYP.ipynb` |
| **Job poster NER model** | PROJECT `JOB_POSTER_NER_LOAD_DIR`; training in repo `job_poster_ner_pipeline/`, `fyp/job-poster-ner/` |
| **IPD docs** | **docs/ipd/** — requirements-analysis, requirements-implemented-vs-pending, architecture-and-schedule, etc. |
| **PPRS summary** | **docs/project/proposal-summary.md** |

---

*Use this table in your IPD presentation under "Formal requirements specification" and to describe "Progress since PPRS".*
