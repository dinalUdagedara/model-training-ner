# Chapter 08: Testing (thesis draft — paste into Word)

**Student:** Udagedara Thiyunu Dinal Bandara | **ID:** W1998730  
**Project:** CrackInt — AI-driven personalized interview preparation platform  

**How to use (author notes — delete before submission):** Paste into your thesis `.docx` using the **IIT 2025/26** styles for Chapter 8 (Testing). Replace `[Figure X]` / `[Table X]` if numbering differs. **Quantitative values** below must stay **consistent** with **Chapter 07** (Tables 7.2 & 7.4) and **Appendix G** (training notebooks, corpora, exported checkpoints).

**Template:** §8.1–8.11 follow the official **Chapter 8 : Testing** outline. Detailed functional test tables and evidence appear in **Appendix D** (Appendix B is use cases).

---

## CHAPTER 08: TESTING

### 8.1 Chapter overview

This chapter reports **how** CrackInt was validated after implementation (Chapter 07). The **goals of testing** are:

1. **Model testing** — Quantify **named entity recognition (NER)** quality for **résumés** and **job postings** using held-out data and **entity-level** precision, recall, and F1 (seqeval).
2. **Functional testing** — Check that the **web application and REST API** behave in line with the **Software Requirements Specification (SRS)** functional requirements (FRs).
3. **Non-functional testing** — Provide evidence (or scoped limitations) for selected **non-functional requirements (NFRs)**—security, usability, and maintainability where measurable without a dedicated load-testing lab.

Testing was carried out **manually** for the full-stack system (browser + API), supported by **notebook evaluation** for NER and **Swagger UI** (`/api/v1/docs`) for API contracts. *[Optional: Insert Figure — testing pyramid or V-model diagram linking SRS → test types → evidence.]*

---

### 8.2 Testing criteria

Testing is organised into three complementary types:


| Type                       | Focus                                         | Evidence in this chapter                                                                             |
| -------------------------- | --------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| **Model (AI/ML)**          | Résumé NER and job-poster NER                 | §8.3–8.6; splits and metrics consistent with **Chapter 07** and **Appendix G** (frozen training run) |
| **Functional (black-box)** | FRs: auth, ingestion, sessions, match, etc.   | §8.7; traceability to FR IDs from SRS (Chapter 04)                                                   |
| **Non-functional**         | NFRs: security, responsiveness, documentation | §8.8; honest status for items not load-tested                                                        |


**Scope:** If automated **unit/integration** tests are run (e.g. `pytest`), state counts here or in **Appendix B**; otherwise describe **manual** and **regression** testing only.

---

### 8.3 Model testing

CrackInt’s core ML components are **token-level NER** models with **BIO** tags and a **CRF** decoder (Chapter 07). **Evaluation** follows standard **sequence labelling** practice.

#### 8.3.1 Metrics and procedure

- **Library:** **seqeval** (entity-level **precision**, **recall**, **F1**); micro-averaged scores aggregate over all entities.  
- **Splits:** **80% / 10% / 10%** train / validation / test, **random seed 42**, after shuffling (see Chapter 07, Table 7.1 & 7.3).  
- **Padding:** Label index **-100** is masked out in the loss; evaluation aligns predicted tags with gold tags only on **non-padded** tokens.  
- **Entity types:**  
  - **Résumé:** NAME, EMAIL, SKILL, OCCUPATION, EDUCATION, EXPERIENCE.  
  - **Job poster:** JOB_TITLE, COMPANY, LOCATION, SALARY, SKILLS_REQUIRED, EXPERIENCE_REQUIRED, EDUCATION_REQUIRED, JOB_TYPE.

*[Optional: confusion-matrix style discussion — only if exported from the training/evaluation notebooks listed in Appendix G.]*

#### 8.3.2 Résumé NER — experiments and results

**Data:** **4738** annotated résumés; test set **475** documents. **Training artefacts** and hyperparameters: Chapter 07, **Table 7.1**.

**Table 8.1 — Résumé NER: test-set performance (entity-level F1)**

*Same underlying results as Chapter 07 **Table 7.2**; reproduce here for examiner convenience or cross-reference “see Table 7.2”.*


| Entity            | Precision | Recall | F1       |
| ----------------- | --------- | ------ | -------- |
| NAME              | 0.99      | 0.93   | 0.96     |
| EMAIL             | 1.00      | 0.93   | 0.96     |
| SKILL             | 0.92      | 0.79   | 0.85     |
| OCCUPATION        | 0.73      | 0.58   | 0.65     |
| EDUCATION         | 0.84      | 0.72   | 0.77     |
| EXPERIENCE        | 0.89      | 0.67   | 0.77     |
| **Micro average** | 0.90      | 0.77   | **0.83** |


**Validation** (development): micro F1 **~0.86**. **Test** seqeval F1 **~0.830** (notebook log).

#### 8.3.3 Job-poster NER — experiments and results

**Data:** **6327** job postings; test set **634**. **Hyperparameters:** Chapter 07, **Table 7.3**.

