#!/usr/bin/env python3
"""Join Week 5 DK salaries to the PFF+ Week 5 master table (name + team)."""
import csv, re, unicodedata, sys

def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[.'\-]", "", s)
    s = re.sub(r"\b(jr|sr|ii|iii|iv|v)\b", "", s)
    return re.sub(r"\s+", " ", s).strip()

DST_NAME = {}
dk = list(csv.DictReader(open("data/2026-wk05-DKSalaries.csv", encoding="utf-8-sig")))
pff = list(csv.DictReader(open("data/pff/2026/wk05-package/master_players_week5.csv")))
idx = {}
for r in pff:
    key = (r["team"], "DST") if r["position"] == "DST" else (norm(r["player"]), r["team"])
    idx[key] = r

out, miss = [], []
for r in dk:
    pos = r["Position"]
    key = (r["TeamAbbrev"], "DST") if pos == "DST" else (norm(r["Name"]), r["TeamAbbrev"])
    p = idx.get(key)
    if p is None and pos != "DST":
        # same name on a different team = roster conflict -> flag, never merge
        alt = [x for x in pff if norm(x["player"]) == norm(r["Name"])]
        if alt: miss.append(f"TEAM CONFLICT {r['Name']} DK={r['TeamAbbrev']} PFF={alt[0]['team']}")
    proj = float(p["proj_fpts"]) if p and p["proj_fpts"] else None
    a, b = r["Game Info"].split(" ")[0].split("@")
    out.append(dict(
        name=r["Name"], pos=pos, team=r["TeamAbbrev"], opp=b if r["TeamAbbrev"] == a else a,
        sal=int(r["Salary"]), dk_status=r["Status"], dk_avg=r["AvgPointsPerGame"],
        pff_proj=proj if proj is not None else "",
        val=round(proj / int(r["Salary"]) * 1000, 2) if proj else "",
        pff_inj=p["injury_status_w5"] if p else "", w5_rank=p["w5_pos_rank"] if p else "",
        season_fppg=p["season_fppg"] if p else "", xfp_ppg=p["xfp_expected_ppg"] if p else "",
        xfp_over=p["xfp_ppg_over_expected"] if p else "", sos_wk5=p["sos_wk5"] if p else "",
        grade=p["pff_grade_off"] if p else "", snaps=p["pff_snaps_off"] if p else "",
        opp_def=p["opp_pff_def_grade"] if p else "", opp_cov=p["opp_pff_cov_grade"] if p else "",
        opp_rdef=p["opp_pff_rdef_grade"] if p else "",
        tgts=p["season_targets"] if p else "", carries=p["season_carries"] if p else "", games=p["season_games"] if p else "",
    ))
with open("data/2026-wk05-pool-joined.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
print(f"{len(out)} DK rows, {sum(1 for o in out if o['pff_proj'] != '')} with PFF projection")
print("\n".join(miss) or "no team conflicts")
