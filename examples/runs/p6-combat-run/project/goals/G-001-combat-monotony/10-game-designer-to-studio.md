---
kind: handoff
goal: G-001
seq: 10
from: game-designer
to: studio
stage: Specify
outcome: done
---
# 10: game-designer → studio — Option A spec written; rulings on questions 1–7

## Task

Decide whether Plan is needed, then route the spec to Build (`gameplay-engineer`). Route the other items below.

## Context

G-001: combat monotony. D-002 chose Option A. The spec is in `design/combat.md` (build 0.5 target) and the run/room rules are recorded in D-003. It was checked against the rooms 4–5 report (08) and QA's report (06). No bots or play runs were used; the spec is not verified against the build.

## Findings

### What the spec changes (Option A, D-002)

- **Grub:** Approach → Wind-up (0.5 s, visible) → Strike (0.15 s) → Recovery (0.9 s). It is harmless outside Strike. At most 2 grubs attack at once. A hit during Wind-up cancels the strike.
- **Spitter:** Charge (0.8 s, visible) → Fire → Recovery. A volley every 2.5 s, staggered per spitter. The aim is locked at the end of the charge, so the shot can be dodged. Spitters can be approached and hit, and a hit during Charge cancels the shot.
- **Hit feedback:** swipe arc, damaged state, remaining HP in the text, multi-hit allowed.
- This answers the 08 observations: spitters as scenery, projectiles never reacted to, grubs as the only pressure, the dash buying quiet seconds with no use.

### Rulings

1. **Room mix:** across rooms, not per room. Rooms 1–3 are not defects. Per-room mixing is Option B (D-003).
2. **Zero hearts:** enemies stop, projectiles vanish, 2.0 s later a "run over" screen, attack starts a new run at room 1.
3. **Room cleared:** hearts carry over, +1 heart on clear, 1.5 s later the next room loads. It cannot happen while the player is down.
4. **Practice room and `x` marker:** documented in `design/combat.md`. The manual needs updating (see below).
5. **30/60 FPS:** criteria AC-1…AC-17 and the tolerance section in the spec.
6. **"(nothing happens)":** intended, but must always give a reason: miss, too soon, stunned, down.
7. **Twice-printed spit line:** one line per spitter is expected, but identical lines make it read as a duplicate. It is a minor presentation defect. **Route to `qa`** to log it. The spec requires the line to name the spitter (AC-8).

### Checks against 08

- Rooms 4–5 had no variety beyond count, and the spitters were mirrored. The spec therefore staggers them and gives them a dodgeable shot. It does not change D-002's scope.
- The dash gave a live player nothing to do with the quiet seconds. The spec gives the quiet time a use (counter in Recovery, approach a spitter).
- This does not contradict the diagnosis, so no Director return is needed.

## Decisions already made

- D-001, D-002 (unchanged).
- D-003 (new): room mix across rooms; run-end rule; room clear heal.

## Constraints

- No new inputs. Timings in seconds. 30 and 60 FPS. Reuse existing enemy, projectile and timer systems.

## Open questions

- **Manual changes needed** (not on my write list): list the practice room behavior, the `x` marker, the new glyphs/states, the swipe arc, the run-over screen, and the new attack messages in `manual.md`.
- Swipe reach, cone width and projectile speed are targets. Build should report as-built values.
- Glyph/color choices need `art-director` review (threat colors saturated orange/red).
- Feasibility of the attack-slot limit and the aim-lock is not checked. Ask `technical-director` or Plan if there is doubt.
- Run progression after "run over" is not defined. It is outside this goal unless the Director wants it.
- All timings marked [tune] need a live playtest after Build, especially to see that grubs are not trivial and the dash still matters.

## Expected output

The Studio routes: Plan if wanted, then Build; `qa` for the duplicate spit line; `art-director` for the visual states. After Build, QA verifies AC-1…AC-17 at 30 and 60 FPS, then a live reactive playtest. Reopen Option B only if that playtest still shows sameness (D-002).

## Sender assessment

Confidence medium-high that the rules fix single-state, untelegraphed behavior. The effect size and the numbers are unproven until a live playtest.

## Load

- Role: studio/roles/qa.md or studio/roles/gameplay-engineer.md (per routing)
- Skills: none specified
- Project: design/combat.md, manual.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-response-scope.md, decisions/D-003-run-end-and-room-rules.md
- Previous handoff: goals/G-001-combat-monotony/09-studio-to-game-designer.md
