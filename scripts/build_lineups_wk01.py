#!/usr/bin/env python3
"""Week 1 2026 lineup builder — 5 cash + 25 GPP from the curated player pool.

Projections and ownership are Claude's rough ESTIMATES (env/role-based),
not scraped numbers. Rules enforced:
  - $49,000–$50,000 salary (cash allows $48,500+)
  - GPP: QB stacked with 1–2 same-team pass catchers; bring-back most of the time
  - No DST facing any of our own offensive players
  - Exposure caps per player across the 30-lineup portfolio
  - Every lineup differs from every other by 2+ players
  - Fades excluded entirely (Jeanty, Hubbard, Brooks, NYJ/TEN offense)
"""
import csv, random, itertools, sys
from collections import defaultdict

random.seed(2026)
SAL_PATH = "data/2026-wk01-DKSalaries.csv"

rows = {r["Name"]: r for r in csv.DictReader(open(SAL_PATH, encoding="utf-8-sig"))}
def opp(team, gi):
    a, b = gi.split(" ")[0].split("@"); return b if team == a else a

# name: (proj, own%) — Claude estimates, Sept 2026
POOL = {
 "QB": {"Jared Goff": (19.5, 12), "Joe Burrow": (21, 18), "Jalen Hurts": (20.5, 12),
        "Josh Allen": (22, 15), "Caleb Williams": (19, 8), "Justin Herbert": (18.5, 10),
        "Baker Mayfield": (18, 7), "Jayden Daniels": (20, 10), "Trevor Lawrence": (17.5, 6),
        "Daniel Jones": (16.5, 4), "Jordan Love": (17, 6)},
 "RB": {"Jahmyr Gibbs": (22, 30), "Bijan Robinson": (19, 15), "Jonathan Taylor": (18.5, 12),
        "James Cook III": (17, 10), "Chase Brown": (17, 12), "De'Von Achane": (18, 10),
        "Saquon Barkley": (16, 12), "Omarion Hampton": (17.5, 25), "Derrick Henry": (17, 14),
        "MarShawn Lloyd": (13, 45), "Bucky Irving": (14.5, 15), "Travis Etienne Jr.": (13, 8),
        "David Montgomery": (12, 6), "Quinshon Judkins": (11, 5), "Jaylen Warren": (11, 8),
        "Rico Dowdle": (11, 10), "Kenny Gainwell": (10, 4), "Tyler Allgeier": (11, 20),
        "Braelon Allen": (9, 4), "Kaleb Johnson": (8, 10), "Jordan Mason": (10.5, 5)},
 "WR": {"Ja'Marr Chase": (21, 25), "Amon-Ra St. Brown": (20, 20), "Justin Jefferson": (17, 12),
        "Nico Collins": (16, 10), "Chris Olave": (15, 8), "DeVonta Smith": (14, 8),
        "Drake London": (15, 10), "Tee Higgins": (14, 12), "Emeka Egbuka": (12, 8),
        "Tetairoa McMillan": (13, 7), "Jameson Williams": (14, 9), "Christian Watson": (12, 5),
        "Ladd McConkey": (13, 20), "Jordan Addison": (11, 5), "Terry McLaurin": (12, 8),
        "Alec Pierce": (11, 4), "DJ Moore": (13.5, 22), "Brian Thomas Jr.": (11, 6),
        "Rome Odunze": (11, 6), "Michael Wilson": (10, 5), "Chris Godwin Jr.": (11, 9),
        "Stefon Diggs": (11.5, 12), "Marvin Harrison Jr.": (10, 8), "Keon Coleman": (8, 6),
        "Tre' Harris": (7, 4), "Luther Burden III": (9, 5)},
 "TE": {"Trey McBride": (16, 12), "Brock Bowers": (15, 10), "Colston Loveland": (10, 6),
        "Kyle Pitts Sr.": (9, 6), "Dalton Kincaid": (9, 7), "Tucker Kraft": (10, 8),
        "Sam LaPorta": (10, 15), "Harold Fannin Jr.": (8, 6), "Dallas Goedert": (9.5, 12),
        "Mark Andrews": (7, 7), "Juwan Johnson": (7.5, 6)},
 "DST": {"Chargers": (9, 25), "Jaguars": (8.5, 18), "Steelers": (8, 12), "Lions": (7, 8),
         "Eagles": (7, 10), "Bills": (7, 6), "Packers": (6, 5), "Ravens": (6, 5),
         "Bears": (6.5, 15), "Texans": (6, 4)}}

