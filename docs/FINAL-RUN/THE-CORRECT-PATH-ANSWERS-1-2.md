# The Correct Path — Detailed Viva Answers (1 & 2)

This file contains polished, viva-ready answers for:

1. Project story in 2 minutes  
2. Problem -> Gap -> Aim -> Objectives alignment

Use these as primary rehearsal scripts, then personalize wording slightly to sound natural.

---

## 1) Project Story in 2 Minutes (Detailed Answer)

My final year project is **CrackInt: AI-Driven Personalized Interview Preparation Platform**.

The core problem I addressed is that most interview-preparation tools are fragmented and generic. Candidates usually use separate tools for resume analysis, job understanding, question practice, and feedback, which creates a disconnected and lower-confidence preparation experience.

From my analysis of existing systems and recent literature, I identified three practical gaps:

- lack of a unified resume-aware and job-aware personalization flow,
- feedback quality that is often superficial rather than content-focused,
- limited support for longitudinal progress/readiness visibility.

To address this, I designed and implemented CrackInt as a full-stack platform using **Next.js** on the frontend and **FastAPI** on the backend, with **PostgreSQL** for persistence.

For the ML layer, I implemented entity extraction pipelines for both resumes and job posters, primarily using **Word2Vec + BiLSTM + CRF**, with hybrid post-processing for robustness.

On top of that, I integrated:

- authenticated user/session management,
- interactive practice sessions,
- skill-gap analysis,
- readiness-oriented summaries,
- and optional LLM-enabled features controlled via configuration flags for reliability and deployment flexibility.

In terms of outcomes, the system was delivered as a working end-to-end prototype with measurable results. In the frozen evaluation runs:

- resume NER achieved around **0.83 micro-F1**,
- job-poster NER achieved around **0.85 micro-F1**.

These results are practically useful for downstream interview-preparation workflows within my project scope, while also clearly indicating areas for future improvement.

Overall, my main contribution is a **unified, candidate-centric interview-preparation system** that combines extraction, analysis, and interactive coaching in one platform, supported by implementation depth, testing evidence, and critical evaluation.

---

## 2) Problem -> Gap -> Aim -> Objectives Alignment (Detailed Answer)

My project was structured to maintain a clear academic and technical alignment from start to finish.

The **problem statement** is that candidates face fragmented and generic interview preparation support, while real interview expectations are increasingly role-specific and context-sensitive.

From literature and platform review, I defined the **research gap** as the lack of an integrated solution that consistently combines:

1. resume understanding,
2. job-description understanding,
3. interactive semantic coaching with progression visibility.

Based on this, my **research aim** was to design and evaluate an AI-driven platform that improves role-specific interview readiness through integrated extraction and practice workflows.

I then converted that aim into concrete **objectives**, and each objective is mapped to implementation and evaluation evidence:

- Objectives related to information extraction were addressed by implementing separate resume and job-poster NER pipelines and reporting model metrics.
- Objectives related to personalization were addressed by using extracted entities in preparation/session flows.
- Objectives related to actionable feedback and readiness were addressed through session evaluation logic, skill-gap analysis, and readiness summaries.
- Objectives related to software quality were addressed through functional and non-functional testing.
- Objectives related to critical reflection and academic rigor were addressed through evaluation findings, limitations, and future work.

So the complete chain is:

**Problem -> validated gap -> explicit aim -> operational objectives -> implemented modules -> tested evidence -> critical reflection.**

This alignment is reflected in the report structure and evidence tables, and it demonstrates that the project is both technically implemented and academically coherent.

---

## Quick 30-Second Backup Versions

## 1) Project story (short)
CrackInt is an AI-driven interview-preparation platform that solves fragmentation in existing candidate tools. I integrated resume/job extraction, interactive practice, feedback, and readiness support in one full-stack system. Technically, I used Next.js, FastAPI, PostgreSQL, and NER pipelines based on Word2Vec + BiLSTM + CRF with hybrid processing. The prototype works end-to-end and achieved around 0.83 and 0.85 micro-F1 on resume and job-poster NER, respectively.

## 2) Alignment (short)
The project starts from a clearly defined preparation gap, translates that into a focused aim, and operationalizes it through measurable objectives. Each objective is mapped to concrete implementation outputs and tested/evaluated evidence. This gives a full chain from problem definition to validated outcomes and critical reflection.

