# Season-Long Tracking Framework — Prices, Trends, Age, Situations

DK re-prices every player every week, and the market (salaries + ownership)
chases last week's box scores. Our edge is tracking the **inputs** (role,
usage, situation) faster than the market reprices the **outputs** (points).
This file defines what we log weekly and how we use it.

## 1. Price tracking (salary deltas)

Every week's salary CSV is saved to `data/2026-wkNN-DKSalaries.csv`. Compare
week-over-week:

- **Price lag = value.** A player whose role grew but whose salary hasn't
  moved yet (e.g., a back who just inherited a job priced at $4.8K) is the
  best asset in DFS. These windows last 1–3 weeks.
- **Price spike = trap check.** After a 3-TD game, a player often costs $1K+
  more while his underlying usage is unchanged. Pay for usage, not for boxes.
- The generator scripts can diff consecutive CSVs to flag the biggest
  risers/fallers each week — check them against usage, not points.

## 2. Hot / cold (usage trends, not point trends)

"Hot" that continues: rising snap share, route %, target share, RZ touches
over a rolling 3 weeks. "Hot" that regresses: TD spikes on flat usage.
Log per week in the weekly file:

- 3-week trending-up players (buy before price catches up)
- 3-week trending-down players (sell even if the price still looks fair)
- TD-luck outliers both directions (points ≫ or ≪ expected)

## 3. Age & mileage watch

- RBs 27+ or coming off 300+ touch seasons: expect midseason decline/injury
  risk; fine early, lighten exposure late in the year.
- WRs decline more gently (low-30s), QBs/TEs later still.
- Veterans returning from soft-tissue injuries lose burst first — watch
  snap-share caps in their first weeks back (see docs/injury-risk.md).

## 4. Situation changes (in-season)

Update docs/coaching-trends-2026.md and docs/player-movement-2026.md when:
- A play-caller is fired/changed (usually after Week 8 for bad teams) —
  re-baseline that whole offense.
- A trade-deadline move lands a player as a clear No. 1 option — the
  "new favorable situation" premium is real but takes 2–4 weeks for WRs.
- A starting QB change up- or down-grades every pass catcher on the team.
- A star's season-ending injury creates a season-long value (not just one week).

## 5. Weekly results loop (the compounding part)

After every slate, fill the Results section of `weeks/2026-wkNN.md`:
- Our lineup scores vs that week's cash line and GPP-winning score
- Which process calls hit/missed (not just which players)
- One concrete adjustment for next week

Monthly: review bankroll/2026-log.md — ROI split cash vs GPP, and whether
entry sizing still fits the 5–10%-per-slate rule.

## External data upgrades

Chris can drop in PFF/Fantasy Points Data exports (CSV/screenshots) any week.
Priority data if subscribed: snap/route/target shares by week, O-line/D-line
grades, coverage matchups, expected fantasy points. Store season baselines in
`data/` and reference them in weekly research.
