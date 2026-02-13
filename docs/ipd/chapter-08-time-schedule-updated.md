# Chapter 08: Time Schedule (Updated with Actual Progress)

**Purpose:** IPD thesis Chapter 8. Updated Gantt chart showing actual progress up to IPD and tentative timeline for remaining deliverables.

---

## 8.1 Chapter Overview

This chapter presents the project timeline for CrackInt, updated to reflect actual progress as of the Interim Project Demo (IPD) submission. It compares planned versus actual completion dates for key deliverables and explains any deviations.

---

## 8.2 Updated Gantt Chart and Deliverables

### 8.2.1 Deliverables Table

| Deliverable | Original (PPRS) | Actual / Updated | Status |
|-------------|------------------|------------------|--------|
| Project proposal (initial draft) | 26 Sep 2025 | 26 Sep 2025 | ✓ Completed |
| Project proposal (final draft) | 24 Oct 2025 | 24 Oct 2025 | ✓ Completed |
| Literature review | 10 Nov 2025 | 10 Nov 2025 | ✓ Completed |
| SRS / PPRS final | 13 Nov 2025 | 13 Nov 2025 | ✓ Completed |
| Proof of concept | 13 Nov 2025 | 13 Nov 2025 | ✓ Completed |
| Design document | 20 Dec 2025 | 20 Dec 2025 | ✓ Completed |
| **Prototype** | **2 Feb 2026** | **2 Feb 2026** | ✓ Completed |
| **Interim Project Demo (IPD)** | **2 Feb 2026** | **5 Feb 2026** | ✓ On track |
| Implementation (full) | 15 Mar 2026 | 15 Mar 2026 | Tentative |
| Testing | 20 Mar 2026 | 20 Mar 2026 | Tentative |
| Evaluation | 25 Mar 2026 | 25 Mar 2026 | Tentative |
| Thesis submission / MVP | 1 Apr 2026 | 1 Apr 2026 | Tentative |
| Dataset and source code | — | 30 Mar 2026 | Tentative |

### 8.2.2 Work Breakdown and Timeline

| Task | Start | End | Duration | Notes |
|------|-------|-----|----------|-------|
| Proposal & PPRS | Sep 2025 | Nov 2025 | ~8 weeks | Completed |
| Literature review | Oct 2025 | Nov 2025 | ~4 weeks | Completed |
| Design document | Nov 2025 | Dec 2025 | ~4 weeks | Completed |
| NER model training | Nov 2025 | Jan 2026 | ~8 weeks | BiLSTM-CRF Path 2 finalised |
| Backend development | Dec 2025 | Jan 2026 | ~6 weeks | FastAPI, resume/job extract, sessions |
| Frontend development | Dec 2025 | Feb 2026 | ~8 weeks | Next.js, CV upload, job upload, sessions |
| Prototype integration | Jan 2026 | Feb 2026 | ~2 weeks | End-to-end flow working |
| IPD submission | — | 5 Feb 2026 13:00 LK | — | Blackboard + Google Form |
| Full implementation | Feb 2026 | Mar 2026 | ~6 weeks | QG, semantic feedback, auth |
| Testing & evaluation | Mar 2026 | Mar 2026 | ~2 weeks | User testing, metrics |
| Thesis & MVP | Mar 2026 | 1 Apr 2026 | ~2 weeks | Documentation, submission |

---

## 8.3 Deviations and Impact

### 8.3.1 Completed as Planned

- Proposal, PPRS, literature review, design document, and proof of concept were completed on schedule.
- Resume NER (BiLSTM-CRF Path 2) was trained and evaluated; Test F1 ≈ 0.79 achieved.
- Backend (FastAPI) and frontend (Next.js) were developed with resume extraction, job extraction, and session/message APIs.
- Prototype is runnable with CV upload, job description extraction, entity edit, and session persistence.

### 8.3.2 Minor Adjustments

- **IPD deadline:** Official submission 5 Feb 2026 13:00 LK (Blackboard + Google Form). Prototype and demo materials to be ready by this date.
- **Scope for IPD:** Prototype focuses on resume NER, job poster NER, and integrated FE+BE. Question generation (LLM) and semantic feedback are planned for post-IPD (March–April).

### 8.3.3 Impact Assessment

- No major delays. NER training and integration were prioritised to ensure a stable, demonstrable build.
- Prototype demonstrates the core NER pipeline and end-to-end flow, meeting the IPD scope.
- Question generation and semantic feedback remain clearly scoped for the final implementation phase.

---

## 8.4 Chapter Summary

The project timeline has been largely adhered to. Completed deliverables include proposal, PPRS, literature review, design, NER model training, backend and frontend development, and prototype integration. The IPD submission is scheduled for 5 Feb 2026. Remaining work—full implementation (question generation, semantic feedback, authentication), testing, evaluation, and thesis submission—is planned for March–April 2026.
