# Studio operation packet

operation: Step
goal: G-001
role: qa
incoming_handoff: goals/G-001-combat-monotony/12-studio-to-qa.md
next_seq: 15

## You may write

- goals/G-001-combat-monotony/15-qa-to-<recipient>.md

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

<<<FILE goals/G-001-combat-monotony/12-studio-to-qa.md
---
kind: handoff
goal: G-001
seq: 12
from: studio
to: qa
stage: Verify
outcome: routed
---
# 12: studio → qa — Verify the dash/hit invulnerability fix against the named build

## Task

Verify, in the build named under Load, that taking damage during a dash shortly after a hit no longer happens. Check at 30 FPS and at 60 FPS, and return a `pass` or `fail` report with per-criterion evidence.

## Context

Goal G-001 (combat monotony). QA earlier confirmed a defect: after the player is hit and dashes within the hit-invulnerability window, damage could land during the dash (`05-qa-to-studio.md`). A fix has been made. Your previous attempt (`10-qa-to-studio.md`) was blocked because no build file was in the packet. The build files are now listed explicitly under Load.

## Findings

Acceptance criteria (from `05-qa-to-studio.md`, as summarized in your handoff 10):

1. Dash at the earliest moment (about 0.3 s after the hit): no damage during the 0.25 s dash, at least 20 repeats per frame rate, with Grub contact and with Spitter projectile.
2. Dash presses at varied delays after the hit (including during hit-stun, and just before, at and after 0.8 s): no damage during an active dash.
3. Different dash directions (towards and away from the damage source), rooms 1–5, Grubs and Spitters.
4. Dash with no preceding hit: full 0.25 s invulnerability, no regression.
5. Existing rules hold: hit-stun 0.3 s with no input, hit invulnerability to 0.8 s, dash cooldown 0.6 s, attack queued during a dash fires at its end.
6. Damage that would have landed mid-dash is not delayed to land right after the dash ends; damage after the windows expire is normal.

Notes:
- `design/combat.md` was clarified since your last look: hit invulnerability and dash invulnerability are independent timers, and the player is invulnerable while either is active (D-003 also fixes input during hit-stun as ignored, not buffered). The clarification restores no new behavior and adds none. The room enemy range there is now 3–7 (for a later phase; not part of this check).
- The dash-during-hit-stun case is now specified as ignored (D-003). Check it as part of criterion 2 and 5.
- Record boundary results around 0.8 s and 0.85 s with the frame length at 30 FPS (about 33 ms) and 60 FPS (about 17 ms) in view.
- Your plan in handoff 10 (matrix, repeat counts, flicker/sound cues) stands.

## Decisions already made

- D-001: Combat uses one attack button plus dash.
- D-003: Input during hit-stun is ignored, not buffered; hit and dash invulnerability are independent timers.

## Constraints

- Verify from `design/combat.md`, the acceptance criteria and the build. Do not change the spec or the build.
- Must be verified at both 30 and 60 FPS.
- The latest build is `sim/build-0.4.md`; `sim/build-0.3.md` is the baseline for comparison. If neither shows the fix (or the fix cannot be observed), report that as a blocker with `outcome: question`. Do not infer behavior from descriptions of intent.

## Open questions

None new. The non-blocking question about dash during hit-stun is answered by D-003.

## Expected output

A verification report to `studio` with `outcome: pass` or `fail`, per-criterion results at 30 and 60 FPS with evidence, regressions checked, and any undefined behavior found.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat.md; project.md#constraints; sim/build-0.4.md; sim/build-0.3.md; goals/G-001-combat-monotony/05-qa-to-studio.md (defect report with the original criteria)
- Decisions: decisions/D-001-one-button-combat.md; decisions/D-003-input-during-hit-stun.md
- Previous handoff: goals/G-001-combat-monotony/10-qa-to-studio.md
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

<<<FILE goals/G-001-combat-monotony/10-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 10
from: qa
to: studio
stage: Verify
outcome: question
---
# 10: qa → studio — Verification of the dash/hit invulnerability fix could not be done: the 0.3.1 build was not in the packet

## Task

Re-route the verification to QA with the build that is actually player-visible (`sim/build-0.3.1.md` or the latest `sim/build-*.md`). Verification is blocked, and no pass/fail verdict is given.

## Context

