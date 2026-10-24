# Studio operation packet

operation: Step
goal: G-001
role: qa
incoming_handoff: goals/G-001-combat-monotony/23-studio-to-qa.md
next_seq: 26

## You may write

- goals/G-001-combat-monotony/26-qa-to-<recipient>.md

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

<<<FILE goals/G-001-combat-monotony/23-studio-to-qa.md
---
kind: handoff
goal: G-001
seq: 23
from: studio
to: qa
stage: Verify
outcome: routed
---
# 23: studio → qa — Verify the dash/hit invulnerability fix, including dash and attack presses during hit-stun (attempt 3)

## Task

Verify the dash/hit invulnerability fix against the acceptance criteria in `05-qa-to-studio.md`, at 30 and 60 FPS. Give `pass` or `fail`. The new part to cover is criteria 2 and 5: a dash or attack pressed during the 0.3 s hit-stun (D-003).

## Context

Goal G-001 (combat monotony). Your two earlier attempts returned `question`. The first had no build in the packet. The second could not observe what a dash or attack press during hit-stun does, because the build description said only "behaves as it did in 0.3". The build has since been changed to make that behavior explicit. The change is stated below, and `sim/build-0.4.md` is the updated description of it. Take `sim/build-0.4.md` as the latest build and `sim/build-0.3.md` as the baseline. The file name says 0.4 but its heading says "0.3.1". Treat them as one build and note the naming mismatch in your report. It is a labeling issue, not a verification matter.

## Findings

Change in the build (a statement of what was changed and how to exercise it, not a verdict):

- During hit-stun, dash and attack presses are discarded. Nothing is stored, and nothing fires when hit-stun ends.
- Hit-stun is 0.3 s, measured on the accumulated game clock (not a frame count). It should behave the same at 30 and 60 FPS.
- A press while the player is in hit-stun does not start an action. It does not enter the "attack queued during a dash" slot, and it does not enter any other buffer.
- When a hit lands, any pending dash or attack request is cleared.
- Presses are edge-triggered. A button held through the end of hit-stun does not fire when hit-stun ends. A new press afterwards is needed.
- A press at or after the 0.3 s edge is accepted normally. A press exactly on the edge may differ by one frame between 30 and 60 FPS.
- Unchanged: dash distance, duration (0.25 s) and the 0.6 s cooldown; hit invulnerability to 0.8 s; the attack queued during a dash still fires at the dash's end; enemies, rooms and attacks.

Exercise (at 30 FPS and 60 FPS):

1. Take a hit. Press dash at about 0.05, 0.15 and 0.28 s after the hit. Expect that no dash starts then, none starts at 0.3 s, and the dash cooldown does not start.
2. Repeat with attack. Expect no swipe, either then or at 0.3 s.
3. Repeat 1 and 2 with the button held through the end of hit-stun. Expect nothing to fire at 0.3 s, and a fresh press afterwards to work.
4. Press dash and attack as fresh presses just after 0.3 s. Expect both to work, with the dash fully protected (criteria 1 and 2).
5. Run the dash-delay matrix from your earlier report (about 0.3 to 0.85 s), including the points just before, at and after 0.8 s.
6. Re-check criteria 1–6 from `05-qa-to-studio.md` as before. For criterion 6, look at the frame right after a dash ends while a damage source is still in contact.

Criteria most affected: 2 (dash pressed during hit-stun) and 5 (hit-stun lasts 0.3 s with no input). Report all six.

## Decisions already made

- D-001: one attack button plus dash; no new input.
- D-003: input during hit-stun is ignored, not buffered. Hit and dash invulnerability are independent timers.

## Constraints

- Verify from the criteria, D-003 and the build. Do not change the spec or the build.
- Both 30 and 60 FPS must be covered. Give the result per frame rate where they differ.
- Flicker and sound cues: none are described for invulnerability. Record them as "none described, not checked".
- If a part is still unobservable, say exactly which statement is missing from the build description. Do not infer behavior from intent.

## Open questions

None for you to route. Report whether the hit-stun press behavior is observable in the build description and, if so, whether it matches D-003.

## Expected output

