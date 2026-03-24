# Thesis facts sheet (fill in — single source of truth for numbers)

**Instructions:** Update this as you freeze results. Everything you put in the **Abstract** and **Testing** chapter should match this file.

## Student / project


| Field          | Value                                      |
| -------------- | ------------------------------------------ |
| Name           | Udagedara Thiyunu Dinal Bandara            |
| ID (UoW / IIT) | W1998730                                   |
| Project title  | CrackInt — AI-driven interview preparation |
| Supervisor     | Pubudu Arachchige                          |


---

## Résumé NER (training + metrics)


| Field                        | Value                                                 |
| ---------------------------- | ----------------------------------------------------- |
| Dataset / file               | `merged_1030_plus_all_llm_plus_proper.json` (line-delimited JSON; frozen run) |
| Corpus size                  | **4738** résumés                                      |
| Train / val / test counts    | **3790 / 473 / 475** (seed 42)                        |
| Entity types                 | NAME, EMAIL, SKILL, OCCUPATION, EDUCATION, EXPERIENCE |
| Micro F1 (validation)        | **~0.86** (seqeval, frozen run)                       |
| Micro F1 (test)              | **0.83** (P 0.90, R 0.77)                             |
| Per-entity F1 (if in thesis) | see Ch 7 **Table 7.2** / notebook `classification_report` |
| Model / pipeline             | Word2Vec + BiLSTM-CRF (résumé NER); `MAX_LEN` **768** |
| Training notebook (Appendix A) | exact `.ipynb` filename as submitted (see repo)     |


---

## Job poster NER


| Field                     | Value                                 |
| ------------------------- | ------------------------------------- |
| Approach                  | Word2Vec + BiLSTM + CRF (same recipe as résumé NER; `MAX_LEN` **512**) |
| Dataset / file (frozen)   | e.g. `merged_job_poster_ner_full_varied.json` — **Appendix A** |
| Corpus size               | **6327** postings                     |
| Train / val / test        | **5061 / 632 / 634** (seed 42)       |
| Micro F1 (validation)     | **~0.89**                             |
| Micro F1 (test)           | **~0.85** (seqeval **~0.854**)       |
| Per-entity F1             | see Ch 7 **Table 7.4**               |
| Notebook (Appendix A)     | job-poster training `.ipynb` as submitted |
| Fallback behaviour in app | résumé NER if job model not loaded    |


---

## Application (FYP/PROJECT) — what to say is “implemented”

Check boxes when verified in running app + API docs.


| Feature                    | Implemented? | Notes / endpoint                           |
| -------------------------- | ------------ | ------------------------------------------ |
| Register / login / JWT     | yes          | `/api/v1/auth/...`                         |
| Google auth                | yes          |                                            |
| Résumé extract + edit      | yes          | `/resumes/...`                             |
| Job extract                | yes          | `/jobs/extract`                            |
| Job postings CRUD          | yes          | `/job-postings/...`                        |
| Sessions + messages        | yes          | `/sessions/...`                            |
| Chat turn (questions + eval + next Q) | yes | `POST /sessions/{id}/chat` — primary UI; needs `OPENAI_API_KEY` for LLM |
| Legacy split endpoints     | optional     | `next-question`, `evaluate-answer`, `send` — still in API; UI uses `/chat` |
| Skill-gap / match          | yes          | `/match/skill-gap`                         |
| Readiness / dashboard APIs | yes          | `/users/me/...`                            |
| CV score                   | yes          | `CV_SCORING_ENABLED` + API key             |
| Cover letter               | yes          | `/cover-letter/...`                        |
| STT                        | yes          | `/stt/...`                                 |


---

## Environment / demo for examiner


| Variable / note             | Value                                            |
| --------------------------- | ------------------------------------------------ |
| What works without OpenAI   |                                                  |
| What needs `OPENAI_API_KEY` |                                                  |
| NER dirs                    | `RESUME_NER_LOAD_DIR`, `JOB_POSTER_NER_LOAD_DIR` |


---

## Testing summary (for Ch 8)


| Type                      | Count / result      |
| ------------------------- | ------------------- |
| Automated tests run       |                     |
| Functional tests (manual) | pass rate: __%      |
| Model evaluation          | key table reference |


---

## Abstract draft numbers (final pass)

Paste the **three** quantitative phrases you will use (must match tables in Ch 8):