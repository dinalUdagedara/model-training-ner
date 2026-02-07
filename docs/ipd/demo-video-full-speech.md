# IPD Demo Video — Full Speech Script

**Use this as the exact words to say when recording.** Read or paraphrase; adjust names or paths if yours differ. Total: **max 7 min** for Part A, **max 3 min** for Part B.

---

## Part A: Code walk-through (max 7 minutes)

---

### 1. Repo and project structure (~1 min)

**[Show the two folders or repo roots.]**

"Hello. This is the demo video for my IPD submission for CrackInt.

The project is split into two main parts. First, this folder — model-traning-1:30 — is where I train the NER models and prepare the data. It contains the training notebooks for the resume NER and the job poster NER, plus the datasets and saved model artifacts.

The second part is the PROJECT folder, which has the CrackInt web application: the FastAPI backend and the Next.js frontend. That’s where the trained models are loaded and used at runtime. So: training happens here, and the live app runs from there."

---

### 2. Dataset creation: combining different datasets (~1 min)

**[Show resume_ner_pipeline/prepare_data.py and/or job_poster_ner_pipeline/prepare_data.py; optionally list merged_resume_ner.json and merged_job_poster_ner.json.]**

"We built our training data by combining several existing datasets instead of using a single source. For resumes, we merged the original entity_recognition_in_resumes dataset — about 220 resumes — with the Dotin dataset of 545 annotated CVs, and optionally with vrundag91 and minhquan resume corpora. Each source had different label schemes: Dotin has 12 entity types, others use different names. We wrote a prepare_data script that loads all of these and maps every label to a single unified schema: NAME, EMAIL, SKILL, OCCUPATION, EDUCATION, EXPERIENCE, and O. That gives us one merged_resume_ner.json file with consistent labels.

For job postings we did the same idea. We use SkillSpan — an NAACL 2022 dataset of over 11,000 job-posting sentences — and convert it into our JSONL format. The prepare_data script for jobs can also merge multiple sources and maps different label names — like Skill, Qualification, Experience, Occupation — to our unified job-poster types: JOB_TITLE, COMPANY, SKILLS_REQUIRED, EXPERIENCE_REQUIRED, EDUCATION_REQUIRED, and so on. So we get one merged_job_poster_ner.json.

Why combine datasets? First, more training data: a single public dataset is often too small for good NER performance. Second, consistent labels: we need one schema so the model learns the same six resume entities or the same job-poster entities regardless of source. Third, diversity: different annotators and sources reduce bias and improve generalization. So both models are trained on merged, unified data produced by these prepare_data scripts."

---

### 3. Resume NER model (~2 min)

**[Open the Resume NER training notebook.]**

"The first model is the resume NER. In this notebook I train a BERT-BiLSTM-CRF model to extract six entity types from resume text: NAME, EMAIL, SKILL, OCCUPATION, EDUCATION, and EXPERIENCE.

Let me quickly explain how the notebook works end-to-end.

First, it loads the merged dataset file, which is a list of items where each item has the raw text and span annotations. From those spans we generate token-level labels, typically in BIO format, so that every token becomes B-SKILL, I-SKILL, and so on, or O.

Next, we tokenize the text with a BERT tokenizer. The important part here is label alignment: because BERT uses subword tokens, one original word might become multiple WordPieces, so the notebook aligns the BIO label to the correct sub-tokens and ignores special tokens like [CLS] and [SEP].

Then we train the model. BERT produces contextual embeddings, BiLSTM adds sequential context across tokens, and CRF decodes the best global label sequence so we get consistent entity spans rather than noisy independent predictions.

After training we evaluate on a validation or test split, then we save the model weights and label mappings. Those saved artifacts are what the backend loads at runtime."

**[Switch to PROJECT, open crackint-backend/app/ml/resume_ner.py.]**

"In the backend, the resume NER lives in app/ml/resume_ner.py. At runtime we load the saved model from RESUME_NER_LOAD_DIR or from Hugging Face.

The main function is parse_resume_hybrid. The extraction process is:

- If the input is a PDF, we first extract text using PyMuPDF.
- We run lightweight cleanup so the model sees plain text.
- We tokenize the text, run the model forward pass, and decode labels with the CRF to get token-level predictions.
- We convert token-level BIO labels back into final entity spans and group them into a clean JSON structure.
- We also apply simple rule-based extraction for NAME and EMAIL as a reliability layer, and then merge those results with the model output.

Finally, it returns a dictionary of entities for the frontend."

**[Open app/api/resume/service.py and route.py.]"

