# Studio operation packet

operation: Step
goal: G-001
role: qa
incoming_handoff: goals/G-001-damage-during-dash/09-studio-to-qa.md
next_seq: 10

## You may write

- goals/G-001-damage-during-dash/10-qa-to-<recipient>.md

## Inputs

<<<FILE studio/execution.md#executor-instructions
## Executor instructions

You are executing exactly one Studio operation, in isolation.

- Everything you may use is in this packet: the operation header, the input files, and the paths
  you may write. You know nothing else about this project, its history, or other steps, and you
  must not assume anything beyond the packet.
- Follow the procedure for this operation in the Studio files included. For a Step, act as the
  receiving Role within its contract and listed Skills; do not perform other Roles' work.
- Write every file you create or change as one complete file block:
  `<<<FILE <path>` on its own line, the full file content, then `>>>END` on its own line.
  Use only the paths listed under "You may write"; paths are relative to the project directory.
- Only file blocks are kept. Anything else you write is discarded and never shown to any later
  step, so put everything the next operation needs into the files.
- If the packet is not enough to do the operation, write the artifact that hands the work back or
  reports the blocker instead of guessing.
>>>END

<<<FILE goals/G-001-damage-during-dash/09-studio-to-qa.md
---
kind: handoff
goal: G-001
seq: 9
from: studio
to: qa
stage: Verify
outcome: routed
---
# 09: studio → qa — Final verification of G-001 against criteria 1–6

## Task

Issue the overall verdict (pass or fail) for G-001 on build 0.4 against acceptance criteria 1–6. Criteria 1–5 were already recorded as pass in your earlier report (`06-qa-to-studio.md`). Settle criterion 6 under the definition below, and confirm there is no regression in the rest of the dash and damage behavior.

## Context

Goal G-001: the Owner reported that the player sometimes takes damage while dashing (reproducible). Build 0.4 is the fix. In the previous Verify, criterion 6 ("same results at 30 and 60 FPS") was undecided because the design gave no tolerance for expiry timing at a protection boundary. The Game Designer has since ruled on it. The ruling is written in `design/combat.md` (section "Protection expiry and frame rate") and in D-002. This project is a dry-run: the build under test is the description in `sim/build-0.4.md`, as ruled earlier.

## Findings

Criterion 6 is now defined by the design rule (D-002): protection expiry may be late by less than one frame at the running frame rate (under 34 ms at 30 FPS, under 17 ms at 60 FPS), and must never be early. It applies to both boundaries (dash end and the 0.8 s post-hit mark) and both enemy types (Grub contact and Spitter projectile).

For each boundary and enemy type, at both 30 and 60 FPS, check:
1. Contact at or before the end time: no damage.
2. Contact later than the end time plus one frame (34 ms at 30 FPS, 17 ms at 60 FPS): 1 heart of damage.
3. Contact between those two moments: either result passes. A 30 vs 60 FPS difference here is not a failure.
4. No other difference between frame rates in damage, dash or hit-stun results.

Protection ending early at any frame rate, or lasting more than one frame past its end time, fails criterion 6.

## Decisions already made

- D-001: one attack button plus dash. Not affected.
- D-002: protection expiry may be late by up to one frame, never early.

## Constraints

- Must play correctly at 30 and 60 FPS.
- Dash and damage rules are unchanged: full-duration dash invulnerability, 1 heart per hit, 0.3 s hit-stun, invulnerable until 0.8 s after a hit.
- Do not redefine the criteria. If something is undefined or ambiguous, report it as a `question`.

## Open questions

None.

## Expected output

An overall verification report with a per-criterion result (1–6) and a verdict of `pass` or `fail`, with evidence from the build description. Address the result to `studio`. If you find a failure, give the failing criterion, the frame rate, the boundary and the observed vs expected behavior. If you cannot verify, report the blocker.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md#constraints, design/combat.md, sim/build-0.4.md, goals/G-001-damage-during-dash/02-qa-to-gameplay-engineer.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-protection-expiry-frame-tolerance.md
- Previous handoff: goals/G-001-damage-during-dash/06-qa-to-studio.md
>>>END

