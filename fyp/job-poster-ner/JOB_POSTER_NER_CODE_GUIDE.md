# Job Poster NER — Code Block Guide

This document explains each code block in [BERT_BiLSTM_CRF_Job_Poster_NER_FYP.ipynb](BERT_BiLSTM_CRF_Job_Poster_NER_FYP.ipynb).

For the Resume NER notebook, see [../RESUME_NER_CODE_GUIDE.md](../RESUME_NER_CODE_GUIDE.md).

---

## Cell 0 (Markdown)

**Purpose:** Title and brief description.

Introduces the notebook: trains a BERT-BiLSTM-CRF model for job poster NER with entity types JOB_TITLE, COMPANY, LOCATION, SALARY, SKILLS_REQUIRED, EXPERIENCE_REQUIRED, EDUCATION_REQUIRED, JOB_TYPE. Data must be prepared with `prepare_data.py` in `job_poster_ner_pipeline/`.

---

## Cell 1 (Markdown)

**Purpose:** Section header for dependencies.

---

## Cell 2 (Code) — Dependencies

```python
!pip install -q torch transformers pytorch-crf seqeval
```

- **torch:** PyTorch for model training and inference
- **transformers:** Hugging Face BERT tokenizer and model
- **pytorch-crf:** CRF layer for sequence decoding
- **seqeval:** Entity-level F1/precision/recall (ignores padding and special tokens)

`-q` suppresses verbose install output.

---

## Cell 3 (Markdown)

**Purpose:** Section header for mounting Google Drive.

---

## Cell 4 (Code) — Mount Google Drive

```python
try:
    from google.colab import drive
    drive.mount("/content/drive")
    print("Drive mounted.")
except ImportError:
    print("Not in Colab – skip this cell when running locally.")
```

Mounts Google Drive in Colab. On local runs, skips gracefully with a message.

---

## Cell 5 (Markdown)

**Purpose:** Section header for data loading.

---

## Cell 6 (Code) — Data Loading

### Imports and path setup

- `_drive_base`: Uses `/content/drive/MyDrive` or `/content/drive/My Drive` depending on Colab setup
- `DATA_PATH`: First tries Drive path for `merged_job_poster_ner.json`
- Falls back to `../../job_poster_ner_pipeline/merged_job_poster_ner.json` when running from `fyp/job-poster-ner` locally
- Raises `FileNotFoundError` if no path exists

### Load JSONL

- Opens the file and parses each non-empty line as JSON
- Each line is one job posting with `content` and `annotation`
- Appends to `data` list

### Label mapping

- `LABEL_MAPPING`: Maps source labels (e.g. "Job Title", "Company", "Skill", "Occupation") to the unified schema: JOB_TITLE, COMPANY, LOCATION, SALARY, SKILLS_REQUIRED, EXPERIENCE_REQUIRED, EDUCATION_REQUIRED, JOB_TYPE, O
- Iterates over each item’s annotations and replaces labels using this mapping
- Unknown labels map to `"O"`

---

## Cell 7 (Markdown)

**Purpose:** Section header for preprocessing.

---

## Cell 8 (Code) — Preprocessing and Train/Val/Test Split

### `tokenize_with_positions(text)`

- Uses regex `\S+` to split text into non-whitespace tokens
- Returns `[(token, start, end), ...]` for character spans
- Needed to align annotations with tokens

### `create_bio_tags_fixed(tokens, annotations)`

- Builds BIO tags from annotation spans
- Skips annotations whose label is `"O"` (avoids B-O, I-O)
- For each span: first overlapping token → B-ENTITY, rest → I-ENTITY
- Returns a list of BIO labels aligned to `tokens`

### Build sentence/label lists

- Loops over `data`, extracts `content` and `annotation`
- Skips items with empty content or annotations
- Tokenizes, builds BIO tags, stores token lists in `all_sents` and label lists in `all_labels`

### Train/val/test split

- `random.seed(42)` for reproducibility
- Shuffles indices, then splits 80% train, 10% val, 10% test
- Produces `train_sents`, `train_labels`, `val_sents`, `val_labels`, `test_sents`, `test_labels`

---

## Cell 9 (Markdown)

