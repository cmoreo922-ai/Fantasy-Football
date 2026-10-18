# PFF Week 6 2026 package — DraftKings lineup build (PPR)

**Owner:** Christopher. **Season:** NFL 2026. **Upcoming:** Week 6 (Sunday Oct 18, 2026 slate). **Most recent completed week:** Week 5.
**Sources:**
- **PFF+** (Pro Football Focus) exports, downloaded **Oct 17, 2026**: Week 5 single-week stats and expected points, 2026 season-to-date stats, Week 6 projections, Week 6 PPR rankings.
- **DraftKings** public NFL lobby salary export (no login): Classic **main slate**, DraftGroupId **154941**, 10 games, first lock Sun Oct 18 1:00 PM ET. Fetched **2026-10-18 02:33 UTC (Sat Oct 17, 4:33 PM HST)** from `https://www.draftkings.com/lineup/getavailableplayerscsv?contestTypeId=21&draftGroupId=154941`. The raw file is `dk_raw/DKSalaries_154941.csv`. Salaries and injury statuses can change before lock, so re-download before entering contests.
- **Carried over from the Oct 8 build** (labeled `_asof_oct8`): PFF 2026 player grades (through Week 4), team grades, and SOS. **History** 2020–2025 (stats, expected points, PFF grades, player/team trends) is in `history/`. See `history/` file notes below and in the Oct 8 package README.

Scoring: PFF projections are **full PPR**. I verified this by regression on the projected stat lines: 1.005 pts per reception, 0.04/pass yd, 4/pass TD, −1/INT, 0.1/rush or rec yd, 6/TD, MAE 0.05 vs PPR. PFF projections **don't include DraftKings' yardage bonuses** (+3 for 300 pass / 100 rush / 100 rec yds), so DK scores can exceed them slightly. Nothing in this package was invented. Blank means the source didn't have the value. *(derived)* marks simple arithmetic.

## Files
| File | Rows | What |
|---|---|---|
| `master_players_week6.csv` | 779 | **Start here.** One row per player: DK salary/game, Week 6 projection and ranks, Week 5 actuals, usage and expected points, 2026 season-to-date, trends, grades and SOS (as of Oct 8) |
| `PFF_Week6_2026.xlsx` | — | Master first, then every dataset as a tab (header frozen, filters) |
| `dk_salaries_week6_main.csv` | 526 | DraftKings main-slate salaries (QB 70, RB 122, WR 194, TE 120, DST 20; 20 teams) |
| `week6_projections.csv` | 414 | PFF Week 6 projections (QB 57, RB 84, WR 137, TE 80, K 28, DST 28) |
| `week6_rankings.csv` | 333 | PFF Week 6 PPR ranks: positional + FLEX + SUPERFLEX (QB 28, RB 85, WR 114, TE 50, K 28, DST 28) |
| `week5_stats_QB/skill/K/DST.csv` | 37 / 331 / 30 / 30 | Week 5 single-game stats |
| `week5_expected_points_QB/skill.csv` | 36 / 258 | Week 5 actual vs expected fantasy points |
| `season_stats_QB/skill/K/DST.csv` | 59 / 454 / 32 / 32 | 2026 season-to-date (all weeks played so far) |
| `history/` | — | 2020–2025 history + `player_trends.csv`, `team_trends.csv`, grades history, `PFF_History_2020_2025.xlsx` |
| `dk_raw/` | — | Raw DraftKings CSV + fetch timestamp |

