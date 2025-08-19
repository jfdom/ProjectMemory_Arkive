from pathlib import Path
def repo_root(start: Path=None):
    p=(start or Path(__file__)).resolve()
    for _ in range(12):
        if (p/'.git').exists(): return p
        if p.parent==p: break
        p=p.parent
    return Path.cwd()
REPO_ROOT = repo_root()
#!/usr/bin/env python3
"""
split_kjv_symbolic.py — Split KJV into 47 symbolic blocks (34×888, 13×70) with mirrored 70s.
Writes files **directly into PARSED_SCROLLS** (no extra subfolders).

Names:
  KJV_1_888.txt, KJV_2_888.txt, ..., KJV_6_70.txt, ..., KJV_47_888.txt

Usage (preferred, from your PARSED_SCROLLS artifacts):
  python3 split_kjv_symbolic.py --src KJV/PARSED_SCROLLS/kjv_verses.jsonl

Also works from the raw .txt (if you haven't parsed yet):
  python3 split_kjv_symbolic.py --src KJV/YourBibleFile.txt

By default, outputs go to:
  <SRC_DIR>/PARSED_SCROLLS
You may override with --outdir KJV/PARSED_SCROLLS
"""

import sys, json, re, argparse
from pathlib import Path

POSITIONS_70 = {6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42}
TOTAL_CHUNKS = 47
SIZES = [ (70 if (i in POSITIONS_70) else 888) for i in range(1, TOTAL_CHUNKS+1) ]
EXPECTED_TOTAL = sum(SIZES)  # 31102

# Patterns for raw .txt lines
PAT_TAB = re.compile(r'^([1-3]?\s?[A-Za-z][A-Za-z ]+?)\s+(\d+):(\d+)\t(.*)$')
PAT_SP  = re.compile(r'^([1-3]?\s?[A-Za-z][A-Za-z ]+?)\s+(\d+):(\d+)\s+(.*\S.*)$')

def gather_lines_from_jsonl(p: Path):
    out = []
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            out.append(f"{obj['book']} {obj['chapter']}:{obj['verse']}\t{obj['text']}")
    return out

def gather_lines_from_txt(p: Path):
    out = []
    with p.open("r", encoding="utf-8", errors="ignore") as f:
        for raw in f:
            ln = raw.rstrip("\n").strip()
            if not ln:
                continue
            m = PAT_TAB.match(ln) or PAT_SP.match(ln)
            if m:
                book, ch, vs, text = m.groups()
                book = re.sub(r"\s+", " ", book.strip())
                out.append(f"{book} {int(ch)}:{int(vs)}\t{text.strip()}")
            # else skip headers or non-verse lines
    return out

def decide_outdir(src: Path, user_outdir: str|None):
    if user_outdir:
        return Path(user_outdir).expanduser().resolve()
    # If src is already inside a PARSED_SCROLLS folder, use that folder
    if src.parent.name == "PARSED_SCROLLS":
        return src.parent.resolve()
    # Otherwise, place next to src under PARSED_SCROLLS
    return (src.parent / "PARSED_SCROLLS").resolve()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="Path to kjv_verses.jsonl (preferred) or raw KJV .txt")
    ap.add_argument("--outdir", help="Output directory; defaults to <SRC_DIR>/PARSED_SCROLLS")
    args = ap.parse_args()

    src = Path(args.src).expanduser().resolve()
    if not src.exists():
        print(f"Source not found: {src}", file=sys.stderr)
        sys.exit(2)

    outdir = decide_outdir(src, args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    # Collect verse lines
    if src.suffix.lower() == ".jsonl":
        lines = gather_lines_from_jsonl(src)
    else:
        lines = gather_lines_from_txt(src)

    total = len(lines)
    if total < EXPECTED_TOTAL:
        print(f"Warning: Only {total} verse lines found; expected at least {EXPECTED_TOTAL}. Output will truncate final chunk.", file=sys.stderr)
    elif total > EXPECTED_TOTAL:
        print(f"Note: Found {total} lines; expected {EXPECTED_TOTAL}. Extra lines will be ignored.", file=sys.stderr)

    # Split and write named files
    idx = 0
    start = 0
    manifest = []
    for size in SIZES:
        idx += 1
        end = start + size
        chunk = lines[start:end]
        # Build filename
        tag = "70" if idx in POSITIONS_70 else "888"
        fname = f"KJV_{idx}_{tag}.txt"
        outpath = outdir / fname
        outpath.write_text("\n".join(chunk), encoding="utf-8")
        manifest.append({"index": idx, "size": size, "tag": tag, "file": str(outpath)})
        start = end

    # Write manifest for reference
    (outdir / "KJV_SYMBOLIC_MANIFEST.json").write_text(json.dumps({
        "source": str(src),
        "outdir": str(outdir),
        "total_input_lines": total,
        "expected_total": EXPECTED_TOTAL,
        "chunk_count": TOTAL_CHUNKS,
        "positions_70": sorted(POSITIONS_70),
        "chunks": manifest
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Wrote {len(manifest)} files into {outdir}")
    print("Example:", manifest[0]["file"])

if __name__ == "__main__":
    main()