"The resume API is in app/api/resume. The route accepts either a PDF file or raw text. The service extracts text from the PDF using PyMuPDF, then calls parse_resume_hybrid. The response includes the extracted entities and, if needed, the raw extracted text. Then we save the resume record and entities to PostgreSQL and return them to the client. So the full flow is: PDF or text in → text extraction → NER inference → post-processing → entities out → persist → return to UI."

---

### 4. Job poster NER model and job extractor (~2 min)

**[Open the Job Poster NER training notebook.]**

"The second model is the job poster NER. This notebook trains another BERT-BiLSTM-CRF model, but on job descriptions. The training data is the merged job-poster dataset — in our case mainly SkillSpan, converted and merged via prepare_data.

The notebook pipeline is the same pattern as the resume model:

- Load the merged JSONL data with job text plus span annotations.
- Convert spans into token-level BIO labels for the job entities.
- Tokenize with BERT and align labels to subword tokens.
- Train the BERT-BiLSTM-CRF model and evaluate on a split.
- Save model weights plus the label mappings so the backend can reproduce the exact label IDs at inference time.

The entity types here are job-specific: JOB_TITLE, COMPANY, LOCATION, SALARY, SKILLS_REQUIRED, EXPERIENCE_REQUIRED, EDUCATION_REQUIRED, and JOB_TYPE."

**[Open PROJECT/crackint-backend/app/ml/job_poster_ner.py.]**

"In the backend, the job poster NER is in app/ml/job_poster_ner.py. It’s loaded from JOB_POSTER_NER_LOAD_DIR.

The extraction flow is the same idea as resume NER: we take raw text, tokenize, run the model, decode CRF labels, then post-process BIO tags into final entities. We also have rule-based SALARY extraction to catch salary patterns that can be missed by the model. If the job poster model isn’t set — for example in a minimal setup — the job extractor can fall back to the resume NER so the API still works end-to-end."

**[Open app/api/job/route.py and service.py.]**

"The job extractor is the endpoint POST /api/v1/jobs/extract. It accepts a PDF or raw text, extracts text if it’s a PDF, then runs the job poster NER — or the resume NER fallback — and returns the entities as JSON. We don’t persist job extractions in the database in this IPD scope; it’s on-demand only. So the job flow is: PDF/text in → text extraction → job NER inference → post-processing → entities out."

---

### 5. Frontend integration (~1–2 min)

**[Open PROJECT/crackint-frontend/services/resume-uploader.service.ts.]**

"On the frontend, the resume flow is in services/resume-uploader.service. It calls POST /api/v1/resumes/extract with either a file or text. The response has the extracted entities and optional raw text. The CV upload page displays them and lets the user edit entities via a PATCH request."

**[If you have a job description page, open the job-extract service and job-description page.]**

"The job description page does the same for jobs: it sends pasted text or an uploaded PDF to POST /api/v1/jobs/extract and displays the returned entities. Both pages are in the app router — cv-upload and job-description — and each one calls its backend endpoint and shows the result in a simple card layout. That’s the integration: two pages, two extract APIs, and both NER models used in the backend."

---

## Part B: Prototype demonstration (max 3 minutes)

---

### 1. Open the app

**[Open the app in the browser.]**

"Now I’ll show the prototype running in the browser."

---

### 2. Resume flow

**[Go to CV Upload.]**

"I’m on the CV Upload page. I’ll paste a short resume-style text — [or: I’ll upload a sample resume PDF]. Then I click Extract."

**[Click Extract; wait for result.]**

"Here we see the extracted information: name, email, skills, occupation, education, and experience. I can edit any of these with the Edit button, or replace the resume and extract again. So the resume NER is working end-to-end: from the frontend through the API to the model and back."

---

### 4. Closing

"This is the current IPD prototype: resume extraction and job extraction, with both NER models integrated in the backend and exposed through the frontend. Thank you."

---

## Short version (if you need to trim time)

**Part A (shorter):**

- "Two parts: this repo for training, PROJECT for the app. We combined several datasets for training: for resumes, existing 220 + Dotin 545 (and optionally vrundag91, minhquan), mapped to one schema via prepare_data; for jobs, SkillSpan (11k+ sentences) converted and merged. Why: more data, one consistent label set, and more diversity. Resume NER: BERT-BiLSTM-CRF for NAME, EMAIL, SKILL, OCCUPATION, EDUCATION, EXPERIENCE; job poster NER: same architecture, job-specific entities; both loaded in the backend and used by the resume and job extract APIs. Frontend: CV upload and job description pages call the two extract endpoints and show the entities."

**Part B (shorter):**

- "Here’s the app. CV Upload: I paste resume text and click Extract — entities appear; I can edit. Job description: I paste a job and click Extract — job entities appear. Both flows work. Thanks."

---

*Rehearse once with a timer; adjust wording to match your exact file names and paths.*
