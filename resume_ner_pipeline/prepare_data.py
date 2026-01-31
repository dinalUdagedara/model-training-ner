#!/usr/bin/env python3
"""
Merge existing resume NER JSON (220) with Dotin dataset (545) and output
a single JSONL file for the BERT-BiLSTM-CRF notebook.

Dotin labels (12) are mapped to unified labels: NAME, EMAIL, SKILL, OCCUPATION,
EDUCATION, EXPERIENCE, O.

Usage:
  python prepare_data.py --existing ../entity_recognition_in_resumes.json \\
                        --dotin path/to/dotin_extracted \\
                        --output merged_resume_ner.json
  # Or use Dotin only:
  python prepare_data.py --dotin path/to/dotin_extracted --output merged_resume_ner.json
"""

import argparse
import glob
import html
import json
import os
import re

# Dotin 12 entities -> unified 6 entity types + O (same as notebook LABEL_MAPPING)
DOTIN_TO_UNIFIED = {
    "Name": "NAME",
    "Email Address": "EMAIL",
    "Designation": "OCCUPATION",
    "Degree": "EDUCATION",
    "College Name": "EDUCATION",
    "Graduation Year": "EDUCATION",
    "Company": "EXPERIENCE",
    "Companies worked at": "EXPERIENCE",
    "Years of Experience": "EXPERIENCE",
    "Job Specific Skill": "SKILL",
    "Job Specific Skills": "SKILL",   # XML uses this variant
    "Soft Skills": "SKILL",
    "Tech Tools": "SKILL",
    "Skills": "SKILL",
    "Location": "O",
    "UNKNOWN": "O",
}

# Match <label type="...">...</label> (inner text can span lines)
LABEL_PATTERN = re.compile(r'<label\s+type="([^"]+)"\s*>([\s\S]*?)</label>', re.IGNORECASE)


def read_jsonl(path: str) -> list[dict]:
    """Read JSONL: one JSON object per line."""
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def normalize_annotations(item: dict, label_map: dict) -> dict:
    """Apply label mapping to annotation labels. Mutates item."""
    for ann in item.get("annotation", []):
        labels = ann.get("label") or []
        ann["label"] = [label_map.get(str(l).strip(), "O") for l in labels]
    return item


def _xml_to_item(xml_str: str) -> dict | None:
    """Convert one Dotin XML string to {content, annotation} format."""
    # Strip root <cv>...</cv> for parsing (we work on inner content)
    inner = re.sub(r'^\s*<\?xml[\s\S]*?\?>\s*', '', xml_str.strip())
    inner = re.sub(r'^\s*<cv>\s*', '', inner)
    inner = re.sub(r'\s*</cv>\s*$', '', inner)
    content_parts = []
    annotations = []
    last_end = 0
    for m in LABEL_PATTERN.finditer(inner):
        content_parts.append(inner[last_end : m.start()])
        start = sum(len(p) for p in content_parts)
        text = html.unescape(m.group(2))
        content_parts.append(text)
        end = sum(len(p) for p in content_parts)
        annotations.append({
            "label": [m.group(1).strip()],
            "points": [{"start": start, "end": end, "text": text}],
        })
        last_end = m.end()
    content_parts.append(inner[last_end:])
    content = "".join(content_parts)
    content = html.unescape(content)
    if not content.strip():
        return None
    return {"content": content, "annotation": annotations, "extras": None}


def load_dotin_xml(path: str) -> list[dict]:
    """Load Dotin from XML file(s). path = single .xml file or directory of .xml files."""
    out = []
    if os.path.isfile(path) and path.lower().endswith(".xml"):
        with open(path, "r", encoding="utf-8") as f:
            item = _xml_to_item(f.read())
        if item:
            out.append(item)
        return out
    if os.path.isdir(path):
        for fp in sorted(glob.glob(os.path.join(path, "*.xml"))):
            with open(fp, "r", encoding="utf-8") as f:
                item = _xml_to_item(f.read())
            if item:
                out.append(item)
        return out
    return out


