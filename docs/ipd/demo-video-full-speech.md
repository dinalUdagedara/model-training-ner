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

"The first model is the resume NER. In this notebook I train a BERT-BiLSTM-CRF model to extract six entity types from resume text: NAME, EMAIL, SKILL, OCCUPATION, EDUCATION, and EXPERIENCE. The data comes from the merged dataset we just described — combined resumes from multiple sources with a unified schema. We load that into the notebook, fine-tune the model, and then save the state dict and a small config so the backend can load it later."

**[Switch to PROJECT, open crackint-backend/app/ml/resume_ner.py.]**

"In the backend, the resume NER lives in app/ml/resume_ner.py. At runtime we load the saved model from RESUME_NER_LOAD_DIR or from Hugging Face. The main function is parse_resume_hybrid: it runs the BERT-BiLSTM-CRF model and also uses simple rule-based extraction for NAME and EMAIL to improve reliability. It returns a dictionary of entities."

**[Open app/api/resume/service.py and route.py.]"

"The resume API is in app/api/resume. The route accepts either a PDF file or raw text. The service extracts text from the PDF using PyMuPDF, then calls parse_resume_hybrid. The result is saved to PostgreSQL and returned to the client. So the full flow is: PDF or text in, entities out, and we persist the resume record."

---

### 4. Job poster NER model and job extractor (~2 min)

**[Open the Job Poster NER training notebook.]**

"The second model is the job poster NER. This notebook trains another BERT-BiLSTM-CRF model, but on job descriptions. The training data is the merged job-poster data — in our case mainly SkillSpan, converted and merged via prepare_data. The entity types are job-specific: JOB_TITLE, COMPANY, LOCATION, SALARY, SKILLS_REQUIRED, EXPERIENCE_REQUIRED, EDUCATION_REQUIRED, and JOB_TYPE. Same architecture as the resume model, but the labels and data are different. We save this model the same way so the backend can load it."

**[Open PROJECT/crackint-backend/app/ml/job_poster_ner.py.]**

"In the backend, the job poster NER is in app/ml/job_poster_ner.py. It’s loaded from JOB_POSTER_NER_LOAD_DIR. We also have rule-based SALARY extraction to catch salary phrases. If the job poster model isn’t set — for example in a minimal setup — the job extractor falls back to the resume NER so the API still works."

**[Open app/api/job/route.py and service.py.]**

"The job extractor is the endpoint POST /api/v1/jobs/extract. It accepts a PDF or raw text, extracts the text, then runs the job poster NER — or the resume NER fallback — and returns the entities. We don’t persist job extractions; it’s on-demand only. So that’s the job extractor: same idea as the resume API, but for job descriptions and with no database save."

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

### 3. Job extractor flow

**[Go to Job description page.]**

"Next, the job description page. I’ll paste a short job description — [or: upload a job PDF]. Then I click Extract."

**[Click Extract; wait for result.]**

"And here are the extracted job entities: job title, company, skills required, experience required, and so on. This uses the job poster NER in the backend — or the resume NER fallback if the job model isn’t loaded. So both extraction flows are working in the prototype."

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
