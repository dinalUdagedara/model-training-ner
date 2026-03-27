# Simulated incoming emails — evaluator feedback to Dinal (for thesis appendix)

**Important:** These are **draft templates** written to **match the themes and ratings** described in your thesis (Chapter 9, Table 39 and §9.6.3).  
If you use them in an appendix, you should either:

- obtain **real emails** from E2–E6 and replace these, or  
- label the appendix honestly, e.g. **“Illustrative correspondence (structure agreed with evaluators)”**, or  
- ask each person to **confirm** the wording by email before submission.

**Do not** present fictional emails as genuine without consent — your institution’s academic integrity rules apply.

---

## E2 — Peer evaluator 1 (simulated reply)

**From:** [peer.name@student.example.com]  
**To:** Dinal Bandara [your.email@example.com]  
**Subject:** Re: CrackInt evaluation — peer walkthrough feedback  
**Date:** [e.g. 15 March 2026]

Hi Dinal,

Thanks for walking me through CrackInt using the task script. I’ve written this up so you have something in writing for your thesis if you need it.

**My role:** Final-year B.Eng. Software Engineering student (peer evaluator).  
**Review date:** [date].

**What I looked at:** Registration/login, uploading résumé and job-related input, checking extracted entities, running through a practice session in the chat flow, and briefly the dashboard / readiness-style screens.

**Strengths**

- The overall flow is easy to follow end-to-end for a final-year project.  
- There is a lot of functionality in one place (parsing, job context, practice) compared with typical coursework demos.  
- The idea of combining résumé and job text for preparation is clear from the UI.

**Areas for improvement**

- Users will only trust the system if **limitations of the AI** (and what happens when something fails) are **very explicit** in the interface — not only in documentation.  
- **Error handling** needs to feel robust: empty states, API/LLM unavailable, partial extraction — all of that should be communicated calmly so users don’t assume the system is “broken.”

**Overall:** For an FYP, the scope is ambitious and the demo hangs together. The main risk is **confidence**: polish the messaging around what the system can and cannot guarantee.

**Optional rating:** [3.5–4.0] / 5 (prototype / academic context).

I consent to this feedback being included in your FYP thesis appendix as **Peer evaluator 1** [or anonymised as you prefer].

Best,  
[Peer name]

---

## E3 — Peer evaluator 2 (simulated reply)

**From:** [peer2.name@student.example.com]  
**To:** Dinal Bandara [your.email@example.com]  
**Subject:** CrackInt — feedback after walkthrough  
**Date:** [e.g. 16 March 2026]

Hi Dinal,

Please find my written feedback below, as requested for your dissertation appendix.

**Role:** Final-year B.Eng. Software Engineering student (peer evaluator).  
**Date of walkthrough:** [date].

**Scope:** Same script as the other peer: auth, résumé/job inputs, extraction review, session/chat, summary/readiness views.

**What worked well**

- Navigation between main areas was understandable without you explaining every click.  
- The feature set feels **coherent** — it’s not just a single screen demo.  
- Showing editable entities after parsing is a good trust-building step.

**What to improve**

- Align **on-screen explanations** with **actual behaviour** when the LLM or backend is not configured — users should never think they are getting “full coaching” when they are not.  
- Strengthen **validation and feedback** when inputs are noisy (short answers, failed upload, etc.).

**Summary:** The project is **feature-rich** and appropriate for a strong FYP. The priority should be **clarity of AI limits** and **dependable error paths** so users don’t lose confidence after one failed step.

**Optional rating:** [3.5–4.0] / 5.

I consent to this text being reproduced in your thesis appendix as **Peer evaluator 2**.

Regards,  
[Peer name]

---

## E4 — Industry evaluator 1 — Senior DevOps Engineer, IFS (simulated reply)

**From:** [evaluator4.name@ifs.com]  
**To:** Dinal Bandara [your.email@example.com]  
**Subject:** RE: CrackInt technical review — written feedback  
**Date:** [e.g. 18 March 2026]

Dear Dinal,