Goal G-001 (combat monotony). Handoff 09 asked QA to verify the 0.3 → 0.3.1 fix for "damage during a dash shortly after a hit" against the six acceptance criteria in `05-qa-to-studio.md`, at 30 and 60 FPS.

The Load list of handoff 09 names "the latest build under sim/ (`sim/build-*.md`)". No `sim/` file was supplied to this step. The inputs were:

- the handoff;
- the QA role and the `verify-change` skill;
- `design/combat.md`;
- project.md;
- D-001;
- handoff 05.

The role and skill require QA to observe behavior in the build, not to rely on the engineer's explanation. The only description of the change is the "What changed" text in handoff 09. That is a description of intent. It is not observed behavior, and it must not stand in for evidence. Passing or failing any criterion from it would be invented evidence.

## Findings

### Verdict

No verdict (`pass` or `fail`). Verification is **blocked** for lack of the build. Nothing was observed, so nothing is reported as passing.

### Per-criterion status (all from handoff 05)

| # | Criterion | 30 FPS | 60 FPS | Evidence |
|---|---|---|---|---|
| 1 | Dash at the earliest moment (~0.3 s after the hit): no damage during the 0.25 s dash, at least 20 repeats, Grub contact or Spitter projectile | not verified | not verified | no build available |
| 2 | Dash presses at varied delays after the hit (including during hit-stun, and just before, at and after 0.8 s): no damage during an active dash | not verified | not verified | no build available |
| 3 | Different dash directions (towards and away from the source), rooms 1–5, Grubs and Spitters | not verified | not verified | no build available |
| 4 | Dash with no preceding hit: full 0.25 s invulnerability, no regression | not verified | not verified | no build available |
| 5 | Existing rules hold: hit-stun 0.3 s with no input, hit invulnerability to 0.8 s, dash cooldown 0.6 s, attack queued during a dash fires at its end | not verified | not verified | no build available |
| 6 | Previously mid-dash damage is not delayed to land right after the dash ends; damage after the windows expire is normal | not verified | not verified | no build available |

### Regressions checked

None. I could not check the flicker or sound cues that may have depended on the old shared invulnerability state, because there is no build to observe.

### Undefined-behavior cases

- A dash pressed during hit-stun (ignored or buffered) is unspecified in `design/combat.md`. Handoff 09 says the handling is unchanged. I could not observe it, so I have no observation to report. It stays an open, non-blocking question for `game-designer`, as already noted in handoff 05.
- Handoff 09 expects a one-frame difference for damage landing exactly on a 0.8 s or 0.25 s boundary (`now < expiry`). Once the build is available, I will record boundary results at 0.8 s and 0.85 s with the frame at 30 FPS (about 33 ms) and 60 FPS (about 17 ms) in view. The one-frame tolerance will not hide a failure of more than one frame.

### Plan once the build is available

1. Run the matrix from handoff 09 at 30 and 60 FPS. Use dash delays of 0.3, 0.4, 0.5, 0.55, 0.6, 0.7, 0.79, 0.8 and 0.85 s after the hit. Keep a damage source present through the dash and until at least 0.8 s after the hit.
2. For each run, record whether damage landed:
   - during the dash;
   - between the dash end and 0.8 s after the hit;
   - after 0.8 s with no dash active.
3. Run the no-hit dash.
4. Cover both dash directions, rooms 1–5, and both enemy types.
5. Repeat the earliest-dash case at least 20 times per frame rate.
6. Check the cooldown, hit-stun, queued attack, and flicker/sound cues.

## Decisions already made

- D-001: Combat uses one attack button plus dash. No new input is involved.

## Constraints

- Verify from `design/combat.md`, the acceptance criteria and the build.
- Do not change the spec or the build.
- Must be verified at both 30 and 60 FPS.

## Open questions

- Please supply `sim/build-0.3.1.md` (the latest `sim/build-*.md`). Without it QA cannot verify the change.
- Non-blocking, for `game-designer`: how should a dash pressed during hit-stun be handled?

## Expected output

Studio re-routes to `qa` with the 0.3.1 build included in the Load. QA then returns a `pass` or `fail` verification report with per-criterion evidence at 30 and 60 FPS. If the build still cannot be supplied, Studio should say so and not count the fix as verified.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat.md; project.md#constraints; the latest `sim/build-*.md` (must be included this time)
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/09-studio-to-qa.md
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
