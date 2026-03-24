#!/usr/bin/env python3
"""
Generate synthetic job postings using an LLM and output them in the same format as
merged_job_poster_ner.json: one JSON object per line with "content" and "annotation"
(character-offset spans for JOB_TITLE, COMPANY, LOCATION, SALARY, SKILLS_REQUIRED,
EXPERIENCE_REQUIRED, EDUCATION_REQUIRED, JOB_TYPE).

Requires: pip install openai
Set OPENAI_API_KEY in the environment (or pass --api-key).

Usage:
  # Generate 5 job postings
  python generate_job_postings_llm.py --count 5 --output llm_generated_job_postings.jsonl

  # Generate 1000 in batches of 100 (flush after each batch; re-run to resume if it fails)
  python generate_job_postings_llm.py --target 1000 --output llm_generated_job_postings.jsonl --batch-size 100

  # Generate with 5 postings per API call (fewer round-trips, faster)
  python generate_job_postings_llm.py --target 1000 --output llm_generated_job_postings.jsonl --batch-size 100 --per-call 5

  # Optional: pause 2 seconds after each batch to reduce rate limits
  python generate_job_postings_llm.py --target 1000 --output llm_generated_job_postings.jsonl --batch-size 100 --delay-batch 2

  # Generate Sri Lankan tech job postings (Colombo, Virtusa, WSO2, etc.)
  python generate_job_postings_llm.py --count 100 --sri-lanka --output llm_sri_lanka_jobs.jsonl

  # Generate varied formats (unstructured, bullet, compact, poster) for model robustness
  python generate_job_postings_llm.py --count 500 --format-style mix --output llm_varied_formats.jsonl

  # Merge with existing SkillSpan data (use merge_job_posters.py)
  python merge_job_posters.py --existing merged_job_poster_ner.json --llm llm_generated_job_postings.jsonl --output merged_job_poster_ner_with_llm.json
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
import time

VALID_LABELS = frozenset({
    "JOB_TITLE", "COMPANY", "LOCATION", "SALARY", "SKILLS_REQUIRED",
    "EXPERIENCE_REQUIRED", "EDUCATION_REQUIRED", "JOB_TYPE",
})

SYSTEM_PROMPT = """You are a job posting generator. You output valid JSON only, no markdown or extra text.

