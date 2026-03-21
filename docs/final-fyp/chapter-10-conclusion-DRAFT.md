# Chapter 10: Conclusion (thesis draft — paste into Word)

**Student:** Udagedara Thiyunu Dinal Bandara | **ID:** W1998730  
**Project:** CrackInt — AI-driven personalized interview preparation platform  
**Programme:** BEng (Hons) Software Engineering — University of Westminster (IIT)

**Template check:** Aligns with the official **IIT 2025/26** thesis template — **Chapter 10 : Conclusion** (overview; achievements of aims & objectives; utilization of course knowledge; existing vs new skills; learning outcomes; problems/challenges; deviations; limitations; future enhancements; contribution; concluding remarks).

**Sources used for this draft:** IPD submission **`docs/ipd/w1998730_20221214_IPD.pdf`** (Table 1 research objectives and LO mapping), **`docs/project/proposal-summary.md`**, and **frozen results** aligned with **Chapter 07–08** (résumé NER test micro F1 **0.78**; job-poster test micro F1 **~0.85**).

**How to use (author notes — delete before submission):** Paste into Word; apply IIT styles. If **Chapter 01** Table 1 wording differs slightly from IPD, keep **Chapter 01** as the master copy and adjust this file to match.

---

## CHAPTER 10: CONCLUSION

### 10.1 Chapter overview

This chapter concludes the dissertation by summarising **what was achieved**, how it relates to the **research aim** and **research objectives** (Chapter 01, Table 1), what **knowledge and skills** were applied and gained, what **challenges** arose, where the project **deviated** from early plans, what **limitations** remain (including testing and evaluation in Chapters 08–09), and how the work could be **extended**. Final remarks reinforce CrackInt’s **contribution** to practice and to applied NLP in career preparation.

---

### 10.2 Achievements of research aims and objectives

**Research aim (Chapter 01).** The overarching goal of this research was to **conceive, implement, and critically evaluate CrackInt** — an AI-driven, web-based interview-preparation platform that unifies **résumé and job-poster understanding** (NER), **adaptive, role-aware practice** (including LLM-backed session flows where configured), and **semantic, content-aware feedback**, within a **single candidate-centric** system. The final artefact (Chapters 06–07) delivers authenticated ingestion, dual NER pipelines, practice sessions with persisted messages, readiness-oriented APIs, and documented evaluation evidence (Chapters 08–09).

**Table 10.1 — Research objectives (Chapter 01, Table 1) — achievement status**

*Objectives and LO mappings are taken from the IPD / Chapter 01 table (R02–R22). Status reflects the **final** system and thesis at submission.*

| Ref. | Objective (summary from Chapter 01) | LOs (Ch 1) | Status | How addressed / evidence |
|------|-------------------------------------|------------|--------|---------------------------|
| **R02** | In-depth literature survey on AI-driven interview preparation | LO1, LO4, LO6 | **Achieved** | Chapter 02; gaps motivate CrackInt. |
| **R03** | Literature on résumé parsing and NER-based extraction | LO1, LO4 | **Achieved** | Chapter 02; implementation Ch 07. |
| **R04** | Literature on question generation and semantic feedback | LO1, LO4 | **Achieved** | Chapter 02; LLM session design Ch 07. |
| **R05** | Identify stakeholders | LO3, LO6 | **Achieved** | Chapter 04; onion / SRS. |
| **R06** | Identify requirement elicitation methods | LO2, LO3 | **Achieved** | Chapter 04 (survey, interviews, etc.). |
| **R07** | Identify user requirements for integrated prep system | LO3, LO6 | **Achieved** | Chapter 04 FR/NFR tables. |
| **R08** | Design architecture (NER, QG, feedback modules) | LO1, LO3, LO7 | **Achieved** | Chapter 06; implemented Ch 07. |
| **R09** | Design DB schema; secure storage; analytics | LO1, LO6, LO7 | **Achieved** | Chapter 06–07; PostgreSQL + optional S3. |
| **R10** | Collect / use annotated résumé and job data for NER | LO1, LO5 | **Achieved** | Chapter 07; merged corpora; **3023** résumés / **6327** job postings (frozen splits). |
| **R11** | OCR / preprocessing for multi-format ingestion | LO1, LO5, LO7 | **Achieved** | Chapter 07; PyMuPDF / OCR paths; user may paste text. |
| **R13** | LLM-driven question generator with adaptive difficulty | LO1, LO5, LO7 | **Partial** | Session **next-question** agent when enabled; difficulty hooks where implemented — not a separate fine-tuned QG model for all flows. |
| **R14** | Semantic feedback engine (depth, clarity, relevance) | LO1, LO5, LO7 | **Partial** | **Evaluate-answer** path when LLM enabled; no separate embedding-only engine as sole evaluator. |
| **R15** | Integrate into Next.js + FastAPI with secure storage & history | LO1, LO5, LO7 | **Achieved** | Chapter 07; sessions, JWT, OpenAPI. |
| **R16** | Evaluate NER with precision, recall, F1 | LO1, LO7, LO8 | **Achieved** | Chapter 08; résumé test micro F1 **0.78**; job-poster test micro F1 **~0.85** (seqeval). |
| **R17** | Assess question quality (BLEU/ROUGE; expert evaluation) | LO1, LO7, LO8 | **Partial** | BLEU/ROUGE against references **not** run as primary metric; no large expert QG panel — scope bounded in Ch 09. |
| **R18** | Validate semantic feedback vs expert ratings | LO1, LO7, LO8 | **Partial** | No correlation study with human raters; LLM outputs evaluated functionally (Ch 08–09). |
| **R19** | User studies on readiness / engagement | LO2, LO8 | **Partial** | **Two** final-year peer walkthroughs + self-evaluation (Ch 09); not a large longitudinal readiness study. |
| **R20** | Document architecture, implementation, evaluation | LO4, LO5, LO8 | **Achieved** | Chapters 06–09; API documentation via OpenAPI. |
| **R21** | Prepare final thesis with LR, methodology, results, contributions | LO4, LO8, LO9 | **Achieved** | This dissertation. |
| **R22** | Publish literature review / platform gaps | LO4, LO9 | **Partial** | Conference/journal paper **optional** post-submission; LR completed in thesis. |