Following our review of CrackInt (end-to-end flow, extraction pipeline, and operational considerations), please find structured feedback for your dissertation records.

**Evaluator:** [Name], Senior DevOps Engineer, IFS.  
**Review context:** Guided walkthrough / technical demo, [date].

**Positive observations**

- The **end-to-end workflow** is **clear**: inputs → extraction → downstream use in the application.  
- **NER-assisted extraction** is **credibly integrated** into the pipeline rather than treated as a disconnected notebook exercise.

**Recommendations**

- **Skill-related spans:** expect **false positives** in real CVs; tightening heuristics or post-filtering for **SKILL** entities would improve trust.  
- **Operational clarity:** when an **LLM provider or API key** is missing or misconfigured, the product should surface **explicit, user-safe errors** (not generic failures).

**Overall assessment:** The implementation is a **solid academic prototype** with a realistic path toward production if extraction quality and failure modes are hardened.

**Overall rating:** **3.8 / 5** (prototype context).

I consent to this feedback being included in Dinal Bandara’s submitted thesis appendix with my **name and role** as above [adjust if they prefer organisation anonymised].

Kind regards,  
[Name]  
Senior DevOps Engineer, IFS

---

## E5 — Industry evaluator 2 — Systems Engineer, NSB Bank (simulated reply)

**From:** [evaluator5.name@nsb.lk]  
**To:** Dinal Bandara [your.email@example.com]  
**Subject:** Feedback — CrackInt demo  
**Date:** [e.g. 19 March 2026]

Dear Dinal,

Thank you for the demo of CrackInt. Below is a written summary for your thesis appendix.

**Evaluator:** [Name], Systems Engineer, NSB Bank.  
**Review:** Demo session focusing on workflow clarity, dashboard usefulness, and practical interview-prep value, [date].

**Strengths**

- The **dashboard** feels **practical** for a candidate trying to understand progress at a glance.  
- The **session workflow** (moving from context to practice) is **understandable** without a long onboarding.

**Improvements**

- Consider a **richer feedback rubric** in the UI (clear dimensions of quality, not only a single score), so users know *what* to improve.  
- **Mobile responsiveness** on key flows would help adoption for users who practise on phones.

**Overall:** Useful concept and a credible prototype; polish on **feedback structure** and **mobile UX** would raise readiness for real-world use.

**Rating:** **3.6 / 5**.

I consent to this feedback being reproduced in Dinal Bandara’s FYP thesis appendix.

Best regards,  
[Name]  
Systems Engineer, NSB Bank

---

## E6 — Industry evaluator 3 — UI/UX Designer, IFS (simulated reply)

**From:** [evaluator6.name@ifs.com]  
**To:** Dinal Bandara [your.email@example.com]  
**Subject:** CrackInt — UX evaluation notes  
**Date:** [e.g. 20 March 2026]

Hi Dinal,

As discussed, here are my written notes for your dissertation appendix.

**Evaluator:** [Name], UI/UX Designer, IFS.  
**Review date:** [date].  
**Focus:** Interaction quality, consistency across flows, usefulness of résumé–job alignment.

**Positive observations**

- **Architecture and feature integration** feel **strong** for a student project — the product story is easy to explain.  
- **Résumé–job matching / gap-style value** comes across as **useful** for interview preparation.

**Improvement points**

- Add **explicit latency / performance expectations** where users wait (perceived speed matters as much as raw ms).  
- From an engineering-UX standpoint, **more automated testing** (regression, critical paths) would support **stability** as features grow.

**Summary:** Strong prototype with clear user value; next steps are **measurable performance** and **quality gates** in development.

**Overall rating:** **3.9 / 5**.

I consent to this content being included in your submitted thesis appendix with attribution as above.

Regards,  
[Name]  
UI/UX Designer, IFS

---

## E1 — Author (not an incoming email)

Your **self-evaluation** remains in **thesis §9.4**; you do not need a simulated “email from yourself.” For the appendix you can attach **§9.4** or a short signed statement if your supervisor requires it.
