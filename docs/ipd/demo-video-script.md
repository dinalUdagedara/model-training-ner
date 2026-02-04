# IPD Demo Video — Script and Outline

**Purpose:** Use this document as your script when recording the IPD **video demonstration** (5–10 min total). The walk-through must include **both** the **Resume NER** and **Job Poster NER** models and the **job extractor** in the backend.

**IPD requirement:** Code explanation **max 7 minutes**; prototype demonstration **max 3 minutes**; voice-over throughout; upload to YouTube as unlisted.

---

## 1. Timing and rules

| Part | Max duration | Content |
|------|----------------|--------|
| **Part A: Code walk-through** | **7 minutes** | Repo structure, resume NER model, job poster NER model + job extractor, frontend integration. |
| **Part B: Prototype demo** | **3 minutes** | Live app: resume flow then job description flow. |

**Rules:**

- **Voice-over throughout** — explain what you are showing; do not leave long silences.
- **Clear audio** — use a decent microphone; minimise background noise.
- **Avoid:** Rushing through code; reading every line; going over 7 min for Part A or 3 min for Part B.
- **Do:** Show the key files and say what they do; one run-through of each flow in the live demo.

---

## 2. Part A: Code walk-through (max 7 minutes)

### 2.1 Repo and project structure (~1 min)

**What to show:**

- **Two main locations:**
  - **model-traning-1:30** (or your NER training repo): Where the NER **models are trained** — datasets, notebooks, saved model artifacts.
  - **PROJECT** (crackint-frontend + crackint-backend): The **web application** — where the trained models are **loaded and used** at runtime.

**Talking points:**

- "The project is split into two parts: one repo for training the NER models and preparing the data, and another for the CrackInt web app."
- "In the training repo we have the resume NER and job poster NER notebooks and data; in PROJECT we have the FastAPI backend that loads these models and the Next.js frontend that calls the APIs."

---

### 2.2 Resume NER model (~2 min)

**What to show:**

1. **Training:** Open the **Resume NER** notebook — e.g. `fyp/BERT_BiLSTM_CRF_Resume_NER_FYP.ipynb` or `resume_ner_pipeline/BERT_BiLSTM_CRF_Job_Poster_NER.ipynb` (whichever you use). Briefly show: data loading, model architecture (BERT-BiLSTM-CRF), entity types (NAME, EMAIL, SKILL, OCCUPATION, EDUCATION, EXPERIENCE), and that the model is saved (e.g. state dict + config).
2. **Runtime (backend):** Open **PROJECT/crackint-backend/app/ml/resume_ner.py**. Say: "At runtime the backend loads the saved model from `RESUME_NER_LOAD_DIR` or from Hugging Face. The main function is `parse_resume_hybrid`: it runs the BERT-BiLSTM-CRF model plus rule-based extraction for NAME and EMAIL, and returns a dictionary of entities."
3. **API use:** Open **PROJECT/crackint-backend/app/api/resume/service.py** and **route.py**. Say: "The resume API accepts either a PDF file or raw text. The service extracts text from the PDF with PyMuPDF, then calls `parse_resume_hybrid`. The result is persisted to PostgreSQL and returned to the client."

**Talking points:**

- "The resume NER is a BERT-BiLSTM-CRF model fine-tuned to extract NAME, EMAIL, SKILL, OCCUPATION, EDUCATION, and EXPERIENCE from resume text."
- "In the backend we load this model once and use it for every extract request; we also use simple rules for email and name to improve reliability."

---

### 2.3 Job poster NER model and job extractor (~2 min)

**What to show:**

1. **Training:** Open the **Job Poster NER** notebook — e.g. `fyp/job-poster-ner/BERT_BiLSTM_CRF_Job_Poster_NER_FYP.ipynb`. Briefly show: job-specific entity types (e.g. JOB_TITLE, COMPANY, LOCATION, SALARY, SKILLS_REQUIRED, EXPERIENCE_REQUIRED, EDUCATION_REQUIRED, JOB_TYPE), same BERT-BiLSTM-CRF architecture, and where the model is saved.
2. **Runtime (backend):** Open **PROJECT/crackint-backend/app/ml/job_poster_ner.py**. Say: "The job poster NER is loaded from `JOB_POSTER_NER_LOAD_DIR`. It has the same architecture as the resume NER but is trained on job descriptions and outputs job-specific tags. We also have rule-based SALARY extraction. If the job poster model is not set, the job extractor falls back to the resume NER so the API still works."
3. **Job extractor API:** Open **PROJECT/crackint-backend/app/api/job/route.py** and **service.py**. Say: "The job extractor endpoint is POST /api/v1/jobs/extract. It accepts a PDF or raw text, extracts text, then runs the job poster NER — or the resume NER fallback — and returns the entities. We don’t persist job extractions; it’s on-demand only."