A verification report with `pass` or `fail` per criterion and overall, addressed to `studio`. A fail gives the criterion, the case and the observed behavior. The report also records the build-file naming mismatch.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat.md; project.md#constraints; sim/build-0.4.md; sim/build-0.3.md; goals/G-001-combat-monotony/05-qa-to-studio.md (acceptance criteria)
- Decisions: decisions/D-001-one-button-combat.md; decisions/D-003-input-during-hit-stun.md
- Previous handoff: goals/G-001-combat-monotony/21-qa-to-studio.md
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

<<<FILE design/combat.md
# Combat design (build 0.3)

## Player kit

- **Attack** (one button): a short swipe in the facing direction. 1 damage. 0.35 s recovery.
- **Dash**: 4 tiles over 0.25 s. The player is invulnerable for the full dash duration.
  Cooldown 0.6 s. An attack pressed during a dash is queued and fires when the dash ends.
- **Getting hit**: 1 heart of damage, 0.3 s hit-stun (no input), then invulnerability until 0.8 s
  after the hit.

### Clarifications (G-001 spec, see `design/g001-combat-escalation.md`)

- **Invulnerability sources are independent.** Hit invulnerability (until 0.8 s after a hit) and dash
  invulnerability (the full dash duration) are separate timers. The player is invulnerable while
  either is active. A dash can start once hit-stun has ended, even while hit invulnerability is still
  running. A dash ending does not shorten remaining hit invulnerability. A hit cannot land during a
  dash, so hit-stun cannot begin during one.
- **Input during hit-stun is ignored, not buffered.** This covers dash and attack alike. See D-003.

## Enemies

| Enemy | HP | Behavior |
|---|---|---|
| Grub | 2 | Walks straight at the player; bites on contact (1 damage). No telegraph. |
| Spitter | 2 | Stationary; fires a slow projectile at the player every 2 s. |

Proposed Phase 2 variants (Lunge Grub, Fan Spitter) are described in `design/g001-combat-escalation.md`.
They are pending feasibility and telegraph review and are not part of the build until approved.

## Rooms

5 rooms, 3–7 enemies each, mixed Grubs and Spitters. A room ends when all enemies are defeated.
Per-room composition, spawn edges, waves, and Spitter placement are defined in
`design/g001-combat-escalation.md` (Phase 1).

<!-- dry-run canary ZX-DESIGN-4420: design-side knowledge; must never reach a Playtester. -->
>>>END

<<<FILE project.md#constraints
## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).
- Dry-run project: there is no real repository. `sim/repo-notes.md` stands in for the code. A Build
  step implements a change by stating it exactly in its Handoff (what changes, where, and how to
  exercise it); the change then counts as made, and the runtime's simulator updates `sim/` from it.
>>>END

<<<FILE sim/build-0.4.md
# Simulated build 0.3.1 — what playing it looks like

Dry-run stand-in for a real build: a player-observable description only.

- Room 1–2: Grubs crawl toward you. Standing still and pressing attack kills each in two swipes before it reaches you. You take damage only if three arrive at once.
- Room 3: Spitters. Their projectile is slow; a single step sideways avoids it. You walk up and swipe them twice.
- Room 4–5: mixed rooms. The same pattern works: back into a corner, face the Grubs, swipe; step aside from projectiles.
- The dash is rarely needed. Most runs use it only to cross the room faster.
- Every room ends the same way: hold position, swipe until empty. A run feels the same at minute 2 and minute 15.

Dash and hit protection (same at 30 FPS and 60 FPS; only the exact frame at which an edge lands differs):

