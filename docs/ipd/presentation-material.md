# IPD Presentation — Full Slide Content

**Use this document to copy-paste content into each slide.**  
Slide order matches the IPD requirements and the template mapping. Total presentation: **20 minutes** (content after 20 min is not marked).

---

## Slide 1 — Title

**Slide title:** (Leave as title slide or use project title below.)

**Content to display:**

- **CrackInt: AI-Driven Personalized Interview Preparation Platform**
- **Student:** Udagedara Thiyunu Dinal Bandara
- **UoW / IIT ID:** W1998730
- **Supervisor:** Mr. Pubudu Arachchige
- **Module:** 6COSC023W – Computer Science Final Project  
- **Interim Progression Demonstration (IPD)**

---

## Slide 2 — Agenda

**Slide title:** Agenda

**Content (bullets):**

- Problem background
- Research problem & research gap
- Identification of project stakeholders
- Formal requirements specification (implemented vs pending)
- System design
- Overall system architecture & wireframes
- Updated time schedule
- Progress since PPRS
- Conclusion
- References

---

## Slide 3 — Problem background

**Slide title:** Problem background

**Content (bullets):**

- Employers use AI for screening; candidate-side prep tools remain static (generic questions, one-way video, résumé scoring).
- **Gap 1 — Resume–job awareness:** Generic question banks; no alignment with candidate background or target role.
- **Gap 2 — Semantic-level feedback:** Focus on tone/pace/grammar, not content depth, relevance, or structure (e.g. Big Interview).
- **Gap 3 — Integrated progress tracking:** No unified platform for session history and improvement over time.
- **Gap 4 — UX:** Real-time, mobile-friendly, low-latency experience often missing.
- **Summary:** No holistic, AI-powered platform combines résumé parsing, role-specific question generation, and semantic feedback in one candidate-centric system.

**Optional:** Add one citation (e.g. Fulk 2022; Horodyski 2023) or a simple chart if available.

---

## Slide 4 — Research problem & research gap

**Slide title:** Research problem & research gap

**Research problem (1–2 bullets):**

- Current platforms fail to provide personalized, content-aware coaching from both candidate résumé and target job posting.
- They rely on static question banks, superficial feedback, and fragmented workflows (résumé, questions, and feedback in separate tools).

**Research gap (bullets):**

- **Resume–job awareness:** No platform dynamically generates questions from both candidate résumé and job description (e.g. VMock, Kickresume do not combine both).
- **Semantic feedback:** Tools like Big Interview give superficial metrics (tone, pace); content quality and reasoning are not evaluated.
- **Adaptive learning:** Little support for session history and difficulty adaptation from prior performance (e.g. Huntr).
- **Integration:** No single platform unites parsing, question generation, and semantic evaluation; employer tools (FairHire, HireVue) serve recruiters, not candidates.

**CrackInt addresses this by:**

- NER-based résumé and job parsing  
- LLM-based question generation  
- Semantic feedback engine  
- Persistent analytics  

---

## Slide 5 — Identification of project stakeholders

**Slide title:** Identification of project stakeholders

**Include:** An **onion diagram** (four concentric layers: Core → Operational → Strategic → External). Draw in PowerPoint/Google Slides or use the table below beside the diagram.

**Table (roles and interests):**

| Layer        | Stakeholders                                              | Roles / interests                                                                 |
|-------------|------------------------------------------------------------|------------------------------------------------------------------------------------|
| **1 – Core** | Job seekers, students, early-career professionals         | Personalized questions, actionable feedback, progress tracking, affordable access |
| **2 – Operational** | Career services, technical support, development team | Effectiveness, reliability, integration, maintenance                              |
| **3 – Strategic** | Academic institutions, corporate partners, research community | Outcomes, candidate readiness, accreditation, recruitment efficiency           |
| **4 – External** | Regulatory (GDPR/CCPA), AI ethics bodies, competitors, tech providers | Compliance, transparency, bias mitigation, ethical data use              |

---

## Slide 6 — Formal requirements specification

**Slide title:** Formal requirements specification

**Subtitle or note:** Implemented vs pending (must be clearly indicated for marking).

**Implemented (done in prototype):**

- **FR03** – Resume upload (PDF + paste).
- **FR04** – Resume NER extraction (BERT-BiLSTM-CRF + rules).
- **FR05** – Review and edit extracted entities.
- **NFR13** – Modular architecture and OpenAPI docs.

**Partial (backend or part of flow only):**

- **FR06–FR07** – Job description input and analysis (API done; frontend optional for IPD).
- **FR14** – Persist resume/entities (no practice-session history yet).
- **FR25** – Basic application logging.
- **NFR02, NFR06, NFR08, NFR09, NFR12, NFR18** – Partially addressed; not fully validated.

