# CrackInt — Implemented vs pending (final thesis draft)

**Purpose:** Align **PPRS functional/non-functional requirements** with what the **current backend** exposes. Use this in **Chapter 4 (SRS)** and **Chapter 9 (evaluation)**.

**Sources of truth**

| Type | Location |
|------|----------|
| API routes & behaviour | `FYP/PROJECT/crackint-backend/app/api/router.py` + **[API_OVERVIEW.md](../../../PROJECT/crackint-backend/API_OVERVIEW.md)** (from repo root: `../PROJECT/crackint-backend/API_OVERVIEW.md`) |
| Feature flags / env | `crackint-backend/app/config.py` (e.g. `SESSION_QA_AGENT_ENABLED`, `CV_SCORING_ENABLED`, `OPENAI_API_KEY`) |
| Original FR/NFR IDs | [project/proposal-summary.md](../project/proposal-summary.md) §7–8 (PPRS Table 11–12) |

**Note:** `API_OVERVIEW.md` does not list every route in one table (e.g. **auth**, **job-postings**, **cover-letter** are in code). This document merges **router + README + route files**. Update if you add endpoints.

---

## 1. API surface (quick reference)

| Prefix | Router module | Main capabilities |
|--------|----------------|-------------------|
| `/api/v1/auth` | `app/api/auth/route.py` | Register, login, Google OAuth, `GET /me` (JWT) |
| `/api/v1/health` | `health` | Health check |
| `/api/v1/resumes` | `resume` | Extract, CRUD, list, **score** (LLM, gated) |
| `/api/v1/jobs` | `job` | Job text/PDF **extract** |
| `/api/v1/job-postings` | `job_posting` | Job posting **CRUD**, reorder, deadlines (auth) |
| `/api/v1/sessions` | `session` | Prep sessions, messages, **next-question**, **evaluate-answer** |
| `/api/v1/match` | `match` | **Skill-gap** (resume vs job posting) |
| `/api/v1/users` | `users` | **Readiness**, summary, trend, **home-summary** |
| `/api/v1/stt` | `stt` | Socket.IO speech-to-text hooks |
| `/api/v1/cover-letter` | `cover_letter` | Generate / read / update / delete cover letters |
| `/api/v1/uploads` | `uploads` | Image upload to **S3** (when configured) |

Interactive: **`/api/v1/docs`** (Swagger), **`/api/v1/redoc`**.

---

## 2. Functional requirements (FR) — PPRS vs implementation

| ID | PPRS requirement (summary) | Status | Evidence / notes |
|----|----------------------------|--------|-------------------|
| **FR01** | Register (email, profile) | **Implemented** | `POST /api/v1/auth/register` |
| **FR02** | Secure auth, encrypted passwords | **Implemented** | `POST /api/v1/auth/login`, JWT (`app/auth/jwt.py`), `hash_password` / bcrypt-style hashing; `POST /auth/google` if `GOOGLE_CLIENT_ID` set |
| **FR03** | Résumé upload PDF/DOCX (max size) | **Partial** | `POST /resumes/extract` — PDF + text; max `MAX_UPLOAD_SIZE_MB` (default 10 in config). Confirm DOCX in `text_extraction` / route if thesis claims it |
| **FR04** | NER: name, email, skills, education, experience | **Implemented** | `parse_resume_hybrid` + `RESUME_NER_LOAD_DIR` / HF; entities in API responses |
| **FR05** | Review / edit extracted data | **Implemented** | `PATCH /resumes/{id}` |
| **FR06** | Job description input (paste / title) | **Implemented** | `POST /jobs/extract` (text or PDF); job postings stored via `/job-postings` |
| **FR07** | Analyse job (skills, qualifications, etc.) | **Implemented** | Job NER + entities; job poster model or fallback per `JOB_POSTER_NER_LOAD_DIR` |
| **FR08** | 10–15 personalized questions (LLM) | **Partial** | `POST /sessions/{id}/next-question` — requires **`SESSION_QA_AGENT_ENABLED=true`** + **`OPENAI_API_KEY`**; count/limit is agent behaviour (document in Ch 7) |
| **FR09** | Chat-based practice UI | **Implemented** | Session + message model + frontend `(dashboard)/sessions`; STT optional via Socket.IO |
| **FR10** | Text answers | **Implemented** | `POST .../messages` + evaluate flow |
| **FR11** | Semantic evaluation of answers | **Partial** | `POST .../evaluate-answer` when agent enabled; exact rubric = agent implementation |
| **FR12** | Feedback: score 0–100, strengths, improvements | **Partial** | API returns `feedback`, `score`, `dimension_tags`; wording depends on LLM |
| **FR13** | Conversational follow-ups | **Partial / TBC** | Confirm in `session_qa_agent` whether follow-ups are generated |
| **FR14** | Save sessions (questions, answers, feedback, scores) | **Implemented** | PostgreSQL sessions + messages; readiness fields as per models |
| **FR15** | Progress analytics dashboard | **Partial** | `GET /users/me/readiness/summary`, `/readiness/trend`, `/home-summary` — dashboard data; “charts” = frontend |
| **FR16** | Visual charts | **Partial** | Backend supplies trend/summary; charts are **frontend** (e.g. Recharts) — state explicitly in thesis |
| **FR17** | Export progress PDF | **Pending** | No dedicated export endpoint in router overview |
| **FR18** | Profile, multiple résumés, preferences | **Partial** | `GET /auth/me`; multiple resumes via list + upload; full “preferences” UI TBC |
| **FR19** | Pause / resume session, auto-save | **Partial** | Messages persisted; timed auto-save every 2 min may not match — verify product behaviour |
| **FR20** | Hints on request | **Pending / TBC** | Check session agent for hint messages |
| **FR21** | Adaptive difficulty | **Partial** | `next-question` + `prefer_difficulty`; session difficulty curve in agent |
| **FR22** | Search session history | **Pending** | List endpoints; full-text search not listed |
| **FR23** | Email notifications | **Pending** | Not in API router |
| **FR24** | Fallbacks (LLM fail → bank; evaluator fail → rules) | **Partial** | NER fallback resume→job; evaluation fallback — confirm in agent code |
| **FR25** | Admin error logging | **Partial** | App logging; dedicated admin error dashboard not listed |

