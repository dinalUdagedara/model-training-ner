# CrackInt Viva PowerPoint Full Pack (Exact 20:00)

Use this file to build your PPT slide by slide.

Rules from supervisor integrated:

- exactly 20 minutes,
- include demo,
- strong focus on problem + research gap + novelty,
- include AI/ML dataset, preprocessing, training, experiments,
- include testing, critical evaluation, contribution, limitations, and skills.

---

## Timing Map (must sum to 20:00)

- Slide 1: 00:20
- Slide 2: 00:20
- Slide 3: 01:20
- Slide 4: 01:50
- Slide 5: 01:20
- Slide 6: 01:30
- Slide 7: 01:40
- Slide 8: 01:20
- Slide 9: 01:40
- Slide 10 (Demo): 03:30
- Slide 11: 01:30
- Slide 12: 01:20
- Slide 13: 01:20
- Slide 14: 01:00
- Slide 15: 00:40
- Slide 16: 00:40

Total = 20:00

---

## Slide 1 - Title (00:20)

### Slide content (paste to PPT)

- CrackInt: AI-Driven Personalized Interview Preparation Platform
- Final Year Project Viva
- Dinal Bandara | w1998730
- BEng Software Engineering

### Speaker notes

"Good [morning/afternoon]. I am presenting my final year project, CrackInt, an AI-driven interview preparation platform that integrates resume/job understanding, session practice, and feedback."

---

## Slide 2 - Agenda (00:20)

### Slide content

- Problem and research gap
- Aim and objectives
- Design and implementation
- AI/ML pipeline
- Demo
- Testing and critical evaluation
- Contribution, limitations, conclusion

### Speaker notes

"I will follow this structure and include a live demo inside the 20-minute time."

---

## Slide 3 - Problem Statement with LR Support (01:20)

### Slide content

- Interview prep tools are fragmented (separate tools for CV, JD, practice, feedback).
- Many platforms provide generic support, not role-specific personalized flow.
- Users must manually combine outputs and track progress.
- Literature and platform review indicate gaps in integrated workflow quality.

### Speaker notes

"The core problem is fragmentation. Candidates use separate tools for resume analysis, job understanding, question practice, and feedback. This creates weak continuity and lower confidence. Literature and existing platform review show this integration problem is still practical and relevant."

### Evidence line

- Use citations from your Chapter 2 LR on interview prep systems and NLP/AI recruitment tooling.

---

## Slide 4 - Research Gap (Most Important) (01:50)

### Slide content

- Gap G1: No strongly unified resume-aware + job-aware + session-linked prep flow.
- Gap G2: Feedback is often shallow, not sufficiently content-aware.
- Gap G3: Limited readiness/progress visibility in one continuous platform.
- Gap G4: Weak traceability from extraction -> coaching -> measurable outcomes.

### Visual suggestion

- Concept map:
  - Existing tools (fragmented nodes)
  - Missing links (highlighted red)
  - CrackInt integrated path (highlighted green)

### Speaker notes

"This is the most important slide. I am not claiming no similar tools exist globally. My claim is evidence-bounded: within reviewed literature and platforms, I identified this integration gap. My novelty is implementing and evaluating a single candidate-centric system that connects these missing links."

### Defense line (memorize)

"Originality here is contribution-level integration novelty, not a global first-ever claim."

---

## Slide 5 - Aim and Objectives Alignment (01:20)

### Slide content

- Aim: Design, implement, and critically evaluate an integrated AI-driven interview prep platform.
- Objectives mapped to delivery:
  - R02-R09: LR, requirements, architecture, secure data design.
  - R10-R16: NER datasets, preprocessing, training, evaluation.
  - R17-R19: advanced evaluation objectives (partially achieved due to scope).
  - R20-R22: documentation, dissertation, dissemination intent.

### Speaker notes

"My project chain is clear: Problem -> Gap -> Aim -> Objectives -> Implementation -> Testing -> Critical reflection. Most implementation/evaluation objectives were achieved, while large-scale expert studies and publication-level outcomes are explicitly marked partial."

---

## Slide 6 - System Design (Architecture) (01:30)

### Slide content

- Tiered architecture:
  - Presentation: Next.js frontend
  - Logic: FastAPI backend + ML/AI orchestration
  - Data: PostgreSQL (+ S3/object storage where relevant)