**Pending (for post-IPD / April):**

- **FR01–FR02** – Registration and auth.
- **FR08–FR13** – Question generation, chat interface, semantic feedback, follow-ups.
- **FR15–FR24** – Analytics, export, profile, fallbacks, etc.
- **NFR01, NFR03–NFR05, NFR07, NFR10–NFR12, NFR14–NFR17** – Security, performance, privacy, backup, accessibility.

**Tip:** Use a 3-column layout: **Implemented** | **Partial** | **Pending** with the IDs or one-line labels above.

---

## Slide 7 — System design

**Slide title:** System design

**Content (bullets):**

- **System design goals:** Integrated platform (résumé + job parsing, question generation, semantic feedback, progress tracking); candidate-centric; scalable and secure.
- **Methodology:** Object-Oriented Analysis and Design (OOAD); modular components (Resume Parser, Question Generator, Feedback Engine, Analytics).
- **Development:** Agile (Scrum), 4 sprints.
- **Stack:** Next.js 14, FastAPI, PostgreSQL, NER/LLM; OOP (TypeScript, Python).
- **Research methodology:** Saunders Research Onion – Pragmatism, abductive, mixed methods; DSR + experiment + survey.

---

## Slide 8 — Overall system architecture

**Slide title:** Overall system architecture

**High-level (target system):**

- **Flow:** User → Browser → Next.js (frontend) → FastAPI (backend) → NER / LLM / Semantic modules → PostgreSQL & AWS S3.
- **Caption:** Current prototype implements NER + DB; LLM and Semantic are pending.

**Current prototype (IPD scope):**

- **Flow:** CV Upload page + Job Description page → POST /api/v1/resumes/extract, POST /api/v1/jobs/extract → PDF text extraction + Resume NER + Job Poster NER → response; resume data persisted in PostgreSQL; Edit via PATCH.
- **Caption:** Resume and job extraction flow; edit entities via PATCH.

**Wireframes (short descriptions or sketches):**

- **Upload résumé:** Tabs (Upload PDF | Paste text), Extract button → “Extracted information” card (Name, Email, Skills, Occupation, Education, Experience) + Edit button.
- **View parsed entities:** Same page; Edit opens modal; “Replace resume” returns to upload/paste.
- **Job description:** Paste or upload job → Extract → result card (e.g. Job title, Company, Skills required, Experience required, Education required).

**Tip:** Use the Mermaid diagrams from `docs/ipd/architecture-and-schedule.md` (Section 1 and 2) or redraw in PowerPoint/Google Slides.

---

## Slide 8b (optional) — Dataset creation: combining different datasets

**Slide title:** Dataset creation — combining different datasets

**Use this slide if you want to explicitly present how and why we built the training data.**

**What we did:**

- **Resume NER data:** Merged multiple sources into one training file:
  - Existing `entity_recognition_in_resumes.json` (~220 resumes).
  - Dotin dataset (545 annotated CVs); optionally vrundag91 and minhquan corpora.
  - `prepare_data.py` maps each source’s labels (e.g. Dotin’s 12 types) to a **unified schema:** NAME, EMAIL, SKILL, OCCUPATION, EDUCATION, EXPERIENCE, O.
  - Output: `merged_resume_ner.json`.
- **Job poster NER data:** SkillSpan (NAACL 2022, 11k+ sentences) converted to our JSONL; `prepare_data.py` merges sources and maps labels (Skill, Qualification, Experience, Occupation, etc.) to **unified job-poster types:** JOB_TITLE, COMPANY, SKILLS_REQUIRED, EXPERIENCE_REQUIRED, EDUCATION_REQUIRED, etc. Output: `merged_job_poster_ner.json`.

**Why we combined datasets:**

- **More training data** — single public datasets are often too small for robust NER.
- **Consistent labels** — one schema so the model learns the same entity set regardless of source.
- **Diversity** — different annotators and sources help reduce bias and improve generalization.

---

## Slide 9 — Updated time schedule

**Slide title:** Updated time schedule

**Gantt table:**

