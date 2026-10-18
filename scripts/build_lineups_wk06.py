#!/usr/bin/env python3
"""Week 6 2026 lineup builder — 5 cash + 25 GPP.

Week 5 lessons enforced in code:
  - GPP lineups are STACK-FIRST: QB + 2 same-team pass catchers + 1 bring-back
    from the opponent (Week 5's best possible lineup was a GB/NE stack we never built).
  - Hard cap lowered 8 -> 7 of 30, QBs capped at 6, so leverage plays get room.
  - Max one Q per lineup; no Q or sub-8-PPG punts in cash.
Projections/ownership are Claude ESTIMATES from PFF Week 6 projections adjusted
for Vegas implied totals and Saturday injury news, labeled as such.
"""
import csv, random, sys
from collections import defaultdict

random.seed(20261018)
rows = {r["Name"]: r for r in csv.DictReader(
    open("data/2026-wk06-DKSalaries.csv", encoding="utf-8-sig"))}

POOL = {
 "QB": {"Josh Allen": (23.5, 16), "Matthew Stafford": (21.5, 14), "Drake Maye": (19.5, 9),
        "Patrick Mahomes": (19, 8), "Kirk Cousins": (19, 10), "Caleb Williams": (20, 7),
        "Tyler Shough": (17, 4), "Jacoby Brissett": (16.5, 4), "Aaron Rodgers": (16.5, 5),
        "Bryce Young": (16.5, 4), "Jameis Winston": (16.5, 6), "Michael Penix Jr.": (17, 6),
        "Daniel Jones": (16, 4), "Tyler Huntley": (15, 7)},
 "RB": {"Kenneth Walker III": (19.5, 12), "Bijan Robinson": (21, 15), "Jonathan Taylor": (20, 14),
        "Kyren Williams": (18.5, 18), "James Cook III": (18.5, 14), "Derrick Henry": (16.5, 8),
        "Chuba Hubbard": (16, 10), "D'Andre Swift": (17, 14), "Jaylen Warren": (15, 15),
        "Ashton Jeanty": (16, 10), "Braelon Allen": (14.5, 15), "Tyler Allgeier": (12.5, 9),
        "Rhamondre Stevenson": (14, 6), "Bucky Irving": (13, 7), "Cam Skattebo": (12.5, 5),
        "Dameon Pierce": (12.5, 14), "Blake Corum": (9.5, 4)},
 "WR": {"Puka Nacua": (23, 25), "Drake London": (18, 14), "Chris Olave": (16, 6),
        "Garrett Wilson": (16, 10), "Tetairoa McMillan": (15, 7), "Malik Nabers": (16, 11),
        "Michael Wilson": (14.5, 5), "Davante Adams": (15.5, 9), "Zay Flowers": (12, 5),
        "Luther Burden III": (12.5, 8), "Xavier Worthy": (12.5, 12), "DK Metcalf": (11.5, 4),
        "Jalen Coker": (12, 4), "Devaughn Vele": (11, 5), "Josh Downs": (11, 4),
        "Ladd McConkey": (11, 5), "Carnell Tate": (11, 5), "Germie Bernard": (10.5, 12),
        "Tre Tucker": (11, 7), "Rome Odunze": (10, 5), "Emeka Egbuka": (10, 5),
        "Keenan Allen": (9.5, 5), "Khalil Shakir": (10, 4), "DeVonta Smith": (12, 4),
        "DJ Moore": (11, 4), "Kendrick Bourne": (8, 3)},
 "TE": {"Brock Bowers": (19, 16), "Trey McBride": (18, 12), "Isaiah Likely": (13, 15),
        "Travis Kelce": (12.5, 7), "Dalton Kincaid": (11.5, 6), "Colston Loveland": (11, 7),
        "Harold Fannin Jr.": (10.5, 6), "Juwan Johnson": (10, 4), "Kyle Pitts Sr.": (9, 5),
        "Tyler Higbee": (9, 6), "Michael Mayer": (8, 4), "Tyler Warren": (12.5, 5)},
 "DST": {"Rams": (9, 18), "Patriots": (8, 12), "Chiefs": (8, 10), "Steelers": (7.5, 8),
         "Ravens": (7, 6), "Saints": (7, 7), "Panthers": (7.5, 8), "Colts": (7.5, 8),
         "Browns": (7, 6), "Giants": (6.5, 4), "Jets": (6, 4)},
}

def opp(team, gi):
    a, b = gi.split(" ")[0].split("@"); return b if team == a else a

