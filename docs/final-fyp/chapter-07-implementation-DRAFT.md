# Chapter 07: Implementation (thesis draft — paste into Word)

**Student:** Udagedara Thiyunu Dinal Bandara | **ID:** W1998730  
**Project:** CrackInt — AI-driven personalized interview preparation platform  

**How to use:** Copy sections into your final thesis `.docx`. Apply template styles (Chapter heading ALL CAPS 16pt, etc.). Replace `[Figure X]` with your exported diagrams/screenshots. Align figure numbers with your List of Figures.

**Thesis wording:** In the main chapters, describe **what** was built (e.g. “Path 2 training notebook”, “data merge scripts”). Put **exact filenames, USB/CD contents, or repository links** in **Appendix A** (or your department’s *Project Artefacts* / *Submission Checklist*)—do **not** paste internal machine paths like `model-traning-1:30/...` in the thesis body.

**Sample thesis alignment:** The structure follows the same pattern as a strong FPR (e.g. Pansilu Wijesiri, *AMGAN*): **overview → technology selection (stack, languages, frameworks, libraries, IDE, summary) → core implementation (layered by subsystem) → UI implementation → challenges → summary**. Your project adds **authentication**, **LLM agents**, and **REST + optional WebSocket** components—reflect that in 7.3.

---

## CHAPTER 07: IMPLEMENTATION

### 7.1 Chapter overview

This chapter describes how the CrackInt system was implemented: how design decisions were turned into a working **full-stack** application. It begins with **technology selection**—frontend, backend, database, NLP inference, and optional cloud integrations—justified against the Software Requirements Specification (SRS). The **core implementation** covers **résumé NER** including **data preparation, model training** (Path 2 notebook, hyperparameters in Table 7.1, Word2Vec + BiLSTM + CRF loop), **deployment artefacts**, and **inference**; **job-poster** NER and text extraction; REST APIs under `/api/v1`; **JWT-based authentication**; **prep sessions** with message history; **LLM-backed** session question generation and answer evaluation (when enabled); **skill-gap analysis**; **readiness** aggregation; and optional **cover letter generation**, **CV scoring**, **speech-related** services, and **image uploads**. The **user interface** implementation summarises the Next.js App Router structure, dashboard modules, and integration with the backend. **Challenges** encountered during integration and deployment are discussed with mitigations. Detailed **quantitative evaluation** of models and functional tests is reserved for Chapter 08.

*[Optional: Insert Figure — high-level implemented architecture: Browser → Next.js → FastAPI → PostgreSQL / NER / LLM agents.]*

---

### 7.2 Technology selection

#### 7.2.1 Technology stack

CrackInt follows a **three-tier** pattern: **client** (browser), **application server** (FastAPI), and **data** (PostgreSQL), with **ML inference** (PyTorch-based NER) and **optional LLM** calls (OpenAI API) running inside the backend process. *[Insert Figure: technology stack diagram — self-composed or from Design chapter.]*

#### 7.2.2 Programming languages

| Language | Role | Rationale |
|----------|------|-----------|
| **Python 3.11+** | Backend, ML inference, agents | Ecosystem for FastAPI, PyTorch, Gensim (Word2Vec), and async database access; single language for API and NER. |
| **TypeScript** | Frontend | Type safety and maintainability for a growing Next.js codebase. |
| **SQL** | Schema / migrations | Expressed via SQLAlchemy/Alembic migrations for PostgreSQL. |

#### 7.2.3 Development frameworks

| Framework | Role | Rationale |
|-----------|------|-----------|
| **FastAPI** | REST API | Automatic OpenAPI documentation, async request handling, Pydantic validation. |
| **Next.js** (App Router) | Web UI | Server and client components, routing, and deployment-friendly structure. |
| **PyTorch** | NER inference | Loads trained Word2Vec + BiLSTM + CRF weights for token-level prediction. |

#### 7.2.4 Libraries and toolkits (selected)

**Backend (from `pyproject.toml`):** `fastapi`, `uvicorn`, `pydantic`, `pydantic-settings`, `sqlmodel`, `sqlalchemy[asyncio]`, `asyncpg`, `alembic`, `python-jose[cryptography]`, `passlib[bcrypt]`, `openai`, `torch`, `pytorch-crf`, `gensim`, `pymupdf`, `pillow`, `pytesseract`, `python-socketio`, `boto3`, `google-auth`, etc.

