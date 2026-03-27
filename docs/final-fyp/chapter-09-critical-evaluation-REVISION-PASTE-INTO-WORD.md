# Chapter 9 — Critical evaluation (REVISION for paste into Word)

**Use this to replace your current Chapter 9 text** so it aligns with **real email feedback** and **Appendix I** (screenshots of correspondence).  
Adjust **appendix letter** if yours is not **Appendix I**.  
Adjust **§8.x** cross-references if your Chapter 8 numbering differs.

**Note:** The `.docx` at `crackInt/FINAL/w1998730_FYP.docx` was not edited automatically; paste these sections in Word and preserve your heading styles (Heading 1 = CHAPTER 09, etc.).

---

## CHAPTER 09: CRITICAL EVALUATION

### 9.1 Chapter overview

This chapter presents a critical evaluation of CrackInt after implementation (Chapter 07) and testing (Chapter 08). The purpose is not to repeat raw metrics alone, but to interpret them: judge how well the system meets its Software Requirements Specification (SRS) (Chapter 04), identify strengths and weaknesses, and state honestly what could not be validated within the project timeframe (e.g. large-scale user trials, production load testing).

The chapter is organised as follows: evaluation methodology and criteria (§9.2–9.3); self-evaluation (§9.4); selection of evaluators and protocol (§9.5); evaluation results from peers, industry practitioners, an external final-year student from a management programme, and written academic feedback on the dissertation (§9.6); limitations of the evaluation (§9.7); functional and non-functional requirement implementation status (§9.8); and a summary (§9.9).

**Primary qualitative evidence** for external views is reproduced as **screenshots of email correspondence** in **Appendix I (Figure I.1–I.7)**. This chapter summarises and synthesises that evidence thematically.

---

### 9.2 Evaluation methodology and approach

**Purpose.** The critical evaluation phase answers: (i) whether the artifact (CrackInt) addresses the problem posed in Chapter 01; (ii) whether technical claims (especially NER quality and LLM-backed coaching) are supported by evidence from Chapter 08; and (iii) what trade-offs were accepted (accuracy vs. latency, automation vs. manual correction).

**Approach.** The project follows a design-science style trajectory (see Chapter 03): build a system, measure it, reflect. Evaluation combines:

- **Quantitative evidence:** Entity-level precision, recall, and F1 for résumé and job-poster NER (Chapter 08; metrics tables); functional testing outcomes where recorded (Chapter 08; summary tables and Appendix D).
- **Qualitative evidence:** Author self-evaluation (§9.4); **written feedback by email** after online demonstration and/or hands-on walkthrough from **two peer evaluators** (final-year software engineering), **three industry evaluators** (DevOps, information security / systems perspective at a bank, UX engineering), **one external final-year management student** (another university), and **one academic reviewer** who commented on the **dissertation structure** as well as the system narrative. Full messages are evidenced in **Appendix I**.
- **Requirements traceability:** Mapping FR and NFR IDs from the SRS to implemented behaviour (§9.8).

**What this evaluation is not.** It is not a randomised controlled trial with hundreds of participants. Generalisation to all industries and interview formats is not claimed. External benchmarking of NER against public leaderboards remains limited (Chapter 08).

---

### 9.3 Evaluation criteria

**Table 37: Evaluation criteria**


| Criterion                       | Meaning                                                                                                                                               | Primary evidence                                                                 |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| C1 – Functional coverage        | Core flows (auth, résumé/job ingestion, sessions, analytics-oriented APIs) work end-to-end.                                                           | Chapter 08 functional testing; §9.8 FR table.                                    |
| C2 – ML utility                 | NER models achieve usable extraction quality on held-out data.                                                                                        | Chapter 08 model testing; metrics tables.                                        |
| C3 – Semantic coaching          | Where enabled, LLM-backed question and evaluation routes provide structured outputs; behaviour is configurable and should fail clearly when disabled. | Chapter 07; Chapter 08; peer and industry comments on transparency (Appendix I). |
| C4 – Security & maintainability | Authentication, JWT-protected routes, hashed passwords; OpenAPI for APIs.                                                                             | Chapter 08; implementation.                                                      |
| C5 – Usability                  | Responsive UI; clarity of feedback and progress.                                                                                                      | Industry and peer email feedback; Chapter 08 NFR discussion.                     |
| C6 – Ethics & transparency      | Users can correct entities; AI limitations and error paths (SLEP, Chapter 05).                                                                        | Chapters 05, 07, 08; Appendix I (peer emphasis on messaging and errors).         |


---

### 9.4 Self-evaluation

*(Keep your existing §9.4 paragraphs if they are still accurate — architecture, NER F1, hybrid strategy, LLM gating, “what would improve with more time”. No change required unless you wish to tighten wording.)*

---

### 9.5 Selection of evaluators

