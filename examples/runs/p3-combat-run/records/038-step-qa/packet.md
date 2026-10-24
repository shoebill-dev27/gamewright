# Studio operation packet

operation: Step
goal: G-001
role: qa
incoming_handoff: goals/G-001-combat-monotony/30-studio-to-qa.md
next_seq: 31

## You may write

- goals/G-001-combat-monotony/31-qa-to-<recipient>.md

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

<<<FILE goals/G-001-combat-monotony/30-studio-to-qa.md
---
kind: handoff
goal: G-001
seq: 30
from: studio
to: qa
stage: Verify
outcome: routed
---
# 30: studio → qa — Verify the dash-damage fix (incl. hit-stun input) against build 0.5, with the criteria text supplied

## Task

Verify the dash-damage fix, including the hit-stun input part, against `sim/build-0.5.md` and give a per-criterion verdict for criteria 1–6 plus an overall `pass` or `fail`. This repeats the verification of handoff 28. The only change is that the text of the acceptance criteria is now in your Load list.

## Context

- Goal G-001 (combat monotony). Before Phase 1 of the chosen direction is built, the earlier dash-damage fix and the hit-stun input change must be verified.
- Build under verification: `sim/build-0.5.md` (D-007). `sim/build-0.3.md` is the baseline only. `sim/build-0.4.md` is outdated; do not use it.
- Your previous report (handoff 29) found every observable statement in `sim/build-0.5.md` consistent with the criteria. It could not give a verdict because the criteria text was missing. That text is in `goals/G-001-combat-monotony/05-qa-to-studio.md` (your defect report with the acceptance criteria), and handoff 23 restates and numbers the criteria. Both are in the Load list now.
- The hit-stun statements are present in build 0.5. That question is closed. This is not a hand-back on the same missing input.

## Findings

Nothing from the implementation side is passed to you. Your own handoff 29 (sections A to D) is in the Load list. You may reuse its observations from `sim/build-0.5.md`, but re-check each against the criteria text, since that text is new to you.

## Decisions already made

- D-003: input during hit-stun is ignored, not buffered.
- D-007: verify against `sim/build-0.5.md`; `sim/build-0.4.md` is outdated.

## Constraints

- Do not widen or narrow the criteria. Use the wording in handoff 05 and the numbering in handoff 23. If the two disagree, report exactly where and judge against 05.
- Must hold at both 30 and 60 FPS. A one-frame difference at an exact boundary is allowed where the spec allows it.
- Do not modify the build.
- Loop limit: if the criteria text for any numbered criterion is still not available after this Handoff, say exactly which criterion and what is missing. The Studio will then escalate to the Owner for that input and will not route it to a Role again.

## Open questions

- Is the wording of criteria 1–6 now sufficient to give a verdict on each? If not, which criterion is unclear?
- Keep your optional notes: the frame after a dash ends with a source in contact; the file name versus heading mismatch (`sim/build-0.5.md` reads "0.3.2").

## Expected output

A verification report (verify-change) with a verdict for each of criteria 1–6, an overall `pass` or `fail`, and the regression check against the baseline. Write it as a handoff addressed to `studio`. Do not hand back `question` unless a criterion's text is truly missing or contradictory; if it is, name it.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: sim/build-0.5.md, sim/build-0.3.md (baseline only), design/combat.md, project.md#constraints
- Decisions: decisions/D-003-input-during-hit-stun.md, decisions/D-007-verify-against-build-0-5.md
- Previous handoff: goals/G-001-combat-monotony/29-qa-to-studio.md
- Also: goals/G-001-combat-monotony/05-qa-to-studio.md (acceptance criteria text), goals/G-001-combat-monotony/23-studio-to-qa.md (criteria numbering), goals/G-001-combat-monotony/28-studio-to-qa.md (the previous request)
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

<<<FILE sim/build-0.5.md
# Simulated build 0.3.2 — what playing it looks like

- Room 1–2: Grubs crawl toward you. Standing still and pressing attack kills each in two swipes before it reaches you. You take damage only if three arrive at once.
- Room 3: Spitters. Their projectile is slow; a single step sideways avoids it. You walk up and swipe them twice.
- Room 4–5: mixed rooms. The same pattern works: back into a corner, face the Grubs, swipe; step aside from projectiles.
- The dash is rarely needed. Most runs use it only to cross the room faster.
- Every room ends the same way: hold position, swipe until empty. A run feels the same at minute 2 and minute 15.

Dash and hit protection (same at 30 FPS and 60 FPS; only the exact frame at which an edge lands differs):

