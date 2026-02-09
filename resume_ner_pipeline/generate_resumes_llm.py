#!/usr/bin/env python3
"""
Generate synthetic resumes using an LLM and output them in the same format as
merged_resume_ner.json: one JSON object per line with "content" and "annotation"
(character-offset spans for NAME, EMAIL, SKILL, OCCUPATION, EDUCATION, EXPERIENCE).

Requires: pip install openai
Set OPENAI_API_KEY in the environment (or pass --api-key).

Usage:
  # Generate 5 resumes
  python generate_resumes_llm.py --count 5 --output llm_generated_resumes.jsonl

  # Generate 1000 in batches of 100 (flush after each batch; re-run same command to resume if it fails)
  python generate_resumes_llm.py --target 1000 --output llm_generated_resumes.jsonl --batch-size 100

  # Generate 1000 with 5 resumes per API call (fewer round-trips, faster)
  python generate_resumes_llm.py --target 1000 --output llm_generated_resumes.jsonl --batch-size 100 --per-call 5

  # Optional: pause 2 seconds after each batch to reduce rate limits
  python generate_resumes_llm.py --target 1000 --output llm_generated_resumes.jsonl --batch-size 100 --delay-batch 2

  # Merge with existing merged_resume_ner.json
  cat merged_resume_ner.json llm_generated_resumes.jsonl > merged_resume_ner_with_llm.json
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
import time

# Same entity types as the notebook LABEL_MAPPING
VALID_LABELS = frozenset({"NAME", "EMAIL", "SKILL", "OCCUPATION", "EDUCATION", "EXPERIENCE"})

# Resume format: section structure can vary; entity rules are strict. Support both students and employed.
SYSTEM_PROMPT = """You are a resume generator. You output valid JSON only, no markdown or extra text.

Resumes can be from students (no work experience) or employed people. The text format may vary: section order, header names (e.g. "Work Experience", "Employment", "EXPERIENCE"), or layout may differ. Always apply the entity rules by meaning, not by section title.

Generate a resume that typically follows this structure (ALL CAPS or similar section headers; order can vary):

