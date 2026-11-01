# PFF Week 8 2026 package — DraftKings lineup build (PPR)

**Owner:** Christopher. **Season:** NFL 2026. **Upcoming:** Week 8 (Thu Oct 29 – Mon Nov 2, 2026; DraftKings Sunday Nov 1 main slate). **Most recent completed week:** Week 7.
**Sources:**
- **PFF+** (Pro Football Focus) exports, downloaded **Oct 28, 2026**: Week 7 single-week stats and expected points (pff.com/fantasy/expected-points; same column layout as prior weeks), 2026 season-to-date stats, Week 8 projections, Week 8 PPR rankings (QB/RB/WR/TE/K/DST + FLEX + SUPERFLEX; each file's Position column checked against its name).
- **DraftKings** public NFL lobby salary export (no login): Classic **main slate**, DraftGroupId **153728**, 11 games, first lock Sun Nov 1 1:00 PM ET. Fetched **2026-10-28 19:37 UTC (Wed Oct 28, 9:37 AM HST)** from `https://www.draftkings.com/lineup/getavailableplayerscsv?contestTypeId=21&draftGroupId=153728`. The raw file is `dk_raw/DKSalaries_153728.csv`. Off-slate games were identified from the DK NFL lobby (same day). Salaries and injury statuses can change before lock, so re-download before entering contests.
- **Carried over, NOT refreshed this week** (labeled `_asof_oct8`): PFF 2026 player grades (through Week 4), team grades, and SOS, all from the Oct 8 build — the same values the Week 6 and Week 7 packages used. **History** 2020–2025 (stats, expected points, PFF grades, player/team trends) is in the repo's `data/pff/history/` folder, copied unchanged from the Week 7 package.

Scoring: PFF projections are **full PPR**. I re-verified this on the Week 8 projected stat lines (QB/RB/WR/TE, least-squares fit): 1.00 pts per reception, 0.04/pass yd, ~3.94/pass TD, ~−0.91/INT, 0.1/rush or rec yd, 6/TD; standard PPR formula (incl. −2 fumble lost, +2 two-pt) MAE 0.045 (max 0.24). PFF projections **don't include DraftKings' yardage bonuses** (+3 for 300 pass / 100 rush / 100 rec yds), so DK scores can exceed them slightly. Nothing in this package was invented. Blank means the source didn't have the value. *(derived)* marks simple arithmetic.

## Files
| File | Rows | What |
|---|---|---|
| `master_players_week8.csv` | 794 | **Start here.** One row per player: DK salary/game, Week 8 projection and ranks, Week 7 actuals, usage and expected points, 2026 season-to-date, trends, grades and SOS (as of Oct 8) |
| `PFF_Week8_2026.xlsx` | — | Master first, then every dataset as a tab (header frozen, filters) |
| `dk_salaries_week8_main.csv` | 554 | DraftKings main-slate salaries (QB 75, RB 126, WR 204, TE 127, DST 22; 22 teams) |
| `week8_projections.csv` | 414 | PFF Week 8 projections (QB 57, RB 84, WR 140, TE 77, K 28, DST 28) |
| `week8_rankings.csv` | 333 | PFF Week 8 PPR ranks: positional + FLEX + SUPERFLEX (QB 28, RB 85, WR 114, TE 50, K 28, DST 28) |
| `week7_stats_QB/skill/K/DST.csv` | 33 / 311 / 28 / 28 | Week 7 single-game stats |
| `week7_expected_points_QB/skill.csv` | 31 / 239 | Week 7 actual vs expected fantasy points |
| `season_stats_QB/skill/K/DST.csv` | 62 / 485 / 36 / 32 | 2026 season-to-date (Weeks 1–7) |
| `../../history/` (= `data/pff/history/`) | — | 2020–2025 history + `player_trends.csv`, `team_trends.csv`, grades history, `PFF_History_2020_2025.xlsx` |
| `dk_raw/` | — | Raw DraftKings CSV + fetch timestamp |

## Key master columns
- **Identity/game:** player, position, team, opponent, home_away, bye_week, injury_status_w8 (PFF rankings tag: ACTIVE/QUEST/PROB/OUT), week8_note (bye / off-main-slate game notes).
- **DraftKings:** dk_salary, dk_roster_position (e.g., RB/FLEX), dk_game, dk_game_time_et, dk_status (DK injury tag: Q/OUT/IR), dk_avg_ppg (DK's own season average), on_dk_main_slate (team plays in the 11-game main slate), dk_id.
- **dk_value_pts_per_1k** *(derived)* = proj_fpts ÷ (dk_salary / 1000). Rough guide: about 3x salary-in-thousands is a common cash target and 4x+ a GPP target. Those benchmarks are general DFS conventions, not from these files.
- **Week 8:** proj_fpts, proj_rank_overall (PFF's export order — not a pure points sort), proj_pos_rank *(derived, by proj_fpts within position)*, w8_pos_rank, w8_flex_rank, w8_superflex_rank, and projected stat line (proj_pass_*, proj_rush_*, proj_targets, proj_rec, proj_rec_yds, proj_rec_td).
- **Week 7 actual/usage:** w7_fpts, w7_targets, w7_rec, w7_rec_yds, w7_rec_td, w7_adot (avg depth of target), w7_rz_targets, w7_ez_targets, w7_carries, w7_rush_yds, w7_rush_td, w7_rz_carries, w7_i5_carries (inside-5), w7_pts_per_snap. QB: w7_dropbacks, w7_pass_att, w7_pass_yds, w7_pass_td, w7_int, w7_ez_pass_att. **Snap counts and routes run are not in these exports.**
- **Week 7 expected:** w7_xfp_expected, w7_fpts_minus_expected (positive = scored above expected, so regression risk; negative = below expected, so possible bounce-back).
- **Season to date:** season_games, season_fpts, season_fppg *(derived)*, season targets, rec, yards, TDs, carries, passing.
- **Trends (history):** ppg_3yr_avg_2023_2025, ppg_2025, season_fppg_vs_3yr_avg *(derived)*, team_changes, grade_2025, grade_3yr_avg_2023_2025.
- **As of Oct 8 (not refreshed):** pff_grade_off/pass/run/recv/pos_rank_asof_oct8 (2026 grades through Week 4); sos_wk8_asof_oct8 (Week 8 column of the Oct 8 position-matchup SOS table, 0–10; **higher = easier**, inferred, see Oct 8 README); sos_season_wk5_14 / sos_playoffs_wk15_17_asof_oct8; opp_pff_def/cov/rdef_grade_asof_oct8 (opponent team defense grades, as of Oct 8, mapped to the Week 8 opponent).
- **sources_matched:** proj, w8 (Week 8 ranks), dk, season, w7 (Week 7 stats), w7x (Week 7 expected). **join_flags:** position conflicts (one this week: Jackson Meeks DET — TE in projections/DK, WR in season stats).

## Join method and match rates
- **Key:** normalized name + team (DST by team), same as prior builds. DraftKings/PFF first-name aliases after a same-team/same-position/same-surname check: Kenny→Kenneth Gainwell, Hollywood→Marquise Brown, Mitchell→Mitch Trubisky, Nick→Nicholas Singleton, Matt→Matthew Hibner, Mitch→Mitchell Tinsley, Ben→Benjamin Yurosek. **No new aliases were needed this week** (no DK-only player shares a surname + team with an unmatched PFF row).
- **DraftKings coverage:** every PFF-projected non-kicker on a main-slate team has a DK salary (**306/306**), as does every Week 8-ranked one (**242/242**). Of 554 DK players, 306 have a PFF projection and 394 match at least one PFF source. The 248 DK players without a projection are mostly deep backups PFF didn't project, or DK-tagged IR (53) / OUT (5) / Q (5).
- **DK players ≥ $4,000 with no PFF match in any file:** 60 — 59 are at DK's $4,000 floor (backup QBs/RBs/FBs PFF doesn't list), plus James Conner (ARI RB, $4,700, IR).
- **Team changes (name matches, team differs, so not joined):** Jimmy Horn Jr. (DK CLE / PFF season CAR), Ryan Miller (DK NE / season MIA), Marquez Valdes-Scantling (DK PIT / season LAC); all $3,000 on DK. Their 2026 season stats sit on a separate master row under the old team. (Andy Dalton ATL and Jared Wayne MIA now match on their new teams.)
- **Projected QB/RB/WR/TE (358):** W8 rank 266, Week 7 stats 258, Week 7 expected 214, season stats 339, Oct 8 grade 221, 3-yr trend 296, DK salary 284. Players not on main-slate teams have no salary.
- **Oddity:** Josh Oliver (MIN TE) has a PFF projection (2.4) but DK lists him IR.

## Data issues and as-of notes
- **Week 8 byes: HOU, NO, NYG, SF** (absent from PFF Week 8 projections and rankings; projections have 28 DST teams). In master they are marked `opponent = BYE`, `bye_week = 8` *(derived)*.
- **Thursday game CAR @ GB (Oct 29, 8:15 PM ET) is NOT on the DK main slate** and had not been played when this was built. Also off the main slate: **PHI @ WAS** (Sunday night Nov 1, 8:20 PM ET) and **CHI @ SEA** (Monday night Nov 2, 8:15 PM ET) — both in DK's Sun–Mon 13-game slate. All flagged in `week8_note`; these players have PFF projections but no DK salary. (DK's Thu–Mon slate has 14 games = all 28 non-bye teams.)
- **Main slate games (11):** ARI@DAL, ATL@TB, BAL@BUF, CLE@PIT, IND@JAX, LV@NYJ, MIN@DET, TEN@CIN (1:00 PM ET); LAC@LAR (4:05 PM ET); KC@DEN, NE@MIA (4:25 PM ET). Times are ET as listed by DK (Nov 1 is after the DST change: 1:00 PM ET = 8:00 AM HST).
- **Season-to-date = Weeks 1–7** (22 teams with 7 games, 10 with 6 because of byes). Season = Week 7 package season + Week 7 for all players present in both (no difference > 0.15 pts) — no stat corrections spotted.
- **Season files carry PFF's default minimum-snaps filter**, so low-usage players may be missing from `season_stats_*` (and so have blank season columns). One QB row (Davis Mills, HOU) shows 0 games / 0 pts.
- **Week 7 files:** byes in Week 7 were BUF, JAX, LAC, WAS (DST file has 28 teams). Week 7 stats for NE and CHI are their Thursday Oct 22 game.
- **Injury tags differ by source:** e.g., Lamar Jackson is PROB in PFF rankings but Q on DK; Amon-Ra St. Brown is ACTIVE in PFF but Q on DK. Check news before lock.
- **Not refreshed since Oct 8:** player grades (through Week 4), team grades, SOS. There are no ROS rankings, and no Vegas lines or implied totals.
- DK `dk_avg_ppg` is DraftKings' own number and won't exactly match PFF season PPG.

## History (in `data/pff/history/`)
Same files as the Oct 8 / Week 6 / Week 7 packages: `history_stats_{QB,skill,K,DST}_2020_2025.csv` (2026 rows there are the **Oct 8** partial, through Week 4; the fresher 2026 numbers are in this folder's `season_stats_*`), `history_expected_points_2024_2025.csv`, `history_player_grades_2020_2025.csv`, `history_team_grades_2020_2025.csv` (REGPO exceptions: team 2020, QB 2020, HB 2021, WR 2023, TE 2023), `player_trends.csv`, `team_trends.csv`, `PFF_History_2020_2025.xlsx`.

---

## Starter prompt for Claude (copy/paste)

> I've attached a PFF + DraftKings data package for **NFL 2026 Week 8** (Sunday Nov 1 main slate). Read `README_for_Claude.md` first, then use `master_players_week8.csv` (or the first tab of `PFF_Week8_2026.xlsx`) as the main table. Use only this data. Don't invent salaries, injuries, news or Vegas lines; if something's missing, say so.
>
> **Contest:** DraftKings NFL **Classic**, **$50,000 salary cap**, roster **QB, RB, RB, WR, WR, WR, TE, FLEX (RB/WR/TE), DST**. Full PPR, plus DK's +3 bonuses at 300 pass / 100 rush / 100 rec yards. Only players with `on_dk_main_slate = True` and a `dk_salary` are eligible. Exclude dk_status OUT/IR and flag Q.
>
> Please:
> 1. **Player pool by position:** proj_fpts, dk_salary, dk_value_pts_per_1k, Week 8 rank, Week 7 usage (targets, carries, red-zone and end-zone looks, aDOT), Week 7 actual vs expected (`w7_fpts_minus_expected`), season PPG vs 3-yr average, and matchup (sos_wk8_asof_oct8, opponent defense grades).
> 2. **Cash lineup (50/50, double-ups):** maximize floor. Prioritize high-volume players (targets/carries), strong projections per $1K, and players whose expected points ≥ actual (not reliant on TD luck). Avoid Q tags.
> 3. **3 GPP lineups (tournaments):** higher ceiling and leverage. Include **QB + 1–2 pass-catcher stacks** from the same team, with a **bring-back** from the opponent (same `dk_game`). Use cheaper value plays to fit studs, and players who underperformed expected points in Week 7 (likely lower ownership, positive regression). Make the three lineups meaningfully different.
> 4. Each lineup must total ≤ $50,000 and fill every slot exactly once. Show salary used, total projected points, and a one-line reason per player.
> 5. Note risks: byes (HOU, NO, NYG, SF), CAR@GB (Thursday), PHI@WAS (Sunday night) and CHI@SEA (Monday night) are not on this slate, late-game swaps (4:05/4:25 PM ET games), and anything stale (grades/SOS as of Oct 8).
>
> My own season-long roster and opponents will be supplied separately.
