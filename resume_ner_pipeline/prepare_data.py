#!/usr/bin/env python3
"""
Merge existing resume NER JSON (220) with Dotin (545), vrundag91, and minhquan
datasets and output a single JSONL file for the BERT-BiLSTM-CRF notebook.

All source labels are mapped to: NAME, EMAIL, SKILL, OCCUPATION, EDUCATION, EXPERIENCE, O.

Usage:
  python prepare_data.py --existing ../entity_recognition_in_resumes.json \\
                        --dotin path/to/545_cvs_train_v2 --dotin-test path/to/set_aside_test_v2_50cvs \\
                        --vrundag path/to/Resume-Corpus-Dataset/data-files \\
                        --minhquan path/to/RESUME_NER_DATASET/data \\
                        --output merged_resume_ner.json
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

# vrundag91/Resume-Corpus-Dataset (Label Studio export): 36 entities -> unified
VRUNDAG_TO_UNIFIED = {
    "candidate_city": "O", "candidate_name": "NAME", "candidate_email": "EMAIL",
    "designation": "OCCUPATION", "work_year": "EXPERIENCE", "work_cities": "O",
    "technical_skills": "SKILL", "soft-skills": "SKILL", "company_name": "EXPERIENCE",
    "higher_education": "EDUCATION", "basic_education": "EDUCATION",
    "place_basic_education": "EDUCATION", "place_higher_education": "EDUCATION",
    "certification": "EDUCATION", "analyzing": "O", "innovative": "O",
    "work_with_people": "O", "applying_expertise": "O", "adaption_to_change": "O",
    "learning": "O", "deciding": "O", "initiating_actions": "O", "persuading": "O",
    "supervising": "O", "researching": "O", "commercial_thinking": "O",
}
# minhquan/RESUME_NER_DATASET (spaCy-style): map to unified
MINHQUAN_TO_UNIFIED = {
    "PERSON_NAME": "NAME", "ADDRESS": "O", "EDUCATION": "EDUCATION", "GPA": "EDUCATION",
    "SKILL": "SKILL", "EXPERIENCE_LEVEL": "EXPERIENCE", "JOB_TITLE": "OCCUPATION",
    "DATE_BIRTH": "O", "MAJOR": "EDUCATION", "MARIAGE_STATUS": "O", "ORGANIZATION": "EXPERIENCE",
    "GENDER": "O",
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


def load_vrundag(path: str) -> list[dict]:
    """
    Load vrundag91/Resume-Corpus-Dataset (Label Studio JSON export).
    Each file is a list of tasks; each task has data.text and annotations[].result.
    """
    out = []
    files = []
    if os.path.isfile(path) and path.lower().endswith(".json"):
        files = [path]
    elif os.path.isdir(path):
        files = sorted(glob.glob(os.path.join(path, "*.json")))
    for fp in files:
        if os.path.basename(fp) == "Data.md":
            continue
        try:
            with open(fp, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue
        if not isinstance(data, list):
            data = [data] if isinstance(data, dict) else []
        try:
            for task in data:
                if not isinstance(task, dict):
                    continue
                text = (task.get("data") or {}).get("text")
                if not text or not isinstance(text, str):
                    continue
                anns = task.get("annotations") or []
                result = None
                for a in anns:
                    if isinstance(a, dict) and a.get("result"):
                        result = a["result"]
                        break
                if not result:
                    continue
                annotations = []
                for r in result:
                    if not isinstance(r, dict) or r.get("type") != "labels":
                        continue
                    v = r.get("value") or {}
                    start = v.get("start")
                    end = v.get("end")
                    labels = v.get("labels") or []
                    if start is None or end is None or not labels:
                        continue
                    lbl = VRUNDAG_TO_UNIFIED.get(str(labels[0]).strip(), "O")
                    annotations.append({
                        "label": [lbl],
                        "points": [{"start": int(start), "end": int(end), "text": v.get("text", text[int(start):int(end)])}],
                    })
                if annotations:
                    out.append({"content": text, "annotation": annotations, "extras": None})
        except Exception:
            continue
    return out


def load_minhquan(path: str) -> list[dict]:
    """
    Load minhquan23102000/RESUME_NER_DATASET (spaCy-style JSON).
    Structure: annotations = [ [text, {"entities": [[start, end, label], ...]}], ... ].
    """
    out = []
    if not os.path.isdir(path):
        return out
    for fp in sorted(glob.glob(os.path.join(path, "**", "*.json"), recursive=True)):
        try:
            with open(fp, "r", encoding="utf-8") as f:
                raw = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue
        annotations_list = raw.get("annotations") if isinstance(raw, dict) else None
        if not annotations_list:
            continue
        for entry in annotations_list:
            if not isinstance(entry, (list, tuple)) or len(entry) < 2:
                continue
            text = entry[0]
            if not isinstance(text, str):
                continue
            ent_dict = entry[1] if isinstance(entry[1], dict) else {}
            entities = ent_dict.get("entities") or []
            if not entities:
                continue
            our_annotations = []
            for ent in entities:
                if not isinstance(ent, (list, tuple)) or len(ent) < 3:
                    continue
                start, end, label = int(ent[0]), int(ent[1]), ent[2]
                if start < 0 or end > len(text):
                    continue
                lbl = MINHQUAN_TO_UNIFIED.get(str(label).strip(), "O")
                our_annotations.append({
                    "label": [lbl],
                    "points": [{"start": start, "end": end, "text": text[start:end]}],
                })
            if our_annotations:
                out.append({"content": text, "annotation": our_annotations, "extras": None})
    return out


def main():
    p = argparse.ArgumentParser(description="Merge existing + Dotin + vrundag91 + minhquan resume NER data")
    p.add_argument("--existing", default="", help="Path to entity_recognition_in_resumes.json (optional)")
    p.add_argument("--dotin", default="", help="Path to Dotin train XML/JSON (e.g. 545_cvs_train_v2/)")
    p.add_argument("--dotin-test", default="", dest="dotin_test", help="Path to Dotin test set (e.g. set_aside_test_v2_50cvs/)")
    p.add_argument("--vrundag", default="", help="Path to vrundag91/Resume-Corpus-Dataset data-files/ (optional)")
    p.add_argument("--minhquan", default="", help="Path to minhquan/RESUME_NER_DATASET data/ (optional)")
    p.add_argument("--output", default="merged_resume_ner.json", help="Output JSONL path")
    args = p.parse_args()

    if not any([args.existing, args.dotin, args.vrundag, args.minhquan]):
        p.error("Provide at least one of --existing, --dotin, --vrundag, or --minhquan")

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

    if args.vrundag and os.path.exists(args.vrundag):
        vrundag = load_vrundag(args.vrundag)
        for item in vrundag:
            normalize_annotations(item, VRUNDAG_TO_UNIFIED)
            all_items.append(item)
        print(f"Loaded {len(vrundag)} resumes from vrundag91/Resume-Corpus-Dataset")
    else:
        if args.vrundag:
            print(f"Warning: --vrundag path not found: {args.vrundag}")

    if args.minhquan and os.path.exists(args.minhquan):
        minhquan = load_minhquan(args.minhquan)
        for item in minhquan:
            normalize_annotations(item, MINHQUAN_TO_UNIFIED)
            all_items.append(item)
        print(f"Loaded {len(minhquan)} resumes from minhquan/RESUME_NER_DATASET")
    else:
        if args.minhquan:
            print(f"Warning: --minhquan path not found: {args.minhquan}")

    os.makedirs(os.path.dirname(os.path.abspath(args.output)) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        for item in all_items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(f"Wrote {len(all_items)} resumes to {args.output}")


if __name__ == "__main__":
    main()
