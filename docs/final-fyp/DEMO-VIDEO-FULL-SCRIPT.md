# CrackInt — FYP demo video: full read-aloud script

**Student:** Udagedara Thiyunu Dinal Bandara (W1998730) — adjust if needed.  
**How to use:** Read **bold cue lines** as stage directions only (do not read aloud). Speak everything else in a clear, steady pace. If you run **over 30 minutes**, shorten Part 3 by skipping one positive flow (e.g. P5 or P7) and one negative (e.g. N3).

---

## Opening (10–20 seconds)

**[SCREEN: title slide or browser on CrackInt login page]**

Hello. I am [your full name], student ID W1998730. This video is the final demonstration of my Final Year Project, **CrackInt** — an AI-driven personalised interview preparation platform. I will follow the required structure: first the problem and research gap, then the solution and technical design including a code walkthrough, and finally a live system demonstration with positive and negative test cases.

---

# PART 1 — Problem and research gap (about 3 to 5 minutes)

Many graduates and job seekers struggle to prepare for interviews in a way that is **structured**, **role-specific**, and **grounded in their own experience**. They often rely on generic question lists or general-purpose chat tools that are **not** tied to their actual curriculum vitae or to a **specific** job description they are targeting.

This matters for final-year students, career switchers, and anyone applying at high volume: preparation takes **time**, and feedback is not always **consistent** or **traceable** to the skills an employer actually asks for in the posting.

There is a **practice gap** between three kinds of tools. First, **résumé parsers** may extract text or entities but do not necessarily deliver **end-to-end interview coaching** linked to a job. Second, **practice Q and A applications** may simulate interviews but are often **generic** and not driven by **structured** understanding of both the candidate profile and the job text. Third, **large language models** alone can sound convincing but may **hallucinate** or drift without a clear link to **verified** structured fields from the user’s documents.

**CrackInt** addresses this gap by combining **named-entity recognition** for résumés and job postings, **skill-gap and matching** logic, **authenticated** practice **sessions** with optional **LLM-based** question generation and evaluation when configured, and **readiness-oriented** summaries for the dashboard — in **one** integrated full-stack system.

That is the motivation for the project. I will now describe how the solution is built and then demonstrate it running.

---

# PART 2 — Solution, technical design, and code walkthrough (about 8 to 12 minutes)

## 2.1 One-sentence solution

CrackInt is a **full-stack** web application: a **Next.js** front end talks to a **FastAPI** back end with **JWT authentication** and **PostgreSQL** persistence, while **PyTorch-based NER** models — **Word2Vec plus BiLSTM plus CRF** — extract structured entities from résumé and job text, and **optional OpenAI-backed agents** support session coaching when API keys and feature flags allow.

## 2.2 Architecture

On the **client**, the user works in the browser. The UI is implemented with **Next.js** using the App Router, **TypeScript**, and **Tailwind**-based components. Protected actions attach a **Bearer token** after login.

On the **server**, **FastAPI** exposes versioned REST APIs under `/api/v1`, with modular routers for **authentication**, **résumés**, **jobs**, **job postings**, **prep sessions**, **matching**, **users** readiness endpoints, and optional features such as **cover letter** or **CV scoring** depending on configuration. **OpenAPI** documentation is available at `/api/v1/docs`, which supports manual testing and examiner review.

**PostgreSQL** stores users, résumés, job-related entities, sessions, messages, and related analytics fields. **NER** weights load from environment variables such as **`RESUME_NER_LOAD_DIR`** and **`JOB_POSTER_NER_LOAD_DIR`** — do not show secret values on screen; exact filenames are in **Appendix G**.

The **machine learning** path for the submitted frozen runs uses **Gensim Word2Vec** for static word embeddings, a **bidirectional LSTM** encoder, and a **CRF** layer for structured **BIO** tagging, trained in the **submitted Jupyter notebook** (see below) and evaluated with **seqeval**, with test **micro F1** of approximately **zero point eight three** on the résumé test split and approximately **zero point eight five** on the job-poster test split, consistent with **Chapter Seven** and **Chapter Eight** of the report.

---

### Code walkthrough — exact files (open these before recording Part 2)

Paths below are **relative to your CrackInt backend project root** (the folder you zip for **FPC** submission — often named like `crackint-backend`). If a file is missing, use **Find in Files** in Cursor/VS Code for the **symbol name** in the right column.

