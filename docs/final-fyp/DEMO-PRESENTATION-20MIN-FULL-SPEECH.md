# CrackInt — Viva presentation full read‑aloud script (exact 20:00)

Use this as your **speaker notes**. Read it end‑to‑end; if you run fast/slow, add a 5–10 second buffer by slightly pausing after the “key message” lines.

**Slide plan (exact time budget = 20 minutes)**
1. Title Slide — 0:25  
2. Agenda Slide — 0:15  
3. Problem — 1:30  
4. Research Gap — 2:00  
5. Project Aim — 0:40  
6. System Design — 1:30  
7. Technology Stack — 0:40  
8. Dataset & Preprocessing — 1:10  
9. Model Training & Experiments — 1:10  
10. Prototype Demonstration — 4:30  
11. Testing & Evaluation — 1:20  
12. Critical Evaluation Outcome — 1:30  
13. Contribution to Knowledge & Novelty — 1:30  
14. Limitations & Future Work — 0:50  
15. Skills + Conclusion + Final Summary — 1:00  

Total = 20:00

---

## Slide 1 (0:25) — Title Slide
**On-slide text:** Project title, your name/ID, department/institute.

Speaker notes:
“Good [morning/afternoon]. I’m [your name], student ID W1998730. Today I present **CrackInt**, an AI‑driven interview preparation ecosystem that combines résumé and job understanding with authenticated practice sessions. This viva presentation follows the required structure: problem and research gap first, then system design and implementation, followed by demonstration, testing and evaluation, and finally critical evaluation and future work.”

---

## Slide 2 (0:15) — Agenda Slide
**On-slide text:** only icons/section labels (do not spell out).

Speaker notes:
“I’ll start with the problem, then my identified research gap and project aim. Next, I’ll explain the system design and the AI/ML model pipeline, show a prototype demonstration, and present testing and evaluation results. I’ll conclude with critical evaluation, contributions and novelty, limitations and future work, and what skills I acquired.”

---

## Slide 3 (1:30) — Tell the Problem clearly (with literature)
**On-slide items (3 bullets max):**
- Asymmetric recruitment: heavy AI screening
- Candidates rely on static/generic prep
- Lack of grounded feedback + end-to-end practice

Speaker notes:
“The recruitment and interview process has become increasingly asymmetric. Many organisations deploy AI systems to screen and filter candidates, while early-career job seekers still rely on fragmented, static, and generic preparation resources. This mismatch creates two key issues.  
First, generic question banks or general chat assistants don’t adapt to the candidate’s own CV and don’t reflect the specific role being applied for.  
Second, feedback is often not traceable to structured competencies extracted from documents, so the preparation focus may be inaccurate or inconsistent.  
Therefore, the core problem is not only generating interview questions, but providing preparation that is **personalised** and **grounded** in both the candidate résumé and the target job description, with measurable outcomes.”

**[Insert your citations here on the slide]**: Literature about AI screening impact and generic prep limitations.

---

## Slide 4 (2:00) — Tell the Research Gap (most important)
**On-slide items: concept map / LR → Gap**
Centre: **CV + Job Description → NER → Skill-gap → Session Coaching → Readiness**
Side gaps:
- Not end‑to‑end, grounded coaching
- Limited structured extraction + integration
- Weak/unclear evaluation metrics in prototypes

Speaker notes:
“From the literature, existing solutions typically fall into two categories. Some focus on document processing, such as extracting fields from résumés, using NER or similar techniques. Others focus on practice Q&A, simulating interview conversations.  
The research gap is that these categories are usually not integrated into a single end‑to‑end ecosystem that is grounded in **both** the résumé and the job description.  
More specifically, three gaps remain open:  
1. **Grounded question generation**: question flows are often generic rather than driven by structured entities and role specifications.  
2. **Skill-gap alignment**: systems may extract information, but they don’t reliably convert it into a structured preparation plan for practice sessions.  
3. **Measured readiness**: prototypes rarely report evaluation that ties document extraction quality and functional system behaviour to coaching outcomes in a way examiners can verify.  
So my project addresses this by unifying résumé and job understanding via a structured NER pipeline, then using those extracted competencies to drive personalised sessions and readiness analytics.”

**[Add citations for each gap node on slide 4]**

---

## Slide 5 (0:40) — Tell the Project Aim
**On-slide items:**
- Build CrackInt (full-stack)
- CV + Job → NER + skill-gap
- Authenticated practice sessions + readiness analytics

