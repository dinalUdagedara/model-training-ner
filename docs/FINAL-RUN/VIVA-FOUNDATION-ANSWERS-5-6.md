# Viva Foundation Answers (5 & 6)

This file gives viva-ready answers for:

5. SLEP (Social, Legal, Ethical, Professional)  
6. Design chapter

Language is simple spoken English and based on your report content.

---

## 5) SLEP (Social, Legal, Ethical, Professional) — Detailed Answer

In chapter 5, I evaluated the wider impact and responsibility side of my project, not only the technical side.

My SLEP analysis covered:

- social issues,
- legal/compliance issues,
- ethical issues,
- professional responsibilities.

### Social perspective
The system supports job seekers by giving structured interview preparation support.  
But social risk exists if AI feedback is wrong or demotivating.  
So I included mitigations like constructive feedback style, manual correction options, and clear communication of limitations.

### Legal perspective
The main legal focus is personal data protection because users upload CVs and related text data.  
So the system design considers:

- consent before data processing,
- privacy policy clarity,
- data minimization and retention control,
- secure handling of PII,
- compliance-oriented thinking aligned with GDPR/CCPA expectations.

### Ethical perspective
The key ethical concerns are transparency, fairness, and informed consent.

- transparency: users should know that AI is used and has limits,
- fairness: avoid discriminatory behavior and bias-prone design choices,
- informed consent: users must explicitly agree to processing.

### Professional perspective
I aligned this with BCS Code of Conduct principles:

- public interest,
- integrity,
- competence,
- accountability.

Practically, this means:

- no false claims about AI capability,
- documenting model limitations,
- logging/versioning/documentation,
- ownership of decisions and data handling.

### Consent and data handling in my report
- consent from participants where applicable,
- consent during resume upload process,
- anonymization principles for training-use scenarios,
- no uncontrolled handling of sensitive personal content.

So, chapter 5 shows that I treated this as a responsible software system, not only a feature implementation exercise.

---

## 6) Design Chapter — Detailed Answer

Chapter 6 explains how requirements were translated into a concrete architecture and module-level design.

I started with design goals linked to NFRs:

- performance,
- usability,
- accuracy,
- security,
- maintainability,
- reliability.

I then used a **tiered architecture**:

1. **Presentation tier** (Next.js frontend)
2. **Logic tier** (FastAPI backend + ML/AI orchestration)
3. **Data tier** (PostgreSQL + S3 where relevant)

### Data tier decisions
- PostgreSQL stores structured application data (users, sessions, messages, extracted entities, etc.).
- S3/object storage handles binary files (CV PDFs/images and related artifacts).
- This separation improves maintainability and scaling.

### Logic tier decisions
The backend is the control center:

- versioned REST APIs,
- text extraction and OCR support paths,
- resume/job NER services,
- session flow and semantic feedback orchestration,
- optional remote LLM integrations,
- ORM/repository data access layer.

### Presentation tier decisions
Frontend handles user interaction and API-driven state rendering:

- upload/edit flows,
- session/chat interface,
- dashboard/readiness views,
- client-side validation and responsive behavior.

### Detailed module design
Backend modules were separated clearly (`api`, `ml`, `services`, `models`, `config`).  
Frontend modules were also separated (`app`, `components`, `services`, `lib`).

### Data model design
Core entities include:

- User,
- Resume,
- JobPosting,
- PrepSession,
- Message.

JSONB usage supports flexible entity payloads where required.

### Sequence-level design
The chapter includes key sequence flows:

- resume extraction flow,
- job extraction flow,
- session chat flow.

These show request/response progression across tiers and help defend implementation coherence.

So chapter 6 demonstrates that architecture decisions were intentional, requirements-driven, and aligned with quality goals.

---

## Quick 30-Second Backup Versions

## 5) SLEP (short)
In SLEP, I addressed social, legal, ethical, and professional risks of using AI in interview preparation. I covered consent, privacy, fairness, transparency, and accountability, and linked mitigations to practical controls like clear disclosure, manual correction, secure handling, and responsible professional conduct.

## 6) Design (short)
My design uses a three-tier architecture: Next.js frontend, FastAPI logic layer, and PostgreSQL/S3 data layer. I mapped design decisions to NFR goals like performance, security, reliability, and maintainability, and defined clear module boundaries and core sequence flows.

---

## Challenge Questions (SLEP + Design Defense)

## Q1) "Why do we need SLEP for this project?"

**Answer:**  
Because this project processes personal data and gives AI-generated guidance that can influence users.  
So technical correctness alone is not enough; responsible and compliant usage is required.

## Q2) "What is your biggest ethical risk?"

**Answer:**  
A major risk is misleading feedback or biased outcomes.  
Mitigations include transparency, clear limitation communication, and correction/support mechanisms.

## Q3) "How do you handle consent?"

**Answer:**  
Users give consent at relevant points (for example data upload/processing context), and data handling is explained through policy-level communication and controlled processing behavior.

## Q4) "How is legal compliance considered?"

**Answer:**  
Through privacy-first handling, limited retention principles, secure processing, and explicit consent orientation aligned with GDPR/CCPA-style expectations in project scope.

## Q5) "How does BCS Code of Conduct apply here?"

**Answer:**  
It guides public interest, integrity, competence, and accountability.  
In practice, I apply this by documenting limitations, avoiding overclaiming AI accuracy, and maintaining traceable engineering processes.

## Q6) "Why this architecture and not a simpler one?"

**Answer:**  
A simpler monolithic approach might work for a small demo, but this project needs modularity across UI, backend logic, persistence, and AI services.  
Tiered modular design gives better maintainability and clearer responsibility boundaries.

## Q7) "Where exactly is reliability handled in design?"

**Answer:**  
Reliability is addressed through modular service separation, controlled API boundaries, validation paths, persistence consistency, and fallback behavior for AI-dependent features.

## Q8) "How do you prove design is requirement-driven?"

**Answer:**  
The design goals are linked to NFRs in the report, and architecture/module decisions are justified using those goals (performance, security, usability, maintainability, reliability).

## Q9) "Is your architecture scalable?"

**Answer:**  
It is scalable in structure because tiers and modules are separated, storage concerns are split, and services are not tightly coupled.  
This supports extension and operational growth better than tightly mixed design.

## Q10) "What design decision are you most confident about?"

**Answer:**  
Separation of concerns across tiers and modules.  
It made implementation clearer, testing easier, and future extension safer.

---

## Keyword Meanings (Simple)

- **SLEP:** Social, Legal, Ethical, Professional analysis.
- **Privacy:** Protecting user personal information.
- **Consent:** User agrees before processing their data.
- **Transparency:** Clearly telling users what AI is doing and its limits.
- **Fairness:** Avoiding unfair or biased behavior.
- **Accountability:** Taking responsibility for system behavior and decisions.
- **Tiered architecture:** Splitting system into frontend, logic, and data layers.
- **Separation of concerns:** Keeping different responsibilities in different modules.
- **Maintainability:** Easy to update/fix later.
- **Reliability:** System behaves consistently and safely.
- **NFR:** Non-functional requirement (performance/security/usability/etc.).

---

## One-Line Closing for Chapters 5 & 6

My chapter 5 ensures the system is responsible and compliant in context, and chapter 6 ensures the system is technically structured, maintainable, and aligned with requirements.

