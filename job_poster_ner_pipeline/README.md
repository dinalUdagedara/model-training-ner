# Job Poster NER Pipeline

Extract **job details** from job posting text using the same BERT-BiLSTM-CRF architecture as the resume NER pipeline. Entity types: **JOB_TITLE**, **COMPANY**, **LOCATION**, **SALARY**, **SKILLS_REQUIRED**, **EXPERIENCE_REQUIRED**, **EDUCATION_REQUIRED**, **JOB_TYPE**.

**A real dataset is already set up:** SkillSpan (NAACL 2022) is downloaded and merged — **11,543 job-posting sentences** in `merged_job_poster_ner.json`. See **[GETTING_DATA.md](GETTING_DATA.md)** for details and other options (LREC 2022, DIY annotation).

**Current model coverage:** The model **architecture** has all 8 entity types (JOB_TITLE, COMPANY, LOCATION, SALARY, SKILLS_REQUIRED, EXPERIENCE_REQUIRED, EDUCATION_REQUIRED, JOB_TYPE), but the **training data** (SkillSpan) only contains **SKILLS_REQUIRED** (skill + knowledge). So a model trained on the current `merged_job_poster_ner.json` effectively predicts only **SKILLS_REQUIRED**; the other slots are usually empty unless you add rule-based extraction (e.g. SALARY via regex in the backend) or train on data that has those labels (LREC 2022, or your own annotations).

## 1. Data format

Each sample is one JSON object per line (JSONL):

- **content**: Full job posting text.
- **annotation**: List of spans with **label** (e.g. `["JOB_TITLE"]`) and **points** (`[{start, end, text}]`).

See [DATA_FORMAT.md](DATA_FORMAT.md) for the full schema, examples, and how to create or import annotated data.

## 2. Prepare data

From this folder:

```bash
# Single JSONL file
python prepare_data.py --input job_postings.jsonl --output merged_job_poster_ner.json

# Or a directory of JSONL files
python prepare_data.py --input data/ --output merged_job_poster_ner.json
```

To try the pipeline on the small sample:

```bash
python prepare_data.py --input sample_job_poster_ner.json --output merged_job_poster_ner.json
```

Label names from your JSONL are mapped to the unified set (JOB_TITLE, COMPANY, LOCATION, SALARY, SKILLS_REQUIRED, EXPERIENCE_REQUIRED, EDUCATION_REQUIRED, JOB_TYPE, O). See `prepare_data.py` for the full mapping.

## 3. Run the notebook

1. Open **BERT_BiLSTM_CRF_Job_Poster_NER.ipynb** in Jupyter or Cursor.
2. Run cells in order. Cell 1 loads `merged_job_poster_ner.json` (or `sample_job_poster_ner.json` if that’s what you merged).
3. Train (cell 6), evaluate (cell 7), save (cell 8). Default save directory is `job_poster_ner` (or Google Drive `job_poster_ner` if in Colab).
4. Load saved model (cell 10) and run the inference cells to extract entities from job poster text.

## 4. Entity types

| Type | Description |
|------|-------------|
| JOB_TITLE | Job title (e.g. Senior Data Scientist) |
| COMPANY | Employer / company name |
| LOCATION | Location (city, remote, etc.) |
| SALARY | Salary or pay range |
| SKILLS_REQUIRED | Required skills or technologies |
| EXPERIENCE_REQUIRED | Experience level or years |
| EDUCATION_REQUIRED | Required education |
| JOB_TYPE | Full-time, part-time, contract, etc. |

## 5. Files

- **prepare_data.py** – Merge JSONL into `merged_job_poster_ner.json`.
- **scripts/download_skillspan.py** – Download SkillSpan (GitHub) and convert to our JSONL.
- **skillspan_job_poster.jsonl** – Converted SkillSpan data (11,543 sentences).
- **merged_job_poster_ner.json** – Merged data used by the notebook (SkillSpan + any other JSONL you add).
- **DATA_FORMAT.md** – Data schema and annotation options.
- **GETTING_DATA.md** – How to get annotated data (SkillSpan ready-to-use, LREC 2022, DIY).
- **sample_job_poster_ner.json** – 3 example lines for testing.
- **BERT_BiLSTM_CRF_Job_Poster_NER.ipynb** – Train and run inference (same setup as resume NER).
- **README.md** – This file.

## 6. Public datasets

If you use a dataset with different label names (e.g. LREC 2022 job description corpus: Skill, Qualification, Experience, Occupation, Domain), add a mapping in `prepare_data.py` (e.g. Occupation → JOB_TITLE, Skill → SKILLS_REQUIRED, Qualification → EDUCATION_REQUIRED, Experience → EXPERIENCE_REQUIRED, Domain → O).
