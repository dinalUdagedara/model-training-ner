# CrackInt – Project Proposal Summary (PPRS)

**Document source:** 20221214_w1998730.pdf – Project Proposal and Requirements Specification  
**Student:** Udagedara Thiyunu Dinal Bandara | **UoW/IIT ID:** W1998730  
**Supervisor:** Mr. Pubudu Arachchige  
**Course:** BEng Software Engineering, University of Westminster (IIT)  
**Submission:** November 2025

---

## 1. Project overview

**CrackInt** is an **AI-driven, web-based interview preparation platform** that provides:

- **Résumé-aware question generation** (from candidate CV + job description)
- **Interactive, chat-based practice** with real-time **semantic feedback**
- **Longitudinal progress tracking** and analytics

**Tech stack:** Next.js 14, Tailwind CSS, shadcn UI (frontend); FastAPI (backend); NER/resume parsing; LLM (GPT-4/Gemini) for question generation and semantic evaluation; PostgreSQL, AWS S3.

---

## 2. Problem statement

Current interview-prep tools are **fragmented** and lack:

1. **Resume–job awareness** – Generic question banks; no alignment with candidate background or target role.
2. **Semantic-level feedback** – Focus on tone/pace/grammar, not content depth, relevance, or structure.
3. **Integrated progress tracking** – No unified platform for session history and improvement over time.
4. **Scalable, integrated UX** – Real-time, mobile-friendly, low-latency experience often missing.

**Summary:** There is no holistic, AI-powered platform that combines **résumé parsing**, **role-specific question generation**, and **semantic feedback** in one candidate-centric system.

---

## 3. Research gap

- **Resume–job awareness:** No platform dynamically generates questions from both candidate résumé and job description.
- **Semantic feedback:** Tools like Big Interview give superficial metrics; content quality and reasoning are not evaluated.
- **Adaptive learning:** Little support for session history and difficulty adaptation from prior performance.
- **Integration:** Few systems unite parsing, question generation, and semantic evaluation in one secure, scalable product.

**CrackInt** addresses this by: NER-based résumé/job parsing, LLM-based question generation, semantic feedback engine, and persistent analytics.

---

## 4. Research aim and objectives (summary)

**Aim:** Design, implement, and evaluate **CrackInt** as an integrated platform that unifies:

- Résumé parsing and job-description analysis  
- Adaptive, role-specific question generation  
- Semantic, content-aware feedback  
- Longitudinal progress tracking  

**Key objectives (from Table 1):** Literature review (R02–R04); stakeholder & requirements elicitation (R05–R07); system design & DB schema (R08–R09); dataset, OCR, NER, LLM QG, semantic feedback, integration (R10–R15); evaluation (R16–R19); documentation and thesis (R20–R22).

---

## 5. Stakeholders (for IPD Onion diagram)

| Layer | Stakeholders | Roles / interests |
|-------|--------------|-------------------|
| **1 – Core** | Job seekers, students, early-career professionals | Personalized questions, actionable feedback, progress tracking, affordable access |
| **2 – Operational** | Career services, technical support, development team | Effectiveness, reliability, integration, maintenance |
| **3 – Strategic** | Academic institutions, corporate partners, research community | Outcomes, candidate readiness, accreditation, recruitment efficiency |
| **4 – External** | Regulatory (GDPR/CCPA), AI ethics bodies, competitors, tech providers | Compliance, transparency, bias mitigation, ethical data use |

*Table 6 and Section 4.3.1–4.3.2 in PPRS; detailed viewpoints in Appendix C.*

---

## 6. Use cases (high level)

| ID | Use case | Actor | Description |
|----|----------|--------|-------------|
| UC-01 | Register and create profile | Job seeker | Account creation with email verification |
| UC-02 | Upload and parse résumé | Job seeker | Extract skills, education, experience (NER) |
| UC-03 | Generate role-specific questions | Job seeker | Personalized questions from résumé + job description |
| UC-04 | Practice with semantic feedback | Job seeker | Chat-based practice with AI evaluation (core use case) |
| UC-05 | View progress analytics | Job seeker | Session history, trends, improvement over time |
| UC-06 | Manage account and settings | Job seeker | Profile, résumés, preferences |

---

## 7. Functional requirements (FR) – from PPRS Table 11

**Must have (February prototype focus):**

- **FR01–FR02:** Registration, secure auth, encrypted passwords  
- **FR03–FR05:** Résumé upload (PDF/DOCX, max 5MB), NER parsing (name, email, skills, education, experience), review/edit extracted data  
- **FR06–FR08:** Job description input; analyze job; generate 10–15 personalized questions (LLM)  
- **FR09–FR12:** Chat interface; text responses; semantic evaluation; real-time feedback (score 0–100, strengths, improvements, suggestions)  
- **FR14:** Save all sessions (questions, answers, feedback, scores)  

