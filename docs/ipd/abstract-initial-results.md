# IPD Abstract – Initial Results Paragraph

**Purpose:** Third paragraph for the IPD Abstract (≤300 words total). Provides quantitative prototype results as required by the template.

---

## Paragraph 3: Initial Results

**Copy-paste ready text:**

> Initial Results: The prototype implements a BiLSTM-CRF Named Entity Recognition (NER) model trained on 3,993 annotated resumes (80/10/10 train/validation/test split). The model achieves an entity-level Test F1-score of 0.79 and Validation F1 of 0.83. Per-entity performance on the test set: EMAIL (precision 0.99, recall 0.94, F1 0.96), NAME (0.99, 0.89, 0.94), SKILL (0.89, 0.80, 0.84), EXPERIENCE (0.83, 0.67, 0.74), EDUCATION (0.64, 0.61, 0.62), and OCCUPATION (0.59, 0.57, 0.58). The model uses Word2Vec embeddings (256-dim) trained on the resume corpus, a 2-layer bidirectional LSTM (hidden 384), and a CRF decoder. Evaluation is performed with seqeval at the entity level. The NER pipeline is integrated into a FastAPI backend and Next.js frontend: users can upload PDF or paste resume text, receive extracted entities (NAME, EMAIL, SKILL, OCCUPATION, EDUCATION, EXPERIENCE), edit them manually, and persist to PostgreSQL. Job description extraction is also implemented. These results validate the feasibility of NER-based resume parsing for the CrackInt platform and provide a baseline for future question-generation and semantic-feedback modules.

---

## Full Abstract (Three Paragraphs) – Draft

**Paragraph 1 – Problem:**
> The accelerating adoption of artificial intelligence (AI) in recruitment has fundamentally transformed candidate evaluation processes, with automated applicant screening and AI-driven interview systems now increasingly used across industries. However, while employers leverage automation to enhance hiring efficiency, the tools available to job seekers for interview preparation have largely remained static. Most platforms provide generic question banks, one-way video simulations, or résumé scoring without offering personalized, context-aware feedback aligned with a candidate’s experience or targeted role. This disconnect highlights the urgent need for adaptive learning environments that bridge the gap between candidate preparation and AI-powered recruitment expectations.

**Paragraph 2 – Methodology:**
> This study introduces CrackInt, an AI-powered, web-based interview-preparation platform designed to provide résumé-aware question generation, interactive practice sessions, and real-time semantic feedback. Building on prior research on AI-based video interview systems, chatbot-enabled learning, and machine learning-driven résumé parsers, CrackInt addresses three key gaps: reliance on generic or domain-only prompts instead of role-specific questions; lack of personalized, content-level feedback; and absence of longitudinal progress tracking. The system leverages fine-tuned NER models for résumé and job-description parsing, with plans for transformer-based question generation and semantic evaluation, embedded within a chat-based interface. Developed with Next.js, Tailwind CSS, and FastAPI, CrackInt offers a responsive, mobile-first experience.

**Paragraph 3 – Initial Results:**
> (Use the “Initial Results” paragraph above.)

---

## Subject Descriptors (ACM CCS)

- Information systems → Education systems → Intelligent tutoring systems  
- Computing methodologies → Artificial intelligence → Natural language processing → Machine learning  

## Keywords

AI interview systems, résumé parsing, Named Entity Recognition, BiLSTM-CRF, adaptive learning, semantic feedback
