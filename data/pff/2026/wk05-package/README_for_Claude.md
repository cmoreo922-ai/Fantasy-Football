# PFF Week 5 2026 Fantasy Data Package (PPR)

**Source:** PFF+ (Pro Football Focus) exports, downloaded **Oct 8, 2026**. NFL **2026 season, current week = Week 5**. All fantasy scoring is **PPR**.
**Also included:** 2020–2025 season history and player/team trends in `history/`.
**Owner:** Christopher (fantasy football + DFS). His own roster and opponents' rosters will be supplied separately.

Every value comes straight from the PFF exports. Nothing was invented: blank means the source didn't have it. A few columns are **derived** (simple arithmetic on PFF values). They're marked *(derived)* below.

---

## Files

| File | Rows | What it is |
|---|---|---|
| `master_players_week5.csv` | 584 | **Start here.** One row per player (QB/RB/WR/TE/K/DST). Joins Week 5 projection, Week 5 rank, ROS rank, season stats, expected points, PFF grades, SOS, and team/opponent PFF grades. |
| `PFF_Week5_2026.xlsx` | — | Workbook: master sheet first, then `player_trends` (history), then every 2026 dataset below as its own tab (header row frozen, filters on). |
| `history/` | — | **2020–2025 history + trends** (see “History 2020–2025” section). Includes `PFF_History_2020_2025.xlsx` with all history tabs. |
| `week5_projections.csv` | 449 | PFF Week 5 projections (offense 389, K 30, DST 30). |
| `week5_rankings.csv` | 340 | PFF Week 5 rankings: positional, FLEX, and SUPERFLEX ranks (QB 30, RB 85, WR 115, TE 50, K 30, DST 30). |
| `ros_rankings.csv` | 447 | PFF rest-of-season rankings as of Week 5 (QB 64, RB 128, WR 191, TE 64). No K/DST. |
| `season_stats_QB.csv` | 54 | 2026 season-to-date passing/rushing stats and fantasy points, QBs. |
| `season_stats_skill.csv` | 432 | 2026 season-to-date receiving and rushing stats and fantasy points, RB/WR/TE. |
| `season_stats_K.csv` | 32 | 2026 kicking stats and fantasy points. |
| `season_stats_DST.csv` | 32 | 2026 team defense/special teams stats and fantasy points. |
| `season_stats_IDP.csv` | 758 | 2026 individual defensive player stats (IDP). Fantasy points are all 0 in the export (see Data notes). |
| `expected_points_QB.csv` | 51 | 2026 actual vs **expected** fantasy points (xFP), QBs. |
| `expected_points_skill.csv` | 379 | 2026 actual vs expected fantasy points, RB/WR/TE. |
| `player_grades_2026.csv` | 293 | PFF 2026 player grades (0–100) and snap counts: QB 37, RB/HB 62, WR 115, TE 79. Parsed from PDFs of premium.pff.com. |
| `team_grades_2026.csv` | 32 | PFF 2026 team grades (Reg + Post), with record and points for/against. |
| `sos_by_position.csv` | 160 | PFF fantasy strength of schedule by position (QB/RB/WR/TE/DST × 32 teams), Weeks 5–17. |
| `power_ratings.csv` | 32 | PFF NFL power ratings **before Week 5**. |

## Conventions
- **Team codes** use standard NFL abbreviations everywhere. PFF's own codes were converted: ARZ→ARI, BLT→BAL, CLV→CLE, HST→HOU, LA→LAR.
- **Positions:** QB, RB, WR, TE, K, DST. PFF grade pages label RBs as "HB". That label is kept in `player_grades_2026.pff_position_label`, but `position` = RB.
- **Bye in Week 5: KC and CAR.** These teams have no Week 5 projection or Week 5 rank. `opponent` = `BYE`.

---

## Column guide