1. Full name (one line, can be ALL CAPS)
2. Field or degree line (e.g. "Software Engineering" or "Computer Science")
3. Email | optional: LinkedIn/Github URLs | Phone (use a plausible format for the candidate's region)
4. SUMMARY (or similar)
5. EDUCATION – Institution, date. Degree (e.g. BSc Computer Science, BSc Business, BEng, MSc). Use real or plausible institutions for the chosen region.
6. EXPERIENCE (or Work Experience, Employment) – only if the person is employed: Role – Company Name, City, dates. Use plausible companies (tech or other sector as appropriate).
7. PROJECTS (optional) – Project Name – Organization | Status. Bullet points. Include "Tech Stack: ..." where relevant.
8. CERTIFICATIONS (optional) – bullet list
9. SKILLS – bullets for languages, tools, soft skills
10. REFERENCES (optional) – do not tag anything in this section

Most resumes should be IT/tech related; others can be from other sectors. Vary both region and career.
- Region: Rotate between Sri Lanka (e.g. University of Colombo, Virtusa, Colombo), India, US, UK, and other countries—with matching names, institutions, cities, and companies.
- Career type: Prefer IT/tech roles (e.g. Software Engineer, Full Stack Developer, Data Scientist, DevOps Engineer, Cloud Engineer, QA Engineer, Security Engineer, IT Support, Mobile Developer, ML Engineer, tech student). Some resumes can be other professions (e.g. Healthcare Administrator, Financial Analyst, Project Manager, Marketing Manager, Teacher, HR). Match skills and education to the chosen career.
Keep the resume concise but complete.

Output a single JSON object with exactly two keys:
- "content": the full resume text as a single string (use \\n for newlines).
- "entities": an array of objects, each with "type" (NAME, EMAIL, SKILL, OCCUPATION, EDUCATION, or EXPERIENCE) and "text" (the exact substring as it appears in content). List entities in the order they first appear. Use the exact spelling and spacing as in content.

REQUIRED when present in the text:
- NAME and EMAIL: always exactly one each (candidate only).
- If the resume contains any work experience (job titles and companies): you MUST tag every job title as OCCUPATION and every company/employer as EXPERIENCE. Omitting OCCUPATION when job titles appear in the text is invalid.
- If the resume has education: tag at least one degree or institution as EDUCATION.
- If the resume has skills: tag each as SKILL.
Students (no work history) will have no OCCUPATION and no EXPERIENCE—that is valid.

CRITICAL – DO NOT TAG ANYTHING IN REFERENCES:
Do not add any entity whose text appears only inside the REFERENCES section. That includes: reference person names, reference job titles (e.g. "Senior Software Engineer"), reference organizations, reference emails, reference phone numbers. Only tag the candidate's own NAME (first line), EMAIL (contact line), and entities that appear in SUMMARY, EDUCATION, EXPERIENCE, PROJECTS, CERTIFICATIONS, or SKILLS.

ENTITY RULES (follow exactly):

• NAME: Tag only the candidate's full name (the very first line of the resume). One entity. Never tag anyone mentioned in REFERENCES.

• EMAIL: Tag only the candidate's email address—the one in the contact line near the top (line 3). One entity. Never tag emails that appear only in REFERENCES.

• OCCUPATION: Whenever the resume text contains a job title or role (e.g. in an experience section, or in SUMMARY like "Software Engineer with 5 years"), you MUST tag every such job title as OCCUPATION. Examples: "Software Engineer", "Data Scientist", "DevOps Engineer", "Backend Developer", "QA Engineer", "Junior Developer". Tag each distinct job title that describes the candidate's role. For lines like "Role – Company, City" you must tag both the Role (OCCUPATION) and the Company (EXPERIENCE)—never skip the job title. Do NOT tag: the field line (e.g. "Computer Science", "Software Engineering"); project or certification names; "Personal Project"; or any title that appears only in REFERENCES.

• EDUCATION: For every entry under the EDUCATION section you must tag both (1) the degree or qualification name (e.g. "Bachelor of Science in Computer Science", "BSc", "MSc", "Advanced Level") and (2) the institution name (e.g. "University of California, Berkeley", "University of Colombo", "D.S. Senanayake National College"). Never skip the institution—every degree line has an institution. If there are multiple degrees or schools, tag every degree and every institution. Do not tag dates, cities, or "Present" unless they are part of the institution name.

• EXPERIENCE: Tag every company or employer name (e.g. "Tech Innovations Inc.", "Virtusa", "Infosys"). Do NOT tag job titles (those are OCCUPATION), date ranges, or locations. Only for employed resumes.

• SKILL: Tag every distinct technology, tool, and soft skill. Include: (1) every item under the SKILLS section—each programming language, each web technology, each database, each tool, each soft skill phrase (e.g. "Problem-solving", "Communication", "Teamwork"); (2) every technology mentioned in any "Tech Stack: X, Y, Z" line under PROJECTS—tag each tech in the Tech Stack even if it does not appear under SKILLS (e.g. "Spring Boot", "Django"). Tag each as a separate entity. Do not tag section labels like "Programming Languages:" or "Tech Stack:".

COMPLETENESS CHECKLIST (before returning, verify):
- Exactly one NAME and one EMAIL.
- If the text contains job titles (in experience section or summary), every one is tagged as OCCUPATION.
- If the text contains companies/employers, every one is tagged as EXPERIENCE.
- Every degree and institution in EDUCATION is tagged as EDUCATION.
- Every skill and Tech Stack tech is tagged as SKILL.
- No entity is from the REFERENCES section."""

# Most resumes will be IT; a minority will be other sectors. Weights: ~75% IT, ~25% other.
CAREER_HINTS_IT = [
    "Software Engineer or Full Stack Developer",
    "Backend Developer (e.g. Java, Python, Node.js)",
    "Frontend Developer (e.g. React, Angular, Vue)",
    "Data Scientist or Data Analyst",
    "Data Engineer or ETL Developer",
    "DevOps Engineer or SRE",
    "Cloud Engineer (AWS, Azure, or GCP)",
    "QA Engineer or Test Automation Engineer",
    "Security Engineer or Cybersecurity Analyst",
    "Mobile Developer (iOS/Android or React Native)",
    "Machine Learning Engineer",
    "Systems Administrator or IT Support",
    "Tech / CS student (no work experience, seeking first role)",
]
CAREER_HINTS_OTHER = [
    "Healthcare Administrator or Nurse",
    "Financial Analyst or Accountant",
    "Project Manager or Operations Manager",
    "Marketing Manager or Digital Marketing Specialist",
    "Teacher or Lecturer",
    "HR Manager or Recruiter",
    "Student (no work experience, seeking first role)",
]
IT_WEIGHT = 0.75  # probability of picking an IT career
REGION_HINTS = ["Sri Lanka", "India", "USA", "UK", "Australia", "Canada", "Singapore"]

USER_PROMPT_TEMPLATE = """Generate one realistic resume (section order and header names can vary). For this resume use career: {career}. Use region: {region} (names, institutions, companies, and contact format should match this region). Use the appropriate field line and matching job titles (if employed), skills, and companies.

Before returning JSON you MUST: (1) If the resume has work experience, tag every job title (e.g. "Software Engineer", "Data Analyst") as OCCUPATION and every company as EXPERIENCE—never omit OCCUPATION when job titles appear in the text. (2) Tag at least one degree or institution under EDUCATION if present. (3) Tag every skill and Tech Stack tech as SKILL. (4) Do not tag anything in REFERENCES. Return JSON with "content" and "entities" (exact substrings, in document order)."""

# For batched mode: ask for N resumes in one response (fewer API calls).
BATCH_USER_PROMPT_TEMPLATE = """Generate exactly {n} different resumes. Return a single JSON array of {n} objects—no other text. Each object must have "content" (full resume text as a single string with \\n for newlines) and "entities" (array of {{"type": "NAME"|"EMAIL"|"SKILL"|"OCCUPATION"|"EDUCATION"|"EXPERIENCE", "text": "exact substring"}} in document order).

Requirements for each resume: (1) Vary career (mostly IT: Software Engineer, Data Scientist, DevOps, etc.; some non-IT: Healthcare, Finance, Marketing) and region (Sri Lanka, India, US, UK, etc.). (2) Tag every job title as OCCUPATION and every company as EXPERIENCE when present. (3) Tag at least one degree or institution as EDUCATION. (4) Tag every skill as SKILL. (5) Do not tag anything in REFERENCES.

Output only the JSON array, e.g. [{{"content": "...", "entities": [...]}}, {{"content": "...", "entities": [...]}}, ...]"""


def _extract_json_from_response(raw: str) -> dict:
    """Parse JSON from LLM response, optionally inside a markdown code block."""
    raw = raw.strip()
    # Remove optional markdown code block
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```\s*$", "", raw)
    return json.loads(raw)


def _find_spans_in_order(content: str, entities: list[dict]) -> list[dict]:
    """
    Build annotation list with character offsets.
    entities: list of {"type": "NAME"|..., "text": "exact span"}
    We find each "text" in content in order (so duplicate text gets first occurrence then next, etc.).
    """
    annotations = []
    search_start = 0
    for ent in entities:
        label = (ent.get("type") or "").strip().upper()
        if label not in VALID_LABELS:
            continue
        text = (ent.get("text") or "").strip()
        if not text:
            continue
        # Find next occurrence of this exact text from search_start
        idx = content.find(text, search_start)
        if idx == -1:
            # Try without extra whitespace / normalise spaces
            norm = " ".join(text.split())
            idx = content.find(norm, search_start)
        if idx == -1:
            continue
        end = idx + len(text)
        annotations.append({
            "label": [label],
            "points": [{"start": idx, "end": end, "text": content[idx:end]}],
        })
        search_start = end
    return annotations


def _content_from_entities_only(entities: list[dict]) -> str:
    """Build minimal content by joining entity texts (fallback if LLM omits full content)."""
    parts = []
    for e in entities:
        t = (e.get("text") or "").strip()
        if t:
            parts.append(t)
    return " ".join(parts)


def _item_from_content_entities(content: str, entities: list) -> dict | None:
    """Convert content + entities to one output item (content, annotation, extras) or None if invalid."""
    if not content and entities:
        content = _content_from_entities_only(entities)
    if not content:
        return None
    annotations = _find_spans_in_order(content, entities)
    if not annotations:
        return None
    return {"content": content, "annotation": annotations, "extras": None}


def generate_batch(client, n: int, model: str = "gpt-4o-mini", timeout: int = 120) -> list[dict]:
    """Call LLM once asking for n resumes; return list of valid items (may be fewer than n)."""
    if n <= 0:
        return []
    user_prompt = BATCH_USER_PROMPT_TEMPLATE.format(n=n)
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.8,
            timeout=max(timeout, 60 + n * 15),
        )
        raw = (response.choices[0].message.content or "").strip()
        if not raw:
            return []
        data = _extract_json_from_response(raw)
        if not isinstance(data, list):
            return []
        out = []
        for obj in data:
            if not isinstance(obj, dict):
                continue
            content = (obj.get("content") or "").strip()
            entities = obj.get("entities") or []
            if not isinstance(entities, list):
                entities = []
            item = _item_from_content_entities(content, entities)
            if item:
                out.append(item)
        return out
    except Exception as e:
        print(f"LLM batch call failed: {e}", file=sys.stderr)
        return []


def generate_one(client, model: str = "gpt-4o-mini", timeout: int = 60, career_hint: str | None = None, region_hint: str | None = None) -> dict | None:
    """Call LLM once and return one item in merged_resume_ner format or None on failure."""
    if career_hint is None:
        career = random.choice(CAREER_HINTS_IT) if random.random() < IT_WEIGHT else random.choice(CAREER_HINTS_OTHER)
    else:
        career = career_hint
    region = region_hint or random.choice(REGION_HINTS)
    user_prompt = USER_PROMPT_TEMPLATE.format(career=career, region=region)
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.8,
            timeout=timeout,
        )
        raw = (response.choices[0].message.content or "").strip()
        if not raw:
            return None
        data = _extract_json_from_response(raw)
        content = (data.get("content") or "").strip()
        entities = data.get("entities") or []
        if not isinstance(entities, list):
            entities = []
        return _item_from_content_entities(content, entities)
    except Exception as e:
        print(f"LLM call failed: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(description="Generate resume JSONL via LLM (same format as merged_resume_ner.json)")
    parser.add_argument("--count", type=int, default=5, help="Number of resumes to generate this run")
    parser.add_argument("--target", type=int, default=None, help="Target total lines: if output file exists, generate only (target - current count) and append")
    parser.add_argument("--output", type=str, default="llm_generated_resumes.jsonl", help="Output JSONL file path")
    parser.add_argument("--append", action="store_true", help="Append to output file instead of overwriting")
    parser.add_argument("--batch-size", type=int, default=100, help="Flush and report progress after every N resumes (so you don't lose progress if run fails)")
    parser.add_argument("--per-call", type=int, default=1, help="Resumes to request per API call (e.g. 5 = fewer calls, faster; 1 = one resume per call)")
    parser.add_argument("--delay-batch", type=float, default=0, help="Seconds to sleep after each batch (e.g. 2 to reduce rate limits)")
    parser.add_argument("--api-key", type=str, default=None, help="OpenAI API key (or set OPENAI_API_KEY)")
    parser.add_argument("--model", type=str, default="gpt-4o-mini", help="OpenAI model name")
    parser.add_argument("--timeout", type=int, default=60, help="Timeout per request in seconds")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Set OPENAI_API_KEY or pass --api-key", file=sys.stderr)
        sys.exit(1)

    try:
        import openai
    except ImportError:
        print("pip install openai", file=sys.stderr)
        sys.exit(1)

    # Resolve how many to generate and whether to append
    existing = 0
    if args.target is not None:
        want = args.target
        if os.path.exists(args.output):
            with open(args.output, "r", encoding="utf-8") as f:
                existing = sum(1 for line in f if line.strip())
        to_generate = max(0, want - existing)
        mode = "a" if existing > 0 else "w"
        if existing:
            print(f"Output has {existing} lines; generating {to_generate} more to reach target {want}", file=sys.stderr)
    else:
        to_generate = args.count
        if args.append and os.path.exists(args.output):
            with open(args.output, "r", encoding="utf-8") as f:
                existing = sum(1 for line in f if line.strip())
            mode = "a"
            print(f"Appending; existing lines: {existing}", file=sys.stderr)
        else:
            mode = "w"

    if to_generate <= 0 and args.target is not None:
        print("Already at or above target. Nothing to generate.", file=sys.stderr)
        return

    batch_size = max(1, args.batch_size)
    per_call = max(1, min(args.per_call, 10))
    target_total = (existing + to_generate) if args.target else (existing + to_generate)
    if args.target:
        target_total = args.target
    print(f"Batches of {batch_size} (progress saved after each batch). Target total: {target_total}. Resumes per API call: {per_call}", file=sys.stderr)

    client = openai.OpenAI(api_key=api_key)
    written = 0
    remaining = to_generate
    with open(args.output, mode, encoding="utf-8") as f:
        while remaining > 0:
            want_this_call = min(per_call, remaining)
            items = []
            if want_this_call == 1:
                for attempt in range(3):
                    item = generate_one(client, model=args.model, timeout=args.timeout, career_hint=None, region_hint=None)
                    if item:
                        items = [item]
                        break
                    if attempt < 2:
                        time.sleep(2 ** attempt)
            else:
                for attempt in range(3):
                    items = generate_batch(client, want_this_call, model=args.model, timeout=args.timeout)
                    if items:
                        break
                    if attempt < 2:
                        time.sleep(2 ** attempt)
            if not items:
                remaining -= want_this_call
                continue
            for item in items:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
                written += 1
                remaining -= 1
                total = existing + written
                if args.target:
                    print(f"  Generated {written}/{to_generate} (total {total}/{args.target})", file=sys.stderr)
                else:
                    print(f"  Generated {written}/{to_generate}", file=sys.stderr)
            if (existing + written) % batch_size == 0:
                f.flush()
                print(f"Progress saved. Total in file: {existing + written}.", file=sys.stderr)
            if args.delay_batch and args.delay_batch > 0 and remaining > 0:
                time.sleep(args.delay_batch)
        f.flush()
    print(f"Done. Wrote {written} resumes to {args.output} (total in file: {existing + written})", file=sys.stderr)


if __name__ == "__main__":
    main()
