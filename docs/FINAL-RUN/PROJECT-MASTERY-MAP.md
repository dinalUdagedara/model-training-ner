# CrackInt Project Mastery Map (Frontend + Backend + Models)

This file is your end-to-end technical revision map for viva.

---

## 1) High-Level System Understanding

CrackInt is a full-stack interview-preparation platform with:

- **Frontend:** Next.js (App Router), React, React Query, Axios, NextAuth, ShadCN/Radix UI
- **Backend:** FastAPI, SQLModel/SQLAlchemy, PostgreSQL, JWT auth, optional Socket.IO
- **ML:** Resume NER + Job Poster NER inference pipelines (`Word2Vec + BiLSTM + CRF` or `BERT + BiLSTM + CRF` depending on saved config)
- **AI services:** LLM-based session Q&A, CV scoring, resume-job fit, cover letter generation (feature-flag controlled)

---

## 2) Backend Architecture Map

## Entry and app composition
- `app/main.py`
  - App factory `get_app()`
  - Loads NER models at startup (`load_resume_ner()`, `load_job_poster_ner()`)
  - Adds global CORS
  - Registers API router under `/api/v1`
  - Registers global validation/general exception handlers
  - Wraps FastAPI in Socket.IO app

- `app/api/router.py`
  - Includes routers: `auth`, `admin`, `health`, `resumes`, `jobs`, `job-postings`, `sessions`, `match`, `users`, `stt`, `cover-letter`, `uploads`

## Configuration and DB
- `app/config.py`
  - Central env-driven settings: DB, model paths, agent flags, JWT, AWS/S3
- `app/database.py`
  - Async engine/session creation, TLS requirement outside localhost
- `app/api/deps.py`
  - `get_db`, `get_current_user`, `get_current_admin_user`
- `app/auth/jwt.py`
  - token create/decode for Bearer auth

## Domain models (`app/models.py`)
- `User`, `Resume`, `JobPosting`, `PrepSession`, `Message`, `ResumeJobAnalysis`, `CoverLetter`
- JSONB-heavy design for flexible entities/meta fields
- UUID primary keys + timestamps mixins

---

## 3) Core Backend Flows (Must Explain in Viva)

## A) Resume extraction flow
1. Frontend uploads file/text -> `POST /resumes/extract`
2. `app/api/resume/route.py` validates type/size and ownership context
3. `app/api/resume/service.py`:
   - file path: `extract_text_from_file(...)`
   - text path: direct pass
4. NER call -> `parse_resume_hybrid(...)` in `app/ml/resume_ner.py`
5. Optional LLM entity validation if `validate=true` and flag enabled
6. Persist `Resume` row (entities + raw_text + optional S3 source URL)

## B) Job extraction flow
1. Frontend -> `POST /jobs/extract`
2. Validation/type checks in `app/api/job/route.py`
3. `app/api/job/service.py` extracts text then runs NER
4. NER uses `app/ml/job_poster_ner.py`
5. Optional LLM entity correction via job entity agent

## C) Session chat flow
1. Frontend sends message -> `POST /sessions/{id}/chat`
2. `app/api/session/route.py` loads session context (resume, job, previous messages)
3. Stores user message
4. Branches:
   - tutor mode -> `generate_tutor_chat_reply(...)`
   - interview mode:
     - classify greeting/skip/off-topic
     - evaluate answer (`evaluate_answer(...)`)
     - store feedback + optional session title + periodic summary
     - generate next question (`generate_next_question(...)`)
5. Returns `new_messages[]` to append in UI

## D) Skill gap + readiness flow
1. `POST /match/skill-gap`
2. Rule-based gap in `app/services/skill_gap_service.py`:
   - missing skills
   - weak experience/education
   - severity + alerts
3. Optional LLM fit enrichment + location suitability
4. Persists result in `ResumeJobAnalysis`
5. `GET /users/me/readiness` combines:
   - CV score
   - session averages
   - gap penalty
   via `compute_combined_readiness(...)`

## E) CV scoring flow
1. `POST /resumes/score` (file) or `GET /resumes/{id}/score` (text)
2. `app/services/cv_scoring.py`
   - docx -> text path
   - pdf/image -> vision path
3. `app/agents/cv_scoring_agent.py` calls LLM, returns score + breakdown + suggestions

