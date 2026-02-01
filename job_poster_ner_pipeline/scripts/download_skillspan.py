#!/usr/bin/env python3
"""
Download SkillSpan dataset (NAACL 2022) and convert to job poster NER JSONL format.

SkillSpan: https://github.com/larkinbb/skillspan
- 14.5K sentences, 12.5K+ spans, English job postings
- Tags: tags_skill (B/I/O), tags_knowledge (B/I/O)
- We map both to SKILLS_REQUIRED for the pipeline.

Usage:
  python download_skillspan.py --out skillspan_job_poster.jsonl
  # Then: python prepare_data.py --input skillspan_job_poster.jsonl --output merged_job_poster_ner.json
"""

import argparse
import json
import os
import urllib.request

BASE = "https://raw.githubusercontent.com/larkinbb/skillspan/main/data/json"
FILES = ["train.json", "dev.json", "test.json"]


def bio_to_spans(tokens: list, tags: list, label: str) -> list:
    """Convert BIO tag sequence to list of {label, points} spans. tags are 'B','I','O'."""
    if not tokens or len(tokens) != len(tags):
        return []
    # Build content and char offsets
    parts = []
    offsets = []  # (start, end) per token
    pos = 0
    for t in tokens:
        start = pos
        text = t if isinstance(t, str) else str(t)
        parts.append(text)
        pos += len(text) + 1  # +1 for space
        offsets.append((start, start + len(text)))
    content = " ".join(parts)
    # Recompute offsets: our content has single space between tokens
    offsets = []
    pos = 0
    for i, t in enumerate(tokens):
        start = pos
        text = t if isinstance(t, str) else str(t)
        end = start + len(text)
        offsets.append((start, end))
        pos = end + 1 if i < len(tokens) - 1 else end
    # Extract spans
    spans = []
    i = 0
    while i < len(tags):
        if tags[i] == "B":
            start, end = offsets[i]
            j = i + 1
            while j < len(tags) and tags[j] == "I":
                end = offsets[j][1]
                j += 1
            text = content[start:end]
            spans.append({"label": [label], "points": [{"start": start, "end": end, "text": text}]})
            i = j
        else:
            i += 1
    return spans


def convert_line(obj: dict) -> dict | None:
    """Convert one SkillSpan JSON line to our JSONL item (content + annotation)."""
    tokens = obj.get("tokens") or []
    if not tokens:
        return None
    tags_skill = obj.get("tags_skill") or []
    tags_knowledge = obj.get("tags_knowledge") or []
    # Pad to same length
    n = len(tokens)
    while len(tags_skill) < n:
        tags_skill.append("O")
    while len(tags_knowledge) < n:
        tags_knowledge.append("O")
    tags_skill = tags_skill[:n]
    tags_knowledge = tags_knowledge[:n]
    content = " ".join(t if isinstance(t, str) else str(t) for t in tokens)
    annotation = []
    annotation.extend(bio_to_spans(tokens, tags_skill, "SKILLS_REQUIRED"))
    annotation.extend(bio_to_spans(tokens, tags_knowledge, "SKILLS_REQUIRED"))
    if not annotation:
        return {"content": content, "annotation": []}
    return {"content": content, "annotation": annotation}


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "JobPosterNER/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8")


def main():
    p = argparse.ArgumentParser(description="Download SkillSpan and convert to job poster JSONL")
    p.add_argument("--out", default="skillspan_job_poster.jsonl", help="Output JSONL path")
    p.add_argument("--dir", default=None, help="Output directory (default: same as script)")
    args = p.parse_args()
    out_path = args.out
    if args.dir:
        os.makedirs(args.dir, exist_ok=True)
        out_path = os.path.join(args.dir, os.path.basename(args.out))
    else:
        os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".", exist_ok=True)

    total = 0
    with open(out_path, "w", encoding="utf-8") as f:
        for name in FILES:
            url = f"{BASE}/{name}"
            print(f"Fetching {url} ...")
            try:
                raw = fetch(url)
            except Exception as e:
                print(f"Warning: could not fetch {url}: {e}")
                continue
            count = 0
            for line in raw.strip().split("\n"):
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    item = convert_line(obj)
                    if item:
                        f.write(json.dumps(item, ensure_ascii=False) + "\n")
                        count += 1
                except json.JSONDecodeError:
                    continue
            print(f"  {name}: {count} sentences")
            total += count
    print(f"Wrote {total} sentences to {out_path}")
    print("Next: python prepare_data.py --input", out_path, "--output merged_job_poster_ner.json")


if __name__ == "__main__":
    main()
