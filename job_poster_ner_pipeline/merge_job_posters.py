#!/usr/bin/env python3
"""
Merge existing job poster JSONL (e.g. SkillSpan) with LLM-generated job postings.
Output: merged JSONL for use in the training notebook.

Usage:
  python merge_job_posters.py --existing skillspan_job_poster.jsonl --llm llm_generated_job_postings.jsonl --output merged_job_poster_ner.json
  python merge_job_posters.py --existing merged_job_poster_ner.json --llm llm_sri_lanka_jobs.jsonl --output merged_job_poster_ner_with_llm.json
"""

import argparse
import json
import os
import sys

# Reuse label mapping from prepare_data
JOB_POSTER_LABEL_MAP = {
    "JOB_TITLE": "JOB_TITLE", "COMPANY": "COMPANY", "LOCATION": "LOCATION", "SALARY": "SALARY",
    "SKILLS_REQUIRED": "SKILLS_REQUIRED", "EXPERIENCE_REQUIRED": "EXPERIENCE_REQUIRED",
    "EDUCATION_REQUIRED": "EDUCATION_REQUIRED", "JOB_TYPE": "JOB_TYPE", "O": "O",
    "Job Title": "JOB_TITLE", "Company": "COMPANY", "Location": "LOCATION", "Salary": "SALARY",
    "Skill": "SKILLS_REQUIRED", "Occupation": "JOB_TITLE", "Qualification": "EDUCATION_REQUIRED",
}


def normalize_annotations(item: dict) -> None:
    """Apply label mapping. Mutates item."""
    for ann in item.get("annotation", []):
        labels = ann.get("label") or []
        ann["label"] = [JOB_POSTER_LABEL_MAP.get(str(l).strip(), "O") for l in labels]


def count_lines(path: str) -> int:
    with open(path, "r", encoding="utf-8") as f:
        return sum(1 for line in f if line.strip())


def main():
    p = argparse.ArgumentParser(description="Merge existing job poster JSONL with LLM-generated JSONL")
    p.add_argument("--existing", required=True, help="Existing job poster JSONL (e.g. skillspan_job_poster.jsonl)")
    p.add_argument("--llm", required=True, help="LLM-generated job postings JSONL")
    p.add_argument("--output", default="merged_job_poster_ner_with_llm.json", help="Output merged JSONL file")
    args = p.parse_args()

    for pth in [args.existing, args.llm]:
        if not os.path.exists(pth):
            print(f"Error: {pth} not found.", file=sys.stderr)
            sys.exit(1)

    n_existing = count_lines(args.existing)
    n_llm = count_lines(args.llm)

    out_dir = os.path.dirname(os.path.abspath(args.output))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    valid = 0
    with open(args.output, "w", encoding="utf-8") as f_out:
        for path in [args.existing, args.llm]:
            with open(path, "r", encoding="utf-8") as f_in:
                for line in f_in:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        item = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if not isinstance(item, dict) or "content" not in item:
                        continue
                    if "annotation" not in item or not item["annotation"]:
                        continue
                    normalize_annotations(item)
                    f_out.write(json.dumps(item, ensure_ascii=False) + "\n")
                    valid += 1

    print(f"Merged: {n_existing} (existing) + {n_llm} (LLM) → {valid} job postings → {args.output}")


if __name__ == "__main__":
    main()
