# Advanced Metrics — What Actually Predicts Fantasy Points

Core principle: **volume/opportunity is stable and predictive; touchdowns and
efficiency are volatile.** Chase opportunity, and the points follow. A player's
usage tells you next week's range; his TD count last week tells you almost nothing.

## Opportunity metrics (the ones that matter most)

| Metric | What it is | Why it matters | Good threshold |
|---|---|---|---|
| **Target share** | % of team targets | Most stable WR/TE predictor | 20%+ startable, 25%+ alpha |
| **Targets per route run (TPRR)** | Targets ÷ routes | Best "earning targets" signal | 22%+ elite |
| **Air yards / aDOT** | Total intended downfield yards; avg depth of target | Intent + ceiling indicator | High air yards + high target share = league winner |
| **WOPR** | 1.5 × target share + 0.7 × air-yards share | Combines volume + downfield role, 0–1 scale | 0.60+ elite. Caveat: doesn't account for team pass volume |
| **Snap share** | % of offensive snaps | Leading indicator — rises *before* production | 70%+ every-down role; watch 3-week trends |
| **Route participation** | % of dropbacks running a route | Better than snaps for pass catchers | 85%+ locked in |
| **Opportunity share (RB)** | (carries + targets) ÷ team RB total | Workhorse detector | 65%+ bell cow |
| **Red-zone / inside-10 touches** | Carries + targets near the goal line | Where TDs come from | Track weekly; RZ role > total volume for TD expectation |
| **Expected fantasy points (xFP)** | Points an average player scores on that exact usage | The cleanest single opportunity number | Player scoring far *below* xFP = buy/target; far above = regression risk |

## Efficiency metrics (context, not gospel)

- **Yards per route run (YPRR):** best WR talent metric; 2.0+ good, 2.5+ elite.
- **Yards after catch, missed tackles forced, yards created:** talent signals
  that persist when a player's role grows.
- **EPA per play / success rate (team level):** identifies genuinely good
  offenses vs. teams stat-padding in garbage time.
- **Pass rate over expectation (PROE):** does a team throw more than
  game-situation predicts? High-PROE teams inflate every pass catcher; low-PROE
  (run-heavy) teams inflate RB volume. Set mostly by the coach — see
  coaching-trends doc.

## Regression signals (buy-low / sell-high detector)

- **TD regression:** a WR scoring on 15% of catches will fall back (~1 TD per
  ~15–20 targets is normal-ish); an RB with big RZ work and zero TDs will
  positively regress. In DFS this = under-owned value.
- **xFP gap:** points ≪ expected points = usage is there, results are coming.
  Points ≫ expected = fading candidate at rising ownership.
- **Deep-ball variance:** low-target, high-aDOT WRs are boom/bust — GPP-only.

## Matchup analysis (how to actually use "defense vs. position")

- Raw "fantasy points allowed to position" is noisy — adjust for the offenses
  they've faced. Prefer EPA-based or schedule-adjusted defensive metrics.
- **Where a defense is weak matters:** a defense that funnels targets to slot
  WRs or gives up RB receptions helps specific *roles*, not the whole position.
- **Cornerback matchups:** shadow corners (elite CB follows the WR1) can mute
  an alpha; the beneficiary is the WR2/slot against backups.
- **O-line vs D-line:** pressure rate ruins QB play; a bad run-blocking line
  caps RB efficiency regardless of talent.
- **Pace:** two fast-pace teams = more plays = more of everything. Two slow,
  run-heavy teams = fewer possessions, lower totals.

## The hierarchy when picking a player

1. **Role/volume** — is the usage locked in this week? (injuries, depth chart)
2. **Environment** — implied team total, game script, pace (see vegas doc)
3. **Matchup** — schedule-adjusted, role-specific
4. **Talent/efficiency** — tiebreaker between similar volumes
5. **Price & ownership** — converts a good play into a good *DFS* play