**Frontend (from `package.json`):** `next` **16.1.6**, `react` **19.2.3**, `@tanstack/react-query`, `axios`, Radix UI primitives, `tailwindcss` **4.x**, `next-themes`, `recharts`, `socket.io-client`, etc.

#### 7.2.5 Integrated development environments (IDEs)

Development used **Visual Studio Code** or **Cursor** (or equivalent) with Python and TypeScript language support, integrated terminals for Poetry/npm, and access to FastAPI **Swagger UI** at `/api/v1/docs` for API verification.

#### 7.2.6 Summary of technology selection

The stack prioritises **modularity** (routers per domain), **maintainability** (typed APIs and ORM models), **security** (hashed passwords, JWT), and **extensibility** (feature flags for LLM and NER paths). This aligns with NFRs for structured design and OpenAPI documentation.

---

### 7.3 Core functionalities implementation

#### 7.3.1 Dataset and résumé NER model

The résumé NER component uses a **merged annotated corpus** built during **data preparation** (combining and harmonising multiple sources—see Step 1 below) with a standard **train / validation / test** split. Entity types follow **BIO** tagging for **NAME**, **EMAIL**, **SKILL**, **OCCUPATION**, **EDUCATION**, and **EXPERIENCE**.

The deployed model is **Word2Vec + BiLSTM + CRF** only. The backend loads weights from `ner_config.json` and checkpoint files under `RESUME_NER_LOAD_DIR` (e.g. local path or bundled artefacts). Hybrid **rule-based** extraction supplements **NAME** and **EMAIL** for robustness.

**Training workflow (not inference only):** This section documents both **training** and **deployment** so examiners can follow the full lifecycle from data to inference. The steps below match the **Path 2 Jupyter notebook** developed for this FYP (exact filename listed in **Appendix A: Project artefacts**).

**Step 1 — Data consolidation and labels.** Multiple public and project-specific sources (e.g. Dotin-style XML, Label Studio exports, merged JSONL) are **normalised** to the six entity types above. **Python scripts** written for data merging map heterogeneous labels onto a **unified schema**, build **word-level** token sequences, and assign **BIO** tags using character-span annotations (tokenisation and span alignment are implemented in the Path 2 training notebook). The merged dataset used for the final experiments is a single **JSONL** file on the order of **~4k** annotated résumés—state the **final filename and document count** in Chapter 08 and/or Appendix A to match your frozen run.

**Step 2 — Train / validation / test split.** The merged corpus is split **80% / 10% / 10%** (train / validation / test) with a fixed **random seed** (e.g. 42) after shuffling, as implemented in the Path 2 notebook; **exact counts** should match the table you report in Chapter 08.

**Step 3 — Path 2 (production NER): Word2Vec + BiLSTM + CRF.** The **final chosen résumé model** for this FYP is **Path 2**, implemented in the **Path 2 training notebook** (Jupyter). That notebook carries out:

1. **Word2Vec** (Gensim) trained on **resume-token sentences** from the corpus to obtain static embeddings and a **word → id** vocabulary.  
2. A **PyTorch** `Word2VecBiLSTMCRF`-style model: embeddings → **BiLSTM** sequence encoder → **linear emission scores** → **CRF** loss (`pytorch-crf` / `torchcrf`) for structured prediction.  
3. **Mini-batch training** with `DataLoader` (shuffle, padding mask, **CRF negative log-likelihood**), **optimizer steps** (`zero_grad` → forward loss → `backward` → `step`), and **epoch** loops until convergence or a stopping criterion.  
4. **Evaluation** with **seqeval** (entity-level precision / recall / F1), aligned with Chapter 08.  
5. **Artifact export:** e.g. `word2vec.model`, `bilstm_crf_state.pt`, **`word2id` / embedding dimensions** in a **JSON config** consumed by the backend so the **`Word2VecBiLSTMCRF`** class in the résumé NER module can reload weights.

Numeric defaults (**256**-dim embeddings, **384** hidden, **768** max length) match Table 7.1; **confirm** against your saved `ner_config.json` if you retuned the notebook.

