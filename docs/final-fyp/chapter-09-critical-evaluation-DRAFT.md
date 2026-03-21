# Chapter 09: Critical evaluation (thesis draft — paste into Word)

**Student:** Udagedara Thiyunu Dinal Bandara | **ID:** W1998730  
**Project:** CrackInt — AI-driven personalized interview preparation platform  

**Template check:** Aligns with the official **IIT 2025/26** thesis template — **Chapter 9 : Critical Evaluation**, sections **9.1–9.9**. Subsections **9.6.x** are adapted to the **actual** evaluation set (self + two final-year peers); formal supervisor or industry-expert reviews are **not** claimed unless you add them later.

**How to use (author notes — delete before submission):** Paste into Word; apply IIT heading styles. Replace bracketed names/dates. Keep **numbers** aligned with **Chapter 07**, **Chapter 08**, and **Appendix A**. Do **not** cite internal repo filenames in examiner-facing text.

---

## CHAPTER 09: CRITICAL EVALUATION

### 9.1 Chapter overview

This chapter presents a **critical evaluation** of CrackInt after **implementation** (Chapter 07) and **testing** (Chapter 08). The purpose is not to repeat raw metrics, but to **interpret** them: judge how well the system meets its **Software Requirements Specification (SRS)** (Chapter 04), identify **strengths and weaknesses**, and state **honestly** what could not be validated within the project timeframe (e.g. large-scale user trials, production load testing).

The chapter is organised as follows: **evaluation methodology and criteria** (§9.2–9.3); **self-evaluation** of design and engineering decisions (§9.4); **selection of evaluators** and **peer evaluation protocol** (§9.5); **evaluation results** from the author and **two final-year student evaluators** (§9.6); **limitations of the evaluation itself** (§9.7); a consolidated view of **functional and non-functional requirement implementation** (§9.8); and a **summary** (§9.9). **Formal supervisor review** and **industry-expert review** were **not** available as structured inputs at the time this chapter was finalised; that boundary is stated explicitly in §9.5 and §9.7.

---

### 9.2 Evaluation methodology and approach

**Purpose.** The critical evaluation phase answers: *(i)* whether the **artifact** (CrackInt) solves the problem posed in Chapter 01; *(ii)* whether **technical claims** (especially NER quality and LLM-backed coaching) are **supported by evidence** from Chapter 08; and *(iii)* what **trade-offs** were accepted (accuracy vs. latency, automation vs. manual correction).

**Approach.** The project follows a **design-science** style trajectory (see Chapter 03): build a system, measure it, reflect. Evaluation combines:

1. **Quantitative evidence** — Entity-level **precision, recall, F1** for résumé and job-poster NER (Chapter 08, Tables 8.1–8.2); functional test **pass rate** where recorded (Chapter 08, §8.7).  
2. **Qualitative evidence** — **Self-evaluation** (§9.4) and **structured walkthrough feedback** from **two independent final-year evaluators** (same cohort, not industry experts); inspection of **API documentation** (OpenAPI) for maintainability. **Supervisor** and **industry-expert** evaluations are **not** included as primary sources in §9.6 (see §9.5).  
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

**NER performance.** **Résumé** test **micro F1 0.78** and **job-poster** **~0.85** (Chapter 08) show the models are **fit for purpose** as **assistive** extractors, not infallible parsers. **SKILLS_REQUIRED** on job postings remains the **weakest** entity type—expected for long, variable skill phrases. The **hybrid** strategy (rules for high-precision fields where applicable, model for spans) is **justified** in practice.

**LLM features.** Session **next-question** and **evaluate-answer** behaviour depends on **provider availability** and **feature flags**. When disabled, the system should not silently claim “full coaching”; Chapter 08 records **partial** verification where appropriate. This is an **honest** limitation, not a failure of coding effort.

**What would be improved with more time.** Larger **user evaluation** (task-based usability); **automated regression** tests in CI; **documented** latency percentiles on a fixed hardware profile; **broader** OCR stress tests on résumé scans.

