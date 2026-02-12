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

  # Merge with existing merged dataset
  cat merged_1030_plus_all_llm.jsonl llm_sri_lanka_tech.jsonl > merged_1030_plus_all_llm_plus_sri_lanka_tech.jsonl

  # Fix missing EDUCATION/OCCUPATION with a second LLM call per incomplete resume (adds API cost)
  python generate_resumes_llm.py --count 20 --fix-missing --entity-rich --output llm_fixed.jsonl

  # Generate Sri Lankan tech resumes (structured: SUMMARY, EDUCATION, EXPERIENCE, PROJECTS with Tech Stack, SKILLS subsections, etc.)
  python generate_resumes_llm.py --count 50 --sri-lanka-tech --output llm_sri_lanka_tech.jsonl
  python generate_resumes_llm.py --target 1000 --sri-lanka-tech --output llm_sri_lanka_tech.jsonl --batch-size 100 --per-call 5
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

• EDUCATION: Tag only (1) degree or qualification names (e.g. "Bachelor of Science in Computer Science", "BSc", "MSc") and (2) educational institution names (e.g. "University of California, Berkeley", "University of Colombo"). Never tag a company or employer as EDUCATION—those are EXPERIENCE. Tag every degree and every institution in the EDUCATION section—do not skip the first (or any) entry. Do not tag dates or cities unless part of the institution name.

• EXPERIENCE: Tag every company or employer name (e.g. "Tech Innovations Inc.", "Virtusa", "Analytics Ltd.", "WSO2"), including the first employer in each role—do not skip the first entry in the experience section. Do NOT tag job titles (those are OCCUPATION), date ranges, locations, universities, or schools. Only for employed resumes. Never tag a university or college as EXPERIENCE—those are EDUCATION.

• SKILL: Tag every distinct technology, tool, and soft skill (e.g. "Python", "Java", "Problem-solving", "Communication"). Do NOT tag company or employer names as SKILL—those are EXPERIENCE (e.g. "Analytics Ltd.", "Tech Solutions" = EXPERIENCE, not SKILL). Tag each programming language, tool, and soft skill under SKILLS and in "Tech Stack:" lines. Do not tag section labels like "Programming Languages:" or "Tech Stack:".

COMPLETENESS CHECKLIST (before returning, verify):
- Exactly one NAME and one EMAIL.
- If the text contains job titles (in experience section or summary), every one is tagged as OCCUPATION.
- Tag every company (including the first employer in each role) as EXPERIENCE and every degree and every institution as EDUCATION—do not skip the first entry in a section.
- If the text contains companies/employers, every one is tagged as EXPERIENCE (never as EDUCATION or SKILL).
- Every degree and institution in EDUCATION is tagged as EDUCATION (never tag companies as EDUCATION).
- Every skill and Tech Stack tech is tagged as SKILL (never tag company names as SKILL).
- No entity is from the REFERENCES section.

CRITICAL – Do not confuse entity types: Companies (e.g. "Virtusa", "Tech Solutions Ltd.") = EXPERIENCE only. Universities/schools (e.g. "University of Colombo") = EDUCATION only. Technologies/tools (e.g. "Python", "Java") = SKILL only.

Before returning: confirm you have at least one EDUCATION entity (degree or institution) and, if the resume has work experience, one EXPERIENCE entity per role (do not skip the first company)."""

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

Before returning JSON you MUST: (1) If the resume has work experience, tag every job title as OCCUPATION and every company as EXPERIENCE (including the first employer in each role)—do not skip the first entry in a section. (2) Tag every degree and every institution under EDUCATION—do not skip any. (3) Tag every skill and Tech Stack tech as SKILL (not company names). (4) Do not tag anything in REFERENCES. Return JSON with "content" and "entities" (exact substrings, in document order)."""