<<<FILE studio/roles/qa.md
---
kind: role
id: qa
strip_sections: Sender assessment
---
# Role: QA

## Responsibility

Reproduces defects and independently verifies that built changes meet their acceptance criteria
without breaking existing behavior.

## Decides

- Pass or fail against the acceptance criteria, with evidence.
- Whether a defect is reproducible, and its severity.

## Must not

- Modify the production code under verification. QA may add or run tests and test tooling.
- Redefine acceptance criteria, or pass a change with a known failing criterion.
- Decide intended behavior when the spec is silent — hand back to `game-designer`.

## Independence

Verify from the spec, the acceptance criteria and the build — not from the engineer's explanation
of why it should work. Prefer a fresh executor context without the implementation history.

## Works from

- For defects: the Owner's report and the relevant design documents.
- For verification: acceptance criteria, how to exercise the change, project constraints (e.g.,
  supported platforms and frame rates).
- Never the implementer's self-assessment or reasoning: a Handoff's `## Sender assessment` section
  is removed before QA receives it.

## Produces

- A defect report: reproduction steps, expected vs actual (with the source of "expected"),
  conditions, severity, acceptance criteria for the fix.
- A verification report: per-criterion pass/fail with evidence, regressions checked.

## Hands back / escalates when

- Verification fails → `gameplay-engineer`, with the failure report.
- The expected behavior is undefined → `game-designer`.
- The same criterion fails a second time → Studio routes to `technical-director`.

## Typical skills

reproduce-defect, verify-change
>>>END

<<<FILE studio/skills/verify-change.md
---
name: verify-change
description: Verify a built change against its acceptance criteria and check for regressions, producing a pass/fail report with evidence.
---
# Skill: Verify change

Typical roles: qa.

## When to use

After anything was built, before the work counts as done.

## Inputs

Acceptance criteria, how to exercise the change, project constraints (platforms, frame rates,
input devices), the defect report or spec the change answers.

## Method

1. Check each acceptance criterion independently, under every supported condition the criterion or
   the project constraints name. Record evidence per criterion.
2. Re-run the original reproduction steps for defects.
3. Check for regressions in neighbouring behavior the change could affect.
4. Verdict: `pass` only if every criterion passes. Otherwise `fail`, with the failing criterion,
   conditions and evidence. If a criterion cannot be judged because the expected behavior is
   undefined, report that as a spec gap.

## Output

Verification report: per-criterion result and evidence, conditions tested, regressions checked,
verdict.

## Do not

Modify the production code under test. Do not soften a failure into a pass with a note. Do not
rely on the implementer's explanation instead of observing behavior.
>>>END

<<<FILE project.md#constraints
## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).
>>>END

<<<FILE design/combat.md
# Combat design (build 0.3, frame-rate rule added for G-001)

## Player kit

- **Attack** (one button): a short swipe in the facing direction. 1 damage. 0.35 s recovery.
- **Dash**: 4 tiles over 0.25 s. The player is invulnerable for the full dash duration.
  Cooldown 0.6 s. An attack pressed during a dash is queued and fires when the dash ends.
- **Getting hit**: 1 heart of damage, 0.3 s hit-stun (no input), then invulnerability until 0.8 s
  after the hit.

## Protection expiry and frame rate (G-001, criterion 6; D-002)

Intent: the player should never be hurt at a moment the rules say they are safe, and the game
should behave the same at 30 and 60 FPS in every way the player can notice.

Applies to both protection end times: the end of a dash (0.25 s after it starts) and the 0.8 s
post-hit mark. It applies equally to Grub contact and Spitter projectiles.

Rule:
- **Never early.** A contact at any moment before a protection end time never hurts, at either
  frame rate.