- Separation of concerns:
  - frontend `app/components/services/lib`
  - backend `api/services/ml/models/config`

### Speaker notes

"I used layered modular architecture to keep the system maintainable and testable. AI is inside backend logic services, not directly in UI. This supports controlled orchestration, validation, persistence, and cleaner failure handling."

---

## Slide 7 - AI/ML Design (Model Architecture + Flow) (01:40)

### Slide content

- Final model path for both NER tasks:
  - Word2Vec -> BiLSTM -> CRF
- Why this choice:
  - controllable training and deployment,
  - strong sequence-tagging baseline,
  - practical inference cost.
- Flow:
  - raw text -> tokenization -> BIO tags -> train/val/test -> inference -> structured entities.

### Speaker notes

"For both resume and job-poster NER, I used Path 2 Word2Vec-BiLSTM-CRF. Word2Vec gives embeddings, BiLSTM learns context both directions, and CRF enforces valid sequence decoding. This is practical and explainable for final-year scope."

---

## Slide 8 - Implementation + Tech Stack (01:20)

### Slide content

- Frontend: Next.js, TypeScript, React Query/Axios patterns
- Backend: FastAPI, Python, SQLModel/SQLAlchemy, JWT auth
- Database: PostgreSQL
- ML integration: loaded model artifacts by config dirs
- Core modules: extraction, sessions/chat, skill-gap, readiness summaries

### Speaker notes

"This is not a notebook-only system. Models are integrated into authenticated backend APIs and full frontend workflows with persistence and user/session context."

---

## Slide 9 - AI/ML Pipeline Details (Dataset, Preprocessing, Training, Experiments) (01:40)

### Slide content

- Resume NER:
  - frozen run size: 4,738 resumes
  - split: 3790 / 473 / 475
- Job-poster NER:
  - frozen run size: 6,327 postings
  - split: 5061 / 632 / 634
- Preprocessing:
  - label normalization,
  - tokenization + BIO tagging,
  - weighted sampling for class imbalance.
- Training/evaluation:
  - held-out test,
  - entity-level precision/recall/F1.

### Speaker notes

"I followed a full ML lifecycle: data preparation, normalized labels, BIO tagging, reproducible splits, weighted sampling, training, and held-out evaluation. This gave measurable performance and deployment-ready artifacts."

---

## Slide 10 - Prototype Demonstration (03:30)

### Slide content

- Demo path:
  1. Login
  2. Upload resume -> extraction
  3. Input/upload job poster -> extraction
  4. Start session chat (question + answer feedback)
  5. Show readiness/summary outputs

### Speaker notes (demo narration)

"Now I will demonstrate the end-to-end flow. First authentication. Next resume extraction where entities are parsed and editable. Then job extraction. After that I run a session turn to show question and evaluation flow. Finally I show readiness-style summary outputs."

### If live demo is slow

"I will continue with backup screenshots/video for timing stability, but this is the same tested flow."

---

## Slide 11 - Testing and Evaluation (01:30)

### Slide content

- Model testing:
  - Resume NER micro-F1: 0.83
  - Job-poster NER micro-F1: ~0.85
- Functional testing:
  - FR-aligned flows (auth, extraction, session, analytics endpoints)
- Non-functional checks:
  - security baseline (JWT, hashing),
  - maintainability (OpenAPI, modularity),
  - usability/performance baseline checks

### Speaker notes

"I validated the system in three layers: model, functional, and non-functional. I reported measurable model outcomes and linked functional tests to requirements for traceability."

---

## Slide 12 - Critical Evaluation Outcome (01:20)

### Slide content

- Triangulated evaluation:
  - quantitative metrics,
  - self-evaluation,
  - peer + industry + external academic feedback,
  - FR/NFR status mapping.
- Strengths:
  - coherent integrated prototype,
  - practical usefulness.
- Improvement themes:
  - harder entity quality cases,
  - clearer AI messaging,
  - more automation and mobile polish.

### Speaker notes

"This chapter is about maturity, not only scores. I combine multiple evidence sources and explicitly classify what is met, partial, or pending."

---

## Slide 13 - Contribution, Novelty, and Challenges (01:20)

### Slide content

