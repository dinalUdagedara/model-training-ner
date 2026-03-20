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
| Dataset / file               | e.g. merged JSONL name                                |
| Train / val / test counts    |                                                       |
| Entity types                 | NAME, EMAIL, SKILL, OCCUPATION, EDUCATION, EXPERIENCE |
| Micro F1 (test)              |                                                       |
| Per-entity F1 (if in thesis) | paste table or “see Table X”                          |
| Model / pipeline             | Word2Vec + BiLSTM-CRF (Path 2)                        |
| Path 2 notebook (Appendix A) | exact `.ipynb` filename as submitted                  |


---

## Job poster NER


| Field                     | Value                                 |
| ------------------------- | ------------------------------------- |
| Training data note        | e.g. SkillSpan limitation if relevant |
| Metrics (if reported)     |                                       |
| Fallback behaviour in app | resume NER if job model not loaded    |


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
| Next question (LLM)        | yes          | needs `SESSION_QA_AGENT_ENABLED` + API key |
| Evaluate answer            | yes          |                                            |
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