**Should have (e.g. April / post-prototype):**

- FR13 (conversational follow-ups), FR15–FR16 (analytics dashboard, charts), FR18 (profile, multiple résumés), FR19 (pause/resume), FR24 (fallbacks), FR25 (error logging)  

**Could have:** FR17 (export PDF), FR20 (hints), FR21 (adaptive difficulty), FR22 (search history), FR23 (email notifications).

---

## 8. Non-functional requirements (NFR) – from PPRS Table 12

**Must have:**

- **Security:** bcrypt (≥10 rounds), AES-256 at rest for résumés/data (e.g. S3)  
- **Performance:** Résumé parsing ≤10 s (95%); job analysis ≤5 s; QG ≤15 s; semantic feedback ≤5 s (95%)  
- **Reliability:** Zero data loss; auto-save every 2 min and on answer submit  
- **Usability:** Mobile-responsive (320px–2560px), keyboard navigation  
- **Compatibility:** Chrome, Firefox, Safari, Edge; iOS Safari, Android Chrome  
- **Privacy:** GDPR (consent, deletion, portability, policy); anonymization for training; session expiry 30 min; JWT over HTTPS  

**Should have:** Scalability (500 concurrent users, DB 50k+ sessions, <2 s query); 99.5% uptime; page load (e.g. 3 s homepage); maintainability (modular, OpenAPI); backup/recovery; logging/monitoring.  

**Could have:** WCAG 2.1 Level AA.

---

## 9. Scope (in / out)

**In scope:**  
PDF/DOCX résumé parsing (NER); job description or title input; technical, system-design, behavioral question generation (LLM); real-time semantic feedback; session history and progress analytics; privacy and secure storage; responsive web UI (Next.js, Tailwind, shadcn).

**Out of scope:**  
Multi-language (English only); audio/video mock interviews or facial analysis; guaranteed ATS/job-portal integration; legal/career counselling beyond AI feedback; niche domain models (e.g. legal, medical); guarantee of zero AI errors/hallucinations.

---

## 10. Methodology (for IPD "System Design" slide)

- **Research:** Saunders Research Onion – Pragmatism, abductive, mixed methods, DSR + experiment + survey; cross-sectional.  
- **Development:** Agile (Scrum), 4 sprints.  
- **Analysis/design:** OOAD; UML (use case, class, sequence).  
- **Stack:** Next.js + FastAPI; OOP (TypeScript, Python).

---

## 11. Gantt / time schedule (from PPRS Table 4)

| Deliverable | Date |
|-------------|------|
| Project proposal (initial/final drafts) | Sep–Oct 2025 |
| Literature review | 10 Nov 2025 |
| SRS / PPRS final | 13 Nov 2025 |
| Proof of concept | 13 Nov 2025 |
| Design document | 20 Dec 2025 |
| **Prototype** | **2 Feb 2026** |
| **Interim project demo (IPD)** | **2 Feb 2026** |
| Implementation | 15 Mar 2026 |
| Testing | 20 Mar 2026 |
| Evaluation | 25 Mar 2026 |
| Thesis submission / MVP | 1 Apr 2026 |

*For IPD: use updated Gantt in [../ipd/architecture-and-schedule.md](../ipd/architecture-and-schedule.md) and explain any deviations from this baseline.*

---

## 12. Risks (from PPRS Table 5)

- Overfitting; poor model accuracy; high FP/FN in feedback; insufficient training data; integration (FE/BE); hardware limits; training delays; **privacy breach**.  
Mitigations: regularization, cross-validation, augmentation; hyperparameter tuning; threshold tuning, human-in-the-loop; contract-first API, CI, mocks; cloud GPU; encryption, anonymization, access control, audits.

---

## 13. References to use in IPD

- **Problem/background:** Fulk (2022), Jones (2020), Horodyski (2023), Lewton & Haddad (2024), Daryanto et al. (2024, 2025), Baby et al. (2025), Machhale et al. (2024).  
- **Platforms:** Big Interview, HireVue, VMock, Huntr, Kickresume, FairHire, Conversate, Prepmania.  
- **Methods:** Saunders et al. (2019) – Research Onion; Beck et al. (2001) – Agile.  
- **Tech:** spaCy, Hugging Face Transformers, OpenAI GPT-4, Google Gemini, Next.js, FastAPI, PostgreSQL, AWS S3.

---

*This summary is derived from 20221214_w1998730.pdf (PPRS). Use it for IPD presentation, requirements checklist, and alignment with the IPD marking criteria (stakeholders, requirements, architecture, time schedule).*
