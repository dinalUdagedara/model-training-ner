"""
BERT-BiLSTM-CRF pipeline for Resume NER (rule-compliant fix).
Assumes `data` is already loaded: list of dicts with 'content' and 'annotation'.
Run after the notebook cells that load JSON and apply label_mapping.

Usage in Colab:
  1. Run cells that load data, label_mapping, tokenize_with_positions, create_bio_tags (fixed).
  2. Run: from bert_bilstm_crf_pipeline import build_and_train_bert_bilstm_crf
  3. build_and_train_bert_bilstm_crf(data, ...)
Or paste this file's contents into notebook cells.
"""

import re
import random
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import BertModel, BertTokenizer

# Try torchcrf; if not installed: pip install pytorch-crf
try:
    from torchcrf import CRF
except ImportError:
    CRF = None  # fallback: use simple cross-entropy if CRF not available

# --- Label and tag setup (must match notebook) ---
LABEL_MAPPING = {
    "Name": "NAME",
    "Email Address": "EMAIL",
    "Skills": "SKILL",
    "Designation": "OCCUPATION",
    "Degree": "EDUCATION",
    "College Name": "EDUCATION",
    "Graduation Year": "EDUCATION",
    "Companies worked at": "EXPERIENCE",
    "Years of Experience": "EXPERIENCE",
    "Location": "O",
    "UNKNOWN": "O",
}

TAGS = [
    "O", "B-NAME", "I-NAME", "B-EMAIL", "I-EMAIL",
    "B-SKILL", "I-SKILL", "B-OCCUPATION", "I-OCCUPATION",
    "B-EXPERIENCE", "I-EXPERIENCE", "B-EDUCATION", "I-EDUCATION",
]
LABEL2ID = {t: i for i, t in enumerate(TAGS)}
ID2LABEL = {i: t for i, t in enumerate(TAGS)}
NUM_LABELS = len(TAGS)


def tokenize_with_positions(text):
    """Tokenize into words with (start, end) character positions."""
    tokens = []
    for match in re.finditer(r"\S+", text):
        tokens.append((match.group(), match.start(), match.end()))
    return tokens


def create_bio_tags_fixed(tokens, annotations):
    """
    Create BIO labels; skip entities with label 'O' (no B-O / I-O).
    tokens: list of (text, start, end)
    annotations: list of dicts with 'label' and 'points' (start, end).
    """
    bio_labels = ["O"] * len(tokens)
    for ann in annotations:
        if not ann.get("label"):
            continue
        entity_label = ann["label"][0]
        if entity_label == "O":
            continue
        for point in ann.get("points", []):
            s, e = point["start"], point["end"]
            first = True
            for i, (_, ts, te) in enumerate(tokens):
                if te <= s:
                    continue
                if ts >= e:
                    break
                bio_labels[i] = f"B-{entity_label}" if first else f"I-{entity_label}"
                first = False
    return bio_labels


def build_splits_from_data(data, label_mapping=None, train_ratio=0.8, val_ratio=0.1, seed=42):
    """
    Build train_sents, train_labels, val_sents, val_labels, test_sents, test_labels
    from raw `data` using fixed create_bio_tags. Apply label_mapping to annotations first.
    """
    if label_mapping is None:
        label_mapping = LABEL_MAPPING
    all_sents, all_labels = [], []
    for item in data:
        content = item.get("content", "")
        annotations = item.get("annotation", [])
        if not content or not annotations:
            continue
        # Apply label_mapping to annotation labels
        anns = []
        for a in annotations:
            old_labels = a.get("label", [])
            new_labels = [label_mapping.get(l, "O") for l in old_labels]
            anns.append({"label": new_labels, "points": a.get("points", [])})
        tokens = tokenize_with_positions(content)
        if not tokens:
            continue
        labels = create_bio_tags_fixed(tokens, anns)
        words = [t[0] for t in tokens]
        all_sents.append(words)
        all_labels.append(labels)

    n = len(all_sents)
    random.seed(seed)
    idx = list(range(n))
    random.shuffle(idx)
    n_train = int(n * train_ratio)
    n_val = int(n * val_ratio)
    n_test = n - n_train - n_val
    train_idx = idx[:n_train]
    val_idx = idx[n_train : n_train + n_val]
    test_idx = idx[n_train + n_val :]

    train_sents = [all_sents[i] for i in train_idx]
    train_labels = [all_labels[i] for i in train_idx]
    val_sents = [all_sents[i] for i in val_idx]
    val_labels = [all_labels[i] for i in val_idx]
    test_sents = [all_sents[i] for i in test_idx]
    test_labels = [all_labels[i] for i in test_idx]
    return train_sents, train_labels, val_sents, val_labels, test_sents, test_labels


