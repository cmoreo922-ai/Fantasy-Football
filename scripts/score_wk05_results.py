#!/usr/bin/env python3
"""Score Week 5 lineups with reconstructed DK points (from published box scores, Oct 11-12).
DK: pass .04/yd 4/TD -1 INT +3 @300; rush/rec .1/yd 6/TD 1/rec +3 @100.
EST = no published line found; value is a labeled estimate."""
import csv
def qb(py, ptd, ints, ry=0, rtd=0): return round(py*.04+ptd*4-ints+(3 if py>=300 else 0)+ry*.1+rtd*6+(3 if ry>=100 else 0),2)
def sk(ry=0, rtd=0, rec=0, recy=0, rectd=0):
    return round(ry*.1+rtd*6+rec+recy*.1+rectd*6+(3 if ry>=100 else 0)+(3 if recy>=100 else 0),2)
PTS = {
 # DET@ARI 45-21
 "Jared Goff": qb(271,3,0), "Jahmyr Gibbs": sk(151,2,5,56), "Amon-Ra St. Brown": sk(0,0,6,69),
 "Sam LaPorta": sk(0,0,5,88,1), "Jameson Williams": sk(0,0,2,47,2),
 "Jacoby Brissett": qb(292,3,1), "Trey McBride": sk(0,0,9,66,1), "Michael Wilson": round(sk(0,0,4,30)+7*.04,2),
 # IND@PIT 22-34
 "Aaron Rodgers": qb(235,3,0), "Jaylen Warren": sk(101,1,6,87,1), "DK Metcalf": sk(0,0,3,12),
 "Jonathan Taylor": 11.2, "Tyler Warren": sk(0,0,5,83),          # T.Warren receptions EST (5)
 "Roman Wilson": 3.0, "Josh Downs": 6.0,                              # EST: no line found; R.Wilson left injured
 # LV@NE 17-45
 "Drake Maye": qb(374,4,0,25,1), "TreVeyon Henderson": sk(22), "Efton Chism III": sk(2,0,1,17),
 "Romeo Doubs": sk(0,0,1,16), "Brock Bowers": sk(0,0,8,110,1), "Ashton Jeanty": sk(27,0,3,50),
 "Tre Tucker": sk(-6,0,3,25), "Kirk Cousins": qb(243,1,0), "Rhamondre Stevenson": 6.0,  # Stevenson EST
 # CHI@GB 7-31
 "Jordan Love": qb(367,2,0,6), "Christian Watson": sk(0,0,6,143,2), "Matthew Golden": sk(0,0,6,123),
 "Tucker Kraft": sk(2,0,5,64), "MarShawn Lloyd": sk(31,2), "D'Andre Swift": sk(43,1,4,30),
 "Luther Burden III": sk(0,0,4,47), "Caleb Williams": 0.0,             # DNP
 # SF@SEA 32-29
 "Brock Purdy": qb(189,2,1), "Mike Evans": sk(0,0,7,113,1), "Christian McCaffrey": sk(68,1,3,15),
 "George Kittle": sk(0,0,5,24), "Sam Darnold": qb(195,1,2), "Jaxon Smith-Njigba": sk(0,0,5,102,1),
 "Emanuel Wilson": sk(61,1),
 # CIN@MIA 31-24
 "Joe Burrow": qb(190,4,0), "Chase Brown": sk(39,0,3,21), "Mike Gesicki": sk(0,0,1,4,1),
 "Dohnte Meyers": 3.0, "Malik Washington": sk(0,0,6,43),             # Meyers EST (KR yards don't score on DK)
 "Ja'Marr Chase": sk(0,0,6,77,1), "Tee Higgins": 0.0,
 # CLE@NYJ 12-17
 "Braelon Allen": sk(116,1), "Garrett Wilson": sk(0,0,7,104,1), "Quinshon Judkins": sk(44),
 "Denzel Boston": sk(0,0,3,46,1), "Isaiah Williams": 4.0, "Harold Fannin Jr.": 6.0,  # EST
 # NYG@WAS 27-27
 "Jayden Daniels": qb(199,0,0,103,2), "Cam Skattebo": sk(59,0,2,12), "Antonio Williams": sk(0,0,3,31),
 # MIN@NO 23-13
 "Aaron Jones Sr.": sk(113,1,3,4), "Justin Jefferson": sk(0,0,6,79,1), "Chris Olave": sk(0,0,4,46),
 "Tyler Shough": qb(96,0,2), "Juwan Johnson": sk(0,0,4,16),
 # DEN@LAC 23-17
 "Jaylen Waddle": sk(0,0,2,19), "Omarion Hampton": sk(33,0,1,6),
 # HOU@TEN 26-3
 "C.J. Stroud": qb(261,1,0,5,1), "Nico Collins": 0.0, "Dalton Schultz": sk(0,0,3,30), "David Montgomery": sk(11),
 # DST — points-allowed tier is exact; sacks/turnovers partly EST
 "Texans": 15, "Packers": 16, "Broncos": 12, "Jets": 9, "Bengals": 6, "Patriots": 3,
 "Steelers": 3, "Commanders": 2, "Titans": 2, "Raiders": -3,
}
EST = {"Tyler Warren","Roman Wilson","Josh Downs","Rhamondre Stevenson","Dohnte Meyers","Isaiah Williams",
       "Harold Fannin Jr.","Texans","Packers","Broncos","Jets","Bengals","Patriots","Steelers","Commanders","Titans","Raiders"}
rows = list(csv.reader(open("data/2026-wk05-lineups-readable.csv")))
out = []
for r in rows[1:]:
    names = [c.rsplit(" $",1)[0] for c in r[2:11]]
    miss = [n for n in names if n not in PTS]
    if miss: raise SystemExit(f"missing {miss}")
    tot = round(sum(PTS[n] for n in names), 2)
    est = round(sum(PTS[n] for n in names if n in EST), 1)
    out.append((int(r[0]), r[1], tot, est, float(r[12]), names))
with open("data/2026-wk05-results-scored.csv","w",newline="") as f:
    w = csv.writer(f); w.writerow(["#","Type","ReconstructedDK","PtsFromEstimates","PreLockEstProj","Players"])
    for o in out: w.writerow([o[0],o[1],o[2],o[3],o[4]," | ".join(f"{n} {PTS[n]}" for n in o[5])])
for o in sorted(out, key=lambda x:-x[2]):
    print(f"#{o[0]:2} {o[1]:4} {o[2]:6.1f}  (est part {o[3]:4.1f}, proj {o[4]})  " + ", ".join(f"{n.split()[-1] if n not in ('Texans','Packers','Broncos','Jets','Bengals','Patriots','Steelers','Commanders','Titans','Raiders') else n} {PTS[n]}" for n in o[5]))
print("\nTop individual scores among players we used:")
used = {n for o in out for n in o[5]}
for n in sorted(used, key=lambda n:-PTS[n])[:12]: print(f"  {PTS[n]:5.1f} {n}")
