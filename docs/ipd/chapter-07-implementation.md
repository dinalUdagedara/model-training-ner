# Chapter 07: Implementation

**Purpose:** Implementation chapter for IPD thesis. Covers technology selection, core functionalities, dataset, code structure, UI implementation, and challenges/solutions.

---

## 7.1 Chapter Overview

This chapter describes how CrackInt was implemented from design to a working prototype. It justifies technology choices, documents the implementation of core modules (resume NER, job poster NER, text extraction, API, database), presents dataset statistics and train/val/test splits for the NER model, outlines the code structure of frontend and backend, and discusses challenges encountered and solutions applied.

### 7.1.1 Implemented Architecture Overview

Figure 10 shows the high-level system architecture as implemented. The prototype follows the tiered design (Client → Next.js Frontend → FastAPI Backend → PostgreSQL) with ML services for resume and job NER.

![Figure 10: Implemented System Architecture](diagrams/02-high-level-architecture.png)

*Figure 10: Implemented System Architecture*

---

## 7.2 Technology Selection

### 7.2.1 Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| **Frontend** | Next.js | 16.x | App Router, SSR, TypeScript support, ecosystem. |
| **Frontend** | React | 19.x | Component model, widespread adoption. |
| **Frontend** | Tailwind CSS | 4.x | Utility-first styling, rapid UI development. |
| **Frontend** | shadcn/ui (Radix) | Latest | Accessible, customizable components. |
| **Backend** | FastAPI | ≥0.115 | Async support, auto OpenAPI docs, Pydantic validation. |
| **Backend** | Python | 3.11 | ML/NLP ecosystem, type hints. |
| **Database** | PostgreSQL | 15 | ACID, JSONB for flexible entity storage. |
| **ORM** | SQLModel / SQLAlchemy | 2.x | Async support, type-safe models. |
| **ML** | PyTorch | ≥2.0 | NER model training and inference. |
| **ML** | pytorch-crf | ≥0.7.2 | CRF layer for sequence labelling. |
| **ML** | gensim | ≥4.0 | Word2Vec for Path 2 embeddings. |

### 7.2.2 Backend Dependencies (pyproject.toml)

- **API:** fastapi, uvicorn, python-multipart, pydantic, pydantic-settings  
- **ML:** torch, transformers, pytorch-crf, gensim  
- **PDF/OCR:** pymupdf, pillow, pytesseract  
- **Database:** sqlalchemy, sqlmodel, asyncpg, alembic  
- **Optional:** openai (for entity validation agent), gdown (model download from Drive)

### 7.2.3 Frontend Dependencies (package.json)