- Contribution to practice:
  - candidate-centric integrated interview prep workflow
- Contribution to research domain:
  - measurable NER evidence + transparent limitations
- Novelty claim (safe):
  - integration novelty within scope and reviewed evidence
- Key challenges solved:
  - noisy document handling, artifact loading, schema evolution, fallback behavior

### Speaker notes

"My contribution is the engineered integration and validated workflow, not only one model metric. Novelty is contribution-level and scope-bounded, which is academically safer and more defendable."

---

## Slide 14 - Limitations and Future Work (01:00)

### Slide content

- Limitations:
  - no large-scale controlled user trial
  - no production load-testing proof
  - LLM variability by provider/runtime
  - limited generalization claims outside project corpora
- Future work:
  - automated CI/regression tests
  - broader user studies
  - stronger parsing robustness
  - explainability improvements

### Speaker notes

"I clearly separate what is achieved and what remains outside current scope. This transparency strengthens the credibility of my conclusions."

---

## Slide 15 - Conclusion (00:40)

### Slide content

- Aim achieved with a working full-stack integrated artifact.
- Most core objectives achieved; advanced external-scale objectives partial.
- Evidence-backed outcomes + critical reflection provided.

### Speaker notes

"In conclusion, CrackInt demonstrates a practical and evidence-backed integrated interview preparation platform, with clear strengths, explicit limitations, and realistic next steps."

---

## Slide 16 - Skills + Final Summary (00:40)

### Slide content

- Existing skills applied:
  - software architecture, backend API design, database engineering
- New skills acquired:
  - end-to-end NER pipeline design/training/deployment,
  - AI service orchestration in production-style workflow
- Final takeaway:
  - strong ownership, evidence, and critical reflection

### Speaker notes

"This project strengthened my engineering and research capabilities together. My final takeaway is a complete, tested, and critically evaluated system with responsible claims."

---

## Demo Script (Detailed Click Path + Backup)

## Live path (target 3:30)

1. Open login page -> login (00:25)
2. Open resume upload -> upload sample -> show extracted entities + edit ability (00:55)
3. Open job extraction -> input/paste/upload JD -> show extracted job entities (00:45)
4. Open session page -> run one QA turn -> show answer feedback (00:55)
5. Open readiness/summary view -> show final user-facing insight (00:30)

## Backup plan (if app/network fails)

- Keep 6 screenshots ready in order:
  - login success,
  - resume extraction result,
  - editable entities,
  - job extraction result,
  - session Q/A feedback,
  - readiness summary.
- Optional 60-90s fallback video clip.
- Backup line:
  - "To keep timing exact, I am using prepared captures of the same tested workflow."

---

## Major Examiner Questions by Section (and best short answer)

## Problem/Gap

- Q: "How is this different from just ChatGPT?"  
A: "ChatGPT is a model endpoint; CrackInt is a full system with workflow, persistence, validations, and integrated extraction-to-feedback lifecycle."

## Aim/Objectives

- Q: "Are all objectives fully achieved?"  
A: "Core engineering objectives are achieved; larger external-scale evaluation objectives are marked partial within documented scope."

## Design

- Q: "Why this architecture?"  
A: "Layered modular design gives clearer responsibilities, easier maintenance, and safer integration of AI components."

## Model choice

- Q: "Why Word2Vec-BiLSTM-CRF?"  
A: "It gives a controllable and practical sequence-tagging pipeline with strong results for scope and easier deployment control."

## Testing

- Q: "How can we trust your results?"  
A: "Results are triangulated: held-out metrics, FR-linked functional tests, NFR checks, and external evaluator feedback."

## Critical evaluation

- Q: "Why include limitations strongly?"  
A: "Clear boundaries improve academic credibility and show responsible engineering judgment."

## Novelty

- Q: "Is this globally unique?"  
A: "I do not claim global exclusivity. My defensible claim is scope-bounded integration novelty with evidence-backed implementation."

---

## Speed Control Lines (to hit exactly 20:00)

- If running fast: "I will briefly connect this to the next slide with one practical example."
- If running slow: "For time, I will summarize this point and move to the demonstrated evidence."
- Before demo: "I will keep the demo tightly scoped to five key actions."
- Before final slide: "I will close with three key takeaways."

