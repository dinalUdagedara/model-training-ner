# Resume NER Pipeline (merged data)

This folder contains the **merged pipeline**: your existing 220 resumes + Dotin 545 + optional **vrundag91** and **minhquan** datasets for more training data.

## 1. Get the datasets

### Dotin (required or use existing)

1. Go to: https://github.com/dotin-inc/resume-dataset-NER-annotations  
2. Download **545_cvs_train_v2.zip** (and optionally **set_aside_test_v2_50cvs.zip**)  
3. Unzip into a folder (e.g. `545_cvs_train_v2/`, `set_aside_test_v2_50cvs/`).

### vrundag91 / Resume-Corpus-Dataset (optional, more resumes)

1. Clone or download: https://github.com/vrundag91/Resume-Corpus-Dataset  
2. Use the **data-files/** folder path (contains `*.json` Label Studio exports).

### minhquan / RESUME_NER_DATASET (optional, 120 CVs, spaCy format)

1. Clone or download: https://github.com/minhquan23102000/RESUME_NER_DATASET  
2. Use the **data/** folder path (contains spaCy-style JSON files).

## 2. Merge data (run once)

From this folder (`resume_ner_pipeline`), run:

```bash
# Merge existing + Dotin + vrundag91 + minhquan into merged_resume_ner.json
python prepare_data.py \
  --existing "../entity_recognition_in_resumes.json" \
  --dotin "545_cvs_train_v2" \
  --dotin-test "set_aside_test_v2_50cvs" \
  --vrundag "/path/to/Resume-Corpus-Dataset/data-files" \
  --minhquan "/path/to/RESUME_NER_DATASET/data" \
  --output merged_resume_ner.json
```

- **`--existing`**: Path to your current `entity_recognition_in_resumes.json` (220 resumes).  
- **`--dotin`**: Path to **Dotin train** XML folder (e.g. `545_cvs_train_v2/`).  
- **`--dotin-test`**: (Optional) Path to **Dotin test set** XML folder.  
- **`--vrundag`**: (Optional) Path to **vrundag91** `data-files/` folder.  
- **`--minhquan`**: (Optional) Path to **minhquan** `data/` folder.  
- **`--output`**: Output file (default: `merged_resume_ner.json`).

You must provide **at least one** of `--existing`, `--dotin`, `--vrundag`, or `--minhquan`.

**Example without extra datasets** (existing + Dotin only):

```bash
python prepare_data.py \
  --existing "../entity_recognition_in_resumes.json" \
  --dotin "545_cvs_train_v2" \
  --dotin-test "set_aside_test_v2_50cvs" \
  --output merged_resume_ner.json
```

**Dotin-only**:

```bash
python prepare_data.py --dotin 545_cvs_train_v2 --output merged_resume_ner.json
```

After this, `merged_resume_ner.json` will be in this folder.

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
