# Final Thesis — Checklist (from IIT/Westminster 2025–26 template)

**Derived from:** `[Template FYP -2025_26] Final Thesis .docx`  
**Full verbatim export:** `thesis-template-2025-26-export.md` (and `thesis-template-2025-26-FULL-TEXT.txt`)

Use this as a **tick-list** while you align your CrackInt thesis to the official template.

---

## Global rules (highest priority)

- [ ] **Page limit (marking):** Only the **first 100 pages** of **Introduction → Conclusion** count. Nothing beyond that is evaluated.
- [ ] **Numbering:** **Roman numerals (i, ii, iii…)** from **Abstract** through **List of abbreviations**. **Arabic (1, 2, 3…)** from **Introduction** to **Conclusion**.
- [ ] **Cover page:** No page number on cover (per template note).
- [ ] **TTT structure:** Tell what you will tell → tell it → tell what you told.
- [ ] **Figures/tables:** Only your own work; every figure needs a **caption** and a **short explanatory paragraph** before/after.
- [ ] **Appendix:** Do **not** put essential arguments/results only in appendix — examiners may skip it.
- [ ] **Formatting:** Times New Roman; chapter title **16pt, ALL CAPS, bold**; 1st-level subhead **14pt**; 2nd-level **12pt**; body **12pt, 1.5 line spacing, justified**; **1 inch** margins.
- [ ] **Header:** Left = short project name; Right = chapter name. **No decorative lines** (except coversheet if required).
- [ ] **Footer:** Centre = page number; include **first name + initials** or **student ID** (IIT / UoW).
- [ ] **References:** **Harvard** style; **≥20 sources**; **≥80%** from **high-impact journals/conferences**. References **do not** count toward the 100-page body limit.
- [ ] **Appendices** also **do not** count toward the 100-page limit.

---

## Front matter (before Chapter 1)

| Section | Check |
|--------|--------|
| Cover page (standard template) | [ ] |
| Abstract | [ ] |
| Declaration | [ ] |
| Acknowledgement | [ ] |
| Table of contents (all sections + page numbers) | [ ] |
| List of figures (number, caption, page) | [ ] |
| List of tables (number, title, page) | [ ] |
| List of abbreviations | [ ] |

---

## Abstract (template rules)

- [ ] **≤ 300 words**
- [ ] **Three paragraphs:** (1) Problem (2) Methodology (3) **Initial quantitative results** (e.g. metrics relevant to your work)
- [ ] **ACM CCS** subject descriptors (hierarchical, `→` style as in template)
- [ ] **3–5 keywords**

---

## Chapter 01: Introduction

| Section | What to include | Check |
|--------|-----------------|-------|
| 1.1 Chapter overview | Preview of chapter | [ ] |
| 1.2 Problem background | Domain context; **max ~1.5 pages** | [ ] |
| 1.3 Problem definition | Concise problem; **~½–⅔ page** | [ ] |
| 1.3.1 Problem statement | **One sentence** “in a nutshell” | [ ] |
| 1.4 Research motivation | Why it matters / technical challenge; **one paragraph** | [ ] |
| 1.5 Existing work | **Table:** citation, summary, limitation, contribution + **critical paragraph** | [ ] |
| 1.6 Research gap | Justify need for your project | [ ] |
| 1.7 Contribution | Problem-domain + research-domain contributions | [ ] |
| 1.8 Research challenges | Key challenges | [ ] |
| 1.9 Research questions | **3–4 RQs** (answers = thesis) | [ ] |
| 1.10 Research aim | Clear aim statement | [ ] |
| 1.10 Research objectives | Table: objectives, description, **LO mapping**, **RQ mapping** | [ ] |
| 1.11 Scope | 1.11.1 In scope / 1.11.2 Out of scope | [ ] |
| 1.12 HW/SW requirements | Tables: dev CPU, training GPU (if any), software/tools | [ ] |
| 1.13 Chapter summary | | [ ] |

---

## Chapter 02: Literature review

| Section | Check |
|--------|-------|
| 2.1 Chapter overview | [ ] |
| 2.2 Concept map | Visual map of LR focus | [ ] |
| 2.x Problem domain | Detailed domain discussion (template uses 2.2/2.3 — align numbering with your TOC) | [ ] |
| Existing work | Critical review; **Google Scholar** forward/backward citation strategy as suggested | [ ] |
| Large survey table | Pipeline/columns as appropriate to your topic | [ ] |
| 2.4 Dataset selection | Datasets + citations | [ ] |
| 2.5 Benchmarking & evaluation | Compare prior work on clear criteria | [ ] |
| Chapter summary | Gaps → link to your work | [ ] |

*(Template also includes an example LR outline with subdomains, metrics, benchmarking — mirror structure to your project.)*

---

## Chapter 03: Methodology