Speaker notes:
“My aim is to build **CrackInt**, a full‑stack platform that converts résumé and job documents into structured entities using a BiLSTM‑CRF NER model, performs skill‑gap matching, and then supports authenticated practice sessions. When configured, optional LLM‑based agents generate and evaluate session steps; otherwise the system still behaves consistently and returns documented partial outcomes.”

---

## Slide 6 (1:30) — Design of the System (architecture diagram + flow/algorithm)
**On-slide items:**
- Architecture boxes: Next.js → FastAPI → PostgreSQL + NER/Agents
- Flow: Input docs → Entity extraction → Skill-gap → Session coaching → Readiness

Speaker notes:
“Design‑wise, CrackInt follows a layered full‑stack architecture. The browser interface is implemented with **Next.js** and calls versioned REST APIs. The **FastAPI** back end orchestrates document extraction, skill‑gap analysis, session management, and optional agent workflows.  
The data layer is **PostgreSQL**, storing users, résumés, job postings, sessions, messages, and analytics fields.  
For the ML component, the entity extraction uses a neural pipeline with **Word2Vec embeddings**, a **bidirectional LSTM**, and a **CRF** layer for structured BIO tagging.  
The overall algorithmic flow is: extract entities from résumé and job text, align them into a role‑specific competency view, generate preparation steps, then update readiness information over the course of the practice session.”

---

## Slide 7 (0:40) — Implementation with technology stack diagrams
**On-slide items: technology stack diagram**
- Frontend: Next.js, React, Tailwind
- Backend: FastAPI, PostgreSQL, JWT
- ML: PyTorch, gensim Word2Vec, pytorch-crf, seqeval
- Optional: OpenAI + feature flags

Speaker notes:
“Implementation uses a standard but maintainable stack: **Next.js** for the front end, **FastAPI** for the API and orchestration, and **PostgreSQL** for persistence. Authentication and protected routes use **JWT**, and the application provides OpenAPI documentation through Swagger, which supports transparency in testing.  
On the ML side, the pipeline uses PyTorch for the BiLSTM‑CRF model, gensim for Word2Vec, and seqeval for evaluation. Optional LLM features are gated by configuration flags and API key availability.”

---

## Slide 8 (1:10) — If AI/ML model: dataset + preprocessing
**On-slide items:**
- Résumé dataset count: 4,738 annotated résumés; split 3790/473/475
- Job dataset count: 6,327 annotated job postings
- Label mapping: NAME, EMAIL, SKILL, OCCUPATION, EDUCATION, EXPERIENCE (resume); job labels separately
- BIO tagging + tokenisation + MAX_LEN (768 resume, 512 job)

Speaker notes:
“For the résumé NER, the frozen dataset consists of **4,738 annotated résumés**. Training uses an 80/10/10 split with a fixed random seed, resulting in 3,790 training, 473 validation, and 475 test samples.  
Preprocessing includes mapping heterogeneous source labels into a unified entity schema, converting annotations into token‑level examples, and applying BIO tagging so the CRF can model structured transitions. Word‑level sequences are padded or truncated to **MAX_LEN = 768** for résumé processing.  
For the job‑poster NER, the dataset contains **6,327 job postings**, processed similarly with a job‑specific entity set and a sequence length of **MAX_LEN = 512**.”

---

## Slide 9 (1:10) — Explain experiments: training, experiments conducted, results metrics
**On-slide items:**
- Resume: micro‑F1 ~0.83 (test); validation ~0.86
- Job: micro‑F1 ~0.85 test; validation ~0.89
- Early stopping, weighted sampling, scheduler, gradient clipping
- Export artefacts: word2vec.model, bilstm_crf_state.pt, ner_config.json

Speaker notes:
“During training, the experiments focused on stable learning for the frozen runs. I used **weighted sampling** to reduce class imbalance effects, early stopping based on validation F1 with a patience window, gradient clipping for stability, and a learning‑rate schedule that supports warmup then decay.  
For the résumé model, the test micro‑F1 is approximately **0.83**, with validation around **0.86**. For job‑poster extraction, the test micro‑F1 is approximately **0.85**, consistent with the job‑poster metrics in the thesis.  
After training, the pipeline exports the Word2Vec embeddings model, the BiLSTM‑CRF checkpoint, and the NER configuration file used by the API to load the frozen model in deployment.”

---

## Slide 10 (4:30) — Demonstration of the prototype
**On-slide items:** screenshots or short flow diagram; keep minimal text.

