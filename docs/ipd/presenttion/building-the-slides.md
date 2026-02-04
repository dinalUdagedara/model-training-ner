# Building the IPD Presentation Slides

**Purpose:** Step-by-step guide to build the 20-minute IPD video presentation. Follow this order; content is pulled from the other docs in this folder and from [../project/proposal-summary.md](../project/proposal-summary.md).

**Timing:** Total **20 minutes**. Content after 20 minutes is **not marked**. Aim for ~2 minutes per slide (about 10–12 slides), or adjust: e.g. 1 slide for short sections, 2 slides for Problem background and Research gap.

---

## Slide order and content sources

| # | Slide title | Source doc & section | Suggested slides | Notes |
|---|-------------|---------------------|------------------|--------|
| 1 | Title | Below | 1 | |
| 2 | Agenda | Below | 1 | |
| 3 | Problem background | [proposal-summary](../project/proposal-summary.md) §2 | 1–2 | Add citation or chart if you have one |
| 4 | Research problem & research gap | [proposal-summary](../project/proposal-summary.md) §3 | 1–2 | Problem then gap; mention existing work |
| 5 | Identification of project stakeholders | [proposal-summary](../project/proposal-summary.md) §5 | 1 | **Onion diagram** + roles |
| 6 | Formal requirements specification | [requirements-implemented-vs-pending](requirements-implemented-vs-pending.md) | 1–2 | **Implemented vs pending** clearly shown |
| 7 | System design | [proposal-summary](../project/proposal-summary.md) §10 | 1 | Goals + OOAD |
| 8 | Overall system architecture | [architecture-and-schedule](architecture-and-schedule.md) §1–3 | 1–2 | Diagrams + wireframes |
| 9 | Updated time schedule | [architecture-and-schedule](architecture-and-schedule.md) §4 | 1 | Gantt + deviations |
| 10 | Progress since PPRS | [current-state-audit](current-state-audit.md), [prototype-scope](prototype-scope.md) | 1 | Clear bullet list |
| 11 | Conclusion | Below | 1 | Main takeaways |
| 12 | References | Below | 1 | Alphabetical, cited only |

---

## 1. Title slide

**Copy or adapt:**

- **Title:** CrackInt: AI-Driven Personalized Interview Preparation Platform  
- **Student:** Udagedara Thiyunu Dinal Bandara  
- **UoW / IIT ID:** W1998730  
- **Supervisor:** Mr. Pubudu Arachchige  
- **Module:** 6COSC023W – Computer Science Final Project | Interim Progression Demonstration (IPD)

---

## 2. Agenda

**Bullets (in point form):**

- Problem background  
- Research problem & research gap  
- Project stakeholders  
- Formal requirements (implemented vs pending)  
- System design  
- Overall system architecture & wireframes  
- Updated time schedule  
- Progress since PPRS  
- Conclusion  
- References  

---

## 3. Problem background

**Source:** [proposal-summary.md](../project/proposal-summary.md) §2 (Problem statement).

**Talking points:**

- Employers use AI for screening; candidate-side prep tools are mostly static (generic questions, one-way video, résumé scoring).
- Gaps: (1) No resume–job awareness, (2) Feedback is superficial (tone/pace, not content), (3) No integrated progress tracking, (4) UX often not real-time or mobile-friendly.
- One sentence: No holistic platform that combines résumé parsing, role-specific question generation, and semantic feedback.

**Slide:** 3–4 short bullets; optional: one citation (e.g. Fulk 2022, Horodyski 2023) or a simple chart if you have one.

---

## 4. Research problem & research gap

**Source:** [proposal-summary.md](../project/proposal-summary.md) §3 (Research gap).

**Slide 1 – Research problem:**  
Current platforms fail to provide personalized, content-aware coaching from both candidate résumé and target job posting; they use static question banks, superficial feedback, and fragmented workflows.

**Slide 2 – Research gap (and existing work):**

- **Gap 1:** No resume–job aware question generation (e.g. VMock, Kickresume don’t combine both).
- **Gap 2:** No semantic-level feedback (e.g. Big Interview: tone/pace, not content depth).
- **Gap 3:** Limited adaptive learning and progress tracking (e.g. Huntr).
- **Gap 4:** No single platform integrating parsing + QG + semantic evaluation (employer tools like FairHire, HireVue serve recruiters, not candidates).