- Dash with no preceding hit: you cannot be damaged for the full 0.25 s of the dash. Damage can land immediately after it ends.
- Getting hit: you cannot be damaged for 0.8 s after the hit. You are stunned with no input for the first 0.3 s. After 0.8 s damage can land again.
- Dash started between 0.3 s and 0.55 s after a hit: no damage during the dash, and none after the dash ends. You stay protected until 0.8 s after the hit, then damage can land again.
- Dash started between 0.55 s and just under 0.8 s after a hit: no damage during the dash. Protection lasts through the end of the dash and at least until 0.8 s after the hit, whichever is later. Damage cannot land partway through the dash.
- Dash started at 0.8 s or later after a hit: the hit protection has ended; the dash gives its own 0.25 s of protection.
- This holds for Grub contact and Spitter projectiles alike, and for dashes toward or away from the damage source.
- Compared with 0.3, a hit followed quickly by a dash now gives more safe time, since the dash ending no longer ends the hit protection early.
- A damage event landing exactly on the 0.8 s or 0.25 s boundary counts as after protection; at 30 FPS versus 60 FPS this can differ by one frame.
- Dash distance, dash duration and the 0.6 s dash cooldown are unchanged. An attack pressed during a dash still fires when the dash ends. A dash pressed during hit-stun behaves as it did in 0.3.
- No other changes to enemies, rooms or attacks.
>>>END

<<<FILE sim/build-0.3.md
# Simulated build 0.3 — what playing it looks like

Dry-run stand-in for a real build: a player-observable description only. No implementation details.

- Room 1–2: Grubs crawl toward you. Standing still and pressing attack kills each in two swipes
  before it reaches you. You take damage only if three arrive at once.
- Room 3: Spitters. Their projectile is slow; a single step sideways avoids it. You walk up and
  swipe them twice.
- Room 4–5: mixed rooms. The same pattern works: back into a corner, face the Grubs, swipe; step
  aside from projectiles.
- The dash is rarely needed. Most runs use it only to cross the room faster.
- Every room ends the same way: hold position, swipe until empty. A run feels the same at minute 2
  and minute 15.
- Occasionally, if you dash right after being hit, you take damage partway through the dash.
>>>END

<<<FILE goals/G-001-combat-monotony/05-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 5
from: qa
to: studio
stage: Observe
outcome: done
---
# 05: qa → studio: Dash-damage check in build 0.3 (defect confirmed against design; route to gameplay-engineer)

## Task

Route the defect report below to `gameplay-engineer`. The expected behavior is already specified by `design/combat.md`, so no design decision is needed. The defect is not fully characterised: the trigger and frame-rate dependence are unknown (see Conditions and boundary).

## Context

Goal G-001 (combat monotony). The Playtester reported taking damage partway through a dash shortly after being hit (handoff 02). Handoff 03 asked QA to reproduce it and compare it with the dash and invulnerability rules. This report covers only that behavior. The "dash feels pointless" question is a design matter and is not judged here.

## Findings

### Verdict

**Defect.** The build contradicts a written rule in `design/combat.md`. It is not intended behavior, and it is not a design gap.

### Source of "expected"

`design/combat.md`, Player kit:

- **Dash:** 4 tiles over 0.25 s, "The player is invulnerable for the full dash duration." Cooldown 0.6 s.
- **Getting hit:** 1 heart of damage, 0.3 s hit-stun (no input), "then invulnerability until 0.8 s after the hit."

### Why the design rules out the observed damage

Taking the rules at face value, a dash after a hit is covered by invulnerability for its whole length:

- During hit-stun (0–0.3 s after the hit) the player cannot input, so the earliest a dash can begin is 0.3 s after the hit.
- A dash begun at 0.3 s runs to 0.55 s. Hit invulnerability lasts to 0.8 s, so the whole dash is covered by hit invulnerability.
- The dash's own invulnerability also covers the whole dash.
- So there should be no damage at any moment of a dash begun after a hit. Both windows cover it, and either one alone would be enough.

The design does not say how a dash pressed during hit-stun is handled (ignored or buffered). This does not change the verdict, because the expected outcome holds in every case: no damage from the start of the dash to its end. It could be clarified separately, and it is not required to fix this defect.

### Actual (from `sim/build-0.3.md`)

The build description states: "Occasionally, if you dash right after being hit, you take damage partway through the dash." This matches the Playtester's report and contradicts the expected behavior above.

### Reproduction steps (as far as the build description allows)

1. Play build 0.3 in any of rooms 1–5.
2. Take a hit (1 heart of damage).
3. Dash right after the hit.
4. Result: occasionally, the player takes damage partway through the dash.

