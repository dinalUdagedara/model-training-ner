# FYP: Resume NER

This folder contains the FYP notebooks for **Resume Named Entity Recognition**. The **final chosen model** is **Path 2: BiLSTM-CRF** (Word2Vec embeddings, no transformer).

---

## Final model: BiLSTM-CRF Path 2

**Notebook:** [BiLSTM_CRF_Resume_NER_Path2_FYP.ipynb](BiLSTM_CRF_Resume_NER_Path2_FYP.ipynb)

- **Architecture:** Word2Vec embeddings → BiLSTM → CRF (built from scratch, no pre-trained transformer)
- **Entity types:** NAME, EMAIL, SKILL, OCCUPATION, EDUCATION, EXPERIENCE
- **Reported performance (Test):** F1 ≈ 0.79, EMAIL/NAME ~95%, SKILL ~84%, EXPERIENCE ~74%, OCCUPATION ~58%
- **Data:** `merged_1030_plus_all_llm_plus_sri_lanka_tech.jsonl` (~4k resumes)

**Setup:**
- **Colab:** Mount Google Drive and place the data file in My Drive root.
- **Local:** Place the data file in `../resume_ner_pipeline/` (or run from project root).

**Requirements:** `torch`, `pytorch-crf`, `seqeval`, `gensim` (for Word2Vec).

---

## Alternative: BERT-BiLSTM-CRF

**Notebook:** [BERT_BiLSTM_CRF_Resume_NER_FYP.ipynb](BERT_BiLSTM_CRF_Resume_NER_FYP.ipynb)

- Uses BERT embeddings with BiLSTM-CRF. Requires `transformers`.
- **Optional:** `agent_corrector.py` provides a second-stage LLM corrector. Set `OPENAI_API_KEY` for section 7b.

---

## Code guides

- [RESUME_NER_CODE_GUIDE.md](RESUME_NER_CODE_GUIDE.md) — BERT-based notebook
- [job-poster-ner/JOB_POSTER_NER_CODE_GUIDE.md](job-poster-ner/JOB_POSTER_NER_CODE_GUIDE.md) — Job Poster NER