### master_players_week5.csv
| Column | Meaning |
|---|---|
| player, position, team | Player identity (team = current team per projections/rankings) |
| opponent, home_away | Week 5 opponent and home/away, from projections. For players without a projection row, this is taken from their team's Week 5 game in projections. `BYE` = team on bye. |
| bye_week | Bye week |
| injury_status_w5 | PFF injury status from the Week 5 rankings (falls back to ROS rankings): ACTIVE, QUEST (questionable), DOUBT, OUT, PROB |
| proj_fpts | PFF Week 5 projected PPR fantasy points |
| proj_rank_overall | PFF's overall rank by projected points (all positions, from the export) |
| proj_pos_rank | *(derived)* rank of proj_fpts within position |
| w5_pos_rank / w5_flex_rank / w5_superflex_rank | PFF Week 5 **expert rankings** (positional; FLEX = RB/WR/TE combined; SUPERFLEX = QB/RB/WR/TE combined) |
| ros_pos_rank / ros_flex_rank | PFF rest-of-season rankings (positional; FLEX for RB/WR/TE) |
| season_games, season_fpts | 2026 games played and total PPR fantasy points |
| season_fppg | *(derived)* season_fpts / season_games |
| xfp_games, xfp_actual_fpts, xfp_expected_fpts | Games and actual vs expected PPR points from PFF's expected-points model |
| xfp_fpts_over_expected, xfp_ppg_over_expected | Actual minus expected (total and per game). **Positive = outperforming expected** (possible TD/efficiency luck). **Negative = underperforming** (possible buy-low). |
| xfp_actual_ppg, xfp_expected_ppg | Per-game actual and expected points |
| sos_wk5 | Position-specific fantasy matchup score for Week 5 (0–10, **higher = more favorable**; see SOS notes) |
| sos_season_wk5_14 / sos_playoffs_wk15_17 / sos_all_wk5_17 | Position SOS for the rest of the fantasy regular season, fantasy playoffs, and all remaining weeks |
| pff_grade_off | PFF overall offensive grade (0–100), 2026 season |
| pff_grade_pos_rank | PFF grade rank among that position (PFF requires a snap minimum) |
| pff_grade_pass / run / recv / pblk / rblk | PFF sub-grades: passing, running, receiving, pass blocking, run blocking |
| pff_snaps_off | Offensive snaps (from the grades page) |
| team_pff_off_grade | Player's team PFF offense grade (team_grades_2026) |
| opp_pff_def_grade / opp_pff_rdef_grade / opp_pff_prsh_grade / opp_pff_cov_grade | Week 5 **opponent's** PFF team defense, run defense, pass rush, and coverage grades. Higher = better defense, so a tougher matchup. |
| proj_* (pass_att … rec_td) | Week 5 projected stat line |
| season_* (pass_att … rush_td) | Season-to-date stat totals |
| sources_matched | Which datasets this player was found in: proj, w5, ros, stats, xfp, grades |
| join_flags | Join caveats (position conflicts, same name on a different team) |

### week5_projections.csv
proj_rank_overall, proj_pos_rank *(derived)*, player, team, position, opponent, home_away, bye_week, proj_fpts, then the projected stat line: pass_comp/att/yds/td/int/sacked, rush_att/yds/td, recv_targets/receptions/yds/td, fumbles, fumbles_lost, two_pt, return_yds/td. Kicker columns: fg_madeXXXX / fg_attXXXX by distance band (0–19, 20–29, 30–39, 40–49, 50+), pat_made/att. DST columns: dst_sacks, safeties, int, fumbles_forced/recovered, td, return_yds/td. dst_ptsX = **probability** that the defense allows that points band (0, 1–6, 7–13, 14–20, 21–27, 28–34, 35+). These sum to about 1. The all-zero IDP projection columns were dropped.

### week5_rankings.csv / ros_rankings.csv
player, team, position, positional rank, FLEX rank (RB/WR/TE), SUPERFLEX rank (Week 5 only), bye_week, injury_status.