| Deliverable              | Original (PPRS) | Updated / actual | Note                                              |
|--------------------------|------------------|------------------|---------------------------------------------------|
| Project proposal (drafts)| Sep–Oct 2025     | Sep–Oct 2025     | As planned.                                       |
| Literature review        | 10 Nov 2025      | 10 Nov 2025      | As planned.                                       |
| SRS / PPRS final         | 13 Nov 2025      | 13 Nov 2025      | As planned.                                       |
| Proof of concept         | 13 Nov 2025      | 13 Nov 2025      | As planned.                                       |
| Design document          | 20 Dec 2025      | 20 Dec 2025      | As planned.                                       |
| **Prototype**            | **2 Feb 2026**   | **2 Feb 2026**   | On track: resume + job extraction; NER integrated.|
| **IPD submission**       | 2 Feb 2026       | **5 Feb 2026**   | IPD deadline 05 Feb 2026 13:00 LK.                |
| Implementation           | 15 Mar 2026      | 15 Mar 2026      | Full implementation (QG, feedback, auth) planned. |
| Testing                  | 20 Mar 2026      | 20 Mar 2026      | As planned.                                       |
| Evaluation               | 25 Mar 2026      | 25 Mar 2026      | As planned.                                       |
| Thesis submission / MVP  | 1 Apr 2026       | 1 Apr 2026       | As planned.                                       |

**Deviations and impact (2–3 bullets):**

- No major delays. Resume NER and Job Poster NER training and integration took priority.
- Prototype scope for IPD: resume + job extraction (no LLM/semantic feedback yet) to ensure a stable, demonstrable build by the deadline.
- Impact: Prototype demonstrates core NER pipeline and integrated FE+BE; question generation and semantic feedback scoped for post-IPD (March–April).

---

## Slide 10 — Progress since PPRS

**Slide title:** Progress since PPRS

**Done:**

- **Dataset creation:** Combined multiple public datasets for both NER models. *Resume:* merged existing 220 resumes + Dotin 545 (+ optional vrundag91, minhquan) via `prepare_data.py` into a unified schema (NAME, EMAIL, SKILL, OCCUPATION, EDUCATION, EXPERIENCE). *Job poster:* SkillSpan (11k+ sentences) converted and merged into unified job-poster labels. *Why:* more training data, one consistent label set, and greater diversity for better generalization.
- Resume NER: training pipeline, BERT-BiLSTM-CRF model, Hugging Face; backend + frontend flow (upload/paste → extract → display → edit).
- Job poster NER: training, model; backend job extract API (PDF/text).
- Frontend: CV Upload page (file drop + paste, entities card, Edit dialog); backend: FastAPI, resume + job routes, PostgreSQL, OpenAPI docs.
- Resume data persisted; PATCH for entity updates.

**Partial:**

- Job extract API (frontend UI optional or added for IPD); resume saved (no practice-session history yet).

**Next (post-IPD):**

- Auth (FR01–FR02); LLM question generation (FR08); chat interface and semantic feedback (FR09–FR12); analytics dashboard (FR15–FR16); hosting and Google Drive submission.

---

## Slide 11 — Conclusion

**Slide title:** Conclusion

**Main takeaways (3–4 bullets):**

- CrackInt aims to be an integrated, AI-driven interview preparation platform: résumé + job parsing, role-specific questions, semantic feedback, and progress tracking.
- The IPD prototype delivers resume and job extraction (NER) with a working frontend and backend; the core NER pipeline is integrated and demonstrable.
- Requirements and architecture are documented with clear **implemented vs pending** status; question generation and semantic feedback are scoped for the next phase.
- Next steps: finalise job UI (if needed), host prototype, submit to Blackboard and Google Form, then proceed to full implementation, testing, and thesis.

---

## Slide 12 — References

**Slide title:** References

**Rule:** Alphabetical order; **only** references you actually cited in the slides.

**Suggested list (include only those cited):**

- Baby et al. (2025)
- Beck, K. et al. (2001). Agile. (cite full reference if required)
- Daryanto et al. (2024)
- Daryanto et al. (2025)
- Fulk (2022)
- Horodyski (2023)
- Jones (2020)
- Lewton & Haddad (2024)
- Machhale et al. (2024)
- Saunders et al. (2019). Research Onion. (cite full reference if required)

**Optional (if cited):** Big Interview, HireVue, VMock, Huntr, Kickresume, FairHire, Conversate, Prepmania.

Use your thesis or module referencing style (e.g. APA, Harvard) consistently.

---

## Slide 13 — Thank you (optional)

**Slide title:** Thank you

**Content:**

- **Thank you**
- Optional: Contact / project link / supervisor name

---

## Quick checklist before recording

- [ ] Slide 1: Project title, your name, W1998730, supervisor, IPD.
- [ ] Slide 2: Agenda matches actual slide order.
- [ ] Slide 5: Onion diagram (four layers) + stakeholder table.
- [ ] Slide 6: Implemented / Partial / Pending clearly shown.
- [ ] Slide 8: High-level and current prototype architecture; wireframes described or shown.
- [ ] Slide 9: Gantt table + deviations explained.
- [ ] Slide 10: Progress since PPRS in one clear list.
- [ ] Slide 12: References alphabetical; only cited sources.
- [ ] Rehearse: total content fits **20 minutes**.