External feedback was collected **after** an **online demonstration** and/or **guided walkthrough** using a short task script: authenticate; submit résumé and job-related input; inspect extraction outputs; run a practice session / chat turn where available; review dashboard or readiness-style screens. Evaluators replied by **email**; **screenshots of those messages** are included in **Appendix I** as primary evidence.

**Table 38: Selection of evaluators**


| Code | Evaluator (role as stated in correspondence)                                                             | Contribution                                                                                                                                                                                                 |
| ---- | -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| E1   | Author                                                                                                   | Self-evaluation (§9.4); ran tests in Chapter 08; demonstrated the build.                                                                                                                                     |
| E2   | Kavithra Methnula — peer (final-year Software Engineering)                                               | Independent walkthrough feedback (email; Appendix I, Figure I.1).                                                                                                                                            |
| E3   | Ginura Premawardana — peer (final-year Software Engineering)                                             | Second peer walkthrough feedback on the same scope (email; Appendix I, Figure I.7).                                                                                                                          |
| E4   | Nethmi Navodya — Senior DevOps Engineer, IFS R&D International (Pvt) Ltd                                 | Technical review: pipeline, NER integration, operational recommendations (email; Appendix I, Figure I.3).                                                                                                    |
| E5   | Sakindu Udagedara — Information Security Engineer, National Savings Bank                                 | Review of dashboard, session workflow, feedback presentation and mobile use (email; Appendix I, Figure I.2).                                                                                                 |
| E6   | Promodh Madusha — UX Engineer                                                                            | UX-focused review: architecture/integration, résumé–job value, perceived performance, testing (email; Appendix I, Figure I.5).                                                                               |
| E7   | Tharushi (M.G.T.) Hanshika — final-year B.Sc. Marketing Management, Sabaragamuwa University of Sri Lanka | External student perspective: end-to-end journey, sessions, feedback usefulness, extraction and mobile polish (email; Appendix I, Figure I.4).                                                               |
| E8   | Hiranya Udagedara — academic reviewer (credentials as on correspondence)                                 | Written feedback on **dissertation** narrative, testing/evaluation chapter structure, cross-references, and appendix concreteness, in addition to commendations on the work (email; Appendix I, Figure I.6). |


**Scope note.** The panel is small and purposive; findings are **directional** and support **thematic** conclusions, not population-level usability statistics. E8’s comments focus partly on the **written thesis**, which complements but is distinct from pure end-user testing of the live application.

---

### 9.6 Evaluation results

#### 9.6.1 Overall synthesis

Across **E1–E8**, CrackInt was generally viewed as a **coherent end-to-end platform** with **credible NER integration** and **practical interview-preparation value** for a final-year artifact. Industry-aligned reviewers rated the prototype **moderately positively** where numerical scores were given (approximately **3.6/5 to 3.9/5** in the industry emails reproduced in Appendix I). Peer and external-student feedback consistently praised **navigation**, **scope**, and **session-style practice**, while asking for **clearer communication of AI limits**, **stronger validation and error handling**, and **richer feedback structure** (rubric, benchmarks, mobile polish). **Appendix I** provides the verbatim email evidence behind this synthesis.

#### 9.6.2 Industry practitioner findings (E4–E6)

Industry feedback was analysed thematically against §9.3.

**Table 39: Industry evaluation summary (thematic analysis; aligned with Appendix I)**


| Code | Role (as on correspondence)        | Positive observations (summary)                                                                                                    | Improvement points (summary)                                                                                                                                          | Overall (where stated)                                                                                     |
| ---- | ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| E4   | Senior DevOps Engineer, IFS        | Clear end-to-end workflow; NER credibly integrated in the pipeline, not a disconnected notebook exercise.                          | Tighten SKILL span quality (false positives on real CVs); define **benchmark targets** (e.g. response-time and extraction-quality thresholds) for future measurement. | Solid academic prototype; path toward production if extraction and failure modes are hardened (see email). |
| E5   | Information Security Engineer, NSB | Practical **dashboard**; **session workflow** understandable without heavy onboarding.                                             | **Richer feedback rubric** in the UI (dimensions of quality, not only a single score); **improve mobile responsiveness** on key flows.                                | Useful concept and credible prototype (see email).                                                         |
| E6   | UX Engineer                        | Strong **architecture and feature integration** for a student project; **résumé–job / gap-style** value useful for interview prep. | Communicate **latency / performance expectations** where users wait; **more automated testing** (regression, critical paths) for stability as features grow.          | Strong prototype; emphasise measurable performance and quality gates (see email).                          |


**Interpretation.** Industry and UX feedback converges on **production-readiness**: refine **extraction trustworthiness**, make **feedback and progress** easier to interpret, improve **mobile** experience, set **explicit benchmarks**, and strengthen **automated testing** and **transparent** behaviour when services are constrained.

#### 9.6.3 Peer walkthrough findings (E2–E3)

