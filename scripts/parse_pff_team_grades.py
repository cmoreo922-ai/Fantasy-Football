#!/usr/bin/env python3
"""Parse a PFF *team* grades page paste into CSV.

Paste shape: 32 team names (alphabetical), then one block per team in the same
order: "W - L", points-for, points-against, 13 grades, "Team Reports".

COLUMN ORDER IS CLAUDE'S READ, NOT CONFIRMED BY CHRIS — verify against the
page header before trusting individual facets (we mis-ordered PBLK/RBLK once
on the 2025 player tables).

Usage: parse_pff_team_grades.py <raw.txt> <out.csv> <season> <through>
"""
import sys, csv, re

raw, out, season, through = sys.argv[1:5]
lines = [l.strip() for l in open(raw, encoding="utf-8") if l.strip()]

rec = re.compile(r"^\d+\s*-\s*\d+$")
split = next(i for i, l in enumerate(lines) if rec.match(l))
teams = lines[:split]
rest = [l for l in lines[split:] if l != "Team Reports"]

GRADES = ["grade_overall", "grade_off", "grade_pass", "grade_passblock",
          "grade_recv", "grade_run", "grade_runblock", "grade_def",
          "grade_rundef", "grade_tackling", "grade_passrush", "grade_cov",
          "grade_special"]
STRIDE = 3 + len(GRADES)          # record, PF, PA, 13 grades
assert len(rest) == len(teams) * STRIDE, f"{len(rest)} vals / {len(teams)} teams"

with open(out, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["team", "season", "through", "wins", "losses", "pf", "pa"] + GRADES)
    for i, team in enumerate(teams):
        b = rest[i * STRIDE:(i + 1) * STRIDE]
        wins, losses = [x.strip() for x in b[0].split("-")]
        w.writerow([team, season, through, wins, losses, b[1], b[2]] + b[3:])
print(f"parsed {len(teams)} teams -> {out}")
