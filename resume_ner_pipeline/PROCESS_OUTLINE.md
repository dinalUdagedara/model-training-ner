# Resume NER Pipeline — Process Outline & Roadmap

Outline of what was done and what remains for the FYP resume NER project.

---

## 1. What Was Done

### 1.1 Data Pipeline

- **Existing data:** 220 resumes (DataTurks `entity_recognition_in_resumes.json`).
- **Dotin dataset:** 545 CVs (12 entity types) in XML; train + optional test set merged.
- **vrundag91 / Resume-Corpus-Dataset:** Label Studio JSON export supported; 36 entities mapped to unified schema.
- **minhquan / RESUME_NER_DATASET:** spaCy-style JSON supported; 12 entity types mapped to unified schema.
- **Unified schema:** All sources mapped to 6 entity types + O: **NAME, EMAIL, SKILL, OCCUPATION, EDUCATION, EXPERIENCE, O**.
- **Script:** `prepare_data.py` merges one or more of: `--existing`, `--dotin`, `--dotin-test`, `--vrundag`, `--minhquan` → single JSONL `merged_resume_ner.json`.
- **Current merged size:** 1,033 resumes (Dotin train + test + minhquan `data/`); can add `--existing` and/or `--vrundag` for more.

### 1.2 Model & Training

- **Architecture:** BERT (bert-base-uncased) + BiLSTM + CRF for token-level NER (BIO tags).
- **Input:** JSONL with `content` (full text) and `annotation` (list of `{label, points}`); converted to word-level BIO.
- **Train/val/test:** 80% / 10% / 10% split (shuffled, seed 42).
- **Training:** Cross-entropy loss (CRF), Adam optimizer, gradient clipping; early stopping (e.g. 5 epochs no improvement); optional LR scheduler for longer runs.
- **Checkpointing:** Best model by validation F1 saved; early stopping restores best checkpoint.
- **Results (typical):** Val micro F1 ~0.52, macro ~0.57; test micro F1 ~0.47. EMAIL and NAME strongest; SKILL/EXPERIENCE/EDUCATION moderate; some fragmentation (split spans, punctuation in spans).

### 1.3 Inference & Production Strategy

- **Hybrid extraction:**
  - **Rules (high recall):** NAME (heuristic: first Title-Case line), EMAIL (regex).
  - **Model:** SKILL, EXPERIENCE, EDUCATION, OCCUPATION (and fallback for NAME/EMAIL if rules miss).
- **Functions:** `parse_resume()` (model only), `parse_resume_hybrid()` (rules for NAME/EMAIL + model for rest).
- **Output:** Word-level tags + entity dict (type → list of phrases).

### 1.4 Save / Load

- **Save:** Model state, tokenizer, and config (tags, bert_name, num_labels) to a directory.
- **Default in Colab:** If Google Drive is mounted (`/content/drive/MyDrive` exists), save/load default to **`/content/drive/MyDrive/resume_ner`**; otherwise current directory.
- **Override:** Env vars `RESUME_NER_SAVE_DIR` and `RESUME_NER_LOAD_DIR`.

### 1.5 Documentation

- **README.md:** How to get Dotin, vrundag91, minhquan; merge command; label mapping (Dotin); run notebook.
- **PROCESS_OUTLINE.md:** This document (process + roadmap).

---

## 2. What Needs to Be Done (Checklist)

### 2.1 Before Submission / Demo

- [ ] **Run full pipeline once in target environment (Colab or local):** Load merged data → train → evaluate → save (to Drive if Colab).
- [ ] **Record final metrics:** Val/test F1 (micro/macro), per-entity precision/recall/F1, token accuracy; paste into report.
- [ ] **Demo hybrid inference:** Run `parse_resume_hybrid()` on 2–3 sample resumes; document that NAME/EMAIL come from rules, rest from model.
- [ ] **Save model to Google Drive (if using Colab):** Mount Drive before save so model persists; note path in report.
- [ ] **FYP report:** Describe problem, data (sources + unified schema), model (BERT-BiLSTM-CRF), training (loss, early stopping, metrics), hybrid approach, results, limitations, future work.

### 2.2 Optional Improvements (If Time)

- [ ] **Add existing 220 resumes to merge:** Run `prepare_data.py` with `--existing ../entity_recognition_in_resumes.json` for 1,253 total resumes; retrain and compare F1.
- [ ] **Add vrundag91 data:** Download Resume-Corpus-Dataset `data-files/`, run with `--vrundag`; retrain.
- [ ] **Class weights:** Weight SKILL/EXPERIENCE (and optionally EDUCATION) higher in loss to reduce under-prediction.
- [ ] **Post-processing:** Merge consecutive same-label spans; strip trailing punctuation from entity phrases.
- [ ] **LLM corrector (optional):** Second-stage agent that takes raw text + extracted entities and corrects/validates (with fallback to NER output if agent fails).

### 2.3 Future Work (Post–FYP)

- [ ] **Job-poster NER:** Separate model for job descriptions (JOB_TITLE, COMPANY, LOCATION, SKILLS, etc.); reuse same codebase, different data and label set.
- [ ] **More data / fine-tuning:** Integrate more resume NER datasets; aim for 80%+ F1 with larger data and/or fine-tuned BERT-for-NER.
- [ ] **Match pipeline:** Use resume NER + job-poster NER outputs for candidate–job matching (e.g. skill/experience overlap).

---

## 3. Quick Reference

| Item | Location / Command |
|------|--------------------|
| Merge data | `python prepare_data.py --dotin 545_cvs_train_v2 --dotin-test set_aside_test_v2_50cvs --minhquan data [--existing ...] [--vrundag ...] --output merged_resume_ner.json` |
| Train & evaluate | Run `resume_ner_pipeline/BERT_BiLSTM_CRF_Resume_NER.ipynb` cells 1–7 |
| Save model | Run notebook cell 8 (saves to Drive in Colab if mounted) |
| Load model | Run notebook cell 10 (loads from Drive in Colab if mounted) |
| Hybrid inference | Use `parse_resume_hybrid(text, tokenizer, model, device, ID2LABEL)` in notebook |
| Data format | JSONL: one line per resume, `{"content": "...", "annotation": [{"label": ["TYPE"], "points": [{"start", "end", "text"}]}]}` |

---

## 4. File Roles

| File | Role |
|------|------|
| `prepare_data.py` | Merge existing + Dotin + vrundag91 + minhquan → `merged_resume_ner.json` |
| `merged_resume_ner.json` | Single JSONL used by the notebook for training |
| `BERT_BiLSTM_CRF_Resume_NER.ipynb` | Load data, train, evaluate, save/load, hybrid inference |
| `README.md` | Dataset links, merge usage, label mapping |
| `PROCESS_OUTLINE.md` | This outline: process done + what needs to be done |
