---
kind: handoff
goal: G-001
seq: 59
from: game-designer
to: studio
stage: Route
outcome: done
---
# 59: game-designer → studio — Spec updated with A1–A3 and A5; manual draft for the Owner; retest guideline

## Task

Route the updated `design/combat.md` and D-011 to Build, to Verify (acceptance criteria AC-19…AC-27) and to QA's open check (55). Send the manual draft below to the Owner to place in `manual.md` (D-005, D-007 pattern). Use the retest guideline for the next Play and Review. Nothing goes to `game-director` now.

## Context

G-001 (combat monotony), Option A (D-002). Handoff 56 asked for A1, A2, A3 and the A5 gaps, the ring question for room 2, A4's trigger, the manual draft and a retest guideline. I did not run `play` or `bots`: the changes are rules with acceptance criteria and the evidence I would add (still-player runs, 53) already exists. The retest needs a reactive player, which I cannot script.

## Findings

### What changed in `design/combat.md` (see D-011)

- **A1 wind-up spacing:** no grub starts a Wind-up within 1.0 s [tune] of another grub's Wind-up start (cancelled or defeated ones still count). A blocked grub is Waiting.
- **Second rule for the ring (answer to the open question):** A1 alone does not handle room 2. With four grubs it spaces the bites but still lets four grubs stand on all sides, and the tester felt "no gap to leave through". So at most 2 grubs may be within 1.5 tiles of the player at once; the others wait at 2.0 tiles. Result for a still player in room 2: at most 2 grubs close, one committed bite at a time, bites at least 1.0 s apart, and the player has a gap to dash or counter. The 2-in-Wind-up/Strike limit stays as a backstop.
- **A2:** hit-stun 0.3 s → 0.15 s [tune]. Invulnerability to 0.8 s is unchanged. No buffer.
- **A3 body hit:** an enemy within 0.5 tile of the player (distance 0 too) is hit by every swipe whatever the facing. This also closes the distance-0 swipe gap, so no separate rule is needed.
- **A5 dash and facing:** a dash with a direction sets facing to it (like movement). A dash without a direction keeps facing. A queued attack fires in the dash direction.
- **A5 dash distance:** up to 4 tiles in 0.25 s, stopping at the room edge, invulnerable throughout. QA's check (55) is judged against this rule.
- **A5 swipe cases:** a swipe resolves on true positions in every grub state. A hit during Strike cancels that strike (attacks resolve before enemy damage in a tick) and puts the grub in a 0.6 s Recovery. A swipe in Recovery hits normally.
- **A5 miss wording:** "(miss) too far" when an enemy is within 2.5 tiles but beyond reach; "(miss) not in front" when an enemy is within 1.5 tiles but outside the cone and the body radius; "(miss)" alone otherwise. The word "(miss)" is kept, so AC-11 and the manual's phrase still hold.
- **New acceptance criteria AC-19…AC-27** (spacing, cap, turns, hit-stun, body hit, dash and facing, dash distance, Strike/Recovery swipes, miss wording), each stated for `fps 30` and `fps 60`. AC-17 now covers them. AC-1…AC-18 are unchanged except the stun value inside the text, and AC-11 notes the miss causes.
- Room layouts, knockback, the grub cycle, spitters, the cone and reach are unchanged.

### A4 and the held items

- **A4 (120° cone) stays held.** It comes in if the retest's trace shows the "(miss) not in front" line on at least 1 in 4 swipes of a reactive session where an enemy was within reach, or testers still report missing grubs standing diagonally in front after A3 is in. Then widen to 120° [tune] and add an AC.
- **D1 (facing mechanic)** goes to `game-director` only if the retest still reports swipes into air after dashes or trouble turning, with A3 and the dash-facing rule in. **D2 (room 1 composition)** only if four grubs still read as a wall after A1 and the cap. This is as agreed in 56; neither is routed now.
- The cheap fixes do not need a facing mechanic or a room composition change, so there is no hand-back to the Director.

### Manual draft for the Owner (group B; text only, `manual.md` not edited)

Keep every phrase `ManualTest` checks (glyphs, "run over — rooms cleared: N", "press attack to start again", "a grub rears back", "the grub is open", "(miss)", "(too soon)", "(stunned)", "(down)", "(dash not ready)", the On screen section with `x` and the practice room). The phrase check ignores line wraps (D-009). Suggested placement:

**1. Controls section: replace the Attack and Dash bullets with:**

- **Attack**: a short swipe in the direction you face. It reaches a little more than one tile in a wide cone and hits every enemy inside it. An enemy right next to you or on your tile is always hit, whichever way you face. After a swipe you must wait a moment before the next. You can swipe an enemy at any time, even while it rears back to bite: a hit on a grub that is rearing back stops that bite. This is the best answer to a bite.
- **Dash**: a quick burst of up to four tiles in a direction (or the way you face). You turn to face the way you dash. You cannot be hurt while dashing, and you can dash through enemies and shots. A dash stops at the wall. It needs a moment to recharge.
- **Getting hit** costs a heart and stuns you for a very short moment (less than a quarter of a second), during which you cannot move, swipe or dash. Then you are safe for a little under a second.

