# Green Sheet Frontend Review

This folder is for reviewing the website/product side of Green Sheet separately from production.

The live product is: https://green-sheet.greensheet-hq.workers.dev/

`index.html` in this folder is intended to be a frozen review copy of the frontend from the private `showdown-v8-cleanup` development branch. It is for code inspection only. This public sandbox has no Cloudflare deployment workflow, production secrets, or automatic write-back to the private repository.

## What to review

Please use the live site like a DraftKings NFL user, then inspect the frontend code. Focus on navigation, information hierarchy, readability, mobile/desktop behavior, lineup-builder UX, Showdown vs Main Slate clarity, Results flow, labels/tooltips, unnecessary controls, responsiveness/performance, and anything that makes the product harder to understand or trust.

The production frontend is currently heavily concentrated in a large single `index.html` containing HTML, CSS and client-side JavaScript. Architectural suggestions for splitting UI, state, data access and optimizer/rendering logic are welcome.

## Guardrail

Do not treat this sandbox as production. Changes here do not affect the live site. Recommendations or patches should be reviewed before anything is deliberately transferred back to the private Green Sheet repository.