**Purpose:** Section header for BERT tokenizer and dataset.

---

## Cell 10 (Code) — BERT Tokenizer and Dataset

### Tag and label mappings

- `TAGS`: All BIO tags for job poster entities (O, B-JOB_TITLE, I-JOB_TITLE, B-COMPANY, I-COMPANY, B-LOCATION, I-LOCATION, B-SALARY, I-SALARY, B-SKILLS_REQUIRED, I-SKILLS_REQUIRED, B-EXPERIENCE_REQUIRED, I-EXPERIENCE_REQUIRED, B-EDUCATION_REQUIRED, I-EDUCATION_REQUIRED, B-JOB_TYPE, I-JOB_TYPE)
- `LABEL2ID`: tag string → integer index
- `ID2LABEL`: integer index → tag string
- `NUM_LABELS`: number of classes (17)

### `align_to_bert(words, word_labels, tokenizer, max_len=512)`

Aligns word-level BIO labels to BERT subword tokens:

1. Builds subword sequence with [CLS], subwords for each word, [SEP]
2. Records index of first subword for each word in `first_idx`
3. Converts tokens to IDs, creates attention mask
4. Aligns labels: label only at `first_idx` positions, -100 elsewhere (ignored by loss)
5. Truncates to `max_len` if needed

Returns `(input_ids, attention_mask, aligned_labels)`.

### `BertNERDataset`

- PyTorch `Dataset` that wraps `(sents, labels)` and tokenizer
- `__getitem__` returns `(input_ids, mask, labels)` for one sample
- Drops samples where `len(words) != len(labels)`

### DataLoaders

- `collate`: Pads sequences to max length in the batch; pads labels with -100
- `rare_tags`: SALARY, EDUCATION_REQUIRED, JOB_TYPE, EXPERIENCE_REQUIRED (often under-represented in SkillSpan)
- `train_weights`: 2.0 for samples with rare entities, 1.0 otherwise
- `WeightedRandomSampler`: oversamples rare-entity samples
- `train_loader`: batch_size=8, sampler, collate_fn
- `val_loader`: batch_size=8, no sampler

---

## Cell 11 (Markdown)

**Purpose:** Section header for the model.

---

## Cell 12 (Code) — Model: BERT-BiLSTM-CRF

### `BertBiLSTMCRF`

1. **BERT:** `BertModel.from_pretrained("bert-base-uncased")` — 768-dim hidden state per token
2. **BiLSTM:** 1-layer bidirectional LSTM, hidden_dim=256 (128 per direction)
3. **Dropout:** 0.3 before LSTM and linear
4. **Linear:** 768 → num_labels (17 for job poster)
5. **CRF:** Decodes valid BIO sequences

**forward:**

- Training: returns negative log-likelihood (CRF loss). Labels -100 are masked.
- Inference: returns decoded tag sequences (list of lists) via `crf.decode`.

### Device selection

- Uses CUDA if available, else MPS (Apple Silicon), else CPU

### Optimizer

- **Differentiated learning rates:**
  - BERT (no decay): 2e-5
  - BERT (bias, LayerNorm): 2e-5, weight_decay=0
  - Head (no decay): 1e-4
  - Head (bias, LayerNorm): 1e-4, weight_decay=0
- `AdamW` with these parameter groups

---

## Cell 13 (Markdown)

**Purpose:** Section header for training.

---

## Cell 14 (Code) — Training

### `run_validation(model, val_loader, device, id2label, num_labels)`

- Sets model to eval, runs validation without gradients
- Collects true and predicted BIO sequences (ignoring -100)
- Returns `(f1_score, true_all, pred_all)` using seqeval’s entity-level F1

### Training loop

- `EPOCHS=60`, `PATIENCE=12`
- **LR scheduler:** warmup for 10% of epochs (factor 0.1), then linear decay to 20% of initial LR
- Each epoch: forward, backward, gradient clipping (1.0), optimizer step
- After each epoch: run validation, update `best_f1` and `best_state` if improved
- Early stop when no improvement for `PATIENCE` epochs
- Restores best checkpoint at the end

---

## Cell 15 (Markdown)

**Purpose:** Section header for saving.