**Note on numbering:** The IPD copy of Table 1 lists objectives **R10–R11** then **R13–R15** (implementation). If your Chapter 01 includes an **R12** row, insert it in the same table and mark status — do **not** leave a gap unexplained.

**Synthesis.** The **core** pipeline — requirements, design, **dual NER** training and evaluation, integrated **web stack**, and **documented** testing — is **delivered**. Objectives that assumed **external** expert scoring, **BLEU**-based QG evaluation, or **large** user trials are **partially** met within FYP constraints; this is **explicit** in Chapters 08–09 and does not diminish the **technical** contribution of the artefact.

---

### 10.3 Utilization of knowledge from the course

The **BEng Software Engineering** programme provided foundations in **software engineering process** (requirements through to testing), **object-oriented analysis and design**, **databases**, **web application development**, and **research methods** — applied here as: **SRS and UML-style artefacts** (Chapters 04–06); **API-first** backend design and **PostgreSQL** persistence (Chapters 06–07); **structured testing and critical evaluation** (Chapters 08–09). **Research methodology** (Chapter 03 — pragmatism, mixed methods, design-science style artefact) justified combining **quantitative** NER metrics with **qualitative** peer feedback and **requirements traceability**.

---

### 10.4 Use of existing skills (prior to the project)

Prior coursework and practice contributed: **Python** and **TypeScript**, **REST API** design, **relational data modelling**, **Git** version control, and **academic writing**. These supported **FastAPI** services, **Next.js** client development, **Alembic/SQLModel** persistence, and **clear** limitation statements suitable for examiners.

---

### 10.5 Use of new skills (developed through the project)

The following were developed or significantly deepened (**technical** emphasis):

- **Sequence labelling** for NER: **Word2Vec + BiLSTM + CRF**, **BIO** tagging, **seqeval** entity-level metrics, train/val/test protocol (Chapters 07–08).  
- **Separate job-poster NER** pipeline and **fallback** behaviour when only one model is deployed.  
- **Integrating PyTorch inference** with a production-style API (configuration, loading checkpoints, hybrid rules + model).  
- **LLM orchestration** for sessions: agents, feature flags, graceful failure when keys are missing.  
- **End-to-end verification**: Swagger/OpenAPI, manual functional tests, small **peer** evaluation protocol (Chapter 09).

---

### 10.6 Achievement of learning outcomes

Chapter 01 maps each research objective to **University of Westminster module learning outcomes LO1–LO9** (see Table 1, “LOs Mapped”). The table below links those outcome **IDs** to how this dissertation demonstrates them (wording of LOs is exactly as in your **module handbook** — if the handbook uses different labels, replace the second column only).

**Table 10.2 — Mapping of module learning outcomes (LO1–LO9) to this project**

| LO | Typical theme (verify against handbook) | How demonstrated in this work |
|----|----------------------------------------|-------------------------------|
| **LO1** | Subject knowledge / technical depth | NER design, training, metrics (Ch 07–08); full-stack implementation (Ch 07). |
| **LO2** | Research / inquiry | Literature review (Ch 02); methodology (Ch 03); survey/interviews in requirements (Ch 04); evaluation design (Ch 09). |
| **LO3** | Requirements / problem understanding | SRS, stakeholders, FR/NFR (Ch 04); traceability in Ch 09. |
| **LO4** | Communication / documentation | Thesis structure; diagrams; API documentation; **R20–R21** completed. |
| **LO5** | Implementation / engineering practice | Next.js + FastAPI + DB + ML integration (Ch 07); **R10–R15** addressed in code. |
| **LO6** | Professional / ethical / stakeholder awareness | SLEP (Ch 05); consent and data handling; honest limits on AI (Ch 08–09). |
| **LO7** | Design / architecture | OOAD, architecture, sequences (Ch 06); realised in Ch 07. |
| **LO8** | Evaluation / testing | Model testing + functional/NFR discussion (Ch 08); critical evaluation (Ch 09). |
| **LO9** | Scholarship / dissemination | Final thesis (**R21**); **R22** remains optional publication beyond submission. |

