# IPD (Interim Progression Demonstration) — Documentation

All documents for the IPD submission (6COSC023W, 15% of FYP). **Deadline:** 05 February 2026, 13:00 LK time. Submit to **both** Blackboard and Google Form.

---

## Contents

| Document | Purpose |
|----------|---------|
| [requirements-analysis.md](requirements-analysis.md) | Submission rules, marking criteria, mandatory components, slide structure, checklist. **Start here** for what to submit and how it is marked. |
| [requirements-short.md](requirements-short.md) | Short summary: deadline, what to submit, how it is marked, quick checklist. |
| [requirements-implemented-vs-pending.md](requirements-implemented-vs-pending.md) | FR/NFR table with **Implemented / Partial / Pending** and file locations. Use for the "Formal requirements specification" slide and "Progress since PPRS". |
| [current-state-audit.md](current-state-audit.md) | Audit of what is done vs not done (NER, prototype, IPD docs). |
| [prototype-scope.md](prototype-scope.md) | Minimum viable prototype scope for IPD (resume + job extraction). |
| [architecture-and-schedule.md](architecture-and-schedule.md) | High-level and current prototype architecture (Mermaid), wireframes, updated Gantt and deviations. Use for "Overall system architecture" and "Updated time schedule" slides. |
| [building-the-slides.md](presenttion/building-the-slides.md) | **Step-by-step guide to build the presentation:** slide order, content for each slide (with source doc + section), talking points, and checklist before recording. |
| [presentation-material.md](presentation-material.md) | **Full content for every slide:** copy-paste ready text, bullets, tables, and references for all 12–13 slides in one document. |
| [presentation-full-speech-20min.md](presentation-full-speech-20min.md) | **Full speech for the presentation:** word-for-word ~20-minute script aligned to your slide order, with timings. |
| [demo-video-script.md](demo-video-script.md) | **Demo video script and outline:** code walk-through (max 7 min) for both NER models and job extractor, prototype demo steps (max 3 min), talking points, and checklist before recording. |
| [demo-video-full-speech.md](demo-video-full-speech.md) | **Full speech for the demo:** word-for-word script to read aloud for Part A (repo, resume NER, job NER, job extractor, frontend) and Part B (live demo and closing); includes a short version if you need to trim time. |

### IPD thesis chapter drafts (missing from PPRS)

| Document | Purpose |
|----------|---------|
| [chapter-05-slep.md](chapter-05-slep.md) | **Chapter 5: SLEP** — Social, Legal, Ethical, Professional issues; 2×2 table; BCS Code of Conduct; consent and data handling. |
| [chapter-06-design.md](chapter-06-design.md) | **Chapter 6: Design** — Design goals, system architecture, BiLSTM-CRF algorithm, detailed design, UI wireframes. |
| [chapter-07-implementation.md](chapter-07-implementation.md) | **Chapter 7: Implementation** — Technology stack, dataset/NER stats, core modules, code structure, UI, challenges and solutions. |
| [abstract-initial-results.md](abstract-initial-results.md) | **Abstract paragraph 3** — Initial results: NER metrics (F1 0.79), per-entity performance, integration. Copy-paste for IPD abstract. |
| [chapter-08-time-schedule-updated.md](chapter-08-time-schedule-updated.md) | **Chapter 8: Time Schedule** — Updated Gantt, actual vs planned, deviations, impact. |

### Diagrams

| Folder | Purpose |
|--------|---------|
| [diagrams/](diagrams/) | Mermaid diagram files (.mmd) for Chapter 4 & 6: Stakeholder Onion, System Architecture, Prototype Component, Class Diagram, Sequence Diagrams (Resume, Job, Session), Activity Diagram, BiLSTM-CRF Architecture. Use [mermaid.live](https://mermaid.live) to export to PNG/SVG. |
| [diagrams/10-ui-wireframes-spec.md](diagrams/10-ui-wireframes-spec.md) | UI wireframe specifications (ASCII layouts + element specs) for draw.io/Figma. |

---

## Related

- **Project proposal summary (PPRS):** [../project/proposal-summary.md](../project/proposal-summary.md) — stakeholders, problem, research gap, use cases, FR/NFR list, references for slides.
- **Prototype code:** See path `PROJECT` in [requirements-implemented-vs-pending.md](requirements-implemented-vs-pending.md) (crackint-frontend + crackint-backend).
- **NER training / data:** Repository root `resume_ner_pipeline/`, `job_poster_ner_pipeline/`, `fyp/`.
