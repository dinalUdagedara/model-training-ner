# CrackInt: Research Gaps, Technical Novelty & Research Novelty — Reference Document

**Purpose:** Single reference for research gaps, technical novelty, and research novelty, with real-world verification. Use when writing the thesis, preparing slides, or responding to examiner questions.

**Source:** IPD (w1998730_20221214_IPD.pdf), proposal-summary.md, and real-world platform verification (2024–2025).

**Last updated:** March 2025

---

## Table of Contents

1. [Research Gaps](#1-research-gaps)
2. [Technical Novelty](#2-technical-novelty)
3. [Research Novelty](#3-research-novelty)
4. [Quick Reference Table](#4-quick-reference-table)
5. [Caveats and Nuances](#5-caveats-and-nuances)

---

## 1. Research Gaps

For each gap: (a) formal statement, (b) evidence from literature, (c) real-world verification.

---

### Gap 1: Lack of Resume–Job Awareness

#### 1.1 Formal Statement

> Existing platforms do not dynamically generate questions that are aligned with both a candidate’s résumé and target role. Instead, most systems rely on generic question sets, which reduces preparation efficiency and may negatively impact interview performance.
>
> — IPD Ch. 1.6; VMock, Kickresume (n.d.)

#### 1.2 Evidence from Literature

| Source | Finding |
|--------|---------|
| IPD Table (1.5) | VMock: “Limited to CV scoring; no dynamic interview prep” |
| IPD Table (1.5) | Kickresume: “Question generator — Not role-specific, no semantic feedback” |
| IPD Table (1.5) | Huntr: “No chat-style practice, no resume-job parsing” |
| Synthesis | “None integrate dynamic, role-specific question generation based on both candidate CV and job description” (IPD Ch. 1.5) |

#### 1.3 Real-World Verification (2024–2025)

**Change since IPD:** Several products now use resume + job for question generation.

| Platform | Resume + Job for QG? | Notes |
|----------|----------------------|--------|
| **Kickresume** | Yes | AI uses resume + job role + industry for QG (GPT-4.1) |
| **Next Rounds AI** | Yes | Paste job, upload resume → 15–20 personalized questions |
| **InterviewAiHub** | Yes | Resume-based QG with section analysis |
| **AIOffer.me** | Yes | Resume tailoring + mock interviews with role-specific Qs |
| **HireUp** | Yes | Live AI mock interviewer with role-calibrated questions |
| **Big Interview** | Yes (Dynamic Interview) | Qs based on job description + resume; role alignment, clarity, confidence |
| **VMock** | Limited | Resume optimization + job-specific tailoring; mock interview questions less tied to structured resume parsing |
| **Huntr** | No | Job tracking; generic Q&A; no resume-job parsing |

**Conclusion:** This gap has **narrowed**. Many tools now generate questions from resume + job. CrackInt’s distinction is:

- **NER-based structured parsing** (explicit skills, education, experience) vs black-box LLM analysis
- **End-to-end integration** with semantic feedback and progress tracking
- **Academic validation** (elicitation, surveys, competitive analysis)

Use a **refined statement** in the thesis: “Few platforms combine structured NER-based resume and job parsing with personalized question generation in an integrated, validated workflow.”

---

### Gap 2: Absence of Semantic-Level Feedback

#### 2.1 Formal Statement

> While some tools provide superficial feedback on tone, pacing, or grammar, they generally fail to evaluate the content quality, depth, and structure of responses. Candidates receive limited actionable insights to improve technical or behavioral answers.
>
> — IPD Ch. 1.6; Fulk et al. (2022); Jones (2020)

#### 2.2 Evidence from Literature

| Source | Finding |
|--------|---------|
| Fulk (2022) | Big Interview: 9 superficial metrics (pace, filler words, vocabulary, energy, eye contact, etc.); engagement high but feedback content-shallow |
| Lewton & Haddad (2024) | 234 pharmacy students: 79.9% felt more prepared, but requested “questions specific to my resume” and “deeper analysis of answer content, not just how I said it” |
| Daryanto et al. (2025) | Conversate: dialogic feedback valued, but lacked resume-aware personalization |
| IPD Ch. 2.4.5 | “Big Interview and VMock focus on presentation metrics, not content depth” |

#### 2.3 Real-World Verification (2024–2025)

| Platform | Feedback Type | Content Depth? |
|----------|---------------|----------------|
| **Big Interview VideoAI** | Pace, vocabulary, eye contact, body language | No — presentation metrics |
| **Big Interview Dynamic** | Role alignment, clarity, confidence | Partial — structure/clarity, not semantic technical depth |
| **VMock SMART Interview** | Non-verbal, delivery, “content strength” (structure, necessary elements) | Partial — structure/elements, not reasoning or technical correctness |
| **Conversate** (academic) | Dialogic, content-focused | Yes — research prototype |
| **Zara** (academic) | LLM-based technical + interpersonal feedback | Yes — research prototype |

**Conclusion:** This gap is **still valid**. Mainstream tools focus on presentation; content-quality and reasoning evaluation are mostly in academia. CrackInt’s contribution is **semantic feedback in a candidate-facing product** (embedding-based scoring, relevance, depth).

---

### Gap 3: Limited Adaptive Learning and Progress Tracking

#### 3.1 Formal Statement

> Most existing platforms lack mechanisms to store session histories or adapt question difficulty based on previous performance, restricting longitudinal skill development.
>
> — IPD Ch. 1.6; Huntr (n.d.)

#### 3.2 Evidence from Literature

| Source | Finding |
|--------|---------|
| Apriani et al. (2024) | Progress tracking linked to 41% skill improvement and 45% self-efficacy increase |
| IPD survey (n=95) | 51.6% rated progress tracking as “very valuable” |
| Interviews (IPD) | 4/5 participants wanted objective progress indicators |
| Huntr | Job tracking; no structured session history or adaptive difficulty |

#### 3.3 Real-World Verification (2024–2025)

| Platform | Session History | Adaptive Difficulty | Longitudinal Analytics |
|----------|-----------------|---------------------|------------------------|
| **LeetCode** | Yes (problem history) | No explicit adaptivity | Yes (stats, trends) |
| **Pramp** | Yes (session list) | No (random peer matching) | Limited |
| **Big Interview** | Yes (My Videos) | No clear adaptivity from prior performance | Limited |
| **VMock** | Yes (recordings, Network Feedback) | No evidence of difficulty adaptation | Limited |
| **CrackInt** (planned) | Yes (PrepSession, Message) | Planned (from resume + prior performance) | Planned (analytics dashboard) |

**Conclusion:** **Partially valid.** Many tools have basic history; few have **difficulty adaptation from prior performance**. CrackInt’s novelty is **adaptive difficulty driven by resume and session history**.

---

### Gap 4: Scalability and Integration Challenges

#### 4.1 Formal Statement

> Few systems integrate résumé parsing, dynamic question generation, and semantic evaluation into a single platform capable of managing diverse file formats, multiple concurrent users, and secure data storage.
>
> — IPD Ch. 1.6; VMock, Kickresume (n.d.)

#### 4.2 Evidence from Literature

| Source | Finding |
|--------|---------|
| IPD Ch. 1.5 | “Some focus exclusively on resume optimization (VMock), others on video-based delivery (Big Interview), and a few on generic Q&A (Huntr). Crucially, none integrate [all three].” |
| IPD Ch. 2.4.5 | No candidate-focused platform integrates all four: parsing + QG + semantic feedback + progress tracking |

#### 4.3 Real-World Verification (2024–2025)

| Platform | Resume Parse | Job Parse | QG | Semantic Feedback | Progress Tracking |
|----------|--------------|-----------|-----|-------------------|-------------------|
| Big Interview | Limited (Resume Builder) | Yes (Dynamic) | Yes | No (presentation) | Limited |
| VMock | Yes (SMART Resume) | Yes (Resume Optimizer) | Yes (Mock) | Partial | Limited |
| Kickresume | Yes | Yes ( tailoring) | Yes | No | Limited |
| Next Rounds AI | Yes (upload) | Yes (paste) | Yes | No evidence | No evidence |
| Conversate | No | No | Yes | Yes | No |
| **CrackInt** | Yes (NER) | Yes (NER) | Planned | Planned | Planned |

**Conclusion:** Gap is **valid**. Few products combine **all** of: (1) NER-based parsing for resume and job, (2) dynamic QG, (3) semantic feedback, (4) progress analytics. Most cover 2–3 of these.

---

### Gap 5: Privacy and Ethical Considerations

#### 5.1 Formal Statement

> Handling sensitive candidate data (résumés, practice responses) requires secure storage, anonymization, and ethical AI processing. Most platforms do not address these concerns in detail, particularly when leveraging cloud-based AI models.
>
> — IPD Ch. 1.6; Jones (2020)

#### 5.2 Evidence from Literature

| Source | Finding |
|--------|---------|
| Horodyski (2023) | 37% of applicants concerned about AI tool transparency |
| IPD survey | 81% willing to upload resume if encryption + clear policy; 5% absolute refusal |
| IPD Ch. 5 (SLEP) | GDPR/CCPA, consent, right to erasure, anonymization for training |

#### 5.3 Real-World Verification

- Few platforms explain: data retention, model training on user data, right to erasure, and portability in detail.
- IPD explicitly defines NFR14–NFR16 (GDPR, anonymization, session expiry).
- CrackInt’s contribution: **explicit SLEP treatment** and **documented privacy-by-design** in an academic context.

**Conclusion:** Gap is **valid**. Privacy and ethics are often under-addressed; CrackInt provides structured SLEP and compliance planning.

---

## 2. Technical Novelty

For each technical claim: formal description, reality check, and defensible framing.

---

### 2.1 Integrated NER Pipeline for Resume and Job

| Aspect | Description | Reality Check |
|--------|-------------|---------------|
| **Claim** | Custom Word2Vec + BiLSTM-CRF for resume and job NER; hybrid rules (NAME/EMAIL) + model (SKILL, OCCUPATION, EDUCATION, EXPERIENCE). | BiLSTM-CRF is standard. Hybrid extraction is common. |
| **Novelty** | Application to resume + job in one pipeline; transparent, auditable extraction vs opaque LLM. | Incremental, defensible. |
| **For thesis** | “Implements a hybrid NER pipeline for resume and job parsing, combining rule-based extraction for high-precision entities with a BiLSTM-CRF model for domain entities, achieving Test F1 0.79.” |

---

### 2.2 Resume + Job Fusion for Question Generation

| Aspect | Description | Reality Check |
|--------|-------------|---------------|
| **Claim** | Parse resume and job → structured entities → LLM prompt for role-specific questions. | Some commercial tools do similar flows. |
| **Novelty** | Use of **explicit NER entities** (skills, experience, education) rather than raw text or keyword matching; documented in requirements and design. | Distinguishes from black-box LLM-only approaches. |
| **For thesis** | “Uses NER-extracted entities from resume and job as structured inputs to an LLM-based question generator, enabling transparent and controllable personalization.” |

---

### 2.3 Semantic Feedback Engine

| Aspect | Description | Reality Check |
|--------|-------------|---------------|
| **Claim** | Embedding-based evaluation of answer depth, relevance, and clarity. | Semantic evaluation exists in research (Conversate, Zara); less common in products. |
| **Novelty** | Implementation in an **integrated product** with resume/job parsing and practice sessions. | Practical application, not algorithm invention. |
| **For thesis** | “Implements a semantic feedback module that evaluates candidate answers beyond presentation metrics, using embedding-based similarity and content-depth assessment.” |

---

### 2.4 End-to-End Candidate-Centric Architecture

| Aspect | Description | Reality Check |
|--------|-------------|---------------|
| **Claim** | One platform: resume parsing + job parsing + QG + semantic feedback + progress tracking. | Rarely found in a single product. |
| **Novelty** | **Integration** of modules in a coherent candidate-facing flow. | Valid; emphasize integration, not individual algorithms. |
| **For thesis** | “CrackInt integrates NER parsing, job analysis, question generation, and semantic feedback within a unified candidate-centric platform.” |

---

### 2.5 Chat-Based Practice with Follow-Up

| Aspect | Description | Reality Check |
|--------|-------------|---------------|
| **Claim** | Chat interface; follow-up questions (“Why was this weak?”); dialogic feedback. | Conversate (Daryanto 2025) does this; CrackInt applies it in a full product. |
| **Novelty** | Combination with resume-aware QG and progress tracking. | Incremental, defensible. |
| **For thesis** | “Supports a chat-based practice flow with dialogic follow-up, combined with resume-aware question generation and session tracking.” |

---

## 3. Research Novelty

---

### 3.1 Problem-Domain Contribution

| Claim | Evidence | Real-World Assessment |
|-------|----------|------------------------|
| Introduces a scalable, AI-driven platform integrating multiple functions | IPD Ch. 1.7.1 | Many tools are narrow; integration is a real contribution. |
| Fuses resume/job parsing, QG, and semantic evaluation | IPD Ch. 1.7.1 | Few products do all three; valid. |
| Supports iterative skill development with tracking | IPD Ch. 1.7.1 | Progress tracking exists elsewhere; combined with semantic feedback it is less common. |
| Reduces inefficiency in technical/hybrid interview prep | IPD Ch. 1.7.1 | Plausible; needs user-study evidence. |

**Defensible statement:** “CrackInt contributes a candidate-centric platform that integrates NER-based parsing, LLM-based question generation, and semantic feedback, addressing fragmentation in existing interview preparation tools.”

---

### 3.2 Research-Domain Contribution

| Claim | Evidence | Real-World Assessment |
|-------|----------|------------------------|
| NER + LLM + semantic evaluation pipeline | IPD Ch. 1.7.2 | Established techniques; novelty in **combination and application**. |
| Adaptive dialogue for interview prep | IPD Ch. 1.7.2 | Related work exists (e.g. Conversate); CrackInt extends to full workflow. |
| Empirical insights on AI in career/education | IPD Ch. 1.7.2 | Valid; needs evaluation results. |

**Defensible statement:** “The project contributes an applied NLP pipeline for interview preparation and empirical insights into integrating AI in sensitive career applications.”

---

### 3.3 Methodological Contribution

| Claim | Evidence | Real-World Assessment |
|-------|----------|------------------------|
| Triangulated requirements (literature, interviews, survey, competitive analysis, brainstorming) | IPD Ch. 4 | Thorough elicitation; strengthens validity. |
| MoSCoW prioritization with stakeholder input | IPD Ch. 4 | Standard but well-executed. |
| SLEP analysis and BCS alignment | IPD Ch. 5 | Valuable for ethical and professional framing. |

**Defensible statement:** “The project demonstrates a triangulated requirements process and SLEP-aware design for an AI career platform.”

---

## 4. Quick Reference Table

| Item | Status | Refined Statement for Thesis |
|------|--------|------------------------------|
| **Gap 1: Resume–job awareness** | Narrowed | Few platforms combine structured NER-based parsing with personalized QG in a validated workflow. |
| **Gap 2: Semantic feedback** | Valid | Mainstream tools focus on presentation; content-level evaluation is rare in products. |
| **Gap 3: Adaptive learning** | Partial | Basic progress exists; difficulty adaptation from prior performance is uncommon. |
| **Gap 4: Integration** | Valid | Few products integrate parsing + QG + semantic feedback + tracking. |
| **Gap 5: Privacy/ethics** | Valid | Often under-addressed; CrackInt provides SLEP and compliance planning. |
| **Technical novelty** | Incremental | Integration and application, not new algorithms. |
| **Research novelty** | Application + methodology | Applied pipeline, empirical insights, triangulated elicitation. |

---

## 5. Caveats and Nuances

### 5.1 Landscape Changes (2024–2025)

- **Resume + job QG:** Several tools (Kickresume, Next Rounds AI, Big Interview Dynamic, etc.) now use resume and job for questions. The gap is no longer “no one does this.”
- **Semantic feedback:** Commercial tools still lean toward presentation; content-depth evaluation is mostly in research.
- **Updates:** Re-check competitor features before final submission.

### 5.2 How to Frame in the Thesis

1. **Gap 1:** Emphasize **NER-based structured parsing** and **full integration**, not “first ever” resume+job QG.
2. **Gap 2:** Emphasize **content-level semantic evaluation** vs presentation metrics.
3. **Technical novelty:** Emphasize **integration and application**, not algorithmic novelty.
4. **Research novelty:** Emphasize **triangulated validation**, SLEP, and empirical insights.

### 5.3 References to Cite

- Fulk (2022) — Big Interview, superficial feedback  
- Lewton & Haddad (2024) — User requests for content feedback  
- Daryanto et al. (2025) — Conversate, dialogic feedback  
- Jones (2020) — HireVue, employer focus  
- Baby et al. (2025) — FairHire, employer-side automation  
- Chandak et al. (2024) — Resume parsing, job recommendation  
- Machhale et al. (2024) — Chat-based interview prep  

---

*This document is for internal reference. Update competitor information and real-world verification before thesis submission or viva.*