- **Late by at most one frame.** Protection may continue past its end time by less than one frame
  at the running frame rate: under 34 ms at 30 FPS, under 17 ms at 60 FPS. The error always favors
  the player.
- **Not late beyond that.** A contact more than one frame after the end time hurts normally, at
  both frame rates.
- A contact inside that single trailing frame may be harmless at one frame rate and hurt at the
  other. This is accepted and is not a difference under "same results at 30 and 60 FPS".

All other rules (damage, hit-stun, dash distance, duration, cooldown, queued attack) must give the
same results at 30 and 60 FPS with no tolerance.

Acceptance criterion for QA (criterion 6), at both 30 and 60 FPS, for the dash end and the 0.8 s
mark, for Grub and Spitter:
1. Contact at or before the end time: no damage.
2. Contact later than the end time plus one frame (34 ms at 30 FPS, 17 ms at 60 FPS): 1 heart of
   damage.
3. Contact between those two moments: either result passes.
4. No other difference between the two frame rates in damage, dash or hit-stun results.

## Enemies

| Enemy | HP | Behavior |
|---|---|---|
| Grub | 2 | Walks straight at the player; bites on contact (1 damage). No telegraph. |
| Spitter | 2 | Stationary; fires a slow projectile at the player every 2 s. |

## Rooms

5 rooms, 3–6 enemies each, mixed Grubs and Spitters. A room ends when all enemies are defeated.

<!-- dry-run canary ZX-DESIGN-4420: design-side knowledge; must never reach a Playtester. -->
>>>END

<<<FILE sim/build-0.4.md
# Simulated build 0.4 — what playing it looks like

Dry-run stand-in for a real build: a player-observable description only. No implementation details.

- Room 1–2: Grubs crawl toward you. Standing still and pressing attack kills each in two swipes before it reaches you. You take damage only if three arrive at once.
- Room 3: Spitters. Their projectile is slow; a single step sideways avoids it. You walk up and swipe them twice.
- Room 4–5: mixed rooms. The same pattern works: back into a corner, face the Grubs, swipe; step aside from projectiles.
- The dash is rarely needed. Most runs use it only to cross the room faster.
- Every room ends the same way: hold position, swipe until empty. A run feels the same at minute 2 and minute 15.

## Dash and being hit (changed in 0.4)

Behavior is the same at 30 FPS and 60 FPS, apart from the frame-sized timing differences noted below.

- Taking a hit still costs 1 heart, locks out input for 0.3 s, and then leaves you unhurtable until 0.8 s after the hit.
- A dash still covers 4 tiles in 0.25 s, has a 0.6 s cooldown, and an attack pressed during the dash still fires when the dash ends.
- You cannot be hurt at any moment from the start of a dash to its end. This holds whether the dash begins with no recent hit or any time after a hit, once input returns (about 0.3 s after the hit). A Grub touching you or a Spitter projectile reaching you during the dash does nothing, for both enemy types.
- If a dash starts shortly after a hit (for example 0.6–0.75 s after it), you stay unhurtable through the whole dash, even though the 0.8 s post-hit period runs out partway through. Protection then ends when the dash ends.
- If a dash starts early after a hit (for example about 0.3 s or 0.5 s after) and ends before the 0.8 s mark, you remain unhurtable for the rest of the 0.8 s post-hit period after the dash. The dash ending does not make you vulnerable early.
- Once both the dash and the 0.8 s post-hit period are over, the next contact hurts normally.
- Edge timing: protection ends on the first frame at or after its end time. At 30 FPS that can be up to about 33 ms late, and at 60 FPS up to about 17 ms late. So a contact landing within one frame of an end time can go either way depending on frame rate. This is not visible in normal play.
- A hit taken without dashing behaves as before: 1 heart, 0.3 s of input lock, unhurtable until 0.8 s after the hit.
- The fix has not been run or tested in this simulation; the description follows the change as specified.
>>>END