### season_stats_* (PFF field names, converted to snake_case)
- **QB:** dropbacks, att, comp, drops (dropped passes), com_drop (completion % with drops counted as completions), yds, pass_yds300_games, depth_aim (average depth of target), tds, td40s/td50s (40+/50+ yd TDs), ints, sks, ez_* (end-zone attempts/TDs/INTs/%), rush_carries/yds/tds, rz_rush_* (red-zone), i5_rush_* (inside-5), pat_*, fantasy_pts, fantasy_ppg *(derived)*, pts_per_db (fantasy points per dropback).
- **Skill:** rec_targ, rec_rec, rec_yds, rec_tds, rec_drops, catch (catch %), depth (aDOT), ypt (yds/target), ypr (yds/reception), rac (yards after catch per rec), rz_rec_* and ez_rec_* (red-zone/end-zone targets, receptions, TDs, shares), rush_carries, rush_yds, rush_tds, ypc, yac (yards after contact), rush_ta / tat (tackles avoided / per attempt, as labeled by PFF), rz_rush_*, i5_rush_*, fumbles, fantasy_pts, fantasy_ppg *(derived)*, pts_per_snap, pts_per_touch.
- **K:** completeNN/attemptNN/pctNN = FG made/att/% by distance band (19 = 0–19, 29 = 20–29, 39, 49, 50 = 50+). eps_* = extra points.
- **DST:** sacks, fumble_recoveries, interceptions, defense_touchdowns, safeties, blocked_kicks, kick/punt return yds & TDs, pa_per_game (points allowed/game), paXX_games (games in each points-allowed band), pass/run_yds_per_game allowed, yaXX_games (games in each yards-allowed band), fantasy_pts, fantasy_ppg.
- **IDP:** tkl, ass (assists), tfl, sks, safety, ints, pd (passes defended), ff, fr, touchdowns, blocked_kicks, tpop / qbp / skcon / ta_percent / pob (PFF pressure/sack/tackle-efficiency metrics, exact definitions not given in the export), fantasy_pts, pts_per_opp.

### expected_points_*
fpts, x_fpts, fpts_minus_x_fpts, ppg, x_ppg, ppg_minus_x_ppg, games, then actual vs expected component stats (QB: passing_att, com vs x_com, int vs x_int, yds vs x_yds, td vs x_td; skill: receiving rec/yds/td and rushing yds/td, each with an x_ version).

