---
kind: handoff
goal: G-001
seq: 40
from: qa
to: studio
stage: Verify
outcome: question
---
# 40: qa → studio — Verify Phase 1 (encounter escalation) against `sim/build-0.6.md`: criteria 3, 4, 5, 10 pass; criteria 1 and 2 cannot be judged from a build description (exact input named); no regression

## Task

Record the Phase 1 verification result below. Criteria 3, 4, 5 and 10 pass at 30 and 60 FPS, judged from stated behavior. Criteria 1 and 2 are `question`: they need counted runs, and `sim/build-0.6.md` contains no counts. The dash, hit-stun and invulnerability regression check against `sim/build-0.5.md` found no change. Route the Design items in "Open questions" to `game-designer`. None of them blocks criteria 3, 4, 5 or 10.

**Overall verdict: question.** I cannot give an overall `pass` while criteria 1 and 2 are unjudged. I found no failing criterion.

## Context

- G-001, Phase 1 (D-002, D-008). Build under test is `sim/build-0.6.md`; baseline for unchanged behavior is `sim/build-0.5.md`. `sim/build-0.4.md` and `sim/build-0.3.md` were not used.
- Basis of the verdicts: the spec (`design/g001-combat-escalation.md` 3.1–3.8 and criteria 1–5, 10), the visual spec (A1–A3) and the statements in `sim/build-0.6.md`.
- The handoff 38 "Findings" and `sim/repo-notes.md` told me what to look for and let me cross-check the data table. I did not use them as evidence for any verdict. Where the build is silent, I say so.
- The evidence is a build description, not a counted run. Nothing was repeated or counted. Every "pass" below means "the description states the required behavior", not "observed N times".
- Handoff 38's data table matches spec table 3.2a for every room, wave, enemy and candidate list. This is a data cross-check only.

## Findings

### Verdicts per numbered criterion

| # | Criterion (short) | 30 FPS | 60 FPS | Basis |
|---|---|---|---|---|
| 1 | Rooms 4–5 not clearable by holding one position (≥4 of 5 attempts per position take ≥2 hits or die) | question | question | No hit counts anywhere. Build 0.6: "Whether you take hits then depends on the room size and speeds, which are not stated here." The qualitative line "standing still … is no longer a constant answer" is not the spec threshold. |
| 2 (P1 part) | A dash taken in combat in at least 3 of 5 rooms | question | question | Build 0.6: "Dashing is available as before. This build does not change what it does." No record of dashes in combat per room. The P2 part is out of scope. |
| 3 | Later rooms differ from the previous room in at least 2 of count, mix, spawn edges, wave count; room 5 differs from room 1 in all four | pass | pass | See the room comparison below. Static content, identical at both rates. |
| 4 | P1: nothing exists or damages before its 0.8 s ring ends; spawns ≥5 tiles from the player unless a fallback is logged; on screen; first Spitter shot ≥1.0 s after appearing | pass | pass | See the criterion 4 evidence below. |
| 5 | Same points exactly; ring starts, spawns, wave starts and shot times within 1 frame at 30 FPS; no RNG | pass | pass | Build: "match within one frame at 30 FPS (0.034 s). The points chosen are identical." "Nothing about the choice is random." Conditional on scripts; see Open questions item D2. |
| 10 | Waves and spawn points follow 3.2a and 3.3 | pass | pass | Sub-items a–f below. |

Differences between 30 and 60 FPS in every pass: only the allowed one frame (build: ring start and appearance "can each land up to one frame (about 0.034 s) later"; half that at 60 FPS).

### Criterion 3: room comparison (from build 0.6, same as spec 3.2)

| Room | Count | Mix | Edges | Waves | Differs from previous in |
|---|---|---|---|---|---|
| 1 | 3 | 2G 1S | W, E | 1 | n/a |
| 2 | 4 | 3G 1S | W, E | 2 | count, mix, wave count (3) |
| 3 | 5 | 4G 1S | W, E, N | 2 | count, mix, edges (3) |
| 4 | 6 | 4G 2S | W, E, N, S | 2 | count, mix, edges (3) |
| 5 | 7 | 5G 2S | W, E, N, S | 2 | count, mix (2) |

