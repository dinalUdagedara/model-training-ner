# Algorithm design — Word2Vec BiLSTM–CRF for résumé NER

*Adjust section numbers (e.g. 6.5) to match your report template. Insert the architecture figure from your design chapter.*

---

## 6.5 Algorithm design

Résumé named entity recognition is treated as **token-level sequence labelling**: each word receives a label from a fixed set of **BIO** tags (Begin, Inside, Outside) for types such as name, email, skill, occupation, experience, and education. The model follows the **BiLSTM–CRF** approach (Huang *et al.*, 2015; Lample *et al.*, 2016): a recurrent encoder produces **context-dependent emission scores** at each position, and a **linear-chain conditional random field** (CRF) chooses a **globally consistent** tag sequence, discouraging invalid transitions (for example, an *I-* tag without a preceding *B-* for the same entity type).

### 6.5.1 Input preprocessing and tokenisation

Input text is **normalised** and **tokenised at word level**. Tokens are mapped to integer indices using a vocabulary constructed from the training data. **Padding** symbols align sequences to a common length within a batch; **unknown-word** handling maps tokens outside the vocabulary to a dedicated index. A **binary validity mask** marks real tokens versus padding. The mask is applied in the CRF **training loss** and at **decoding** so that padded positions are neither scored nor labelled.

### 6.5.2 Word representation and embedding layer

Each token index is embedded with a **trainable lookup table** of dimension **256**. Vectors are **initialised** from **Word2Vec** representations trained on the same domain text as the NER task, then **fine-tuned** end-to-end. The vocabulary size **\(|V|\)** is determined by the training corpus and Word2Vec settings (minimum word frequency, *etc.*); the value obtained after vocabulary construction should be stated where hyperparameters are summarised. **Dropout** with rate **0.35** is applied to the embedding output before the recurrent layers. The embedded sequence has shape **\(B \times L \times 256\)**, where \(B\) is batch size and \(L\) is padded sequence length.

### 6.5.3 Contextual encoding with stacked bidirectional LSTMs

The embedded sequence is encoded with a **two-layer bidirectional LSTM**. Each direction uses a hidden size of **192**; forward and backward outputs are **concatenated**, giving **384** dimensions per time step. **Dropout** with rate **0.20** is applied **between** the two LSTM layers. A further **dropout** with rate **0.35** is applied to the recurrent output **before** the linear emission layer. The tensor entering the emission layer has shape **\(B \times L \times 384\)**.

### 6.5.4 Emission layer and linear-chain CRF

A **linear layer** maps each 384-dimensional vector to **\(K = 13\)** scores—one per label. The label set consists of the **O** tag plus **B-** and **I-** variants for **NAME**, **EMAIL**, **SKILL**, **OCCUPATION**, **EXPERIENCE**, and **EDUCATION**. These scores act as **emissions** for a **linear-chain CRF**, which learns **transition compatibility** between adjacent tags. **Training** minimises the **negative log-likelihood** of the reference tag sequence under the model, with padding excluded via the mask. **Inference** uses **Viterbi decoding** to obtain the highest-scoring admissible tag sequence.

### 6.5.5 Output

The model outputs a **BIO tag sequence** aligned with tokens. Tags are aggregated into **entity spans** for downstream use (storage, display, and comparison with job postings in the CrackInt application).

---

**Figure X** *(insert number)*: Neural architecture of the Word2Vec BiLSTM–CRF model for résumé named entity recognition.

*If the deployed system uses a different encoder (for example a transformer-based embedding), describe that configuration in the implementation chapter and, where appropriate, provide a separate figure so that the report matches what is run in production.*

---

## References

Huang, Z., Xu, W., & Yu, K. (2015). Bidirectional LSTM-CRF models for sequence tagging. *arXiv:1508.01991*.

Lample, G., Ballesteros, M., Subramanian, S., Kawakami, K., & Dyer, C. (2016). Neural architectures for named entity recognition. In *Proceedings of NAACL-HLT*.

Mikolov, T., Chen, K., Corrado, G., & Dean, J. (2013). Efficient estimation of word representations in vector space. *arXiv:1301.3781*. *(If Word2Vec is discussed in detail.)*

Lafferty, J., McCallum, A., & Pereira, F. (2001). Conditional random fields: Probabilistic models for segmenting and labelling sequence data. In *Proceedings of ICML*. *(If classical CRF theory is cited.)*
