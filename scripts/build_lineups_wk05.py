#!/usr/bin/env python3
"""Week 5 2026 lineup builder — 5 cash + 25 GPP.

Week 1 lessons enforced in code:
  - HARD CAP 8/30 on every player (Lloyd was 18/30 and split a backfield)
  - No single-game script concentration: SF (-12.5) capped like any other team
  - Projections lean on 2026 Week 1 PFF grades + implied totals, not 2025 units
Projections/ownership are Claude ESTIMATES, labeled as such.
"""
import csv, random, sys
from collections import defaultdict

random.seed(20261011)
rows = {r["Name"]: r for r in csv.DictReader(
    open("data/2026-wk05-DKSalaries.csv", encoding="utf-8-sig"))}

# name: (proj, own%) — Claude ESTIMATES: PFF+ Week 5 PPR projection adjusted
# for Vegas implied totals (Oct 10) and Friday/Saturday injury news.
POOL = {
 "QB": {"Jared Goff": (21, 14), "Jacoby Brissett": (19.5, 18), "Joe Burrow": (19, 9),
        "Aaron Rodgers": (17, 8), "Brock Purdy": (18.5, 7), "Sam Darnold": (17, 6),
        "Drake Maye": (18.5, 8), "Jordan Love": (17, 6), "Kirk Cousins": (16.5, 4),
        "C.J. Stroud": (16.5, 5), "Tyler Shough": (18, 6), "Jayden Daniels": (17.5, 7),
        "Caleb Williams": (19, 6)},
 "RB": {"Jahmyr Gibbs": (25.5, 30), "Jonathan Taylor": (19, 14), "Christian McCaffrey": (17, 8),
        "Chase Brown": (17, 14), "Ashton Jeanty": (16, 8), "Jaylen Warren": (16, 13),
        "Aaron Jones Sr.": (15, 10), "Braelon Allen": (15, 22), "D'Andre Swift": (16, 16),
        "Cam Skattebo": (13.5, 8), "Omarion Hampton": (13, 6), "Emanuel Wilson": (13, 12),
        "Rhamondre Stevenson": (11.5, 4), "TreVeyon Henderson": (11, 5), "Quinshon Judkins": (12, 5),
        "David Montgomery": (11.5, 6), "Jeremiyah Love": (12.5, 5), "MarShawn Lloyd": (10.5, 7)},
 "WR": {"Jaxon Smith-Njigba": (21, 22), "Amon-Ra St. Brown": (20.5, 20), "Justin Jefferson": (17.5, 12),
        "Chris Olave": (17.5, 10), "Nico Collins": (16, 10), "Garrett Wilson": (16, 10),
        "Christian Watson": (14.5, 9), "Michael Wilson": (15, 14), "Mike Evans": (13.5, 6),
        "Malik Nabers": (13.5, 7), "Jameson Williams": (13, 9), "Matthew Golden": (12.5, 5),
        "Josh Downs": (12.5, 5), "DK Metcalf": (12.5, 7), "Malik Washington": (12, 9),
        "Luther Burden III": (12, 10), "Roman Wilson": (10.5, 14), "Isaiah Williams": (10, 8),
        "Efton Chism III": (9.5, 9), "Dohnte Meyers": (11, 15), "Ja'Marr Chase": (20, 10),
        "Tee Higgins": (15, 5), "Antonio Williams": (9.5, 8), "Romeo Doubs": (11, 5),
        "Jaylen Waddle": (13, 6), "Tre Tucker": (10, 4), "Denzel Boston": (10, 4)},
 "TE": {"Trey McBride": (17.5, 15), "Brock Bowers": (17, 12), "Sam LaPorta": (13.5, 16),
        "Tyler Warren": (12.5, 9), "George Kittle": (12, 6), "Tucker Kraft": (12, 7),
        "Mike Gesicki": (11, 10), "Harold Fannin Jr.": (11, 6), "Juwan Johnson": (10.5, 5),
        "Dalton Schultz": (9, 3)},
 "DST": {"Texans": (9, 18), "Bengals": (8, 10), "Commanders": (7.5, 10), "Jets": (7, 8),
         "Packers": (7.5, 8), "Patriots": (7, 7), "Broncos": (7, 7), "Steelers": (7, 6),
         "Raiders": (6.5, 4), "Titans": (5.5, 3)},
}

def opp(team, gi):
    a, b = gi.split(" ")[0].split("@"); return b if team == a else a

P = {}
for pos, d in POOL.items():
    for name, (proj, own) in d.items():
        if name not in rows:
            sys.exit(f"NOT ON SLATE: {name}")
        r = rows[name]
        if r["Status"] in ("OUT", "IR", "D"):
            sys.exit(f"INACTIVE in pool: {name} ({r['Status']})")
        P[name] = dict(name=name, pos=pos, sal=int(r["Salary"]), team=r["TeamAbbrev"],
                       opp=opp(r["TeamAbbrev"], r["Game Info"]), proj=proj, own=own,
                       nid=r["Name + ID"], q=r["Status"] == "Q")