**Table 8.2 — Job-poster NER: test-set performance (entity-level F1)**

*Aligned with Chapter 07 **Table 7.4**.*


| Entity              | Precision | Recall | F1       |
| ------------------- | --------- | ------ | -------- |
| JOB_TITLE           | 1.00      | 1.00   | 1.00     |
| COMPANY             | 1.00      | 1.00   | 1.00     |
| LOCATION            | 0.98      | 0.98   | 0.98     |
| SALARY              | 0.97      | 0.97   | 0.97     |
| SKILLS_REQUIRED     | 0.74      | 0.73   | 0.73     |
| EXPERIENCE_REQUIRED | 0.98      | 0.98   | 0.98     |
| EDUCATION_REQUIRED  | 0.98      | 0.98   | 0.98     |
| JOB_TYPE            | 1.00      | 0.99   | 0.99     |
| **Micro average**   | 0.86      | 0.85   | **0.85** |


**Validation** micro F1 **~0.89**; **test** seqeval F1 **~0.854**.

---

### 8.4 Benchmarking

**Résumé NER:** The training corpus **merges** multiple sources (see data preparation, Chapter 07). Direct **numeric comparison** to a single published benchmark is **not** straightforward because **label schema**, **preprocessing**, and **splits** differ from public leaderboard tasks.

**Job-poster NER:** Data include **SkillSpan**-aligned merges and **project-specific** expansions. Reported **F1 scores** on SkillSpan in the literature use **different** entity sets and evaluation protocols; therefore this chapter reports **internal** test metrics (Tables 8.1–8.2) and treats external work as **contextual background** (Chapter 02) rather than a strict head-to-head benchmark.

**Qualitative positioning:** Word2Vec + BiLSTM + CRF is a **strong** classical baseline for sequence NER; **weighted sampling** during training was used to mitigate **class imbalance** (Chapter 07). A formal **ablation study** (e.g. with vs without sampling) is **optional future work** unless already recorded in **Appendix G** training logs.

---

### 8.5 Further evaluations (optional)

*[Include only if you have evidence. Examples:]*

- **Qualitative samples:** 2–3 **screenshots** or short JSON snippets of **good** vs **noisy** extractions (PDFs).  
- **LLM features:** Smoke test `**POST /api/v1/sessions/{id}/chat`** (the unified turn used by the UI): after a valid prep session, send a chat turn and assert `**ChatTurnPayload.new_messages**` with expected QUESTION/FEEDBACK shapes when the provider and OpenAI credentials are configured per **Appendix G** (document **HTTP status**, response shape, redact secrets). Optionally repeat for legacy routes (`next-question`, `evaluate-answer`) if you document them.

---

### 8.6 Results discussion

**NER: The résumé model achieves test micro F1 0.83; job-poster test micro F1 ~0.85 and seqeval ~0.854. Job-poster SKILLS_REQUIRED remains the hardest span type (lowest F1 per table), consistent with long, multi-token skill lists. EMAIL and NAME on résumés are high precision, supporting rule-based post-processing in the hybrid pipeline (Chapter 07).**

**Link to requirements:** **FR04** (résumé entity extraction) and **FR07** (job analysis) are **supported** by these metrics, subject to **deployment** of the résumé and job-poster NER checkpoints and configuration described in **Appendix G** (artefact paths and environment mapping).

**System features:** End-to-end **skill-gap** and **readiness** features **depend** on NER quality but also on **API** and **LLM** availability; functional tests (§8.7) validate **integration**, not only F1.

---

### 8.7 Functional testing

Functional tests were derived from the **SRS** (Chapter 04) and **PPRS** requirement IDs where applicable. Tests were executed against the **running** backend (FastAPI) and **Next.js** frontend (same environment as the demo for examiners). **Full test case tables** (all steps, screenshots, raw responses) may be placed in **Appendix D**; this section summarises **representative** cases and the **pass rate**.

**Method:** For each test: **preconditions** (e.g. user registered), **action** (API call or UI step), **expected** (HTTP 200 + schema or UI state), **actual**, **Pass/Fail**.

**Table 8.3 — Representative functional test cases (sample)**


| ID    | FR        | Scenario                                                          | Expected outcome                                 | Result                                                          |
| ----- | --------- | ----------------------------------------------------------------- | ------------------------------------------------ | --------------------------------------------------------------- |
| FT-01 | FR01      | Register with email/password                                      | User created; can log in                         | *Pass*                                                          |
| FT-02 | FR02      | Login; access protected route with JWT                            | 401 without token; 200 with Bearer token         | *Pass*                                                          |
| FT-03 | FR04      | `POST` résumé extract with valid PDF/text                         | JSON with entity fields populated                | *Pass*                                                          |
| FT-04 | FR05      | Patch saved résumé entities                                       | Updated entities persisted                       | *Pass*                                                          |
| FT-05 | FR06–FR07 | `POST` job extract (text + optional PDF)                          | Job entities or fallback per config              | *Pass*                                                          |
| FT-06 | FR08–FR11 | Session: create → next question → **evaluate** (with LLM enabled) | Messages stored; evaluation payload when enabled | *Partial / Pass* — *requires provider credentials (Appendix G)* |
| FT-07 | FR14      | List sessions; messages persist after refresh                     | Data persisted in DB                             | *Pass*                                                          |
| FT-08 | —         | `POST` skill-gap match (resume + job posting)                     | JSON skill-gap structure                         | *Pass*                                                          |
| FT-09 | —         | `GET` readiness / home-summary                                    | Dashboard payload                                | *Pass*                                                          |