# For batched mode: ask for N resumes in one response (fewer API calls).
BATCH_USER_PROMPT_TEMPLATE = """Generate exactly {n} different resumes. Return a single JSON array of {n} objects—no other text. Each object must have "content" (full resume text as a single string with \\n for newlines) and "entities" (array of {{"type": "NAME"|"EMAIL"|"SKILL"|"OCCUPATION"|"EDUCATION"|"EXPERIENCE", "text": "exact substring"}} in document order).

Requirements for each resume: (1) Vary career (mostly IT: Software Engineer, Data Scientist, DevOps, etc.; some non-IT: Healthcare, Finance, Marketing) and region (Sri Lanka, India, US, UK, etc.). (2) Tag every job title as OCCUPATION and every company as EXPERIENCE (including the first employer in each role)—do not skip the first entry in a section. (3) Tag every degree and every institution as EDUCATION—do not skip any. (4) Tag every skill as SKILL (not company names). (5) Do not tag anything in REFERENCES.

Output only the JSON array, e.g. [{{"content": "...", "entities": [...]}}, {{"content": "...", "entities": [...]}}, ...]"""

# Optional suffix to encourage more OCCUPATION/EXPERIENCE annotations (for entity-rich expansion).
ENTITY_RICH_APPEND = " For employed resumes: include at least two distinct job titles (tag as OCCUPATION) and two company names (tag as EXPERIENCE) so annotations are clear and complete."

# Sri Lankan tech (structured) resumes: fixed layout (SUMMARY, EDUCATION, EXPERIENCE, PROJECTS with Tech Stack, CERTIFICATIONS, SKILLS subsections, REFERENCES).
SRI_LANKA_TECH_STRUCTURE = """
Use this EXACT structure and style (Sri Lanka only; names, institutions, companies, and +94 phone):
1. Full name in ALL CAPS (e.g. JOHN PERERA)
2. Field line (e.g. Software Engineering or Computer Science)
3. Email | LinkedIn URL | GitHub URL | Phone (+94 7x xxx xxxx or 0xx-xxxxxxx)
4. SUMMARY – short paragraph (2–3 sentences)
5. EDUCATION – Institution (e.g. Trincomalee Campus, Eastern University, Sri Lanka OR University of Colombo OR D.S. Senanayake College, city). Dates. Degree (e.g. Bachelor of Computer Science (CGPA - x.xx)). Include A/L or similar if relevant.
6. EXPERIENCE – "Role – Company Name (abbrev), City, Date range". Use Sri Lankan companies (e.g. Sri Lanka Telecom (SLT), Virtusa, WSO2, Dialog, Tech Solutions, etc.). Bullet points with •
7. PROJECTS – "Project Name – Company | Status". Bullet points with •. Each project MUST include a line "Tech Stack: ..." listing technologies (e.g. React, Node.js, MongoDB, Python).
8. CERTIFICATIONS – bullet list with •
9. SKILLS – use these subsection headers with bullets: "Programming Languages: ...", "Web Technologies: ...", "Frameworks / Libraries: ...", "DevOps, Cloud and System Tools: ...", "Databases: ...", "Tools & Platforms: ...", "Soft Skills: ..."
10. REFERENCES – optional (do not tag anything in this section)

Keep total length similar to a full 1–2 page resume (plenty of skills and at least 2–3 projects with Tech Stack). Use • for bullets. Tag every skill, every Tech Stack item, every degree/institution, every job title, and every company.
"""

USER_PROMPT_SRI_LANKA_TECH_TEMPLATE = """Generate ONE resume in the structured Sri Lankan tech format. Career for this resume: {career}. Region: Sri Lanka only—use Sri Lankan names, institutions (e.g. Eastern University, University of Colombo, Trincomalee Campus), companies (e.g. Sri Lanka Telecom, Virtusa, WSO2), and +94 phone format.
""" + SRI_LANKA_TECH_STRUCTURE + """
Before returning JSON: tag every job title as OCCUPATION, every company as EXPERIENCE, every degree and institution as EDUCATION, every skill and Tech Stack tech as SKILL. Do not tag anything in REFERENCES. Return JSON with "content" and "entities" (exact substrings, in document order)."""

