# Chapter 09: Critical evaluation (thesis draft — paste into Word)

**Student:** Udagedara Thiyunu Dinal Bandara | **ID:** W1998730  
**Project:** CrackInt — AI-driven personalized interview preparation platform  

**Template check:** Aligns with the official **IIT 2025/26** thesis template — **Chapter 9 : Critical Evaluation**, sections **9.1–9.9**. Subsections **9.6.x** are adapted to the **actual** evaluation set (self + peers + three industry practitioners).

**How to use (author notes — delete before submission):** Paste into Word; apply IIT heading styles. Replace bracketed names/dates. Keep **numbers** aligned with **Chapter 07**, **Chapter 08**, and **Appendix G**. Do **not** cite internal repo filenames in examiner-facing text.

---

## CHAPTER 09: CRITICAL EVALUATION

### 9.1 Chapter overview

This chapter presents a **critical evaluation** of CrackInt after **implementation** (Chapter 07) and **testing** (Chapter 08). The purpose is not to repeat raw metrics, but to **interpret** them: judge how well the system meets its **Software Requirements Specification (SRS)** (Chapter 04), identify **strengths and weaknesses**, and state **honestly** what could not be validated within the project timeframe (e.g. large-scale user trials, production load testing).

The chapter is organised as follows: **evaluation methodology and criteria** (§9.2–9.3); **self-evaluation** of design and engineering decisions (§9.4); **selection of evaluators** and evaluation protocol (§9.5); **evaluation results** from the author, peer-level walkthroughs, and **three industry practitioners** (§9.6); **limitations of the evaluation itself** (§9.7); a consolidated view of **functional and non-functional requirement implementation** (§9.8); and a **summary** (§9.9).

---

### 9.2 Evaluation methodology and approach

**Purpose.** The critical evaluation phase answers: *(i)* whether the **artifact** (CrackInt) solves the problem posed in Chapter 01; *(ii)* whether **technical claims** (especially NER quality and LLM-backed coaching) are **supported by evidence** from Chapter 08; and *(iii)* what **trade-offs** were accepted (accuracy vs. latency, automation vs. manual correction).

**Approach.** The project follows a **design-science** style trajectory (see Chapter 03): build a system, measure it, reflect. Evaluation combines:

1. **Quantitative evidence** — Entity-level **precision, recall, F1** for résumé and job-poster NER (Chapter 08, Tables 8.1–8.2); functional test **pass rate** where recorded (Chapter 08, §8.7).  
2. **Qualitative evidence** — **Self-evaluation** (§9.4), structured walkthrough feedback from **two independent final-year evaluators**, and structured feedback from **three industry practitioners** (DevOps, systems engineering, UI/UX).  
3. **Requirements traceability** — Mapping **FR** and **NFR** IDs from the SRS to **implemented behaviour**, marking items as **fully met**, **partially met**, or **not demonstrated**, with justification (§9.8).

**What this evaluation is not.** It is **not** a randomised controlled trial with hundreds of participants. **Generalisation** to all industries and interview formats is **not** claimed. **External benchmarking** of NER against public leaderboards is **limited** (Chapter 08, §8.4).

---

### 9.3 Evaluation criteria

Evaluation uses the following **criteria**, aligned with the SRS and project aims:

| Criterion | Meaning | Primary evidence |
|-----------|---------|------------------|
| **C1 — Functional coverage** | Core flows (auth, résumé/job ingestion, sessions, analytics-oriented APIs) work end-to-end. | Chapter 08 functional tests; §9.8 FR table. |
| **C2 — ML utility** | NER models achieve **usable** extraction quality on held-out data. | Chapter 08 §8.3; Tables 8.1–8.2. |
| **C3 — Semantic coaching** | Where enabled, LLM-backed question and evaluation routes provide **structured** outputs; behaviour is **configurable** and **fails gracefully** when disabled. | Chapter 07; Chapter 08 §8.7–8.8; limitations. |
| **C4 — Security & maintainability** | Authentication, JWT-protected routes, hashed passwords; **OpenAPI** for APIs. | Chapter 08 §8.8; implementation. |
| **C5 — Usability (engineering view)** | Responsive UI stack; no formal WCAG audit claimed unless completed. | Chapter 08; honest NFR status. |
| **C6 — Ethics & transparency** | Users can correct entities; AI limitations stated (SLEP, Chapter 05). | Chapters 05, 07, 08. |

