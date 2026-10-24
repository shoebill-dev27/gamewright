---
kind: decision
id: D-007
status: accepted
decided_by: owner
goal: G-001
date: 2026-10-15
supersedes: none
---
# D-007: The Owner places the practice-room paragraph in `manual.md` (Option A)

## Decision

The Owner chose Option A of escalation 36. The Owner added the following paragraph to `manual.md`, in the `## On screen` section, at the end of the section, with no change to the wording:

> The practice room (`room empty`) is not part of a run. Enemies appear only where your script places them (`spawn`), and you stand where `player` puts you. Nothing heals, there is no next room, and the session ends a moment after you go down. If a grub or spitter is on your tile, it is drawn on a free tile next to you, so you can always see it.

Owner's words (2026-10-15): 「A。36 の段落を一字も変えずに manual.md の ## On screen セクションの末尾に追記しました（Owner の代理として Studio の推奨案を採用）。」

Limits:
- This settles only who places the paragraph and that Option A applies. It does not change D-005 (the Owner places `manual.md` content) or D-006 (the practice room is listed in the On screen section). Options B and C were not chosen.
- The placement is the Owner's statement. QA verifies it independently (AC-15, `ManualTest`) and does not take it on trust.
- The Owner's reply says the choice follows the Studio's recommendation, made on the Owner's behalf. The Studio records it as the Owner's decision as given.

## Rationale

The wording was already fixed by D-006 and AC-15, and only the file edit was missing. It is a small, reversible edit. Options B (a permanent change to write permissions or D-005) and C (overturning D-006) were out of proportion to the gap.

## Alternatives considered

- B: let roles edit `manual.md`. It changes the D-005 policy and needs an environment change, which is too much for one paragraph.
- C: drop the practice-room entry from AC-15. It reverses D-006 and needs a Design re-decision, which is unnecessary.

## Revisit when

- QA finds the paragraph missing, altered, or outside `## On screen`, or `ManualTest` still fails for a manual-related reason.
- Roles repeatedly need to edit `manual.md`. Then reconsider Option B and D-005.
