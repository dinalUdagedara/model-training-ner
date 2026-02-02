# FYP: Job Poster NER (BERT-BiLSTM-CRF)

This folder contains the FYP notebook for **Job Poster Named Entity Recognition** using a BERT-BiLSTM-CRF model. Entity types: **JOB_TITLE**, **COMPANY**, **LOCATION**, **SALARY**, **SKILLS_REQUIRED**, **EXPERIENCE_REQUIRED**, **EDUCATION_REQUIRED**, **JOB_TYPE**. The notebook is intended for **Google Colab** or local runs.

**Setup:**  
- **Colab:** Mount Google Drive first (step at the top). Place `merged_job_poster_ner.json` in your My Drive root.  
- **Local:** Run the notebook from `fyp/job-poster-ner`; it will use `../../job_poster_ner_pipeline/merged_job_poster_ner.json` if the file is not on Drive.

Prepare the data with `job_poster_ner_pipeline/prepare_data.py` before running the notebook.

**Requirements:** `torch`, `transformers`, `pytorch-crf`, `seqeval`

**Inference:** The notebook defines `parse_job_poster` (model only) and `parse_job_poster_hybrid` (SALARY from rules, rest from model). Use the hybrid for higher recall on salary phrases.