Weights are **implicit**: **C1–C2** are highest for a project whose core novelty is **integrated** parsing and practice; **C3–C5** matter for deployment readiness; **C6** is mandatory for responsible use.

---

### 9.4 Self-evaluation

This section records the **author’s own** critical assessment of CrackInt.

**Architecture and stack.** The **Next.js** frontend and **FastAPI** backend provide a **clear separation of concerns**, JSON APIs, and **automatic OpenAPI** documentation—appropriate for an academic prototype and **NFR13**. **PostgreSQL** with structured entities stored for résumés and job postings supports **FR04–FR07** and session history **FR14**. The choice of **Word2Vec + BiLSTM + CRF** for NER (rather than a heavy transformer encoder at inference) trades **absolute SOTA** on generic benchmarks for **controllable training**, **faster inference**, and **transparent** failure modes on noisy text—reasonable for the FYP scope.

**NER performance.** **Résumé** test **micro F1 0.83** and **job-poster** **~0.85** (Chapter 08) show the models are **fit for purpose** as **assistive** extractors, not infallible parsers. **SKILLS_REQUIRED** on job postings remains the **weakest** entity type—expected for long, variable skill phrases. The **hybrid** strategy (rules for high-precision fields where applicable, model for spans) is **justified** in practice.

**LLM features.** The production UI drives **`POST /sessions/{id}/chat`**, which invokes question generation and evaluation **in one call**; provider availability and **`OPENAI_API_KEY`** still gate real LLM output. When the provider is unavailable, the API should not silently claim “full coaching”; Chapter 08 records **partial** verification where appropriate. This is an **honest** limitation, not a failure of coding effort.

**What would be improved with more time.** Larger **user evaluation** (task-based usability); **automated regression** tests in CI; **documented** latency percentiles on a fixed hardware profile; **broader** OCR stress tests on résumé scans.

---

### 9.5 Selection of evaluators

The **IIT template** encourages inputs from technical and domain-facing stakeholders. Within project constraints, this chapter uses a **mixed evaluator set**: author self-evaluation, peer walkthroughs, and **three industry practitioners** with relevant software-delivery experience.

**Who evaluated the system (for §9.6)**

| Evaluator | Role | Contribution |
|-----------|------|----------------|
| **E1 — Author** | Developer and researcher | Self-evaluation (§9.4); ran tests in Chapter 08; demonstrated the build. |
| **E2 — Peer evaluator 1** | Final-year B.Eng. Software Engineering student | Independent walkthrough of CrackInt using a common task script. |
| **E3 — Peer evaluator 2** | Final-year B.Eng. Software Engineering student | Same protocol as E2; feedback collected separately to reduce group bias. |
| **E4 — Industry evaluator 1** | Senior DevOps Engineer, IFS | Technical review of end-to-end flow, reliability signals, and operational concerns. |
| **E5 — Industry evaluator 2** | Systems Engineer, NSB Bank | Review of workflow clarity, practical usefulness, and dashboard experience. |
| **E6 — Industry evaluator 3** | UI/UX Designer, IFS | Review of interaction quality, usability, and experience consistency. |

**Protocol (summary).** Evaluators were given a short script: authenticate, submit résumé/job input, inspect extraction outputs, run a session/chat turn, and review summary/readiness screens. Feedback was collected as **strengths**, **improvement points**, and **overall rating** (1–5 scale). The chapter reports thematic findings; detailed notes can be placed in an appendix if required.

**Scope note.** A large expert panel was not feasible in the available timeframe. Findings therefore represent a focused qualitative evaluation rather than population-level usability statistics.