---

### 9.5 Selection of evaluators

The **IIT template** describes ideal inputs from **domain experts**, **technical experts**, and sometimes **users**. Within this FYP’s **time and access constraints**, the **qualitative** evaluation for this chapter was deliberately limited to **peer-level** feedback from the **same academic cohort**, so that claims remain **traceable** and **honest**.

**Who evaluated the system (for §9.6)**

| Evaluator | Role | Contribution |
|-----------|------|----------------|
| **E1 — Author** | Developer and researcher | Self-evaluation (§9.4); ran tests in Chapter 08; demonstrated the build. |
| **E2 — Peer evaluator 1** | Final-year B.Eng. Software Engineering student | Independent walkthrough of CrackInt using a **task script** (see §9.6); qualitative feedback on clarity, flow, and perceived usefulness. |
| **E3 — Peer evaluator 2** | Final-year B.Eng. Software Engineering student | Same protocol as E2; feedback collected **separately** to reduce group bias. |

*[Optional for Word: replace “Peer evaluator 1/2” with first names or initials if participants consented to be named; otherwise keep anonymous IDs.]*

**What was explicitly *not* used for this chapter (at finalisation)**

| Source | Status | Note |
|--------|--------|------|
| **Supervisor** | **Not included** as a formal graded evaluation in §9.6 | Routine supervision continues outside this structured evaluation; a **future** submission may add supervisor comments if required by the module. |
| **Industry / career expert** | **Not conducted** | No recruitment professional or employer evaluator was engaged; **domain** claims in §9.6.2 remain **literature- and requirements-based**. |

**Protocol (summary).** Each peer evaluator (E2, E3) was given **the same short task list** (e.g. register or use a test account → upload or paste résumé text → run job extraction → open a practice session if LLM features are enabled → note any confusion). **Time on task** and **free-text comments** were collected; optional **Likert-style** ratings (e.g. ease of use 1–5) may be summarised in §9.6.4.

**Note.** A **large** panel (e.g. five technical and five domain experts) was **not** run. Findings are **stronger on technical measurement** (NER, API behaviour, Chapter 08) than on **broad** user-satisfaction statistics. This is reflected in **§9.7**.

---

### 9.6 Evaluation results

#### 9.6.1 Overall synthesis (no supervisor-led “expert opinion”)

This subsection summarises the **combined** view from **§9.4 (self)** and **§9.6.4 (peer walkthroughs)**. A **separate supervisor sign-off** or **external expert report** was **not** used as evidence in this chapter (see §9.5).

Across E1–E3, CrackInt is **read** as a **coherent** full-stack story when demonstrated end-to-end: **ingestion → structured entities → practice sessions → readiness-oriented APIs/UI**, consistent with the **problem statement** in Chapter 01. The **main risk** peers echoed is **trust in AI output** (NER mistakes, LLM variability); mitigations align with **manual entity editing (FR05)**, **documented** configuration, and **testing limitations** in Chapter 08.

#### 9.6.2 Domain perspective (literature and requirements — not industry expert)

**Industry or HR expert evaluation was not conducted** (§9.5). The **domain** angle in this subsection is therefore **conceptual**: interview preparation benefits from **role-aligned** practice and **actionable** feedback (Chapter 02; SRS Chapter 04). CrackInt addresses this by combining **structured profile data** from NER with **conversational** practice. **Limitation:** there is **no** validation from recruitment professionals in this dissertation.

#### 9.6.3 Technical perspective (student evaluators — scope, architecture, implementation)

From the **final-year evaluators’** viewpoint (E2, E3), supported by the author’s technical self-evaluation (E1):

**Scope.** The system presents as a **candidate-centric** preparation tool; there is **no** employer-side screening workflow in scope.

**Architecture.** The **three-tier** pattern (browser → **FastAPI** backend → **PostgreSQL**) and **documented** REST API were considered **understandable** for a final-year project; peers could follow the **Swagger** interface where shown.