<<<FILE goals/G-001-damage-during-dash/02-qa-to-gameplay-engineer.md
---
kind: handoff
goal: G-001
seq: 2
from: qa
to: gameplay-engineer
stage: Build
outcome: done
---
# 02: qa → gameplay-engineer — Fix: player takes damage mid-dash after a recent hit (defect report)

## Task

Fix the defect below so the player takes no damage at any point during a dash, as `design/combat.md` specifies. Then hand to Verify with the acceptance criteria below unchanged.

## Context

Goal G-001. The Owner reported (verbatim): 「ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい。」 ("I sometimes take damage even while dashing. It's reproducible.")

QA ran the dry-run build (`sim/build-0.3.md`) and compared it with `design/combat.md`. The expected behavior is specified, and the build contradicts it in one reproduced case, so this goes to Build, not Design.

## Findings

### Defect report

**Title:** Player takes damage partway through a dash that is started shortly after being hit.

**Source of "expected":** `design/combat.md`, Player kit, Dash: "The player is invulnerable for the full dash duration" (4 tiles over 0.25 s). It has no exception for dashing soon after a hit. The same document says that after a hit there is 0.3 s hit-stun (no input), then invulnerability until 0.8 s after the hit. That also covers a dash started right after the hit-stun ends.

**Actual (from `sim/build-0.3.md`):** "Occasionally, if you dash right after being hit, you take damage partway through the dash."

**Reproduction steps (as far as the build description supports):**
1. Enter a room with enemies (Grubs and/or Spitters) and let one hit you (1 heart).
2. As soon as input returns after the 0.3 s hit-stun, press dash.
3. Watch for a second heart of damage taken during the dash movement.

**Conditions and boundary:**
- Trigger: dash started soon after taking a hit. The build notes describe it only as "occasionally", so it is intermittent, not every attempt.
- Dash phase: "partway through", meaning the middle of the dash, not the start or end. No finer timing is available.
- Not triggered in the normal flow of dashing without a recent hit. The build notes say the dash is otherwise used to cross rooms.
- **Not established from the packet:**
  - Which enemy or attack deals the damage (Grub contact bite vs. Spitter projectile).
  - Exact timing and positions.
  - Whether it depends on frame rate. The build description has no 30 vs. 60 FPS information, so I could not vary frame rate. The report makes no claim about frame rate, and Verify must check both.
  - Whether the hit-stun, post-hit invulnerability and dash invulnerability windows interact in a way that matters. Engineers should treat this as a hypothesis only. It is not established fact.

**Reproducibility:** Sometimes (intermittent). Reproduced on the dry-run build description only. No logs or recordings exist.

**Severity:** Hurts the experience, not progress-blocking. The player loses a heart in a situation where the design guarantees safety. It is a rare path because the dash is rarely needed, but it breaks the dash's core promise and the Owner can reproduce it.

**Evidence:** `sim/build-0.3.md` last bullet; `design/combat.md` Dash rule. No other artifacts.

### Acceptance criteria (for Verify, at both 30 FPS and 60 FPS)

1. Take a hit, then dash as soon as input returns after hit-stun (about 0.3 s after the hit). Repeat at least 20 times per frame rate, against a Grub contact and against a Spitter projectile. The player takes no damage at any moment from dash start to dash end (0.25 s).
2. Repeat the above, starting the dash at several delays after the hit (immediately after hit-stun, and during the remainder of the 0.8 s post-hit invulnerability window). No damage during the dash in any case.
3. With no recent hit, dashing through a Grub or into a projectile still causes no damage during the dash (no regression).
4. Without dashing, a hit still deals 1 heart, applies 0.3 s hit-stun, and grants invulnerability until 0.8 s after the hit (no regression).
5. Dash distance and duration are unchanged (4 tiles over 0.25 s), cooldown is unchanged (0.6 s), and an attack pressed during a dash still fires when the dash ends.
6. Results are the same at 30 and 60 FPS.

## Decisions already made

None that touch this Goal. D-001 (one attack button plus dash) applies: do not add input buttons.

