# Getting Annotated Data for Job Poster NER

This pipeline expects JSONL with `content` and `annotation` (see [DATA_FORMAT.md](DATA_FORMAT.md)). Below are practical options; **SkillSpan is already downloaded and merged** for this repo.

---

## Ready-to-use: SkillSpan (already in this repo)

**SkillSpan** (NAACL 2022) is a job-posting NER dataset that is **downloaded and converted** for this pipeline.

- **Source:** [larkinbb/skillspan](https://github.com/larkinbb/skillspan) — *SkillSpan: Hard and Soft Skill Extraction from English Job Postings*
- **Content:** English job postings (sentence-level), tech + house domains.
- **Stats:** **11,543 sentences** (4.8k train, 3.2k dev, 3.6k test); 12.5K+ skill/knowledge spans.
- **Labels in dataset:** Skill (B/I/O), Knowledge (B/I/O). Both are mapped to **SKILLS_REQUIRED** in this pipeline.

### Files in this repo

| File | Description |
|------|-------------|
| `skillspan_job_poster.jsonl` | Converted SkillSpan → our JSONL (content + annotation). |
| `merged_job_poster_ner.json` | Merged data used by the notebook (from the above + `prepare_data.py`). |

### Re-download or re-convert

From the pipeline folder:

```bash
python scripts/download_skillspan.py --out skillspan_job_poster.jsonl
python prepare_data.py --input skillspan_job_poster.jsonl --output merged_job_poster_ner.json
```

Then open `BERT_BiLSTM_CRF_Job_Poster_NER.ipynb` and train; the notebook loads `merged_job_poster_ner.json` by default.

**Note:** SkillSpan only has skill/knowledge spans (→ SKILLS_REQUIRED). For JOB_TITLE, COMPANY, LOCATION, SALARY, EXPERIENCE_REQUIRED, EDUCATION_REQUIRED, JOB_TYPE you need extra data (e.g. LREC 2022 or your own annotations).

---

## 1. LREC 2022 Job Description Corpus (5 entity types)

**Paper:** Green, T.A.F., Maynard, D., Lin, C. (2022). *Development of a Benchmark Corpus to Support Entity Recognition in Job Descriptions.* LREC 2022.

**Dataset:** https://tinyurl.com/skill-extraction-dataset (corpus + schema + baseline CRF).

- **License:** Creative Commons BY (attribution required).
- **Content:** UK job descriptions (sentence-split), from Kaggle/trainrev1 (e.g. TotalJobs).
- **Stats:** ~10,000 sentences, ~245k tokens, **18,617 entities** in 5 types.
- **Scheme:** BIO (one label per token).

### Entity types (LREC 2022)

| Entity | Description | Examples |
|--------|-------------|----------|
| Skill | Tasks/abilities (incl. soft skills) | computer programming, French, honesty |
| Qualification | Certifications from course/exam | Bachelor's Degree, chartership |
| Experience | Lengths of time | 2 years experience, minimum of 5 years |
| Occupation | Job titles | Teaching Assistant, CEO |
| Domain | Areas of industry | aerospace, oil industry, education |

### Mapping to this pipeline

`prepare_data.py` already maps: Skill → SKILLS_REQUIRED, Qualification → EDUCATION_REQUIRED, Experience → EXPERIENCE_REQUIRED, Occupation → JOB_TITLE, Domain → O.

**Not in this corpus:** COMPANY, LOCATION, SALARY, JOB_TYPE.

### Using LREC 2022

1. Download from the link above (repository with corpus + guidelines).
2. Convert their format to our JSONL (`content`, `annotation` with `label` and `points`).
3. Run: `python prepare_data.py --input <path_to_jsonl> --output merged_job_poster_ner.json`
4. Optionally merge with SkillSpan: put both JSONL files in a directory and run `prepare_data.py --input <dir> --output merged_job_poster_ner.json`.

---

## 2. Creating your own annotations

- **Collect:** Job post text (e.g. from job boards).
- **Annotate:** Use [Label Studio](https://labelstud.io/), [Brat](https://brat.nlplab.org/), or similar; export to our JSONL schema.
- **Schema:** `content` (string), `annotation` (list of spans with `label` and `points`). See DATA_FORMAT.md.

Start with a few hundred examples; more data improves performance.

---

## 3. Other public sources (partial)

- **O*NET** (https://www.onetonline.org/): occupation/skill taxonomies, not a NER corpus.
- **ESCO:** good for ontology, not raw job-description NER.
- **Hugging Face:** e.g. `jacob-hugging-face/job-descriptions` (853 rows, company/title/description) — no token-level NER; could be used for silver labeling or separate tasks.

---

## Summary

- **Use SkillSpan first:** it is already in this repo (`skillspan_job_poster.jsonl` → `merged_job_poster_ner.json`). Train with the notebook; you get SKILLS_REQUIRED (skill + knowledge) from real job postings.
- **Add LREC 2022** for Occupation, Qualification, Experience, Domain (and more skills) once you have their corpus in our JSONL format.
- **Add your own annotations** for COMPANY, LOCATION, SALARY, JOB_TYPE and any extra entities.
