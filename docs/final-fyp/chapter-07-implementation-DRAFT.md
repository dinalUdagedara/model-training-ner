# Chapter 07: Implementation (thesis draft — paste into Word)

**Student:** Udagedara Thiyunu Dinal Bandara | **ID:** W1998730  
**Project:** CrackInt — AI-driven personalized interview preparation platform  

**How to use:** Copy sections into your final thesis `.docx`. Apply template styles (Chapter heading ALL CAPS 16pt, etc.). Replace `[Figure X]` with your exported diagrams/screenshots. Align figure numbers with your List of Figures.

**Thesis wording:** In the main chapters, describe **what** was built (e.g. “résumé NER training notebook”, “data merge scripts”). Put **exact filenames, USB/CD contents, or repository links** in **Appendix G** (or your department’s *Project Artefacts* / *Submission Checklist*)—do **not** paste internal machine paths like `model-traning-1:30/...` in the thesis body.

**Sample thesis alignment:** The structure follows the same pattern as a strong FPR (e.g. Pansilu Wijesiri, *AMGAN*): **overview → technology selection (stack, languages, frameworks, libraries, IDE, summary) → core implementation (layered by subsystem) → UI implementation → challenges → summary**. Your project adds **authentication**, **LLM agents**, and **REST + optional WebSocket** components—reflect that in 7.3.

---

## CHAPTER 07: IMPLEMENTATION

### 7.1 Chapter overview

This chapter describes how the CrackInt system was implemented: how design decisions were turned into a working **full-stack** application. It begins with **technology selection**—frontend, backend, database, NLP inference, and optional cloud integrations—justified against the Software Requirements Specification (SRS). The **core implementation** covers **résumé NER** including **data preparation, model training** (Jupyter training notebook—Appendix G; hyperparameters and split sizes in Table 7.1; indicative test metrics in Table 7.2; Word2Vec + BiLSTM + CRF loop), **deployment artefacts**, and **inference**; **job-poster NER** using the **same overall methodology** as résumé NER (Word2Vec + BiLSTM + CRF; **Tables 7.3–7.4**, §7.3.2) plus text extraction; REST APIs under `/api/v1`; **JWT-based authentication**; **prep sessions** with message history; **LLM-backed** session question generation and answer evaluation (when enabled); **skill-gap analysis**; **readiness** aggregation; and optional **cover letter generation**, **CV scoring**, **speech-related** services, and **image uploads**. The **user interface** implementation summarises the Next.js App Router structure, dashboard modules, and integration with the backend. **Challenges** encountered during integration and deployment are discussed with mitigations. Detailed **quantitative evaluation** of models and functional tests is reserved for Chapter 08.

*[Optional: Insert Figure — high-level implemented architecture: Browser → Next.js → FastAPI → PostgreSQL / NER / LLM agents.]*

---

### 7.2 Technology selection

#### 7.2.1 Technology stack

CrackInt follows a **three-tier** pattern: **client** (browser), **application server** (FastAPI), and **data** (PostgreSQL), with **ML inference** (PyTorch-based NER) and **optional LLM** calls (OpenAI API) running inside the backend process. *[Insert Figure: technology stack diagram — self-composed or from Design chapter.]*

#### 7.2.2 Programming languages


| Language         | Role                          | Rationale                                                                                                      |
| ---------------- | ----------------------------- | -------------------------------------------------------------------------------------------------------------- |
| **Python 3.11+** | Backend, ML inference, agents | Ecosystem for FastAPI, PyTorch, Gensim (Word2Vec), and async database access; single language for API and NER. |
| **TypeScript**   | Frontend                      | Type safety and maintainability for a growing Next.js codebase.                                                |
| **SQL**          | Schema / migrations           | Expressed via SQLAlchemy/Alembic migrations for PostgreSQL.                                                    |


#### 7.2.3 Development frameworks


| Framework                | Role          | Rationale                                                                     |
| ------------------------ | ------------- | ----------------------------------------------------------------------------- |
| **FastAPI**              | REST API      | Automatic OpenAPI documentation, async request handling, Pydantic validation. |
| **Next.js** (App Router) | Web UI        | Server and client components, routing, and deployment-friendly structure.     |
| **PyTorch**              | NER inference | Loads trained Word2Vec + BiLSTM + CRF weights for token-level prediction.     |


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