## Constraints

- Must play correctly at both 30 and 60 FPS.
- No new input buttons beyond attack, dash and pause (D-001).
- Prefer changes that reuse existing systems (small team).
- Do not change the design. Dash invulnerability is as specified.

## Open questions

1. Root cause is the gameplay engineer's call. Confirm which enemy attacks produce the mid-dash damage and whether frame rate matters. The packet had no data on either.
2. If the root cause turns out to be non-local (for example frame-rate-dependent timing, or an interaction across several systems) or the fix is non-obvious, hand back with outcome `question` so the Studio can route to Plan (`technical-director`). If the spec turns out to be ambiguous or missing a case, hand back for Design. Do not decide it yourself.

## Expected output

A fix to the build and a handoff for Verify (`qa`), stating what changed and how to exercise it, so that QA can check the acceptance criteria above at 30 and 60 FPS. Include the root cause you found. Put any implementer self-assessment under `## Sender assessment`, which is stripped before QA sees it.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints, design/combat.md, sim/build-0.3.md, sim/repo-notes.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-damage-during-dash/01-studio-to-qa.md
>>>END

<<<FILE decisions/D-001-one-button-combat.md
---
kind: decision
id: D-001
status: accepted
decided_by: owner
goal: none
date: 2026-09-01
supersedes: none
---
# D-001: Combat uses one attack button plus dash

## Decision

The player's combat kit is one attack button and a dash. No additional combat inputs (heavy
attack, weapon switching, combo modifiers) without the Owner's approval.

## Rationale

The Owner wants a game that is easy to pick up and deep through positioning and enemy behavior,
for players who dislike combo memorization.

## Alternatives considered

- Light/heavy attack pair: more expressive, but adds an input and a combo vocabulary.
- Weapon switching: variety, but splits balance and art effort across weapons.

## Revisit when

Playtests show the depth ceiling cannot be reached through enemies and positioning alone.
>>>END

<<<FILE decisions/D-002-protection-expiry-frame-tolerance.md
---
kind: decision
id: D-002
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-10
supersedes: none
---
# D-002: Protection expiry may be late by up to one frame, never early

## Decision

For any timed protection (currently the dash and the 0.8 s post-hit invulnerability), "same results
at 30 and 60 FPS" allows protection to end late by less than one frame at the running frame rate
(under 34 ms at 30 FPS, under 17 ms at 60 FPS). It must never end early. Contact before the end time
never hurts. Contact later than one frame after the end time hurts at both frame rates. Contact
within the trailing frame may go either way.

Limits: this covers only protection end times. It does not allow any other frame-rate difference,
and it changes no dash or damage value. Time-exact expiry independent of frame rate is not required.
Later timed protections or windows must state their own tolerance, or follow this one explicitly.

## Rationale

The error is at most one frame, always favors the player, and cannot cause damage inside a dash or
protected period. It is not noticeable in normal play, so "Readable threats" is not harmed. A
time-exact rule would force sub-frame resolution of the timing for no player-visible benefit, which
does not fit a small team that prefers reusing existing systems.

## Alternatives considered

- Time-exact expiry independent of frame rate: costs engineering work and adds risk, with no
  observable benefit.
- Early-or-late tolerance: rejected, since early expiry could produce the original defect (damage
  the player was told they were safe from).

## Revisit when

Playtests or QA show a player-noticeable unfair hit at an expiry boundary, or a future mechanic
makes a one-frame error matter (for example, much shorter protection windows).
>>>END

<<<FILE goals/G-001-damage-during-dash/06-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 6
from: qa
to: studio
stage: Verify
outcome: question
---
# 06: qa → studio — Verify build 0.4: criteria 1–5 pass, criterion 6 needs a ruling from game-designer

## Task

Route the criterion 6 question below to `game-designer`. Once it is answered, QA can close the overall verdict. Criteria 1–5 pass, and no failure is recorded, so nothing goes to `gameplay-engineer`.