BATCH_USER_PROMPT_SRI_LANKA_TECH_TEMPLATE = """Generate exactly {n} different resumes. Each resume MUST follow the structured Sri Lankan tech format: ALL CAPS name; field line; email | LinkedIn | GitHub | +94 phone; SUMMARY; EDUCATION (institution, degree); EXPERIENCE (Role – Company, City, dates); PROJECTS (each with "Tech Stack: ..."); CERTIFICATIONS; SKILLS with subsections (Programming Languages, Web Technologies, Frameworks/Libraries, DevOps/Cloud, Databases, Tools & Platforms, Soft Skills); REFERENCES. Use • for bullets. Vary names, institutions (Eastern University, University of Colombo, etc.), companies (SLT, Virtusa, WSO2, etc.), and careers (Full Stack Developer, Software Engineer, Data Scientist, etc.). Tag every OCCUPATION, EXPERIENCE, EDUCATION, SKILL (including all Tech Stack items). Do not tag REFERENCES.

Return a single JSON array of {n} objects: [{{"content": "...", "entities": [...]}}, ...]. No other text."""

SRI_LANKA_TECH_CAREER_HINTS = [
    "Full Stack Developer or Software Engineering student/intern",
    "Software Engineer (React, Node.js, MERN)",
    "Data Scientist or ML Engineer (Python, TensorFlow)",
    "DevOps Engineer or Cloud Engineer",
    "Mobile Developer (React Native or Android)",
    "QA Engineer or Test Automation",
]

# Second-pass "fix" call: given content + current entities, return complete entity list (fixes missing EDUCATION/OCCUPATION/EXPERIENCE).
FIX_ENTITIES_SYSTEM_PROMPT = """You are an entity-annotation fixer for resume NER. You receive resume text and a current list of entities (type + text). Some entities may be missing.

Your task: output the COMPLETE list of entities in document order. Add any missing entities; keep existing correct ones. Rules:
- NAME: exactly one (candidate's full name, first line). EMAIL: exactly one (contact line).
- EDUCATION: tag EVERY degree (e.g. BSc, MSc, MBA) and EVERY institution (e.g. University of Colombo) that appear in the EDUCATION section. Do not tag companies as EDUCATION.
- EXPERIENCE: tag EVERY company/employer name. Do not tag job titles or universities as EXPERIENCE.
- OCCUPATION: tag EVERY job title (e.g. Software Engineer, Data Scientist, Junior Developer) that appears in the EXPERIENCE section or in SUMMARY. Do not tag the field line (e.g. "Computer Science") or section headers.
- SKILL: every technology, tool, and soft skill. Not company names.
- Do not tag anything in REFERENCES.

Output valid JSON only: {"entities": [{"type": "NAME"|"EMAIL"|"SKILL"|"OCCUPATION"|"EDUCATION"|"EXPERIENCE", "text": "exact substring"}, ...]} in document order. No other text."""

FIX_ENTITIES_USER_TEMPLATE = """Resume content (exact text):

{content}

Current entities (may be incomplete):
{current_entities}

Return the complete list of entities in document order as JSON: {{"entities": [...]}}"""


def _annotation_to_entities_list(annotation: list) -> list[dict]:
    """Convert annotation format to list of {type, text} for the fix prompt."""
    out = []
    for a in annotation or []:
        labels = a.get("label") or []
        pts = a.get("points") or []
        if not labels or not pts:
            continue
        label = labels[0] if isinstance(labels[0], str) else str(labels[0])
        text = (pts[0].get("text") or "").strip() if pts else ""
        if text and label in VALID_LABELS:
            out.append({"type": label, "text": text})
    return out