P = {}  # name -> dict
for pos, d in POOL.items():
    for name, (proj, own) in d.items():
        r = rows[name]
        P[name] = dict(name=name, pos=pos, sal=int(r["Salary"]), team=r["TeamAbbrev"],
                       opp=opp(r["TeamAbbrev"], r["Game Info"]), proj=proj, own=own,
                       id=r["ID"], nid=r["Name + ID"], q=r["Status"] == "Q")

CAPS = defaultdict(lambda: 9)  # max appearances in 30
CAPS.update({"MarShawn Lloyd": 18, "Jahmyr Gibbs": 14, "DJ Moore": 7, "Omarion Hampton": 11,
             "Ja'Marr Chase": 11, "Amon-Ra St. Brown": 11, "Ladd McConkey": 10,
             "Bucky Irving": 10, "Dallas Goedert": 9, "Sam LaPorta": 8, "Tyler Allgeier": 3,
             "Tee Higgins": 7, "Emeka Egbuka": 4, "Keon Coleman": 3, "Tucker Kraft": 5,
             "Luther Burden III": 4, "Rome Odunze": 4, "Bears": 10, "Chargers": 9,
             "Jaguars": 8, "Jared Goff": 8, "Joe Burrow": 7, "Jalen Hurts": 7, "Josh Allen": 5,
             "Kenny Gainwell": 3, "Jordan Mason": 3, "Tre' Harris": 2, "Braelon Allen": 2,
             "Kaleb Johnson": 2, "Jaylen Warren": 4, "Mark Andrews": 3, "Juwan Johnson": 5, "Alec Pierce": 3,
             "Stefon Diggs": 5, "Michael Wilson": 3, "Marvin Harrison Jr.": 4,
             "DeVonta Smith": 8, "De'Von Achane": 8, "Lions": 6, "Jordan Love": 2,
             "Christian Watson": 4, "Colston Loveland": 4,
             "Terry McLaurin": 3, "David Montgomery": 4, "Saquon Barkley": 4})

# weight multiplier for portfolio core — pushes the generator toward our best plays
BOOST = defaultdict(lambda: 1.0)
BOOST.update({"MarShawn Lloyd": 4, "Jahmyr Gibbs": 4.5, "Ja'Marr Chase": 4, "Joe Burrow": 3.5,
              "Amon-Ra St. Brown": 2.5, "Omarion Hampton": 2,
              "Bucky Irving": 1.5, "Tee Higgins": 2, "Jameson Williams": 1.8,
              "Chris Olave": 1.8, "Trey McBride": 2.5, "Brock Bowers": 2,
              "Derrick Henry": 1.5, "Nico Collins": 1.5, "Chargers": 1.5, "Jaguars": 1.5,
              # PFF 2025 matchup adjustments (see weeks/2026-wk01.md matchup board)
              "DeVonta Smith": 2.2, "De'Von Achane": 3.0, "Ladd McConkey": 1.5,
              "Chase Brown": 1.4, "Lions": 3.5, "Christian Watson": 1.5,
              "Rome Odunze": 1.3, "Colston Loveland": 1.3})

# Cash rework after full PFF sweep: DJ Moore 5->2 (HOU elite secondary),
# Diggs 4->2 (PHI coverage strong), DeVonta Smith in 3 (WAS coverage worst on
# slate), McConkey in 3 (ARI slot CB smash).
CASH = [
 ["Jared Goff","Jahmyr Gibbs","MarShawn Lloyd","Amon-Ra St. Brown","DJ Moore","Stefon Diggs","Dallas Goedert","Bucky Irving","Bears"],
 ["Jalen Hurts","Omarion Hampton","MarShawn Lloyd","Amon-Ra St. Brown","DeVonta Smith","Chris Godwin Jr.","Juwan Johnson","Bucky Irving","Bears"],
 ["Josh Allen","Jahmyr Gibbs","MarShawn Lloyd","DJ Moore","Ladd McConkey","Stefon Diggs","Juwan Johnson","Omarion Hampton","Bears"],
 ["Jared Goff","Omarion Hampton","MarShawn Lloyd","Amon-Ra St. Brown","Ladd McConkey","DeVonta Smith","Juwan Johnson","Bucky Irving","Bears"],
 ["Jalen Hurts","Jahmyr Gibbs","MarShawn Lloyd","Ladd McConkey","Chris Godwin Jr.","DeVonta Smith","Dallas Goedert","Bucky Irving","Bears"],
]

use = defaultdict(int)
lineups = []

def ok_lineup(names):
    ps = [P[n] for n in names]
    sal = sum(p["sal"] for p in ps)
    if not (48500 <= sal <= 50000): return False
    dst = next(p for p in ps if p["pos"] == "DST")
    if any(p["opp"] == dst["team"] for p in ps if p["pos"] != "DST"): return False
    if len({p["team"] + p["name"] for p in ps}) != 9: return False
    s = set(names)
    return all(len(s - set(l)) >= 2 for l in lineups)

