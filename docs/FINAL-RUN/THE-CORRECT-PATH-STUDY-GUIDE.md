# The Correct Path — Deep Study Guide (Viva Ready)

This is the expanded, exam-focused version of **Section 1: The Correct Path** from your viva guide.
Use this file to study in sequence and build confidence even if you are restarting from zero.

---

## How to use this guide

For each step:

1. Read the **Purpose**
2. Learn the **What to say**
3. Learn the **Evidence to show**
4. Practice the **Likely viva questions**
5. Use the **Answer frame**

Do not skip steps. This sequence is designed to match how examiners test ownership and reasoning.

---

## Step 1 — Project Story in 2 Minutes

## Purpose
You must open the viva with a clear, controlled narrative.  
This sets examiner confidence before technical probing starts.

## What to say (core content)
- Project title and one-line summary.
- Real problem in current interview-prep tools (fragmented, generic, limited actionable feedback).
- Your solution: unified platform combining resume understanding, job understanding, and practice feedback.
- System scope: web app + backend + NER + optional LLM modules.
- Outcome headline: working prototype + measurable model performance + evaluation insights.

## Your recommended story structure (memorize)
- **Problem:** Candidate interview prep tools are often generic and disconnected.
- **Gap:** Existing systems do not reliably combine resume-aware + job-aware + semantic coaching in one flow.
- **Solution:** CrackInt integrates extraction, analysis, and interactive preparation in one platform.
- **Result:** You delivered a functional system with tested backend/frontend flows and measurable NER results.

## Evidence to show
- Report abstract and chapter map
- Architecture figure
- Key metric tables (resume NER/job NER)
- Demo path (upload -> extraction -> session -> feedback)

## Likely viva questions
- "Summarize your project in under 2 minutes."
- "Why does this project matter in practice?"
- "What exactly is your final contribution?"

## Answer frame
- One sentence problem
- One sentence solution
- One sentence technical method
- One sentence results
- One sentence contribution

---

## Step 2 — Problem -> Gap -> Aim -> Objectives Alignment

## Purpose
Examiners check whether your work is academically coherent, not just technically built.

## What to say
- Problem statement defines real pain points.
- Literature and platform review identified specific unresolved gaps.
- Aim addresses the exact gap.
- Objectives operationalize aim into concrete deliverables.
- Later chapters provide evidence objective-by-objective.

## Critical quality check
You must avoid mismatch such as:
- Aim says "semantic evaluation", but implementation only does keyword matching.
- Objective says "evaluation with stakeholders", but no stakeholder evidence shown.

## Evidence to show
- Chapter 1: problem, gap, aim, objectives
- Chapter 2: supporting literature gap
- Chapter 7/8/9/10: objective achievement evidence
- Objective-achievement table in conclusion/evaluation sections

## Likely viva questions
- "What is your exact research gap?"
- "How do your objectives map to implementation?"
- "Which objective was hardest and why?"

## Answer frame
- "The gap is X, supported by Y literature/platform findings."
- "The aim is Z, and objectives O1..On implement that aim."
- "Evidence appears in chapter/table A/B/C."

---

## Step 3 — Methodology Justification

## Purpose
This is where many students lose marks. You must justify *why* your approach is valid.

## What to say
- Why your philosophy/approach fits an applied software + AI artifact.
- Why mixed methods were needed (not one method only).
- How triangulation improved reliability/validity.
- How ethics/risk were considered during design and implementation.

## Minimum justification you should be fluent with
- **Pragmatism:** chosen because project success depends on practical outcomes + measurable evidence.
- **Abductive logic:** combined existing theory with iterative design/implementation insights.
- **Mixed methods:** interviews/survey/analysis for requirements + quantitative metrics for model/system performance.
- **Triangulation:** multiple evidence sources reduced single-source bias.

## Evidence to show
- Methodology chapter
- Elicitation tables and synthesis section
- Risk and SLEP sections
- Testing/evaluation chapters showing quantitative+qualitative evidence

## Likely viva questions
- "Why this methodology over alternatives?"
- "How did you ensure validity?"
- "How did requirements evidence change implementation decisions?"

## Answer frame
- "I selected methodology M because project type T requires A+B."
- "Validity was strengthened via sources S1/S2/S3 and cross-confirmation."
- "This directly changed design decision D."

---

## Step 4 — Design and Architecture Decisions

## Purpose
Examiners test whether your architecture is intentional or accidental.

## What to say
- Main architecture components and boundaries.
- Why each major technology was selected.
- Key data flow across frontend, backend, DB, ML, optional LLM services.
- Trade-offs accepted and why.

## Must-cover points for your project
- Frontend: Next.js + React Query + auth/session handling
- Backend: FastAPI modular routers + service layer + SQLModel/SQLAlchemy
- Data: PostgreSQL + JSONB for flexible entity storage
- ML: resume/job NER modules loaded at startup; hybrid extraction logic
- Optional AI features controlled by config flags (safe degradation path)

## Evidence to show
- Design chapter architecture diagrams
- Backend router/service/module structure
- Model runtime files
- API endpoint behavior in docs/code