Generate realistic job postings that typically include:
1. Job title (e.g. Senior Software Engineer, Data Scientist)
2. Company name
3. Location (Remote, city, country, hybrid)
4. Salary or pay range (e.g. $80k-120k, Competitive, £50k)
5. Job description / responsibilities
6. Required skills and technologies
7. Experience level required (e.g. 5+ years, Entry level)
8. Education required (e.g. Bachelor's in CS, PhD preferred)
9. Job type (Full-time, Part-time, Contract, Internship)

Output a single JSON object with exactly two keys:
- "content": the full job posting text as a single string (use \\n for newlines).
- "entities": an array of objects, each with "type" (one of JOB_TITLE, COMPANY, LOCATION, SALARY, SKILLS_REQUIRED, EXPERIENCE_REQUIRED, EDUCATION_REQUIRED, JOB_TYPE) and "text" (the exact substring as it appears in content). List entities in the order they first appear. Use the exact spelling and spacing as in content.

ENTITY RULES (follow exactly):

• JOB_TITLE: Tag the job title/role (e.g. "Senior Data Scientist", "Software Engineer", "DevOps Engineer"). Tag every distinct job title if multiple are mentioned. One entity per distinct title.

• COMPANY: Tag the employer/company name (e.g. "Acme Corp", "Tech Solutions Ltd", "Virtusa"). Exactly one per posting unless multiple employers in a consortium.

• LOCATION: Tag location(s)—city, country, "Remote", "Hybrid", office address. Tag each distinct location mentioned.

• SALARY: Tag salary or pay range (e.g. "$80k-120k", "$120,000", "£50k", "Competitive", "Negotiable", "80k-100k"). Tag every salary mention.

• SKILLS_REQUIRED: Tag each required skill, technology, or tool (e.g. "Python", "Machine Learning", "React", "AWS", "SQL"). Tag every skill in the requirements section. Do NOT tag company names as skills.

• EXPERIENCE_REQUIRED: Tag experience level or years (e.g. "5+ years", "3-5 years", "Entry level", "Mid-level", "Senior"). Tag every such mention.

• EDUCATION_REQUIRED: Tag required education (e.g. "Bachelor's in Computer Science", "PhD preferred", "BSc", "Master's degree"). Tag every education requirement.

• JOB_TYPE: Tag employment type (e.g. "Full-time", "Part-time", "Contract", "Internship", "Remote"). Tag every such mention.

REQUIRED: Every job posting must have at least JOB_TITLE, COMPANY, and SKILLS_REQUIRED. Include LOCATION, SALARY, EXPERIENCE_REQUIRED, EDUCATION_REQUIRED, JOB_TYPE when present in the text.

List entities in document order. Use exact substrings from content."""

# Job role hints (mostly tech)
ROLE_HINTS = [
    "Software Engineer", "Senior Software Engineer", "Full Stack Developer",
    "Data Scientist", "Data Engineer", "Machine Learning Engineer",
    "DevOps Engineer", "Cloud Engineer", "Frontend Developer", "Backend Developer",
    "QA Engineer", "Security Engineer", "Product Manager", "Technical Lead",
    "Mobile Developer", "UI/UX Designer", "Data Analyst", "Solutions Architect",
]

# Company name hints (mix of generic and regional)
COMPANY_HINTS = [
    "Acme Corp", "Tech Solutions Ltd", "Innovation Labs", "DataDriven Inc",
    "CloudFirst", "Digital Ventures", "Analytics Pro", "DevOps Consulting",
    "Virtusa", "WSO2", "Sri Lanka Telecom", "Dialog", "John Keells",
    "Google", "Amazon", "Microsoft", "Meta", "Stripe", "Shopify",
]

# Location hints
LOCATION_HINTS = [
    "Remote", "Colombo", "New York", "San Francisco", "London", "Berlin",
    "Singapore", "Bangalore", "Hybrid", "Sri Lanka", "USA", "UK",
]

# Salary format hints
SALARY_HINTS = [
    "$80k-120k", "$100k-150k", "£50k-70k", "Competitive", "Negotiable",
    "$120,000", "80k-100k", "€60k-80k",
]

USER_PROMPT_TEMPLATE = """Generate one realistic job posting. For this posting use:
- Role: {role}
- Company: {company}
- Location: {location}
- Salary/pay: {salary}
- Job type: {job_type}

Include a brief description, key responsibilities, required skills (at least 3-5 technologies), experience level, and education requirement. Keep it concise (1-2 paragraphs).

Return JSON with "content" (full job text) and "entities" (array of {{"type": "JOB_TITLE"|"COMPANY"|"LOCATION"|"SALARY"|"SKILLS_REQUIRED"|"EXPERIENCE_REQUIRED"|"EDUCATION_REQUIRED"|"JOB_TYPE", "text": "exact substring"}} in document order). Tag every entity that appears in the text."""

BATCH_USER_PROMPT_TEMPLATE = """Generate exactly {n} different job postings. Return a single JSON array of {n} objects—no other text. Each object must have "content" (full job posting text as a single string with \\n for newlines) and "entities" (array of {{"type": "JOB_TITLE"|"COMPANY"|"LOCATION"|"SALARY"|"SKILLS_REQUIRED"|"EXPERIENCE_REQUIRED"|"EDUCATION_REQUIRED"|"JOB_TYPE", "text": "exact substring"}} in document order).

Requirements for each posting: (1) Vary role (Software Engineer, Data Scientist, DevOps, etc.), company, location (Remote, Colombo, New York, etc.), salary format, and job type. (2) Include at least JOB_TITLE, COMPANY, SKILLS_REQUIRED, LOCATION or JOB_TYPE. (3) Tag every entity that appears in the text.

Output only the JSON array, e.g. [{{"content": "...", "entities": [...]}}, ...]"""

# Sri Lankan tech job postings
USER_PROMPT_SRI_LANKA_TEMPLATE = """Generate one realistic job posting for a Sri Lankan tech company. Use:
- Role: {role}
- Company: {company} (use Sri Lankan company: Virtusa, WSO2, Dialog, Sri Lanka Telecom, John Keells, Hayleys, etc.)
- Location: Colombo or Sri Lanka or Remote (Sri Lanka)
- Salary: LKR or USD competitive; e.g. "Competitive", "LKR 200k-300k", "Negotiable"
- Job type: Full-time or Contract

Include required skills (Python, Java, React, AWS, etc.), experience level, and education. Keep concise.

Return JSON with "content" and "entities" (array of {{"type": "JOB_TITLE"|"COMPANY"|"LOCATION"|"SALARY"|"SKILLS_REQUIRED"|"EXPERIENCE_REQUIRED"|"EDUCATION_REQUIRED"|"JOB_TYPE", "text": "exact substring"}}). Tag every entity."""

BATCH_USER_PROMPT_SRI_LANKA_TEMPLATE = """Generate exactly {n} different job postings for Sri Lankan tech companies. Use companies like Virtusa, WSO2, Dialog, Sri Lanka Telecom, John Keells, Hayleys, LOLC, hSenid. Locations: Colombo, Sri Lanka, Remote. Roles: Software Engineer, Data Scientist, DevOps, Full Stack Developer, etc. Include salary (Competitive, LKR range, or Negotiable), skills, experience, education.

Return a single JSON array of {n} objects: [{{"content": "...", "entities": [...]}}, ...]. Tag every entity (JOB_TITLE, COMPANY, LOCATION, SALARY, SKILLS_REQUIRED, EXPERIENCE_REQUIRED, EDUCATION_REQUIRED, JOB_TYPE)."""

# Format-style prompts for varied layouts (helps model handle image/OCR output)
FORMAT_INSTRUCTIONS = {
    "structured": (
        "Write in the standard structured format: 'Job Title: X\\nCompany: Y\\nLocation: Z\\nSalary: ...' "
        "with explicit labels for each field."
    ),
    "unstructured": (
        "Write in UNSTRUCTURED prose. Do NOT use explicit labels like 'Job Title:' or 'Company:'. "
        "Mention the job title, company, location, salary etc. naturally within sentences. "
        "Example: 'Acme Corp is hiring a Senior Data Scientist. The role is Remote with competitive pay ($120k-150k). "
        "We need Python, ML experience. 5+ years. Full-time.'"
    ),
    "bullet": (
        "Write using BULLET POINTS only. No 'Job Title:' or 'Company:' labels. Use lines like: "
        "'• Senior Software Engineer\\n• Virtusa, Colombo\\n• $80k-120k\\n• Python, Java, AWS\\n• 3+ years Full-time'"
    ),
    "compact": (
        "Write in COMPACT form: minimal punctuation, short phrases, comma-separated. "
        "Example: 'Senior Engineer Acme Corp Remote $100k Python Java 3+ years Full-time' "
        "or single paragraph with commas. No line breaks required."
    ),
    "poster": (
        "Write in POSTER/FLYER style. Job title as a headline or first prominent line. "
        "Then company, location, brief description. No 'Job Title:' prefix. "
        "Example: 'WE ARE HIRING\\nSoftware Engineer\\nJoin Virtusa in Colombo. Competitive salary. Python, Java. Full-time.'"
    ),
    "email": (
        "Write as an EMAIL or announcement. Start with subject-line style: 'Subject: Software Engineer – Acme Corp'. "
        "Body: 'We are excited to announce...' or 'Hi, Acme Corp is hiring a Senior Data Scientist. "
        "Location: Remote. Salary: $100k-150k. Skills: Python, ML. 5+ years. Full-time.' No explicit field labels."
    ),
    "linkedin": (
        "Write in LINKEDIN/JOB-BOARD style. Use pipe-separated header: "
        "'Software Engineer | Acme Corp | Remote | Full-time | $100k-150k'. "
        "Then brief description. Skills and experience in short lines. No 'Job Title:' or 'Company:' labels."
    ),
    "minimal": (
        "Write MINIMAL/ULTRA-SHORT. One or two lines, comma or period separated. "
        "Example: 'Senior Engineer at Acme Corp. Remote. $100k. Python Java AWS. 3+ years. Full-time.' "
        "Or: 'Data Scientist, Virtusa, Colombo, LKR negotiable, Python R ML, 5y, Bachelor required.'"
    ),
    "conversational": (
        "Write in CONVERSATIONAL/casual tone. No formal structure. "
        "Example: 'Hey! We're looking for a Data Scientist to join our team at Acme. "
        "You'd work remotely, we pay around $120k. Need Python and ML experience—5 years or so. Full-time. Bachelor's preferred.'"
    ),
    "table": (
        "Write in TABLE-like layout. Use 'Role: X' or '| X | Y | Z' style. "
        "Example: 'Role: Software Engineer | Company: Acme | Location: Remote | Salary: $100k | "
        "Skills: Python, Java | Experience: 3+ years | Type: Full-time'"
    ),
}

USER_PROMPT_FORMAT_TEMPLATE = """Generate one realistic job posting with this specific format:

{format_instruction}

For this posting use:
- Role: {role}
- Company: {company}
- Location: {location}
- Salary/pay: {salary}
- Job type: {job_type}

Include skills (3-5), experience, and education. Keep concise.

Return JSON with "content" and "entities" (array of {{"type": "JOB_TITLE"|"COMPANY"|"LOCATION"|"SALARY"|"SKILLS_REQUIRED"|"EXPERIENCE_REQUIRED"|"EDUCATION_REQUIRED"|"JOB_TYPE", "text": "exact substring"}}). Tag every entity that appears."""

BATCH_USER_PROMPT_FORMAT_TEMPLATE = """Generate exactly {n} different job postings. Each must use this format:

{format_instruction}

Vary role (Software Engineer, Data Scientist, DevOps, etc.), company, location (Remote, Colombo, etc.), salary, job type. Include at least JOB_TITLE, COMPANY, SKILLS_REQUIRED. Tag every entity.

Return a single JSON array of {n} objects: [{{"content": "...", "entities": [...]}}, ...]"""


def _extract_json_from_response(raw: str):
    """Parse JSON from LLM response, optionally inside a markdown code block."""
    raw = raw.strip()
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```\s*$", "", raw)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        repaired = re.sub(r",\s*([}\]])", r"\1", raw)
        try:
            return json.loads(repaired)
        except json.JSONDecodeError:
            raise


def _find_spans_in_order(content: str, entities: list[dict]) -> list[dict]:
    """Build annotation list with character offsets from entities."""
    annotations = []
    search_start = 0
    for ent in entities:
        if not isinstance(ent, dict):
            continue
        label = (ent.get("type") or "").strip().upper()
        if label not in VALID_LABELS:
            continue
        text = (ent.get("text") or "").strip()
        if not text:
            continue
        idx = content.find(text, search_start)
        if idx == -1:
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


def _item_from_content_entities(content: str, entities: list) -> dict | None:
    """Convert content + entities to output item (content, annotation) or None."""
    if not content:
        return None
    annotations = _find_spans_in_order(content, entities)
    if not annotations:
        return None
    return {"content": content, "annotation": annotations}


def _item_has_minimum_entities(item: dict) -> bool:
    """Return True if item has at least JOB_TITLE, COMPANY, SKILLS_REQUIRED."""
    if not item:
        return False
    anns = item.get("annotation") or []
    labels = set()
    for a in anns:
        lbls = a.get("label") or []
        if lbls:
            labels.add(str(lbls[0]).strip())
    return "JOB_TITLE" in labels and "COMPANY" in labels and "SKILLS_REQUIRED" in labels


def generate_one(
    client,
    model: str = "gpt-4o-mini",
    timeout: int = 60,
    role_hint: str | None = None,
    company_hint: str | None = None,
    location_hint: str | None = None,
    salary_hint: str | None = None,
    job_type_hint: str | None = None,
    sri_lanka: bool = False,
    format_style: str = "structured",
) -> dict | None:
    """Call LLM once and return one job posting item or None on failure."""
    role = role_hint or random.choice(ROLE_HINTS)
    if sri_lanka:
        company = company_hint or random.choice([
            "Virtusa", "WSO2", "Dialog", "Sri Lanka Telecom", "John Keells",
            "Hayleys", "LOLC", "hSenid", "Zone24x7", "Vee Technologies",
        ])
        location = location_hint or random.choice(["Colombo", "Sri Lanka", "Remote"])
        salary = salary_hint or random.choice(["Competitive", "LKR 200k-300k", "Negotiable"])
        job_type = job_type_hint or random.choice(["Full-time", "Contract"])
    else:
        company = company_hint or random.choice(COMPANY_HINTS)
        location = location_hint or random.choice(LOCATION_HINTS)
        salary = salary_hint or random.choice(SALARY_HINTS)
        job_type = job_type_hint or random.choice(["Full-time", "Part-time", "Contract", "Remote"])

    if format_style and format_style != "structured" and format_style in FORMAT_INSTRUCTIONS:
        fmt = FORMAT_INSTRUCTIONS[format_style]
        sri_note = " Use Sri Lankan companies and LKR salary. " if sri_lanka else ""
        user_prompt = USER_PROMPT_FORMAT_TEMPLATE.format(
            format_instruction=fmt + sri_note,
            role=role, company=company, location=location,
            salary=salary, job_type=job_type,
        )
    elif sri_lanka:
        user_prompt = USER_PROMPT_SRI_LANKA_TEMPLATE.format(role=role, company=company)
    else:
        user_prompt = USER_PROMPT_TEMPLATE.format(
            role=role, company=company, location=location,
            salary=salary, job_type=job_type,
        )
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
        if isinstance(data, list) and len(data) >= 1:
            data = data[0]
        if not isinstance(data, dict):
            return None
        content = (data.get("content") or "").strip()
        entities = data.get("entities") or []
        if not isinstance(entities, list):
            entities = []
        item = _item_from_content_entities(content, entities)
        if not item or not _item_has_minimum_entities(item):
            return None
        return item
    except Exception as e:
        print(f"LLM call failed: {e}", file=sys.stderr)
        return None


def generate_batch(
    client,
    n: int,
    model: str = "gpt-4o-mini",
    timeout: int = 120,
    sri_lanka: bool = False,
    format_style: str = "structured",
) -> list[dict]:
    """Call LLM once asking for n job postings; return list of valid items."""
    if n <= 0:
        return []
    if format_style and format_style != "structured" and format_style in FORMAT_INSTRUCTIONS:
        fmt = FORMAT_INSTRUCTIONS[format_style]
        sri_note = " Use Sri Lankan companies, Colombo, LKR. " if sri_lanka else ""
        user_prompt = BATCH_USER_PROMPT_FORMAT_TEMPLATE.format(
            n=n,
            format_instruction=fmt + sri_note,
        )
    elif sri_lanka:
        user_prompt = BATCH_USER_PROMPT_SRI_LANKA_TEMPLATE.format(n=n)
    else:
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
            try:
                if not isinstance(obj, dict):
                    continue
                content = (obj.get("content") or "").strip()
                entities = obj.get("entities") or []
                if not isinstance(entities, list):
                    entities = []
                item = _item_from_content_entities(content, entities)
                if item and _item_has_minimum_entities(item):
                    out.append(item)
            except Exception as item_err:
                print(f"Batch item skipped: {item_err}", file=sys.stderr)
        return out
    except Exception as e:
        print(f"LLM batch call failed: {e}", file=sys.stderr)
        return []


def main():
    parser = argparse.ArgumentParser(
        description="Generate job posting JSONL via LLM (same format as merged_job_poster_ner.json)"
    )
    parser.add_argument("--count", type=int, default=5, help="Number of job postings to generate this run")
    parser.add_argument("--target", type=int, default=None, help="Target total lines; if output exists, generate (target - current) and append")
    parser.add_argument("--output", type=str, default="llm_generated_job_postings.jsonl", help="Output JSONL file path")
    parser.add_argument("--append", action="store_true", help="Append to output file instead of overwriting")
    parser.add_argument("--batch-size", type=int, default=100, help="Flush after every N postings")
    parser.add_argument("--per-call", type=int, default=1, help="Postings per API call (e.g. 5 = fewer calls)")
    parser.add_argument("--delay-batch", type=float, default=0, help="Seconds to sleep after each batch")
    parser.add_argument("--api-key", type=str, default=None, help="OpenAI API key (or set OPENAI_API_KEY)")
    parser.add_argument("--model", type=str, default="gpt-4o-mini", help="OpenAI model name")
    parser.add_argument("--timeout", type=int, default=60, help="Timeout per request in seconds")
    parser.add_argument("--sri-lanka", action="store_true", help="Generate Sri Lankan tech job postings (Virtusa, WSO2, Colombo, etc.)")
    parser.add_argument(
        "--format-style",
        type=str,
        default="structured",
        choices=["structured", "unstructured", "bullet", "compact", "poster", "email", "linkedin", "minimal", "conversational", "table", "mix"],
        help="Format: structured, unstructured, bullet, compact, poster, email, linkedin, minimal, conversational, table, or mix (round-robin)",
    )
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
        else:
            mode = "w"

    if to_generate <= 0 and args.target is not None:
        print("Already at or above target. Nothing to generate.", file=sys.stderr)
        return

    per_call = max(1, min(args.per_call, 10))
    batch_size = max(1, args.batch_size)
    target_total = args.target if args.target else (existing + to_generate)
    print(f"Batches of {batch_size}. Target total: {target_total}. Postings per API call: {per_call}", file=sys.stderr)
    if args.sri_lanka:
        print("Mode: Sri Lankan tech job postings", file=sys.stderr)
    if args.format_style != "structured":
        print(f"Format style: {args.format_style}", file=sys.stderr)

    format_choices = [
        "structured", "unstructured", "bullet", "compact", "poster",
        "email", "linkedin", "minimal", "conversational", "table",
    ]
    format_idx = [0]

    def _get_format_style():
        if args.format_style == "mix":
            style = format_choices[format_idx[0] % len(format_choices)]
            format_idx[0] += 1
            return style
        return args.format_style

    client = openai.OpenAI(api_key=api_key)
    written = 0
    remaining = to_generate
    with open(args.output, mode, encoding="utf-8") as f:
        while remaining > 0:
            want_this_call = min(per_call, remaining)
            items = []
            if want_this_call == 1:
                for attempt in range(3):
                    item = generate_one(
                        client,
                        model=args.model,
                        timeout=args.timeout,
                        sri_lanka=args.sri_lanka,
                        format_style=_get_format_style(),
                    )
                    if item:
                        items = [item]
                        break
                    if attempt < 2:
                        time.sleep(2 ** attempt)
            else:
                for attempt in range(3):
                    items = generate_batch(
                        client,
                        want_this_call,
                        model=args.model,
                        timeout=args.timeout,
                        sri_lanka=args.sri_lanka,
                        format_style=_get_format_style(),
                    )
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
            if args.delay_batch > 0 and remaining > 0:
                time.sleep(args.delay_batch)
        f.flush()

    print(f"Done. Wrote {written} job postings to {args.output} (total: {existing + written})", file=sys.stderr)


if __name__ == "__main__":
    main()