**Training workflow (not inference only):** This section documents both **training** and **deployment** so examiners can follow the full lifecycle from data to inference. The steps below match the **résumé NER training notebook** (Jupyter) developed for this FYP (exact filename listed in **Appendix G: Project artefacts**).

**Step 1 — Data consolidation and labels.** Multiple public and project-specific sources (e.g. Dotin-style XML, Label Studio exports, merged JSONL) are **normalised** to the six entity types above. **Python scripts** written for data merging map heterogeneous labels onto a **unified schema**, build **word-level** token sequences, and assign **BIO** tags using character-span annotations (tokenisation and span alignment are implemented in that training notebook). The merged dataset for the **frozen submitted run** comprised **4738** annotated résumés (line-delimited JSON, file: `merged_1030_plus_all_llm_plus_proper.json` in the training workflow); the exact filename can also be listed in **Appendix G**. If you merge additional data later, update this count everywhere it appears (abstract, Ch 7, Ch 8).

**Step 2 — Train / validation / test split.** The merged corpus is split **80% / 10% / 10%** (train / validation / test) with **random seed 42** after shuffling. For the frozen run: **3790** train, **473** validation, **475** test—**use the same figures** in Chapter 08 with your metrics tables.

**Step 3 — Résumé NER model: Word2Vec + BiLSTM + CRF.** The **final résumé NER model** for this FYP is implemented in the **résumé NER training notebook** (Jupyter). That notebook carries out:

1. **Word2Vec** (Gensim) trained on **resume-token sentences** from the corpus to obtain static embeddings and a **word → id** vocabulary.
2. A **PyTorch** `Word2VecBiLSTMCRF`-style model: embeddings → **BiLSTM** sequence encoder → **linear emission scores** → **CRF** loss (`pytorch-crf` / `torchcrf`) for structured prediction.
3. **Mini-batch training** with `DataLoader` (padding mask, **CRF negative log-likelihood**), `**WeightedRandomSampler`** on the training set to **oversample** sentences containing rarer entity types (e.g. EDUCATION, EXPERIENCE, OCCUPATION), **optimizer steps** (`zero_grad` → forward loss → `backward` → `step`), and **epoch** loops until early stopping or max epochs.
4. **Evaluation** with **seqeval** (entity-level precision / recall / F1), aligned with Chapter 08.
5. **Artifact export:** e.g. `word2vec.model`, `bilstm_crf_state.pt`, `**word2id` / embedding dimensions** in a **JSON config** consumed by the backend so the `**Word2VecBiLSTMCRF`** class in the résumé NER module can reload weights.

Deployed `**max_len**` and embedding/hidden sizes must match `**ner_config.json**` exported with the checkpoint (for the frozen run these align with Table 7.1).

**Step 4 — Optimisation during training.** The training notebook uses **validation F1** (via **seqeval**) after each epoch, **learning-rate scheduling** (warmup with reduced factor, then **linear decay** toward a lower end factor), **gradient clipping** on the global norm, and **early stopping**: training stops if validation F1 does not improve for `**PATIENCE`** consecutive epochs, and the **best** weights (by validation F1) are **restored** before test evaluation. Exact integers are listed in Table 7.1 below.

**Step 5 — Deployment.** Trained weights (`word2vec.model`, `bilstm_crf_state.pt`, etc.) and the **NER configuration file** are placed on the deployment host (environment variable `**RESUME_NER_LOAD_DIR`** in the implementation). The backend loads the **Word2Vec + BiLSTM + CRF** stack through the `**Word2VecBiLSTMCRF`** implementation in the résumé NER service. No retraining is performed at inference time.

##### Detailed résumé NER training (notebook)

The **authoritative training procedure** for the final résumé model is the **résumé NER training notebook** (Jupyter) submitted with this project (see **Appendix G** for the filename and any version note). The notebook:

- Loads the **merged** line-delimited JSON file used for training (see **Appendix G** for the exact filename used in the frozen run).  
- Applies a **label-mapping** table so all annotations use the unified entity types, then builds word-level sentences and **BIO** tags using **tokenisation with character positions** and **fixed BIO assignment** from spans.  
- Runs the pipeline described in the steps and Table 7.1 below.

**Data split (early section of the notebook).** `random.seed(42)`; shuffle index; **80% / 10% / 10%**. The frozen run yielded **3790 / 473 / 475**—keep Chapter 08 consistent with these counts.

**Word2Vec (embedding section).** Gensim `**Word2Vec`** is trained on **all tokenised sentences** from the corpus with the settings in Table 7.1. A `**word2id`** map includes `**<PAD>**` and `**<UNK>**`; rows of the **embedding matrix** are filled from Word2Vec vectors where a word exists in the Gensim vocabulary, otherwise a **small Gaussian** draw (so rare or unseen words still get a trainable row in the embedding table).

**Model architecture.** `**BiLSTMCRF`**: learned embedding matrix → **one bidirectional LSTM layer** (see Table 7.1 for hidden size and dropout) → linear emissions → `**pytorch-crf` CRF** (`batch_first=True`). The training objective is **CRF negative log-likelihood** (mean over the batch).

**Training loop.** For each epoch: set the model to training mode; for each batch—pad word ids and labels to the batch max length, build a **mask**, compute loss, **back-propagate**, **clip gradients**, **optimiser step**; then **learning-rate scheduler step**; compute **validation micro-averaged F1**; track **best F1** and **early-stop** when validation F1 does not improve for `**PATIENCE`** epochs (frozen run stopped around epoch **47**). After training, the notebook saves `**word2vec.model`**, a PyTorch **state dict**, and a **JSON config** (`tags`, `word2id`, `embed_dim`, `num_labels`, `max_len`) for backend loading.

The following **listings** show the **core training logic** inline (abbreviated from the résumé NER training notebook; variable names may match your submitted file). They complement Table 7.1, which collects hyperparameter **values**.

**Listing 7.1 — Train / validation / test split (illustrative)**  
*After building `all_sents` and `all_labels` from the merged JSONL.*

```python
n = len(all_sents)
random.seed(42)
idx = list(range(n))
random.shuffle(idx)
n_train, n_val = int(0.8 * n), int(0.1 * n)
train_sents = [all_sents[i] for i in idx[:n_train]]
val_sents = [all_sents[i] for i in idx[n_train : n_train + n_val]]
test_sents = [all_sents[i] for i in idx[n_train + n_val :]]
# same indexing for train_labels, val_labels, test_labels
```

**Listing 7.2 — BIO tags from character-span annotations (illustrative)**  
*Each token is `(text, start, end)`; annotations carry unified labels and `points` with `start`/`end`.*

```python
def create_bio_tags_fixed(tokens, annotations):
    bio = ["O"] * len(tokens)
    for ann in annotations:
        if not ann.get("label") or ann["label"][0] == "O":
            continue
        entity = ann["label"][0]
        for pt in ann.get("points", []):
            s, e = pt["start"], pt["end"]
            first = True
            for i, (_, ts, te) in enumerate(tokens):
                if te <= s or ts >= e:
                    continue
                bio[i] = f"B-{entity}" if first else f"I-{entity}"
                first = False
    return bio
```

**Listing 7.3 — Inner training loop with gradient clipping (illustrative)**  
*Assumes `model(ids, mask, labels)` returns CRF negative log-likelihood; tensors are moved to `device` in the notebook.*

```python
model.train()
for ids, mask, lab in train_loader:
    ids, mask, lab = ids.to(device), mask.to(device), lab.to(device)
    optimizer.zero_grad()
    loss = model(ids, mask, lab)
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=2.0)
    optimizer.step()
# then: scheduler.step(); validation F1; early stopping on best checkpoint
```

**Table 7.1 — Résumé NER (Word2Vec + BiLSTM + CRF): hyperparameters (frozen Colab run; training notebook—Appendix G)**