**CrackInt** addresses this by: NER-based résumé/job parsing, LLM question generation, semantic feedback, persistent analytics.

---

## 5. Identification of project stakeholders

**Source:** [proposal-summary.md](../project/proposal-summary.md) §5.

**Must have on slide:** An **onion diagram** (four concentric layers). Text or table:

| Layer | Who | Roles / interests |
|-------|-----|-------------------|
| **1 – Core** | Job seekers, students, early-career professionals | Personalized questions, actionable feedback, progress tracking, affordable access |
| **2 – Operational** | Career services, technical support, development team | Effectiveness, reliability, integration, maintenance |
| **3 – Strategic** | Academic institutions, corporate partners, research community | Outcomes, candidate readiness, accreditation, recruitment efficiency |
| **4 – External** | Regulatory (GDPR/CCPA), AI ethics bodies, competitors, tech providers | Compliance, transparency, bias mitigation, ethical data use |

You can draw the onion in PowerPoint/Google Slides (circles or rounded rectangles) and label each ring.

---

## 6. Formal requirements specification

**Source:** [requirements-implemented-vs-pending.md](requirements-implemented-vs-pending.md) — full tables and “Summary for IPD slides”.

**Requirement:** **Implemented vs pending** must be clearly indicated (10% of marks).

**Slide A – Functional requirements:**

- **Implemented:** FR03 (resume upload), FR04 (resume NER), FR05 (review/edit entities).
- **Partial:** FR06–FR07 (job input & analysis — backend done; frontend optional for IPD), FR14 (resume persisted; no practice sessions yet), FR25 (basic logging).
- **Pending:** FR01–FR02 (auth), FR08–FR13 (question gen, chat, semantic feedback), FR15–FR24 (analytics, export, profile, etc.).

**Slide B – Non-functional requirements (short):**

- **Implemented:** NFR13 (modular architecture, OpenAPI docs).
- **Partial:** NFR02, NFR06, NFR08, NFR09, NFR12, NFR18 (performance, DB, usability, compatibility, logging — partially addressed).
- **Pending:** NFR01, NFR03–NFR05, NFR07, NFR10–NFR12, NFR14–NFR17 (security, privacy, backup, etc.).

Use a simple table or three columns (Implemented | Partial | Pending) with requirement IDs or one-line labels.

---

## 7. System design (one slide)

**Source:** [proposal-summary.md](../project/proposal-summary.md) §10 (Methodology).

**Bullets:**

- **System design goals:** Integrated platform (résumé + job parsing, question generation, semantic feedback, progress tracking); candidate-centric; scalable and secure.
- **Methodology:** Object-Oriented Analysis and Design (OOAD); modular components (Resume Parser, Question Generator, Feedback Engine, Analytics).
- **Development:** Agile (Scrum); stack: Next.js, FastAPI, PostgreSQL, NER/LLM.

Keep to one slide; no need for full UML here (architecture slide has the diagrams).

---

## 8. Overall system architecture

**Source:** [architecture-and-schedule.md](architecture-and-schedule.md) §1 (high-level), §2 (current prototype), §3 (wireframes).

**Slide A – High-level (target):**  
Use the Mermaid diagram from architecture-and-schedule §1, or redraw in PowerPoint: User → Next.js → FastAPI → (NER, LLM, Semantic) → PostgreSQL, S3. Caption: “Current prototype implements NER + DB; LLM and Semantic pending.”

**Slide B – Current prototype:**  
Use the Mermaid from §2, or redraw: CV Upload + Job Description pages → extract APIs → PDF extraction + Resume NER + Job NER → DB. Caption: “Resume and job extraction flow; edit via PATCH.”

**Slide C – Wireframes (optional but recommended):**  
Short descriptions or sketches:

- **Upload résumé:** Tabs (Upload PDF | Paste text), Extract button, then “Extracted information” card with entity groups + Edit.
- **View parsed entities:** Same page; Edit opens modal; “Replace resume” resets.
- **Job description:** Paste/upload job → Extract → result card with job entities (job title, company, skills required, etc.).

You can use simple wireframe screenshots from your app or hand-drawn boxes.

