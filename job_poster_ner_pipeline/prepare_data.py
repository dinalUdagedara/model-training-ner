#!/usr/bin/env python3
"""
Merge job poster NER JSONL into a single file for the BERT-BiLSTM-CRF job poster notebook.

Unified labels: JOB_TITLE, COMPANY, LOCATION, SALARY, SKILLS_REQUIRED, EXPERIENCE_REQUIRED,
EDUCATION_REQUIRED, JOB_TYPE, O.

Usage:
  python prepare_data.py --input job_postings.jsonl --output merged_job_poster_ner.json
  python prepare_data.py --input data/ --output merged_job_poster_ner.json
"""

import argparse
import glob
import json
import os

# Map common label names to unified job-poster entity types
JOB_POSTER_LABEL_MAP = {
    # Canonical
    "JOB_TITLE": "JOB_TITLE",
    "COMPANY": "COMPANY",
    "LOCATION": "LOCATION",
    "SALARY": "SALARY",
    "SKILLS_REQUIRED": "SKILLS_REQUIRED",
    "EXPERIENCE_REQUIRED": "EXPERIENCE_REQUIRED",
    "EDUCATION_REQUIRED": "EDUCATION_REQUIRED",
    "JOB_TYPE": "JOB_TYPE",
    "O": "O",
    # Variants
    "Job Title": "JOB_TITLE",
    "job_title": "JOB_TITLE",
    "title": "JOB_TITLE",
    "Company": "COMPANY",
    "company": "COMPANY",
    "Employer": "COMPANY",
    "Location": "LOCATION",
    "location": "LOCATION",
    "Salary": "SALARY",
    "salary": "SALARY",
    "Pay": "SALARY",
    "Skills": "SKILLS_REQUIRED",
    "Skill": "SKILLS_REQUIRED",
    "Skills Required": "SKILLS_REQUIRED",
    "Experience": "EXPERIENCE_REQUIRED",
    "Experience Required": "EXPERIENCE_REQUIRED",
    "Education": "EDUCATION_REQUIRED",
    "Education Required": "EDUCATION_REQUIRED",
    "Qualification": "EDUCATION_REQUIRED",
    "Qualifications": "EDUCATION_REQUIRED",
    "Job Type": "JOB_TYPE",
    "job_type": "JOB_TYPE",
    "Employment Type": "JOB_TYPE",
    # LREC 2022 job description corpus (Skill, Qualification, Experience, Occupation, Domain)
    "Occupation": "JOB_TITLE",
    "Domain": "O",
}


def normalize_annotations(item: dict, label_map: dict) -> dict:
    """Apply label mapping to annotation labels. Mutates item."""
    for ann in item.get("annotation", []):
        labels = ann.get("label") or []
        ann["label"] = [label_map.get(str(l).strip(), "O") for l in labels]
    return item


def read_jsonl(path: str) -> list[dict]:
    """Read JSONL: one JSON object per line."""
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return out


def load_input(path: str) -> list[dict]:
    """Load from a single JSONL file or a directory of JSONL files."""
    if os.path.isfile(path):
        if path.lower().endswith(".jsonl") or path.lower().endswith(".json"):
            return read_jsonl(path)
        return []
    if os.path.isdir(path):
        all_items = []
        for fp in sorted(glob.glob(os.path.join(path, "**", "*.jsonl"), recursive=True)) + sorted(
            glob.glob(os.path.join(path, "**", "*.json"), recursive=True)
        ):
            all_items.extend(read_jsonl(fp))
        return all_items
    return []


def main():
    p = argparse.ArgumentParser(description="Merge job poster NER JSONL into one file")
    p.add_argument("--input", default="", help="Path to JSONL file or directory of JSONL files")
    p.add_argument("--existing", default="", dest="existing", help="Alias for --input")
    p.add_argument("--output", default="merged_job_poster_ner.json", help="Output JSONL path")
    args = p.parse_args()

    input_path = args.input or args.existing
    if not input_path:
        p.error("Provide --input (or --existing) path to JSONL file or directory")
    if not os.path.exists(input_path):
        p.error(f"Path not found: {input_path}")

    items = load_input(input_path)
    if not items:
        print("No valid JSONL items found.")
        return

    for item in items:
        if not isinstance(item, dict) or "content" not in item:
            continue
        if "annotation" not in item or not item["annotation"]:
            continue
        normalize_annotations(item, JOB_POSTER_LABEL_MAP)

    valid = [x for x in items if isinstance(x, dict) and x.get("content") and "annotation" in x]
    out_dir = os.path.dirname(os.path.abspath(args.output))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        for item in valid:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(f"Loaded {len(items)} items, wrote {len(valid)} job postings to {args.output}")


if __name__ == "__main__":
    main()
