# Running the BERT-BiLSTM-CRF notebook in Cursor

## New notebook: `BERT_BiLSTM_CRF_Resume_NER.ipynb`

- **New file** (recommended): Run this notebook; it keeps your original `BiLSTM_CRF_28_1.ipynb` unchanged.
- **Edit existing**: You can instead copy these cells into `BiLSTM_CRF_28_1.ipynb` if you prefer one file.

---

## “Requires ipykernel” / kernel setup in Cursor

If Cursor says **“Running cells with 'Python 3.x' requires the ipykernel package”**, do one of the following **in your Mac Terminal** (not in Cursor).

### Option A – Install ipykernel for your current Python (quick)

```bash
/opt/homebrew/bin/python3 -m pip install ipykernel -U --user --force-reinstall --break-system-packages
```

Then in Cursor: click the kernel name (top-right) → **Select Another Kernel** → **Python Environments** → choose **Python 3.13.5** (or your version). Run the first cell again.

### Option B – Use a virtual environment (recommended)

Your project path contains **`:`** (`model-traning-1:30`), so Python will not create a venv inside this folder. Create the venv in a folder **without** `:` and use it as the notebook kernel.

1. **Create venv** (e.g. in your home or FYP parent folder):

   ```bash
   python3 -m venv ~/venv-resume-ner
   source ~/venv-resume-ner/bin/activate
   ```

2. **Install ipykernel and notebook dependencies:**

   ```bash
   pip install ipykernel torch transformers pytorch-crf seqeval
   ```

3. **Register the venv as a Jupyter kernel** (optional, so Cursor lists it):

   ```bash
   python -m ipykernel install --user --name=resume-ner --display-name="Python (resume-ner)"
   ```

4. In Cursor: **Select Kernel** → **Python (resume-ner)** or browse to `~/venv-resume-ner/bin/python`.

---

## Run from Cursor

1. **Open the notebook**  
   Open `BERT_BiLSTM_CRF_Resume_NER.ipynb` in Cursor.

2. **Select a kernel**  
   Top-right: choose a Python interpreter that has **ipykernel** (e.g. the one you used in Option A or B above).

3. **Run cells**  
   - **One cell**: Click the ▶ Run button next to the cell, or press **Shift+Enter**.  
   - **All cells**: Use “Run All” from the notebook toolbar (or the command palette: “Notebook: Run All”).

4. **Data path**  
   In **cell 1**, set `DATA_PATH` to where your JSON file is:
   - **Local**: e.g. `"entity_recognition_in_resumes.json"` (file in project folder) or a full path.
   - **Colab Drive**: e.g. `"/content/drive/My Drive/DATASETS/entity_recognition_in_resumes.json"` (after mounting Drive).

5. **Dependencies**  
   Cell 3 runs: `pip install -q torch transformers pytorch-crf seqeval`  
   Run it once (or install in your environment beforehand).

---

## If you don’t have the JSON locally

- Download `entity_recognition_in_resumes.json` into the project folder, or  
- Use Colab: upload the notebook, mount Drive, set `DATA_PATH` to the file on Drive, then run all cells.

---

## Summary

| Action        | How in Cursor                          |
|---------------|----------------------------------------|
| Run one cell  | ▶ next to cell or **Shift+Enter**      |
| Run all       | “Run All” in notebook toolbar          |
| Change data   | Edit `DATA_PATH` in cell 1              |
| Install deps  | Run cell 3 once                        |