Speaker notes:
“Now I demonstrate the prototype.  
First, I show **registration and login**. A valid user can log in and then access protected features.  
Second, I demonstrate **résumé extraction** by uploading a sample PDF or paste text. The back end returns structured entities such as name, email, and domain‑specific skills.  
Third, I show the next step where extracted data can be reviewed or persisted in the system, demonstrating that the solution is not only extraction but also application integration.  
Fourth, I demonstrate **job extraction or job posting input**, where job‑side entities are produced or a documented fallback path is used depending on configuration.  
Fifth, I run the **skill‑gap / match** between the résumé and the job posting, showing a structured alignment that drives the practice plan.  
Sixth, I show a **practice session**. The system stores messages and, when LLM features are enabled and credentials are present, generates a coaching step and evaluation.  
Finally, I open the **readiness or dashboard view** to show integration across extraction, matching, session persistence, and analytics.”

**Negative/edge mention (must be visible in the demo):**
“As a negative test, I also demonstrate a protected endpoint call without a JWT token to show the expected 401 behaviour. Additionally, I show documented partial behaviour when LLM features are disabled or credentials are not available.”

---

## Slide 11 (1:20) — Testing and evaluation
**On-slide items:**
- NER evaluation: micro‑F1 tables cross‑reference (Chapter 7/8)
- Functional testing summary: pass rate in Appendix D
- Mention negative tests shown in demo

Speaker notes:
“Evaluation has two parts: AI/ML testing and functional testing.  
For the AI/ML testing, evaluation uses seqeval entity‑level precision, recall, and micro‑F1, aligned with the thesis tables and the frozen run. Résumé extraction achieves approximately 0.83 micro‑F1, and job‑poster extraction achieves approximately 0.85 on the test split.  
For functional testing, I ran black‑box tests derived from the SRS functional requirements. The prototype demonstration includes both positive and negative cases. The full matrix and execution results are documented in Appendix D, including pass and partial outcomes and the computed pass rate under the chosen denominator.”

---

## Slide 12 (1:30) — Critical Evaluation Outcome
**On-slide items:**
- What worked well (3 bullets)
- What was limited (3 bullets)
- Challenges encountered + mitigations (short)

Speaker notes:
“In critical evaluation, the key positive outcome is that the system delivers an integrated pipeline from document understanding to authenticated practice and readiness feedback. The hybrid approach—rules for high‑confidence fields and neural NER for contextual entities—improves robustness on realistic text.  
However, limitations exist: LLM‑dependent functionality is environment‑dependent, so some coaching steps become partial when provider credentials are missing. Additionally, noisy PDFs and OCR/layout errors can degrade live extraction quality compared to evaluation on clean tokenised text.  
Finally, the project prototype was not load‑tested under large concurrent usage. Therefore, performance and scalability claims are limited to observed behaviour in the testing environment.”

---

## Slide 13 (1:30) — Contribution to body of knowledge + Novelty
**On-slide items:**
- Contribution statements (2–3 bullets)
- Novelty explicitly stated

Speaker notes:
“My contribution is the bridging of theoretical NLP to practical interview readiness by unifying résumé and job extraction with coaching workflows. The challenge in achieving this is ensuring that extracted structured fields meaningfully drive downstream question generation and evaluation, rather than remaining as isolated outputs.  
The novelty lies in the integrated pipeline: structured entity extraction via BiLSTM‑CRF, conversion into role‑specific competency views, and the use of those views to guide session coaching and readiness analytics. The system also uses feature flags and documented partial behaviour, which makes the prototype behaviour consistent and defensible for examiners.”

---

## Slide 14 (0:50) — Limitations and future work
**On-slide items:**
- More datasets / better annotation consistency
- Better OCR and multilingual support
- Formal usability study + load testing

Speaker notes:
“For future work, I would improve OCR robustness and consider additional languages and domain‑specific entity labels. I would also run formal usability studies with participants and add load and scalability testing for stronger non‑functional evidence. Finally, I would extend missing optional features such as additional export formats and broader session capabilities if required by future versions.”

---

## Slide 15 (1:00) — New skills acquired + Use of existing skills + Conclusion + Final summary
**On-slide items:**
- 1–2 bullets new skills
- 1 bullet existing skills used
- Final summary (1 sentence)

Speaker notes:
“To conclude, the CrackInt project delivered an end‑to‑end, authenticated interview preparation ecosystem. It combines résumé and job entity extraction with skill‑gap matching, practice sessions, and readiness‑oriented analytics, with functional and ML evaluation documented in the thesis.  
In terms of skills, I acquired deeper practical experience in full‑stack integration with Next.js and FastAPI, and in building and evaluating structured NER models using Word2Vec, BiLSTM, and CRF layers.  
I also used existing software engineering skills such as version control, documentation, and systematic testing. Thank you for your attention.”