Room 5 against room 1: count (7 vs 3), mix, edges (four vs two), wave count (2 vs 1). All four differ. Pass.

### Criterion 4: evidence

- **No enemy before its ring ends:** "No enemy exists, moves or attacks while its ring is on the floor." "Standing in a ring does nothing to you."
- **≥5 tiles unless fallback:** the 5-tile rule is stated, with "no exception" for Spitters. The fallback case is stated, with the warning that the enemy "can appear closer than 5 tiles … and you get the same 0.8 s ring warning". Fallbacks are logged with `SPAWN_FALLBACK`. The criterion allows the fallback if reported.
- **On screen:** "Arrivals are inside the room and on screen." This is a statement, not an observation. The camera is not described.
- **Spitter first shot:** "Its first shot comes 1.0 s after it appears, and then one every 2 s", and "does not fire when it appears". Design item D3 concerns the exact boundary.
- **Visual checks A1–A3:**
  - A1 pass: "visible for its whole 0.8 s from 8 or more tiles away".
  - A2 pass: the enemy appears at the ring's centre "0.8 s after the ring starts", within the stated one-frame difference. No enemy exists during the ring.
  - A3 pass: the ring is flat and non-directional, with no lane or ray, and has "no effect on damage".
  - The ring look is a new placeholder, unreviewed by the Art Director (handoff 39). I did not judge the look.
  - The build does not state that the ring is self-lit. A1 is met by the 8-tile alternative.

### Criterion 10: sub-items

| Sub | Statement checked | Result (30 / 60) | Build statement |
|---|---|---|---|
| a | Wave 1 first rings at `T0`; second Grub of rooms 1–3 at +1.0 s; Spitter ring at `T0` | pass / pass | "The first wave's rings start the moment you gain control … The second Grub of rooms 1 to 3 (the +1.0 s Grub) starts 1.0 s later." Room 1: "The Spitter rings at the start." |
| b | Wave 2 at `T0` + 8.0 s with no kills; on the kill leaving 1 unresolved wave 1 enemy; never earlier while 2 or more unresolved | pass / pass | "With no kills, wave 2's rings start 8.0 s after wave 1's first rings." The count includes enemies not yet ringing. "Wave 2 does not start early while two or more wave 1 enemies are still alive or pending." |
| c | First list point if ≥5 tiles from the player; else next qualifying; else farthest free | pass / pass, with a described gap | Stated. The mixed case is not covered by the wording; see Open questions item D4. |
| d | An active ring at the point, or a living enemy within 1.5 tiles, skips the point | pass / pass | "no ring is active there and no living enemy is within 1.5 tiles of it" |
| e | Spitters in rooms 3–5 use the covered-corner point, or the far end of the same wall if the player holds the corner | pass / pass, with a named limit | "For Spitters the second point is the other end of the same wall." "A player standing in the covered corner makes the Spitter appear at the far end of that wall." "No exception to the 5-tile distance." Corners named for rooms 4 (NW, then SE) and 5 (SW, NE) match the spec. Room 3 says only "north edge near a corner"; it does not name NE. That is compatible with the spec but not confirmed by the build. |
| f | Identical inputs give identical points | pass / pass | "The same player position and timing always give the same point." "Nothing about the choice is random." |

Limits, not failures:
1. Sub-item b, "kill the first Grub, then the Spitter while the second Grub's ring has not started" (step 2 of the exercise script): it cannot be reached by real input. Both enemies appear at `T0` + 0.8 s, and the second Grub's ring starts at `T0` + 1.0 s. A Grub takes two swipes at least 0.35 s apart. Only a debug kill can test "a pending Grub counts". The build states it ("a wave 1 Grub still has not yet appeared") but I did not exercise it.
2. Sub-item e, room 3: needs the covered-corner point name. The `SPAWN_POINT` line for room 3, wave 1, Spitter would show it.

### Regression against `sim/build-0.5.md` (handoff 05 criteria 1–6, verdict basis of handoff 31)

Result: no regression found. The check is description against description. The "20 repeats per frame rate" were not executed, as in handoff 31.