---

## 9. Updated time schedule

**Source:** [architecture-and-schedule.md](architecture-and-schedule.md) §4 (table + “Deviations and impact”).

**Slide content:**

- **Gantt (table or chart):** Use the “Updated time schedule” table from §4 (Deliverable | Original | Updated | Note). Or use the same in a Gantt bar chart (e.g. Excel or thesis Chapter 8 template).
- **Deviations:**  
  - No major delays.  
  - IPD submission date: 05 Feb 2026 13:00 LK (Blackboard + Google Form).  
  - Prototype scope for IPD: resume + job extraction (NER integrated); question generation and semantic feedback planned for post-IPD (March–April).  
  - Impact: Prototype demonstrates core NER and FE+BE integration; QG and feedback clearly scoped for later.

---

## 10. Progress since PPRS (one slide)

**Source:** [current-state-audit.md](current-state-audit.md) (Done), [prototype-scope.md](prototype-scope.md).

**Bullets (clear and concise):**

- **Done:** Resume NER (training, model, Hugging Face); job poster NER (training, model); backend resume + job extract APIs; frontend CV upload flow (upload/paste → extract → display → edit); DB persistence for resumes; OpenAPI docs.
- **Partial:** Job extract API (no frontend UI yet, or added for IPD); resume data saved (no practice-session history yet).
- **Next (post-IPD):** Auth, LLM question generation, chat interface, semantic feedback, analytics dashboard, hosting and Google Drive submission.

Keep to one slide; 5–7 bullets total.

---

## 11. Conclusion (one slide)

**Main takeaways (3–4 bullets):**

- CrackInt aims to be an integrated, AI-driven interview prep platform (résumé + job parsing, role-specific questions, semantic feedback, progress tracking).
- IPD prototype delivers resume and job extraction (NER) with a working frontend and backend; core pipeline is integrated and demonstrable.
- Question generation and semantic feedback are scoped for the next phase; requirements and architecture are documented with clear implemented vs pending status.
- Next steps: complete job UI (if not done), host prototype, submit to Blackboard and Google Form, and proceed to full implementation and testing.

---

## 12. References

**Rule:** Alphabetical order; **only** references you actually cited in the slides.

**Suggested list** (from [proposal-summary.md](../project/proposal-summary.md) §13 — include only those you cited):

- Baby et al. (2025)  
- Beck et al. (2001) – Agile  
- Daryanto et al. (2024, 2025)  
- Fulk (2022)  
- Horodyski (2023)  
- Jones (2020)  
- Lewton & Haddad (2024)  
- Machhale et al. (2024)  
- Saunders et al. (2019) – Research Onion  

Add any other papers or sources you mention (e.g. platform names like Big Interview, VMock, HireVue only if you cited them as primary source; otherwise optional). Use consistent format (e.g. APA or your thesis style).

---

## Checklist before recording

- [ ] Title slide has project title, your name, UoW/IIT ID, supervisor name.  
- [ ] Agenda matches the actual slide order.  
- [ ] Stakeholders slide includes an **onion diagram** (four layers).  
- [ ] Formal requirements slide(s) clearly show **implemented vs pending** (and partial where applicable).  
- [ ] Architecture slide(s) show high-level and current prototype; wireframes included or described.  
- [ ] Updated time schedule includes Gantt and **explanation of deviations**.  
- [ ] Progress since PPRS is one clear slide.  
- [ ] References are alphabetical and only cited sources.  
- [ ] Total content fits **20 minutes** (rehearse and trim if needed).

---

## Where to find everything

| Need | Document |
|------|----------|
| Submission rules, marking, slide list | [requirements-analysis.md](requirements-analysis.md) |
| Problem, gap, stakeholders, use cases, methodology, refs | [../project/proposal-summary.md](../project/proposal-summary.md) |
| Implemented vs pending (FR/NFR) | [requirements-implemented-vs-pending.md](requirements-implemented-vs-pending.md) |
| Architecture diagrams, wireframes, Gantt, deviations | [architecture-and-schedule.md](architecture-and-schedule.md) |
| Done vs not done, scope | [current-state-audit.md](current-state-audit.md), [prototype-scope.md](prototype-scope.md) |