def _extract_json_from_response(raw: str):
    """Parse JSON from LLM response, optionally inside a markdown code block. Returns parsed value or raises."""
    raw = raw.strip()
    # Remove optional markdown code block
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```\s*$", "", raw)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Try to fix common issues: trailing comma before ] or }
        repaired = re.sub(r",\s*([}\]])", r"\1", raw)
        try:
            return json.loads(repaired)
        except json.JSONDecodeError:
            raise


def _find_spans_in_order(content: str, entities: list[dict]) -> list[dict]:
    """
    Build annotation list with character offsets.
    entities: list of {"type": "NAME"|..., "text": "exact span"}
    We find each "text" in content in order (so duplicate text gets first occurrence then next, etc.).
    """
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
        if not isinstance(e, dict):
            continue
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


def _item_fails_completeness(item: dict) -> bool:
    """Return True if item should be discarded: content clearly has EDUCATION section but no EDUCATION entities."""
    if not item:
        return True
    content = (item.get("content") or "").strip().upper()
    annotations = item.get("annotation") or []
    has_education_section = "EDUCATION" in content
    has_education_entity = any(
        isinstance(a, dict) and (a.get("label") or []) and (a.get("label") or [])[0] == "EDUCATION"
        for a in annotations
    )
    return has_education_section and not has_education_entity


def _item_fails_occupation(item: dict) -> bool:
    """Return True if content has EXPERIENCE section with role–company pattern but no OCCUPATION entities."""
    if not item:
        return True
    content = (item.get("content") or "").strip()
    annotations = item.get("annotation") or []
    has_experience_section = "EXPERIENCE" in content.upper() and (" – " in content or " - " in content)
    has_occupation_entity = any(
        isinstance(a, dict) and (a.get("label") or []) and (a.get("label") or [])[0] == "OCCUPATION"
        for a in annotations
    )
    return has_experience_section and not has_occupation_entity


def _item_needs_fix(item: dict) -> bool:
    """True if item has missing EDUCATION or OCCUPATION and should get a fix call."""
    return _item_fails_completeness(item) or _item_fails_occupation(item)


def fix_item_entities(client, item: dict, model: str = "gpt-4o-mini", timeout: int = 45) -> dict | None:
    """Second LLM call: given content + current annotation, return item with fixed annotation or None on failure."""
    if not item:
        return None
    content = (item.get("content") or "").strip()
    if not content:
        return None
    current = _annotation_to_entities_list(item.get("annotation") or [])
    current_entities_str = json.dumps(current, ensure_ascii=False, indent=0)
    user_prompt = FIX_ENTITIES_USER_TEMPLATE.format(content=content, current_entities=current_entities_str)
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": FIX_ENTITIES_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
            timeout=timeout,
        )
        raw = (response.choices[0].message.content or "").strip()
        if not raw:
            return None
        try:
            data = _extract_json_from_response(raw)
        except Exception as parse_err:
            print(f"Fix-entities parse failed: {parse_err}", file=sys.stderr)
            return None
        if isinstance(data, list):
            entities = data
        elif isinstance(data, dict):
            entities = data.get("entities")
        else:
            entities = None
        if not isinstance(entities, list):
            return None
        annotations = _find_spans_in_order(content, entities)
        if not annotations:
            return None
        return {"content": content, "annotation": annotations, "extras": None}
    except Exception as e:
        print(f"Fix-entities call failed: {e}", file=sys.stderr)
        return None


def generate_batch(client, n: int, model: str = "gpt-4o-mini", timeout: int = 120, entity_rich: bool = False, sri_lanka_tech: bool = False, strict_completeness: bool = True, fix_missing: bool = False) -> list[dict]:
    """Call LLM once asking for n resumes; return list of valid items (may be fewer than n)."""
    if n <= 0:
        return []
    if sri_lanka_tech:
        user_prompt = BATCH_USER_PROMPT_SRI_LANKA_TECH_TEMPLATE.format(n=n)
    else:
        user_prompt = BATCH_USER_PROMPT_TEMPLATE.format(n=n)
        if entity_rich:
            user_prompt += "\n\n" + ENTITY_RICH_APPEND
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
        try:
            data = _extract_json_from_response(raw)
        except Exception as parse_err:
            print(f"LLM batch parse failed: {parse_err}", file=sys.stderr)
            return []
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
                if not item:
                    continue
                if strict_completeness and _item_needs_fix(item):
                    if fix_missing:
                        try:
                            fixed = fix_item_entities(client, item, model=model, timeout=min(timeout, 45))
                            if fixed is not None:
                                item = fixed
                        except Exception as fix_err:
                            print(f"Fix call failed (keeping original): {fix_err}", file=sys.stderr)
                    if _item_fails_completeness(item):
                        continue
                elif strict_completeness and _item_fails_completeness(item):
                    continue
                out.append(item)
            except Exception as item_err:
                print(f"LLM batch item skipped: {item_err}", file=sys.stderr)
                continue
        return out
    except Exception as e:
        print(f"LLM batch call failed: {e}", file=sys.stderr)
        return []


def generate_one(client, model: str = "gpt-4o-mini", timeout: int = 60, career_hint: str | None = None, region_hint: str | None = None, entity_rich: bool = False, sri_lanka_tech: bool = False, strict_completeness: bool = True, fix_missing: bool = False) -> dict | None:
    """Call LLM once and return one item in merged_resume_ner format or None on failure."""
    if sri_lanka_tech:
        career = career_hint or random.choice(SRI_LANKA_TECH_CAREER_HINTS)
        region_hint = "Sri Lanka"
        user_prompt = USER_PROMPT_SRI_LANKA_TECH_TEMPLATE.format(career=career)
    else:
        if career_hint is None:
            career = random.choice(CAREER_HINTS_IT) if random.random() < IT_WEIGHT else random.choice(CAREER_HINTS_OTHER)
        else:
            career = career_hint
        region = region_hint or random.choice(REGION_HINTS)
        user_prompt = USER_PROMPT_TEMPLATE.format(career=career, region=region)
        if entity_rich:
            user_prompt += "\n\n" + ENTITY_RICH_APPEND
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
        try:
            data = _extract_json_from_response(raw)
        except Exception as parse_err:
            print(f"LLM parse failed: {parse_err}", file=sys.stderr)
            return None
        # Accept single object or single-element array
        if isinstance(data, list) and len(data) >= 1:
            data = data[0]
        if not isinstance(data, dict):
            return None
        content = (data.get("content") or "").strip()
        entities = data.get("entities") or []
        if not isinstance(entities, list):
            entities = []
        item = _item_from_content_entities(content, entities)
        if not item:
            return None
        if strict_completeness and _item_needs_fix(item):
            if fix_missing:
                try:
                    fixed = fix_item_entities(client, item, model=model, timeout=min(timeout, 45))
                    if fixed is not None:
                        item = fixed
                except Exception as fix_err:
                    print(f"Fix call failed (keeping original): {fix_err}", file=sys.stderr)
            if _item_fails_completeness(item):
                return None
        elif strict_completeness and _item_fails_completeness(item):
            return None
        return item
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
    parser.add_argument("--entity-rich", action="store_true", help="Ask for at least 2 job titles (OCCUPATION) and 2 companies (EXPERIENCE) per employed resume for clearer training data")
    parser.add_argument("--no-strict-completeness", action="store_true", help="Do not discard items that have an EDUCATION section in content but no EDUCATION entities (default: discard such items)")
    parser.add_argument("--fix-missing", action="store_true", help="When an item is missing EDUCATION or OCCUPATION, make a second LLM call to fill in missing entities (adds API cost)")
    parser.add_argument("--sri-lanka-tech", action="store_true", help="Generate structured Sri Lankan tech resumes: SUMMARY, EDUCATION, EXPERIENCE, PROJECTS (with Tech Stack), CERTIFICATIONS, SKILLS subsections, REFERENCES")
    args = parser.parse_args()
    strict_completeness = not args.no_strict_completeness

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
                    item = generate_one(client, model=args.model, timeout=args.timeout, career_hint=None, region_hint=None, entity_rich=args.entity_rich, sri_lanka_tech=args.sri_lanka_tech, strict_completeness=strict_completeness, fix_missing=args.fix_missing)
                    if item:
                        items = [item]
                        break
                    if attempt < 2:
                        time.sleep(2 ** attempt)
            else:
                for attempt in range(3):
                    items = generate_batch(client, want_this_call, model=args.model, timeout=args.timeout, entity_rich=args.entity_rich, sri_lanka_tech=args.sri_lanka_tech, strict_completeness=strict_completeness, fix_missing=args.fix_missing)
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
