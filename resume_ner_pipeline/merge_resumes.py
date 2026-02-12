#!/usr/bin/env python3
"""
Merge existing merged_resume_ner.json (JSONL) with LLM-generated llm_generated_resumes.jsonl.
Output: merged_resume_ner_with_llm.json (JSONL) for use in the training notebook.

Usage:
  python merge_resumes.py
  python merge_resumes.py --existing merged_resume_ner.json --llm llm_generated_resumes.jsonl --output merged_resume_ner_with_llm.json
"""

import argparse
import os
import sys


def count_lines(path: str) -> int:
    with open(path, "r", encoding="utf-8") as f:
        return sum(1 for line in f if line.strip())


def main():
    p = argparse.ArgumentParser(description="Merge existing resume JSONL with LLM-generated JSONL")
    p.add_argument("--existing", default="merged_resume_ner.json", help="Existing merged JSONL file")
    p.add_argument("--llm", default="llm_generated_resumes.jsonl", help="LLM-generated JSONL file")
    p.add_argument("--output", default="merged_resume_ner_with_llm.json", help="Output merged JSONL file")
    args = p.parse_args()

    if not os.path.exists(args.existing):
        print(f"Error: {args.existing} not found.", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(args.llm):
        print(f"Error: {args.llm} not found.", file=sys.stderr)
        sys.exit(1)

    n_existing = count_lines(args.existing)
    n_llm = count_lines(args.llm)

    with open(args.existing, "r", encoding="utf-8") as f_ex, open(args.llm, "r", encoding="utf-8") as f_llm, open(
        args.output, "w", encoding="utf-8"
    ) as f_out:
        for line in f_ex:
            if line.strip():
                f_out.write(line.rstrip("\n") + "\n")
        for line in f_llm:
            if line.strip():
                f_out.write(line.rstrip("\n") + "\n")

    total = count_lines(args.output)
    print(f"Merged: {n_existing} (existing) + {n_llm} (LLM) = {total} resumes → {args.output}")


if __name__ == "__main__":
    main()