def add(names):
    lineups.append(sorted(names))
    for n in names: use[n] += 1

for lu in CASH:
    assert ok_lineup(lu), f"cash lineup invalid: {lu}"
    add(lu)

qbs = list(POOL["QB"])
def wpick(cands, k=1):
    c = [x for x in cands if use[x] < CAPS[x]]
    if len(c) < k: return None
    w = [(P[x]["proj"] / max(P[x]["sal"], 1) * 1000 + 1) * BOOST[x] for x in c]
    out = []
    for _ in range(k):
        x = random.choices(c, weights=w)[0]
        i = c.index(x); c.pop(i); w.pop(i); out.append(x)
    return out

tries = 0
while len(lineups) < 30 and tries < 200000:
    tries += 1
    qb = wpick(qbs)[0] if wpick(qbs) else None
    if not qb: continue
    q = P[qb]
    mates = [n for n, p in P.items() if p["team"] == q["team"] and p["pos"] in ("WR", "TE")]
    br = [n for n, p in P.items() if p["team"] == q["opp"] and p["pos"] in ("WR", "TE", "RB")]
    stack = wpick(mates, random.choice([1, 1, 2]))
    if not stack: continue
    names = [qb] + stack
    if random.random() < 0.75 and br:
        b = wpick(br)
        if b: names += b
    # fill remaining slots
    need = {"RB": 2, "WR": 3, "TE": 1, "DST": 1}
    for n in names[1:]:
        pp = P[n]["pos"]
        if need.get(pp, 0) > 0: need[pp] -= 1
        else: need["FLEX"] = need.get("FLEX", 0) - 1  # overflow into flex
    flex_left = 1 + need.get("FLEX", 0)
    if flex_left < 0: continue
    fill = []
    okf = True
    for pos, cnt in [("RB", need["RB"]), ("WR", need["WR"]), ("TE", need["TE"]), ("DST", 1)]:
        if cnt <= 0: continue
        got = wpick([x for x in POOL[pos] if x not in names + fill], cnt)
        if not got: okf = False; break
        fill += got
    if not okf: continue
    if flex_left == 1:
        fpos = random.choices(["RB", "WR", "TE"], weights=[5, 4, 1])[0]
        got = wpick([x for x in POOL[fpos] if x not in names + fill], 1)
        if not got: continue
        fill += got
    cand = names + fill
    if len(cand) != 9: continue
    if ok_lineup(cand): add(cand)

if len(lineups) < 30:
    sys.exit(f"only built {len(lineups)} lineups")

# ---- outputs ----
SLOTS = ["QB", "RB", "RB", "WR", "WR", "WR", "TE", "FLEX", "DST"]
def slotify(names):
    ps = sorted((P[n] for n in names), key=lambda p: -p["sal"])
    out, used = {}, []
    for slot in ["QB", "DST"]:
        p = next(p for p in ps if p["pos"] == slot); out[slot] = [p]; used.append(p["name"])
    rem = [p for p in ps if p["name"] not in used]
    out["RB"] = [p for p in rem if p["pos"] == "RB"][:2]
    out["WR"] = [p for p in rem if p["pos"] == "WR"][:3]
    out["TE"] = [p for p in rem if p["pos"] == "TE"][:1]
    used += [p["name"] for p in out["RB"] + out["WR"] + out["TE"]]
    out["FLEX"] = [p for p in rem if p["name"] not in used]
    order = out["QB"] + out["RB"] + out["WR"] + out["TE"] + out["FLEX"] + out["DST"]
    assert len(order) == 9
    return order

with open("data/2026-wk01-lineups-DK-upload.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(SLOTS)
    for lu in lineups: w.writerow([p["nid"] for p in slotify(lu)])

with open("data/2026-wk01-lineups-readable.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["#", "Type"] + SLOTS + ["Salary", "EstProj", "SumOwn%"])
    for i, lu in enumerate(lineups, 1):
        ps = slotify(lu)
        w.writerow([i, "CASH" if i <= 5 else "GPP"] +
                   [f"{p['name']} ${p['sal']}" + (" (Q)" if p["q"] else "") for p in ps] +
                   [sum(p["sal"] for p in ps), round(sum(p["proj"] for p in ps), 1),
                    round(sum(p["own"] for p in ps))])

print(f"built {len(lineups)} lineups in {tries} tries")
print("\nEXPOSURES (of 30):")
for n, c in sorted(use.items(), key=lambda x: -x[1]):
    if c >= 3: print(f"  {c:2}x {n}" + ("  [Q]" if P[n]["q"] else ""))
