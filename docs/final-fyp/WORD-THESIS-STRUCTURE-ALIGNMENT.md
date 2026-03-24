# Word thesis — structure alignment (vs IIT 2025/26 template)

Use this when fixing your **`.docx`** export (e.g. content like *Untitled-1*) so chapter numbers, TOC, and examiner expectations match **`docs/thesis-template-2025-26-export.md`**.

---

## 1. Official chapter order (2025/26 export)

| Ch | Title |
|----|--------|
| 1 | Introduction |
| 2 | Literature Review |
| 3 | Methodology *(includes **Gantt / schedule** — see §3.4.2)* |
| 4 | SRS |
| 5 | SLEP |
| 6 | Design |
| 7 | Implementation |
| **8** | **Testing** *(model, functional, non-functional, limitations, summary)* |
| 9 | Critical Evaluation |
| 10 | Conclusion |

**There is no separate “Time Schedule” chapter** in this template. The **Gantt chart** belongs under **Chapter 3** (methodology / project management / schedule), not as Chapter 8.

---

## 2. Problem in *Untitled-1*-style drafts

1. **TOC** lists `CHAPTER 08: TIME SCHEDULE` — that matches an **older** layout, not 2025/26.
2. **Body** has **`CHAPTER 08: TESTING`** *and then* **`CHAPTER 08: TIME SCHEDULE`** → **duplicate Chapter 8** (invalid).
3. **Testing chapter** is incomplete vs template: missing **§8.5** (optional), **§8.8 Non-functional testing** (text references it in summary but body may be missing), **§8.9** (optional).
4. **Internal filenames** in running text (e.g. `THESIS-FACTS-SHEET.md`) — replace with neutral wording for examiners (“project fact sheet” / “frozen evaluation run”) or **Appendix A** references only.

---

## 3. What to do in Word

1. **Keep one Chapter 8 — Testing only.** Use full text from **`chapter-08-testing-DRAFT.md`** (§8.1–8.11).
2. **Move “Time Schedule” content** (deliverables table, Figure 15 Gantt, deviations) into **Chapter 3** as **§3.4.2 Schedule** / **Gantt** (or merge with your existing §3.7 Gantt if you already have one — **one** schedule section, not two).
3. **Delete** the second `CHAPTER 08: TIME SCHEDULE` heading and renumber nothing after Ch 8 until you add **Ch 9** and **Ch 10** if missing.
4. **Update List of Tables / Figures** — Table “Model Metrics” etc. should align with Ch 7/8 numbering after merge.
5. **Regenerate TOC** (Word: References → Update Table of Contents).

---

## 4. Abstract (*Untitled-1* issues)

- Remove **duplicated** middle paragraphs / bullet lists (lines 27–31 area).
- Align claims with **built system**: LLM session Q&A / evaluation are **implemented** where configured — avoid “plans for future phases” if Ch 7 already describes them.
- **NER numbers:** use **`THESIS-FACTS-SHEET.md`** (résumé test micro F1 **0.83**, job-poster **~0.85**) consistently with Ch 7 Tables 7.2 & 7.4 — avoid mixed values across sections unless explicitly justified.

---

## 5. Single source for Ch 8 body

Repo draft: **`docs/final-fyp/chapter-08-testing-DRAFT.md`** — paste into Word and apply template styles; fill pass rate in §8.7 when you finish manual tests.

---

*Last updated: align with IIT 2025/26 template export in this repo.*
