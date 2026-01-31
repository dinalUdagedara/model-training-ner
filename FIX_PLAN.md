# Fix Plan: Resume NER (Rule-Compliant)

## Goal
Improve F1 from ~0.11 while staying within **Rules**: BiLSTM-CRF core, BERT only as feature (embeddings), same data & BIO, seqeval metrics.

---

## Step 1 – Data & labels (do first)

1. **Use fixed `create_bio_tags`**
   - Skip any annotation whose normalized label is `"O"` (so you never produce `B-O` / `I-O`).
   - Use this version everywhere you build BIO from annotations.

2. **Build train/val/test from JSON in memory**
   - From `data`: for each item, `tokenize_with_positions(content)` then `create_bio_tags(tokens, annotation)`.
   - Split 80% train, 10% val, 10% test (or 80/20 if you prefer).
   - Result: `train_sents`, `train_labels`, `val_sents`, `val_labels`, `test_sents`, `test_labels` (list of token lists, list of label lists).

3. **Optional: re-save to files**
   - If you still want `train.txt` / `valid.txt` / `test.txt`, write them from the above lists so they never contain `B-O`/`I-O`.

---

## Step 2 – BERT + BiLSTM-CRF (main fix)

1. **Tokenization**
   - Use a BERT tokenizer (e.g. `bert-base-uncased`).
   - For each sample: tokenize the **words** (your existing word list) into subwords; keep a mapping from word index → first subword index.

2. **Label alignment**
   - One label per **word** (BIO). For each word, assign its label to the **first subword** position; set **-100** for all other subwords and for special tokens ([CLS], [SEP], padding). Result: one label id per BERT input position (padded with -100).

3. **Model**
   - **BERT** (frozen or fine-tuned) → last hidden state `[batch, seq, 768]`.
   - Optional: linear to reduce 768 → `hidden_dim` (e.g. 256).
   - **BiLSTM** on top (same as now: 1 layer, bidirectional, optional dropout).
   - **Linear** → num_labels, then **CRF**.
   - Pipeline: Tokenization → BERT embeddings → BiLSTM → CRF → Prediction (unchanged).

4. **Training**
   - Loss: CRF negative log-likelihood; **mask** = valid positions (not padding), labels use -100 at padding.
   - Optimizer: Adam, lr e.g. 2e-5 if fine-tuning BERT, or 1e-3 for only BiLSTM+CRF.
   - Batch size 8 or 16; a few epochs (3–5 if BERT is tuned).

5. **Evaluation**
   - Decode with CRF; for each sample build the **label list** only for **non-padding** positions (mask or label != -100).
   - Pass to seqeval as **list of lists** (one list of tag strings per sample). Report precision, recall, F1 and per-entity metrics.

---

## Step 3 – Optional tweaks (Rules allow)

- Add **dropout** in BiLSTM (e.g. 0.3–0.5).
- Tune **batch size**, **learning rate**, **epochs**.
- If sequences are long, **truncate** to 512 BERT tokens or split into segments; keep label alignment consistent.

---

## Files / code

- **`bert_bilstm_crf_pipeline.py`** – Standalone pipeline that assumes `data` (list of JSON items) is already loaded. Run after the notebook cells that load the JSON. It builds data with the fixed `create_bio_tags`, aligns BERT labels, defines BERT-BiLSTM-CRF, trains and evaluates with seqeval.

---

## Summary

| What              | Action                                      |
|------------------|---------------------------------------------|
| Core model       | Keep BiLSTM-CRF                             |
| Input features   | Replace random embeddings with BERT        |
| Labels           | Fix BIO (no B-O); align to BERT subwords    |
| Metrics          | seqeval, list-of-lists, strip padding       |
| Rules            | No new architecture; BERT = feature only    |
