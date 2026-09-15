# Green Sheet Review Sandbox

Public, isolated technical-review copy of selected Green Sheet NFL DraftKings Showdown research code.

This repository is deliberately separate from the private production Green Sheet repository. It contains no Cloudflare deployment workflow, production secrets, live-site controls, or automatic write-back to production.

## Purpose
Use this repo to inspect, run, modify and critique the experimental Showdown portfolio work safely.

Start with `Green_Sheet_Review.ipynb` in Google Colab.

## Included code
- `src/showdown_adaptive_portfolio_v1.py` — adaptive captain concentration and five-lineup portfolio selection.
- `src/showdown_ceiling_game_script_v1.py` — experimental TournamentP90 and game-script layer.
- `src/showdown_backtest_v1.py` — old-vs-new A/B backtest harness.
- `src/precompute_showdown_five_v8_reference.py` — previous V8 server algorithm retained as a reference.
- `docs/SHOWDOWN_ENGINE_CURRENT.md` — current architecture notes and known weaknesses.
- `data/den_kc_prelock_sample.json` — frozen pre-lock sample slate for review/testing.

## Research goal
For five-entry top-heavy Showdown tournaments, the experimental objective is to improve the chance that at least one of five lineups captures a high-end game outcome. Captain concentration should be earned by pregame tournament strength/confidence rather than forced diversity, and multiple lineups can express different correlated versions of the same strong game thesis.

## Important caveat
The Adaptive/Ceiling approach is experimental. Its weights and confidence thresholds are not validated production constants. Complete historical DraftKings result fixtures are still needed for a trustworthy multi-game quantitative A/B scorecard.

## Safety boundary
Nothing in this repository deploys the live Green Sheet. Changes made here stay here unless someone deliberately transfers reviewed code back into the private production project.
