---
kind: decision
id: D-002
status: accepted
decided_by: game-director
goal: G-001
date: 2026-10-15
supersedes: none
---
# D-002: Respond to combat sameness by reworking existing enemy behavior first (Option A)

## Decision

1. **Option A is approved as the first response for G-001.** The existing Grub and Spitter get legible, varied behavior:
   - a visible wind-up before damage is possible;
   - a recovery pause after attacking;
   - staggered Spitter volleys with a visible charge-up;
   - clear hit feedback on the player's own attacks, including a visible damaged state.
   The game-designer owns the exact timings, knockback and feedback rules.
2. **Option B (mixed rooms, moving spitters, staggered grub arrival) is deferred.** It is not rejected. It is reconsidered only if a playtest of the Option A build still shows sameness. It is in scope for G-001 only after that playtest.
3. **Option C (new enemy types) is out of scope for G-001 for now.** It is reopened only if A and B have been playtested and sameness remains.
4. **Another play round on rooms 4 and 5 runs before the spec is finalized.** The designer may start the spec for A in parallel, but must check it against the round's results before handing it on.

## Limits

- All work stays within D-001: no new inputs beyond attack, dash and pause.
- All new timings are specified in seconds. Acceptance criteria must hold at both 30 and 60 FPS.
- Every damaging action must be preceded by a visible telegraph (pillar 3).
- Prefer reuse of existing enemy, projectile and timer systems (small-team constraint).
- This decision does not cover the possible defects (room composition vs. spec, no game-over/restart state). Those are routed to `qa` separately and may change the spec's wording or add a rule.
- It does not decide whether Spitters get a way to be approached. The designer decides that within A, using the rooms 4 and 5 evidence.

## Rationale

- The diagnosis traces all four symptoms to one root cause: each enemy has a single behavior with no state change, timing variation or readable cue. Option A addresses that root cause directly, covering S1, S2 and S3 and part of S4.
- It supports pillar 1 (depth from positioning, timing and enemy behavior) and pillar 3 (readable threats). It matches the player profile, which favors spacing and dodging.
- It is the cheapest and lowest-risk option, and it reuses existing systems.
- No escalation trigger fires. No pillar, D-001 or Goal meaning changes, and the scope and cost are modest.
- Variety (B, C) layered on flat enemies would add busyness or content cost without fixing the cause.
- The rooms 4 and 5 round is cheap. The current sample is homogeneous and was blind-scripted, so it understates winnability and cannot show whether the dash answers grubs. Specifying timings without that evidence risks mistuning.

## Alternatives considered

- **B first or A+B together:** rejected for now. Without A the fights are only busier, and it adds scope before A's effect is known.
- **C (charger, shielded enemy):** rejected for now. It has the highest cost and scope risk and leaves the existing enemies flat.
- **Spec immediately, no further play round:** rejected. Rooms 4 and 5 are the only place to check the "mixed rooms" claim, and the dash/grub question needs reactive play.

## Revisit when

- The rooms 4 and 5 round shows they already contain the missing variety or different enemy behavior, which would change what Option A needs to cover.
- A playtest of the Option A build still reports monotony (open B, then C).
- A live playtest shows the Option A changes make grubs trivial or the dash insufficient. This is a tuning matter for the designer, unless it touches D-001.
