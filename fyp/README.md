# FYP: Resume NER (BERT-BiLSTM-CRF)

This folder contains the FYP notebook for **Resume Named Entity Recognition** using a BERT-BiLSTM-CRF model. The notebook is intended for **Google Colab**.

**Setup:** Mount Google Drive first (step at the top of the notebook). Data must be in **Google Drive**: place `merged_resume_ner.json` in your My Drive root. Prepare the data with `resume_ner_pipeline/prepare_data.py` before running the notebook.

**Requirements:** `torch`, `transformers`, `pytorch-crf`, `seqeval`. For optional agent corrector: `openai`.

**Optional:** `agent_corrector.py` provides a second-stage LLM corrector to fix entity errors. Set `OPENAI_API_KEY` and run section 7b in the notebook.

**Code guides:** [RESUME_NER_CODE_GUIDE.md](RESUME_NER_CODE_GUIDE.md) and [job-poster-ner/JOB_POSTER_NER_CODE_GUIDE.md](job-poster-ner/JOB_POSTER_NER_CODE_GUIDE.md) explain each code block in the notebooks.
