# Chapter 08: Testing — plan (IIT template + CrackInt)

**Sources:** `docs/thesis-template-2025-26-export.md` (Chapter 8), `docs/thesis-final-submission-checklist-from-template.md`, `THESIS-FACTS-SHEET.md`, `chapter-07-implementation-DRAFT.md` (Tables 7.1–7.4).

**Mapping note:** The **module rubric** (Excel) sometimes labels “Testing” as “Chapter 7” in a shorter outline; the **official Word template** uses **Chapter 8 : Testing** with the structure below. Use **template numbering** in your `.docx`.

---

## What the IIT template requires (verbatim structure)

| § | Title | What to include |
|---|--------|-----------------|
| **8.1** | Chapter overview | Objectives and **goals of testing** (what you will validate). |
| **8.2** | Testing criteria | Types of testing you conduct (e.g. **model**, **functional**, **non-functional**). |
| **8.3** | Model testing *(if AI/ML)* | Evaluation tasks, **metrics** (how scores are calculated). Examples: confusion matrix, accuracy, F1, precision, recall, AUC/ROC. **Table of experiments + results.** |
| **8.4** | Benchmarking *(if AI/ML)* | Compare to **baselines / literature** (especially if public or comparable data). Discuss results. |
| **8.5** | Further evaluations *(optional)* | Extra experiments on trained models; discussion. |
| **8.6** | Results discussions | Interpret **8.3–8.5** (not just paste numbers). |
| **8.7** | Functional testing | Test cases from **SRS functional requirements**; execute on prototype; **pass rate %**; template says put **full test cases + results in appendix**. |
| **8.8** | Non-functional testing | Pick **NFRs** (aligned with SRS priority); criteria + results. Template lists: accuracy, performance, load/scalability, security — **adapt** to your project. |
| **8.9** | Additional testing *(optional)* | e.g. API smoke tests, accessibility checklist, STT if tested. |
| **8.10** | Limitations of the testing process | Honest limits (data size, no formal load test, etc.). |
| **8.11** | Chapter summary | Short recap + link to Ch 9 evaluation if useful. |

**User / usability testing:** The template’s **Chapter 8** does **not** have a dedicated “user testing” subsection; **Chapter 9 (Critical evaluation)** includes focus groups / usability-style content. If your rubric mentions “user testing,” place a **short** subsection under **8.9** *or* cross-reference **§9.x** so examiners see it.

---

## Suggested content for CrackInt (fill as you write)

### 8.1 Overview
- Goals: validate **résumé NER**, **job-poster NER**, **end-to-end web app** behaviour against **FRs/NFRs**.
- One paragraph: testing happens at **model** (offline notebooks + metrics) and **system** (API + UI against SRS).

### 8.2 Testing criteria
- **Model:** entity-level NER (seqeval), held-out test sets, definitions of P/R/F1.
- **Functional:** black-box against **FR** IDs from SRS (auth, CV pipeline, job extract, sessions, match, …).
- **Non-functional:** security (JWT), usability/accessibility notes, performance *as feasible* (e.g. response time informal, or “not load-tested in scope”).

### 8.3 Model testing
- **Résumé NER:** data split, metrics — **mirror or cite Chapter 7 Table 7.2** (`THESIS-FACTS-SHEET`: 3023 docs, 2418/302/303, test F1 ~0.78 micro). Optional: per-entity discussion (SKILL vs OCCUPATION harder, etc.).
- **Job-poster NER:** **mirror or cite Table 7.4** (6327 postings, 5061/632/634, test micro ~0.85, seqeval ~0.854).
- **How metrics are computed:** seqeval, BIO → entity, ignore padding; one short paragraph.
- **Confusion / error analysis (optional but good):** 1 paragraph or small table of common failure modes (no full confusion matrix required unless you have it).

### 8.4 Benchmarking
- If **SkillSpan** or public data was used for job posters, cite **literature / reported F1** and compare **qualitatively** (different schema/split → “not directly comparable”).
- If no clean benchmark: state **limitation** + **ablation** idea (e.g. weighted sampling helped) as “comparison to simpler baseline” if you ran one; otherwise **honest scope statement**.

### 8.5 Further evaluations (optional)
- Qualitative samples (good/bad extractions), or LLM session behaviour smoke tests — only if you have evidence.

### 8.6 Results discussion
- Tie numbers to **research questions / objectives** (e.g. “NER supports skill-gap feature”).
- Compare résumé vs job model **difficulty** (e.g. SKILLS_REQUIRED F1 lower).

### 8.7 Functional testing
- **Table:** Test ID | FR ref | Scenario | Expected | Actual | Pass/Fail.
- **Pass rate:** e.g. “**X%** of **N** tests passed.”
- Point to **Appendix** for full case list (template expectation).
- Use `IMPLEMENTED-VS-PENDING-FINAL.md` / Swagger to ensure claims match the build.

### 8.8 Non-functional testing
- Map to SRS NFRs: e.g. **security** (HTTPS, JWT, password hashing — describe *what you checked*), **usability** (React/Radix, responsive — manual walkthrough), **reliability** (feature flags, error codes).  
- **Performance:** be honest (manual timing, browser devtools, or “not formally load-tested”).

### 8.9 Optional additional testing
- API integration tests, STT path, or accessibility checklist.

### 8.10 Limitations
- e.g. no large-scale user study, no formal penetration test, NER on noisy PDFs, LLM costs limit stress testing.

### 8.11 Summary
- 1 short paragraph; “testing supports claims in Implementation (Ch 7) and sets up Critical evaluation (Ch 9).”

---

## Evidence to gather before writing

| Evidence | Where |
|----------|--------|
| NER numbers (frozen) | `THESIS-FACTS-SHEET.md`, Ch 7 Tables 7.2 & 7.4 |
| FR list + IDs | SRS (Ch 4 in template) |
| What is implemented | `IMPLEMENTED-VS-PENDING-FINAL.md` |
| Screenshots for functional tests | Same environment as Ch 7 figures |

---

## Page budget

First **100 pages** (Intro → Conclusion) count for marking — keep Ch 8 **tight**: **tables + short discussion**, push long test case lists to **appendix**.

---

*End of plan. Create `chapter-08-testing-DRAFT.md` when you are ready to paste into Word.*
