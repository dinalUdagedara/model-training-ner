# FYP Resume NER: Changes and Decisions (Viva Reference)

This document records the main changes and design decisions made for the FYP submission notebook. Use it as a reference during your viva.

---

## 1. Notebook structure and submission cleanup

### 1.1 Data source: Google Drive only

- **Decision:** Data is loaded only from Google Drive (no local path fallback).
- **Reason:** Submission is intended for Google Colab; keeping a single data source keeps the notebook simple and reproducible for examiners.
- **Implementation:** `DATA_PATH` is set to `{MyDrive or "My Drive"}/merged_resume_ner.json`. Users must place `merged_resume_ner.json` in their My Drive root and mount Drive before running.

### 1.2 Mount Google Drive at the top

- **Decision:** A “Mount Google Drive” step was added immediately after Dependencies and before Data loading.
- **Reason:** Ensures Drive is mounted once at the start so all later steps (data load, and optionally save/load) work without extra instructions. Linear flow: mount → load data → train → evaluate.

### 1.3 Removed optional sections

- **Removed:** “Optional: Running on Google Colab” (redundant; mounting is now required at the top).
- **Removed:** “Optional: Extended training with LR scheduler” (one main training flow for submission).
- **Reason:** Cleaner, single-path notebook for submission and viva demos.

### 1.4 Comment and text cleanup

- **Shortened** Dependencies section to “Run once.” (removed “skip if your environment already has these”).
- **Removed** long inline comment in the data-loading cell (no local/Drive fallback explanation).
- **Kept** one-line docstrings for key functions (`create_bio_tags_fixed`, `align_to_bert`, `BertNERDataset`, `BertBiLSTMCRF`, `parse_resume`, `parse_resume_hybrid`) for readability.

---

## 2. Hyperparameter changes (aiming for 80%+ entity-level F1)

After an initial run gave ~53% entity-level F1 and 87% token accuracy, the following changes were made to improve entity F1 toward 80%+.

### 2.1 Training duration and early stopping

| Parameter   | Before | After | Reason |
|------------|--------|--------|--------|
| `EPOCHS`   | 30     | **60** | Validation F1 was still improving near epoch 27; more epochs allow further improvement. |
| `PATIENCE` | 7      | **12** | Avoid stopping too early when F1 plateaus briefly; give the model more time to improve. |

### 2.2 Learning rates

| Component        | Before | After   | Reason |
|-----------------|--------|--------|--------|
| BERT parameters | 1e-5   | **2e-5** | Slightly higher LR for BERT to learn resume-specific patterns without large overfitting risk. |
| Head (BiLSTM + CRF) | 5e-5 | **1e-4** | Task head can learn faster; common practice for NER with BERT. |

Differentiated learning rates are kept: BERT lower (fine-tune gently), head higher (learn task faster).

### 2.3 Dropout

| Parameter | Before | After | Reason |
|----------|--------|--------|--------|
| Model dropout | 0.4 | **0.3** | Slightly less regularization to reduce underfitting when targeting higher F1. |

---

## 3. Model and pipeline (unchanged)

- **Architecture:** BERT-base-uncased → BiLSTM → CRF (same as original design).
- **Entity types:** NAME, EMAIL, SKILL, OCCUPATION, EDUCATION, EXPERIENCE.
- **Data format:** JSONL with `content` and `annotation` (points + labels); BIO tagging; 80/10/10 train/val/test split, seed 42.
- **Inference:** Hybrid parsing (rule-based NAME/EMAIL, model for SKILL, OCCUPATION, EDUCATION, EXPERIENCE) as in the original notebook.

---

## 4. File and folder layout

- **Notebook:** `fyp/BERT_BiLSTM_CRF_Resume_NER_FYP.ipynb`
- **Data:** Prepared with `resume_ner_pipeline/prepare_data.py`; expected file: `merged_resume_ner.json` in Google Drive root.
- **README:** `fyp/README.md` — states Colab usage, Drive-only data, and mount step.

---

## 5. Quick viva answers

- **Why Google Drive only?** Submission is for Colab; one data path keeps the notebook simple and reproducible.
- **Why these learning rates?** BERT is fine-tuned gently (2e-5); the NER head learns faster (1e-4). This is a common pattern for BERT-based NER.
- **Why 60 epochs and patience 12?** Initial run showed F1 still improving after 27 epochs; we allow more training and avoid stopping too early.
- **Why lower dropout (0.3)?** To reduce underfitting when aiming for higher entity F1; 0.4 was quite strong regularization.

---

## 6. Other ways to increase accuracy (without more data)

If you are capped at ~1,033 resumes and want to push entity-level F1 further, try these in order.

### 6.1 Training and optimisation

- **Batch size:** Try `batch_size=16` in the DataLoader if GPU memory allows; can sometimes improve stability and F1.
- **Learning rate schedule:** Use a longer warmup (e.g. 15% of epochs instead of 10%) or decay to a lower end factor (e.g. `end_factor=0.1` instead of `0.2`) so the model trains longer at small LRs.
- **More epochs / patience:** If F1 is still rising at epoch 60, try `EPOCHS=80` and `PATIENCE=15`.

### 6.2 Class imbalance (oversample rare entities) — **implemented**

- EDUCATION, EXPERIENCE, OCCUPATION often have fewer examples than SKILL/NAME/EMAIL. A **weighted random sampler** is used in the notebook: samples that contain at least one of B/I-EDUCATION, B/I-EXPERIENCE, or B/I-OCCUPATION get weight 2.0, others 1.0, so the model sees rarer-entity resumes more often. Implemented in section 3 (BERT tokenizer and dataset) with `WeightedRandomSampler`.

### 6.3 Data augmentation (preserve spans)

- **Synonym replacement:** For tokens labeled **O** only, replace with a synonym occasionally (e.g. from a small word list) so the model sees more varied O-context without changing entity spans.
- **Duplicate + light noise:** Duplicate 10–20% of training resumes and apply only span-safe noise (e.g. normalise whitespace, optional lowercasing of O tokens). Do not change text inside annotated spans.

### 6.4 Model tweaks

- **Dropout:** Try `0.35` (between 0.3 and 0.4) if 0.3 overfits or 0.4 underfits.
- **BiLSTM depth:** Try a 2-layer BiLSTM for a bit more capacity (may need more data to benefit).

### 6.5 Post-processing and hybrid rules

- You already use rule-based NAME/EMAIL. Add a **small known-skills list** (e.g. "Python", "Java", "SQL") and, when the model predicts O for such a token in a skills-like context, optionally override to SKILL. Use sparingly to avoid false positives.

### 6.6 Ensemble

- Train **2–3 models** with different random seeds (e.g. 42, 123, 456). At inference, take **majority vote** per token (or average logits then decode). Ensembles often add 1–3% F1 at the cost of 2–3× inference time.