## Key master columns
- **Identity/game:** player, position, team, opponent, home_away, bye_week, injury_status_w6 (PFF), week6_note.
- **DraftKings:** dk_salary, dk_roster_position (e.g., RB/FLEX), dk_game, dk_game_time_et, dk_status (DK injury tag: Q/OUT/IR), dk_avg_ppg (DK's own season average), on_dk_main_slate (team plays in the 10-game main slate), dk_id.
- **dk_value_pts_per_1k** *(derived)* = proj_fpts ÷ (dk_salary / 1000). Rough guide: about 3x salary-in-thousands is a common cash target and 4x+ a GPP target. Those benchmarks are general DFS conventions, not from these files.
- **Week 6:** proj_fpts, proj_rank_overall, proj_pos_rank *(derived)*, w6_pos_rank, w6_flex_rank, w6_superflex_rank, and projected stat line (proj_pass_*, proj_rush_*, proj_targets, proj_rec, proj_rec_yds, proj_rec_td).
- **Week 5 actual/usage:** w5_fpts, w5_targets, w5_rec, w5_rec_yds, w5_rec_td, w5_adot (avg depth of target), w5_rz_targets, w5_ez_targets, w5_carries, w5_rush_yds, w5_rush_td, w5_rz_carries, w5_i5_carries (inside-5), w5_pts_per_snap. QB: w5_dropbacks, w5_pass_att, w5_pass_yds, w5_pass_td, w5_int, w5_ez_pass_att. **Snap counts and routes run are not in these exports.**
- **Week 5 expected:** w5_xfp_expected, w5_fpts_minus_expected (positive = scored above expected, so regression risk; negative = below expected, so possible bounce-back).
- **Season to date:** season_games, season_fpts, season_fppg *(derived)*, season targets, rec, yards, TDs, carries, passing.
- **Trends (history):** ppg_3yr_avg_2023_2025, ppg_2025, season_fppg_vs_3yr_avg *(derived)*, team_changes, grade_2025, grade_3yr_avg_2023_2025.
- **As of Oct 8 (not refreshed):** pff_grade_off/pass/run/recv/pos_rank_asof_oct8 (2026 grades through Week 4); sos_wk6_asof_oct8 (position matchup score 0–10; **higher = easier**, inferred, see Oct 8 README); sos_season_wk5_14 / sos_playoffs_wk15_17_asof_oct8; opp_pff_def/cov/rdef_grade_asof_oct8 (opponent team defense grades).
- **sources_matched:** proj, w6, dk, season, w5, w5x (Week 5 expected). **join_flags:** position conflicts (none this week).

## Join method and match rates
- **Key:** normalized name + team (DST by team), same as the Oct 8 build. I aliased 5 DraftKings first-name variants after a same-team/same-position/same-surname check: Kenny→Kenneth Gainwell, Hollywood→Marquise Brown, Mitchell→Mitch Trubisky, Nick→Nicholas Singleton, Matt→Matthew Hibner.
- **DraftKings coverage:** every PFF-projected non-kicker on a main-slate team has a DK salary (276/276), as does every Week 6-ranked one (215/215). Of 526 DK players, 276 have a PFF projection. The other 250 are mostly DK-tagged IR (63) or OUT (20), or deep backups PFF didn't project.
- **Projected QB/RB/WR/TE (358):** W6 rank 269, Week 5 stats 274, Week 5 expected 230, season stats 322, Oct 8 grade 217, 3-yr trend 299, DK salary 256. Players not on main-slate teams have no salary.
- No name-spelling misses remain.

## Data issues and as-of notes
- **DEN and SEA already played Week 6 (Thursday Oct 15).** Their "season-to-date" rows have 6 games and include that game. Their Week 6 projections and rankings are pre-game, and they're not on the DK Sunday main slate. Flagged in `week6_note`. Season totals for everyone else are through Week 5.
- **Week 6 byes:** CIN, DET, MIA, MIN (not in projections). Also off the main slate: HOU vs JAX (London, 9:30 AM ET), DAL @ GB (Sunday night), WAS @ SF (Monday night).
- **Week 5 DST file has 30 teams, not 29.** CAR and KC were on bye in Week 5.
- **Stat corrections:** season-to-date = previous (Oct 8) totals + Week 5 for 92–95% of players. Small differences elsewhere (e.g., Tyler Shough +0.3, Jayden Daniels +1.3, Antonio Williams −2.3) look like PFF stat corrections. Kaytron Allen (MIA) is new in the season file.
- **Not refreshed since Oct 8:** grades, SOS and team grades. There are no ROS rankings, and no Vegas lines or implied totals.
- DK `dk_avg_ppg` is DraftKings' own number and won't exactly match PFF season PPG.

## History (in `history/`)
Same files as the Oct 8 package: `history_stats_{QB,skill,K,DST}_2020_2025.csv` (2026 rows there are the **Oct 8** partial, through Week 4; the fresher 2026 numbers are in this folder's `season_stats_*`), `history_expected_points_2024_2025.csv`, `history_player_grades_2020_2025.csv`, `history_team_grades_2020_2025.csv` (REGPO exceptions: team 2020, QB 2020, HB 2021, WR 2023, TE 2023), `player_trends.csv`, `team_trends.csv`, `PFF_History_2020_2025.xlsx`.

---

## Starter prompt for Claude (copy/paste)

> I've attached a PFF + DraftKings data package for **NFL 2026 Week 6** (Sunday Oct 18 main slate). Read `README_for_Claude.md` first, then use `master_players_week6.csv` (or the first tab of `PFF_Week6_2026.xlsx`) as the main table. Use only this data. Don't invent salaries, injuries, news or Vegas lines; if something's missing, say so.
>
> **Contest:** DraftKings NFL **Classic**, **$50,000 salary cap**, roster **QB, RB, RB, WR, WR, WR, TE, FLEX (RB/WR/TE), DST**. Full PPR, plus DK's +3 bonuses at 300 pass / 100 rush / 100 rec yards. Only players with `on_dk_main_slate = True` and a `dk_salary` are eligible. Exclude dk_status OUT/IR and flag Q.
>
> Please:
> 1. **Player pool by position:** proj_fpts, dk_salary, dk_value_pts_per_1k, Week 6 rank, Week 5 usage (targets, carries, red-zone and end-zone looks, aDOT), Week 5 actual vs expected (`w5_fpts_minus_expected`), season PPG vs 3-yr average, and matchup (sos_wk6_asof_oct8, opponent defense grades).
> 2. **Cash lineup (50/50, double-ups):** maximize floor. Prioritize high-volume players (targets/carries), strong projections per $1K, and players whose expected points ≥ actual (not reliant on TD luck). Avoid Q tags.
> 3. **3 GPP lineups (tournaments):** higher ceiling and leverage. Include **QB + 1–2 pass-catcher stacks** from the same team, with a **bring-back** from the opponent (same `dk_game`). Use cheaper value plays to fit studs, and players who underperformed expected points in Week 5 (likely lower ownership, positive regression). Make the three lineups meaningfully different.
> 4. Each lineup must total ≤ $50,000 and fill every slot exactly once. Show salary used, total projected points, and a one-line reason per player.
> 5. Note risks: DEN/SEA already played (not on this slate), late-game swaps (4:05/4:25 PM ET games), and anything stale (grades/SOS as of Oct 8).
>
> My own season-long roster and opponents will be supplied separately.