P = {}
for pos, d in POOL.items():
    for name, (proj, own) in d.items():
        if name not in rows: sys.exit(f"NOT ON SLATE: {name}")
        r = rows[name]
        if r["Status"] in ("OUT", "IR", "D"): sys.exit(f"INACTIVE in pool: {name} ({r['Status']})")
        P[name] = dict(name=name, pos=pos, sal=int(r["Salary"]), team=r["TeamAbbrev"],
                       opp=opp(r["TeamAbbrev"], r["Game Info"]), proj=proj, own=own,
                       nid=r["Name + ID"], q=r["Status"] == "Q", gi=r["Game Info"])
# News-based Q flags beyond DK's tag (Caleb listed Q; reports say he plays)
for n in ["Caleb Williams"]: P[n]["q"] = True

HARD_CAP = 7
CAPS = defaultdict(lambda: HARD_CAP)
for n, p in P.items():
    if p["pos"] == "QB": CAPS[n] = 6
CAPS.update({"Chris Olave": 4, "DJ Moore": 2, "Tyler Warren": 3, "Caleb Williams": 4,
             "Jaylen Warren": 4,            # +21 pts over expected in Wk5: regression, priced up
             "Blake Corum": 2, "Kendrick Bourne": 2, "Tyler Huntley": 3,
             "Jets": 3, "Tyler Allgeier": 5})
CASH_EXCLUDE = {"Blake Corum", "Kendrick Bourne", "Germie Bernard", "Jets", "Giants", "Tyler Huntley"}
BOOST = defaultdict(lambda: 1.0)
BOOST.update({"Josh Allen": 1.8, "Matthew Stafford": 2.3, "Kirk Cousins": 2.0, "Drake Maye": 1.3, "Puka Nacua": 1.8,
              "Brock Bowers": 1.7, "Kyren Williams": 1.6, "James Cook III": 1.5, "D'Andre Swift": 1.5,
              "Dameon Pierce": 1.5, "Isaiah Likely": 1.5, "Drake London": 1.4, "Malik Nabers": 1.4,
              "Davante Adams": 1.3, "Xavier Worthy": 1.3, "Tre Tucker": 1.3, "Rams": 1.5,
              "Panthers": 1.3, "Bijan Robinson": 1.3, "Garrett Wilson": 1.3})

def gkey(p): return "".join(sorted([p["team"], p["opp"]]))
def valid(names, lineups):
    ps = [P[n] for n in names]
    if len(set(names)) != 9: return False
    if not (48500 <= sum(p["sal"] for p in ps) <= 50000): return False
    dst = next(p for p in ps if p["pos"] == "DST")
    if any(p["opp"] == dst["team"] for p in ps if p["pos"] != "DST"): return False
    g = defaultdict(int)
    for p in ps: g[gkey(p)] += 1
    if max(g.values()) > 4: return False          # a full stack + bring-back is 4
    if sum(1 for p in ps if p["q"]) > 1: return False
    s = set(names)
    return all(len(s - set(l)) >= 2 for l in lineups)

def solve_cash(n=5):
    best, seen = [], set()
    for _ in range(500000):
        lu = [random.choice(list(POOL["QB"]))] + random.sample(list(POOL["RB"]), 2) \
           + random.sample(list(POOL["WR"]), 3) + [random.choice(list(POOL["TE"]))]
        fp = random.choices(["RB", "WR", "TE"], weights=[5, 4, 1])[0]
        fl = [x for x in POOL[fp] if x not in lu]
        lu += [random.choice(fl), random.choice(list(POOL["DST"]))]
        if len(set(lu)) != 9: continue
        if any(P[x]["q"] or x in CASH_EXCLUDE for x in lu): continue
        ps = [P[x] for x in lu]
        if not (48500 <= sum(p["sal"] for p in ps) <= 50000): continue
        dst = next(p for p in ps if p["pos"] == "DST")
        if any(p["opp"] == dst["team"] for p in ps if p["pos"] != "DST"): continue
        g = defaultdict(int)
        for p in ps: g[gkey(p)] += 1
        if max(g.values()) > 3: continue
        k = tuple(sorted(lu))
        if k in seen: continue
        seen.add(k); best.append((sum(p["proj"] for p in ps), sorted(lu)))
    best.sort(key=lambda x: -x[0]); out = []
    for _, lu in best:
        if all(len(set(lu) - set(o)) >= 3 for o in out): out.append(lu)
        if len(out) == n: break
    return out

use = defaultdict(int); lineups = []
def add(names):
    lineups.append(sorted(names))
    for n in names: use[n] += 1
for lu in solve_cash():
    assert valid(lu, lineups), lu
    add(lu)

def wpick(cands, k=1):
    c = [x for x in cands if use[x] < CAPS[x]]
    if len(c) < k: return None
    w = [(P[x]["proj"] / P[x]["sal"] * 1000 + 1) * BOOST[x] for x in c]
    out = []
    for _ in range(k):
        x = random.choices(c, weights=w)[0]; i = c.index(x); c.pop(i); w.pop(i); out.append(x)
    return out