*Replace `Pass`/`Partial` with your observed results after running the demo.*

**Pass rate:** *[Fill in:]* **___** / **___** tests passed (**___%**) for the **core** subset (auth, NER extract, session CRUD, match). **Partial** items (**FR08–FR12**, LLM-dependent) should be **flagged** with **environment** (e.g. 503 when agent disabled).

**Appendix D:** The full matrix in **Appendix D** adds **FT-10–FT-17** (health, profile, résumé list, job postings CRUD, readiness trend, CV score, cover letter, Swagger) and optional **FT-18–FT-20**. Report pass rate **either** for core **FT-01–FT-09** only **or** for all **FT-01–FT-17**—state which in §8.7 and in Appendix D.

---

### 8.8 Non-functional testing

Selected NFRs from the SRS were checked as follows:


| NFR theme                | Evaluation criteria                               | Method                                           | Result / note                                                       |
| ------------------------ | ------------------------------------------------- | ------------------------------------------------ | ------------------------------------------------------------------- |
| **Security (auth)**      | Passwords hashed; JWT required for private routes | Code review + `GET` with/without `Authorization` | JWT **401** without token; bcrypt-style hashing in backend          |
| **Security (transport)** | HTTPS in production                               | Deployment config                                | *[State your deployment or “dev HTTP only”]*                        |
| **Maintainability**      | OpenAPI / modular API                             | Swagger `/api/v1/docs`                           | **OpenAPI** available                                               |
| **Usability / UI**       | Responsive layout; accessible forms               | Manual resize; keyboard focus on main flows      | **Partial** — Radix-based components; **no** formal WCAG audit      |
| **Performance**          | Acceptable latency for single-user demo           | Informal timing / browser devtools               | **Partial** — not **load-tested**; depends on OpenAI for LLM routes |
| **Reliability**          | Graceful errors when LLM/NER off                  | Trigger 503 with missing keys                    | **Partial** — document observed behaviour                           |


**Accuracy testing (NFR):** For ML, **“accuracy”** is interpreted as **NER F1** (§8.3), not single-label accuracy.

---

### 8.9 (Optional) Additional testing

*[Include if applicable:]*

- **API smoke test:** `GET /api/v1/health` returns **200**.  
- **STT / Socket.IO:** Only if demonstrated — document **configuration** (AWS, etc.).  
- **Accessibility:** Short checklist (e.g. **focus visible**, **contrast** in dark mode).

---

### 8.10 Limitations of the testing process

1. **No large-scale user study** — Usability is based on **developer** and **supervisor** walkthroughs, not a formal **n** participant study.
2. **No formal penetration test** — Security review is **best-effort**; production hardening requires dedicated ops review.
3. **NER on noisy PDFs** — Metrics are on **tokenised** text; **OCR** and layout issues can degrade **live** extraction.
4. **LLM-dependent features** — Behaviour varies with **model version**, **prompt**, and **rate limits**; tests are **environment-dependent**.
5. **Benchmarking** — External **numeric** comparison is **limited** due to **dataset** and **schema** differences (§8.4).
6. **Load and scalability** — **Not** validated under concurrent users (NFR05–NFR07).

---

### 8.11 Chapter summary

This chapter presented **model testing** (résumé and job-poster NER with **test F1** summarised in §8.3 and Tables **8.1–8.2**), **benchmarking** limitations (§8.4), **functional** checks against **FRs** (§8.7), and **non-functional** evidence (§8.8). **Limitations** (§8.10) bound the claims that can be made in the **Conclusion** and **Critical evaluation** (Chapter 09). Quantitative results here must remain **internally consistent** with **Chapter 07**, **Appendix G**, and the **Abstract**.

---

## Appendix for you (not in thesis)

**Before submission:**

1. Run through **Table 8.3** in the real app; update **Pass/Partial** and **pass rate %**.
2. Copy **full** test matrix to **Appendix D** if the module requires it.
3. Align **Chapter 04** FR IDs if your SRS uses different numbering than **PPRS** (`FR01`…).
4. If **Chapter 8** and **Chapter 7** both duplicate Tables 8.1–8.2 / 7.2–7.4, examiners accept **cross-reference** (“see Table 7.2”) — avoid **contradictory** numbers.

---

*End of draft. Update pass rate; fill optional deployment HTTPS row; insert figure numbers in Word.*