def align_labels_to_bert_tokenizer(words, word_labels, tokenizer, max_length=512):
    """
    Map word-level BIO labels to BERT subword positions.
    Returns: input_ids, attention_mask, aligned_label_ids (with -100 for non-first subwords and special tokens).
    """
    first_subword_indices = []
    subword_tokens = ["[CLS]"]
    for w in words:
        pieces = tokenizer.tokenize(w)
        if not pieces:
            pieces = [tokenizer.unk_token]
        first_subword_indices.append(len(subword_tokens))
        subword_tokens.extend(pieces)
    subword_tokens.append("[SEP]")

    input_ids = tokenizer.convert_tokens_to_ids(subword_tokens)
    attention_mask = [1] * len(input_ids)
    aligned = [-100] * len(input_ids)
    for pos, label in zip(first_subword_indices, word_labels):
        if pos < len(aligned):
            aligned[pos] = LABEL2ID.get(label, LABEL2ID["O"])

    if len(input_ids) > max_length:
        input_ids = input_ids[: max_length - 1] + [tokenizer.sep_token_id]
        attention_mask = attention_mask[: max_length - 1] + [1]
        aligned = aligned[: max_length - 1] + [-100]

    return input_ids, attention_mask, aligned


def collate_bert_batch(batch):
    """Batch: list of (input_ids, attention_mask, label_ids). Pad to max_len in batch."""
    max_len = max(len(b[0]) for b in batch)
    pad_id = 0  # BERT pad_token_id
    input_ids = []
    attention_mask = []
    labels = []
    for ids, mask, labs in batch:
        pad_len = max_len - len(ids)
        input_ids.append(ids + [pad_id] * pad_len)
        attention_mask.append(mask + [0] * pad_len)
        labels.append(labs + [-100] * pad_len)
    return (
        torch.tensor(input_ids, dtype=torch.long),
        torch.tensor(attention_mask, dtype=torch.long),
        torch.tensor(labels, dtype=torch.long),
    )


class BertBiLSTMCRFDataset(Dataset):
    def __init__(self, sentences, label_lists, tokenizer, max_length=512):
        self.samples = []
        for words, labs in zip(sentences, label_lists):
            if len(words) != len(labs):
                continue
            input_ids, attention_mask, aligned = align_labels_to_bert_tokenizer(
                words, labs, tokenizer, max_length
            )
            self.samples.append((input_ids, attention_mask, aligned))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, i):
        return self.samples[i]


class BertBiLSTMCRF(nn.Module):
    """BERT (embedding) -> BiLSTM -> Linear -> CRF. Mask for padding."""

    def __init__(self, bert_name="bert-base-uncased", hidden_dim=256, num_labels=NUM_LABELS, dropout=0.3):
        super().__init__()
        self.bert = BertModel.from_pretrained(bert_name)
        self.bert_dim = self.bert.config.hidden_size  # 768
        self.lstm = nn.LSTM(
            self.bert_dim,
            hidden_dim // 2,
            num_layers=1,
            bidirectional=True,
            batch_first=True,
            dropout=0,
        )
        self.dropout = nn.Dropout(dropout)
        self.hidden2tag = nn.Linear(hidden_dim, num_labels)
        if CRF is not None:
            self.crf = CRF(num_labels, batch_first=True)
        else:
            self.crf = None
        self.num_labels = num_labels

    def forward(self, input_ids, attention_mask, labels=None):
        # BERT
        out = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        emissions = out.last_hidden_state  # [B, L, 768]
        # BiLSTM
        emissions, _ = self.lstm(emissions)
        emissions = self.dropout(emissions)
        emissions = self.hidden2tag(emissions)  # [B, L, num_labels]
        mask = attention_mask.byte()  # 1 = real, 0 = pad
        if labels is not None and self.crf is not None:
            loss = -self.crf(emissions, labels, mask=mask, reduction="mean")
            return loss
        if self.crf is not None:
            preds = self.crf.decode(emissions, mask=mask)
            return preds
        return emissions


