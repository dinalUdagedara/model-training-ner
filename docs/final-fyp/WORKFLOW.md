# Final thesis — writing workflow

## Why this order

Examiners care that **claims match evidence**. Writing **Implementation → Testing → Evaluation → Conclusion → Abstract** first forces you to **collect evidence** early. Introduction and literature can be polished after the “truth” is fixed.

## Suggested chapter order (production)

1. **Ch 7 Implementation** — Stack, modules, screenshots, map features → FR IDs from SRS.
2. **Ch 8 Testing** — NER metrics table; functional test cases vs FRs; pass %; NFR checks where feasible; limitations.
3. **Ch 9 Critical evaluation** — Use **[chapter-09-critical-evaluation-DRAFT.md](./chapter-09-critical-evaluation-DRAFT.md)** (template §9.1–9.9); FR/NFR summary vs **[IMPLEMENTED-VS-PENDING-FINAL.md](./IMPLEMENTED-VS-PENDING-FINAL.md)** (verify in app before finalising).
4. **Ch 10 Conclusion** — Use **[chapter-10-conclusion-DRAFT.md](./chapter-10-conclusion-DRAFT.md)**; objectives table must match **Chapter 01** Table 1.
5. **Abstract** — ≤300 words; para 1 problem, para 2 method, para 3 **numbers** from Ch 8.
6. **Ch 4 SRS** — Update MoSCoW and diagrams if the app changed after IPD.
7. **Ch 5 SLEP** — Tie to real data handling (auth, API keys, consent for interviews).
8. **Ch 6 Design** — Architecture + sequence diagrams + wireframes/screenshots consistent with Ch 7.
9. **Ch 1–3** — Polish: aim, objectives, LR; fix scope if needed.

## Per-chapter habit

Before saving a section:

- **Product sentence?** → Confirm in `PROJECT` or `API_OVERVIEW.md`.
- **Number (F1, split size)?** → Confirm in notebooks / `THESIS-FACTS-SHEET.md`.

## Screenshots

Capture one **consistent** environment (same theme, same sample CV/job). Name files clearly, e.g. `fig-7-1-cv-upload.png`, and list them in **List of figures** in Word.

## References

Harvard; ≥20 sources; ≥80% strong venues — track citations as you write (Zotero/Mendeley or Word citations).