**Implementation.** NER quality is judged **primarily** on **Chapter 08 metrics**, not impression alone. **Security** basics (JWT, password hashing) were **not** subjected to formal penetration testing in this evaluation.

*[Fill in after sessions: 1–2 sentences on whether peers found any screen confusing or any endpoint failing during the walkthrough.]*

#### 9.6.4 Peer user evaluation (two final-year participants)

**Participants.** Two **independent** final-year students (E2, E3), **not** the author, following the **same task script** (§9.5). **Supervisor** did not act as a participant in this mini evaluation.

**Tasks (example — align with your demo).**

1. Log in or register (test account).  
2. Submit résumé content and review extracted entities.  
3. Submit job text and review job entities.  
4. Open a **prep session** and attempt at least one **question → answer** cycle *(if LLM features are enabled; otherwise note “feature not demonstrated”)*.  
5. Briefly view **readiness** or **dashboard** information if exposed in the UI.

**Observations.** *[Fill in:]*

| Theme | E2 (peer) | E3 (peer) |
|-------|-----------|-----------|
| Ease of navigation | *[e.g. clear / minor confusion at …]* | *[fill]* |
| Trust in extraction | *[e.g. would edit entities]* | *[fill]* |
| Session / chat experience | *[fill]* | *[fill]* |
| Overall (optional 1–5) | *__* | *__* |

**Representative comments (paraphrased).** *[Insert short anonymised quotes or bullet themes — e.g. “wanted clearer error when API key missing”.]*

**Interpretation.** This is a **small, homogeneous** sample (software engineering students); insights support **face-validity** and **debugging UX**, not **general population** hiring outcomes. Results complement **functional** testing (Chapter 08), not replace it.

---

### 9.7 Limitations of evaluation

1. **Sample size and cohort** — Only **two** external peer evaluators plus the author; both peers are **final-year computing students**, not a diverse user panel. Qualitative insights are **exploratory**, not statistically generalisable.  
2. **No supervisor or industry expert inputs in §9.6** — This chapter does **not** report a formal **supervisor evaluation sheet** or **industry-expert** review; claims about recruitment practice rely on **literature** (§9.6.2), not HR professionals.  
3. **Template ideal vs reality** — The template’s notional **large** expert panel was **not** feasible; the **actual** method is documented in §9.5–9.6.  
4. **Deployment context** — Evaluation reflects **development/staging**-style deployment unless you have production metrics; **NFR05–NFR07** (scale, uptime) are **not** empirically proven.  
5. **LLM variability** — Provider models and prompts **change** over time; peer experience with **session** features is **snapshot**-like and **configuration-dependent**.  
6. **NER generalisation** — Metrics are on **project corpora**; new industries or languages are **not** validated.

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

This chapter critically evaluated CrackInt using **stated criteria** (§9.3), **self-evaluation** (§9.4), **peer evaluation** from **two final-year students** (§9.5–9.6), and **explicit limitations** (§9.7). **Supervisor** and **industry-expert** reviews were **not** used as primary evidence here. **Functional and non-functional** fulfilment is **summarised** in §9.8: **core** parsing, auth, and session flows are **largely met**; **LLM-dependent** and **scale-related** items are **partially met** or **bounded** by evidence. The next chapter (**Conclusion**) ties these findings to **research objectives**, **contributions**, and **future work**.

---

## Appendix for you (not in thesis)

1. **Reconcile Table 9.1–9.2** (FR/NFR) with your live app + Swagger walkthrough; change any **Partial** to **Met** only if true.  
2. If Chapter 04 FR numbering differs from PPRS, **one table** in Chapter 04 should be the master list—mirror IDs here.  
3. **Before submission:** run the **peer task script** with E2/E3; fill **§9.6.3–9.6.4** table and quotes; obtain **consent** for anonymised use of feedback.  
4. If the module later **requires** supervisor comments in Chapter 9, add a short subsection or appendix paragraph—do **not** contradict §9.5.

---

*End of draft.*
