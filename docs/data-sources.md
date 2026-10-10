# Weekly Data Sources

Where to look for each input of the weekly process. (Availability from a Claude
session depends on the network; use search when a site is blocked and always
prefer the freshest source for lines/injuries.)

## Vegas lines & implied totals
- Sportsbook lines via search ("NFL week N odds spreads totals")
- Implied-total tools: Sharp Football Analysis implied team totals, FantasyLabs
  Vegas dashboard, firstdown.studio/implied-totals

## Injuries & news
- Official team injury reports (Wed–Fri practice participation)
- NFL.com / ESPN injury pages; beat reporters for game-time decisions
- Sunday inactives ~90 min before kickoff

## Usage & advanced stats
- Snap counts / target share / air yards: PlayerProfiler, FantasyData,
  statrankings.com, NFL Next Gen Stats
- xFP and opportunity data: various (4for4, Fantasy Points Data, RotoViz-style
  tools)
- Team tendencies (PROE, pace, personnel): rbsdm.com-style EPA dashboards,
  Sharp Football Analysis, Ringer/ESPN scheme coverage

## DFS-specific
- Salaries: DraftKings lobby (export CSV from any contest screen)
- Projected ownership: Stokastic, Establish The Run, FantasyLabs, RotoGrinders
  (ownership projections are the leverage input — worth finding each week)
- Slate strategy articles: Stokastic NFL DFS hub, Establish The Run, 4for4

## Premium data (worth considering at $100+/week stakes)

- **PFF (PFF+ ~$100/yr, PFF Pro ~$200/yr):** player grades by facet, 50+
  premium stats (EPA/play, success rate, coverage matchups), O-line/D-line
  grades — best for matchup analysis (WR vs CB, OL vs DL pressure rates).
- **Fantasy Points Data (~subscription):** hand-charted per-game data —
  expected fantasy points, schedule-adjusted points allowed, separation
  metrics. Best xFP source.
- **NFL Next Gen Stats (free):** tracking data — separation, time to throw,
  rush yards over expected. Free and underused.
- Free workhorses: Pro-Football-Reference (usage/snaps), rbsdm.com-style EPA
  dashboards, PlayerProfiler (opportunity metrics).
- Note: Chris can paste screenshots/CSV exports from any of these into a
  session and Claude will incorporate them into the weekly process.

## Weather
- NFL weather sites / national forecast, checked Sat + Sun AM; wind speed at
  kickoff is the number that matters

## Strategy reading list (evergreen)
- Establish The Run "NFL Showdown 101"
- Stokastic "How to Win DFS Tournaments: Ownership + Leverage" and contest
  selection guides
- 4for4 DFS bankroll management guide
- RotoGrinders DraftKings NFL strategy + site scoring comparison

## PFF+ data packages in `data/pff/2026/`

Chris's PFF+ subscription feeds the repo two ways:

1. **Per-team grade pastes** (`data/pff/2026/raw/` → `parsed/` via
   `scripts/parse_pff_paste.py`). Used Weeks 1–2.
2. **Weekly bulk export package** starting Week 5:
   `data/pff/2026/wk05-package/` (read its `README_for_Claude.md` first).
   Exported Oct 8, 2026, PPR scoring. Contents:
   - `master_players_week5.csv` — **start here.** One row per QB/RB/WR/TE/K/DST
     joining Week 5 projection + expert rank, ROS rank, season-to-date stats,
     expected points (xFP), 2026 PFF grades + snaps, position SOS, and the
     team's/opponent's team-level PFF grades.
   - Supporting 2026 tables: projections, rankings, season stats (QB/skill/K/
     DST/IDP), expected points, player grades, team grades, SOS by position,
     pre-Week-5 power ratings.
   - `history/` — 2020–2025 season stats, PFF grades, team grades, xFP
     (2024–25), plus `player_trends.csv` / `team_trends.csv` (PPG and
     positional finish by season, 3-yr baselines, team changes).
   - The two Excel workbooks in the original zip duplicate the CSVs and were
     not committed.

   How to use it in `/weekly-picks`:
   - Team/roster claims: the **DK salary CSV is still authoritative**; the
     package's `team` column is a second check (both must agree).
   - `sos_wk5` is 0–10, **higher = easier**; `opp_pff_*` grades are higher =
     tougher defense.
   - `xfp_ppg_over_expected` positive = running hot (regression risk);
     negative = usage says buy-low.
   - 2026 grades/stats are a ~4-game sample. Lean on `history/player_trends.csv`
     (`ppg_3yr_avg_2023_2025`, `ppg_2026td_vs_3yr_avg`) before trusting a
     spike.
   - It has **no salaries, no Vegas lines, no game logs, no snap/target
     trends by week** — those still come from the DK CSV and fresh research.