---

### 9.6 Evaluation results

#### 9.6.1 Overall synthesis

Across self, peer, and industry feedback (E1–E6), CrackInt was generally viewed as a **coherent end-to-end platform** (ingestion → extraction → session practice → summary/readiness). Overall scoring from industry participants was **moderate-positive** (3.6/5 to 3.9/5), indicating practical value with clear room for refinement before production-grade deployment.

#### 9.6.2 Industry evaluator findings (E4–E6)

Industry feedback was analysed thematically, following the criteria in §9.3.

**Table 9.3 — Industry evaluation summary (thematic analysis)**

| Evaluator | Role | Positive observations | Improvement points | Overall |
|-----------|------|-----------------------|--------------------|---------|
| **E4** | Senior DevOps Engineer, IFS | End-to-end workflow is clear; NER extraction is useful in the pipeline. | Improve SKILL false-positive handling; provide clearer error messaging when LLM key/provider is unavailable. | **3.8/5** |
| **E5** | Systems Engineer, NSB Bank | Dashboard is practical; session workflow is understandable. | Add richer feedback rubric (more structured scoring dimensions); improve mobile responsiveness for key screens. | **3.6/5** |
| **E6** | UI/UX Designer, IFS | Architecture and feature integration are strong; résumé-job matching is useful. | Add explicit latency/performance benchmarks; increase automated testing coverage for stability and regression control. | **3.9/5** |

**Interpretation.** Feedback indicates the current system is a **credible and usable prototype**, while experts consistently requested stronger **production-readiness controls**: output-quality tuning, clearer failure communication, measurable performance targets, and broader automated testing.

#### 9.6.3 Peer walkthrough findings (E2–E3)

Peer walkthroughs aligned with the industry view: the flow is understandable and feature-rich for an FYP, but user confidence depends on clear communication of AI limitations and robust error handling. These observations support the same improvement themes identified by E4–E6.

#### 9.6.4 Consolidated improvement themes

Across all evaluators, four recurring themes emerged:

1. **Extraction quality refinement** — especially reducing false positives in skill extraction.
2. **Operational transparency** — clearer user-facing errors for disabled/missing LLM configuration.
3. **Usability polish** — stronger mobile responsiveness and clearer feedback presentation.
4. **Engineering hardening** — explicit latency benchmarks and expanded automated tests.

---

### 9.7 Limitations of evaluation

1. **Sample size** — The qualitative set is still small (author + peers + three industry practitioners), so findings are directional rather than statistically generalisable.  
2. **Evaluator profile breadth** — While industry practitioners were included, no dedicated recruitment/HR domain panel was run; career-domain validity should be interpreted cautiously.  
3. **Template ideal vs reality** — A larger multi-organization panel was not feasible; the method used is documented transparently in §9.5–9.6.  
4. **Deployment context** — Evaluation reflects prototype/development conditions; **NFR05–NFR07** (scale, availability) are not proven via load-testing.  
5. **LLM variability** — Session behaviour can vary with provider/model changes and runtime configuration.  
6. **NER generalisation** — Metrics are based on project corpora; broader cross-domain/language performance is not yet validated.

These limitations **do not invalidate** the technical contributions but **bound** the strength of **user-centric** claims. They should be **echoed** in Chapter 10.

---

### 9.8 Functional and non-functional requirements implementation

This section summarises implementation status against the **SRS** (Chapter 04). Status labels: **Met** (fully addressed in the submitted system), **Partial** (works with constraints or incomplete edge cases), **Not demonstrated** (not implemented or out of scope for the final build).

#### 9.8.1 Functional requirements (summary)

**Table 9.1 — Functional requirements — implementation status**