| Step | File to open | Search (Ctrl/Cmd+F) or landmark | What you show on camera |
|------|----------------|----------------------------------|-------------------------|
| **A — Hybrid NER** | `app/ml/resume_ner.py` | `parse_resume_hybrid` | The **function definition** and the block where **rules** (name/email) merge with **model** output. Scroll slowly; 15–25 lines is enough. |
| **B — JWT** | `app/api/deps.py` | `get_current_user` | If not here, search the whole backend for **`get_current_user`** (sometimes `app/core/deps.py` or `app/dependencies.py`). Show where **Bearer** is parsed and **401** is raised. |
| **C — JWT helper (optional 20 s)** | `app/auth/jwt.py` (if present) | `decode` or `create_access_token` | Only if you have time: show **token encode/decode** without pasting secrets. Skip if redundant with B. |
| **D — Session / LLM (optional swap for C)** | Under `app/agents/` (exact `.py` name varies) | `chat.completions` or `OpenAI` | One short block where the session agent **builds messages** and calls the API — ties to **Listing 7.6** in the thesis. |
| **E — Training notebook** | In **this training repo:** `fyp/BiLSTM_CRF_Resume_NER_Path2_FYP.ipynb` | Notebook section headings | See **notebook map** below. |

**Résumé NER notebook — which cells to scroll to**

| Show | In file `fyp/BiLSTM_CRF_Resume_NER_Path2_FYP.ipynb` |
|------|-----------------------------------------------------|
| Model class | Markdown heading **“## 5. Model (BiLSTM-CRF)”** → code cell with **`class BiLSTMCRF`**. |
| Training loop | **“## 6. Training”** → cell with **`for epoch in range(EPOCHS)`** and **`clip_grad_norm`**. |
| Word-level inference | **“## 9. Inference”** → cell with **`def parse_resume_path2`**. |