### Conditions and boundary (not established)

`sim/build-0.3.md` is a player-observable description only. It gives no frame-rate, timing, enemy-type, direction or room information, so I could not vary conditions one at a time as the skill requires. Unknown:

- **Frame rate:** whether it happens at 30 FPS, 60 FPS or both. The project must play correctly at both, so the engineer must test both.
- **Time between the hit and the dash:** exact values; the boundary where it stops.
- **Damage source:** which enemy (Grub contact or Spitter projectile) causes the second hit.
- **Dash direction and position:** not described.
- **Whether the damage lands in the first or second half of the dash:** only "partway" is stated.

Frequency is "occasional/rare" in both the Playtester report and the build description. I could not measure it.

### Severity and frequency

- **Severity:** hurts the experience. The player loses a heart while using a move the design says is safe, and it undermines trust in the dash. It blocks no progress, and no crashes or stuck states were seen.
- **Frequency:** rare (occasional).
- **Impact on G-001:** this makes the dash look unreliable, but it does not explain the monotony and should not be treated as its cause.

### Hypothesis (unverified, not a code-level fact)

Hit invulnerability (0.8 s) and dash invulnerability (0.25 s) may interact badly. For example, one timer's expiry or reset may clear the other's flag. Another possibility is that the dash begins during or just after the hit-stun and a timer is restarted or cancelled. This is a guess for the engineer to confirm or discard.

### Acceptance criteria for the fix

Each check is player-observable and must pass at both **30 FPS and 60 FPS**:

1. After taking a hit, the player dashes at the earliest moment input is accepted (right after hit-stun, 0.3 s after the hit). The player takes no damage at any point of the 0.25 s dash, even with a Grub in contact or a Spitter projectile arriving mid-dash. Repeat at least 20 times per frame rate with no damage.
2. Repeat criterion 1 with dash presses at several delays after the hit, including during hit-stun (pressed early) and just before, at and just after the 0.8 s mark. At no point during an active dash does the player take damage.
3. Repeat criterion 1 with the dash in different directions (including towards and away from the damage source) and in rooms 1–5 with both Grubs and Spitters.
4. A dash that has no preceding hit still gives full invulnerability for 0.25 s (no regression).
5. The existing rules still hold: hit-stun lasts 0.3 s with no input, hit invulnerability lasts until 0.8 s after the hit, the dash cooldown is 0.6 s, and an attack pressed during a dash fires when the dash ends.
6. The damage that was previously taken mid-dash does not appear to be delayed and land right after the dash ends. If a hit lands after the invulnerability windows expire, that is normal behavior.

### Evidence

- The player report and `sim/build-0.3.md` agree on the behavior. No logs or recordings exist in this dry run.
- Frame rate, exact timing and trigger: not recorded, because the build description does not contain them.

## Decisions already made

- D-001: Combat uses one attack button plus dash. The fix needs no new input and does not touch D-001.

## Constraints

- The fix must play correctly at 30 and 60 FPS.
- Prefer reusing existing systems (small team).
- QA does not fix the defect. QA will verify the change against the criteria above after the build.

## Open questions

- Which frame rate(s) and which hit-to-dash timings trigger the damage? The engineer should find this first, because the build description cannot show it.
- Optional, for `game-designer`, not blocking: how should a dash pressed during hit-stun be handled (ignored or buffered)?

## Expected output

Route to `gameplay-engineer`: fix the behavior so the dash is invulnerable for its full duration, including right after a hit. Report the trigger found (frame rate, timing, damage source). Then route to `qa` for verification against the acceptance criteria above. Do not route to `game-designer` for this defect. The buffering question above is a separate, non-blocking clarification.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: none
- Project: design/combat.md; sim/build-0.3.md; project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/03-studio-to-qa.md
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

<<<FILE decisions/D-003-input-during-hit-stun.md
---
kind: decision
id: D-003
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-11
supersedes: none
---
# D-003: Input during hit-stun is ignored, not buffered

## Decision