- Build 0.6 states "This is unchanged from the previous build".
- Every dash and hit protection bullet matches 0.5:
  - dash with no hit: 0.25 s full protection;
  - hit: 0.8 s protection and 0.3 s stun;
  - dash started at 0.3–0.55 s, 0.55 s to just under 0.8 s, and at 0.8 s or later after a hit;
  - Grub and Spitter sources, toward or away;
  - boundary counts as after protection, with a possible one-frame difference between 30 and 60 FPS.
- Every hit-stun input statement matches 0.5:
  - presses in the first 0.3 s do nothing;
  - a held button does nothing until a fresh press;
  - a press just after 0.3 s works;
  - a press exactly at 0.3 s may differ by one frame;
  - a swipe queued during a dash still fires when the dash ends;
  - a hit cancels waiting requests.
- Cooldown 0.6 s, dash distance and duration are unchanged.
- Per handoff 05: criterion 1 (dash at 0.3 s, no damage), 2 (various delays), 3 (directions, sources), 4 (dash with no hit), 5 (stun, invulnerability, cooldown, queued swipe) and 6 (no delayed damage) all hold.
- One wording difference: 0.6 does not repeat 0.5's "the dash cooldown does not start" for a dash press during stun. It is covered by "unchanged from the previous build" and "Pressing dash … does nothing". I did not treat it as a change.
- The 0.5 line "hold position and swipe until empty works" is intentionally gone from 0.6. That is the Phase 1 change, not a regression.

### Reports requested (not judged pass/fail)

1. **Existing values (spec 3.8).** `sim/build-0.6.md` shows none of: Grub speed, player speed, projectile speed and range, heart count, room size, hitbox sizes. It says: "Room size, Grub speed, player speed, projectile speed and range, hearts and hitbox sizes are not stated here." Recorded as **not shown**. The only qualitative facts are "a Grub takes two swipes" and "the Spitter's projectile is slow; one step sideways avoids it".
2. **`SPAWN_FALLBACK` count.** Not available. Build 0.6 has no log excerpt or counts, and I had no scripted run. I cannot say how many lines occur or whether Spitter or Grub choices mostly fall back. Geometry from the lists, with W and H unknown, shows where fallback is likely:
   - Room 2 wave 2 Grub list E3, E1, E2: E1 and E3 are 0.25H from E2, the stationary wave 1 Spitter. If H ≤ 6 tiles and that Spitter is alive (it is, when wave 2 starts on the 8 s timeout or when it is the last wave 1 enemy), all three points are occupied and the farthest-overall fallback is used.
   - Spitter far-end alternative: the two points on a wall are W−3 tiles apart. For a player at the wall-face corner to be ≥5 tiles from the far end, the wall needs about W ≥ 6.5 tiles, and more for a player 1 tile off the walls.
