# BERT-BiLSTM-CRF Resume NER – Step-by-step guide

Run the notebook **BERT_BiLSTM_CRF_Resume_NER.ipynb** in Cursor. Follow these steps in order.

---

## Step 1 – Kernel and data path

1. **Select the kernel**  
   Top-right of the notebook → click the kernel name → **Select Another Kernel** → **Python Environments** → choose **Python 3.12.3** (or the one where you installed `ipykernel`). Do **not** use Colab if you want to run in Cursor.

2. **Set the data path (if needed)**  
   - Open **cell 1** (the first code cell: “Load data”).  
   - If `entity_recognition_in_resumes.json` is **in the same folder** as the notebook, leave `DATA_PATH = "entity_recognition_in_resumes.json"` as is.  
   - If you get **“JSON file not found”**, set the full path at the top of that cell, for example:
     ```python
     DATA_PATH = r"/Users/dinalbandara/Desktop/IIT/4th year/FYP/model-traning-1:30/entity_recognition_in_resumes.json"
     ```

3. **Run cell 1**  
   Press **Shift+Enter** or click ▶.  
   You should see: `Loaded 220 resumes`.

---

## Step 2 – Build train / val / test

4. **Run cell 2 (data build)**  
   The cell that starts with `# 2) Build train/val/test from JSON...`  
   - Builds word-level tokens and BIO labels (no B-O / I-O).  
   - Splits 80% train, 10% val, 10% test.  
   You should see: `Train 176 Val 22 Test 22` (or similar counts).

5. **Skip the Colab cells**  
   Skip the markdown “Colab only” and the “Mount Google Drive” code cell. You don’t need them when running in Cursor.

---

## Step 3 – Install dependencies (once)

6. **Run the pip cell**  
   The cell that runs: `!pip install -q torch transformers pytorch-crf seqeval`  
   Run it **once**. Wait until it finishes. You can skip it next time if everything is already installed.

---

## Step 4 – BERT tokenizer and dataset

7. **Run the “BERT tokenizer + label alignment” cell**  
   The one that defines `align_to_bert`, `BertNERDataset`, tokenizer, and DataLoaders.  
   - First run may download `bert-base-uncased`.  
   You should see: `Datasets ready`.

---

## Step 5 – Model

8. **Run the “BERT-BiLSTM-CRF model” cell**  
   Defines the model, device, and optimizer.  
   You should see: `Model on cpu` (or `Model on cuda` if you have a GPU).

---

## Step 6 – Training

9. **Run the “Train” cell**  
   Trains for 5 epochs. Each epoch prints a loss.  
   Example: `Epoch 1/5 Loss: 2.3456`

---

## Step 7 – Evaluation

10. **Run the “Evaluate with seqeval” cell**  
    Prints the classification report (precision, recall, F1 per entity) and overall F1.

---

## Quick checklist

| Step | Cell / action | Expected result |
|------|----------------|-----------------|
| 1 | Select kernel (Python 3.12.3), set `DATA_PATH` if needed, run cell 1 | `Loaded 220 resumes` |
| 2 | Run “Build train/val/test” cell | `Train … Val … Test …` |
| 3 | Run pip install cell (once) | Install finishes |
| 4 | Run “BERT tokenizer + dataset” cell | `Datasets ready` |
| 5 | Run “BERT-BiLSTM-CRF model” cell | `Model on cpu` or `cuda` |
| 6 | Run “Train” cell | Epoch losses printed |
| 7 | Run “Evaluate with seqeval” cell | F1 and report printed |

---

## If something fails

- **“JSON file not found”** → Set `DATA_PATH` in cell 1 to the full path of `entity_recognition_in_resumes.json` and re-run cell 1.  
- **“No module named 'torch'” (or transformers, torchcrf, seqeval)** → Run the pip install cell again and wait for it to finish.  
- **“Requires ipykernel”** → In Terminal: `pip install ipykernel` (in the same Python you use as the kernel), then reselect that kernel in Cursor.
