# Resume & Job Poster NER Pipelines — Supervisor Meeting Brief

This document covers both NER pipelines in the FYP:

- **Resume NER:** [fyp/BERT_BiLSTM_CRF_Resume_NER_FYP.ipynb](BERT_BiLSTM_CRF_Resume_NER_FYP.ipynb) — extracts entities from CVs (NAME, EMAIL, SKILL, etc.).
- **Job Poster NER:** [fyp/job-poster-ner/BERT_BiLSTM_CRF_Job_Poster_NER_FYP.ipynb](job-poster-ner/BERT_BiLSTM_CRF_Job_Poster_NER_FYP.ipynb) — extracts entities from job descriptions (JOB_TITLE, COMPANY, SKILLS_REQUIRED, etc.).

Same architecture (BERT + BiLSTM + CRF) for both; different entity types and training data.

---

## 1. What the Pipeline Does

The notebook trains and evaluates a **Named Entity Recognition (NER)** model to extract structured information from resume text. Given raw resume text, it predicts which tokens belong to which entity types:

| Entity Type | Example |
| ----------- | ------- |
| NAME | "John Doe" |
| EMAIL | "john.doe@email.com" |
| SKILL | "Python", "Machine Learning" |
| OCCUPATION | "Software Engineer" |
| EDUCATION | "BSc Computer Science", "University of Colombo 2020" |
| EXPERIENCE | "Tech Corp", "5 years" |

---

## 2. Model Architecture: BERT + BiLSTM + CRF

### What It Is

A **3-layer stack**:

```
Input (Resume Text) → BERT Encoder → BiDirectional LSTM → CRF → BIO Tags per Token
```

- **BERT (bert-base-uncased):** 110M-parameter transformer encoder. Takes tokenized text, outputs context-aware embeddings (768-dim per subword).
- **BiLSTM:** 1-layer bidirectional LSTM (256 hidden units). Captures left–right context around each position.
- **CRF:** Decodes a globally consistent sequence of BIO labels (no invalid transitions like I-NAME after O).

### Why This Architecture?

1. **BERT:** Pre-trained on large corpora; captures grammar, semantics, and domain vocabulary. Fine-tuning adapts it to resume-specific patterns.
2. **BiLSTM:** Adds sequence modelling on top of BERT for NER-style span detection.
3. **CRF:** Enforces BIO rules (e.g. I-NAME only after B-NAME or I-NAME). This improves span-level coherence over per-token classification.

---

## 3. What BERT Does and Why We Chose It

### What BERT Does

- **Input:** Text tokens (subwords via WordPiece).
- **Output:** A 768-dimensional vector per token position. Each vector encodes context from the whole sentence (bidirectional attention).
- **Role here:** Replaces random or static embeddings with strong contextual representations before BiLSTM and CRF.

### Why BERT?

- Strong performance on NER in general.
- `bert-base-uncased` is widely used, well-supported, and fits typical Colab/GPU setups.
- Fine-tuning is straightforward: we keep the architecture and train on resume data.

---

## 4. Options Considered and Why We Chose the Current Selections

### 4.1 Encoder: BERT vs Alternatives

| Option | Pros | Cons | Why we chose BERT |
| ------ | ---- | ---- | ----------------- |
| **BERT (bert-base-uncased)** | Well-documented, strong NER baseline, fits Colab GPU, Hugging Face support | Slower than smaller models | **Chosen.** Best balance of performance, documentation, and Colab compatibility. Widely used in NER literature. |
| **RoBERTa** | Often slightly better on benchmarks | Larger, more compute, less NER-specific prior art in our setup | Rejected for now: marginal gains vs. extra complexity and training time. |
| **DistilBERT** | Faster, smaller (40% fewer params) | May sacrifice some F1; still need to validate on resume domain | Could revisit for production speed; for FYP we prioritised accuracy. |
| **ELECTRA** | Efficient pre-training, strong on some tasks | Fewer ready-made NER examples; newer, less standard | Rejected: BERT has more NER tutorials and established pipelines. |
| **spaCy NER** | Simple, fast, no GPU needed | Generic pre-trained models; weaker on resume-specific entities | Rejected: we need domain-specific fine-tuning on merged resume data. |
| **Word2Vec / GloVe + BiLSTM-CRF** | Lightweight, no transformer | Static embeddings; weaker context understanding | Rejected: BERT’s contextual embeddings significantly outperform static embeddings on NER. |

### 4.2 Decoder: CRF vs Alternatives