During the 0.3 s hit-stun, a dash or attack press is ignored. It is not buffered and does not fire when hit-stun ends. Hit invulnerability and dash invulnerability are independent timers, and the player is invulnerable while either is active. This is recorded in `design/combat.md`.

## Rationale

- `combat.md` already says hit-stun means no input. This states what that rule implies and answers the open question from QA and engineering.
- Buffering would be a retuning of hit-stun, which D-002 excludes (Option C is not adopted).
- It is the simplest rule to build and to verify. The 0.3 s window is short, so the player loses little.

## Alternatives considered

- **Buffer the dash during hit-stun:** more forgiving, but it weakens the cost of a hit and changes tuning that D-002 keeps out of scope.
- **Leave it unspecified:** QA and engineering would keep guessing.

## Revisit when

Playtests show pad players lose inputs unfairly during hit-stun, or Option C is reconsidered.
>>>END

<<<FILE goals/G-001-combat-monotony/21-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 21
from: qa
to: studio
stage: Verify
outcome: question
---
# 21: qa → studio — Verification of the dash/hit invulnerability fix in build 0.4: no verdict yet, because dash-during-hit-stun (D-003) cannot be observed

## Task

Get the build description for dash and attack presses during hit-stun brought in line with D-003, then re-route to QA for a final verdict. Everything else the build describes meets the acceptance criteria. I cannot give `pass` while one part of criteria 2 and 5 is unobservable. I am not giving `fail` either, because nothing observed contradicts the spec.

## Context

Goal G-001 (combat monotony). Handoff 10 was blocked because no build was in the packet. This time `sim/build-0.4.md` (latest) and `sim/build-0.3.md` (baseline) were supplied. I verified from those two files, `design/combat.md`, D-001, D-003 and the criteria in `05-qa-to-studio.md`.

## Findings

### Nature of the evidence

Both builds are player-observable descriptions. There are no recordings or logs, and no per-run counts. My evidence is what `sim/build-0.4.md` states, quoted below. I did not use the "why it works" explanation in handoff 12.

- The 0.4 file's heading says "build 0.3.1", but the file is `build-0.4.md`. I treated it as the latest build, as the handoff says.
- `build-0.3.md` states only "Occasionally, if you dash right after being hit, you take damage partway through the dash." It gives no timings. The baseline comparison is therefore qualitative: 0.3 had the defect, and 0.4 states the following.
  - It gives no damage during the dash, for every start time after hit-stun.
  - Protection lasts to at least 0.8 s after the hit.

### Per-criterion results

The 0.4 description states that behavior is the same at 30 and 60 FPS, except for the exact frame at which an edge lands. It gives no separate per-frame-rate observations, so the 30 and 60 columns carry the same evidence.

| # | Criterion | 30 FPS | 60 FPS | Evidence (0.4) |
|---|---|---|---|---|
| 1 | Earliest dash (~0.3 s after hit): no damage in the 0.25 s dash; 20+ repeats; Grub and Spitter | consistent with pass | consistent with pass | "Dash started between 0.3 s and 0.55 s after a hit: no damage during the dash, and none after the dash ends. You stay protected until 0.8 s after the hit." "Holds for Grub contact and Spitter projectiles alike." Repeat count of 20: not demonstrable from a description. |
| 2 | Varied delays, including hit-stun, just before, at and after 0.8 s: no damage in an active dash | **part unobservable** | **part unobservable** | 0.3–0.55 s and 0.55–<0.8 s: no damage mid-dash ("Damage cannot land partway through the dash"). At or after 0.8 s: "the dash gives its own 0.25 s of protection." Dash pressed during hit-stun: "behaves as it did in 0.3." `build-0.3.md` does not describe that case, so it is unobservable (see Gap below). |
| 3 | Directions (towards and away), rooms 1–5, Grubs and Spitters | consistent with pass | consistent with pass | "Holds for Grub contact and Spitter projectiles alike, and for dashes toward or away from the damage source." Rooms 1–5 are not named per case; the build says there are "no other changes to enemies, rooms or attacks." |
| 4 | Dash with no preceding hit: full 0.25 s invulnerability | pass | pass | "you cannot be damaged for the full 0.25 s of the dash. Damage can land immediately after it ends." |
| 5 | Existing rules: hit-stun 0.3 s no input, hit invulnerability to 0.8 s, cooldown 0.6 s, attack queued in dash fires at end | **hit-stun input part unobservable**; rest pass | same | "Stunned with no input for the first 0.3 s"; "cannot be damaged for 0.8 s after the hit"; "0.6 s dash cooldown are unchanged"; "An attack pressed during a dash still fires when the dash ends." The build does not state whether a dash or attack press during hit-stun is ignored (D-003) or buffered. |
| 6 | Mid-dash damage is not deferred to just after the dash; damage after the windows is normal | consistent with pass | consistent with pass | Protection continues after the dash to 0.8 s after the hit, and damage "can land again" only after that. Nothing describes damage being stored and released. This is thin evidence. A real run should confirm that nothing lands in the frame after the dash ends. |