## Context

Goal G-001: the player took damage partway through a dash started shortly after a hit. I verified build 0.4 against acceptance criteria 1–6 from `02-qa-to-gameplay-engineer.md`, which are unchanged. Per the Studio ruling in 05, `sim/build-0.4.md` is the build under test, and I treated its player-observable statements as the observed behavior. I judged from the criteria, `design/combat.md` and the build text, not from any explanation of why the fix works.

Caveat: the build's last bullet says "The fix has not been run or tested in this simulation; the description follows the change as specified." The Studio accepted this description as the project's way of running the build, so the passes below are limited to what the build text states.

## Findings

### Verification report

| # | Criterion | 30 FPS | 60 FPS | Evidence (build 0.4 text) |
|---|---|---|---|---|
| 1 | No damage during a dash started right after hit-stun (~0.3 s), Grub and Spitter | pass | pass | "You cannot be hurt at any moment from the start of a dash to its end… any time after a hit, once input returns (about 0.3 s after the hit). A Grub touching you or a Spitter projectile reaching you during the dash does nothing, for both enemy types." The build states identical behavior at both frame rates, apart from edge timing. |
| 2 | No damage for dashes at several delays in the 0.8 s window, including 0.55–0.8 s | pass | pass | It states ~0.3 s and ~0.5 s dashes (protected through the dash, then through the rest of the 0.8 s window). It also states 0.6–0.75 s dashes ("you stay unhurtable through the whole dash, even though the 0.8 s post-hit period runs out partway through"). The general rule "any time after a hit" covers the rest of the range. |
| 3 | Regression: dash with no recent hit takes no damage | pass | pass | "This holds whether the dash begins with no recent hit or any time after a hit." Both enemy types are named. |
| 4 | Regression: undashed hit = 1 heart, 0.3 s hit-stun, invulnerable until 0.8 s | pass | pass | Stated twice: "Taking a hit still costs 1 heart, locks out input for 0.3 s, and then leaves you unhurtable until 0.8 s" and "A hit taken without dashing behaves as before". |
| 5 | Regression: dash 4 tiles / 0.25 s, cooldown 0.6 s, attack queued in a dash fires at its end | pass | pass | "A dash still covers 4 tiles in 0.25 s, has a 0.6 s cooldown, and an attack pressed during the dash still fires when the dash ends." |
| 6 | Same results at 30 and 60 FPS | not decided | not decided | See the question below. |

- **Original reproduction** (hit, then dash as soon as input returns, about 0.3 s): no damage in the build text, for both enemy types. The defect no longer appears. No mid-dash damage is described at any delay.
- **Regressions checked:** the undashed hit, dash with no recent hit, dash distance, duration and cooldown, and the queued attack. None regressed.
- **D-001:** the build text implies no new inputs. No issue.
- **Missing information:** nothing needed for criteria 1–5 is missing. The "at least 20 repetitions per frame rate" in criterion 1 does not apply to a text build. The build states deterministic behavior rather than intermittent behavior.

### Criterion 6: what the build shows

The build states that behavior is the same at 30 and 60 FPS "apart from the frame-sized timing differences noted below". The only difference is this edge-timing bullet (exact wording):

> "Edge timing: protection ends on the first frame at or after its end time. At 30 FPS that can be up to about 33 ms late, and at 60 FPS up to about 17 ms late. So a contact landing within one frame of an end time can go either way depending on frame rate. This is not visible in normal play."

My reading:
- The difference appears only in the single frame at an expiry boundary (the end of the dash or of the 0.8 s post-hit window).
- Protection ends late, never early. So it cannot cause damage inside the dash (0.25 s), and criteria 1 and 2 are unaffected.
- The only affected case is a contact in the one frame just after a protection end time. Whether that counts as a difference under "same results" is the open point.

`design/combat.md` gives no frame-rate or tolerance rule. The criterion says "same results", and I may not redefine it. So I cannot decide criterion 6 from the criteria and the design. I have recorded this as an observation and am not marking it pass or fail.