*(Job-poster parallel notebook, if you mention it in speech: `fyp/job-poster-ner/BiLSTM_CRF_Job_Poster_NER_Path2_FYP.ipynb` — same **“## 5. Model”** pattern, `MAX_LEN = 512` in data cell.)*

---

## 2.3 Code walkthrough — hybrid résumé extraction

**[SCREEN: IDE — open `app/ml/resume_ner.py`, scroll to `parse_resume_hybrid`. Font 14–16 or zoom 125%.]**

I will now show a short excerpt from the **back-end** implementation. This function implements **hybrid** résumé entity extraction. **Heuristic rules** are used for high-confidence fields such as **name** and **email**, while the **neural NER model** predicts **skills**, **education**, **experience**, and **occupation**-style entities. The results are **merged** and **normalised** before the API returns them to the client. This design is intentional: rules improve **robustness** for structured contact fields, while the **BiLSTM–CRF** stack captures **contextual** spans in free text. I am not reading every line; the key idea is the **division of labour** between rules and the model and the **single entry point** the API uses for inference.

## 2.4 Code walkthrough — authentication

**[SCREEN: IDE — open `app/api/deps.py` at `get_current_user`, or the file where your search found it.]**

Next, a short excerpt related to **security**. This dependency reads the **Authorization** header, expects a **Bearer** token, **decodes** the JWT, resolves the **user id**, and loads the user from the database. If the token is missing or invalid, the API responds with **401 Unauthorized**. Protected routes **depend** on this function, which aligns with the functional requirement for **secure access** to user-specific resources.

## 2.5 Code walkthrough — training or inference (notebook)

**[SCREEN: Jupyter or VS Code preview — `fyp/BiLSTM_CRF_Resume_NER_Path2_FYP.ipynb` → section “## 5. Model (BiLSTM-CRF)” for `class BiLSTMCRF`; optionally scroll to “## 6. Training” or “## 9. Inference” for `parse_resume_path2`.]**

Finally, a brief look at the **training notebook** submitted with the project. Here you see the **BiLSTMCRF** module: embeddings, **LSTM** encoding, linear **emissions**, and **CRF** loss during training and **Viterbi-style decoding** at inference. The notebook also defines the **train–validation–test split** with **fixed seed**, **early stopping** on validation **F1**, and export of **`ner_config.json`** and checkpoints referenced in **Appendix G**. This links the **quantitative** results in the thesis to the **artefacts** you can inspect in the submission.

## 2.6 Swagger (quick)

**[SCREEN: browser — `http://your-host/api/v1/docs`. Scroll slightly.]**

Here is the **Swagger** interface listing representative endpoints: **authentication**, **résumé extraction**, **sessions**, and others. This satisfies **maintainability** and **reviewability** requirements and was used during **functional testing** recorded in **Appendix D** and **Chapter Eight**.

I will now move to the **live demonstration**.

---

# PART 3 — System demonstration (about 12 to 18 minutes)

**[SCREEN: browser — CrackInt. Use a test account prepared in advance.]**

## 3.1 Positive case P1 — Registration and login

I will first show **registration**. I enter a **valid email** and **password** and submit the form.

**[ACTION: register. Pause on success message or redirect.]**

The account is created. I now **log in** with the same credentials.

**[ACTION: login.]**

I am authenticated. From here on, **protected** areas of the application should only be available with a valid session or token.

## 3.2 Positive case P2 — Résumé extraction

I navigate to **résumé upload** or **extract** as implemented in my UI.

**[ACTION: upload sample PDF or paste text. Run extract.]**

The system returns **structured** fields — for example **name**, **email**, **skills**, **education**, and **experience** — populated from the **hybrid NER** pipeline described earlier. This supports **functional requirement** coverage for **entity extraction** from the curriculum vitae.

## 3.3 Positive case P3 — Edit and persist entities (if your UI supports it)

I will **adjust** one extracted field — for example a **skill** or **job title** line — and **save**.

**[ACTION: edit, save, refresh page.]**

After **refresh**, the change is still present, which shows **persistence** through the API and database.

## 3.4 Positive case P4 — Job text or job posting

I now demonstrate **job-side** understanding. I either **paste job description text** or create a **job posting** record, depending on my implemented flow.

**[ACTION: job extract or create posting.]**

The response includes **job-related** entities such as **title**, **company**, **location**, **skills required**, or similar, according to the **job-poster NER** schema, or a **documented fallback** if only the résumé model path is configured — as described in the thesis.

## 3.5 Positive case P5 — Skill-gap or match

I run **skill-gap** or **match** between a **stored résumé** and a **job posting**.

**[ACTION: select résumé and job, run match.]**

The UI or JSON shows **structured** comparison — for example **missing skills** or **alignment** — which closes the loop from **understanding both sides** to **actionable** preparation focus.

## 3.6 Positive case P6 — Prep session (message or chat)

I open or create a **prep session** and send a **user message** or trigger the **chat** turn as implemented.

**[ACTION: send message. If LLM enabled, wait for response.]**

**Messages** appear in **history**. If the **LLM** path is enabled and keys are present, the system returns a **question** or **feedback** payload in line with **Chapter Seven**. If I am demonstrating without keys, I will show the **graceful** behaviour in the **negative** section next.

## 3.7 Positive case P7 — Dashboard or readiness

I open the **dashboard**, **home summary**, or **readiness** view.

**[ACTION: navigate. Pause on charts or cards.]**

The page loads **without error** and displays **summary** or **trend** data from the **users** readiness endpoints, or a **valid empty state** for a new account.

---

## 3.8 Negative case N1 — Access without authentication

I will now show **security** behaviour. I **log out** or open an **incognito** window and attempt to open a **protected** route, or I call a protected endpoint **without** a Bearer token.

**[ACTION: show 401 in Swagger or redirect to login in UI.]**

As expected, access is **denied** — **401** in the API or **redirect** to login in the UI — which confirms **JWT protection**.

## 3.9 Negative case N2 — Invalid login

I attempt to log in with a **wrong password**.

**[ACTION: failed login.]**

The application shows a **clear error** and does **not** expose internal stack traces to the user.

## 3.10 Negative case N3 or N4 — Invalid input or unavailable LLM (pick what applies)

**Option A — bad input:** I attempt an **empty** upload or an **oversized** file if safe to demonstrate.

**[ACTION: trigger validation error.]**

The system responds with a **client error** such as **four hundred bad request** or a **validation** message, not an unhandled crash.

**Option B — LLM unavailable:** I attempt a session feature that requires **OpenAI** when the key is **missing** or the feature is **disabled**.

**[ACTION: trigger 503 or explanatory message.]**

The response is a **documented partial** outcome — consistent with **Appendix D** and **Chapter Eight** — rather than a silent failure.

## 3.11 Negative case N5 — Minimal job text (optional, short)

I submit a **very short** job description.

**[ACTION: extract.]**

The system still returns a **stable** response — possibly sparse entities — without breaking the session.

---

# CLOSING (about 30 to 60 seconds)

**[SCREEN: neutral — thesis title or thank-you slide]**

To conclude: **CrackInt** delivers an **integrated** pipeline from **structured résumé and job understanding** through **matching** and **authenticated practice sessions** to **readiness-oriented** feedback, with **quantified NER performance** and **functional** validation as reported in the thesis. **Future work** could include deeper **multilingual** support, **formal usability studies**, and **load testing** for scalability claims.

Thank you for watching this demonstration.

---

## After recording

- Watch once with a **stopwatch**. If **over thirty minutes**, cut **Part 3** optional blocks **P5**, **P7**, or **N5** first.  
- Replace bracketed **[ACTION]** steps with **your** exact button names.  
- **Blur** any accidental **keys** or **personal data** in post-production if needed.

