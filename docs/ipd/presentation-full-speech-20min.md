# IPD Presentation — Full 20-Minute Speech (Word-for-Word)

**Use this as your exact speaking script** for the IPD presentation video.  
Estimated total: **~20 minutes**. Adjust pace slightly if needed.

---

## Slide 1 — Title (≈ 1:00)

"Good morning/afternoon. My name is **Udagedara Thiyunu Dinal Bandara**, W1998730, and this is my Interim Progression Demonstration presentation for my final year project, **CrackInt: an AI-driven personalized interview preparation platform**.

The goal of CrackInt is to help candidates prepare for interviews in a way that is **personalized to their résumé and the job they are applying for**, and to provide feedback that goes beyond surface-level delivery metrics, focusing on the actual content quality of answers.

In today’s IPD, I’ll explain the motivation, the research gap, my stakeholders and requirements, the system design and architecture, and then I’ll clearly show what has already been implemented in the working prototype versus what is planned for the next phase."

---

## Slide 2 — Agenda (≈ 0:45)

"Here’s the agenda for the presentation.

First, I’ll cover the **problem background** and why existing interview preparation tools are not sufficient.  
Then I’ll describe the **research problem and the research gap**.  
Next, I’ll identify the **key stakeholders**.  
After that, I’ll go through the **formal requirements**, clearly indicating what is implemented and what is pending.  
Then I’ll present the **system design** and the **overall architecture**, including the current prototype architecture.  
I’ll show my **updated time schedule**, and finally the **progress since the PPRS**, and conclude with next steps and references."

---

## Slide 3 — Problem background (≈ 2:15)

"To explain the problem background, we can start with what is happening in recruitment today.

On the employer side, AI is widely used for screening and shortlisting. But on the candidate side, many preparation tools are still relatively static. They often use generic question banks, provide shallow feedback, or split the workflow across multiple tools.

I highlight four key gaps.

**First: résumé–job awareness.**  
Most tools do not truly combine a candidate’s résumé with the target job posting to guide practice. Candidates end up practicing generic questions that may not match their actual experience or the role’s expectations.

**Second: semantic-level feedback.**  
A lot of platforms focus on delivery: for example tone, pace, filler words, or grammar. Those are useful, but they miss the deeper question: *Was the answer relevant? Was the reasoning strong? Did the candidate provide evidence and structure?* In real interviews, content is what matters most.

**Third: integrated progress tracking.**  
Candidates usually practice multiple times, but many tools do not provide a strong unified view of improvement over time—what topics keep failing, what question types are weak, and how performance changes session by session.

**Fourth: user experience constraints.**  
Some systems are not optimized for real-time, low-latency interaction, or they are not mobile-friendly, and that reduces the practicality of using them consistently.

So overall, the problem is that candidates need a more holistic and intelligent platform: one that understands both their background and the role, generates relevant practice, and provides feedback on content quality, while also tracking progress."

---

## Slide 4 — Research problem & research gap (≈ 3:15)

"Based on that background, my research problem can be summarized like this:

Current interview preparation platforms fail to provide **personalized, content-aware coaching** that uses both the candidate résumé and the job description. They rely on static or semi-static question sets and provide feedback that is often superficial.

Now, the research gap has a few important parts.

**Gap one: résumé + job combined personalization.**  
Tools may parse a résumé or may provide role-based questions, but they do not properly connect both inputs to generate truly personalized questions and coaching.

**Gap two: semantic feedback quality.**  
Delivery metrics alone are not enough. The gap is the lack of systematic evaluation of answer quality—things like relevance, completeness, reasoning, structure, and evidence aligned to the job requirements.

**Gap three: adaptive learning and history.**  
Candidates improve by iteration. There’s a research and product gap in adapting difficulty, question focus, and feedback based on prior performance and session history.

**Gap four: integration.**  
Many systems are fragmented: one tool for résumé scoring, another for question banks, another for speech analysis. The candidate experience is not unified.

CrackInt addresses this gap by combining several components into one pipeline:

- **NER-based parsing** for résumé and job descriptions, so the system has structured facts.
- **LLM-based question generation** using those structured facts, to produce relevant practice.
- A **semantic feedback engine** to evaluate the quality and relevance of answers.
- And **persistent analytics**, so progress can be tracked over time.

For the IPD stage, my focus is to deliver the foundation that everything depends on: **accurate résumé and job extraction**, integrated end-to-end in a working web prototype."

---

## Slide 5 — Stakeholders (≈ 2:30)

"Now I’ll cover the project stakeholders. I used an onion model to group them into four layers.

**At the core**, the primary stakeholders are job seekers—students and early-career professionals. Their interest is direct: they want personalized questions, actionable feedback, progress tracking, and a platform that is easy to use and affordable.

**In the operational layer**, there are stakeholders like career services and support teams—people who care about the platform being reliable, understandable, and maintainable. Also the development and maintenance perspective is here: it must be modular enough to evolve.

**In the strategic layer**, I include academic institutions, potential corporate partners, and the research community. They care about measurable improvement outcomes, employability, and whether the approach is valid and can be evaluated rigorously.

**In the external layer**, there are compliance and ethics stakeholders such as GDPR and privacy concerns, and also competitors and third-party technology providers. Their interests include privacy, transparency, responsible AI use, and ethical data handling.

This stakeholder analysis matters because it affects the requirements—especially privacy, security, explainability, and evaluation methodology."

---

## Slide 6 — Formal requirements specification (≈ 3:30)

"This slide summarizes the formal requirements, and importantly, I classify them as **implemented**, **partial**, or **pending**.

For the IPD prototype, the key implemented requirements are centered around the extraction pipeline.

