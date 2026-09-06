# Fantasy Football Research Playbook

This repo is a knowledge base + workflow for picking NFL players each week on
**DraftKings DFS** (and season-long fantasy). It's built to be used with Claude:
open a session in this repo, ask for the week's picks, and Claude follows the
research process in `.claude/skills/weekly-picks/` using the reference docs below.

## How to use it

1. Start a Claude session in this repo during the NFL week (Wed–Sun).
2. Say something like: **"Run the weekly picks process for Week 3"** or invoke
   `/weekly-picks`.
3. Claude researches the slate (Vegas lines, injuries, usage trends, weather,
   coaching tendencies), then recommends players by position with reasoning,
   split into **cash-game plays** (safe floor) and **GPP/tournament plays**
   (high ceiling, low ownership).
4. Save the week's writeup in `weeks/` so we build a track record and can
   review what worked.

## Reference docs

| Doc | What it covers |
|---|---|
| [docs/draftkings-scoring.md](docs/draftkings-scoring.md) | Exact DK Classic + Showdown scoring, roster rules, what the scoring rewards |
| [docs/scoring-formats.md](docs/scoring-formats.md) | Season-long formats: PPR, half-PPR, standard, superflex |
| [docs/dfs-strategy.md](docs/dfs-strategy.md) | Cash vs GPP, stacking, ownership/leverage, Showdown, bankroll rules |
| [docs/advanced-metrics.md](docs/advanced-metrics.md) | Target share, WOPR, air yards, snap share, red-zone usage, xFP — what actually predicts points |
| [docs/vegas-and-context.md](docs/vegas-and-context.md) | Implied team totals, spreads, weather, injury news — the weekly context layer |
| [docs/coaching-trends-2026.md](docs/coaching-trends-2026.md) | 2026 coaching/coordinator changes and what they mean for player usage |
| [docs/2025-season-review.md](docs/2025-season-review.md) | Last season's point leaders and the durable lessons they teach |
| [docs/player-movement-2026.md](docs/player-movement-2026.md) | Who switched teams, scheme fit, and preseason signals |
| [docs/rookies-2026.md](docs/rookies-2026.md) | Rookie breakout candidates and how to time rookies in DFS |
| [docs/injury-risk.md](docs/injury-risk.md) | Injury types, recurrence data, risk-scoring framework, 2026 watch list |
| [docs/data-sources.md](docs/data-sources.md) | Where to look each week for lines, ownership, injuries, snap counts, premium data |

## Weekly outputs

Each week's research gets saved as `weeks/2026-wkNN.md` using
[weeks/TEMPLATE.md](weeks/TEMPLATE.md), so we can track our process and results
over the season.