**Step 4 — Optimisation during training (Path 2 notebook).** The reference implementation uses **validation F1** (via **seqeval**) after each epoch, **learning-rate scheduling** (warmup with reduced factor, then **linear decay** toward a lower end factor), **gradient clipping** on the global norm, and **early stopping**: training stops if validation F1 does not improve for **`PATIENCE`** consecutive epochs, and the **best** weights (by validation F1) are **restored** before test evaluation. Exact integers are listed in Table 7.1 below.

**Step 5 — Deployment.** Trained weights (`word2vec.model`, `bilstm_crf_state.pt`, etc.) and the **NER configuration file** are placed on the deployment host (environment variable **`RESUME_NER_LOAD_DIR`** in the implementation). The backend loads the **Word2Vec + BiLSTM + CRF** stack through the **`Word2VecBiLSTMCRF`** implementation in the résumé NER service. No retraining is performed at inference time.

##### Detailed résumé NER training (Path 2 notebook)

The **authoritative training procedure** for the final résumé model is the **Path 2 Jupyter notebook** submitted with this project (see **Appendix A** for the notebook filename and any version note). The notebook:

- Loads the **merged JSONL** dataset (the implementation prefers the largest merged file available, then falls back to smaller merged files if needed—record which file your **final** run used in Appendix A / Chapter 08).  
- Applies a **label-mapping** table so all annotations use the unified entity types, then builds word-level sentences and **BIO** tags using **tokenisation with character positions** and **fixed BIO assignment** from spans.  
- Runs the pipeline described in the steps and Table 7.1 below.

**Data split (early section of the notebook).** `random.seed(42)`; shuffle index; **80%** train, **10%** validation, **10%** test. The notebook prints **Train / Val / Test** counts—**report those integers** in Chapter 08 alongside your metrics table.

**Word2Vec (embedding section).** Gensim **`Word2Vec`** is trained on **all tokenised sentences** from the corpus with the settings in Table 7.1. A **`word2id`** map includes **`<PAD>`** and **`<UNK>`**; rows of the **embedding matrix** are filled from Word2Vec vectors where a word exists in the Gensim vocabulary, otherwise a **small Gaussian** draw (so rare or unseen words still get a trainable row in the embedding table).

**Model architecture.** **`BiLSTMCRF`**: learned embedding matrix → **two-layer bidirectional LSTM** (see Table 7.1 for hidden size and dropouts) → linear emissions → **`pytorch-crf` CRF** (`batch_first=True`). The training objective is **CRF negative log-likelihood**.

**Training loop.** For each epoch: set the model to training mode; for each batch—pad word ids and labels to the batch max length, build a **mask**, compute loss, **back-propagate**, **clip gradients**, **optimiser step**; then **learning-rate scheduler step**; compute **validation micro-averaged F1**; track **best F1** and optionally **early-stop**. After training, the notebook saves **`word2vec.model`**, a PyTorch **state dict**, and a **JSON config** (`tags`, `word2id`, `embed_dim`, `num_labels`, `max_len`) for backend loading.

**Table 7.1 — Path 2 résumé NER: hyperparameters (as implemented in the Path 2 training notebook; Appendix A)**

| Category | Setting |
|----------|---------|
| **Sequence length** | `MAX_LEN = 768` (truncate/pad word sequences) |
| **Word2Vec** | `vector_size = 256`, `window = 6`, `min_count = 1`, `epochs = 35`, `workers = 4` |
| **BiLSTM** | `HIDDEN_DIM = 384`, **2** LSTM layers, **bidirectional**, `batch_first=True`; LSTM dropout **0.2** (as in class definition) |
| **Other regularisation** | Additional dropout **0.35** passed into the model wrapper (see notebook instantiation line) |
| **Optimiser** | `Adam`, learning rate **1e-3**, weight decay **5e-5** |
| **Batch size** | Train **6**, validation **12** (test loader **12**)—tuned for GPU memory (notebook comment references T4) |
| **Max epochs** | **120** |
| **Early stopping** | `PATIENCE = 25` (epochs without val-F1 improvement) |
| **LR schedule** | `SequentialLR`: **warmup** segment (`ConstantLR`, factor **0.1**) then **linear decay** (end factor **0.15**); `warmup_epochs = max(2, EPOCHS // 15)` |
| **Gradient clipping** | Global norm **2.0** |
| **Evaluation (during training)** | **seqeval** `f1_score` on validation (entity-level); full **classification report** on test after best checkpoint |