def build_and_train_bert_bilstm_crf(
    data,
    bert_name="bert-base-uncased",
    max_length=512,
    batch_size=8,
    epochs=5,
    lr=2e-5,
    device=None,
):
    """
    Full pipeline: build splits from `data`, create BERT-BiLSTM-CRF, train, evaluate with seqeval.
    """
    if device is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    train_sents, train_labels, val_sents, val_labels, test_sents, test_labels = build_splits_from_data(
        data, LABEL_MAPPING
    )
    print(f"Train: {len(train_sents)}, Val: {len(val_sents)}, Test: {len(test_sents)}")

    tokenizer = BertTokenizer.from_pretrained(bert_name)
    train_ds = BertBiLSTMCRFDataset(train_sents, train_labels, tokenizer, max_length)
    val_ds = BertBiLSTMCRFDataset(val_sents, val_labels, tokenizer, max_length)
    train_loader = DataLoader(
        train_ds, batch_size=batch_size, shuffle=True, collate_fn=collate_bert_batch
    )
    val_loader = DataLoader(val_ds, batch_size=batch_size, collate_fn=collate_bert_batch)

    model = BertBiLSTMCRF(bert_name=bert_name, num_labels=NUM_LABELS).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr)

    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for input_ids, attention_mask, labels in train_loader:
            input_ids = input_ids.to(device)
            attention_mask = attention_mask.to(device)
            labels = labels.to(device)
            optimizer.zero_grad()
            loss = model(input_ids, attention_mask, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"Epoch {epoch + 1}/{epochs} Loss: {total_loss / len(train_loader):.4f}")

    # Evaluate with seqeval
    try:
        from seqeval.metrics import classification_report, f1_score
    except ImportError:
        print("Install seqeval: pip install seqeval")
        return model

    model.eval()
    true_all, pred_all = [], []
    with torch.no_grad():
        for input_ids, attention_mask, labels in val_loader:
            input_ids = input_ids.to(device)
            attention_mask = attention_mask.to(device)
            preds = model(input_ids, attention_mask)  # list of lists; each inner list = one per valid (masked) position
            for b in range(input_ids.size(0)):
                mask_b = attention_mask[b].cpu()
                labs_b = labels[b].cpu()
                pred_b = preds[b]
                true_tok = []
                pred_tok = []
                pos_in_pred = 0
                for i in range(mask_b.size(0)):
                    if mask_b[i].item() == 0:
                        break
                    if pos_in_pred < len(pred_b):
                        pred_label = ID2LABEL[pred_b[pos_in_pred]] if pred_b[pos_in_pred] < NUM_LABELS else "O"
                    else:
                        pred_label = "O"
                    pos_in_pred += 1
                    if labs_b[i].item() == -100:
                        continue
                    true_tok.append(ID2LABEL[labs_b[i].item()])
                    pred_tok.append(pred_label)
                if true_tok and pred_tok:
                    true_all.append(true_tok)
                    pred_all.append(pred_tok)
    print(classification_report(true_all, pred_all))
    print("F1:", f1_score(true_all, pred_all))
    return model


if __name__ == "__main__":
    # Example: load data from JSON then run (e.g. in Colab after loading data)
    import json
    import os
    default_path = "/content/drive/My Drive/DATASETS/entity_recognition_in_resumes.json"
    path = os.environ.get("RESUME_JSON", default_path)
    if os.path.exists(path):
        data = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    data.append(json.loads(line))
        # Apply label_mapping to data annotations (same as notebook)
        for item in data:
            for ann in item.get("annotation", []):
                ann["label"] = [LABEL_MAPPING.get(l, "O") for l in ann["label"]]
        model = build_and_train_bert_bilstm_crf(data, epochs=3, batch_size=8)
    else:
        print("Set RESUME_JSON or run after loading `data` in notebook, then call build_and_train_bert_bilstm_crf(data)")