- Dash with no preceding hit: you cannot be damaged for the full 0.25 s of the dash. Damage can land immediately after it ends.
- Getting hit: you cannot be damaged for 0.8 s after the hit. You are stunned for the first 0.3 s.
- Dash started between 0.3 s and 0.55 s after a hit: no damage during the dash, and none after it ends. You stay protected until 0.8 s after the hit, then damage can land again.
- Dash started between 0.55 s and just under 0.8 s after a hit: no damage during the dash. Protection lasts through the end of the dash and at least until 0.8 s after the hit, whichever is later.
- Dash started at 0.8 s or later after a hit: the hit protection has ended; the dash gives its own 0.25 s of protection.
- This holds for Grub contact and Spitter projectiles alike, and for dashes toward or away from the damage source.
- A damage event landing exactly on the 0.8 s or 0.25 s boundary counts as after protection; at 30 FPS versus 60 FPS this can differ by one frame.

Input during the 0.3 s stun after a hit (same at 30 FPS and 60 FPS):

- Pressing dash at any moment in the first 0.3 s (for example about 0.05, 0.15 or 0.28 s after the hit) does nothing. The player does not dash, the dash cooldown does not start, and no dash happens when the stun ends.
- Pressing attack at any moment in the first 0.3 s does nothing. No swipe appears then, and none appears when the stun ends.
- Holding dash or attack down through the end of the stun does nothing at that moment. Nothing fires until the button is released and pressed again. A fresh press after the stun ends works normally.
- A dash or attack pressed just after 0.3 s works normally, and the dash is fully protected as described above.
- A press landing exactly at 0.3 s may be accepted on one frame earlier or later at 30 FPS than at 60 FPS.
- If a swipe was pressed during a dash, it still fires when the dash ends. A hit cannot land during a dash, so this never overlaps the stun.
- A hit that lands cancels any dash or attack request that was waiting, so nothing carries into the stun.
- Dash distance, dash duration and the 0.6 s dash cooldown are unchanged. No other changes to enemies, rooms or attacks.
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

<<<FILE decisions/D-007-verify-against-build-0-5.md
---
kind: decision
id: D-007
status: accepted
decided_by: owner
goal: G-001
date: 2026-10-11
supersedes: none
---
# D-007: Verify the hit-stun input change against `sim/build-0.5.md`; `sim/build-0.4.md` is outdated

## Decision

The Owner chose Option A of Escalation 27 in substance. The build description that reflects the Build 3c change (handoff 20) already exists as `sim/build-0.5.md`. QA re-verifies the dash-damage fix, including the hit-stun input part, against `sim/build-0.5.md`. `sim/build-0.4.md` is an outdated version and is no longer the build under verification.

Owner's words (from Escalation 27): "A の内容はもう用意されています。ハンドオフ20の変更を反映したビルドは sim/build-0.5.md にあります（sim/build-0.4.md は古い版です）。0.5 で QA に再検証させてください。"

Limits:
- No change to the acceptance criteria (handoff 23, criteria 1–6) or to D-003.
- Options B and C are not used. QA verifies from the build description and does not rely on the engineer's account.
- The Owner added no further conditions.

## Rationale

The only blocker was that the build description lacked the hit-stun statements. The Owner supplied a description that has them, so the independent verification QA's Role requires can proceed without reducing its scope or independence.

## Alternatives considered

- Option B (use Handoff 20 as a substitute build record): lowers QA independence. Not needed now.
- Option C (carry criteria 2 and 5 forward and start Phase 1): leaves D-003 unverified under Phase 1. Not needed now.

## Revisit when

If `sim/build-0.5.md` also turns out not to state the hit-stun behavior, QA hands back `question` a fourth time for the same input. Do not route to a Role again; escalate to the Owner for that input (loop limit).
>>>END

<<<FILE goals/G-001-combat-monotony/29-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 29
from: qa
to: studio
stage: Verify
outcome: question
---
# 29: qa → studio — Build 0.5 verification: every observable statement passes, but the wording of criteria 1–6 is not in my packet

## Task

Verify the dash-damage fix, including the hit-stun input part, against `sim/build-0.5.md` per criteria 1–6 of handoff 23. This is a partial report. The hit-stun input part (the new part) is fully observable in build 0.5 and passes. I cannot give an overall pass or fail because the text of the six criteria is missing from my packet.

## Context