*If you change any constant in the notebook for your final run, update this table to match the run you report in Chapter 08.*

**Table 7.X — Example test-set metrics (entity-level F1; adjust to your frozen evaluation)**

| Entity | Precision | Recall | F1 |
|--------|-----------|--------|-----|
| NAME | *…* | *…* | *…* |
| EMAIL | *…* | *…* | *…* |
| SKILL | *…* | *…* | *…* |
| OCCUPATION | *…* | *…* | *…* |
| EDUCATION | *…* | *…* | *…* |
| EXPERIENCE | *…* | *…* | *…* |
| **Micro average** | *…* | *…* | **0.79** *(example — confirm from your notebook)* |

*[Insert Figure: BiLSTM-CRF architecture — reuse from Design chapter or from materials submitted with the project.]*

#### 7.3.2 Job-poster NER and text extraction

**Job descriptions** are accepted as **raw text** or **PDF** via `POST /api/v1/jobs/extract`. When `JOB_POSTER_NER_LOAD_DIR` is configured, job-specific entity types (e.g. **JOB_TITLE**, **COMPANY**, **SKILLS_REQUIRED**, …) are produced; otherwise the pipeline **falls back** to the résumé NER model so the endpoint remains usable in all environments.

**Text extraction** uses **PyMuPDF** for PDFs and **Tesseract** (via Pillow) for image-based pages where applicable; maximum upload size is governed by configuration (e.g. `MAX_UPLOAD_SIZE_MB`).

#### 7.3.3 Backend API and domain modules

The backend is organised under `app/`:

| Area | Path / module | Responsibility |
|------|----------------|----------------|
| **API routers** | `app/api/` | Versioned REST under `/api/v1`: `auth`, `resumes`, `jobs`, `job_posting`, `session`, `match`, `users`, `cover_letter`, `stt`, `uploads`, `health`. |
| **Authentication** | `app/api/auth/`, `app/auth/` | Registration, login, Google ID token exchange, JWT issuance, password hashing. |
| **ML** | `app/ml/` | `resume_ner.py`, `job_poster_ner.py` — load models, run inference, hybrid post-processing. |
| **Agents** | `app/agents/` | Session Q&A, CV scoring, cover letter, entity validation, résumé–job fit — orchestrate OpenAI calls when flags allow. |
| **Services** | `app/services/` | Text extraction, OCR, S3 uploads, domain services. |
| **Persistence** | `app/models.py`, Alembic | Users, résumés, job postings, prep sessions, messages, etc. |

**Representative endpoints** (full list in the project’s **OpenAPI** documentation and/or **Appendix A**):

- Résumé: extract, list, get, patch entities, optional CV **score**.
- Jobs: extract.
- Job postings: CRUD for authenticated users.
- Sessions: create, list, messages, **next question**, **evaluate answer** (LLM-gated).
- Match: **skill-gap** between a stored résumé and job posting.
- Users: **readiness**, summary, trend, **home-summary** for dashboard cards.

**Configuration:** Feature behaviour is controlled via environment variables (e.g. `SESSION_QA_AGENT_ENABLED`, `CV_SCORING_ENABLED`, `OPENAI_API_KEY`, NER model directories). When a feature is disabled or keys are missing, the API returns documented error codes (e.g. 503) rather than failing silently.

#### 7.3.4 Novel, adapted, and third-party code

The marking scheme (and strong FYP reports such as the sample *AMGAN* dissertation) expect **explicit identification** of **novel** implementation work, **adapted** code, and **third-party** libraries with sources. Table 7.Y summarises CrackInt at a high level; longer or generated code can be placed in **Appendix** with file references.

**Table 7.Y — Code provenance (representative)**