| Category                 | Setting                                                                                                                                                                     |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Corpus**               | **4738** résumés after merge; split **3790** / **473** / **475** (train / val / test), seed **42**                                                                          |
| **Sequence length**      | `MAX_LEN = 768` (truncate/pad word sequences; stored in `ner_config.json`)                                                                                                  |
| **Word2Vec**             | `vector_size = 256`, `window = 6`, `min_count = 1`, `epochs = 35`, `workers = 4`                                                                                            |
| **Vocabulary**           | **~47.4k** word types (incl. `<PAD>`, `<UNK>`) in the frozen run                                                                                                            |
| **BiLSTM**               | `HIDDEN_DIM = 384`, **2** BiLSTM layers, **bidirectional**, `batch_first=True`; LSTM dropout **0.2**                                                                        |
| **Other regularisation** | Dropout **0.35** on embedding and LSTM outputs (see model class)                                                                                                            |
| **Sampling**             | `WeightedRandomSampler`: weight **2.5** for sentences containing selected rare BIO tags (EDUCATION, EXPERIENCE, OCCUPATION), else **1.0**                                   |
| **Optimiser**            | `Adam`, learning rate **1e-3**, weight decay **5e-5**                                                                                                                       |
| **Batch size**           | Train **6**, validation **12**, test **12**                                                                                                                                 |
| **Max epochs**           | **120**                                                                                                                                                                     |
| **Early stopping**       | `PATIENCE = 25` (epochs without val-F1 improvement); best checkpoint restored                                                                                               |
| **LR schedule**          | `SequentialLR`: **warmup** (`ConstantLR`, factor **0.1**) then **linear decay** (end factor **0.15**); `warmup_epochs = max(2, EPOCHS // 15)`                               |
| **Gradient clipping**    | Global norm **2.0**                                                                                                                                                         |
| **Evaluation**           | **seqeval** on validation each epoch; **classification report** + **F1** on test set after training (**val** micro F1 **~0.86**, **test** micro F1 **~0.83**—see Table 7.2) |


*If you retrain with different constants, replace this table and Table 7.2 so the thesis matches the notebook output you submit.*

**Table 7.2 — Test-set metrics (entity-level; seqeval `classification_report`, frozen run)**

*Test split: **475** résumés. Values rounded to two decimals; full precision in notebook log.*


| Entity            | Precision | Recall | F1       |
| ----------------- | --------- | ------ | -------- |
| NAME              | 0.99      | 0.93   | 0.96     |
| EMAIL             | 1.00      | 0.93   | 0.96     |
| SKILL             | 0.92      | 0.79   | 0.85     |
| OCCUPATION        | 0.73      | 0.58   | 0.65     |
| EDUCATION         | 0.84      | 0.72   | 0.77     |
| EXPERIENCE        | 0.89      | 0.67   | 0.77     |
| **Micro average** | 0.90      | 0.77   | **0.83** |


**Validation** (same run, before early stop): micro F1 **~0.86** (see notebook). Repeat the same tables in **Chapter 08** if that chapter is the primary results location—**numbers must match** the abstract and `THESIS-FACTS-SHEET.md`.

*[Insert Figure: BiLSTM-CRF architecture — reuse from Design chapter or from materials submitted with the project.]*

#### 7.3.2 Job-poster NER and text extraction

**Job descriptions** are accepted as **raw text** or **PDF** via `POST /api/v1/jobs/extract`. When `**JOB_POSTER_NER_LOAD_DIR`** is configured, **job-specific** entities are produced; otherwise the pipeline **falls back** to the **résumé** NER weights so the endpoint still returns structured fields in all environments.

**Parallel methodology to résumé NER (§7.3.1).** Job-poster NER was implemented using the **same engineering pattern**, adapted to job text:

1. **Data** — Job postings are collected or merged into a **line-delimited JSON** corpus (content + span annotations), with preparation scripts under the **job-poster data pipeline** (see **Appendix G** for merge filename and provenance).
2. **Labels** — Annotations are mapped to a **job-specific BIO tagset** (distinct from résumé entities): **JOB_TITLE**, **COMPANY**, **LOCATION**, **SALARY**, **SKILLS_REQUIRED**, **EXPERIENCE_REQUIRED**, **EDUCATION_REQUIRED**, **JOB_TYPE**.
3. **Model** — **Word2Vec** (Gensim) + **BiLSTM** + **CRF** (`BiLSTMCRF`), trained in the **job-poster NER training notebook** (Appendix G), evaluated with **seqeval**, exported to `**word2vec.model`**, `**bilstm_crf_state.pt**`, `**ner_config.json**` (same artefact pattern as résumé NER). The frozen run used a **two-layer** BiLSTM in the notebook class definition and `**MAX_LEN = 512`** word tokens—**align** `ner_config.json` with deployment.
4. **Inference** — The API loads checkpoints from `**JOB_POSTER_NER_LOAD_DIR`** when set. The notebook also demonstrates **hybrid** parsing (e.g. combining rules with the model for robust **SALARY** / entity extraction); mirror the behaviour implemented in `**job_poster_ner.py`**.

**Tables 7.3 and 7.4** summarise the **frozen Colab run** for job-poster NER (same role as **Tables 7.1–7.2** for résumés). Repeat or cross-reference these figures in **Chapter 08** if that chapter is the primary results discussion.

**Table 7.3 — Job-poster NER (Word2Vec + BiLSTM + CRF): hyperparameters (frozen Colab run; training notebook—Appendix G)**


| Category                 | Setting                                                                                                                                                                           |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Corpus**               | **6327** job postings (merged file; e.g. `merged_job_poster_ner_full_varied.json` in the frozen run—**Appendix G**); split **5061 / 632 / 634** (train / val / test), seed **42** |
| **Sequence length**      | `MAX_LEN = 512` (truncate/pad word sequences)                                                                                                                                     |
| **Word2Vec**             | `vector_size = 256`, `window = 6`, `min_count = 1`, `epochs = 35`, `workers = 4`                                                                                                  |
| **Vocabulary**           | **~10.1k** word types (incl. `<PAD>`, `<UNK>`) in the frozen run                                                                                                                  |
| **BiLSTM**               | `HIDDEN_DIM = 384`, **2** LSTM layers, **bidirectional**, `batch_first=True`; LSTM dropout **0.2**                                                                                |
| **Other regularisation** | Dropout **0.35** on embedding and LSTM outputs (see model class)                                                                                                                  |
| **Sampling**             | `WeightedRandomSampler`: weight **3.5** for sentences containing at least one **entity** BIO tag (vs **1.0** for all-`O` lines), to reduce collapse to all-`O` predictions        |
| **Optimiser**            | `Adam`, learning rate **5e-4**, weight decay **5e-5**                                                                                                                             |
| **Batch size**           | Train **8**, validation **12**, test **12**                                                                                                                                       |
| **Max epochs**           | **80**                                                                                                                                                                            |
| **Early stopping**       | `PATIENCE = 20`; best checkpoint by validation F1 restored (frozen run stopped ~epoch **65**)                                                                                     |
| **LR schedule**          | Warmup (`ConstantLR`, factor **0.1**) then **linear decay** (end factor **0.15**); `warmup_epochs = max(2, EPOCHS // 15)`                                                         |
| **Gradient clipping**    | Global norm **2.0**                                                                                                                                                               |
| **Evaluation**           | **seqeval** on validation each epoch; **classification report** on test after training (**val** micro F1 **~0.89**, **test** micro F1 **~0.85**—Table 7.4)                        |


*If you retrain with different constants, update this table and Table 7.4 together.*

**Table 7.4 — Job-poster NER: test-set metrics (entity-level; seqeval `classification_report`, frozen run)**

*Test split: **634** postings. Values rounded to two decimals.*


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


**Validation** (same run): micro F1 **~0.89**. **Test** seqeval F1 **~0.854** (see notebook log). Keep **résumé** and **job-poster** tables consistent with `THESIS-FACTS-SHEET.md` and the abstract.

**Text extraction** uses **PyMuPDF** for PDFs and **Tesseract** (via Pillow) for image-based pages where applicable; maximum upload size is governed by configuration (e.g. `MAX_UPLOAD_SIZE_MB`).