- **Framework:** next, react, react-dom  
- **UI:** @radix-ui/*, tailwindcss, lucide-react, class-variance-authority, clsx, tailwind-merge  
- **Data:** @tanstack/react-query  
- **Theme:** next-themes

### 7.2.4 Summary of Technology Selection

Technologies were chosen for alignment with SRS requirements (performance, modularity, maintainability), compatibility with ML libraries (PyTorch, transformers, gensim), and support for mobile-responsive, accessible UIs (Next.js, Tailwind, Radix).

---

## 7.3 Core Functionalities Implementation

### 7.3.1 Dataset and NER Model Statistics

**Dataset:** `merged_1030_plus_all_llm_plus_sri_lanka_tech.jsonl`

| Split | Count | Percentage |
|-------|-------|------------|
| Training | 3,194 | 80% |
| Validation | 399 | 10% |
| Test | 400 | 10% |
| **Total** | **3,993** | 100% |

**Entity types:** NAME, EMAIL, SKILL, OCCUPATION, EDUCATION, EXPERIENCE (BIO format).

**Model:** Word2Vec (256-dim) + 2-layer BiLSTM (hidden 384) + CRF. Vocab size ~46,330. Max sequence length 768.

![Figure 11: BiLSTM-CRF Model Architecture](diagrams/09-bilstm-crf-architecure.png)

*Figure 11: BiLSTM-CRF model architecture — implemented in PyTorch*

**Reported metrics (Test set):**

| Entity | Precision | Recall | F1-Score |
|--------|-----------|--------|----------|
| NAME | 0.99 | 0.89 | 0.94 |
| EMAIL | 0.99 | 0.94 | 0.96 |
| SKILL | 0.89 | 0.80 | 0.84 |
| OCCUPATION | 0.59 | 0.57 | 0.58 |
| EDUCATION | 0.64 | 0.61 | 0.62 |
| EXPERIENCE | 0.83 | 0.67 | 0.74 |
| **Micro avg** | 0.84 | 0.75 | **0.79** |

### 7.3.2 Backend Module Implementation

#### Resume NER (`app/ml/resume_ner.py`)

- **Classes:** `BertBiLSTMCRF`, `Word2VecBiLSTMCRF` (supports both BERT and Word2Vec paths).
- **Loading:** Reads `ner_config.json`, `bilstm_crf_state.pt` (or `bert_bilstm_crf_state.pt`) from `RESUME_NER_LOAD_DIR`.
- **Inference:** `parse_resume_hybrid()` — rules for NAME/EMAIL, model for SKILL/OCCUPATION/EDUCATION/EXPERIENCE.
- **Fallback:** Stub extraction when model not loaded (first-line name, regex email).

#### Job Poster NER (`app/ml/job_poster_ner.py`)

- Skill extraction from job descriptions; can use SkillSpan-based or custom model.
- API: `POST /api/v1/jobs/extract`.

#### Text Extraction (`app/services/text_extraction.py`)

- PDF: PyMuPDF.
- Images: OCR (Tesseract) via Pillow.
- Supported: PDF, PNG, JPEG, WebP.

#### API Routes

| Route | Method | Purpose |
|-------|--------|---------|
| `/api/v1/resumes/extract` | POST | Extract from PDF/text, persist to DB |
| `/api/v1/resumes/preview-extract` | POST | Extract without save (debug) |
| `/api/v1/resumes/{id}` | GET, PUT, PATCH | Read, replace, update entities |
| `/api/v1/jobs/extract` | POST | Extract from job text/PDF |
| `/api/v1/job-postings` | GET, POST | List, create job postings |
| `/api/v1/sessions` | GET, POST | List, create prep sessions |
| `/api/v1/sessions/{id}/messages` | GET, POST | List, append chat messages |
| `/api/v1/health` | GET | Health check |

### 7.3.3 Frontend Implementation

#### Pages

- **Home:** `app/page.tsx` — dashboard, chat input placeholder.
- **CV Upload:** `app/cv-upload/page.tsx` — CVUploadView, file drop, paste, extract, edit.
- **Job Upload:** `app/job-upload/page.tsx` — JobUploadView, job text/PDF extract.
- **Job Postings:** `app/job-postings/page.tsx`, `app/job-postings/[id]/page.tsx` — list and detail.
- **Sessions:** `app/sessions/page.tsx`, `app/sessions/[id]/page.tsx` — list and chat view.

#### Services

- `resume-uploader.service.ts` — POST extract, PATCH entities.
- `job-extractor.service.ts` — job extraction.
- `job-postings.service.ts` — job posting CRUD.
- `sessions.service.ts` — prep sessions and messages.

#### Integration

- React Query for server state.
- Fetch/axios to FastAPI; CORS enabled on backend.

### 7.3.4 Code Structure

**Backend (`crackint-backend/`):**

```
app/
├── api/           # Routes, schemas, deps
├── ml/            # resume_ner.py, job_poster_ner.py
├── services/      # text_extraction.py, ocr.py
├── models.py      # SQLModel entities
├── config.py
├── database.py
└── main.py
```

**Frontend (`crackint-frontend/`):**

```
app/               # Pages (App Router)
components/        # UI components
services/          # API clients
lib/               # Utilities
types/             # api.types.ts
```

---

## 7.4 User Interface Implementation

### 7.4.1 Frontend Development

- **CV Upload:** Tabs for file upload and paste; drop zone; loading spinner; entity cards; Edit modal.
- **Job Upload:** Text area and optional PDF; extract button; entity display.
- **Sessions:** List of sessions; chat view with message list and input.
- **Theme:** next-themes for light/dark mode; shadcn components for consistency.

### 7.4.2 Backend Integration

- Base URL configurable (e.g. `NEXT_PUBLIC_API_URL`).
- Common response format: `{ success, message, payload, meta }`.
- Error handling: 4xx/5xx with structured error payloads.

### 7.4.3 Accessibility Considerations

- Semantic HTML; ARIA where needed.
- Keyboard navigation for main flows.
- Sufficient contrast; responsive layout for mobile.

---

## 7.5 Challenges and Solutions

| Challenge | Solution |
|-----------|----------|
| **Model file size / deployment** | Model loaded from `RESUME_NER_LOAD_DIR`; optional Google Drive download via `gdown` when path not present. |
| **BERT vs Word2Vec path** | Backend detects config (word2id, embed_dim) and loads `Word2VecBiLSTMCRF` or `BertBiLSTMCRF` accordingly. |
| **PDF extraction reliability** | PyMuPDF for PDF; Tesseract for images; fallback to raw text when extraction fails. |
| **Long resumes** | Truncation at 768 tokens (Word2Vec path); 512 for BERT path. |
| **Entity alignment** | BIO tagging; hybrid rules for NAME/EMAIL to improve robustness. |
| **CORS / API access** | CORS middleware allows frontend origin; API prefix configurable. |
| **Database migrations** | Alembic for schema versioning; migrations for users, resumes, job_postings, prep_sessions, messages. |

---

## 7.6 Chapter Summary

This chapter documented the implementation of the CrackInt prototype: technology stack (Next.js, FastAPI, PyTorch, PostgreSQL), dataset and NER model statistics (3,993 resumes, Test F1 0.79), core backend modules (resume NER, job poster NER, text extraction, API routes), frontend pages and services, code organization, and key challenges and solutions. The prototype demonstrates resume and job extraction with editable entities and session/message persistence, providing a foundation for future question generation and semantic feedback features.