- The build under verification is `sim/build-0.5.md` (D-007). `sim/build-0.3.md` was used as baseline only. `sim/build-0.4.md` was not used.
- The hit-stun statements in the build description are present. This is **not** a fourth hand-back on the missing hit-stun statements. Nothing is missing from `sim/build-0.5.md`.
- The criteria themselves are the problem. Handoff 23 says they are in `goals/G-001-combat-monotony/05-qa-to-studio.md`, but neither that file nor handoff 23's list of the criteria is in my Load or inputs. Handoff 23 characterises only these:
  - criteria 1 and 2: dash protection, with criterion 2 covering a dash pressed during hit-stun;
  - criterion 5: hit-stun lasts 0.3 s with no input;
  - criterion 6: the frame right after a dash ends while a damage source is in contact.
- I know of criteria 3 and 4 only by number. I will not guess their wording, because that would widen or narrow them, which the handoff forbids.

## Findings

### A. The six hit-stun statements from handoff 28 (criteria 2 and 5), judged from `sim/build-0.5.md`

Each result is the same at 30 and 60 FPS, as the build states. The header says "same at 30 FPS and 60 FPS".

| # | Statement | Result | Evidence in build 0.5 |
|---|---|---|---|
| 1 | A dash press in hit-stun starts no dash and no cooldown | PASS | "Pressing dash at any moment in the first 0.3 s (about 0.05, 0.15 or 0.28 s)… does nothing. The player does not dash, the dash cooldown does not start, and no dash happens when the stun ends." |
| 2 | An attack press in hit-stun gives no swing and enters no dash-queue buffer | PASS | "Pressing attack at any moment in the first 0.3 s does nothing. No swipe appears then, and none appears when the stun ends." Also: "A hit that lands cancels any dash or attack request that was waiting." The description is player-observable, so the buffer is judged by its observable effect. Nothing fires later, which satisfies it. |
| 3 | Nothing fires or is stored at the end of the stun | PASS | The same two bullets: nothing at 0.3 s. |
| 4 | A held button does not fire. Release and re-press works | PASS | "Holding dash or attack down through the end of the stun does nothing at that moment. Nothing fires until the button is released and pressed again. A fresh press after the stun ends works normally." |
| 5 | Presses after 0.3 s are accepted normally. The boundary frame may differ between 30 and 60 FPS | PASS | "A dash or attack pressed just after 0.3 s works normally, and the dash is fully protected." Also: "A press landing exactly at 0.3 s may be accepted on one frame earlier or later at 30 FPS than at 60 FPS." |
| 6 | Hit-stun length is the same at 30 and 60 FPS | PASS | The header says "same at 30 FPS and 60 FPS; only the exact frame at which an edge lands differs." The stun is "the first 0.3 s" in all bullets. |

The behavior matches D-003: input is ignored, not buffered.

### B. Dash/hit invulnerability matrix (original defect and related criteria)

I checked each case against `design/combat.md`: the two invulnerability timers are independent, a dash ending does not shorten hit invulnerability, and a hit cannot land during a dash.

| Case | Build 0.5 states | Result |
|---|---|---|
| Dash with no preceding hit | Invulnerable for the full 0.25 s. Damage can land right after the dash ends. | PASS |
| Dash started 0.3–0.55 s after a hit | No damage during the dash or after it, until 0.8 s after the hit. | PASS. This is the original defect case: the 0.3 baseline took damage partway through the dash. |
| Dash started 0.55 s to just under 0.8 s | Protected until the later of the dash end and 0.8 s. | PASS |
| Dash started at 0.8 s or later | Hit protection has ended. The dash gives its own 0.25 s. | PASS |
| Grub contact vs Spitter projectile, and dash toward vs away | Stated to hold for all combinations. | PASS |
| Boundary at exactly 0.8 s or 0.25 s | Counts as after protection. It can differ by one frame between 30 and 60 FPS. | PASS. This is the allowed edge-frame difference. |

### C. Regressions checked against 0.3

- The build states these are unchanged: dash distance, dash duration (0.25 s), the 0.6 s cooldown, enemies, rooms and attacks.
- "A swipe pressed during a dash still fires when the dash ends." This matches `design/combat.md`.
- The build states this never overlaps the stun, since a hit cannot land during a dash.
- The room and pacing observations match 0.3. This was expected, because Phase 1 is not yet built.
- I found no regression.

### D. Optional notes

- **Frame right after a dash ends with a damage source in contact (criterion 6):** damage can land on that frame. In the no-hit case it lands immediately. After a hit, the later of the dash end and 0.8 s governs. The build states the boundary frame counts as "after protection". It differs by at most one frame between 30 and 60 FPS, which is consistent with the spec.
- **Naming mismatch:** the file is `sim/build-0.5.md` but its heading reads "Simulated build 0.3.2". Handoff 23 recorded the same kind of mismatch for 0.4/"0.3.1". This is a labeling issue only, and I treated the file as build 0.5 per D-007.
- **Invulnerability flicker and sound cues:** none described, not checked.