| Component | Classification | Notes / source |
|-----------|----------------|----------------|
| **Word2Vec + BiLSTM + CRF** (`Word2VecBiLSTMCRF`) | **Novel** (project-specific) | Designed and trained for résumé/job tasks; PyTorch module and Path 2 training notebook (Appendix A). |
| **`parse_resume_hybrid()` and rule-based NAME/EMAIL** | **Novel** | Heuristic merge of model output with regex/heuristics for robustness. |
| **REST API routers, agents, DB models** | **Novel** | Application logic for CrackInt (FastAPI routes, session flow, skill-gap, readiness). |
| **CRF decoding** | **Third-party** | `pytorch-crf` / `torchcrf` (cite library in references). |
| **Word2Vec training** | **Third-party** | Gensim `Word2Vec` (cite library in references). |
| **JWT auth pattern** | **Adapted** | Standard Bearer-token validation; `python-jose`, Passlib bcrypt—cite docs. |
| **FastAPI / Next.js / React Query** | **Third-party** | Framework usage per official documentation (not copied). |
| **OpenAI client calls (agents)** | **Adapted** | Official `openai` SDK; prompts and orchestration are **novel** project work. |

#### 7.3.5 Illustrative code excerpts

The following excerpts show **main implementation methods** at critical boundaries: **NER hybrid inference** and **authenticated API access**. Line numbers refer to the backend codebase at the time of writing.

**Listing 7.1 — Hybrid résumé entity extraction (core NER path)**  
*Source: résumé NER module (`resume_ner.py`)*

```python
def parse_resume_hybrid(text: str) -> Dict[str, List[str]]:
    """
    Extract entities from resume text: rules for NAME/EMAIL, model for SKILL, EXPERIENCE, EDUCATION, OCCUPATION.
    Returns a dict with keys NAME, EMAIL, SKILL, OCCUPATION, EDUCATION, EXPERIENCE (lists of strings).
    """
    text = text.strip()
    if not text:
        return _empty_entities()

    if not is_model_loaded():
        return _normalize_entities(_stub_entities(text))

    rn = _extract_name_heuristic(text)
    re_list = _extract_email_rules(text)
    _, _, entities = _parse_resume(text)
    if rn:
        entities["NAME"] = rn
    if re_list:
        entities["EMAIL"] = re_list

    base = _empty_entities()
    for k in base:
        base[k] = entities.get(k, [])
    return _normalize_entities(base)
```

This method implements the **hybrid strategy** described in the design chapter: **deterministic rules** for high-precision fields and **neural NER** for domain entities, followed by **`_normalize_entities`** for deduplication and punctuation stripping.

**Listing 7.2 — JWT-protected route dependency**  
*Source: API dependencies module (`deps.py`)*

```python
async def get_current_user(
    request: Request,
    session: AsyncSession = Depends(get_db),
) -> User:
    """Require a valid Bearer JWT and return the corresponding User. Raises 401 if missing or invalid."""
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = auth[7:].strip()
    payload = decode_token(token)
    sub = payload.get("sub")
    if not sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        user_id = uuid.UUID(sub)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalars().one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
```

Protected routes **depend** on `get_current_user`, enforcing **FR02**-style access control for user-scoped resources.

**Further code:** Session question generation and answer evaluation are implemented in the **session Q&A agent** module (LLM prompts and message persistence); cite **OpenAI** API usage in references. **Appendix** may include additional snippets (e.g. skill-gap JSON shape, migration id) if required by the assessor—avoid pasting **pages** of boilerplate in the main chapter.

#### 7.3.6 Frontend implementation

The frontend uses the **Next.js App Router**. Key routes include **login** and **register** (`app/login`, `app/register`) and a **dashboard** group (`app/(dashboard)/`) with pages for **CV upload**, **CV score**, **job upload**, **job postings**, **match**, **sessions** (list and chat), **cover letter**, **resumes**, and **admin**, consistent with the implemented APIs.

**State and API access:** Client modules call the backend using a configurable base URL (`NEXT_PUBLIC_API_URL`), typically with **Axios** or **fetch**, and **TanStack React Query** for caching and loading states. Responses follow the common wrapper `{ success, message, payload, meta }`.

**Charts:** **Recharts** supports readiness and trend visualisations where the UI presents analytics.

#### 7.3.7 Real-time and optional services

- **Speech:** Socket.IO handlers under the STT module integrate with optional **Amazon Transcribe**-related services for audio streaming (configuration-dependent).
- **Uploads:** Authenticated **image** upload to **S3** when bucket and credentials are set (`POST /api/v1/uploads/image`).

