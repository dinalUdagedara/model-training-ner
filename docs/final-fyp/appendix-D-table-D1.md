# Appendix D — Table D.1 (narrow layout for Word)

Use **Table D.1** in portrait; **Scenario** merges preconditions and steps. Fill **Table D.1b** for actual observations. Align FR IDs with Chapter 04 and Chapter 08 §8.7.

**Test count:** **FT-01–FT-09** are the **core** matrix (same as Chapter 08 Table 8.3). **FT-10–FT-17** are **extended** API/integration tests. Report pass rate for **core only** (denominator 9), **extended only** (denominator 8), or **all** (denominator 17)—pick one and use it consistently in Chapter 08.

---

## Table D.1 — Functional test summary (compact)


| **Test ID** | **FR(s)**     | **Scenario (preconditions and main steps)**                                                        | **Expected outcome**                                                           | **Pass / Partial / Fail** |
| ----------- | ------------- | -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | ------------------------- |
| **FT-01**   | **FR01**      | **Register: submit valid email and password (no prior account).**                                  | **User created; success or redirect to login.**                                |                           |
| **FT-02**   | **FR02**      | **Login; protected GET without JWT, then with Bearer (user from FT-01).**                          | **Denied without token; success with valid JWT.**                              |                           |
| **FT-03**   | **FR04**      | **Logged in; NER per Appendix G. POST résumé extract (PDF or text).**                              | **HTTP 200; JSON includes NAME, EMAIL, SKILL, etc.**                           |                           |
| **FT-04**   | **FR05**      | **Saved résumé. PATCH entities; GET same resource.**                                               | **Updates persisted.**                                                         |                           |
| **FT-05**   | **FR06–FR07** | **Logged in if required. POST job extract (text or PDF).**                                         | **HTTP 200; job entities or documented fallback.**                             |                           |
| **FT-06**   | **FR08–FR11** | **Logged in; optional OPENAI_API_KEY. Session; chat/message; evaluate if LLM on.**                 | **Messages stored; feedback when LLM on. Partial OK if HTTP 503 without key.** |                           |
| **FT-07**   | **FR14**      | **At least one session. GET sessions; refresh UI.**                                                | **List matches DB; survives refresh.**                                         |                           |
| **FT-08**   | **—**         | **Résumé + job posting IDs. POST skill-gap / match (your route).**                                 | **JSON skill-gap structure.**                                                  |                           |
| **FT-09**   | **FR15**      | **Logged in. GET readiness or home-summary.**                                                      | **Non-error dashboard payload.**                                               |                           |
| **FT-10**   | **NFR13**     | **No auth. GET** `/api/v1/health` **(or** `/health` **per deployment).**                           | **HTTP 200; service up.**                                                      |                           |
| **FT-11**   | **FR18**      | **Logged in. GET current user profile (**`/api/v1/auth/me` **or equivalent).**                     | **HTTP 200; user payload matches account.**                                    |                           |
| **FT-12**   | **FR18**      | **Logged in. GET list of résumés for user.**                                                       | **HTTP 200; list structure (may be empty).**                                   |                           |
| **FT-13**   | **FR06–FR07** | **Logged in. Create job posting (POST), then GET by id or list.**                                  | **Created record persisted; retrieval matches.**                               |                           |
| **FT-14**   | **FR15**      | **Logged in; optional history. GET readiness trend (e.g.** `/users/me/readiness/trend`**).**       | **HTTP 200; trend payload or documented empty state.**                         |                           |
| **FT-15**   | **—**         | **Logged in;** `CV_SCORING_ENABLED` **and API key if testing. POST résumé CV score (your route).** | **Score payload or HTTP 403/503 when disabled. Partial without LLM.**          |                           |
| **FT-16**   | **—**         | **Logged in; cover-letter feature enabled. GET/POST cover letter per API (or documented skip).**   | **Documented response or 403/503. Partial without LLM.**                       |                           |
| **FT-17**   | **NFR13**     | **Browser: open** `/api/v1/docs` **(Swagger).**                                                    | **OpenAPI UI loads; routes listed.**                                           |                           |


---

## Table D.1b — Actual observations (optional)


| Test ID | Actual observed (HTTP code, key fields, or UI) | Notes |
| ------- | ---------------------------------------------- | ----- |
| FT-01   |                                                |       |
| FT-02   |                                                |       |
| FT-03   |                                                |       |
| FT-04   |                                                |       |
| FT-05   |                                                |       |
| FT-06   |                                                |       |
| FT-07   |                                                |       |
| FT-08   |                                                |       |
| FT-09   |                                                |       |
| FT-10   |                                                |       |
| FT-11   |                                                |       |
| FT-12   |                                                |       |
| FT-13   |                                                |       |
| FT-14   |                                                |       |
| FT-15   |                                                |       |
| FT-16   |                                                |       |
| FT-17   |                                                |       |


---

## Optional tests (edge / environment) — add to D.1b or separate row if needed


| Test ID | FR(s)        | Scenario                                                       | Expected                               |
| ------- | ------------ | -------------------------------------------------------------- | -------------------------------------- |
| FT-18   | FR03         | Upload résumé at or near `MAX_UPLOAD_SIZE_MB` boundary.        | Handled per config (200 or clear 4xx). |
| FT-19   | Google OAuth | `POST` Google auth **only if** `GOOGLE_CLIENT_ID` is set.      | Token exchange or documented N/A.      |
| FT-20   | —            | Optional image upload to S3 **only if** AWS bucket configured. | 200 or documented 503 when off.        |


---

**Pass rate (after execution)**

- **Core only (FT-01–FT-09):** ___ / 9 = ___%
- **Extended (FT-10–FT-17):** ___ / 8 = ___%
- **All mandatory rows (FT-01–FT-17):** ___ / 17 = ___%

Use the same figures in Chapter 08 §8.7 (state which denominator you use).