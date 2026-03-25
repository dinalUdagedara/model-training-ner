# CrackInt — FYP demo video (Unlisted YouTube) — 30:00 read-aloud script

Important: This is a template speaker script. Before recording, read it aloud once and **paraphrase in your own words** so it sounds like you and matches your exact UI/route names.

How to use:
- Read everything as speech.
- Treat **bold [SCREEN: …]** and **bold [ACTION: …]** as cues only.
- Keep a timer; if you run long, cut the last optional demo block (P7 or N5).

---

## 0:00 — Opening (0:15)

**[SCREEN: CrackInt title / login page]**

Hello, I’m [your name], student ID [your ID]. This unlisted YouTube video is my Final Year Project demonstration of **CrackInt**—an AI-driven, personalised interview preparation platform.  
I will follow the required structure: **first** the problem and research gap, **second** the solution and technical design with a code walkthrough, and **third** a system demonstration with positive and negative test cases.

---

## PART 1 — Problem & research gap (0:15–6:15 = 6:00)

### 1.1 Problem (0:15–2:00 = 1:45)

**[SCREEN: Slides or calm background while you talk]**

In today’s recruitment process, many organisations use AI screening tools to filter candidates.  
However, early-career candidates still rely on static and generic interview preparation resources—such as question banks or general chat assistants.  
That creates a mismatch: the candidate’s preparation is often not grounded in their own documents, and it is not aligned to the specific role they are targeting.

### 1.2 Research / practice gap (2:00–5:00 = 3:00)

The gap I identified from the literature and from practical tooling is that document understanding and interview coaching are often separated.  
Some tools focus only on document parsing and entity extraction, but they stop there.  
Other tools focus only on interview practice, but the conversation is generic and not driven by verified fields extracted from the candidate résumé and the job description.  
Because of that separation, two things happen.  
First, question generation and coaching are not reliably grounded in the skills employers ask for.  
Second, evaluation and readiness reporting becomes weak—there is no clear, defensible mapping from extracted competencies to what the coaching actually covers.

### 1.3 My aim (5:00–6:15 = 1:15)

So my aim with CrackInt is to bridge this gap in one integrated system:  
structured entity extraction from résumé and job text, skill-gap and matching, and then authenticated practice sessions with optional AI coaching and readiness-oriented analytics.

---

## PART 2 — Solution & technical design + code walkthrough (6:15–18:15 = 12:00)

### 2.1 Solution summary (6:15–8:00 = 1:45)

**[SCREEN: architecture diagram or split browser/IDE]**

CrackInt is a full-stack web application.  
The front end is built with **Next.js** and calls a **FastAPI** back end.  
Authentication is handled with **JWT**, and the system persists data in **PostgreSQL**.  
On the ML side, the core entity extraction uses **Word2Vec plus BiLSTM plus CRF** to produce BIO-tagged entities for résumé and job-poster text.  
Optional agent features are enabled only when configuration and provider keys are available.

### 2.2 Design / ML pipeline (8:00–10:30 = 2:30)

**[SCREEN: NER pipeline / resume-job extraction slide, or show notebook output]**

For résumé understanding, the pipeline extracts structured fields such as name, email, skills, education, occupation, and experience.  
For job understanding, it extracts job-side entities such as job title, company, location, and the required skills and qualifications.  
The system then aligns the extracted entities into a role-specific skill gap view.  
Finally, during practice sessions, the coaching workflow can use the structured view so the practice is grounded in what the role requires.

### 2.3 Code walkthrough — Hybrid résumé extraction (10:30–13:30 = 3:00)

**[SCREEN: IDE — open your backend file that contains parse_resume_hybrid (search if needed)]**

Now I’ll show a short code walkthrough.  
This hybrid extraction function is the key integration idea.  
It combines heuristic rules for high-confidence contact fields—like name and email—with the neural NER model output for contextual entities—like skills and experience.  
Then it merges and normalises results so the API returns a consistent schema.

**[ACTION: show the function definition and the section where rules + model outputs are merged]**

The reason this is important is robustness: rules increase precision for structured fields, while the BiLSTM–CRF captures span-level context for the rest.

### 2.4 Code walkthrough — JWT protected access (13:30–14:45 = 1:15)