## Decisions already made

- D-003: input during hit-stun is ignored, not buffered. Build 0.5 matches it.
- D-007: verify against `sim/build-0.5.md`. I did.

## Constraints

- I did not widen or narrow the criteria. I did not modify the build.
- I cannot assign per-criterion verdicts for criteria 1–6 by number without their text. The role forbids passing on unseen criteria.

## Open questions

1. Please re-route this verification with `goals/G-001-combat-monotony/05-qa-to-studio.md` (the text of acceptance criteria 1–6) added to the Load. The build description needs no further input.
2. With that file, I expect to confirm the verdict from the evidence above. No failure was observed, and every statement in sections A and B passes.

## Expected output

A re-run with the criteria text produces a per-criterion verdict and an overall `pass` or `fail`. This hand-back is for a different missing input from the three earlier ones, which were about the hit-stun description. Routing is therefore not the loop the D-007 limit describes. If the Studio disagrees, the pending decision is whether to accept the section A and B evidence as sufficient and proceed to Phase 1. I cannot make that call, because the role forbids passing a change when a criterion is unjudged.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: sim/build-0.5.md, sim/build-0.3.md (baseline only), design/combat.md, project.md#constraints
- Decisions: decisions/D-003-input-during-hit-stun.md, decisions/D-007-verify-against-build-0-5.md
- Previous handoff: goals/G-001-combat-monotony/28-studio-to-qa.md
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

<<<FILE goals/G-001-combat-monotony/28-studio-to-qa.md
---
kind: handoff
goal: G-001
seq: 28
from: studio
to: qa
stage: Verify
outcome: routed
---
# 28: studio → qa — Verify the dash-damage fix (including hit-stun input) against build 0.5

## Task

Verify the dash-damage fix against the acceptance criteria 1–6 in handoff 23, using `sim/build-0.5.md` as the build under verification. Give a verdict (pass / fail) per criterion, or hand back `question` only if a criterion truly cannot be judged from the build description.

## Context

Goal G-001 (combat monotony). The fix for damage during a dash after being hit (defect confirmed earlier) is built and has to be verified before Phase 1 work starts. Earlier verification attempts ended without a verdict because the build description then in use did not state what happens when dash or attack is pressed during hit-stun. The Owner has since supplied the current build description, `sim/build-0.5.md` (D-007). `sim/build-0.4.md` is an outdated version: do not use it as the build under verification. `sim/build-0.3.md` is the baseline for comparison only.

## Findings

Nothing from implementation is passed on. Verify from the criteria and the build description.

Statements to observe in the build description, as the hit-stun part of criteria 2 and 5 (intended behavior per D-003):
1. During the 0.3 s hit-stun, a dash press does not start a dash and does not start the dash cooldown.
2. During hit-stun, an attack press produces no swing and does not enter the "attack queued during dash" buffer.
3. At the end of hit-stun (0.3 s), neither press fires or has been stored.
4. Holding a button until hit-stun ends does not fire it; releasing and pressing again works normally.
5. Presses after 0.3 s are accepted normally (the boundary frame may differ between 30 and 60 FPS).
6. The hit-stun length is the same at 30 and 60 FPS.

Optional items to note if visible in the build: the frame right after a dash ends while a damage source is in contact; any mismatch between a version heading in a build file and its file name.

## Decisions already made

- D-003: input during hit-stun is ignored, not buffered.
- D-007 (Owner): verify against `sim/build-0.5.md`; `sim/build-0.4.md` is outdated.

## Constraints

- Both 30 FPS and 60 FPS must be correct (project constraint).
- Judge from the build description and the spec, not from any explanation of why it should work.
- Do not widen or narrow the acceptance criteria; handoff 23 defines them.

## Open questions

None. If a statement above is not stated by `sim/build-0.5.md`, say exactly which one and in which file. This would be the fourth hand-back on the same missing input, and the Studio will then escalate to the Owner instead of routing again.

## Expected output

A verification report with a verdict per criterion and an overall verdict, plus any regressions and the optional notes. Address the result to `studio`. Set `outcome` to `pass`, `fail` or `question`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: sim/build-0.5.md (build under verification), sim/build-0.3.md (baseline only), design/combat.md, project.md#constraints
- Decisions: decisions/D-003-input-during-hit-stun.md, decisions/D-007-verify-against-build-0-5.md
- Previous handoff: goals/G-001-combat-monotony/23-studio-to-qa.md (acceptance criteria 1–6)
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
