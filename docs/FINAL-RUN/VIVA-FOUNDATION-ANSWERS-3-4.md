# Viva Foundation Answers (3 & 4)

This file gives viva-ready answers for:

1. Methodology justification
2. Design and architecture decisions

The wording is based on your report chapters and written in simple spoken English.

---

## 3) Methodology Justification (Detailed Answer)

For methodology, I picked a practical research style because this project is not only a report, it is also a real working software system.

In my report, I used:

- **Research philosophy: Pragmatism**
- **Research approach: Abductive**
- **Research strategy: Mixed strategy (action research + survey + experiment)**
- **Research choice: Mixed methods**
- **Time horizon: Cross-sectional**

In simple words:

- **Pragmatism** means: "Use what works to solve the real problem."
- **Abductive** means: "Go back and forth between theory and what you see during implementation."
- **Mixed methods** means: "Use both qualitative and quantitative evidence."
- **Cross-sectional** means: "Data/evaluation was done in a project period snapshot, not a long multi-year study."

Why this made sense for my project:

- I had to understand user pain points (qualitative side),
- I had to show measurable system/model results (quantitative side),
- and I had to turn findings into actual engineering decisions.

So I used multiple evidence sources:

- literature review,
- interviews,
- survey,
- competitive analysis,
- brainstorming,
- document analysis.

This is called **triangulation** (checking the same problem from different sources), which improves confidence in findings.

Then I used those findings in implementation:

- requirements guided architecture and feature priorities,
- risks and ethics were considered early,
- testing and evaluation were aligned with those requirements.

So my methodology is justified because it links research evidence to real system delivery in one clear process.

## Methodology Terms — Ultra Simple Viva Cheat Sheet

- **Pragmatism:** I focused on practical solutions that work in real life.
- **Abductive approach:** I started with theory, built the system, then refined decisions based on what I observed.
- **Mixed methods:** I used both human feedback and numeric performance results.
- **Action research:** I improved the system while actively developing and evaluating it.
- **Cross-sectional:** Evaluation happened within the project time window, not over many years.
- **Triangulation:** I used many evidence sources so results are more trustworthy.

---

## 4) Design and Architecture Decisions (Detailed Answer)

My design goal was to build a maintainable, reliable, and extensible interview-preparation system that connects extraction, analysis, and user interaction.

From my design chapter, the key design goals were performance, usability, accuracy, security, maintainability, and reliability.

I used a **tiered architecture**:

- **Presentation tier:** Next.js frontend for user interaction and screen flows.
- **Logic tier:** FastAPI backend for API routing, business logic, NER orchestration, session flow, and optional LLM calls.
- **Data tier:** PostgreSQL for structured transactional data and AWS S3 for file/object storage.

I separated PostgreSQL and S3 because:

- PostgreSQL is best for queryable relational data (users, sessions, messages, job/resume entities),
- S3 is better for binary files and uploaded documents.

In backend design, I used modular separation:

- `api/` for request/response routing,
- `services/` for domain logic like extraction/scoring,
- `ml/` for NER model loading and inference,
- `models/` for ORM entities,
- `config/` for environment and runtime settings.

In frontend design, I separated:

- `app/` routes,
- reusable `components/`,
- `services/` for API communication,
- `lib/` utilities and shared behavior.

For model architecture in design, I documented the BiLSTM-CRF based NER pipeline and the flow from text extraction to entity output.

For user flow, I included sequence diagrams for:

- resume extraction,
- job extraction,
- session chat interaction.

So, design decisions were not random. They were based on non-functional requirements and clear separation of concerns, to improve maintainability, reliability, and scalability.

---

## Quick 30-Second Backup Versions

## 3) Methodology (short)

I used a practical methodology because I needed both research quality and a working system. I used qualitative evidence to understand user needs and quantitative evidence to measure performance. I followed an abductive process by moving between literature and implementation findings to improve design decisions.

## 4) Design (short)

