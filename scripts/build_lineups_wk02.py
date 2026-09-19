#!/usr/bin/env python3
"""Week 2 2026 lineup builder — 5 cash + 25 GPP.

Week 1 lessons enforced in code:
  - HARD CAP 8/30 on every player (Lloyd was 18/30 and split a backfield)
  - No single-game script concentration: SF (-12.5) capped like any other team
  - Projections lean on 2026 Week 1 PFF grades + implied totals, not 2025 units
Projections/ownership are Claude ESTIMATES, labeled as such.
"""
import csv, random, sys
from collections import defaultdict

random.seed(2026)
rows = {r["Name"]: r for r in csv.DictReader(
    open("data/2026-wk02-DKSalaries.csv", encoding="utf-8-sig"))}

# name: (proj, own%) — Claude estimates from role x environment x 2026 grade
POOL = {
 "QB": {"Lamar Jackson": (23, 18), "Dak Prescott": (20.5, 14), "Caleb Williams": (20, 15),
        "C.J. Stroud": (18.5, 9), "Brock Purdy": (19, 12), "Jalen Hurts": (21, 13),
        "Jordan Love": (18.5, 7), "Baker Mayfield": (18, 8), "Trevor Lawrence": (18, 7),
        "Bryce Young": (17.5, 5), "Geno Smith": (16.5, 4), "Drake Maye": (17, 6)},
 "RB": {"Derrick Henry": (21, 30), "D'Andre Swift": (18.5, 22), "Javonte Williams": (17.5, 18),
        "Bucky Irving": (16, 14), "David Montgomery": (14.5, 12), "Omarion Hampton": (14.5, 10),
        "Chase Brown": (15.5, 11), "Ashton Jeanty": (14, 9), "Breece Hall": (13.5, 8),
        "Kyle Monangai": (12, 9), "Woody Marks": (11, 7), "Justice Hill": (9.5, 5),
        "Tyjae Spears": (9, 4), "Rachaad White": (9, 4), "Braelon Allen": (9, 5),
        "Kenny Gainwell": (9, 4), "Tony Pollard": (10, 5), "Bhayshul Tuten": (11.5, 8),
        "Chris Rodriguez Jr.": (9, 3), "Saquon Barkley": (16.5, 15)},
 "WR": {"CeeDee Lamb": (18, 20), "Mike Evans": (16, 14), "Jaxon Smith-Njigba": (17.5, 16),
        "Justin Jefferson": (17, 15), "Christian Watson": (15, 11), "Emeka Egbuka": (14.5, 12),
        "George Pickens": (14, 10), "DeVonta Smith": (14.5, 11), "Jalen Coker": (13.5, 8),
        "Cooper Kupp": (12.5, 9), "Matthew Golden": (12, 7), "Rome Odunze": (12.5, 9),
        "Luther Burden III": (12.5, 10), "Chris Olave": (14, 9), "Jerry Jeudy": (10, 5),
        "Terry McLaurin": (13, 10), "Stefon Diggs": (11.5, 7), "Deebo Samuel Sr.": (12, 8),
        "Jayden Reed": (10.5, 5), "Quentin Johnston": (10.5, 7), "Garrett Wilson": (13, 9),
        "Brian Thomas Jr.": (13.5, 10), "Demarcus Robinson": (9.5, 4), "Rashod Bateman": (11, 7),
        "Jakobi Meyers": (10.5, 5), "Adonai Mitchell": (9.5, 4), "Xavier Hutchinson": (9, 6)},
 "TE": {"Dallas Goedert": (12, 14), "Mark Andrews": (11.5, 13), "Tucker Kraft": (11, 11),
        "Juwan Johnson": (10, 8), "T.J. Hockenson": (10, 7), "Colston Loveland": (9.5, 7),
        "Mike Gesicki": (9, 6), "George Kittle": (10.5, 9), "Hunter Henry": (8.5, 5),
        "Brenton Strange": (8.5, 5), "Pat Freiermuth": (8, 4), "Michael Mayer": (8, 4)},
 "DST": {"Buccaneers": (9, 18), "Eagles": (8.5, 16), "49ers": (9, 20), "Patriots": (8, 9),
         "Seahawks": (7.5, 10), "Chargers": (7.5, 9), "Packers": (7, 7), "Ravens": (7.5, 8),
         "Panthers": (6.5, 5), "Bears": (7, 8), "Broncos": (6.5, 4), "Cowboys": (6.5, 6)},
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
CAPS.update({  # Q tags and committees capped tighter still
    "Ladd McConkey": 0, "Kalif Raymond": 0,          # trap / game-time decision
    "Kyle Monangai": 4, "Woody Marks": 4, "Justice Hill": 3, "Rachaad White": 3,
    "Kenny Gainwell": 3, "Chris Rodriguez Jr.": 3, "Braelon Allen": 4,
    "Chris Olave": 5, "Mike Gesicki": 4, "Demarcus Robinson": 4,
})
BOOST = defaultdict(lambda: 1.0)
BOOST.update({"Derrick Henry": 3.5, "D'Andre Swift": 2.6, "CeeDee Lamb": 2.2,
              "Javonte Williams": 2.2, "Mike Evans": 2.0, "Dallas Goedert": 2.2,
              "Mark Andrews": 2.0, "Bucky Irving": 1.8, "Lamar Jackson": 2.2,
              "Dak Prescott": 2.0, "Jalen Coker": 1.8, "Tucker Kraft": 1.7,
              "Cooper Kupp": 1.6, "Buccaneers": 1.6, "Eagles": 1.5, "Matthew Golden": 1.5})

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
        if any(P[x]["q"] or CAPS[x] == 0 for x in lu): continue   # cash: no Q, no traps
        ps = [P[x] for x in lu]
        if not (48500 <= sum(x["sal"] for x in ps) <= 50000): continue
        dst = next(x for x in ps if x["pos"] == "DST")
        if any(x["opp"] == dst["team"] for x in ps if x["pos"] != "DST"): continue
        g = {}
        for x in ps:
            k = "".join(sorted([x["team"], x["opp"]])); g[k] = g.get(k, 0) + 1
        if max(g.values()) > 3: continue
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
    if max(g.values()) > 3: return False
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

with open("data/2026-wk02-lineups-DK-upload.csv","w",newline="") as f:
    w = csv.writer(f); w.writerow(SLOTS)
    for lu in lineups: w.writerow([p["nid"] for p in slotify(lu)])
with open("data/2026-wk02-lineups-readable.csv","w",newline="") as f:
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