| Option | Pros | Cons | Why we chose CRF |
| ------ | ---- | ---- | ----------------- |
| **CRF** | Enforces valid BIO transitions; improves span coherence | Slightly more complex than softmax | **Chosen.** Prevents invalid sequences (e.g. I-NAME after O) and improves entity boundaries. |
| **Softmax (per-token)** | Simpler, faster | No transition constraints; more span errors | Rejected: CRF gives better entity-level consistency. |
| **Span-based / SpanBERT** | Explicit span prediction | Different architecture; different data format | Rejected: BIO + CRF is standard for our data format and easier to integrate. |

### 4.3 BiLSTM: Why Add It on Top of BERT?

| Option | Pros | Cons | Why we chose BERT + BiLSTM |
| ------ | ---- | ---- | -------------------------- |
| **BERT + BiLSTM** | BiLSTM adds local sequence modelling for NER; common in NER papers | Extra parameters and compute | **Chosen.** Improves span coherence and is a well-known pattern for token-level NER. |
| **BERT only (no BiLSTM)** | Simpler, fewer parameters | BERT’s [CLS] / token outputs may not optimally capture NER spans | Rejected: BiLSTM layer helps model sequential entity structure. |
| **BERT + Transformer layers** | More capacity | Heavier, more overfitting risk with ~1k resumes | Rejected: BiLSTM is lighter and sufficient for our data size. |

### 4.4 Optimizer and Schedule

| Option | Pros | Cons | Why we chose AdamW + warmup + decay |
| ------ | ---- | ---- | ----------------------------------- |
| **AdamW + warmup + linear decay** | Standard for BERT fine-tuning; stable | — | **Chosen.** Matches Hugging Face / BERT best practices. |
| **SGD** | Often generalises well | Needs more tuning; slower convergence | Rejected: AdamW is the de facto choice for BERT. |
| **Constant LR** | Simple | BERT fine-tuning benefits from warmup and decay | Rejected: risk of instability or suboptimal convergence. |

### 4.5 Data Split: 80/10/10

| Option | Pros | Cons | Why we chose 80/10/10 |
| ------ | ---- | ---- | --------------------- |
| **80/10/10** | Adequate val and test sets; common default | — | **Chosen.** Enough data for validation and final evaluation with ~1k resumes. |
| **90/5/5** | More training data | Smaller val/test; less reliable metrics | Rejected: validation size is important for early stopping. |
| **70/15/15** | Larger val/test | Less training data | Rejected: we prioritise training data for learning. |

### 4.6 Hybrid Inference: Rules for NAME/EMAIL

| Option | Pros | Cons | Why we chose hybrid |
| ------ | ---- | ---- | ------------------- |
| **Rules for NAME/EMAIL, model for rest** | Regex/heuristics are reliable for EMAIL; name often at top | Rules can fail on unusual formats | **Chosen.** High recall for NAME/EMAIL with rules; model focuses on harder entities. |
| **Model only** | Single system | Model sometimes misses obvious NAME/EMAIL | Rejected: rules give more stable extraction for these common entities. |
| **Rules for all** | No model needed | Impossible for SKILL, EDUCATION, EXPERIENCE (too varied) | Rejected: rules cannot generalise to arbitrary entities. |

---

## 5. Current Accuracy (Typical Numbers)

From CHANGES_AND_DECISIONS.md:

| Metric | Typical Value | Target |
| -------------------------- | ------------- | ------ |
| **Entity-level F1** (val) | ~52–53% | 80%+ |
| **Entity-level F1** (test) | ~47% | 80%+ |
| **Token accuracy** | ~87% | 80%+ |

Entity-level F1 (seqeval) is stricter: it requires correct span boundaries and labels. Token accuracy counts correct tokens only and is usually higher.

---

## 6. Logic and Methods Used to Increase Accuracy

### Already Implemented (in the FYP notebook)

1. **Differentiated learning rates** — BERT: 2e-5, BiLSTM+CRF: 1e-4
2. **Weight decay** — 0.01 for most parameters, 0 for bias and LayerNorm
3. **LR schedule** — Warmup (10% of epochs), linear decay to 20% of initial LR
4. **Early stopping** — Patience = 12 epochs; best model by val F1 restored at end
5. **Weighted random sampler** — Oversamples rare entities (EDUCATION, EXPERIENCE, OCCUPATION)
6. **Hybrid inference** — Rules for NAME/EMAIL, model for SKILL, OCCUPATION, EDUCATION, EXPERIENCE
7. **Hyperparameter changes** — EPOCHS: 60, PATIENCE: 12, Dropout: 0.3, higher LRs