**2. Add to What you hear and read, after the swipe-result bullet:**

- The first hit on a grub or spitter knocks it back about a tile and leaves it hurt. It may be out of reach afterwards: step toward it to hit it again.
- A swipe that does nothing says why: "(miss)" nothing was hit; "(miss) too far" an enemy is near but out of reach, step closer; "(miss) not in front" an enemy is next to you but outside the swipe's cone, face it first; "(too soon)" you are still recovering from the last swipe; "(stunned)" you were just hit; "(down)" you are out of hearts. (Replace the existing bullet on swipes that do nothing with this one.)

**3. Add to the On screen paragraph (after the sentence on grubs drawn beside you):**

Grubs take turns: at most two crowd you at a time, and they do not start to bite at the same moment. A grub waiting for its turn stands a couple of tiles away as a small `g`.

Keep the practice-room paragraph and the `x` row as they are.

### Retest guideline (design-side, qualitative)

Also written into `design/combat.md` ("Retest guideline"). Do not forward it to a Playtester.

- **Room 1:** a skilled player who reads the cues clears it and usually keeps most hearts. Damage comes from a misread or mistimed dash, not from a bite they could not avoid. They can step out, dash through, or hit the winding-up grub, then punish the open grub. A grub on them can be hit.
- **Room 2:** a skilled player can break the ring: only two grubs crowd them, bites come one at a time, and they can dash to a side or wall and fight from a free line. It is a real fight where a hit or two is plausible, but a player who tries clears it, usually with at least one heart left. A player standing still loses.
- Judge monotony only on a survived run.
- Ask the retest to report: swipes with "(miss) not in front" where the player aimed at that grub (A4); swipes into air after a dash (D1); whether four grubs still arrive as one clump that feels like a wall (D2 / Option B).

## Decisions already made

- D-001: one attack button plus dash; no new input.
- D-002: Option A first; staggered arrival (part of B) deferred.
- D-003: room mix across rooms; zero hearts ends the run; clear heals one heart.
- D-006: enemies may overlap the player and are never hidden.
- D-009: the `ManualTest` phrase check ignores line wraps.
- **D-011 (new):** the A1–A3 package, the engagement cap and the A5 rules; A4, D1 and D2 rejected for now with revisit triggers.

## Constraints

- All timings in seconds; hold at 30 and 60 FPS (spacing 1.0 s, stun 0.15 s and dash 0.25 s included).
- No new input (D-001). Reuse the existing grub states and timers.
- Do not forward this handoff, the retest guideline or the design spec to a Playtester unchanged (design-side content).

## Open questions

- **For QA (55):** results on dash distance, facing and swipe cases are to be checked against the rules above. Where the build differs, it is a defect, unless QA shows a rule cannot be built.
- **For Build:** report as built the Waiting behavior of a blocked grub (position held, following a moving player), and whether the display draws per principle 4 still hold with it.
- **For Verify / Review:** the values 1.0 s spacing, the cap of 2 and the 0.15 s stun are [tune]. Retune in this order if the retest says too harsh or too soft: spacing (0.8–1.5 s), cap (2 or 3), stun.
- **For the art-director (optional):** nothing new is required. The "(miss)" cause wording and the Waiting grubs use the existing glyphs; the art-director may review readability of the waiting grubs at 2.0 tiles.

## Expected output

- **Build:** implement the rules in `design/combat.md` (grub spacing and cap, stun 0.15 s, body hit, dash facing and edge stop, Strike/Recovery swipe handling, miss causes) and the AC-19…AC-27 checks.
- **Verify (QA):** run AC-1…AC-27 at both frame rates and settle the dash, facing and swipe cases against the spec.
- **Owner:** place the manual draft in `manual.md`; Verify then re-runs the full suite (D-008, D-009).
- **Play and Review:** one retest of rooms 1 and 2 by a reactive player (a live session, or several short reactive scripts), judged against the retest guideline. A `run_bots` round needs the bots script format; the earlier failure (53) was a format mismatch and should be checked first.

## Sender assessment

- **Confidence:**
  - High: spacing plus cap addresses the ring seen in 54, and the body-hit rule addresses "on you" swipes. Both follow from rules and from the still-player runs in 53.
  - Medium: 0.15 s stun and 1.0 s spacing are the right strength. They rest on one scripted playtest and no reactive data.
  - Low: dash facing as the fix for swipes into air. It is the minimal rule; the backstep variant is held for the Director.
- A still player in room 2 now meets bites at least 1.0 s apart (down about 2 s after the first bite at the earliest), so the idle reference time to down changes. It is a reference, not a target.
- No `play` or `bots` run was used in this step. The retest guideline is what a live or reactive session is judged against.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md, studio/skills/make-decision.md
- Project: design/combat.md, design/combat-visuals.md, manual.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-response-scope.md, decisions/D-003-run-end-and-room-rules.md, decisions/D-006-overlap-display-and-practice-room-manual.md, decisions/D-009-manualtest-phrase-check-ignores-line-wraps.md, decisions/D-011-grub-turns-stun-body-hit-dash-facing.md
- Previous handoff: goals/G-001-combat-monotony/56-studio-to-game-designer.md