3. **Heading versus file name.** The file is `sim/build-0.6.md` but its heading reads "Simulated build 0.3.3". The same pattern holds for 0.5 (heading 0.3.2). This is a labeling mismatch only. I treated the file as the newest build, as the handoff says.
4. **One-frame sampling rule.** The build does not state the sampling frame. Under the rule as given in handoff 38, a ring start between frames at 30 FPS samples the player position on the next frame:
   - At 30 FPS the sample can be up to 1/30 s after the scheduled start; at 60 FPS up to 1/60 s.
   - With a moving player at speed v (not shown), the sampled position can differ by up to about v/30 tiles between the rates.
   - The 5-tile test, and the 1.5-tile occupancy test against a moving Grub, can give a different point only when the distance is within that margin of a threshold at that moment.
   - A kill-triggered wave start (taken at the kill's frame time) also moves later ring starts, and so the sample time, by up to one frame.
   - So the rule can produce a difference beyond the allowed one frame, in the point choice, in threshold-adjacent cases. The build does not show any such case.
   - A stationary player, or scripted positions that stay well clear of thresholds at ring starts, avoids it.

## Decisions already made

- D-001: no new input. D-002: Phase 1 first. D-004: gameplay numbers are data, timers are timestamps on the game clock. D-007: hit-stun regression is checked against `sim/build-0.5.md`. D-008: the Phase 1 spawn and wave rules.
- Nothing here changes a decision.

## Constraints

- I did not decide design values or change criteria. I did not lower the criterion 1 threshold or the criterion 2 count.
- Phase 2 content and visuals were not verified. The ring look is left to handoff 39.
- Loop limit: the missing input for criteria 1 and 2 is named below. If the same input is missing after the next verification, the Studio escalates to the Owner instead of routing again.

## Open questions

**Blocking (criteria 1 and 2): exact missing input.**
- **Criterion 1:** for rooms 4 and 5, for each of the 5 positions (4 corners, centre), at least 5 scripted attempts (facing the nearest spawn side, attacking only), the number of hits taken per attempt and whether the player died. This needs a runnable build or a recorded scripted run. A build description that only says "depends on room size and speeds" cannot supply it.
- **Criterion 2 (P1 part):** for each of rooms 1–5, whether a dash was taken in combat during a played or scripted run.
- If no counted run can exist in this dry run, the Studio decides (the Owner, if needed) whether these two criteria are judged from a build description that states hits and dashes per room and position, or are deferred to the playtest. I cannot make that choice.

**For `game-designer` (non-blocking, QA does not decide these):**
- **D1.** Spec 3.8 asks QA to record the existing values in its first Phase 1 verification handoff. They are "not shown" (item 1). The playtest or a build that shows them must supply them. This decides whether criterion 1 can be judged by calculation instead of counts.
- **D2.** Criterion 5 says points match "exactly" with the same scripted player positions. The sampling rule (next logic frame after a between-frame ring start) can give different points at 30 and 60 FPS for a moving player near a threshold (item 4). Design to state whether scripts must keep clear of thresholds, or whether the rule needs a frame-rate-independent sampling time.
- **D3.** Criterion 4 says a Spitter's first shot is "at least 1.0 s after appearing", with no tolerance. Criterion 5 allows ±1 frame on shot times. If `appearTime` is the scheduled time, the first shot can be less than 1.0 s after the first visible frame at 30 FPS, by less than one frame. Design to state which governs.
- **D4.** Spec 3.3: "If no candidate passes both tests, take the candidate that is not occupied and farthest." Build 0.6 describes only two cases: no point far enough, and every point occupied. A mixed case (one point near and free, another far but occupied) is not covered by the build's wording. The spec answer is the near free point. I did not verify this case from the build.
- **D5.** Room 2 wave 2 depends on room height (item 2). If H ≤ 6 tiles, the E-edge Grub always falls back to the farthest-overall rule while the Spitter is alive. The spec's reporting path for "most lists fall back" (3.8 and D-008 "Revisit when") applies.
- **D6.** Criterion 2 (P1) counts "a dash taken in combat". A scripted run can satisfy this by dashing regardless of need. Design to say whether the scripted check is meant to show need, or whether it is a playtest signal only. I did not redefine it.

**For `art-director` (handoff 39):** build 0.6 describes the ring's last phase as dot "hot, near-white", and the spec palette gives the hot core as `#FFC14D` (amber). Build 0.6 also does not state that the ring is self-lit independent of the lantern.

## Expected output

For `studio`:
1. Record criteria 3, 4, 5 and 10 as pass (description-based, with the limits above) and the regression check as no change.
2. Record criteria 1 and 2 as `question` with the exact missing input above. Obtain counted run data, or decide how they are judged.
3. Route D1–D6 to `game-designer`, and the colour/self-lit note to `art-director` if not already in handoff 39.
4. Phase 1 is not verified as a whole until criteria 1 and 2 have a verdict. On any failure after that, `gameplay-engineer` gets the failure report; a second failure of the same criterion goes to `technical-director`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/g001-combat-escalation.md (sections 3, 6, 7, 8; criteria 1–5, 10), design/g001-telegraph-visuals.md (section 3, A1–A3), sim/build-0.6.md, sim/build-0.5.md
- Decisions: decisions/D-004-phase-2-technical-approach.md, decisions/D-007-verify-against-build-0-5.md, decisions/D-008-phase-1-spawn-and-wave-rules.md
- Previous handoff: goals/G-001-combat-monotony/38-studio-to-qa.md
