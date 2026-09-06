# Fantasy Football Research Repo

This repo is a DraftKings NFL DFS + fantasy football research playbook, not a
software project. The user (Chris) uses Claude sessions here to research which
players to pick each week.

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
