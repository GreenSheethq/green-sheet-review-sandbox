# Green Sheet Showdown Engine — Review Notes

Status: isolated review sandbox. This repository cannot deploy the live Green Sheet.

## Previous V8 exact-five concept
The previous server precompute removed hard-blocked players, excluded blocked/salary-only roles, limited the pool, generated legal Showdown candidates and scored them primarily with 56% lineup P90, 24% lineup Projection, 16% average Tournament Fit, plus a small capped captain-leverage adjustment.

The portfolio then enforced multiple captains, max captain exposure and player exposure caps.

## Design weakness under review
Mechanical roster/captain diversity is not the same as covering genuinely different game outcomes. A strong tournament captain can also be recognized in the player data yet fail to receive enough representation if the portfolio objective is dominated by raw summed ceilings and forced captain diversification.

DEN@KC is one regression example: Kenneth Walker III carried strong pregame role/tournament signals but received no captain slot in the exact V8 five. This is a regression case, not permission to tune specifically to the completed-game winner.

## Experimental direction
1. Preserve median Projection separately from tournament ceiling.
2. Build a TournamentP90/ceiling signal only from information available before lock.
3. Represent game scripts/correlations explicitly.
4. Allocate captain exposure adaptively based on pregame confidence instead of forcing arbitrary captain diversity.
5. Optimize the five lineups as one portfolio, ultimately toward expected-max/marginal scenario coverage.
6. Backtest frozen pregame snapshots and introduce actual DK points only after lineup selection.

## Not proven
Current heuristic weights and confidence thresholds are prototypes, not validated production constants. The backtester still needs complete actual DK fantasy-point fixtures and a larger historical sample. Reviewers should challenge assumptions, identify duplicated signals, and prefer simulation/correlated outcomes where possible.

## Production guardrails
- No result leakage.
- No hindsight-specific player boosts.
- Reproducible frozen pregame tests.
- No deployment from this sandbox.
- Regular/main-slate logic is outside the scope of this Showdown review.