**Implemented:**  
- **FR03**: résumé upload—supporting both PDF upload and pasted text input.  
- **FR04**: résumé information extraction using a trained NER model, combined with some rules for reliability.  
- **FR05**: users can review and edit extracted entities.  
- A modular backend architecture with OpenAPI documentation—supporting maintainability.

**Partial:**  
- Job description analysis exists at the API level—so the backend can extract job entities—but the frontend integration depends on the exact IPD scope.  
- Resume persistence is implemented, meaning extracted resume data is stored, but full session history and interview tracking are not yet complete.  
- Some operational NFRs like logging and performance considerations exist, but are not yet fully validated as a finished product.

**Pending:**  
- User registration and authentication.  
- Question generation using LLMs.  
- The interactive practice interface—chat or voice.  
- The semantic feedback engine.  
- Analytics dashboards, export functions, and advanced user profile features.  
- And the full set of security, scalability, and privacy enhancements planned for the final submission.

So the key point is: the IPD focuses on delivering a stable working prototype for the **core extraction pipeline**, because that is foundational for personalized question generation and feedback later."

---

## Slide 7 — System design (≈ 2:30)

"Next is system design.

My design goals are to build an integrated platform that is candidate-centric and modular: it should support résumé parsing, job parsing, question generation, semantic feedback, and analytics in a way that each module can be improved independently.

I follow an Object-Oriented Analysis and Design approach, with clear components such as:

- Resume Parser  
- Job Description Parser  
- Question Generator  
- Feedback Engine  
- Analytics and History

The development approach is Agile, organized into sprints, to deliver value incrementally while keeping the system stable.

In terms of technology stack, I am using:
- **Next.js** for the frontend,  
- **FastAPI** for the backend,  
- **PostgreSQL** for persistence,  
- and ML components including **BERT-BiLSTM-CRF** for NER.  
LLM and semantic feedback components are planned next.

And for the research methodology, I align with a pragmatic approach and a design-science mindset: I build the artifact, evaluate it through experiments and user feedback, and iteratively improve it."

---

## Slide 8 — Overall system architecture (≈ 2:45)

"Now to architecture. I present both the target high-level architecture and the current IPD prototype architecture.

At the high level, the intended flow is:
User interacts through the browser,
Frontend communicates with the backend APIs,
Backend runs extraction and AI modules,
Data is stored in databases and object storage,
And analytics and personalization use session history.

For the IPD prototype, the architecture focuses on the extraction path.

**Résumé extraction flow:**  
- The user uploads a résumé PDF or pastes text in the frontend.  
- The frontend sends it to the backend endpoint.  
- The backend extracts text from PDF when required.  
- Then it runs the **resume NER model** to extract entities like name, email, skills, education, and experience.  
- The results are returned to the frontend and also persisted in PostgreSQL.  
- The user can edit entities and update the stored data via a PATCH endpoint.

**Job extraction flow:**  
- The user provides a job description as PDF or pasted text.  
- The backend extracts the job entities using the **job poster NER model**.  
- For the IPD scope, the result is returned on demand and not necessarily persisted.

These two extraction modules are important because once we have structured résumé and job information, we can build the next features: generating interview questions based on gaps and alignment, and providing feedback based on role expectations."

---

## Slide 9 — Updated time schedule (≈ 1:45)

"This slide shows the updated time schedule and what has changed since the original PPRS plan.

So far, the early phases—proposal, literature review, SRS/PPRS, proof of concept, and design—have followed the expected timeline.

For the prototype milestone around early February, the scope is intentionally focused. I prioritized **training and integrating the NER models**, and ensuring end-to-end functionality across frontend, backend, and database.

The reason for this scope focus is risk management: building a stable extraction pipeline first reduces downstream risk, because question generation and feedback quality depend heavily on correct extracted information.

The next phase from March onwards will focus on authentication, LLM-based question generation, semantic feedback, analytics, and final evaluation and write-up."

---

## Slide 10 — Progress since PPRS (≈ 2:15)

"Now I’ll summarize progress since the PPRS.

A major achievement is **dataset preparation and training pipelines**. Instead of relying on a single dataset, I combined multiple datasets and mapped them into a unified schema for consistent training. This gives more data, more diversity, and better generalization.

Then, I trained two NER models:
- A **Resume NER** model using BERT-BiLSTM-CRF, integrated into the backend and exposed through an API.  
- A **Job Poster NER** model, also integrated via an API endpoint.

On the software side:
- The backend is implemented using FastAPI with clear routes for resume extraction and job extraction.  
- PostgreSQL persistence is implemented for resumes and extracted entities.  
- The frontend has a CV upload interface that supports both file drop and pasted text, displays extracted entities, and allows edits via a PATCH request.

So at the IPD stage, the core extraction prototype is functional end-to-end. The next steps are to expand toward question generation, semantic feedback, and session history tracking."

---

## Slide 11 — Conclusion (≈ 1:30)

"To conclude:

CrackInt aims to provide an integrated, AI-driven interview preparation experience that is personalized using both résumé and job description understanding.

For the IPD prototype, I have delivered the foundation:
- working résumé and job extraction,  
- trained NER models integrated into a full-stack application,  
- and a clear mapping of requirements showing what is implemented versus pending.

The immediate next steps are to finalize the remaining UI and hosting tasks needed for demonstration, and then proceed with LLM-based question generation, semantic feedback, and analytics for the final project submission.

Thank you."

---

## Slide 12 — References (≈ 0:30)

"These are the references used in the presentation and the project research, listed in alphabetical order. Thank you."

---

## Pacing tips (optional)

- If you’re **short on time**: expand Slide 6 and Slide 8 by giving 1–2 concrete examples (e.g., “skills extracted: Python, SQL…”; “job skills required: React, Docker…”).
- If you’re **over time**: shorten Slide 5 (stakeholders) and Slide 9 (schedule) by ~30 seconds each.