I used a three-tier architecture: Next.js frontend, FastAPI logic layer, and PostgreSQL plus S3 data layer. I separated modules by responsibility to improve maintainability and reliability. Design choices were mapped to NFR goals like performance, security, and usability.

---

## Challenge Questions (Methodology + Design Defense)

## Q1) "Why didn’t you use only one methodology?"

**Answer:**  
Because one method cannot cover everything in this project.  
I needed qualitative evidence to understand user needs and quantitative evidence to validate system performance. Mixed methods gave stronger overall validity.

## Q2) "How can you prove your methodology is valid?"

**Answer:**  
I used multiple evidence sources and triangulated them.  
I did not depend on one source only. Also, the findings were connected to concrete design and implementation decisions, then tested and evaluated.

## Q3) "Why this architecture?"

**Answer:**  
This architecture matches my system needs:

- frontend for interactive user workflows,
- backend for centralized logic and API control,
- separate stores for structured data and binary files.

It keeps the system organized and easier to maintain.

## Q4) "Could this have been a single monolithic script/app?"

**Answer:**  
A small demo could be monolithic, but this project includes multiple workflows, persistence, authentication, and model services.  
So modular layered architecture is better for reliability and future scaling.

## Q5) "What is your strongest design decision?"

**Answer:**  
My strongest decision is clear separation of concerns across tiers and modules.  
It makes each part testable and replaceable, and it reduces coupling between UI, logic, and storage.

## Q6) "Where is AI in your architecture?"

**Answer:**  
AI is in the logic tier:

- NER model inference modules,
- session question/feedback agents,
- CV analysis and fit-related AI services.

But AI is integrated within backend workflows, not used as an isolated standalone script.

## Q7) "What if AI services fail?"

**Answer:**  
The architecture includes reliability controls and fallback behavior.  
Some advanced AI features may degrade, but core platform flows and persisted data remain intact.

---

## One-Line Closing for Section 3 & 4

My methodology gave the right evidence to define and validate the solution, and my architecture translated that into a structured, maintainable, and working system.

---

## Methodology Alternatives Considered (Examiner Defense)

Use these when examiners ask, "What other methodologies did you consider?"

## Q1) "What other methodologies did you consider?"

**Answer:**  
I considered a pure quantitative-only approach, a pure qualitative-only approach, and a strict linear process like waterfall-style research planning.  
I also considered a model-only experimental path without strong user requirement elicitation.

## Q2) "Why didn’t you choose only quantitative methods?"

**Answer:**  
Quantitative-only gives performance numbers, but it does not fully capture user pain points and usability needs.  
My project needed both user understanding and technical measurement.

## Q3) "Why didn’t you choose only qualitative methods?"

**Answer:**  
Qualitative methods are good for understanding needs, but they cannot alone prove model/system performance.  
I still needed measurable evidence from testing and evaluation.

## Q4) "Why not a pure experimental research design?"

**Answer:**  
A pure experiment is good for model benchmarking, but my project is an end-to-end platform, not only a model comparison study.  
I needed requirements, design, implementation, and evaluation together.

## Q5) "Why not a strict deductive approach?"

**Answer:**  
Deductive approach is more fixed-theory-first.  
My project required adaptation during development, so I needed a method that allows going between theory and practical findings.

## Q6) "Why not only inductive approach?"

**Answer:**  
Inductive is mostly observation-first.  
In my case, I started with existing literature and theory, then refined using implementation evidence.  
That is why abductive was a better fit.

## Q7) "Why did you choose abductive specifically?"

**Answer:**  
Because I moved back and forth:

- from literature and known gaps,
- to implementation and testing outcomes,
- then back to refine decisions.

That exactly matches abductive reasoning.

## Q8) "What development process alternatives did you consider?"

**Answer:**  
I considered a strict waterfall-style execution and a coding-first ad-hoc approach.  
I chose iterative development because requirements and technical findings evolved during the project.

## Q9) "Why not full waterfall?"

