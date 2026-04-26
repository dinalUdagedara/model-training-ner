# Resume NER Path 2 - Line-by-Line Understanding

Notebook: `fyp/BiLSTM_CRF_Resume_NER_Path2_FYP.ipynb`  
Final path: Word2Vec -> BiLSTM -> CRF (no transformer encoder in this path)

---

## What this notebook does in one sentence

It trains a resume NER model using Word2Vec embeddings and a BiLSTM-CRF sequence tagger, then evaluates and runs inference.

---

## Cell-by-cell explanation

## Cell 0 (Markdown) - Title
- Introduces the notebook as Resume NER with BiLSTM-CRF.
- Sets expectation that this is the Path 2 model flow.

## Cell 1 (Markdown) - Dependencies section
- Just a section header.

## Cell 2 (Code) - Install packages
- Installs `torch`, `pytorch-crf`, `seqeval`, `gensim`.
- Meaning:
  - `torch`: deep learning framework.
  - `pytorch-crf`: CRF decoding layer for valid tag sequences.
  - `seqeval`: entity-level metrics (precision/recall/F1).
  - `gensim`: Word2Vec training.

## Cell 3 (Markdown) - Colab drive section
- Section header for Google Drive mounting.

## Cell 4 (Code) - Mount Google Drive
- Mounts drive at `/content/drive`.
- Purpose: load JSONL dataset and save model artifacts in Colab.

## Cell 5 (Markdown) - Data loading section
- Section header.

## Cell 6 (Code) - Data load + label mapping
- Imports core modules (`json`, `os`).
- Resolves Drive base path (`MyDrive` vs `My Drive`).
- Sets dataset file path in Drive root.
- Opens JSONL line by line and loads each sample.
- Defines `LABEL_MAPPING` to normalize label names into your fixed schema.
- Applies mapping to every annotation label.
- Why important: this guarantees clean and consistent entity classes before training.

## Cell 7 (Markdown) - Preprocessing section
- Section header.

## Cell 8 (Code) - Tokenization, BIO tags, data split
- Uses regex tokenization (`\S+`) with character positions.
- Converts span annotations to BIO tags (`B-`, `I-`, `O`).
- Builds token/label pairs for all valid samples.
- Uses `random.seed(42)` and splits data 80/10/10 (train/val/test).
- Why important: makes evaluation reproducible and prevents leakage.

## Cell 9 (Markdown) - Word embeddings section
- Section header.

## Cell 10 (Code) - Train Word2Vec + build vocab/embedding matrix
- Trains Word2Vec on training sentences.
- Main settings:
  - `EMBED_DIM = 256`
  - `W2V_MIN_COUNT = 1`
  - `W2V_WINDOW = 6`
  - `W2V_EPOCHS = 35`
- Builds token vocabulary (`word2id`) with PAD/UNK handling.
- Creates embedding matrix from Word2Vec vectors.
- Unknown words are initialized with small random vectors.
- Why important: this is your input representation layer for the BiLSTM model.

## Cell 11 (Markdown) - Dataset section
- Section header.

## Cell 12 (Code) - Dataset class, padding, loaders, weighted sampling
- Defines `WordNERDataset` for word-level IDs and tag IDs.
- Pads sequences in `collate_pad`.
- Sets `MAX_LEN = 768`.
- Creates train/validation datasets.
- Uses weighted sampling to fight imbalance:
  - rare tags include SKILL, EDUCATION, EXPERIENCE, OCCUPATION.
  - sample weights: `2.5` if sample contains rare tags, otherwise `1.0`.
- DataLoader batch sizes:
  - train: `6`
  - validation: `12`
- Why important: prevents the model from collapsing into mostly `O` predictions.

## Cell 13 (Markdown) - Model section
- Section header.

## Cell 14 (Code) - BiLSTM-CRF model definition
- Defines model class with:
  - embedding layer (from Word2Vec matrix),
  - BiLSTM stack,
  - linear projection to tag logits,
  - CRF layer.
- Key config:
  - `HIDDEN_DIM = 384`
  - dropout around `0.35`
  - LSTM uses bidirectional + stacked layers.
- Selects device: CUDA, else MPS, else CPU.
- Why important: CRF enforces better tag transitions than plain token-wise softmax.

## Cell 15 (Markdown) - Training section
- Section header.

## Cell 16 (Code) - Training loop + early stopping + scheduler
- Uses `seqeval` F1 for validation monitoring.
- Optimizer:
  - `Adam`, lr `1e-3`, weight_decay `5e-5`.
- Scheduler strategy:
  - short warmup (very low-to-normal),
  - then linear decay.
- Main training config:
  - `EPOCHS = 120`
  - `PATIENCE = 25`
- Each epoch:
  - train pass, gradient clipping, optimizer step,
  - validation F1 check,
  - save best state by validation F1.
- Early stopping if no improvement for patience window.
- Why important: keeps best checkpoint and avoids overfitting.