**Talking points:**

- "The job poster NER is a second BERT-BiLSTM-CRF model trained on job descriptions to extract job title, company, location, salary, skills required, experience required, education required, and job type."
- "The job extractor in the backend uses this model when it’s configured; otherwise it falls back to the resume NER so the feature still works in any environment."

---

### 2.4 Frontend integration (~1–2 min)

**What to show:**

1. **Resume flow:** Open **PROJECT/crackint-frontend/services/resume-uploader.service.ts**. Say: "The frontend calls POST /api/v1/resumes/extract with either a file or text. The response contains the extracted entities and optional raw text; the CV upload page displays them and allows edit via PATCH."
2. **Job flow:** If you have a job description page, open the **job-extract service** (e.g. `services/job-extract.service.ts`) and the **job-description page** or component. Say: "The job description page does the same for jobs: it sends the pasted text or uploaded PDF to POST /api/v1/jobs/extract and displays the returned entities."
3. **Pages:** Briefly show **app/cv-upload/page.tsx** and **app/job-description/page.tsx** (or the route you use) so the structure is clear.

**Talking points:**

- "The frontend is Next.js: one page for CV upload and one for job description. Each calls the corresponding backend extract endpoint and shows the entities in a simple card layout."

---

## 3. Part B: Prototype demonstration (max 3 minutes)

**What to do:**

1. **Open the app** — "I’ll show the prototype running." Open the app in the browser (localhost or hosted URL).
2. **Resume flow:**
   - Go to the CV Upload page.
   - Either upload a sample resume PDF or paste a short resume-style text.
   - Click Extract (or equivalent).
   - Point out the extracted entities (name, email, skills, education, experience).
   - Optionally: show Edit (change a value) and Replace resume (start again).
3. **Job extractor flow:**
   - Go to the Job description page (sidebar or nav).
   - Paste a short job description text (or upload a job PDF if supported).
   - Click Extract.
   - Point out the extracted job entities (e.g. job title, company, skills required, experience required).
4. **Closing:** "This is the current IPD prototype: resume extraction and job extraction, with both NER models integrated in the backend and exposed through the frontend."

**Tips:**

- Use one short resume and one short job description so the demo stays within 3 minutes.
- Speak while you click: "I’m pasting a job description… now I’ll click Extract… and here we see the job title, company, and skills required."

---

## 4. Checklist before recording

- [ ] **Microphone:** Test recording; no echo or heavy noise.
- [ ] **Screen:** Resolution and font size readable when played back (e.g. 1080p; zoom code to ~100–120%).
- [ ] **Tabs/apps:** Close unrelated windows; only repo, IDE, and browser with the app.
- [ ] **Sample data:** One resume PDF or paste-ready resume text; one paste-ready job description (or job PDF).
- [ ] **App running:** Backend and frontend started; resume and job extract both work.
- [ ] **Rehearse once:** Run through Part A and Part B with a timer; trim if over 7 min or 3 min.

---

## 5. File reference (for screen sharing)

| Topic | Where to open |
|-------|----------------|
| Resume NER training | `model-traning-1:30/fyp/BERT_BiLSTM_CRF_Resume_NER_FYP.ipynb` or `resume_ner_pipeline/` notebook |
| Job poster NER training | `model-traning-1:30/fyp/job-poster-ner/BERT_BiLSTM_CRF_Job_Poster_NER_FYP.ipynb` |
| Resume NER at runtime | `PROJECT/crackint-backend/app/ml/resume_ner.py` |
| Job poster NER at runtime | `PROJECT/crackint-backend/app/ml/job_poster_ner.py` |
| Resume API route + service | `PROJECT/crackint-backend/app/api/resume/route.py`, `service.py` |
| Job extractor API | `PROJECT/crackint-backend/app/api/job/route.py`, `service.py` |
| Frontend resume service | `PROJECT/crackint-frontend/services/resume-uploader.service.ts` |
| Frontend job service (if present) | `PROJECT/crackint-frontend/services/job-extract.service.ts` |
| CV upload page | `PROJECT/crackint-frontend/app/cv-upload/page.tsx` |
| Job description page (if present) | `PROJECT/crackint-frontend/app/job-description/page.tsx` |

---

*Use this script to record the demo video, then upload to YouTube as unlisted and share the URL in both Blackboard and the Google Form.*
