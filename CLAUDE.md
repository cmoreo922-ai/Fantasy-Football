# Fantasy Football Research Repo

This repo is a DraftKings NFL DFS + fantasy football research playbook, not a
software project. The user (Chris) uses Claude sessions here to research which
players to pick each week.

## User profile (Chris's preferences)

- Plays **DraftKings Classic** contests only (QB / 2 RB / 3 WR / TE / FLEX /
  DST, $50K cap), NFL only, during the NFL season.
- Stakes: **serious — $100+/week.** Bankroll discipline matters: log every
  week's entries and results in `bankroll/2026-log.md`, keep single-slate
  exposure ≤5–10% of bankroll, and flag it if losses are being chased.
- Weekly deliverable: **both** a ranked player pool per position AND sample
  cash + GPP lineups (use real DK salaries when Chris pastes them in;
  otherwise organize picks by salary tier), plus the visual picks-board
  artifact and DK bulk-upload CSV.
- **Chris is on Hawaii time (HST).** Main-slate lock is ~7:00 AM HST Sunday;
  inactives drop ~5:30 AM HST — build pre-lock checklists around that.
- Preferred GPP: the big $5 Millionaire contest (150-max, ~20% paid, very
  top-heavy) — build GPP entries for ceiling/leverage, never to min-cash.
- Chris has a **PFF+ annual** subscription (decided against Fantasy Points
  Data for now — usage stats come free from PFR/Next Gen Stats). When he
  provides exports, store baselines in `data/` per docs/season-tracking.md.
- Chris's brother plays **DraftKings Pick6** (higher/lower stat-line parlays)
  and shares slips for review. Grade legs against our usage/matchup research;
  push toward 2-4 high-conviction legs; watch for trap lines (e.g. rushing-
  yard overs on reception-driven backs). Keep Pick6 a small side play.

## How to behave in this repo

- When asked for picks, lineups, "who should I play", or slate research, use
  the `/weekly-picks` skill (.claude/skills/weekly-picks/SKILL.md).
- Ground answers in `docs/` (DK scoring, DFS strategy, advanced metrics, Vegas
  context, coaching trends) and in **fresh web research** — player roles,
  injuries, depth charts, and lines change weekly; never answer from stale
  training knowledge alone.
- Save weekly analysis to `weeks/2026-wkNN.md` (copy weeks/TEMPLATE.md) and
  commit it, so we build a season-long track record.
- Update docs/coaching-trends-2026.md when coordinators/play-callers change.
- Never fabricate stats, salaries, ownership, or injury statuses; label
  estimates as estimates.
- Real money is involved: respect the bankroll guidance in docs/dfs-strategy.md
  and don't encourage oversized entries or chasing losses.
