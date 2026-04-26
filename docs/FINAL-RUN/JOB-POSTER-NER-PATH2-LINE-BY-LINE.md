# Job Poster NER Path 2 - Line-by-Line Understanding

Notebook: `fyp/job-poster-ner/BiLSTM_CRF_Job_Poster_NER_Path2_FYP.ipynb`  
Final path: Word2Vec -> BiLSTM -> CRF (from-scratch sequence model path)

---

## What this notebook does in one sentence

It trains and evaluates a job-poster NER model using Word2Vec embeddings and BiLSTM-CRF decoding, then runs hybrid inference with salary rules.

---

## Cell-by-cell explanation

## Cell 0 (Markdown) - Dependencies title
- Starts the notebook structure.

## Cell 1 (Code) - Install packages
- Installs `torch`, `pytorch-crf`, `seqeval`, `gensim`.
- Same role as resume notebook: training, CRF decoding, metrics, Word2Vec.

## Cell 2 (Markdown) - Drive mount section
- Section header.

## Cell 3 (Code) - Mount Google Drive (safe try/except)
- Tries to mount Drive when running in Colab.
- If not in Colab, prints a skip message.
- Why useful: supports both Colab and local execution.

## Cell 4 (Markdown) - Data loading section
- Section header.

## Cell 5 (Code) - Data load + label normalization
- Imports `json`, `os`.
- Chooses data path from Drive first, then local fallback.
- Loads JSONL job-posting records.
- Applies `LABEL_MAPPING` to standardize labels into:
  - JOB_TITLE, COMPANY, LOCATION, SALARY,
  - SKILLS_REQUIRED, EXPERIENCE_REQUIRED, EDUCATION_REQUIRED, JOB_TYPE.
- Why important: same class schema across all samples.

## Cell 6 (Markdown) - Preprocessing section
- Section header.

## Cell 7 (Code) - Tokenization, BIO tagging, train/val/test split
- Tokenizes with regex `\S+`.
- Aligns character spans to word tokens and produces BIO tags.
- Builds sentence/label arrays.
- Uses fixed-seed 80/10/10 split.
- Why important: clean split and reproducibility.

## Cell 8 (Markdown) - Embeddings section
- Section header.

## Cell 9 (Code) - Word2Vec + vocab + embedding matrix
- Trains Word2Vec embeddings on training text.
- Key settings:
  - `EMBED_DIM = 256`
  - `W2V_MIN_COUNT = 1`
  - `W2V_WINDOW = 6`
  - `W2V_EPOCHS = 35`
- Builds `word2id` mapping with PAD/UNK logic.
- Creates embedding matrix for model initialization.

## Cell 10 (Markdown) - Labels and dataset section
- Section header.

## Cell 11 (Code) - Dataset, padding, loaders, weighted sampler
- Defines tag list (`TAGS`) for 8 entity types + BIO/O.
- Creates `WordNERDataset`.
- Pads token IDs and labels for batching.
- Uses `MAX_LEN = 512`.
- Uses weighted sampling to reduce all-O bias:
  - `entity_tags` contains all entity BIO tags,
  - weight `3.5` for entity-rich samples, else `1.0`.
- DataLoader batch sizes:
  - train: `8`
  - validation: `12`
- Why important: stronger sampling pressure than resume path due to job-posting imbalance/noise.

## Cell 12 (Markdown) - Model section
- Section header.

## Cell 13 (Code) - BiLSTM-CRF model
- Defines BiLSTM-CRF architecture from scratch.
- Key config:
  - `HIDDEN_DIM = 384`
  - dropout around `0.35`
  - stacked bidirectional LSTM layers + CRF decode.
- Device selection: CUDA -> MPS -> CPU.

## Cell 14 (Markdown) - Training section
- Section header.

## Cell 15 (Code) - Training loop
- Validation metric: entity-level F1 via `seqeval`.
- Optimizer:
  - `Adam`, lr `5e-4`, weight_decay `5e-5`.
- Uses warmup + linear decay schedule.
- Main config:
  - `EPOCHS = 80`
  - `PATIENCE = 20`
- Saves best model state by validation F1 and early-stops if needed.
- Why important: balances convergence speed and overfit control.