**Narrative.** Collectively, the project shows **LO1, LO5, LO7, LO8** through the **working artefact** and **measured NER** results; **LO2, LO3** through **structured requirements** and **evaluation**; **LO4, LO9** through the **dissertation**; and **LO6** through **SLEP** and **transparent** limitations.

---

### 10.7 Problems and challenges faced

1. **Heterogeneous documents** — PDFs, scans, and layout noise required robust text extraction and sometimes **manual entity correction** (FR05).  
2. **Class imbalance in NER** — Addressed with weighted sampling and careful metrics (Chapter 07).  
3. **Dual NER stacks** — Maintaining **résumé** and **job-poster** models and deployment paths increased integration work.  
4. **LLM variability and cost** — Mitigated with environment configuration, clear **503**/disabled behaviour, and **partial** claims in evaluation.  
5. **Scope vs time** — A full **BLEU/ROUGE** study, **expert-rater** correlation for feedback, and **large-n** user trials were **not** completed; peer **n = 2** plus author (Chapter 09).  
6. **Documentation drift** — Early proposals referenced multiple LLM providers; the **implemented** system is documented **as built** in Chapter 07.

---

### 10.8 Deviations from the original plan

- **LLM provider emphasis:** Early documents sometimes highlighted **Gemini** alongside OpenAI; the **submitted** implementation uses the **OpenAI** client path for session agents where configured — provider choice follows **feasibility** and **integration** in the codebase, not a comparative study.  
- **Evaluation scale:** The PPRS/Gantt narrative mentioned **larger** user testing (e.g. **20** participants in some planning text); the **reported** critical evaluation uses **self-assessment plus two final-year peers** (Chapter 09), which is **narrower** but **honest**.  
- **NER corpus and metrics:** Prototype-era figures (e.g. different corpus sizes or **~0.79** résumé F1 in older drafts) were **superseded** by the **frozen** training runs documented in Chapter 07 and **test** metrics in Chapter 08 (**0.78** résumé micro F1; **~0.85** job-poster micro F1).  
- **IPD vs final feature set:** The interim demo emphasised **NER extraction**; the final system adds **full session flows**, **readiness/skill-gap** features, and optional services (e.g. cover letter, CV scoring) as described in Chapter 07 — a **positive** extension rather than a reduction.

---

### 10.9 Limitations of the research

These **extend** Chapter 08 (§8.10) and Chapter 09 (§9.7):

- **Generalisation** — NER metrics hold for **project corpora** and splits; new domains or languages are unproven.  
- **LLM behaviour** — Not static across provider updates; feedback quality is **not** certified for hiring decisions.  
- **User evidence** — Small, **student** cohort; no industry expert review in Chapter 09.  
- **Non-functional proof** — Scalability and uptime targets (NFR05–NFR07) are **not** load-tested.  
- **Scope** — **English only**; no **ATS** integration; no **video** interviews (Chapter 01 out-of-scope).

Outputs remain **decision support** for practice, not automated recruitment decisions.

---

### 10.10 Future enhancements

- **Layout-robust parsing** and stronger **OCR** for poor-quality PDFs.  
- **Automated** regression and **CI** tests for critical API paths.  
- **Larger user studies** (task times, SUS, readiness pre/post).  
- **Multilingual** support; **PDF export** of progress (**FR17**) if required.  
- **Explainability** for skill-gap and feedback (user-facing “why”).  
- Optional **publication** fulfilling **R22** with a focused systematic-review or systems paper.

---

### 10.11 Achievement of the contribution to body of knowledge

**Problem domain:** A **workable**, **candidate-centric** integration of **résumé/job NER**, **chat practice**, and **readiness-oriented** analytics — addressing gaps identified in Chapter 02 (generic prep, shallow feedback, fragmented tools).

**Research domain:** **Empirical** NER results on **merged** résumé and job-posting corpora; a **transparent** account of **LLM-assisted** coaching **limits**; and a **requirements-traceable** evaluation suitable for a **final-year** software engineering artefact.

---

### 10.12 Concluding remarks

CrackInt shows that a **classical** neural NER stack (**Word2Vec + BiLSTM + CRF**), combined with a **modern** web platform and **optional** LLM layers, can support a **coherent** interview-preparation workflow with **measurable** parsing quality. The dissertation’s **limitations** are stated as clearly as its **F1 scores**: together they define **responsible** use and a **concrete** agenda for future work. The research objectives in **Table 10.1** are **substantively** met where they concern **delivery and measurement**; where they assumed **external** expert studies or **large** trials, they are **partially** met within the **documented** scope of the FYP.

---

## Appendix for you (not in thesis)

1. **Abstract** — Write last; ≤300 words; **three numbers** consistent with Chapter 08 (résumé F1 **0.78**, job-poster **~0.85**, plus corpus sizes or pass rate if used).  
2. **Table 10.2** — Replace the “Typical theme” column with **verbatim LO titles** from the **6COSC023W** (or current) module handbook if your examiner expects exact wording.  
3. **R12** — Confirm whether Chapter 01 Table 1 includes **R12**; align rows with Word.

---

*End of draft.*
