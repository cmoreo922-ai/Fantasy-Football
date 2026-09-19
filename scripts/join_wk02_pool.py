#!/usr/bin/env python3
"""Join Week 2 DK salaries to 2026 PFF grades (current season, not 2025)."""
import csv, os, glob, collections

SAL="data/2026-wk02-DKSalaries.csv"
grades={}
for f in glob.glob("data/pff/2026/parsed/wk0*-*-offense.csv"):
    for r in csv.DictReader(open(f)):
        grades[r["player"]] = r          # later files overwrite; fine (wk02 > wk01)

rows=[r for r in csv.DictReader(open(SAL,encoding="utf-8-sig"))
      if r["Status"] not in ("OUT","IR","D")]

IMPLIED={"DAL":27.25,"WAS":23.25,"CHI":26.75,"MIN":21.75,"HOU":25.5,"CIN":23,
         "BAL":27.5,"NO":20,"DEN":24,"JAX":21.5,"GB":24.5,"NYJ":20,"SF":28.5,
         "MIA":16,"CAR":23,"ATL":20.5,"LAC":25,"LV":18.5,"TB":25,"CLE":16.5,
         "NE":23.5,"PIT":18,"SEA":22.5,"ARI":18.5,"PHI":23.25,"TEN":16.25}

out=[]
for r in rows:
    g=grades.get(r["Name"])
    out.append(dict(name=r["Name"], pos=r["Position"], sal=int(r["Salary"]),
                    team=r["TeamAbbrev"], avg=r["AvgPointsPerGame"], q=r["Status"]=="Q",
                    imp=IMPLIED.get(r["TeamAbbrev"],0),
                    off=g["grade_off"] if g else "", snaps=g["snaps_total"] if g else "",
                    run=g["snaps_run"] if g else "", pas=g["snaps_pass"] if g else ""))
for pos in ["QB","RB","WR","TE"]:
    print(f"\n=== {pos} (implied-total sorted, salary >= 3500) ===")
    sel=[x for x in out if x["pos"]==pos and x["sal"]>=3500]
    sel.sort(key=lambda x:(-x["imp"], -x["sal"]))
    for x in sel[:26]:
        qq=" Q" if x["q"] else "  "
        print(f" {x['team']:4s} imp{x['imp']:>5.1f} ${x['sal']:>5} {x['name']:24s}{qq} avg {x['avg']:>5s} | wk1 off {x['off']:>5s} snaps {x['snaps']:>4s} run {x['run']:>3s} pass {x['pas']:>3s}")