**[SCREEN: IDE — open the JWT dependency, e.g. get_current_user, or search for “Authorization” header parsing]**

Next, security.  
This function reads the `Authorization` header, verifies the Bearer token, decodes the JWT, and loads the user.  
If the token is missing or invalid, the API returns **401 Unauthorized**.  
That ensures all user-specific actions—like sessions and saved entities—are protected.

**[ACTION: scroll to the 401 error branch / token validation block]**

### 2.5 Code walkthrough — Notebook model class / inference (14:45–18:15 = 3:30)

**[SCREEN: Jupyter / Notebook — open `fyp/BiLSTM_CRF_Resume_NER_Path2_FYP.ipynb` and go to “## 5. Model”]**

Finally, I’ll show the model structure briefly.  
In this notebook you can see the BiLSTM–CRF design: embeddings feed into a bidirectional LSTM, emissions are produced using a linear layer, and the CRF layer performs structured decoding.  
This is how the model predicts BIO tags for each token, producing entity spans after decoding.

**[ACTION: show the `class BiLSTMCRF` and then quickly show `forward()` or decoding section]**

This connects to the thesis evaluation results, where the frozen run achieves micro-F1 performance for résumé and job-poster extraction.

---

## PART 3 — System demonstration (18:15–29:00 = 10:45)

### Setup (18:15–18:30 = 0:15)

**[SCREEN: browser — logged out + then logged in]**

Before the demo starts, I ensure a test user exists and I have sample résumé content and a sample job description ready.

### Positive cases (18:30–25:00 = 6:30)

#### P1 — Register → Login (18:30–19:30 = 1:00)

**[ACTION: Register with email and password]**

I register and confirm the account is created.  
Then I log in.

**[ACTION: Login]**

Now I can access protected features.

#### P2 — Résumé extraction (19:30–21:30 = 2:00)

**[ACTION: Go to résumé upload / extract]**

I upload a résumé PDF or paste résumé text and trigger extraction.

**[ACTION: wait for response and highlight JSON fields or UI entity cards]**

The system returns structured entities—such as name, email, skills, education, and experience—showing the hybrid résumé NER pipeline is working.

#### P3 — Edit / save entities (if your UI supports it) (21:30–22:30 = 1:00)

**[ACTION: Edit one extracted entity and click save]**

After saving, I refresh the page to confirm persistence.

#### P4 — Job extraction / job posting creation (22:30–23:45 = 1:15)

**[ACTION: Extract job text or create a job posting]**

Here, I provide the target job description.  
The system extracts job-side entities required for alignment.

#### P5 — Skill-gap / match (23:45–25:00 = 1:15)

**[ACTION: Run skill-gap / match using the saved résumé and job posting]**

The output shows a structured skill-gap view, which becomes the basis for the practice session focus.

### Negative / edge cases (25:00–29:00 = 4:00)

#### N1 — Protected API without token (25:00–25:45 = 0:45)

**[ACTION: Open Swagger or try accessing a protected endpoint without Authorization]**

I attempt to access a protected route without a valid Bearer token.

Expected behaviour: the API denies access with **401**.

#### N2 — Invalid login (25:45–26:30 = 0:45)

**[ACTION: Login with wrong password]**

Now I test an invalid login attempt.

The system should show a clear error and must not crash.

#### N3 — LLM unavailable behaviour (26:30–27:45 = 1:15)

**[ACTION: Trigger a session step that requires LLM / evaluation with OPENAI disabled or key missing]**

For the next negative test, I demonstrate documented partial behaviour when LLM features are unavailable.  
Depending on configuration, the system should return a **503** or a message that the feature is unavailable, rather than failing silently.

#### N4 — Minimal / weak job input (27:45–29:00 = 1:15)

**[ACTION: Provide minimal job text and run job extract or match again]**

Finally, I provide minimal job input.  
The system should respond in a stable way—entities may be sparse, but the app should remain functional.

---

## Closing (29:00–30:00 = 1:00)

**[SCREEN: final dashboard state]**

This demo confirms that CrackInt provides document-grounded entity extraction, skill-gap matching, and authenticated practice sessions.  
Quantitative NER evaluation and functional testing are documented in the thesis, and the negative tests demonstrate robust behaviour under missing authentication or unavailable optional AI features.

Thank you.