---

## 4) ML Runtime Understanding (Deployed Models)

## Resume NER (`app/ml/resume_ner.py`)
- Supports two runtime modes:
  - **Word2Vec + BiLSTM + CRF** (if config has `word2id` and w2v checkpoint)
  - **BERT + BiLSTM + CRF**
- Hybrid extraction:
  - Model entities + rule-based NAME heuristic + regex EMAIL extraction
- Handles malformed BIO sequences (leading I-tags)
- Fallback stub extraction when model not loaded

## Job Poster NER (`app/ml/job_poster_ner.py`)
- Same dual architecture support (Word2Vec or BERT stack)
- Hybrid extraction:
  - model output + regex salary extraction
- Returns normalized/deduped entities; empty when model unavailable

## Current saved model config evidence
- Resume config includes:
  - `embed_dim=256`, `num_labels=13`, `max_len=768`
- Job config includes:
  - `embed_dim=256`, `num_labels=17`, `max_len=512`

---

## 5) Training-Notebook Understanding (Viva Talking Points)

From your FYP training materials:

- Four notebooks exist:
  - `BERT_BiLSTM_CRF_Resume_NER_FYP.ipynb`
  - `BiLSTM_CRF_Resume_NER_Path2_FYP.ipynb`
  - `job-poster-ner/BERT_BiLSTM_CRF_Job_Poster_NER_FYP.ipynb`
  - `job-poster-ner/BiLSTM_CRF_Job_Poster_NER_Path2_FYP.ipynb`
- Final selected path in your FYP docs: **BiLSTM-CRF (Path 2)**
- Standard pipeline:
  - tokenization + span-to-BIO alignment
  - train/val/test split (80/10/10, seeded)
  - weighted sampling for rare tags
  - CRF sequence decoding
  - seqeval entity-level metrics (precision/recall/F1)
  - early stopping + best checkpoint restore

---

## 6) Frontend Architecture Map

## Auth and API layer
- `app/api/auth/[...nextauth]/route.ts`
  - Credentials + Google OAuth
  - Exchanges Google ID token with backend `/auth/google`
  - Stores backend JWT in NextAuth session
- `lib/axios.ts` + `lib/hooks/useAxiosAuth.ts`
  - shared authenticated axios instance
  - auto injects `Authorization: Bearer`
  - handles 401 -> signout redirect
- `components/providers/Auth401Handler.tsx`
  - global 401 handler registration

## Service layer pattern
- `services/*.service.ts` files call backend endpoints and centralize error handling
- Uses React Query for caching/mutations in UI components

## Session UI flow
- `components/sessions/SessionChatView.tsx`
  - fetches session + messages
  - optimistic pending message
  - posts chat turns via `postChatTurn(...)`
  - mode switching (`TUTOR_CHAT`, `TARGETED`, `QUICK_PRACTICE`)
  - cover letter generation action
- Sidebar (`components/app-sidebar.tsx`) lists recent sessions and supports rename/delete

---

## 7) What You Should Be Able To Explain Without Demo

- How login turns into backend JWT and where it is attached on requests
- Exact request flow for:
  - CV upload and extraction
  - Job upload and extraction
  - Session chat turn and message persistence
  - Skill-gap analysis and readiness aggregation
- Difference between:
  - rule-based extraction
  - model extraction
  - optional LLM post-processing
- Feature-flag behavior (what happens when agents/models are disabled)

---

## 8) High-Risk Viva Questions (Project-Specific)

- Why did you support both BERT and Word2Vec pipelines at runtime?
- Under what conditions does `/jobs/extract` return empty entities?
- How do you prevent unauthorized access to user-specific resumes/sessions?
- How is readiness score computed mathematically?
- What happens when OpenAI services are unavailable mid-session?
- How do you justify the max upload/type validation strategy?
- Which parts are deterministic vs probabilistic in your pipeline?

---

## 9) Honest Status of Understanding

You now have a **deep operational understanding** of:

- backend architecture and route/service layering,
- frontend auth/data flow,
- deployed model runtime logic,
- training-pipeline methodology from notebooks and guides.

Absolute “100% every line” mastery still depends on one more pass of:

- all remaining non-core UI components,
- every auxiliary service/module not used in your main demo path.

For viva readiness, this map covers the high-probability technical defense surface.