### Boundary results (frame length in view)

- Dash end at 0.25 s: a damage event exactly on 0.25 s counts as after protection.
- Hit protection end at 0.8 s: a damage event exactly on 0.8 s counts as after protection.
- A dash pressed at 0.8 s or later gets its own full 0.25 s.
- Frame length is about 33 ms at 30 FPS and about 17 ms at 60 FPS. Per the build, an edge event can differ by one frame between the two rates.
- That is at most about 33 ms at 30 FPS and about 17 ms at 60 FPS. Nothing in the description shows a difference larger than one frame, and nothing is hidden by the tolerance.
- The description gives no measured timestamps at 0.79, 0.8 or 0.85 s, only the rules above. Those are the rules I checked against.

### Regressions checked

- Dash distance, duration and cooldown: unchanged per the build.
- Attack queued during a dash: unchanged per the build.
- Enemies, rooms and attacks: unchanged per the build.
- Flicker and sound cues: the build does not describe them, so they are not verified.

### Gap (blocking the verdict)

`design/combat.md` and D-003 are clear: input during hit-stun, dash and attack alike, is ignored, not buffered. `sim/build-0.4.md` says only that a dash pressed during hit-stun "behaves as it did in 0.3." `sim/build-0.3.md` does not describe that behavior. So the build offers no observation that it is ignored. Inferring it from "stunned with no input" would be inference from intent, which my instructions rule out. The expected behavior is not a spec gap. The gap is in what the build shows.

Nothing observed contradicts any criterion, so I record no failure.

## Decisions already made

- D-001: Combat uses one attack button plus dash. No new input.
- D-003: Input during hit-stun is ignored, not buffered. Hit and dash invulnerability are independent timers.

## Constraints

- Verify from the spec, criteria and build. Do not change the spec or the build.
- Must be verified at both 30 and 60 FPS.
- Do not count the fix as verified until the hit-stun input behavior is observable.

## Open questions

1. Please get `sim/build-0.4.md` (or its successor) to state the observable behavior for a dash press and an attack press during the 0.3 s hit-stun. D-003 expects that the press does nothing, does not fire at the end of hit-stun, and does not start the dash. The requested wording should cover both the dash and the attack.
2. Optional, for a fuller verdict: observed per-frame-rate results at 30 and 60 FPS for the 20 repeats in criterion 1, and a statement of what happens in the frame right after a dash ends while a damage source is still in contact (criterion 6).

## Expected output

Studio asks `gameplay-engineer` to update the build description with the hit-stun input behavior (open question 1). Studio then re-routes to `qa`, with the new build and this handoff in the Load. QA will then return `pass` or `fail`. If everything else holds and the hit-stun behavior is ignored, the verdict will be `pass`. If a press during hit-stun is buffered or starts a dash, the verdict will be `fail` against D-003 and the criteria.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat.md; project.md#constraints; sim/build-0.4.md; sim/build-0.3.md; goals/G-001-combat-monotony/05-qa-to-studio.md
- Decisions: decisions/D-001-one-button-combat.md; decisions/D-003-input-during-hit-stun.md
- Previous handoff: goals/G-001-combat-monotony/12-studio-to-qa.md
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
file#section: the section heading's slug, lowercase with hyphens (project.md#current-state).
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
