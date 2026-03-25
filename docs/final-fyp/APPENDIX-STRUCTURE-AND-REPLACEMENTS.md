# Appendix structure — audit, fixes, and paste-ready skeletons

**Thesis:** CrackInt (W1998730) — align Word document with this map after you edit `w1998730_FYP.docx`.

---

## 1. What was wrong (from `w1998730_FYP-extracted.txt`)

| Issue | Detail |
|--------|--------|
| **Appendix A clash** | **TOC:** Appendix A = **Survey Results**. **Chapters 7–8** say “Appendix A” for **training notebooks, dataset filenames, frozen run, credentials** — that is **not** the survey appendix. |
| **Appendix B clash** | **§8.7** says full functional test tables may go in **Appendix B**, but **Appendix B** in your TOC is **Use Case Descriptions**, not test execution evidence. |
| **Missing letter** | TOC jumps **Appendix C → Appendix E** (no **Appendix D**). |

**Keep as correct (no change):** Pointers to **Appendix C** (stakeholders), **Appendix E** (findings), **Appendix F** (UI), **Appendix B** (use cases) where the text really means those sections.

---

## 2. Recommended final structure

| Appendix | Title (suggested) | Purpose |
|----------|-------------------|---------|
| **A** | Survey Results | **Unchanged** — online survey evidence. |
| **B** | Use Case Descriptions | **Unchanged** — UC-01 … UC-06. |
| **C** | Comprehensive Stakeholder Analysis | **Unchanged**. |
| **D** | Functional test cases and execution results | **NEW** — full FR test matrix, steps, pass/fail, pass rate % (template Ch.8 expects this in an appendix; do **not** overload Appendix B). |
| **E** | Detailed Findings Analysis | **Unchanged** (renumber only if you insert D before E in Word — **E stays E** if D is inserted between C and E). |
| **F** | UI Screenshots | **Unchanged**. |
| **G** | Project artefacts, datasets, and environment | **NEW** — frozen dataset **filenames**, training **`.ipynb`** names, exported **checkpoints** (`ner_config.json`, `.pt`, Word2Vec), **OpenAPI** note, **redacted** env var names (no secrets). Replaces all **wrong** “Appendix A” references in Ch.7–8 for technical artefacts. |
| **H** | Supplementary code listings | **NEW** — optional long **Listings** (Python/API) that are too large for Ch.7; short excerpts stay in Chapter 7. |

**Insert order in Word:** After fixing body text (below), add **Appendix D** and **Appendix G** and **Appendix H** before/after existing letters so the **alphabetical order** matches A–H. Update **Table of Contents** (right-click → Update field).

---

## 3. Word document — find / replace (manual, chapter by chapter)

**Do not** use “Replace all” on the whole thesis for `Appendix A` — you would break real references to **Survey = Appendix A**.

### 3a. Replace artefact / technical “Appendix A” → “Appendix G”

Apply in **Chapter 07** and **Chapter 08** (and **Chapter 09** if it says metrics align with Appendix A for artefacts). Typical strings from your extract:

- `see Appendix A for the filename` → `see Appendix G for the filename`
- `(see Appendix A for the exact filename` → `(see Appendix G for the exact filename`
- `job-poster NER training notebook (Appendix A)` → `… (Appendix G)`
- `frozen runAppendix A` → `frozen run — Appendix G)` *(fix spacing/typo at the same time)*
- `training notebooks (Appendix A)` → `training notebooks (Appendix G)`
- `Chapter 07 and Appendix A (frozen training run)` → `Chapter 07 and Appendix G (frozen training run)`
- `credentials (Appendix A)` → `credentials (Appendix G)`
- `consistent with Chapter 07, Appendix A, and the Abstract` → `… Chapter 07, Appendix G, and the Abstract` *(artefacts/metrics alignment; survey remains separate in Appendix A if you ever cite both, use “Appendices A and G”)*

