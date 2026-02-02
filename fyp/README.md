# FYP: Resume NER (BERT-BiLSTM-CRF)

This folder contains the FYP notebook for **Resume Named Entity Recognition** using a BERT-BiLSTM-CRF model. Data must be prepared with `resume_ner_pipeline/prepare_data.py` before running the notebook.

**Data path:** By default the notebook uses **Google Drive** when Drive is mounted (e.g. on Colab): it looks for `merged_resume_ner.json` in your Drive root (`MyDrive/merged_resume_ner.json`). Override with the `RESUME_NER_DATA_PATH` environment variable or by setting `DATA_PATH` in the data-loading cell. When not on Colab/Drive, the default is `../resume_ner_pipeline/merged_resume_ner.json` (run from project root or `fyp/`).

**Requirements:** `torch`, `transformers`, `pytorch-crf`, `seqeval`