**Kavithra Methnula (E2)** and **Ginura Premawardana (E3)** both reviewed authentication, résumé/job inputs, extraction review, session/chat, and summary/readiness views. **Themes:** intuitive **navigation** and a **cohesive** feature set (not a single-screen demo); **editable entities after parsing** as a **trust-building** step. **Improvements:** **on-screen messaging** must match actual capability when LLM or backend features are limited (avoid implying “full coaching” when not available); **stronger validation and feedback** for noisy inputs, short answers, or failed uploads; **dependable error paths** so users retain confidence after a failed step. These points align with industry concerns on **transparency** and **usability** (§9.6.2). **Evidence:** Appendix I, Figures **I.1** and **I.7**.

#### 9.6.4 External management-student perspective (E7)

**Tharushi Hanshika (E7)** provided structured feedback after demo and practice sessions from a **final-year management** perspective (another university). **Strengths noted:** clear structured journey (input → session → feedback); session format helpful for readiness and confidence; combined preparation steps convenient; feedback useful for strengths and weaknesses. **Improvements:** refine **skill/entity extraction** for edge cases; **mobile** polish on selected pages; **clearer progress benchmarks** (e.g. trends, target ranges); **deeper feedback rubric** (content quality, relevance, clarity). **Overall:** strong academic project with practical value; potential increases with extraction accuracy, mobile UX, and measurable indicators. **Evidence:** Appendix I, **Figure I.4**.

#### 9.6.5 Academic review of the dissertation (E8)

**Hiranya Udagedara (E8)** provided written feedback oriented toward the **dissertation** as well as the project. **Strengths:** clear **end-to-end narrative** from problem to artifact and outcomes; **testing and critical evaluation** sections described as reflective and appropriately structured for undergraduate level; **practical significance** and plausible **extensions**. **Recommendations:** ensure **section numbering and cross-references** (especially Testing/Evaluation) are fully consistent in the final PDF; distinguish explicitly what was **validated in this submission** versus **future / production expectations**; ensure **appendix artefact references** are **concrete** (final filenames, links), not placeholders. **Evidence:** Appendix I, **Figure I.6**.

#### 9.6.6 Consolidated improvement themes

Across **E2–E7** (application-focused feedback), recurring themes are:

1. **Extraction quality** — reduce **false positives** (especially skills) and improve behaviour on **noisy** or **edge-case** inputs.
2. **Transparency and trust** — align **UI copy** with **actual** LLM/backend configuration; **clear** validation and **error** handling.
3. **Feedback and progress UX** — **richer rubric** or dimensions of feedback; **benchmarks** and **trend** indicators for improvement.
4. **Mobile and perceived performance** — better **responsiveness** on key flows; explicit **latency/performance** expectations where users wait.
5. **Engineering practice** — **automated regression** tests and **quality gates** for ongoing stability.

Theme **(6)** from **E8** applies to the **thesis document**: **internal consistency**, **traceability**, and **concrete** appendix references.

---

### 9.7 Limitations of evaluation

- **Sample size and selection** — Feedback is from a **small, purposive** set (author, two software-engineering peers, three industry/UX practitioners, one external management student, one academic reviewer). Results are **not** statistically generalisable.  
- **Method** — Email-based written feedback after demo/walkthrough; not a controlled usability lab study with task timing or standardised instruments (e.g. SUS) unless separately reported.  
- **E8’s role** — Part of E8’s input concerns **dissertation quality**; it should not be read solely as end-user usability evidence.  
- **Deployment context** — Evaluation reflects **prototype** conditions; scale, availability, and load (NFR05–NFR07) are not proven by this panel.  
- **LLM variability** — Session behaviour can vary with provider, model version, and configuration.  
- **NER generalisation** — Reported metrics are on **project corpora**; broader domains/languages are not validated here.

---

### 9.8 Functional and non-functional requirements implementation

*(Retain your existing **Table 40** and **Table 41** and surrounding text from the current thesis unless your implementation status has changed.)*

---

### 9.9 Chapter summary

This chapter critically evaluated CrackInt using stated criteria (§9.3), author self-evaluation (§9.4), and **external written feedback** from peers, industry, an external management student, and an academic reviewer (§9.5–9.6), with **email evidence in Appendix I**. Quantitative NER results remain as reported in Chapter 08. The evaluation supports the conclusion that CrackInt is a **credible integrated prototype** with **clear improvement themes** in extraction quality, transparency, feedback and mobile UX, benchmarking, automated testing, and **thesis presentation consistency**. Limitations of the evaluation design are stated in §9.7; requirement implementation status is summarised in §9.8.

---

## Checklist after paste

1. Insert **Appendix I** figures **I.1–I.7** in the same order as **Table I.1** you use in the appendix (match names to this chapter’s E2–E8 mapping).
2. Update **List of Figures** if required.
3. In **§9.2**, fix any **Chapter 08 §** references to match your final Chapter 8 numbering.
4. If any evaluator requests **anonymisation**, replace names in Table 38 with role-only labels and adjust captions in Appendix I accordingly.
5. Run **Update entire table** on the **TOC** after heading updates.