---

## Cell 16 (Code) — Save Model and Tokenizer

- `_save_base`: Drive path in Colab, or `"."` locally
- `SAVE_DIR`: from env `JOB_POSTER_NER_SAVE_DIR` or default `{_save_base}/job_poster_ner`
- Saves:
  - `bert_bilstm_crf_state.pt`: model state dict
  - `ner_config.json`: TAGS, bert_name, num_labels
  - Tokenizer files (vocab.txt, etc.) via `tokenizer.save_pretrained`

---

## Cell 17 (Markdown)

**Purpose:** Section header for loading and inference.

---

## Cell 18 (Code) — Load Model and Inference

### Load

- `LOAD_DIR`: from env `JOB_POSTER_NER_LOAD_DIR` or default (Drive or local)
- Loads config from `ner_config.json`
- Rebuilds TAGS, LABEL2ID, ID2LABEL, NUM_LABELS
- Loads tokenizer and model, restores weights from `.pt`

### `parse_job_poster(text, tokenizer, model, device, id2label, max_len=512)`

1. Tokenizes text into words with regex `\S+`
2. Builds BERT subword sequence, records `first_idx` per word
3. Truncates to `max_len` if needed
4. Runs model in eval mode, gets CRF decode output
5. Maps predicted indices to tags at `first_idx` positions
6. Converts BIO tags to entity dict: B-X starts entity, I-X continues it
7. **Post-processing:** strips trailing punctuation (.,;:!?)]}\"') from entity phrases
8. Deduplicates entities per type (case-sensitive)
9. Returns `(words, pred_tags, entities)`

### `extract_salary_rules(text)`

- Uses regex to find salary patterns: `$80k-120k`, `£50k`, `Competitive`, `100k-150k`, etc.
- Returns deduplicated list of matched strings

### `parse_job_poster_hybrid(text, tokenizer, model, device, id2label, max_len=512)`

- Runs `parse_job_poster` for model-based entities
- Overwrites SALARY with `extract_salary_rules` result (rules give high recall for salary phrases)
- Returns `(words, pred_tags, entities)`

---

## Cell 19 (Code) — Demo Inference

- Defines sample job poster text
- Calls `parse_job_poster_hybrid`
- Prints entities and first 30 word-level tags

---

## Cell 20 (Markdown)

**Purpose:** Section header for evaluation.

---

## Cell 21 (Markdown)

**Purpose:** Subsection for validation evaluation.

---

## Cell 22 (Code) — Validation Evaluation

- Runs model on validation set (no grad)
- Collects true and predicted BIO sequences
- Prints seqeval `classification_report` (precision, recall, F1 per entity)
- Prints overall entity-level F1
- Computes token accuracy (correct tokens / total non-padding tokens)

---

## Cell 23 (Markdown)

**Purpose:** Subsection for test evaluation.

---

## Cell 24 (Code) — Test Set Evaluation

- Builds `test_ds` and `test_loader` from test split
- Same evaluation logic as validation
- Prints classification report and Test F1
- Test set is held out and never used for training or early stopping

---

## Differences from Resume NER

| Aspect | Resume NER | Job Poster NER |
| ------ | ---------- | --------------- |
| Entity types | NAME, EMAIL, SKILL, OCCUPATION, EDUCATION, EXPERIENCE | JOB_TITLE, COMPANY, LOCATION, SALARY, SKILLS_REQUIRED, EXPERIENCE_REQUIRED, EDUCATION_REQUIRED, JOB_TYPE |
| TAGS count | 13 | 17 |
| Rare tags | EDUCATION, EXPERIENCE, OCCUPATION | SALARY, EDUCATION_REQUIRED, JOB_TYPE, EXPERIENCE_REQUIRED |
| Hybrid rules | NAME (heuristic), EMAIL (regex) | SALARY (regex) |
| Data file | merged_resume_ner.json | merged_job_poster_ner.json |
| Save/load env | RESUME_NER_SAVE_DIR, RESUME_NER_LOAD_DIR | JOB_POSTER_NER_SAVE_DIR, JOB_POSTER_NER_LOAD_DIR |
| Entity post-process | None | Strip punctuation, dedupe |