---

### 7.4 User interface implementation

#### 7.4.1 Frontend structure and screens

The UI is built with **React** components, **Tailwind CSS**, and **Radix**-based primitives for accessible dialogs, dropdowns, and forms. **next-themes** provides light/dark mode. Each major workflow (CV ingestion, job ingestion, practice session, readiness) maps to a dedicated route under the dashboard layout, with shared navigation (sidebar/layout) as implemented in `layout.tsx` and related components.

#### 7.4.2 Backend integration

The frontend attaches **Bearer tokens** to protected routes after login. Error responses are surfaced to the user via toasts or inline messages. File uploads use `multipart/form-data` for résumé/job PDFs and images as specified by the API.

#### 7.4.3 Accessibility and responsiveness

Semantic HTML, keyboard-focusable controls, and contrast-aware styling are applied following component library defaults; the layout is intended to be **responsive** across typical viewports (see non-functional testing in Chapter 08 for any formal checks).

---

### 7.5 Challenges and solutions

| Challenge | Solution |
|-----------|----------|
| **Large NER artefacts and environments** | Models loaded from local `RESUME_NER_LOAD_DIR`; optional Google Drive or archive download for deployment. |
| **Résumé vs job-poster NER** | Separate checkpoints and configs where job-poster NER is enabled; résumé endpoint uses Path 2 stack; single `parse_resume_hybrid` entry point for résumé text. |
| **Noisy PDFs / scans** | PyMuPDF extraction; OCR fallback; user can paste plain text. |
| **Long documents** | Token limits and truncation in the NER pipeline (e.g. max length 768 in Path 2). |
| **LLM cost and availability** | Feature flags and clear 503 responses when API keys or toggles are off. |
| **Cross-origin access** | CORS configured for the frontend origin during development and deployment. |
| **Schema evolution** | Alembic migrations version the database alongside releases. |

---

### 7.6 Chapter summary

This chapter presented the **implementation** of CrackInt: technology choices (Next.js, FastAPI, PostgreSQL, PyTorch NER, optional OpenAI agents), **dataset preparation and NER training** (Path 2 notebook, Table 7.1 hyperparameters, training loop and early stopping, export to `ner_config`/checkpoints), **dataset and NER metrics** (detailed evaluation in Chapter 08), **backend** modular routers and agents, **classification of novel vs adapted vs third-party** components, **illustrative code** for hybrid NER and JWT auth, **frontend** dashboard and integration patterns, and **challenges** faced during build-out. The system delivers an integrated pipeline from **résumé and job understanding** through **authenticated** practice sessions and **analytics-oriented** readiness APIs, with optional **LLM**-enhanced features controlled by configuration.

---

## Appendix for you (not in thesis): Sample thesis takeaways

**From the sample FPR (AMGAN — Chapter 07 style):**

1. **7.1** is one clear paragraph listing *what* the chapter contains (tech → core features → UI → challenges).  
2. **7.2** splits **stack**, **languages table**, **frameworks**, **libraries with rationale**, **IDE**, **short summary**.  
3. **7.3** breaks the **core system** into logical blocks (their: preprocessing + networks; yours: **data/NER + APIs + agents + UI integration**).  
4. **7.4** is dedicated to **UI + backend hookup + accessibility**.  
5. **7.5** is a **table** of challenges vs solutions (examiners like concrete rows).  
6. **7.6** is 1 short paragraph tying back to design and pointing forward to testing.

**Your extra edge:** Explicitly mention **auth**, **JWT**, **feature flags**, and **OpenAPI**—typical web+FYP markers.

**Gap closed vs first draft:** The sample thesis includes **short code listings** and **novel vs adopted** discussion; §7.3.4–7.3.5 now mirror that expectation (provenance table + `parse_resume_hybrid` + `get_current_user`).

**Appendix A (put in the real thesis Word file):** One page listing **project artefacts**—e.g. Path 2 notebook **filename**, merged dataset **filename**, backend/frontend zip or repo URL, **Swagger/OpenAPI** export if required. Chapter 7 references “Appendix A” instead of disk paths.

---

*End of draft. Update Table 7.X with your final frozen metrics; insert real figure numbers after placing images in Word.*
