# Resume NER — Code Block Guide

This document explains each code block in [BERT_BiLSTM_CRF_Resume_NER_FYP.ipynb](BERT_BiLSTM_CRF_Resume_NER_FYP.ipynb).

For the Job Poster NER notebook, see [job-poster-ner/JOB_POSTER_NER_CODE_GUIDE.md](job-poster-ner/JOB_POSTER_NER_CODE_GUIDE.md).

---

## Cell 0 (Markdown)

**Purpose:** Title and brief description.

Introduces the notebook: trains a BERT-BiLSTM-CRF model for resume NER with entity types NAME, EMAIL, SKILL, OCCUPATION, EDUCATION, EXPERIENCE. Data must be prepared with `prepare_data.py` in `resume_ner_pipeline/`.

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
from google.colab import drive
drive.mount("/content/drive")
```

Mounts Google Drive so the notebook can load `merged_resume_ner.json` from My Drive. Required for Colab; skip when running locally with a local data path.

---

## Cell 5 (Markdown)

**Purpose:** Section header for data loading.

---

## Cell 6 (Code) — Data Loading

### Imports and path setup

- `_drive_base`: Uses `/content/drive/MyDrive` or `/content/drive/My Drive` depending on Colab setup
- `DATA_PATH`: Path to `merged_resume_ner.json` in Drive root
- Raises `FileNotFoundError` if the file is missing

### Load JSONL

- Opens the file and parses each non-empty line as JSON
- Each line is one resume with `content` and `annotation`
- Appends to `data` list

### Label mapping

- `LABEL_MAPPING`: Maps source labels (e.g. "Name", "Email Address", "Skills") to the unified schema: NAME, EMAIL, SKILL, OCCUPATION, EDUCATION, EXPERIENCE, O
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

- `TAGS`: All BIO tags (O, B-NAME, I-NAME, B-EMAIL, …)
- `LABEL2ID`: tag string → integer index
- `ID2LABEL`: integer index → tag string
- `NUM_LABELS`: number of classes

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
- `rare_tags`: EDUCATION, EXPERIENCE, OCCUPATION (often under-represented)
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
4. **Linear:** 768 → num_labels
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

- `SAVE_DIR`: from env `RESUME_NER_SAVE_DIR` or default `"resume_ner"`
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

- Loads config from `ner_config.json`
- Rebuilds TAGS, LABEL2ID, ID2LABEL, NUM_LABELS
- Loads tokenizer and model, restores weights from `.pt`

### `parse_resume(text, tokenizer, model, device, id2label, max_len=512)`

1. Tokenizes text into words with regex `\S+`
2. Builds BERT subword sequence, records `first_idx` per word
3. Truncates to `max_len` if needed
4. Runs model in eval mode, gets CRF decode output
5. Maps predicted indices to tags at `first_idx` positions
6. Converts BIO tags to entity dict: B-X starts entity, I-X continues it
7. Returns `(words, pred_tags, entities)`

### `extract_email_rules(text)`

- Uses regex to find email-like strings
- Returns deduplicated list

### `extract_name_heuristic(text)`

- Looks at first few lines
- Skips lines with @, http, www
- Picks first line that looks like a name: 1–4 Title-Case words, length < 80, no trailing period

### `parse_resume_hybrid(text, tokenizer, model, device, id2label, max_len=512)`

- Runs `parse_resume` for model-based entities
- Overwrites NAME with `extract_name_heuristic` result
- Overwrites EMAIL with `extract_email_rules` result
- Returns `(words, pred_tags, entities)`

---

## Cell 19 (Code) — Demo Inference

- Defines sample resume text
- Calls `parse_resume_hybrid`
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