stack_log = []; tries = 0
while len(lineups) < 30 and tries < 600000:
    tries += 1
    qb = wpick(list(POOL["QB"]))
    if not qb: break
    qb = qb[0]; q = P[qb]
    mates = [n for n, p in P.items() if p["team"] == q["team"] and p["pos"] in ("WR", "TE")]
    stack = wpick(mates, 2)                      # Week 5 lesson: two pass catchers by default
    if not stack: continue
    br = [n for n, p in P.items() if p["team"] == q["opp"] and p["pos"] in ("WR", "TE", "RB")]
    bring = wpick(br, 1)                         # bring-back is mandatory
    if not bring: continue
    names = [qb] + stack + bring
    need = {"RB": 2, "WR": 3, "TE": 1}; flex = 1
    for n in names[1:]:
        pp = P[n]["pos"]
        if need[pp] > 0: need[pp] -= 1
        else: flex -= 1
    if flex < 0: continue
    fill = []; ok = True
    for pos in ["RB", "WR", "TE", "DST"]:
        cnt = need.get(pos, 1)
        if cnt <= 0: continue
        got = wpick([x for x in POOL[pos] if x not in names + fill
                     and P[x]["team"] not in (q["team"], q["opp"])], cnt)   # keep stack game at 4
        if not got: ok = False; break
        fill += got
    if not ok: continue
    if flex == 1:
        fpos = random.choices(["RB", "WR", "TE"], weights=[5, 4, 1])[0]
        got = wpick([x for x in POOL[fpos] if x not in names + fill
                     and P[x]["team"] not in (q["team"], q["opp"])])
        if not got: continue
        fill += got
    cand = names + fill
    if len(cand) == 9 and valid(cand, lineups):
        add(cand); stack_log.append((qb, stack, bring[0]))

if len(lineups) < 30: sys.exit(f"only built {len(lineups)} in {tries} tries")

SLOTS = ["QB","RB","RB","WR","WR","WR","TE","FLEX","DST"]
def slotify(names):
    ps = sorted((P[n] for n in names), key=lambda p: -p["sal"]); out = {}; used = []
    for slot in ["QB","DST"]:
        p = next(p for p in ps if p["pos"] == slot); out[slot] = [p]; used.append(p["name"])
    rem = [p for p in ps if p["name"] not in used]
    out["RB"] = [p for p in rem if p["pos"] == "RB"][:2]
    out["WR"] = [p for p in rem if p["pos"] == "WR"][:3]
    out["TE"] = [p for p in rem if p["pos"] == "TE"][:1]
    used += [p["name"] for p in out["RB"]+out["WR"]+out["TE"]]
    out["FLEX"] = [p for p in rem if p["name"] not in used]
    order = out["QB"]+out["RB"]+out["WR"]+out["TE"]+out["FLEX"]+out["DST"]
    assert len(order) == 9; return order

with open("data/2026-wk06-lineups-DK-upload.csv","w",newline="") as f:
    w = csv.writer(f); w.writerow(SLOTS)
    for lu in lineups: w.writerow([p["nid"] for p in slotify(lu)])
with open("data/2026-wk06-lineups-readable.csv","w",newline="") as f:
    w = csv.writer(f); w.writerow(["#","Type"]+SLOTS+["Salary","EstProj","SumOwn%","Stack"])
    for i, lu in enumerate(lineups, 1):
        ps = slotify(lu)
        st = "" if i <= 5 else f"{stack_log[i-6][0]} + {' + '.join(stack_log[i-6][1])} | bring-back {stack_log[i-6][2]}"
        w.writerow([i,"CASH" if i <= 5 else "GPP"]+[f"{p['name']} ${p['sal']}"+(" (Q)" if p["q"] else "") for p in ps]
                   +[sum(p["sal"] for p in ps), round(sum(p["proj"] for p in ps),1), round(sum(p["own"] for p in ps)), st])
print(f"built {len(lineups)} lineups in {tries} tries")
for i, lu in enumerate(lineups[:5], 1):
    print(f"CASH {i}: ${sum(P[n]['sal'] for n in lu)} est {round(sum(P[n]['proj'] for n in lu),1)} | {', '.join(lu)}")
print("\nGPP stacks:"); [print(f"  {s[0]} + {' + '.join(s[1])} | bring-back {s[2]}") for s in stack_log]
print(f"\nEXPOSURES (cap {HARD_CAP}/30, QBs 6):")
for n, c in sorted(use.items(), key=lambda x: -x[1]):
    if c >= 4: print(f"  {c:2}x {n}" + ("  [Q]" if P[n]["q"] else ""))