#### 7.3.3 Backend API and domain modules

The backend is organised under `app/`:


| Area               | Path / module                | Responsibility                                                                                                                                     |
| ------------------ | ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| **API routers**    | `app/api/`                   | Versioned REST under `/api/v1`: `auth`, `resumes`, `jobs`, `job_posting`, `session`, `match`, `users`, `cover_letter`, `stt`, `uploads`, `health`. |
| **Authentication** | `app/api/auth/`, `app/auth/` | Registration, login, Google ID token exchange, JWT issuance, password hashing.                                                                     |
| **ML**             | `app/ml/`                    | `resume_ner.py`, `job_poster_ner.py` — load models, run inference, hybrid post-processing.                                                         |
| **Agents**         | `app/agents/`                | Session Q&A, CV scoring, cover letter, entity validation, résumé–job fit — orchestrate OpenAI calls when flags allow.                              |
| **Services**       | `app/services/`              | Text extraction, OCR, S3 uploads, domain services.                                                                                                 |
| **Persistence**    | `app/models.py`, Alembic     | Users, résumés, job postings, prep sessions, messages, etc.                                                                                        |


**Representative endpoints** (full list in the project’s **OpenAPI** documentation and/or **Appendix G**):

- Résumé: extract, list, get, patch entities, optional CV **score**.
- Jobs: extract.
- Job postings: CRUD for authenticated users.
- Sessions: create, list, messages, **next question**, **evaluate answer** (LLM-gated).
- Match: **skill-gap** between a stored résumé and job posting.
- Users: **readiness**, summary, trend, **home-summary** for dashboard cards.

**Configuration:** Feature behaviour is controlled via environment variables (e.g. `CV_SCORING_ENABLED`, `OPENAI_API_KEY`, NER model directories). The session QA agent is **always enabled** in deployment; LLM calls require provider credentials. When optional features are disabled or keys are missing, the API returns documented error codes (e.g. 503) rather than failing silently.

#### 7.3.4 Novel, adapted, and third-party code

The marking scheme (and strong FYP reports such as the sample *AMGAN* dissertation) expect **explicit identification** of **novel** implementation work, **adapted** code, and **third-party** libraries with sources. Table 7.Y summarises CrackInt at a high level. **Listings 7.1–7.6** in this chapter show **representative** implementation fragments; only **lengthy** boilerplate (e.g. full notebook cells, entire routers) need an **Appendix** if your assessor requests it.

**Table 7.Y — Code provenance (representative)**


| Component                                             | Classification               | Notes / source                                                                                                       |
| ----------------------------------------------------- | ---------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **Word2Vec + BiLSTM + CRF** (résumé + job-poster)     | **Novel** (project-specific) | Two trained stacks (entity schemas differ); PyTorch modules and training notebooks (Appendix G); **Tables 7.1–7.4**. |
| `**parse_resume_hybrid()` and rule-based NAME/EMAIL** | **Novel**                    | Heuristic merge of model output with regex/heuristics for robustness.                                                |
| **REST API routers, agents, DB models**               | **Novel**                    | Application logic for CrackInt (FastAPI routes, session flow, skill-gap, readiness).                                 |
| **CRF decoding**                                      | **Third-party**              | `pytorch-crf` / `torchcrf` (cite library in references).                                                             |
| **Word2Vec training**                                 | **Third-party**              | Gensim `Word2Vec` (cite library in references).                                                                      |
| **JWT auth pattern**                                  | **Adapted**                  | Standard Bearer-token validation; `python-jose`, Passlib bcrypt—cite docs.                                           |
| **FastAPI / Next.js / React Query**                   | **Third-party**              | Framework usage per official documentation (not copied).                                                             |
| **OpenAI client calls (agents)**                      | **Adapted**                  | Official `openai` SDK; prompts and orchestration are **novel** project work.                                         |


#### 7.3.5 Illustrative code excerpts (backend)

The following excerpts show **inference and security** in the deployed API. **Listings 7.1–7.3** above cover **résumé NER training**; here **Listings 7.4–7.6** cover **runtime** behaviour. Line numbers refer to the backend codebase at the time of writing.