## Likely viva questions
- "Why this stack?"
- "How does one user action move through your system?"
- "What fails gracefully and what fails hard?"

## Answer frame
- "Chosen stack optimizes X, Y, Z constraints."
- "Flow is: UI -> API route -> service -> model/DB -> response."
- "If feature F is disabled/unavailable, fallback behavior is B."

---

## Step 5 — Implementation Depth

## Purpose
This proves ownership. Examiners will drill into code-level decisions.

## What to say
- Main modules and responsibilities.
- Separation of concerns (route vs service vs model vs agent).
- Novel code vs adapted patterns vs third-party libraries.
- Security and reliability controls (auth, validation, error handling).

## Your implementation strengths to highlight
- Clean API module segmentation
- Ownership checks per user on protected resources
- File type/size validation and error responses
- Session chat orchestration with persistent message flow
- Distinction between deterministic logic and LLM-dependent logic

## Evidence to show
- Backend route files and services
- Frontend service layer and state/mutation logic
- Validation hooks and shared API/auth utilities
- Novel/adapted/third-party mapping table

## Likely viva questions
- "Show me where ownership checks are enforced."
- "Which parts are your original work?"
- "What happens if external AI service fails?"

## Answer frame
- "Ownership is enforced in dependency + route-level checks."
- "Original contributions are A/B/C; adapted elements are D/E; third-party are F/G."
- "Failures fall back to H with user-safe behavior."

---

## Step 6 — Testing and Evaluation Evidence

## Purpose
Examiners need proof that your system works beyond demonstration.

## What to say
- Testing strategy categories: functional, non-functional, system-level, model-level.
- What metrics were used and why.
- What results mean in practical terms.
- What failed/limited and how you interpreted that critically.

## For your ML defense
- Explain precision/recall/F1 and micro-F1 clearly.
- Explain why residual error remains (data complexity, label ambiguity, unseen formats, span alignment limits).
- Explain entity-wise performance differences (easy vs hard entities).

## For software testing defense
- Input validation cases
- API behavior and negative-path handling
- user-flow stability expectations
- representative non-functional checks

## Evidence to show
- Testing chapter tables
- Model result tables
- Appendix test cases/results
- Evaluation chapter findings

## Likely viva questions
- "Why is your F1 acceptable for this scope?"
- "What evidence shows robustness?"
- "What are your highest-risk failure points?"

## Answer frame
- "Metric M is suitable because objective O requires..."
- "Results R validate baseline practicality, with limitations L."
- "Highest risks are X and mitigations are Y."

---

## Step 7 — Critical Reflection

## Purpose
High marks require mature reflection, not defensive perfection claims.

## What to say
- What worked well and why.
- What did not fully work and why.
- Constraints (time/data/scope/external dependencies).
- What you learned technically and academically.
- Prioritized future improvements.

## Good reflection behavior
- Be specific, not generic.
- Link limitations to evidence.
- Show realistic next steps, not impossible promises.

## Evidence to show
- Critical evaluation chapter
- Limitations sections
- Conclusion/future work section
- Risk/mitigation discussions

## Likely viva questions
- "What is the biggest limitation?"
- "What would you do first with 3 more months?"
- "Where did your assumptions fail?"

## Answer frame
- "Limitation L happened due to C under scope constraints."
- "I mitigated with M."
- "Next best improvement is I because impact-to-effort is highest."

---

## Step 8 — Viva Defense Readiness

## Purpose
Convert knowledge into reliable performance under pressure.

## What to do
- Practice short, structured answers aloud.
- Keep chapter-to-evidence mapping ready.
- Prepare fallback explanations if demo fails.
- Practice random-question response without panic.

## Use this 5-part answer template always
1. Direct answer
2. Why
3. Evidence
4. Limitation
5. Next step

## Quick pressure control rule
If stuck:
- acknowledge scope
- answer what you can prove
- point to evidence
- propose grounded improvement

---

## 10-Minute Daily Drill (Busy Schedule Friendly)

- 2 min: project story
- 2 min: problem-gap-aim-objectives mapping
- 2 min: architecture + one core flow
- 2 min: testing + metric interpretation
- 2 min: limitation + future work defense

Do this daily until viva day.

---

## Fast Self-Assessment (Score Yourself 0-2 each)

Rate each item:
- 0 = cannot explain
- 1 = partial
- 2 = clear and confident

Checklist:
- [ ] I can explain project story in 2 minutes.
- [ ] I can define the gap with evidence.
- [ ] I can justify methodology choices.
- [ ] I can explain architecture and data flow.
- [ ] I can defend implementation ownership.
- [ ] I can interpret model/software test evidence.
- [ ] I can discuss limitations without hesitation.
- [ ] I can answer unexpected questions with structure.

Target score before viva: **14+ / 16**

---

## Final Note

This guide is designed to be highly accurate and viva-ready based on your report, codebase structure, and supervisor expectations.
For best results, pair this with:

- `docs/FINAL-RUN/VIVA-PREPARATION-GUIDE.md`
- `docs/FINAL-RUN/PROJECT-MASTERY-MAP.md`