def load_dotin(path: str) -> list[dict]:
    """
    Load Dotin data. path can be:
    - A directory of .xml files (Dotin zip format) -> parsed to content + annotations
    - A .xml file -> single resume
    - A .json file or directory of .json -> JSONL/JSON (legacy)
    """
    # Prefer XML if path is dir with .xml or path is .xml
    if os.path.isdir(path):
        xml_files = glob.glob(os.path.join(path, "*.xml"))
        if xml_files:
            return load_dotin_xml(path)
    if os.path.isfile(path) and path.lower().endswith(".xml"):
        return load_dotin_xml(path)

    # JSON fallback
    out = []
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read().strip()
        for line in raw.split("\n"):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                if isinstance(obj, dict) and "content" in obj:
                    out.append(obj)
            except json.JSONDecodeError:
                pass
        if not out:
            try:
                data = json.loads(raw)
                if isinstance(data, list):
                    out = [x for x in data if isinstance(x, dict) and "content" in x]
                elif isinstance(data, dict) and "content" in data:
                    out = [data]
            except json.JSONDecodeError:
                pass
        return out
    if os.path.isdir(path):
        for fp in sorted(glob.glob(os.path.join(path, "**", "*.json"), recursive=True)):
            out.extend(load_dotin(fp))
        return out
    return out


def main():
    p = argparse.ArgumentParser(description="Merge existing + Dotin resume NER data")
    p.add_argument("--existing", default="", help="Path to entity_recognition_in_resumes.json (optional)")
    p.add_argument("--dotin", default="", help="Path to Dotin train XML/JSON (e.g. 545_cvs_train_v2/)")
    p.add_argument("--dotin-test", default="", dest="dotin_test", help="Path to Dotin test set (e.g. set_aside_test_v2_50cvs/)")
    p.add_argument("--output", default="merged_resume_ner.json", help="Output JSONL path")
    args = p.parse_args()

    if not args.existing and not args.dotin:
        p.error("Provide at least one of --existing or --dotin")

    all_items = []

    if args.existing and os.path.exists(args.existing):
        existing = read_jsonl(args.existing)
        # Existing file already uses labels that match our unified set; notebook applies LABEL_MAPPING
        # which includes "Skills" -> SKILL, "Companies worked at" -> EXPERIENCE, etc. So we only need
        # to ensure annotation format is correct. No change needed for existing.
        for item in existing:
            normalize_annotations(item, {
                **DOTIN_TO_UNIFIED,
                "Name": "NAME", "Email Address": "EMAIL", "Skills": "SKILL", "Designation": "OCCUPATION",
                "Degree": "EDUCATION", "College Name": "EDUCATION", "Graduation Year": "EDUCATION",
                "Companies worked at": "EXPERIENCE", "Years of Experience": "EXPERIENCE", "Location": "O", "UNKNOWN": "O",
            })
            all_items.append(item)
        print(f"Loaded {len(existing)} resumes from existing file")
    else:
        if args.existing:
            print(f"Warning: --existing path not found: {args.existing}")

    if args.dotin and os.path.exists(args.dotin):
        dotin = load_dotin(args.dotin)
        for item in dotin:
            normalize_annotations(item, DOTIN_TO_UNIFIED)
            all_items.append(item)
        print(f"Loaded {len(dotin)} resumes from Dotin (train)")

    if getattr(args, "dotin_test", None) and os.path.exists(args.dotin_test):
        dotin_test = load_dotin(args.dotin_test)
        for item in dotin_test:
            normalize_annotations(item, DOTIN_TO_UNIFIED)
            all_items.append(item)
        print(f"Loaded {len(dotin_test)} resumes from Dotin (test set)")
    else:
        if getattr(args, "dotin_test", None):
            print(f"Warning: --dotin-test path not found: {args.dotin_test}")

    os.makedirs(os.path.dirname(os.path.abspath(args.output)) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        for item in all_items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(f"Wrote {len(all_items)} resumes to {args.output}")


if __name__ == "__main__":
    main()
