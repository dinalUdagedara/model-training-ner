"""
Agent (LLM) corrector for Resume NER entities.

Second-stage pipeline that takes raw resume text + NER-extracted entities,
optionally sends them to an LLM for correction/validation, and returns
corrected entities or falls back to the NER output on failure.

Usage:
    from agent_corrector import correct_entities_with_agent

    entities_corrected = correct_entities_with_agent(
        text=resume_text,
        entities=entities_from_ner,
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
"""

from __future__ import annotations

import json
import logging
import os
import re
from typing import Any

# Valid entity types for resume NER (must match notebook schema)
VALID_ENTITY_TYPES = frozenset({"NAME", "EMAIL", "SKILL", "OCCUPATION", "EDUCATION", "EXPERIENCE"})

# Default timeout in seconds for LLM API calls
DEFAULT_TIMEOUT = 30

logger = logging.getLogger(__name__)


def _validate_entities(entities: dict[str, list[str]]) -> bool:
    """Check that entities dict has valid structure: {str: [str]} with valid keys."""
    if not isinstance(entities, dict):
        return False
    for k, v in entities.items():
        if k not in VALID_ENTITY_TYPES:
            return False
        if not isinstance(v, list):
            return False
        if not all(isinstance(x, str) for x in v):
            return False
    return True


def _normalize_entities(entities: dict[str, list[str]]) -> dict[str, list[str]]:
    """Strip whitespace, dedupe (case-insensitive), remove empty strings."""
    out = {}
    for k, v in entities.items():
        seen = set()
        values = []
        for s in v:
            s = (s or "").strip()
            if not s:
                continue
            key_lower = s.lower()
            if key_lower in seen:
                continue
            seen.add(key_lower)
            values.append(s)
        out[k] = values
    return out


def correct_entities_openai(
    text: str,
    entities: dict[str, list[str]],
    api_key: str | None = None,
    model: str = "gpt-4o-mini",
    timeout: int = DEFAULT_TIMEOUT,
) -> dict[str, list[str]]:
    """
    Use OpenAI API to correct/validate extracted entities.

    Args:
        text: Raw resume text
        entities: NER-extracted entities dict
        api_key: OpenAI API key (or set OPENAI_API_KEY env var)
        model: Model name (default gpt-4o-mini for cost/speed)
        timeout: Request timeout in seconds

    Returns:
        Corrected entities dict, or original if API fails/invalid
    """
    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        logger.warning("No OpenAI API key; returning original entities")
        return entities

    if not _validate_entities(entities):
        logger.warning("Invalid entities structure; returning original")
        return entities

    try:
        import openai
    except ImportError:
        logger.warning("openai package not installed; pip install openai. Returning original entities.")
        return entities

    client = openai.OpenAI(api_key=api_key)
    prompt = _build_correction_prompt(text, entities)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            timeout=timeout,
        )
        content = (response.choices[0].message.content or "").strip()
        corrected = _parse_llm_response(content)
        if corrected is not None and _validate_entities(corrected):
            return _normalize_entities(corrected)
        logger.warning("LLM response invalid or malformed; using original entities")
        return entities
    except Exception as e:
        logger.warning("LLM corrector failed: %s; using original entities", e)
        return entities


def _build_correction_prompt(text: str, entities: dict[str, list[str]]) -> str:
    """Build the prompt for the LLM corrector."""
    entities_json = json.dumps(entities, indent=2)
    return f"""You are a resume entity correction assistant. Given the raw resume text and the entities extracted by an NER model, correct any obvious errors: wrong entity types, missed entities, or noise (e.g. punctuation-only, irrelevant words).

Rules:
- Output a JSON object with keys: NAME, EMAIL, SKILL, OCCUPATION, EDUCATION, EXPERIENCE
- Each value must be a list of strings (entity phrases)
- Only output valid JSON, no other text
- Keep correct extractions as-is; fix only what is wrong
- If an entity type has no valid entities, use an empty list []
- Deduplicate (case-insensitive)

Resume text:
---
{text[:4000]}
---

Extracted entities (may contain errors):
{entities_json}

Output the corrected entities as JSON only:"""


def _parse_llm_response(content: str) -> dict[str, list[str]] | None:
    """Parse LLM response into entities dict. Returns None if invalid."""
    content = content.strip()
    # Strip markdown code blocks if present
    if content.startswith("```"):
        lines = content.split("\n")
        out_lines = []
        in_block = False
        for line in lines:
            if line.startswith("```"):
                in_block = not in_block
                continue
            if in_block:
                out_lines.append(line)
        content = "\n".join(out_lines)

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        return None

    if not isinstance(data, dict):
        return None

    result = {}
    for k in VALID_ENTITY_TYPES:
        v = data.get(k, [])
        if isinstance(v, list):
            result[k] = [str(x).strip() for x in v if isinstance(x, str) and x.strip()]
        else:
            result[k] = []
    return result


def correct_entities_with_agent(
    text: str,
    entities: dict[str, list[str]],
    api_key: str | None = None,
    use_llm: bool = True,
    model: str = "gpt-4o-mini",
    timeout: int = DEFAULT_TIMEOUT,
) -> dict[str, list[str]]:
    """
    Correct NER-extracted entities using an optional LLM agent.

    If use_llm=True and api_key is provided, calls the LLM to fix obvious errors.
    On any failure (no key, API error, invalid response), falls back to the
    original entities. Also applies light post-processing (normalize, dedupe).

    Args:
        text: Raw resume text
        entities: NER-extracted entities (e.g. from parse_resume_hybrid)
        api_key: OpenAI API key (or OPENAI_API_KEY env)
        use_llm: If False, only applies normalization (no LLM call)
        model: OpenAI model name
        timeout: API timeout in seconds

    Returns:
        Corrected entities dict
    """
    if not entities:
        return entities

    # Always normalize first
    entities = _normalize_entities(entities)

    if not use_llm:
        return entities

    return correct_entities_openai(
        text=text,
        entities=entities,
        api_key=api_key,
        model=model,
        timeout=timeout,
    )