| Section | Check |
|--------|-------|
| 3.1 Chapter overview | [ ] |
| 3.2 Research methodology | **Saunders Research Onion** in **table** (philosophy, approach, choice, strategy, time horizon, etc.) | [ ] |
| 3.3 Development methodology | Waterfall vs Agile/Scrum etc. + **justification** | [ ] |
| 3.3.1 Requirement elicitation methodology | Interviews, surveys, documents, brainstorming, etc. | [ ] |
| 3.3.2 Design methodology | SSADM vs OOADM (pick what matches your system) | [ ] |
| 3.3.3 Programming paradigm | OOP / structured / functional as relevant | [ ] |
| 3.3.4 Testing methodology | Model testing + prototype testing | [ ] |
| 3.3.5 Solution methodology (optional expanded steps) | Dataset → preprocess → train → test → iterate | [ ] |
| Project management | Scope, **Gantt** (WBS, start/end dates), deliverables | [ ] |
| Risk & mitigation | Table: severity × frequency, mitigations | [ ] |
| Chapter summary | [ ] |

**Note:** Template’s sample Gantt dates include **thesis submission 30 Mar 2026** — reconcile with your **actual** module deadline.

---

## Chapter 04: Software Requirement Specification (SRS)

| Section | Check |
|--------|-------|
| 4.1 Chapter overview | [ ] |
| 4.2 Rich picture | Purpose + diagram | [ ] |
| 4.3 Stakeholder analysis | Onion model + **viewpoints table** | [ ] |
| 4.4 Elicitation methodology selection | Why each method | [ ] |
| 4.5 Findings per method | Literature / interviews (codes-themes) / survey (n sent, n received) / brainstorming | [ ] |
| 4.6 Summary of findings | Triangulation | [ ] |
| 4.7 Context diagram | Level 0 DFD style | [ ] |
| 4.8 Use case diagram | Actors consistent with context diagram | [ ] |
| 4.9 Use case descriptions | Main UCs in chapter; rest can point to appendix | [ ] |
| 4.10 Requirements | **MoSCoW** on all **FR** and **NFR** | [ ] |
| 4.11 Chapter summary | [ ] |

---

## Chapter 05: SLEP

- [ ] **BCS Code of Conduct** referenced and applied **specifically** to your project
- [ ] **2×2 grid:** Social / Legal × Ethical / Professional + mitigations
- [ ] Consent called out where needed (e.g. interviewee names)
- [ ] Chapter summary

---

## Chapter 06: Design

- [ ] Design goals aligned with **NFRs** from SRS
- [ ] **System architecture** (tiered/layered) + explain each tier
- [ ] **Detailed design** (class/sequence/activity per OOAD, or DFD per SSADM)
- [ ] **Algorithm / NN architecture** section for ML core
- [ ] **UI:** low-fidelity wireframes; usability & accessibility notes  
  *(Template: wireframes in design **or** screenshots in implementation — not necessarily both.)*
- [ ] Chapter summary

---

## Chapter 07: Implementation

- [ ] Technology selection justified (stack visualization + languages, frameworks, libs, IDE)
- [ ] **Dataset:** sizes, splits, collection process if custom
- [ ] Core modules mapped to **FRs**; code structure; **cite** any reused code
- [ ] UI implementation + backend integration + accessibility
- [ ] Challenges & solutions
- [ ] Chapter summary

---

## Chapter 08: Testing

- [ ] Testing objectives
- [ ] Testing criteria (functional, non-functional, **model** testing if ML)
- [ ] **Model testing:** metrics defined; **experiments table** + results
- [ ] **Benchmarking** vs baselines / literature (especially if public dataset)
- [ ] Further evaluations (optional)
- [ ] Results discussion
- [ ] **Functional testing:** test cases vs FRs; **pass rate %**; full cases in appendix
- [ ] **Non-functional testing:** against prioritized NFRs
- [ ] Optional extra testing
- [ ] **Limitations of testing**
- [ ] Chapter summary

---

## Chapter 09: Critical evaluation

- [ ] Evaluation methodology & criteria
- [ ] **Self-evaluation**
- [ ] Evaluators selection
- [ ] Results: template suggests **5 technical + 5 domain** experts where applicable; focus groups / usability if relevant
- [ ] Limitations of evaluation
- [ ] **Mapping:** FR/NFR implementation status
- [ ] Chapter summary

---

## Chapter 10: Conclusion

- [ ] Achievements vs **aim & objectives** (table + discussion)
- [ ] **Course knowledge** used vs **new skills** learned
- [ ] **Learning outcomes** reflection
- [ ] Problems/challenges & how overcome
- [ ] **Deviations** from plan (justified)
- [ ] **Limitations** (link testing limitations + research limits)
- [ ] **Future work**
- [ ] Contribution to body of knowledge
- [ ] Concluding remarks

---

## References & appendices

- [ ] References (Harvard, ≥20, ≥80% strong venues) — *excluded from 100-page count*
- [ ] Appendices A, B, … — *excluded from 100-page count*; only **supporting** material

---

## AI / integrity note (from template)

- [ ] Follow module **Generative AI** guidance; **do not** paste uncited GenAI text as your own.

---

*End of checklist.*
