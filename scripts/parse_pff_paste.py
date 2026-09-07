#!/usr/bin/env python3
"""Parse a PFF team-grades page copy-paste into a clean CSV.

Expected paste shape (mobile/web copy): a ranked list of player names first
(with rank numbers on their own lines), then one stat block per player in the
same order, each starting with '# <jersey>'.

Column mapping (verified against ARZ 2025 offense paste; confirm per table):
  # jersey, POS, G, total snaps, snapA, snapB, snapC, snapD,
  OFF grade, PASS/RECV grade, RUN-BLOCK grade, RUSH grade, PASS-BLOCK grade,
  penalties as 'N (M)'
Snap splits (offense): A=pass routes/dropbacks, B=pass-block (OL) or run-block-ish,
  C=rush attempts, D=run-block snaps. Positions use the facets that apply; '-'
  means not applicable.

Usage: parse_pff_paste.py <raw.txt> <out.csv> <team> <season> <side>
"""
import sys, csv, re

raw, out, team, season, side = sys.argv[1:6]
lines = [l.strip() for l in open(raw, encoding="utf-8") if l.strip()]

names, stats, i = [], [], 0
# names section: skip header labels and pure rank numbers until first '# NN'
while i < len(lines) and not re.match(r"^#\s*\d+$", lines[i]):
    l = lines[i]
    if not re.match(r"^\d+$", l) and l.lower() not in ("key",) and not l.endswith("- Offense") and not l.endswith("- Defense"):
        names.append(l)
    i += 1
# stat blocks: '# NN' then POS then 12 fields
while i < len(lines):
    if re.match(r"^#\s*\d+$", lines[i]):
        block = [lines[i].lstrip("# ").strip()]
        i += 1
        while i < len(lines) and not re.match(r"^#\s*\d+$", lines[i]):
            block.append(lines[i]); i += 1
        stats.append(block)
    else:
        i += 1

assert len(names) >= len(stats), f"{len(names)} names vs {len(stats)} stat rows"
cols = ["player","team","season","side","jersey","pos","games","snaps",
        "snap_a","snap_b","snap_c","snap_d",
        "grade_off_def","grade_pass_recv","grade_runblock_rundef","grade_rush_passrush",
        "grade_passblock_cov","penalties"]
with open(out, "w", newline="") as f:
    w = csv.writer(f); w.writerow(cols)
    for name, b in zip(names, stats):
        b = (b + [""] * 14)[:14]
        w.writerow([name, team, season, side] + b)
print(f"parsed {len(stats)} players -> {out}")