HARD_CAP = 8                      # Week 1 lesson: nobody above 8/30
CAPS = defaultdict(lambda: HARD_CAP)
CAPS.update({  # Q tags / game-time decisions capped tighter; Q players never in cash
    "Ashton Jeanty": 3, "Ja'Marr Chase": 4, "Tee Higgins": 2, "Dohnte Meyers": 3,
    "Justin Jefferson": 5, "Caleb Williams": 3, "Rhamondre Stevenson": 2,
    "Jeremiyah Love": 3, "MarShawn Lloyd": 3, "Mike Evans": 4, "Malik Nabers": 4,
    "Cam Skattebo": 4, "Kirk Cousins": 3, "Titans": 3, "Raiders": 3,
})
BOOST = defaultdict(lambda: 1.0)
BOOST.update({"Jahmyr Gibbs": 2.6, "Amon-Ra St. Brown": 2.2, "Jared Goff": 2.2,
              "Jacoby Brissett": 2.2, "Trey McBride": 2.0, "Michael Wilson": 1.9,
              "Sam LaPorta": 1.9, "Braelon Allen": 2.4, "Jaxon Smith-Njigba": 1.8,
              "Jaylen Warren": 1.7, "Chase Brown": 1.6, "Jameson Williams": 1.6,
              "Aaron Rodgers": 1.5, "Emanuel Wilson": 1.5, "Texans": 1.7,
              "Roman Wilson": 1.4, "Garrett Wilson": 1.4, "D'Andre Swift": 1.4})

# Week 5 Q flags from news (DK Status column + Fri/Sat reports): never in cash
NEWS_Q = {"Ashton Jeanty", "Ja'Marr Chase", "Tee Higgins", "Dohnte Meyers", "Justin Jefferson",
          "Caleb Williams", "Rhamondre Stevenson", "Jeremiyah Love", "Mike Evans",
          "Malik Nabers", "Cam Skattebo", "D'Andre Swift"}
for n in NEWS_Q: P[n]["q"] = True

# Low-floor punts (season PPG under 8) are GPP-only
CASH_EXCLUDE = {"MarShawn Lloyd", "Efton Chism III", "Isaiah Williams", "Titans", "Raiders", "Dohnte Meyers", "Tre Tucker"}

# Cash lineups are SOLVED against the $50K cap, not hand-picked — the
# hand-built version came in at $54,600. Randomised search on est. projection.
def solve_cash(n=5):
    best, seen = [], set()
    for _ in range(400000):
        lu = [random.choice(list(POOL["QB"]))]
        lu += random.sample(list(POOL["RB"]), 2)
        lu += random.sample(list(POOL["WR"]), 3)
        lu.append(random.choice(list(POOL["TE"])))
        fp = random.choices(["RB", "WR", "TE"], weights=[5, 4, 1])[0]
        fl = [x for x in POOL[fp] if x not in lu]
        if not fl: continue
        lu.append(random.choice(fl))
        lu.append(random.choice(list(POOL["DST"])))
        if len(set(lu)) != 9: continue
        if any(P[x]["q"] or CAPS[x] == 0 or x in CASH_EXCLUDE for x in lu): continue   # cash: no Q, no thin-floor punts
        ps = [P[x] for x in lu]
        if not (48500 <= sum(x["sal"] for x in ps) <= 50000): continue
        dst = next(x for x in ps if x["pos"] == "DST")
        if any(x["opp"] == dst["team"] for x in ps if x["pos"] != "DST"): continue
        g = {}
        for x in ps:
            k = "".join(sorted([x["team"], x["opp"]])); g[k] = g.get(k, 0) + 1
        if any(v > (4 if k == "ARIDET" else 3) for k, v in g.items()): continue
        key = tuple(sorted(lu))
        if key in seen: continue
        seen.add(key)
        best.append((sum(x["proj"] for x in ps), sorted(lu)))
    best.sort(key=lambda x: -x[0])
    out = []
    for proj, lu in best:
        if all(len(set(lu) - set(o)) >= 2 for o in out): out.append(lu)
        if len(out) == n: break
    return out

CASH = solve_cash()
print("Cash lineups solved against cap:")
for lu in CASH:
    print(f"  ${sum(P[x]['sal'] for x in lu)} proj {round(sum(P[x]['proj'] for x in lu),1)} | " + ", ".join(lu))


use = defaultdict(int); lineups = []

def ok(names):
    ps = [P[n] for n in names]
    sal = sum(p["sal"] for p in ps)
    if not (48500 <= sal <= 50000): return False
    dst = next(p for p in ps if p["pos"] == "DST")
    if any(p["opp"] == dst["team"] for p in ps if p["pos"] != "DST"): return False
    if len(set(names)) != 9: return False
    # no more than 3 players from any single game (Week 1 script-stack lesson)
    g = defaultdict(int)
    for p in ps:
        g["".join(sorted([p["team"], p["opp"]]))] += 1
    if any(v > (4 if k == "ARIDET" else 3) for k, v in g.items()): return False
    if sum(1 for p in ps if p["q"]) > 1: return False   # max one Q tag per lineup
    s = set(names)
    return all(len(s - set(l)) >= 2 for l in lineups)