| ID | Requirement theme | Status | Comment |
|----|-------------------|--------|---------|
| FR01 | Registration | **Met** | Email registration available. |
| FR02 | Secure authentication | **Met** | JWT; password hashing. |
| FR03 | Résumé upload formats | **Partial** | PDF and text paths; confirm DOCX if claimed in SRS. |
| FR04 | NER extraction | **Met** | Hybrid résumé NER; metrics in Chapter 08. |
| FR05 | Edit extracted entities | **Met** | Persisted updates via API. |
| FR06–FR07 | Job input and analysis | **Met** | Job extraction; job-poster NER or fallback per deployment. |
| FR08 | Personalised questions (LLM) | **Partial** | Session agent when enabled; count/style depend on agent. |
| FR09–FR10 | Chat practice; text answers | **Met** | Sessions and messages. |
| FR11–FR12 | Semantic evaluation; rich feedback | **Partial** | LLM evaluation when enabled; structure as returned by API. |
| FR13 | Conversational follow-ups | **Partial / TBC** | Confirm behaviour in final agent version. |
| FR14 | Session persistence | **Met** | Stored history. |
| FR15–FR16 | Analytics and charts | **Partial** | Backend readiness/summary/trend; charts depend on UI. |
| FR17 | Export PDF | **Not demonstrated** | Unless implemented before submission. |
| FR18 | Profile / preferences | **Partial** | Core profile; “preferences” as per UI. |
| FR19 | Pause/resume / auto-save | **Partial** | Persistence exists; timed auto-save as per product. |
| FR20–FR23 | Hints, search, email | **Partial / Not demonstrated** | As per final build. |
| FR24–FR25 | Fallbacks; admin logging | **Partial** | Document observed behaviour. |

*Adjust rows to match your final Word document FR table (Chapter 04).*

**Additional capabilities** (skill-gap match, readiness endpoints, optional CV scoring, cover letter routes) **support** the product narrative but may be listed in **Chapter 07** if not every ID exists in the original SRS table.

#### 9.8.2 Non-functional requirements (summary)

**Table 9.2 — Non-functional requirements — implementation status**

| ID | Theme | Status | Comment |
|----|-------|--------|---------|
| NFR01 | Encryption / storage | **Partial** | Password hashing; storage model as implemented; S3 if used for uploads. |
| NFR02–NFR04 | Latency targets | **Partial** | Report informal timings or cite limitation. |
| NFR05–NFR07 | Scale / availability | **Partial / Not demonstrated** | No load-test evidence unless provided. |
| NFR08 | Data integrity | **Partial** | Server-side persistence; define auto-save claims carefully. |
| NFR09–NFR12 | Usability / browsers | **Partial** | Responsive design; spot-check; WCAG not fully audited unless tested. |
| NFR13 | Maintainability / OpenAPI | **Met** | OpenAPI available. |
| NFR14–NFR16 | Privacy / JWT / session | **Partial** | JWT; full GDPR UX flows — verify in app. |
| NFR17+ | Backup, monitoring, cost | **Partial / Pending** | As per deployment. |

---

### 9.9 Chapter summary

This chapter critically evaluated CrackInt using **stated criteria** (§9.3), **self-evaluation** (§9.4), **peer walkthroughs**, and **three industry evaluations** (§9.5–9.6), followed by explicit limitations (§9.7). The expert feedback was **moderate-positive** and consistently pointed to improvement opportunities in extraction precision, UX clarity, performance benchmarking, and automated testing. **Functional and non-functional** fulfilment is summarised in §9.8: core flows are largely met, while LLM-dependent and scale-related aspects remain partially met or bounded by current evidence. The next chapter (**Conclusion**) links these findings to research objectives, contributions, and future work.

---

## Appendix for you (not in thesis)

1. **Reconcile Table 9.1–9.2** (FR/NFR) with your live app + Swagger walkthrough; change any **Partial** to **Met** only if true.  
2. If Chapter 04 FR numbering differs from PPRS, **one table** in Chapter 04 should be the master list—mirror IDs here.  
3. **Before submission:** keep raw notes (date/method/consent) for E4–E6 in appendix evidence.  
4. If the module later requires supervisor comments, add them as a separate source without contradicting §9.5.

---

*End of draft.*
