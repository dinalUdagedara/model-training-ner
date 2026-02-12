#!/usr/bin/env python3
"""
Validate and optionally clean LLM-generated resume JSONL (same format as merged_resume_ner.json).
Required entities: NAME, EMAIL, EDUCATION, SKILL. OCCUPATION and EXPERIENCE are optional (e.g. student
resumes with no work history). Use before or after a large run to spot missing entities and drop
annotations that fall in REFERENCES.

Usage:
  python validate_resumes_jsonl.py llm_generated_resumes.jsonl
  python validate_resumes_jsonl.py llm_generated_resumes.jsonl --fix-references -o cleaned.jsonl
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys


def _ref_start(content: str) -> int | None:
    """Return character index where REFERENCES section starts, or None."""
    m = re.search(r"\nREFERENCES\s*\n", content, re.IGNORECASE)
    return m.start() if m else None


def _has_label(annotation: list, label: str) -> bool:
    return any((a.get("label") or [None])[0] == label for a in annotation)


def validate_line(line: str, idx: int, ref_strip: bool) -> tuple[dict | None, list[str]]:
    """
    Parse one JSONL line, optionally strip annotations that start in REFERENCES.
    Returns (item_or_none, list of issue strings).
    """
    issues = []
    try:
        item = json.loads(line)
    except json.JSONDecodeError as e:
        return None, [f"Invalid JSON: {e}"]

    content = (item.get("content") or "").strip()
    ann = item.get("annotation") or []

    if not content:
        issues.append("Empty content")
    if not ann:
        issues.append("No annotations")

    ref_start = _ref_start(content)
    if ref_start is not None:
        # Drop any annotation whose span starts at or after REFERENCES
        if ref_strip:
            kept = []
            for a in ann:
                pts = [p for p in (a.get("points") or []) if p.get("start", 0) < ref_start]
                if pts:
                    kept.append({"label": a.get("label"), "points": pts})
            item["annotation"] = kept
            ann = kept
        else:
            for a in ann:
                for pt in a.get("points") or []:
                    if pt.get("start", 0) >= ref_start:
                        issues.append("Entity in REFERENCES section (consider --fix-references)")
                        break

    if not _has_label(ann, "NAME"):
        issues.append("Missing NAME")
    if not _has_label(ann, "EMAIL"):
        issues.append("Missing EMAIL")
    if not _has_label(ann, "EDUCATION"):
        issues.append("Missing EDUCATION")
    if not _has_label(ann, "SKILL"):
        issues.append("Missing SKILL")
    # OCCUPATION and EXPERIENCE are optional (e.g. student resumes with no work history).
    # We do not add them to issues so student resumes can pass; main() still counts them for stats.

    return item, issues


def main():
    parser = argparse.ArgumentParser(description="Validate (and optionally clean) resume JSONL")
    parser.add_argument("input", type=str, help="Input JSONL file")
    parser.add_argument("--fix-references", action="store_true", help="Remove annotations that fall in REFERENCES section")
    parser.add_argument("-o", "--output", type=str, default=None, help="Write cleaned output to this file (use with --fix-references)")
    args = parser.parse_args()

    stats = {"total": 0, "ok": 0, "invalid": 0, "missing_name": 0, "missing_email": 0, "missing_education": 0, "missing_skill": 0, "missing_occupation": 0, "missing_experience": 0, "in_references": 0}
    problems = []

    if not os.path.exists(args.input):
        print(f"Error: File not found: {args.input}", file=sys.stderr)
        print("Use the path to your JSONL file (e.g. llm_generated_resumes.jsonl).", file=sys.stderr)
        sys.exit(1)
    with open(args.input, "r", encoding="utf-8") as f:
        lines = f.readlines()

    out_lines = []
    for idx, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
        stats["total"] += 1
        item, issues = validate_line(line, idx, ref_strip=args.fix_references)
        if item is None:
            stats["invalid"] += 1
            problems.append((idx, issues))
            continue
        ann = item.get("annotation") or []
        if "Missing NAME" in issues:
            stats["missing_name"] += 1
        if "Missing EMAIL" in issues:
            stats["missing_email"] += 1
        if "Missing EDUCATION" in issues:
            stats["missing_education"] += 1
        if "Missing SKILL" in issues:
            stats["missing_skill"] += 1
        if not _has_label(ann, "OCCUPATION"):
            stats["missing_occupation"] += 1
        if not _has_label(ann, "EXPERIENCE"):
            stats["missing_experience"] += 1
        if "Entity in REFERENCES" in str(issues):
            stats["in_references"] += 1

        if not issues:
            stats["ok"] += 1
        else:
            problems.append((idx, issues))

        if args.output and item is not None:
            out_lines.append(json.dumps(item, ensure_ascii=False))

    # Report
    print(f"Total lines: {stats['total']}", file=sys.stderr)
    print(f"OK (no issues): {stats['ok']}", file=sys.stderr)
    if stats["invalid"]:
        print(f"Invalid JSON: {stats['invalid']}", file=sys.stderr)
    if stats["missing_name"]:
        print(f"Missing NAME: {stats['missing_name']}", file=sys.stderr)
    if stats["missing_email"]:
        print(f"Missing EMAIL: {stats['missing_email']}", file=sys.stderr)
    if stats["missing_education"]:
        print(f"Missing EDUCATION: {stats['missing_education']}", file=sys.stderr)
    if stats["missing_skill"]:
        print(f"Missing SKILL: {stats['missing_skill']}", file=sys.stderr)
    if stats["missing_occupation"]:
        print(f"Missing OCCUPATION: {stats['missing_occupation']}", file=sys.stderr)
    if stats["missing_experience"]:
        print(f"Missing EXPERIENCE: {stats['missing_experience']}", file=sys.stderr)
    if stats["in_references"]:
        print(f"Entity in REFERENCES: {stats['in_references']}", file=sys.stderr)

    if problems and len(problems) <= 20:
        for idx, issues in problems[:20]:
            print(f"  Line {idx}: {'; '.join(issues)}", file=sys.stderr)
    elif problems:
        print(f"  First 20 problem lines shown above; {len(problems)} total.", file=sys.stderr)

    if args.output and out_lines:
        with open(args.output, "w", encoding="utf-8") as f:
            for ln in out_lines:
                f.write(ln + "\n")
        print(f"Wrote {len(out_lines)} lines to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