**Answer:**  
Waterfall is too rigid for an AI-integrated project where findings can change during development.  
Iteration gave better risk handling and better requirement refinement.

## Q10) "Why was your chosen methodology the best fit?"

**Answer:**  
Because my project needed:

- practical solution building,
- user-centered requirement evidence,
- measurable technical validation,
- and critical reflection.

The chosen methodology covered all of these in one coherent process.

## One-line defense (memorize)

I chose a practical mixed-method, abductive approach because this project required both real user understanding and measurable technical proof, not only theory or only coding.

---

## Keyword Meanings (Simple Glossary for Viva)

Use this when you forget academic words during viva.

## Methodology keywords

- **Methodology:**  
The overall plan for how I did the research and built/evaluated the project.
- **Research philosophy:**  
The general thinking style behind my research decisions.
- **Pragmatism:**  
Focus on what works in practice to solve the real problem.
- **Research approach:**  
The logic style used to move from knowledge to conclusions.
- **Abductive approach:**  
Going back and forth between theory and real findings from implementation/testing.
- **Deductive approach:**  
Start from theory/hypothesis first, then test it.
- **Inductive approach:**  
Start from observations/data, then build theory.
- **Research strategy:**  
The set of methods used to execute the study (for example survey, experiment, action research).
- **Action research:**  
Improve a real system while actively building and evaluating it.
- **Research choice:**  
Whether I used qualitative methods, quantitative methods, or both.
- **Mixed methods:**  
Using both qualitative and quantitative evidence in one study.
- **Qualitative data:**  
Non-numeric evidence (opinions, feedback, interview insights, behavior patterns).
- **Quantitative data:**  
Numeric evidence (metrics, counts, scores, test results).
- **Cross-sectional:**  
Data collected/evaluated in a project time window (snapshot), not over many years.
- **Longitudinal:**  
Study done over a long period with repeated measurement points.
- **Triangulation:**  
Validating findings using multiple evidence sources, not only one source.
- **Validity:**  
Whether I measured the right thing correctly.
- **mmmmReliability:**  
Whether the process/results are consistent and repeatable.

## Design and architecture keywords

- **Architecture:**  
The high-level structure of the system and how parts connect.
- **Tiered architecture:**  
System split into layers (presentation, logic, data).
- **Presentation tier:**  
The frontend/user interface layer.
- **Logic tier:**  
The backend/API/business-logic layer.
- **Data tier:**  
The storage layer (database/object store).
- **Separation of concerns:**  
Keep different responsibilities in different modules/layers.
- **Modular design:**  
Build the system in independent parts so it is easier to test and maintain.
- **Maintainability:**  
How easy it is to update, fix, and extend the system later.
- **Scalability:**  
Ability to handle more users/data/workload as usage grows.
- **Reliability (system):**  
System works consistently and handles failures safely.
- **Extensibility:**  
Ability to add new features without breaking existing parts.
- **NFR (Non-Functional Requirement):**  
Quality requirement like performance, security, usability, reliability.
- **Performance:**  
How fast and efficient the system responds.
- **Usability:**  
How easy and clear the system is for users.
- **Security:**  
Protecting data and access from unauthorized use.
- **ORM (Object-Relational Mapping):**  
Tool to work with database tables using code objects/classes.
- **API contract:**  
Agreed request/response format between frontend and backend.
- **Fallback:**  
Backup behavior used when a preferred service/component fails.
- **Feature flag:**  
Configuration switch to enable/disable specific features.

## ML keywords used in these sections

- **NER (Named Entity Recognition):**  
Extracting important entities (like skills, job title, education) from text.
- **BIO tagging:**  
Label format: B = beginning, I = inside, O = outside an entity.
- **Inference:**  
Using a trained model to make predictions on new input.
- **Training:**  
Teaching the model using labeled data.
- **Evaluation metric:**  
Number used to measure model quality (precision, recall, F1, etc.).

## One-line safe explanation if you forget a term

"In simple words, this means the method/structure I used to make sure the project is practical, technically correct, and backed by proper evidence."