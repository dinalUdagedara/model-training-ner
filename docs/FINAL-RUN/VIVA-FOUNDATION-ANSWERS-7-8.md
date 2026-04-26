# Viva Foundation Answers (7 & 8)

This file gives viva-ready answers for:

7. Implementation  
8. Testing

Written in simple spoken English and based on your report content.

---

## 7) Implementation (Detailed Answer)

Chapter 7 explains how my design became a working full-stack system.

I implemented CrackInt using:

- **Frontend:** Next.js + TypeScript
- **Backend:** FastAPI + Python
- **Database:** PostgreSQL
- **ML:** Word2Vec + BiLSTM + CRF for resume and job-poster NER
- **AI services:** LLM-backed question generation/evaluation and related analysis flows

### System-level implementation
The implemented architecture follows:

- browser/client layer,
- Next.js presentation layer,
- FastAPI logic layer,
- PostgreSQL persistence layer.

ML inference and LLM calls run through backend services, not directly from frontend.

### Resume NER implementation
- Final deployed approach is Word2Vec + BiLSTM + CRF.
- Training data was merged and normalized into a BIO schema.
- Frozen run data size: **4,738 resumes** with split **3790/473/475**.
- Backend loads model artifacts using configuration (`RESUME_NER_LOAD_DIR`).
- Hybrid extraction includes rule support for high-precision fields like NAME/EMAIL.

### Job-poster NER implementation
- Same engineering pattern with job-specific labels.
- Frozen run data size: **6,327 job postings** with split **5061/632/634**.
- Backend loads artifacts from `JOB_POSTER_NER_LOAD_DIR`.
- Supports hybrid behavior (model + rules for robust fields like salary).

### API and backend implementation
Backend is modular under `app/` with:

- routers (`/api/v1` domains),
- authentication (`JWT`, password hashing),
- ML services,
- agent services,
- persistence models and migrations.

Implemented core endpoints include:

- resume extract/list/update/score,
- job extract,
- job postings CRUD,
- sessions and messages,
- skill-gap analysis,
- readiness summary/trend endpoints.

### Frontend implementation
Frontend uses App Router with dashboard routes for:

- CV upload and editing,
- job upload/posting flows,
- sessions/chat,
- match and readiness views,
- cover letter and admin pages.

Integration uses Bearer tokens, API service layer, and user-facing error handling (toasts/inline feedback).

### Challenges and solutions (from report)
- large model artifacts -> configurable local/cloud loading paths
- noisy PDFs/scans -> text extraction + OCR fallback + paste-text fallback
- long document handling -> controlled max-length truncation
- schema evolution -> Alembic migrations
- cross-origin and environment handling -> CORS/config-driven behavior

So chapter 7 shows not only code writing, but complete system integration from data ingestion to user-facing features.

---

## 8) Testing (Detailed Answer)

Chapter 8 explains how I validated the system after implementation.

I tested the project in three areas:

1. **Model testing** (NER quality)
2. **Functional testing** (features vs FR requirements)
3. **Non-functional testing** (selected NFR quality checks)

### 8.1 Model testing
I evaluated NER models using entity-level precision, recall, and F1 (seqeval), with standard 80/10/10 split and fixed random seed.

#### Resume NER test results
- micro-F1: **0.83**
- strong entities: NAME, EMAIL
- weaker entities: OCCUPATION/EXPERIENCE (more variation/ambiguity)

#### Job-poster NER test results
- micro-F1: **~0.85**
- stronger entities: JOB_TITLE, COMPANY, LOCATION, etc.
- weaker entity: SKILLS_REQUIRED (long and variable multi-token phrases)

I also discussed benchmarking limits honestly because dataset/schema differences prevent strict one-to-one external leaderboard comparison.

### 8.2 Functional testing
Functional tests were mapped to SRS FRs and executed on both frontend + backend flows.

Representative verified flows include:

- register/login/auth routes,
- protected route behavior (401 vs authorized access),
- resume extraction/update,
- job extraction,
- session create/question/evaluate flow,
- skill-gap analysis,
- readiness summary routes.

### 8.3 Non-functional testing
I checked selected NFR themes and reported status honestly:

- security checks (JWT auth behavior, hashed passwords),
- maintainability evidence (OpenAPI + modular API),
- usability checks (responsive behavior, accessible components baseline),
- performance checks (informal single-user timings),
- reliability behavior when AI/model dependencies are unavailable.

### 8.4 Testing limitations (important in viva)
I clearly stated limits:

- no large-scale user trial,
- no formal penetration test,
- no concurrent load/scalability validation,
- LLM behavior can vary by provider/runtime state,
- OCR/noisy document behavior can reduce live extraction quality.

So chapter 8 is strong because it gives real evidence and also clearly states what was not fully validated.

---

## Quick 30-Second Backup Versions

## 7) Implementation (short)
I implemented CrackInt as a full-stack system with Next.js frontend, FastAPI backend, PostgreSQL storage, and integrated NER + LLM-backed services. Resume and job NER were trained and deployed with Word2Vec + BiLSTM + CRF pipelines, and I built modular APIs for extraction, sessions, analysis, and readiness. The chapter also documents practical integration challenges and how they were handled.

## 8) Testing (short)
I validated the system using model, functional, and non-functional testing. Model testing reported around 0.83 and 0.85 micro-F1 for resume and job-poster NER. Functional tests covered core user/API flows, and non-functional checks covered security/usability/maintainability basics. I also documented key testing limitations clearly.

---

## Challenge Questions (Implementation + Testing Defense)

## Q1) "What exactly did you implement yourself?"

**Answer:**  
I implemented the integrated application flow: backend APIs, session logic, persistence flow, model integration/runtime loading, and frontend integration paths.  
I also developed project-specific orchestration for extraction, session workflows, and readiness-related outputs.

## Q2) "Is your ML part only inference?"

**Answer:**  
No, my report documents full lifecycle: data preparation, training setup, hyperparameters, checkpoints, deployment loading, and inference behavior.

## Q3) "How do you prove your system is not just a notebook demo?"

**Answer:**  
Because the models are integrated into authenticated backend APIs and full frontend workflows with persistence, not isolated notebook execution.

## Q4) "Why should we trust your test results?"

**Answer:**  
I used standard NER metrics with held-out test splits, functional traceability to SRS requirements, and explicit non-functional status reporting.  
I also declared limitations clearly instead of overclaiming.

## Q5) "Which feature is most dependent on external AI services?"

**Answer:**  
Session question/feedback intelligence and some advanced analysis flows are most dependent on external LLM availability.

## Q6) "What happens when AI service is down?"

**Answer:**  
AI-heavy outputs may degrade, but core platform behavior and persisted data flows continue. The design supports controlled degradation rather than full system collapse.

## Q7) "Why is SKILLS_REQUIRED weaker than other entities?"

**Answer:**  
Because skill spans are often long, varied, and multi-token with high phrasing variability, making them harder than structured fields like emails or company names.

## Q8) "Did you do full production-grade testing?"

**Answer:**  
No, and I stated that clearly.  
I did strong academic/prototype validation, but full production load testing and formal security audit are future work.

## Q9) "How did you connect tests to requirements?"

**Answer:**  
Functional tests were derived from SRS FRs and reported with pass/fail behavior and traceability, not random ad-hoc test cases.

## Q10) "What is your strongest testing practice?"

**Answer:**  
Honest evidence reporting: measurable model metrics, requirement-linked functional tests, and transparent limitations section.

---

## Keyword Meanings (Simple)

- **Inference:** using trained model to predict on new input.
- **Checkpoint:** saved trained model weights.
- **Micro-F1:** overall combined F1 score across entities.
- **Functional test:** checks if required feature works correctly.
- **Non-functional test:** checks quality aspects like security/performance/usability.
- **Traceability:** linking tests/results to requirement IDs.
- **Fallback:** backup behavior when primary service fails.
- **Controlled degradation:** some advanced features reduce, but whole system does not crash.

---

## One-Line Closing for Chapters 7 & 8

Chapter 7 proves I built and integrated the system end-to-end, and chapter 8 proves I validated it with measurable evidence while honestly reporting scope limits.