## Cell 17 (Markdown) - Save section
- Section header.

## Cell 18 (Code) - Save model artifacts
- Builds save directory from env var or default Drive path.
- Saves:
  - model weights (`bilstm_crf_state.pt`),
  - config JSON (tags, vocab map, dimensions, max_len),
  - Word2Vec model (`word2vec.model`).
- Why important: backend/runtime needs these artifacts for inference.

## Cell 19 (Markdown) - Evaluation section
- Section header.

## Cell 20 (Code) - Validation + test evaluation
- Runs entity-level evaluation with `classification_report`.
- Reports:
  - per-entity precision/recall/F1,
  - overall F1 for validation and test sets.
- Keeps test split strictly held out from training/early-stop decisions.

## Cell 21 (Markdown) - Inference section
- Section header.

## Cell 22 (Code) - Inference parser function
- Defines `parse_resume_path2(...)`.
- Steps:
  - tokenize input text,
  - convert words to IDs,
  - run model decoding,
  - map tag IDs back to labels,
  - convert BIO sequence to entity dictionary.
- This is your runtime extraction logic for resume entities.

## Cell 23 (Markdown) - Example section
- Section header.

## Cell 24 (Code) - Demo examples
- Provides sample resume text(s),
- Calls parser and prints extracted entities.
- Purpose: quick sanity check before integrating into backend.

---

## Viva points you must say for this notebook

- This path uses Word2Vec + BiLSTM + CRF as a classical, controllable sequence-tagging pipeline.
- Weighted sampling is used to handle class imbalance.
- Early stopping uses validation F1, not training loss alone.
- Test set is held out for final reporting only.
- Artifacts are saved for deployment-time inference.

---

## One-minute spoken summary

I used a full sequence-tagging pipeline for resume NER: Word2Vec for embeddings, BiLSTM for context, and CRF for structured BIO decoding. I normalized labels, generated BIO tags, and split data into train/validation/test with a fixed seed. During training, I used weighted sampling for rare entities, early stopping on validation F1, and LR scheduling. Finally, I saved model weights, config, and Word2Vec vectors, then validated extraction through inference examples and held-out test metrics.

---

## Basic meanings (very simple)

- **NER (Named Entity Recognition):** finding important words/phrases like NAME, EMAIL, SKILL from normal text.
- **Tokenization:** splitting text into smaller pieces (usually words) so the model can read them.
- **Token:** one small unit after tokenization (for example `Python` or `Engineer`).
- **Label:** the class/tag given to a token (for example `B-SKILL` or `O`).
- **BIO tagging:** way to mark entities:
  - `B` = beginning of an entity,
  - `I` = inside/continuing the same entity,
  - `O` = outside any entity.
- **Word2Vec:** converts each word into numbers (a vector) so model can learn word meaning patterns.
- **Embedding:** that numeric vector representation of a word.
- **BiLSTM:** model that reads sequence in both directions (left->right and right->left) to understand context.
- **CRF:** final decoding layer that chooses a valid best tag sequence (reduces weird tag jumps).
- **Sequence tagging:** giving one label to each token in order.
- **Train/Validation/Test split:** data division:
  - train = learn,
  - validation = tune/check during training,
  - test = final unbiased check.
- **Epoch:** one full pass over all training data.
- **Batch size:** how many samples are processed together in one training step.
- **Optimizer (Adam):** algorithm that updates model weights to reduce error.
- **Learning rate (LR):** how big each update step is.
- **Scheduler:** automatically changes LR during training.
- **Warmup:** start with smaller LR first, then increase to normal.
- **Early stopping:** stop training when validation score stops improving.
- **Class imbalance:** some entity types appear much less than others.
- **Weighted sampling:** showing rare-entity examples more often while training.
- **Overfitting:** model memorizes training data too much and performs worse on new data.
- **Inference:** using trained model on new unseen text.
- **Precision:** out of predicted entities, how many are correct.
- **Recall:** out of real entities, how many model found.
- **F1 score:** balance between precision and recall (higher is better, 1.0 is perfect).
- **Entity-level F1:** F1 calculated on whole entities/spans, not just single tokens.
- **Token accuracy:** percent of tokens with correct labels.
- **Held-out test set:** test data never used for training/tuning, so results are more trustworthy.
- **Reproducible (seed=42):** same seed helps get consistent split/results across reruns.

---

## How to say these in viva (short lines)

- **What is F1?**  
  F1 is one score that balances precision and recall. I use it because both false positives and missed entities matter.

- **What is tokenization?**  
  Tokenization is splitting text into word pieces so the model can process text step by step.

- **Why BIO tags?**  
  BIO tags help the model know where an entity starts and where it continues.

- **Why CRF after BiLSTM?**  
  CRF helps enforce valid tag sequences, so outputs are more consistent than independent token predictions.

- **Why weighted sampling?**  
  Some entities are rare, so weighted sampling prevents the model from predicting mostly `O`.

