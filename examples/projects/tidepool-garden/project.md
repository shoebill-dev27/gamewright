---
kind: project
id: tidepool-garden
name: Tidepool Garden (sample)
repository: none (sample project for dry-runs; builds are simulated under sim/)
owner_language: ja
player_visible: sim/build-*.md
---
# Project: Tidepool Garden (sample)

## Vision

A calm touch puzzle game for children and families: slide tide pools to guide sea creatures home.
Pillars:

1. **No failure, no timers.** Nothing is ever lost; any move can be undone (D-001).
2. **Learn by touching.** Players discover rules by interacting, not by reading.
3. **Soft and warm**, but interactive pieces always stand out clearly.

## Player profile

Children aged 7–10, some still early readers, often playing beside a parent. Short sessions
(5–15 minutes). Quickly lose interest when nothing responds to their touch.

## Current state

Prototype build 0.2: 12 levels. Level 1 teaches dragging with a text bubble ("Drag the tide pool!").
Dry-run only: "running the build" means reading `sim/build-0.2.md`.

## Constraints

- Phones and tablets, touch only.
- No ads, no in-app purchases.
- No mechanic may depend on reading text.
- Small art budget: reuse the existing sprite sheet where possible.

## Art direction

Pastel palette, rounded shapes. Interactive pieces have a darker outline and a gentle idle motion.

## Design index

- `design/onboarding.md` — level 1–3 teaching plan.