## Cell 16 (Markdown) - Save section
- Section header.

## Cell 17 (Code) - Save model assets
- Saves into env-based or default path.
- Persists:
  - model state file,
  - config JSON (`tags`, `word2id`, dims, max_len),
  - Word2Vec model.
- Needed for backend inference deployment.

## Cell 18 (Markdown) - Inference section
- Section header.

## Cell 19 (Code) - Parser + hybrid salary rules
- Defines `parse_job_poster_path2(...)` for model prediction.
- Converts predicted BIO tags to entity dictionary.
- Includes cleanup/postprocessing for extracted spans.
- Defines `parse_job_poster_path2_hybrid(...)`:
  - keeps model output for most entities,
  - uses regex/rule extraction for salary.
- Why important: salary patterns are often format-driven, so hybrid improves practical extraction.

## Cell 20 (Code) - Demo inference text
- Uses sample job ad text.
- Runs parser and prints extracted entities.

## Cell 21 (Markdown) - Evaluation section
- Section header.

## Cell 22 (Code) - Validation and test metrics
- Runs `classification_report` and overall F1.
- Reports per-entity behavior and final held-out test performance.

---

## Viva points you must say for this notebook

- This is a full sequence model path, not a simple regex parser.
- Weighted sampling is intentionally aggressive (`3.5`) to avoid all-O collapse.
- Validation F1 drives checkpoint selection and early stopping.
- Hybrid salary extraction is a practical engineering choice.
- Saved artifacts allow direct backend deployment.

---

## One-minute spoken summary

For job posters, I used the same Path 2 architecture family: Word2Vec embeddings plus BiLSTM-CRF. I standardized labels, generated BIO sequences, and used a reproducible train/validation/test split. Because class imbalance was strong, I used weighted sampling to increase entity-rich samples. I trained with early stopping on validation F1, saved all deployment artifacts, and added a hybrid inference layer where salary is rule-assisted for better practical extraction quality.

---

## Basic meanings (very simple)

- **NER (Named Entity Recognition):** finding important job-posting information like JOB_TITLE, COMPANY, SALARY from text.
- **Tokenization:** splitting text into small pieces (mostly words).
- **Token:** one piece after splitting.
- **Label/Tag:** class attached to each token.
- **BIO format:** `B` begin, `I` inside, `O` outside entity.
- **Word2Vec:** turns each word into numbers so model can learn patterns.
- **Embedding:** that number vector for each word.
- **BiLSTM:** reads sequence in both directions to understand context better.
- **CRF:** picks the best valid full tag sequence.
- **Sequence model:** model predicts labels in order across the full sentence.
- **Train/Validation/Test:** learn, tune, final test.
- **Epoch:** one full round through train data.
- **Batch size:** number of samples per training step.
- **Optimizer (Adam):** updates model to reduce errors.
- **Learning rate:** step size of updates.
- **Scheduler:** changes learning rate over time.
- **Warmup:** starts with smaller learning rate first.
- **Early stopping:** stop when validation metric no longer improves.
- **Class imbalance:** some tags are much rarer than others.
- **Weighted sampling:** gives more chance to samples containing entities.
- **Inference:** prediction on new unseen job text.
- **Rule-based extraction:** regex/rules for formats (like salary patterns).
- **Hybrid extraction:** combine model extraction + rules for specific fields.
- **Precision:** among predicted entities, how many are correct.
- **Recall:** among true entities, how many were found.
- **F1 score:** balanced single score from precision and recall.
- **Entity-level F1:** checks complete entities, not only token-by-token correctness.
- **Held-out test set:** final unbiased evaluation set.

---

## How to say these in viva (short lines)

- **What is F1?**  
  F1 is a balanced score between precision and recall, so it gives a fair quality view.

- **Why tokenization first?**  
  The model cannot read raw paragraph directly; tokenization gives ordered units for labeling.

- **Why BiLSTM + CRF?**  
  BiLSTM learns context, and CRF improves sequence consistency.

- **Why hybrid salary logic?**  
  Salary often follows fixed text patterns, so regex helps improve practical extraction.

- **Why weighted sampling here?**  
  It reduces bias toward predicting `O` too often and helps entity learning.