### player_grades_2026.csv
pff_pos_rank, player, team, jersey, position, pff_position_label, grade_off, grade_pass, grade_run, grade_recv, grade_pblk, grade_rblk (0–100; about 60 = average, 70+ = good, 80+ = high-quality, 90+ = elite on PFF's scale), snaps_off/pass/run/recv/pblk/rblk, age, roster_status (A = active, IR = injured reserve, P = as shown by PFF). Blank grade = no snaps of that type.

### team_grades_2026.csv
team, team_name, record, points_for, points_against, grade_overall, grade_off, grade_pass, grade_pblk, grade_recv, grade_run, grade_rblk, grade_def, grade_rdef (run defense), grade_tack (tackling), grade_prsh (pass rush), grade_cov (coverage).

### sos_by_position.csv
position (offense position, or DST), team, wk5…wk17 (matchup score for that week, 0–10; **blank = bye**), season_games_wk5_14 / season_sos_wk5_14, playoffs_games_wk15_17 / playoffs_sos_wk15_17, all_games_wk5_17 / all_sos_wk5_17.
**Direction (inferred from the data, not stated in the export):** a higher number means an easier, more fantasy-friendly schedule. Evidence: the Week 5 QB score correlates +0.48 with the opponent's passing yards allowed per game and −0.57 with the opponent's power rating. Josh Allen (BUF) vs LAR, the #1 power-rated team, scores 0.00. The scale looks min-max normalized (0 = toughest, 10 = easiest in the set).

### power_ratings.csv (pre-Week 5)
spread_rating_pts (PFF point-spread power rating: points better or worse than an average team), spread_rating_qb_component (QB portion of that rating), sos_to_date_rank, sos_remaining_rank (1–32; the export doesn't say which direction), proj_avg_wins, proj_make_playoffs_pct, proj_win_division_pct, proj_win_conference_pct, proj_win_super_bowl_pct.

---

## Join method and match results
- **Join key:** normalized player name + team. Normalization: lowercase, accents/punctuation removed, Jr./Sr./II/III/IV/V dropped, team codes standardized. Position is then checked: 1 conflict, flagged and merged (Jackson Meeks, DET: TE in projections, WR in stats/xFP). K uses name + team. DST uses team.
- **Team codes matched across all sources** (0 team conflicts), except 1 name: **Xavier Smith** is LAR in season stats/xFP but SF in the WR grades PDF. Not merged; both rows are flagged.
- **Coverage, by source (rows that also have a Week 5 projection):** Week 5 rankings 333/340 (97.9%). ROS 346/447 (77.4%). Season stats 412/527* (78.2%). xFP 326/430 (75.8%). PFF grades 243/293 (82.9%).
  - The 7 ranked-but-not-projected players have no PFF projection row (Sean Tucker, Nicholas Singleton, Jordan James, Marquez Valdes-Scantling, Elijah Sarratt, Jalen Tolbert, Jelani Woods).
  - Of the 101 ROS players with no projection: 29 are on KC/CAR (bye), 30 are OUT, 18 QUEST, 24 ACTIVE but not projected by PFF.
  - *527 = 54 QB + 432 skill + 32 K + 32 DST, minus the 23 zero-point rows excluded below.
- **Of the 389 projected offensive players:** Week 5 rank 70%, ROS rank 89%, season stats 90%, xFP 84%, PFF grade 62%. The grades pages only list players above PFF's snap threshold, and Week 5 rankings cover fewer players than projections.
- No unmatched row was caused by a name-spelling difference. I checked every single-source row for a same-last-name, same-team, same-position candidate and found none. All gaps reflect coverage differences between the exports.
- **Excluded from the master (still in `season_stats_skill.csv`):** 23 players who appear only in season stats with 0.0 fantasy points.

## Data notes and issues
- The ROS **SUPERFLEX** export is not a true combined ranking. It is the QB list plus the FLEX list concatenated, with duplicate "overall" ranks (e.g., Josh Allen and Kenneth Walker III are both #1). Only positional and FLEX ROS ranks are used. The Week 5 SUPERFLEX ranking is a real combined list (1–280) and is included.
- Several downloaded ranking files were byte-identical duplicates and were ignored: the unnumbered file plus (1)–(5) of the ROS exports. `expected-fantasy-points (1).csv` was header-only.
- IDP fantasy points and pts_per_opp are 0 for every row in the export (no IDP scoring configured). The raw IDP stats are fine. IDP projection columns were all 0 and were dropped.
- A few defensive players appear in the skill stats tagged RB (e.g., Jalen Ramsey, Pat Surtain II, Cooper DeJean, Talanoa Hufanga) with 0 points. They are excluded from the master by the zero-point rule.
- Blanks: QB depth_aim and pts_per_db are blank for players with no attempts. pts_per_touch is blank for skill players with no touches.
- **PFF grades** were parsed from PDFs using word coordinates. Row counts match the page totals exactly: QB 37/37, HB 62/62, WR 115/115, TE 79/79, teams 32/32. Site overlay text garbled a few lines in the plain-text extracts (e.g., James Cook, Xavier Hutchinson), but these rows were recovered from the PDF coordinates. Age = 0.0 in the PDF was treated as missing (blank).
- Team grades: the special-teams (SP) column is truncated to a single digit in the PDF, so it was **excluded**. The PDF has no team rank values.
- Grades and stats cover only about 4 games. Treat them as small samples.

## Known gaps
- **No DFS salaries** (DraftKings/FanDuel), so "value" must be judged against salaries supplied separately.
- No Vegas lines or implied team totals. No weekly game logs or snap/target-share trends (season totals only).
- **No ROS projections.** No ROS K/DST rankings.
- **Power ratings are pre-Week 5.**
- Team SP grade is unavailable (truncated in source).
- **History:** no expected-points data before 2024; no historical projections/rankings/SOS; no game-level logs, so no fantasy points allowed by position. Historical team coverage (COV) and special-teams grades are truncated in the PDFs and excluded.

---

## History 2020–2025 (folder `history/`)

**Source:** PFF+ fantasy stats exports, **PPR, regular season, all weeks, all teams**, seasons 2020–2025 (+ PFF expected fantasy points for 2024–2025). Same PFF field names and cleaning as the 2026 files (snake_case, standard team codes ARZ→ARI, BLT→BAL, CLV→CLE, HST→HOU, LA→LAR).
**2026 rows are included** in each history file as `season=2026, partial=True` (copied from the 2026 season-to-date files, ~4 games), so one file shows the full trend. Filter `partial==False` for complete seasons only. Seasons were sanity-checked: max games 16 in 2020 and 17 from 2021 (18 for one player each in 2024/2025 who was traded mid-season); rookies first appear in their draft year (e.g., Ja'Marr Chase 2021, Bijan Robinson 2023, Jayden Daniels 2024, Cam Ward 2025).

| File | Rows | What it is |
|---|---|---|
| `history/player_trends.csv` | 552 | **Start here for trends.** One row per 2026 player in the master sheet (QB/RB/WR/TE/K; DST is in team_trends). Season-by-season PPG, games, total points, positional finish, team, 2020–2025 + 2026-to-date. |
| `history/team_trends.csv` | 224 | Per team per season (2020–2026td): DST fantasy output and points/yards allowed, plus team offensive fantasy points by position (summed from player rows). |
| `history/history_stats_QB_2020_2025.csv` | 550 | QB season stats (2020: 83, 2021: 84, 2022: 85, 2023: 83, 2024: 79, 2025: 82, 2026td: 54) |
| `history/history_stats_skill_2020_2025.csv` | 3,827 | RB/WR/TE season stats (2020: 562, 2021: 604, 2022: 562, 2023: 550, 2024: 558, 2025: 559, 2026td: 432) |
| `history/history_stats_K_2020_2025.csv` | 300 | Kicker season stats (47, 49, 44, 40, 45, 43, 2026td: 32) |
| `history/history_stats_DST_2020_2025.csv` | 224 | Team DST season stats (32 per season) |
| `history/history_expected_points_2024_2025.csv` | 1,577 | Expected fantasy points, QB + RB/WR/TE, 2024 (567), 2025 (580), 2026td (430) |
| `history/history_player_grades_2020_2025.csv` | 3,361 | PFF player grades 2020–2025 (QB Passing, RB/HB Rushing, WR/TE Receiving reports) |
| `history/history_team_grades_2020_2025.csv` | 192 | PFF team grades 2020–2025 (32 per season) |
| `history/PFF_History_2020_2025.xlsx` | — | Workbook with all of the above as tabs |

### History column notes
- `season`, `partial` (True = 2026 season-to-date) prepended to every history file; all other columns are identical to the 2026 `season_stats_*` / `expected_points_*` files.
- `pos_finish_rank` (QB/skill/K) / `dst_finish_rank` *(derived)*: rank by **total PPR points** within the position PFF listed that season (1 = top scorer). For 2026 it is the rank to date.
- `fantasy_ppg` *(derived where PFF didn't supply it)* = fantasy_pts / games.
- Expected points: 2024–2025 QB files include extra columns not in the 2026 export — `scrambles_yds/x_yds/td/x_td`, `designed_runs_yds/x_yds/td/x_td` (blank for 2026 and for RB/WR/TE). Skill-only columns (receiving_*, rushing_*) are blank for QBs.

### player_trends.csv
| Column | Meaning |
|---|---|
| player, position, team_2026 | From the 2026 master sheet |
| proj_fpts, w5_pos_rank, ros_pos_rank | 2026 Week 5 context (from master) |
| ppg_2020 … ppg_2025, ppg_2026_td | PPR points per game each season (2026 = to date) |
| ppg_3yr_avg_2023_2025 | *(derived)* total points ÷ total games over 2023–2025 (seasons played only); `seasons_in_3yr_avg` = how many of those seasons the player appears in |
| ppg_2026td_vs_3yr_avg | 2026-to-date PPG minus 3-year average (positive = running hot vs. his baseline) |
| ppg_change_2026td_vs_2025, ppg_change_YYYY_vs_YYYY-1 | Year-over-year PPG change |
| gp_YYYY, fpts_YYYY | Games played and total PPR points per season |
| pos_rank_YYYY | Positional finish (by total points) per season |
| team_YYYY | Team PFF listed for that season (one team per player-season) |
| team_changes | Team sequence changes 2020→2026 (e.g., `SEA->KC`); `changed_team_since_2025` = 2025 team ≠ 2026 team (111 players) |
| seasons_in_history, first_season_in_data | Count of 2020–2025 seasons found; first season present |
| hist_match | How history was joined: `name+position`, `name only (history position X)` (3 players whose listed position changed: Connor Heyward, Antonio Williams, Jackson Meeks), or `no history 2020-2025` (82 — no row in any 2020–2025 export, e.g. rookies) |

### team_trends.csv
season, partial, team, team_games; **DST:** dst_fpts, dst_fppg, dst_finish_rank, def_points_allowed_pg (real NFL points allowed per game), def_pass_yds_allowed_pg, def_run_yds_allowed_pg, dst_sacks, dst_int, dst_fum_rec, dst_def_td; **Offense:** off_fpts_QB / RB / WR / TE / K (sum of PPR points of players PFF listed on that team that season), off_fpts_QB_RB_WR_TE, off_fppg_QB_RB_WR_TE (÷ team_games), off_rank_QB_RB_WR_TE (1 = most), k_games_attributed (sum of games of kickers listed on the team — a check on attribution).
**Not derivable from these exports:** fantasy points *allowed by position* (no opponent/game-level data). Use def_points_allowed_pg / pass & run yards allowed and the 2026 SOS file instead.

### History join and match rate
- Join: normalized name + position (same normalization as the master); 2026-to-date values join on name + team like the master. Fallback to name only when the name has exactly one historical position and is unique in 2026 (3 players, flagged).
- **2026 players with any 2020–2025 history: 470 / 552 = 85.1%** (QB 87.7%, RB 85.3%, WR 83.3%, TE 85.0%, K 90.6%). Among Week 5-ranked players: 278/310 (89.7%); projected players: 363/419 (86.6%). The 82 without history have no row in any 2020–2025 export — this includes 2026 rookies and players who recorded no fantasy stats in those seasons (top projected examples: Jalon Daniels, Dohnte Meyers, Jeremiyah Love, Carnell Tate).
- Name collisions across seasons (two different players with the same name and position in different years) cannot be fully ruled out from these exports; no duplicate name+position exists within any single season.

### PFF grades history
**Season type:** `REG` = regular season only. **`REGPO`** (regular + postseason) was used for: team grades 2020, QB 2020, HB/RB 2021, WR 2023, TE 2023. All other grade files are REG. Games and stats in REGPO files include playoff games, so they won't match the regular-season stat files exactly for those seasons.
**Report type** (`report` column): QBs come from PFF's **Passing** report, RBs from the **Rushing** report (PFF labels them HB; stored as position=RB), WR and TE from the **Receiving** report. Columns differ by report; position-specific columns are blank where they don't apply.
| Columns | Applies to | Meaning |
|---|---|---|
| pff_rank | all | Rank on that report (by the report's main grade; ties share a rank and the next ranks are skipped) |
| jersey, games | all | Jersey number, games played |
| dropbacks, att, comp, comp_pct, pass_yds, ypa, pass_td, ints | QB | Base passing stats |
| grade_off, grade_pass, grade_run, grade_fum | QB | Overall offense, passing, rushing, ball-security grades (0–100) |
| btt | QB | Big-time throws (count). The BTT% column is cut off in the PDF and excluded |
| snaps, att, rush_yds, ypa, rush_td, fumbles | RB | Base rushing stats (att = carries) |
| grade_off, grade_run, grade_fum, grade_rblk | RB | Overall, rushing, ball-security, run-blocking grades |
| yco, yco_per_att, mtf | RB | Yards after contact, per attempt, missed tackles forced |
| targets, rec, rec_pct, rec_yds, yds_per_rec, rec_td | WR, TE | Base receiving stats |
| grade_off, grade_recv, grade_drop, grade_fum, grade_pblk | WR, TE | Overall, receiving, drop, ball-security, pass-blocking grades |
| snaps_pass, snaps_recv | WR, TE | The two snap-count columns labeled PASS and RECV after the grades (their group header isn't visible in the PDF) |
**Not available (columns cut off at the PDF's right edge):** the reports are wider than the PDF page. For QB, the last visible column (a second `BTT` header, likely BTT%) shows truncated values and is excluded. For team grades, the `CO[V]` column is truncated and excluded, and special teams isn't visible. The WR/TE report's own description says it includes passer rating when targeted, but that column isn't on the page. Any further columns past the edge of the HB, WR or TE reports aren't captured. Blank grades mean PFF didn't assign one (too few snaps), not a parsing miss.
**Row counts (parsed vs expected, all exact):** QB 80/76/82/77/75/76, RB 142/147/144/130/132/136, WR 222/234/226/212/221/223, TE 125/122/118/117/119/125 (2020–2025), teams 32 each.
**Joined into the trend tables:**
- `player_trends.csv`: `grade_YYYY` (overall offensive grade), `subgrade_YYYY` (QB passing / RB rushing / WR+TE receiving), `grade_rank_YYYY` for 2020–2025; `grade_2026` (2026 season-to-date overall grade from the master sheet); `grade_3yr_avg_2023_2025` *(derived, simple mean of seasons present)*; `subgrade_metric` says which sub-grade the `subgrade_YYYY` columns hold. K has no grade columns (PFF has no kicker grades here).
- `team_trends.csv`: `team_grade_overall/off/pass/pblk/recv/run/rblk/def/rdef/tack/prsh` per season, including 2026-to-date (2026 coverage grade exists in the 2026 team file but not historically, so it isn't here).
- **Match rate:** of the 441 non-kicker 2026 players who have any 2020–2025 stats, 425 (96.4%) have at least one historical grade. Per season, 93–95% of those players' stat seasons also have a grade (e.g., 2025: 404 of 425). The gaps are players below PFF's snap minimum for a grade. Across all 3,361 grade rows, 3,360 match a same-season stats row; the one that doesn't is Jacob Harris (WR, LAR, 2022, 2 games).
- "Washington Football Team" (2021 team grades) is mapped to WAS.

### History data issues
- **One team per player-season:** PFF lists a single team for each player-season even if he changed teams mid-year (e.g., DET 2023 has only 4 kicker games attributed — Michael Badgley, 26 pts — for a 17-game season, while CLE 2023 has 29). Team-level sums in team_trends are approximate for those cases — see `k_games_attributed` vs `team_games` (25 team-seasons differ by ≥3 kicker games).
- 2020 was a 16-game season — compare **PPG**, not totals, across years.
- `pts_per_touch`, `pts_per_snap`, `depth_aim`, `pts_per_db` are blank where the player had no touches/snaps/attempts (as in the source).
- Header-only exports (fantasy-stats-receiving (2)–(6), (8)) were ignored.

---

## Starter prompt for Claude (copy/paste)

> I've attached a PFF data package for the **2026 NFL season, Week 5** (PPR scoring), exported from PFF+ on Oct 8, 2026. Please read `README_for_Claude.md` first, then use `master_players_week5.csv` as the primary table (or the `master_players_week5` tab in `PFF_Week5_2026.xlsx`). The other files are supporting detail. Use only the data in these files. Don't invent stats, injuries, or news. If something isn't in the data, say so.
>
> For **Week 5**, please give me:
> 1. **Start/sit tiers by position** (QB, RB, WR, TE, FLEX, K, DST) based on `proj_fpts`, `w5_pos_rank`, and matchup (`sos_wk5`, opponent PFF defense grades). Note injury status (QUEST/DOUBT/OUT) and teams on bye (KC, CAR).
> 2. **DFS targets:**
>    - **High-ceiling / tournament plays:** strong projections plus favorable matchups, high PFF offense grades, heavy usage (targets/carries), and red-zone or end-zone involvement.
>    - **Value plays:** players projected or ranked well above their usual tier or season average, or with strong expected-points profiles (high `xfp_expected_ppg`) on good matchups. I'll supply salaries separately; until then, flag candidates.
> 3. **Expected vs actual:** the biggest **overperformers** (`xfp_ppg_over_expected` most positive; regression risk) and **underperformers** (most negative; buy-low or bounce-back candidates), with a Week 5 view on each.
> 4. **Favorable schedule:** players and teams with the best `sos_wk5` and best `sos_season_wk5_14` / `sos_playoffs_wk15_17` at their position. These are useful for waivers and trades.
> 5. A short list of **stacks** (QB + pass catchers from the same team) and **game environments** worth targeting, based on the projections.
>
> 6. **Trends (use `history/player_trends.csv` and `history/team_trends.csv`):** for the players you recommend, compare 2026-to-date PPG with their 2023–2025 average (`ppg_3yr_avg_2023_2025`, `ppg_2026td_vs_3yr_avg`) and past positional finishes; flag players who changed teams (`team_changes`), who are far above their career baseline (sustainability risk) or far below it (bounce-back candidates), and rookies with no history. Also use `grade_YYYY` / `subgrade_YYYY` and `team_grade_*` to see whether the production was backed by PFF grades (note which seasons are REGPO). Remember 2026 is only ~4 games and 2020 was a 16-game season (compare PPG).
>
> Show key numbers in compact tables. **My own roster and my opponents' rosters will be supplied separately.** After that, I'll ask you to optimize my lineup and compare my team against opponents.