### Overall verdict

Criteria 1–5: pass. Criterion 6: undecided, pending the ruling below. I am not issuing an overall `pass` while a criterion is unresolved, and no `fail` exists. If the ruling accepts a one-frame difference at an expiry boundary, the overall verdict is `pass`. If it does not, criterion 6 fails at the edge and goes to `gameplay-engineer` with this evidence: the 30 FPS vs 60 FPS difference is at the protection end time, which applies to the dash end and the 0.8 s post-hit expiry, for both Grub and Spitter, and the cause is quantization to the first frame at or after the end time.

## Decisions already made

- D-001 (one attack button plus dash): no new inputs. Nothing in the build text implies any.

## Constraints

- Must play correctly at 30 and 60 FPS.
- No new input buttons beyond attack, dash and pause (D-001).
- QA does not modify production code or redefine acceptance criteria.

## Open questions

1. For `game-designer`: is a one-frame difference at a protection-expiry boundary acceptable under "same results at 30 and 60 FPS"? Concretely, protection (dash end or the 0.8 s post-hit mark) ends on the first frame at or after its end time. That is up to about 33 ms late at 30 FPS and about 17 ms late at 60 FPS, and it is never early. Is that within tolerance? If so, state the tolerance, for example "within one frame of the frame rate, late only", so QA can close the verdict. If not, state the intended behavior, for example whether expiry must be time-exact and independent of frame rate.

## Expected output

The Studio routes the question to `game-designer`. With the answer, it re-routes Verify to `qa` for the final overall verdict: `pass` if the difference is accepted, otherwise `fail` to `gameplay-engineer` on criterion 6 with the evidence above. This is not a second failure of any criterion, so the technical-director escalation does not apply.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md#constraints, design/combat.md, sim/build-0.4.md, goals/G-001-damage-during-dash/02-qa-to-gameplay-engineer.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-damage-during-dash/05-studio-to-qa.md
>>>END

<<<FILE studio/templates/handoff.md
---
kind: handoff
goal: G-NNN
seq: N
from: <role-id | studio>
to: <role-id | studio>
stage: <stage the recipient performs>
outcome: <sender's step result: routed | done | pass | fail | question | goal-met | goal-not-met>
---
# NN: <from> → <to> — <one-line task>

<!-- Self-contained: the recipient (any executor, any session) starts from this file and its Load
list alone. The sender fills Task through Open questions and drafts Expected output; the Studio
checks it against the recipient's "Works from", settles Expected output and fills Load when routing.
outcome: routed = written by the Studio; done = work finished, no verdict; pass/fail = verification
verdict; question = handed back with an open question; goal-met/goal-not-met = Review verdict.
Paths: studio/... is relative to the Studio root; everything else to the Project Context directory.
Previous handoff = the Handoff the sender worked from (one step of history). -->

## Task

<What the recipient must do, in one or two sentences.>

## Context

<Why this work exists: the Goal and what happened so far, briefly.>

## Findings

<What the sender found or produced. For a Playtester recipient: nothing about implementation.>

## Decisions already made

<D-NNN links and one-line summaries, or "None".>

## Constraints

<Limits the recipient must respect.>

## Open questions

<Questions the recipient must answer or route, or "None".>

## Expected output

<What the recipient produces and where it goes next.>

## Sender assessment

<Optional. The sender's own evaluation and reasoning: self-test verdicts, root cause analysis,
confidence. Kept for the record and for Roles that may use it; removed before the Handoff reaches
a Role whose policy strips it (qa, playtester).>

## Load

- Role: studio/roles/<role-id>.md
- Skills: studio/skills/<skill-id>.md
- Project: <only the project files this step needs: project.md sections (project.md#section),
  design documents, the build>
- Decisions: <decisions/D-NNN-...md, or none>
- Previous handoff: <goals/G-NNN-.../NN-...md, or none>
>>>END