**Leave unchanged** any sentence that clearly means the **survey questionnaire** (e.g. “survey in Appendix A”). Your current Ch.7 extract does **not** use Appendix A for the survey; the error is only technical.

### 3b. Replace functional-test “Appendix B” → “Appendix D”

In **§8.7** (functional testing):

- `may be placed in Appendix B` → `may be placed in Appendix D`

**Leave unchanged** “use cases … **Appendix B**” in Chapter 04 / SRS.

---

## 4. Paste-ready skeletons (create sections in Word)

### Appendix D — Functional test cases and execution results

**Intro paragraph (paste under heading):**  
This appendix lists functional test cases derived from the Software Requirements Specification (Chapter 04), with execution results against the deployed prototype (FastAPI backend and Next.js frontend). [State overall pass rate: X%.] Secrets (API keys) were redacted; tests requiring credentials are marked as partial or environment-dependent.

**Tables:** One row per test ID (e.g. FT-01 …), columns: Requirement / FR ID, Objective, Steps, Expected result, Actual result, Pass/Fail, Notes/screenshot ref.

---

### Appendix G — Project artefacts, datasets, and environment

**Intro paragraph:**  
This appendix lists frozen filenames and artefacts submitted with the project so that results in Chapters 7 and 8 can be reproduced without internal machine paths.

**Suggested subsections:**

- **G.1 Résumé NER** — Dataset file (line-delimited JSON): `merged_1030_plus_all_llm_plus_proper.json`; training notebook filename: *[paste exact `.ipynb` submitted]*; exports: `word2vec.model`, `bilstm_crf_state.pt`, `ner_config.json` (as submitted); train/val/test split: 3790 / 473 / 475 (seed 42); `MAX_LEN` 768 (align with facts sheet).
- **G.2 Job-poster NER** — Merged corpus: e.g. `merged_job_poster_ner_full_varied.json`; notebook: *[exact `.ipynb`]*; split 5061 / 632 / 634; `MAX_LEN` 512.
- **G.3 Application** — Repository / submission zip name; how to run API (e.g. `uvicorn`); link or note: OpenAPI/Swagger export if required.
- **G.4 Environment (redacted)** — Variable **names** only: e.g. `OPENAI_API_KEY`, `DATABASE_URL`, `RESUME_NER_LOAD_DIR` — **no values**.

---

### Appendix H — Supplementary code listings

**Intro paragraph:**  
This appendix contains supplementary code excerpts referenced from Chapter 7. Full source is included in the project submission archive.

**Listings:** Insert **Listing H.1, H.2, …** (Caption → New Label “Listing” if needed); monospace font; one listing per file excerpt; redact secrets.

Suggested items (choose 3–6): hybrid NER inference snippet; JWT dependency; `POST /sessions/{id}/chat` handler excerpt; `ner_config` load.

---

## 5. Repo files updated to match (drafts + facts sheet)

These repo files now say **Appendix G** for artefacts where they previously said Appendix A: `THESIS-FACTS-SHEET.md`, `chapter-07-implementation-DRAFT.md`, `chapter-08-testing-DRAFT.md`, `chapter-09-critical-evaluation-DRAFT.md`, `DATASET-PROVENANCE-SUMMARY.md`, `README.md`, `WORD-THESIS-STRUCTURE-ALIGNMENT.md`.

**Your Word thesis** must be updated manually (or paste from revised Ch.7/8 drafts).

---

## 6. Checklist before submission

- [ ] TOC lists **Appendices A through H** (or only those you include) in order.
- [ ] No remaining **artefact** pointer to “Appendix A” in Ch.7–8–9.
- [ ] **§8.7** points full test tables to **Appendix D**, not B.
- [ ] **Appendix G** contains real submitted notebook **filenames** (not repo-relative paths like `model-traning-1:30/...`).
- [ ] **Appendix H** (if used) has Listing captions and no secrets.
