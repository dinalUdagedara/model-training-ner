# Resume NER — Optimization Roadmap

Current setup: BERT-BiLSTM-CRF, hybrid inference (rules for NAME/EMAIL, model for SKILL/EDUCATION/EXPERIENCE/OCCUPATION). Typical val F1 ~0.52, test ~0.47; target 80%+.

---

## Already in place

- **Backend post-processing:** Trailing punctuation stripped from entity phrases; duplicates removed (case-insensitive). Improves output quality without retraining.
- **I-X recovery:** Entity builder treats leading I-X spans (when model misses B-X) so EDUCATION/EXPERIENCE like “Computer Science” and “Engineering” are captured.

---

## How to optimize (step-by-step)

### 1. More data
- You have **1033 resumes** (Dotin + minhquan). To add more:
  - **Existing 220:** Run merge with `--existing ../entity_recognition_in_resumes.json` → ~1253 resumes.
  - **vrundag91:** Download [Resume-Corpus-Dataset](https://github.com/vrundag91/Resume-Corpus-Dataset), add `--vrundag /path/to/Resume-Corpus-Dataset/data-files` to the merge.
- After merging, re-run the notebook from cell 1 through train and save.

### 2. Training cell (cell 6) — validation + early stopping + best checkpoint
The training loop should run **validation each epoch**, save the **best model by val F1**, and **restore it** at the end. In cell 6:

1. Change **PATIENCE** from `5` to `7`.
2. After the line `print(f"Epoch {epoch+1}/{EPOCHS} Loss: ...")` **inside** the `for epoch` loop, add:
   - `scheduler.step()`
   - Call `run_validation(model, val_loader, device, ID2LABEL, NUM_LABELS)` → get `val_f1`
   - If `val_f1 > best_f1`: set `best_f1 = val_f1`, `best_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}`, `epochs_no_improve = 0`; else `epochs_no_improve += 1`
   - Print val F1 and best F1
   - If `epochs_no_improve >= PATIENCE`: `break`
3. **After** the loop, add: `if best_state is not None: model.load_state_dict(best_state); print("Restored best checkpoint.")`

### 3. Longer training
- In cell 6, set **EPOCHS** to 40–50, or run the optional cell 11 (more epochs + LR scheduler) after cell 6.

### 4. Class weights (optional, advanced)
To push SKILL/EDUCATION/EXPERIENCE: use sample weighting (oversample resumes with these labels) or a custom loss that weights by label. Try steps 1–3 first.

---

## Quick wins (no or minimal retraining)

| What | Where | Action |
|------|--------|--------|
| **More training data** | `prepare_data.py` | Add `--existing ../entity_recognition_in_resumes.json` and/or `--vrundag /path/to/Resume-Corpus-Dataset/data-files` to the merge; retrain. More resumes → better generalization. |
| **Longer training** | Notebook cell 6 | Increase `PATIENCE` (e.g. 7–10) or add the optional “more epochs + LR scheduler” cell (cell 11) and run extra epochs. |
| **Post-processing (notebook)** | `parse_resume` entity loop | Optionally strip trailing punctuation when building phrases (e.g. `phrase = [w.rstrip(".,;:") for w in phrase]` before `" ".join(phrase)`). Backend already does this. |

---

## Training-side improvements (retrain)

| What | Where | Action |
|------|--------|--------|
| **Class weights** | Notebook: loss / DataLoader | Weight SKILL, EXPERIENCE, EDUCATION higher in the loss (e.g. `weight` per label in CRF or sample weighting) so the model doesn’t under-predict these. |
| **LR / warmup** | Notebook: optimizer | You already use BERT 1e-5, head 5e-5. Try linear warmup (e.g. 10% of steps) + decay for stability. |
| **Dropout** | `BertBiLSTMCRF` | You use 0.4; try 0.35 if overfitting, or 0.45 if underfitting. |
| **Early stopping** | Notebook: training loop | Increase `PATIENCE` (e.g. 7) so best checkpoint isn’t restored too early. |

---

## If you need 80%+ F1

- **Data:** Merge all sources (existing + Dotin + vrundag91 + minhquan) and ensure annotation quality (no misaligned spans, consistent labels).
- **Training:** Class weights for rare entities, longer training with LR scheduler, possibly more epochs.
- **Evaluation:** Track per-entity F1 (seqeval); fix the worst classes (often SKILL/EXPERIENCE/EDUCATION).
- **Optional:** Second-stage corrector (e.g. LLM) that takes raw text + extracted entities and fixes obvious errors; fallback to NER output if the corrector fails.

---

## Summary

- **Done:** Backend normalizes entities (strip punctuation, dedupe); I-X recovery in entity building.
- **Next:** Add more data to the merge and retrain; optionally add class weights and longer training.
- **Later:** Per-entity analysis, optional LLM corrector, job-poster NER if needed.
