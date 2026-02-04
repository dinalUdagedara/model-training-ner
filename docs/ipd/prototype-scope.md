# IPD: Minimum Viable Prototype Scope

**Purpose:** Plan Phase 1, Step 2 — define the smallest integrated flow to demo for the 45% prototype mark. Prototype must be **working**, **hosted**, and **shared** (Google Drive + runnable link).

---

## Chosen scope: Option A+ (resume + job extraction, no LLM yet)

- **Resume flow (already implemented):** User uploads PDF or pastes resume text → backend extracts text (PDF) and runs resume NER → entities displayed → user can edit and persist. Stored in DB.
- **Job flow (backend done; frontend to add):** User pastes job description (or uploads PDF) → backend runs job poster NER (or resume NER fallback) → entities displayed. No persistence required for IPD; optional "copy to use for questions later" note.
- **Out of scope for IPD demo:** Auth, question generation (LLM), chat Q&A, semantic feedback, analytics dashboard, S3, GDPR flows. These remain **pending** in the requirements table and can be planned for April.

This matches **Option A** in the plan (minimal: resume + job NER, display entities) with job extraction visible in the UI so both "resume-aware" and "job-aware" extraction are demonstrable.

---

## Deliverables for prototype (45%)

1. **Runnable app**
   - **Frontend:** Next.js app with (1) CV Upload page (existing), (2) Job description page (new): paste/upload job → call `POST /api/v1/jobs/extract` → show entities.
   - **Backend:** Already provides resume + job extract; ensure env (e.g. `RESUME_NER_LOAD_DIR`, optional `JOB_POSTER_NER_LOAD_DIR`) documented for local and deploy.
2. **Hosting**
   - Deploy frontend (e.g. Vercel) and backend (e.g. Railway, Render, Fly.io) so supervisor can open a URL and use both flows. If deploy is not possible by deadline, provide clear "Run locally" steps and a short Loom/screen recording of the runnable app.
3. **Google Drive**
   - Shared folder containing: PROJECT source (crackint-frontend, crackint-backend); optional model-traning-1:30 link or key files; README with how to run locally and (if applicable) link to hosted demo.
4. **Dataset**
   - If dataset is **collected by you** (not public), include it in the same shared folder. If public, document source and no need to upload.

---

## Implemented vs pending (for slides)

- **Implemented:** FR03 (resume upload), FR04 (resume NER), FR05 (review/edit), NFR13 (modular + OpenAPI). After job UI: **Partial** for FR06–FR07 (job input + analysis).
- **Pending:** FR01–FR02, FR08–FR25 (except partials above), and security/privacy NFRs.

No need to implement LLM question generation or semantic feedback for IPD; the plan allows Option A (resume + optional job NER) as the minimal viable prototype.