def add(names):
    lineups.append(sorted(names))
    for n in names: use[n] += 1

for lu in CASH:
    assert ok(lu), f"cash lineup invalid: {lu} salary={sum(P[n]['sal'] for n in lu)}"
    add(lu)

def wpick(cands, k=1):
    c = [x for x in cands if use[x] < CAPS[x]]
    if len(c) < k: return None
    w = [(P[x]["proj"] / max(P[x]["sal"], 1) * 1000 + 1) * BOOST[x] for x in c]
    out = []
    for _ in range(k):
        x = random.choices(c, weights=w)[0]
        i = c.index(x); c.pop(i); w.pop(i); out.append(x)
    return out

qbs = list(POOL["QB"]); tries = 0
while len(lineups) < 30 and tries < 400000:
    tries += 1
    pick = wpick(qbs)
    if not pick: continue
    qb = pick[0]; q = P[qb]
    mates = [n for n, p in P.items() if p["team"] == q["team"] and p["pos"] in ("WR", "TE")]
    br = [n for n, p in P.items() if p["team"] == q["opp"] and p["pos"] in ("WR", "TE", "RB")]
    stack = wpick(mates, random.choice([1, 1, 2]))
    if not stack: continue
    names = [qb] + stack
    if random.random() < 0.7 and br:
        b = wpick([x for x in br if x not in names])
        if b: names += b
    need = {"RB": 2, "WR": 3, "TE": 1}
    flex = 1
    for n in names[1:]:
        pp = P[n]["pos"]
        if need.get(pp, 0) > 0: need[pp] -= 1
        else: flex -= 1
    if flex < 0: continue
    fill = []; okf = True
    for pos, cnt in [("RB", need["RB"]), ("WR", need["WR"]), ("TE", need["TE"]), ("DST", 1)]:
        if cnt <= 0: continue
        got = wpick([x for x in POOL[pos] if x not in names + fill], cnt)
        if not got: okf = False; break
        fill += got
    if not okf: continue
    if flex == 1:
        fpos = random.choices(["RB", "WR", "TE"], weights=[5, 4, 1])[0]
        got = wpick([x for x in POOL[fpos] if x not in names + fill], 1)
        if not got: continue
        fill += got
    cand = names + fill
    if len(cand) == 9 and ok(cand): add(cand)

if len(lineups) < 30: sys.exit(f"only built {len(lineups)}")

SLOTS = ["QB","RB","RB","WR","WR","WR","TE","FLEX","DST"]
def slotify(names):
    ps = sorted((P[n] for n in names), key=lambda p: -p["sal"])
    out, used = {}, []
    for slot in ["QB","DST"]:
        p = next(p for p in ps if p["pos"] == slot); out[slot] = [p]; used.append(p["name"])
    rem = [p for p in ps if p["name"] not in used]
    out["RB"] = [p for p in rem if p["pos"] == "RB"][:2]
    out["WR"] = [p for p in rem if p["pos"] == "WR"][:3]
    out["TE"] = [p for p in rem if p["pos"] == "TE"][:1]
    used += [p["name"] for p in out["RB"]+out["WR"]+out["TE"]]
    out["FLEX"] = [p for p in rem if p["name"] not in used]
    order = out["QB"]+out["RB"]+out["WR"]+out["TE"]+out["FLEX"]+out["DST"]
    assert len(order) == 9
    return order

with open("data/2026-wk05-lineups-DK-upload.csv","w",newline="") as f:
    w = csv.writer(f); w.writerow(SLOTS)
    for lu in lineups: w.writerow([p["nid"] for p in slotify(lu)])
with open("data/2026-wk05-lineups-readable.csv","w",newline="") as f:
    w = csv.writer(f); w.writerow(["#","Type"]+SLOTS+["Salary","EstProj","SumOwn%"])
    for i, lu in enumerate(lineups,1):
        ps = slotify(lu)
        w.writerow([i,"CASH" if i<=5 else "GPP"]+
                   [f"{p['name']} ${p['sal']}"+(" (Q)" if p["q"] else "") for p in ps]+
                   [sum(p["sal"] for p in ps), round(sum(p["proj"] for p in ps),1),
                    round(sum(p["own"] for p in ps))])
print(f"built {len(lineups)} lineups in {tries} tries")
print(f"\nEXPOSURES (hard cap {HARD_CAP}/30):")
for n,c in sorted(use.items(), key=lambda x:-x[1]):
    if c >= 3: print(f"  {c:2}x {n}" + ("  [Q]" if P[n]["q"] else ""))