---

## 7. What Is an Epoch? How It Works

### Definition

- **1 epoch** = one full pass over the entire training set.
- The model sees every training sample once; gradients are computed and parameters updated for each batch.

### What Happens Per Epoch

1. Shuffle training data
2. Split into batches (batch_size = 8)
3. For each batch: forward pass → loss → backward pass → optimizer step
4. Run validation; compute validation F1
5. If val F1 improves → save checkpoint
6. Step the LR scheduler

### What Happens When We Increase Epochs

| Effect | Explanation |
| ------ | ----------- |
| **Pros** | Model can learn longer; useful if F1 is still improving |
| **Cons** | Risk of overfitting; more compute time |
| **Mitigation** | Early stopping restores best checkpoint when val F1 stops improving |

---

## 8. How to Increase Accuracy Further

Yes, it is possible:

- **Data:** Merge more sources via prepare_data.py (e.g. --existing, --vrundag, --minhquan)
- **Training:** Try batch_size=16, more epochs (80), longer warmup, dropout 0.35
- **Class imbalance:** Add label weights in CRF loss for rare entities
- **Post-processing:** Known-skills list, strip punctuation, merge spans
- **Ensemble:** Train 2–3 models with different seeds; majority vote

---

## 9. Agent Pipeline to Correct Wrong Entities

### Concept

A second-stage **LLM/agent corrector**:

- **Input:** Raw resume text + extracted entities from NER
- **Role:** Detect and fix obvious errors (wrong type, missed span, noise)
- **Fallback:** If the agent fails or times out, use the NER output as-is

### Flow

1. Run NER → get entities
2. Send (raw text, entities) to an LLM/agent
3. Agent returns corrected entities if valid; otherwise fall back to NER output
4. Use final entities for matching, display, etc.

**Implementation:** `agent_corrector.py` implements this pipeline. Set `OPENAI_API_KEY` for LLM mode; otherwise only normalization is applied. Section 7b in the notebook demonstrates usage.

---

## 10. Data Pipeline Summary (Resume NER)

- **Source:** merged_resume_ner.json in Google Drive
- **Preparation:** resume_ner_pipeline/prepare_data.py merges existing 220 + Dotin 545 + optional vrundag91, minhquan
- **Schema:** NAME, EMAIL, SKILL, OCCUPATION, EDUCATION, EXPERIENCE, O
- **Split:** 80% train, 10% val, 10% test (seed 42)
- **Tagging:** BIO scheme; create_bio_tags_fixed ensures no B-O/I-O

---

## 11. Job Poster NER Pipeline

A second NER model for **job descriptions** (postings), using the same BERT-BiLSTM-CRF architecture. Used for CV–job matching and interview prep.

### Entity Types

| Entity Type | Example |
| ----------- | ------- |
| JOB_TITLE | "Senior Data Scientist" |
| COMPANY | "Tech Corp" |
| LOCATION | "Remote", "Colombo" |
| SALARY | "$80k–$120k" |
| SKILLS_REQUIRED | "Python", "Machine Learning" |
| EXPERIENCE_REQUIRED | "5+ years" |
| EDUCATION_REQUIRED | "BSc Computer Science" |
| JOB_TYPE | "Full-time", "Contract" |

### Data and Training

- **Source:** merged_job_poster_ner.json
- **Preparation:** job_poster_ner_pipeline/prepare_data.py merges JSONL files (SkillSpan, LREC 2022, etc.)
- **SkillSpan (NAACL 2022):** ~11,543 job-posting sentences; mainly SKILLS_REQUIRED (skill + knowledge) in the labels
- **Note:** Current SkillSpan data predominantly labels SKILLS_REQUIRED; JOB_TITLE, COMPANY, LOCATION, etc. may need additional datasets (e.g. LREC 2022) or rules (e.g. SALARY regex) for full coverage
- **Split:** 80/10/10, same BIO tagging as resume NER

### Notebooks

- **Training:** `job_poster_ner_pipeline/BERT_BiLSTM_CRF_Job_Poster_NER.ipynb` or `fyp/job-poster-ner/BERT_BiLSTM_CRF_Job_Poster_NER_FYP.ipynb`
- **Hybrid inference:** SALARY from rules (regex); rest from model (same pattern as NAME/EMAIL in resume NER)

### Relation to Resume NER

