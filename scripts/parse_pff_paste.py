#!/usr/bin/env python3
"""Parse a PFF team-grades page copy-paste into a clean CSV.

Expected paste shape (mobile/web copy): a ranked list of player names first
(with rank numbers on their own lines), then one stat block per player in the
same order, each starting with '# <jersey>'.

Column key (VERIFIED by Chris against PFF's own legend, offense table):
  #, POS, #G, TOT, PASS (pass-play snaps), PBLK (pass-block snaps),
  RUN (run-play snaps), RBLK (run-block snaps),
  OFF, PASS, PBLK, RUN, RBLK grades, PEN as 'Total (Declined+Offset)'.
'-' = facet not applicable to that player.

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
META = ["player", "team", "season", "side"]
OFF_COLS = ["jersey","pos","games","snaps_total",
            "snaps_pass","snaps_passblock","snaps_run","snaps_runblock",
            "grade_off","grade_pass","grade_passblock","grade_run","grade_runblock",
            "penalties"]
# Defense key verified by Chris against PFF's legend (order as displayed).
DEF_COLS = ["jersey","pos","games","snaps_total",
            "snaps_rundef","snaps_passrush","snaps_coverage",
            "grade_def","grade_rundef","grade_tackling","grade_passrush","grade_coverage",
            "pressures","sacks","qb_hits","hurries","batted",
            "tackles","assists","missed_tackles","missed_tackle_pct","stops","forced_fumbles",
            "targets","receptions","rec_pct","yards","yards_per_rec","yac","longest",
            "tds_allowed","ints","pass_breakups","passer_rating_against",
            "penalties","align_dl","align_box","align_fs","align_slot","align_corner",
            "align_nt","align_dt","align_over_ot","align_outside_ot"]
cols = DEF_COLS if side.lower().startswith("def") else OFF_COLS
PEN_IDX = cols.index("penalties")
pen_pat = re.compile(r"^\d+ \(\d+\)$")

def align(b):
    """Anchor on the penalties field ('N (M)') — rows for players with no
    coverage stats are shortened in PFF's copy, so pad zeros before PEN and
    pad/truncate the alignment tail after it."""
    p = next((i for i, x in enumerate(b) if pen_pat.match(x)), None)
    if p is None:
        return (b + [""] * len(cols))[:len(cols)]
    head = b[:p] + ["0"] * (PEN_IDX - p) if p < PEN_IDX else b[:PEN_IDX]
    tail = b[p + 1:] if p < PEN_IDX else b[p:][1:]
    pen = b[p]
    tail = (tail + ["0"] * (len(cols) - PEN_IDX - 1))[:len(cols) - PEN_IDX - 1]
    return head + [pen] + tail

with open(out, "w", newline="") as f:
    w = csv.writer(f); w.writerow(META + cols)
    for name, b in zip(names, stats):
        w.writerow([name, team, season, side] + align(b))
print(f"parsed {len(stats)} players x {len(cols)} fields -> {out}")
