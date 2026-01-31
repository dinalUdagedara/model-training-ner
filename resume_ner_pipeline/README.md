# Resume NER Pipeline (merged data)

This folder contains the **merged pipeline**: your existing 220 resumes + Dotin 545 resumes, for better BERT-BiLSTM-CRF training.

## 1. Get the Dotin dataset

1. Go to: https://github.com/dotin-inc/resume-dataset-NER-annotations  
2. Download **545_cvs_train_v2.zip** (and optionally **set_aside_test_v2_50cvs.zip**)  
3. Unzip into a folder, e.g. `dotin_data/`.  
   - If the zip contains a single JSON file (one JSON object per line), note its path.  
   - If it contains many JSON files, use the folder path.

## 2. Merge data (run once)

From this folder (`resume_ner_pipeline`), run:

```bash
# Merge existing 220 + Dotin train (545 XMLs) + Dotin test (50 XMLs) into merged_resume_ner.json
python prepare_data.py \
  --existing "../entity_recognition_in_resumes.json" \
  --dotin "545_cvs_train_v2" \
  --dotin-test "set_aside_test_v2_50cvs" \
  --output merged_resume_ner.json
```

- **`--existing`**: Path to your current `entity_recognition_in_resumes.json` (220 resumes).  
- **`--dotin`**: Path to **Dotin train** XML folder (e.g. `545_cvs_train_v2/` from the zip).  
- **`--dotin-test`**: (Optional) Path to **Dotin test set** XML folder (e.g. `set_aside_test_v2_50cvs/`).  
- **`--output`**: Output file (default: `merged_resume_ner.json`).

**Dotin-only** (if you don’t have the 220 file in this repo):

```bash
python prepare_data.py --dotin /path/to/dotin_extracted --output merged_resume_ner.json
```

**Existing-only** (copy and normalize only):

```bash
python prepare_data.py --existing ../entity_recognition_in_resumes.json --output merged_resume_ner.json
```

After this, `merged_resume_ner.json` should be in this folder.

## 3. Run the notebook

1. Open **BERT_BiLSTM_CRF_Resume_NER.ipynb** in Cursor or Jupyter.  
2. Use a local Python kernel (or Colab).  
3. Run all cells in order.

The notebook loads **merged_resume_ner.json** by default (fallback: `entity_recognition_in_resumes.json` if present).  
Train/val/test split, model, training, evaluation, save/load, and parse cells are the same as the original pipeline.

## Label mapping (Dotin → unified)

Dotin’s 12 entities are mapped to the 6 used in the notebook:

| Dotin              | Unified   |
|--------------------|-----------|
| Name               | NAME      |
| Email Address      | EMAIL     |
| Designation        | OCCUPATION|
| Degree, College Name, Graduation Year | EDUCATION |
| Company, Years of Experience | EXPERIENCE |
| Job Specific Skill, Soft Skills, Tech Tools | SKILL |
| Location           | O         |

## Files in this folder

- **prepare_data.py** – Merges existing + Dotin JSON and writes `merged_resume_ner.json`.  
- **BERT_BiLSTM_CRF_Resume_NER.ipynb** – Same BERT-BiLSTM-CRF pipeline, uses merged data by default.  
- **README.md** – This file.

After merging, you’ll also have **merged_resume_ner.json** (created by `prepare_data.py`).
