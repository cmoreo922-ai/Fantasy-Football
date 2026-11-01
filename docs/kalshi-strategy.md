# Kalshi Strategy — Growing a $350 Bankroll

Chris's setup (Nov 2026): $350 of fun money on Kalshi, **no further deposits**.
Goal: grow it as fast as is smart, and withdraw profits to pay things down.

## How a trade works
- Every contract is yes/no, priced 1–99¢, pays $1 if it hits. Price = market's
  implied chance.
- **Use limit orders.** Claude gives a fair price; Chris sets his order a few
  cents below it, so he only gets filled when there's an edge.
- Kalshi's fee is largest near 50¢ (roughly 1–2¢ per contract), so an edge
  under ~4¢ isn't worth taking.

## Where edges come from
- Player props where PFF's projection clearly disagrees with the price (yards,
  receptions, TDs). This is our main source.
- Game lines (spread, total, halves) are usually priced close to fair. Only
  trade them when injury/weather news moves the true number before the price.
- Skip when the market disagrees with stale data on a player's **role**
  (e.g., a back just back from IR). The market usually knows more.

## Sizing — quarter Kelly
For a contract at price `p` (dollars) where our estimated chance is `q`:

    full Kelly fraction = (q − p) / (1 − p)
    bet = ¼ × that × current balance, capped at 5% of balance

Example: price 50¢, our chance 60% → full Kelly 20% → quarter 5% → $17.50 on $350.

- **Weekly cap:** 15% of current balance across all trades.
- Size off the **current** balance, so bets shrink after losses and grow after wins.
  This is what makes compounding work and keeps a bad week from wiping out the bankroll.
- Why not bigger: full Kelly grows fastest on paper, but one bad estimate can
  cut the balance in half. Quarter Kelly gives up some speed in exchange for
  surviving our own mistakes.

## Cashing out
- Each time the balance reaches **$100 above $350** (i.e., $450), withdraw half
  the profit ($50) and keep playing with the rest. Repeat at each new $100 above
  the post-withdrawal balance.
- Withdrawals are real money paid toward bills. The bankroll itself is never refilled.

## Proving the edge
- Log every trade in `bankroll/2026-log.md`: market, price paid, our fair
  price, stake, result.
- After 30+ trades, check: did contracts we priced at X% hit about X% of the
  time? If yes, keep going. If our edges aren't showing up, cut sizes in half
  and re-examine the model.

## Weekly workflow
1. Chris sends the PFF package by Thursday.
2. Claude builds a fair-price sheet for every main-slate game: props from PFF
   projections, game lines from Vegas consensus, each with a "limit at or
   below" price and a quarter-Kelly stake.
3. Chris screenshots Kalshi; Claude flags which limits are worth placing.
4. Sunday 5:30 AM HST: re-check inactives and cancel orders on anyone ruled out.
5. Monday: log results.
