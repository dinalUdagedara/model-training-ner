# Job Poster NER — Data Format

Same format as the resume pipeline: one JSON object per line (JSONL). Each line is a job posting with `content` (full text) and `annotation` (list of labeled spans).

## Schema

Each line in your JSONL file must be a JSON object:

```json
{
  "content": "Full job posting text as a single string...",
  "annotation": [
    {
      "label": ["JOB_TITLE"],
      "points": [{"start": 0, "end": 22, "text": "Senior Data Scientist"}]
    },
    {
      "label": ["COMPANY"],
      "points": [{"start": 25, "end": 35, "text": "Acme Corp"}]
    }
  ]
}
```

- **content**: Raw job poster text (no newlines required; newlines are allowed).
- **annotation**: List of spans. Each span has:
  - **label**: List with one string — one of: `JOB_TITLE`, `COMPANY`, `LOCATION`, `SALARY`, `SKILLS_REQUIRED`, `EXPERIENCE_REQUIRED`, `EDUCATION_REQUIRED`, `JOB_TYPE`, or `O`.
  - **points**: List of `{start, end, text}`. `start` and `end` are character offsets into `content`; `text` is the substring (usually `content[start:end]`).

Spans are converted to BIO tags per token (whitespace-split) by the notebook; overlapping or nested spans are not supported — each character belongs to at most one entity.

## Unified entity types

| Label | Description |
|-------|-------------|
| JOB_TITLE | Job title, e.g. "Senior Data Scientist", "Software Engineer" |
| COMPANY | Employer / company name |
| LOCATION | Location (city, country, remote, etc.) |
| SALARY | Salary or pay range (e.g. "$80k–120k", "Competitive") |
| SKILLS_REQUIRED | Required skills or technologies |
| EXPERIENCE_REQUIRED | Experience level or years (e.g. "5+ years", "Mid-level") |
| EDUCATION_REQUIRED | Required education (e.g. "Bachelor's in CS", "PhD") |
| JOB_TYPE | Full-time, part-time, contract, internship, etc. |
| O | Not an entity (used for unlabeled spans if you map other labels to O) |

## Example (minimal, one posting)

```json
{"content": "Senior Data Scientist at Acme Corp. Remote. $120k–150k. Skills: Python, ML. 5+ years experience. PhD preferred. Full-time.", "annotation": [{"label": ["JOB_TITLE"], "points": [{"start": 0, "end": 22, "text": "Senior Data Scientist"}]}, {"label": ["COMPANY"], "points": [{"start": 26, "end": 35, "text": "Acme Corp"}]}, {"label": ["LOCATION"], "points": [{"start": 37, "end": 43, "text": "Remote"}]}, {"label": ["SALARY"], "points": [{"start": 45, "end": 55, "text": "$120k–150k"}]}, {"label": ["SKILLS_REQUIRED"], "points": [{"start": 64, "end": 77, "text": "Python, ML"}]}, {"label": ["EXPERIENCE_REQUIRED"], "points": [{"start": 79, "end": 95, "text": "5+ years experience"}]}, {"label": ["EDUCATION_REQUIRED"], "points": [{"start": 97, "end": 111, "text": "PhD preferred"}]}, {"label": ["JOB_TYPE"], "points": [{"start": 113, "end": 122, "text": "Full-time"}]}]}
```

## How to create annotated data

1. **Manual annotation**
   - Use [Label Studio](https://labelstud.io/) or [Brat](https://brat.nlplab.org/) to annotate job posting text with spans and labels.
   - Export to JSON and convert to the format above (one object per line, `content` + `annotation` with `label` and `points`).

2. **From plain text**
   - Put one job posting per file (or one per line in a text file). Use the optional script in this folder to generate a template JSONL with `content` set and empty `annotation: []`. Then annotate spans (by editing JSON or re-importing into Label Studio).

3. **Public datasets**
   - If you use a dataset with different label names (e.g. "Occupation", "Skill"), add a mapping in `prepare_data.py` so they map to JOB_TITLE, SKILLS_REQUIRED, etc. Example: LREC 2022 job description corpus uses Skill, Qualification, Experience, Occupation, Domain — map those to SKILLS_REQUIRED, EDUCATION_REQUIRED, EXPERIENCE_REQUIRED, JOB_TITLE, O (or a custom type).

## Running the pipeline

1. Save your JSONL as e.g. `job_postings.jsonl`.
2. Run: `python prepare_data.py --input job_postings.jsonl --output merged_job_poster_ner.json`
3. Open `BERT_BiLSTM_CRF_Job_Poster_NER.ipynb`, run from cell 1 (load data from `merged_job_poster_ner.json`) through train and save.