### Extra features (not always in original PPRS table)

| Feature | Status | API / module |
|---------|--------|----------------|
| CV strength scoring (0–100) | **Partial** (LLM) | `POST/GET .../resumes/score` — needs **`CV_SCORING_ENABLED`** + API key |
| Skill-gap + alerts | **Implemented** | `POST /match/skill-gap` |
| Combined readiness | **Implemented** | `GET /users/me/readiness` |
| Cover letter generation | **Partial** (LLM) | `/cover-letter/*` — **`COVER_LETTER_AGENT_ENABLED`** (default true in config; still needs API key for generation) |
| Image upload (S3) | **Partial** | `POST /uploads/image` — needs AWS + bucket |
| Speech input | **Partial** | STT service + Socket.IO — document if used in final demo |

---

## 3. Non-functional requirements (NFR) — honest status

| ID | PPRS theme | Status | Notes for thesis |
|----|------------|--------|-------------------|
| **NFR01** | bcrypt; AES-256 / S3 for data | **Partial** | Password hashing implemented; résumé storage in DB; S3 used for **optional** image uploads when configured — state scope clearly |
| **NFR02** | Latency targets (parse, job, QG, feedback) | **Partial** | Measure and report **observed** times in Ch 8 or admit not load-tested |
| **NFR03–NFR04** | QG / feedback SLA | **Partial** | Depends on OpenAI latency; document typical behaviour |
| **NFR05–NFR07** | Scale, uptime | **Pending** | Dev deployment; no evidence of 500 users / 99.5% unless you test |
| **NFR06** | DB scale | **Partial** | PostgreSQL in use; 50k+ sessions not validated |
| **NFR08** | No data loss; auto-save | **Partial** | Server-side persist; browser auto-save policy — verify |
| **NFR09** | Responsive UI | **Partial** | Next.js + Tailwind — state “designed responsive”; optional formal checks |
| **NFR10** | Page load times | **Partial** | Measure key pages or report informal |
| **NFR11** | WCAG AA | **Pending / partial** | Radix/shadcn helps; full audit unlikely |
| **NFR12** | Browser compatibility | **Partial** | Standard stack; spot-test for thesis |
| **NFR13** | Modular + OpenAPI | **Implemented** | FastAPI `/docs`, modular routers |
| **NFR14–NFR16** | GDPR, anonymization, JWT session | **Partial** | JWT implemented; full GDPR flows (consent UI, erasure) — verify in app |
| **NFR17** | Backups | **Pending** | Unless you document DB backup strategy |

---

## 4. Environment: what must be enabled for “full demo”

| Goal | Typical env |
|------|-------------|
| Auth + CRUD | DB + `JWT_SECRET` |
| NER | `RESUME_NER_LOAD_DIR` (and optionally `JOB_POSTER_NER_LOAD_DIR`) |
| LLM questions + evaluation | `OPENAI_API_KEY`, `SESSION_QA_AGENT_ENABLED=true` |
| CV scoring | `OPENAI_API_KEY`, `CV_SCORING_ENABLED=true` |
| Google login | `GOOGLE_CLIENT_ID` |
| S3 image upload | `S3_UPLOADS_BUCKET`, AWS keys |
| Resume/job AI “fit” extras | `RESUME_JOB_FIT_LLM_ENABLED` (see `config.py`) |

Copy exact flags from **`app/config.py`** when writing Implementation chapter.

---

## 5. What to do before submitting the thesis

1. Walk through **Swagger** and your **frontend** once; tick boxes in §2–§3 that you will **claim**.  
2. For anything **Partial**, write one sentence of **limitation** in Ch 8 / Ch 10.  
3. Update **`THESIS-FACTS-SHEET.md`** with the same numbers and env assumptions.

---

*Generated as a first draft from `router.py`, `API_OVERVIEW.md`, `config.py`, and PPRS summary. Revise after any API change.*