**Listing 7.4 — Hybrid résumé entity extraction (core NER path)**  
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

This method implements the **hybrid strategy** described in the design chapter: **deterministic rules** for high-precision fields and **neural NER** for domain entities, followed by `**_normalize_entities`** for deduplication and punctuation stripping.

**Listing 7.5 — JWT-protected route dependency**  
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

**Listing 7.6 — LLM-backed session step (illustrative)**  
*Pattern used in the session Q&A agent: build messages from history, call the API, persist assistant text. Exact prompts and schemas match your implementation.*

```python
# Illustrative — align with your session_qa_agent (or equivalent) module.
response = await client.chat.completions.create(
    model="gpt-4o-mini",  # or configured model name
    messages=[
        {"role": "system", "content": system_prompt},
        *[{"role": m.role, "content": m.content} for m in recent_messages],
    ],
    temperature=0.4,
)
assistant_text = response.choices[0].message.content
# persist assistant_text to DB; return to client
```

Cite **OpenAI** (or your provider) in **References**. Skill-gap and other agents follow the same **orchestration** idea: validated inputs → model call → structured or free-text output → store or return.

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


| Challenge                                | Solution                                                                                                                                                                                    |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Large NER artefacts and environments** | Models loaded from local `RESUME_NER_LOAD_DIR`; optional Google Drive or archive download for deployment.                                                                                   |
| **Résumé vs job-poster NER**             | Separate checkpoints and configs where job-poster NER is enabled; the résumé endpoint uses the **Word2Vec + BiLSTM + CRF** model; single `parse_resume_hybrid` entry point for résumé text. |
| **Noisy PDFs / scans**                   | PyMuPDF extraction; OCR fallback; user can paste plain text.                                                                                                                                |
| **Long documents**                       | Truncation at `**MAX_LEN`** word tokens (e.g. **768** in the frozen run—Table 7.1); very long CVs may lose tail tokens unless split or post-processed.                                      |
| **LLM cost and availability**            | Feature flags and clear 503 responses when API keys or toggles are off.                                                                                                                     |
| **Cross-origin access**                  | CORS configured for the frontend origin during development and deployment.                                                                                                                  |
| **Schema evolution**                     | Alembic migrations version the database alongside releases.                                                                                                                                 |


---

### 7.6 Chapter summary

This chapter presented the **implementation** of CrackInt: technology choices (Next.js, FastAPI, PostgreSQL, PyTorch NER, optional OpenAI agents), **dataset preparation and NER training** (Jupyter notebooks—Appendix G; **Tables 7.1–7.2** résumé, **7.3–7.4** job-poster; **Listings 7.1–7.3** for split, BIO tagging, and training steps; export to `ner_config`/checkpoints), **dataset and NER metrics** (test F1 in Tables **7.2** and **7.4**; full discussion may also appear in Chapter 08), **backend** modular routers and agents, **classification of novel vs adapted vs third-party** components, **illustrative code** (**Listings 7.4–7.6**: hybrid NER, JWT, LLM session pattern), **frontend** dashboard and integration patterns, and **challenges** faced during build-out. The system delivers an integrated pipeline from **résumé and job understanding** (including **parallel NER pipelines** for résumé and job-poster text where configured) through **authenticated** practice sessions and **analytics-oriented** readiness APIs, with optional **LLM**-enhanced features controlled by configuration.

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

**Gap closed vs first draft:** The sample thesis includes **short code listings** and **novel vs adopted** discussion; this chapter adds **Listings 7.1–7.3** (training), **7.4–7.6** (hybrid NER, JWT, LLM session pattern), plus Table 7.Y (provenance).

**Appendix G (put in the real thesis Word file):** One page listing **project artefacts**—e.g. résumé NER training notebook **filename** (`.ipynb`), merged dataset **filename**, backend/frontend zip or repo URL, **Swagger/OpenAPI** export if required. Chapter 7 references “Appendix G” instead of disk paths.

---

*End of draft. Renumber tables (7.1, 7.2, …) to match your Word template; insert real figure numbers after placing images in Word.*