| Aspect | Resume NER | Job Poster NER |
| ------ | ---------- | --------------- |
| Architecture | BERT + BiLSTM + CRF | Same |
| Input | CV / resume text | Job description text |
| Output entities | NAME, EMAIL, SKILL, OCCUPATION, EDUCATION, EXPERIENCE | JOB_TITLE, COMPANY, LOCATION, SALARY, SKILLS_REQUIRED, EXPERIENCE_REQUIRED, EDUCATION_REQUIRED, JOB_TYPE |
| Backend config | `RESUME_NER_LOAD_DIR` | `JOB_POSTER_NER_LOAD_DIR` |
| Use case | Extract CV entities | Extract job poster entities; fallback to resume NER if job poster model not loaded |

---

## 12. Backend and Frontend (PROJECT Directory)

The trained NER models are integrated into the full application under:

**Path:** `FYP/PROJECT` (sibling to `model-traning-1:30`)

### Backend: `PROJECT/crackint-backend/`

| Component | Path | Role |
| --------- | ---- | ---- |
| Resume NER | `app/ml/resume_ner.py` | Loads model, exposes `parse_resume_hybrid`; entities: NAME, EMAIL, SKILL, OCCUPATION, EDUCATION, EXPERIENCE |
| Job Poster NER | `app/ml/job_poster_ner.py` | Loads model, exposes `parse_job_poster_hybrid`; entities: JOB_TITLE, COMPANY, LOCATION, SALARY, SKILLS_REQUIRED, etc. |
| Resume API | `app/api/resume/` | Extract entities from uploaded/pasted CVs (uses resume NER) |
| Job API | `app/api/job/` | Extract entities from job descriptions; uses **job poster NER** when `JOB_POSTER_NER_LOAD_DIR` is set, else **fallback to resume NER** |
| Resume model download | `scripts/download_resume_ner_model.py` | Downloads resume NER from Hugging Face |
| GDrive download | `scripts/download_resume_ner_from_gdrive.py` | Fetches resume NER from Google Drive |

**Config:** In `.env` set `RESUME_NER_LOAD_DIR=./model/resume_ner` and optionally `JOB_POSTER_NER_LOAD_DIR=./model/job_poster_ner`.

### Frontend: `PROJECT/crackint-frontend/`

| Component | Path | Role |
| --------- | ---- | ---- |
| CV upload / paste | `app/cv-upload/`, `components/cv-upload/` | Upload PDF or paste text; trigger extraction |
| Entity display / edit | `components/cv-upload/EditEntitiesDialog.tsx` | Shows extracted entities; user can edit |
| Home dashboard | `app/`, `components/home-dashboard/` | Chat input, file upload, summary views; job description upload uses job poster NER |
| API client | `services/resume-uploader.service.ts` | Calls backend extract endpoints |

### Flow

- **CV extraction:** User uploads/pastes CV → Resume API → `parse_resume_hybrid` → entities (NAME, EMAIL, SKILL, etc.)
- **Job extraction:** User uploads/pastes job description → Job API → `parse_job_poster_hybrid` (if job poster model loaded) or `parse_resume_hybrid` (fallback) → entities (JOB_TITLE, COMPANY, SKILLS_REQUIRED, etc.)

---

## 13. Quick Supervisor Q&A

| Question | Answer |
| -------- | ------ |
| What is the model? | BERT-base-uncased + BiLSTM + CRF |
| Why BERT over RoBERTa/DistilBERT/spaCy? | Best balance of performance, docs, Colab compatibility; spaCy/static embeddings weaker on domain-specific entities |
| Why CRF over softmax? | CRF enforces valid BIO transitions; improves span coherence |
| Why BiLSTM on top of BERT? | Adds sequence modelling for NER spans; standard pattern in token-level NER |
| Current accuracy? | ~52% val F1, ~47% test F1, ~87% token accuracy |
| Target? | 80%+ entity-level F1 |
| Main improvement lever? | More training data; then tuning (batch size, epochs, dropout) |
| Agent pipeline? | Second-stage LLM corrector to fix entity errors; fallback to NER output |
| Where is backend/frontend? | `PROJECT/crackint-backend/` and `PROJECT/crackint-frontend/`; Resume NER in `app/ml/resume_ner.py`, Job Poster NER in `app/ml/job_poster_ner.py` |
| Job Poster NER? | Same architecture (BERT-BiLSTM-CRF); extracts JOB_TITLE, COMPANY, SKILLS_REQUIRED, etc. from job descriptions; SkillSpan data; fallback to resume NER if not loaded |
