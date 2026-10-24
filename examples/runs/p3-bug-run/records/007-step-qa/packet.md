# Studio operation packet

operation: Step
goal: G-001
role: qa
incoming_handoff: goals/G-001-dash-damage/03-gameplay-engineer-to-qa.md
next_seq: 4

## You may write

- goals/G-001-dash-damage/04-qa-to-<recipient>.md

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

<<<FILE goals/G-001-dash-damage/03-gameplay-engineer-to-qa.md
---
kind: handoff
goal: G-001
seq: 3
from: gameplay-engineer
to: qa
stage: Verify
outcome: done
---
# 03: gameplay-engineer → qa — Verify fix: player takes damage mid-dash when the dash overlaps the end of post-hit invulnerability

## Task

Verify the change below against the acceptance criteria in handoff 02, at both 30 FPS and 60 FPS. Give a pass or fail verdict.

## Context

Goal G-001. The Owner reported: "Sometimes I take damage even while dashing." QA's defect report (02) established that `design/combat.md` says the dash makes the player invulnerable for its full 0.25 s. It also says a hit is followed by 0.3 s hit-stun and then invulnerability until 0.8 s after the hit. The change is stated below and counts as made, per the dry-run rules in `project.md#constraints`.

## Findings

### Change

Where: the player invulnerability logic. The enemy controller, hit-stun, dash movement and cooldown are not touched.

What:
1. The shared invulnerability on/off flag and its two "switch the flag off" timer callbacks are removed.
2. Two independent sources of invulnerability remain:
   - Dash source: the player is invulnerable while the dash state is active, read from the dash state itself.
   - Post-hit source: on a hit, `hitInvulnUntil = hitTime + 0.8 s` is stored, using accumulated game time. The source is active while `gameTime < hitInvulnUntil`.
3. `isInvulnerable = isDashing || gameTime < hitInvulnUntil`.
4. The damage check reads `isInvulnerable` at the moment damage would apply.

Frame rate: both sources compare against accumulated game time or the dash state, with no per-frame countdown.

Tests added: unit tests stepping the simulation at fixed delta times of 1/30 s and 1/60 s, covering hit then dash at several offsets, a dash with no prior hit, damage resuming after the invulnerability window, and a dash and a hit in the same frame.

### How to exercise it (maps to the acceptance criteria in 02)

At both 30 FPS and 60 FPS:
1. Get hit, then dash at about 0.3 s, 0.4 s, 0.55 s, 0.7 s and 0.79 s after the hit, with a Grub in contact range. Expect no damage for the full dash (criteria 1 and 2).
2. Repeat with a Spitter projectile crossing the dash path (criterion 3).
3. Dash with no recent hit and enemies in contact range. Expect no damage (criterion 4).
4. Regression (criterion 5):
   - Dash is still 4 tiles over 0.25 s, with a 0.6 s cooldown.
   - An attack pressed during a dash is still queued and fires when the dash ends.
   - A hit still deals 1 heart with 0.3 s hit-stun.
   - After a dash that ends before 0.8 s after the hit, the player stays invulnerable until 0.8 s after the hit.
   - Once the dash and the post-hit window have both ended, the player takes damage normally.
5. Also try a dash started and a dash ended while an enemy is in contact range (edge frames of the dash).

## Decisions already made

- D-001: no new input buttons beyond attack, dash and pause. This change adds none.

## Constraints

- Must play correctly at both 30 and 60 FPS.
- Desktop, keyboard and gamepad.
- No new input buttons (D-001).

## Open questions

None.

## Expected output

A verification Handoff with outcome `pass` or `fail`, stating the result for each acceptance criterion at 30 FPS and at 60 FPS. Address the result to `studio`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md#constraints, design/combat.md, sim/build-0.4.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-dash-damage/02-qa-to-gameplay-engineer.md
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
- Dry-run project: there is no real repository. `sim/repo-notes.md` stands in for the code. A Build
  step implements a change by stating it exactly in its Handoff (what changes, where, and how to
  exercise it); the change then counts as made, and the runtime's simulator updates `sim/` from it.
>>>END

<<<FILE design/combat.md
# Combat design (build 0.3)

## Player kit

- **Attack** (one button): a short swipe in the facing direction. 1 damage. 0.35 s recovery.
- **Dash**: 4 tiles over 0.25 s. The player is invulnerable for the full dash duration.
  Cooldown 0.6 s. An attack pressed during a dash is queued and fires when the dash ends.
- **Getting hit**: 1 heart of damage, 0.3 s hit-stun (no input), then invulnerability until 0.8 s
  after the hit.

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

Observations are the same at 30 FPS and 60 FPS, apart from timing differences of up to about one frame (roughly 33 ms at 30 FPS, 17 ms at 60 FPS) at the moment protection after a hit runs out.

- Room 1–2: Grubs crawl toward you. Standing still and pressing attack kills each in two swipes before it reaches you. You take damage only if three arrive at once.
- Room 3: Spitters. Their projectile is slow; a single step sideways avoids it. You walk up and swipe them twice.
- Room 4–5: mixed rooms. The same pattern works: back into a corner, face the Grubs, swipe; step aside from projectiles.
- The dash is still rarely needed. Most runs use it only to cross the room faster. It covers 4 tiles in 0.25 s, with a 0.6 s wait before you can dash again.
- Every room ends the same way: hold position, swipe until empty. A run feels the same at minute 2 and minute 15.
- Dashing right after being hit: dashing at about 0.3, 0.4, 0.55, 0.7 or 0.79 s after a hit, with a Grub touching you or a Spitter projectile crossing your path, you take no damage for the whole dash, including its last moment. This holds at both frame rates.
- Dashing with no recent hit, with enemies in contact range or projectiles crossing the path: no damage during the dash.
- After a hit you lose 1 heart and are stunned for 0.3 s. You are then untouchable until 0.8 s after the hit. If you dash early in that period and the dash ends before 0.8 s, you stay untouchable until 0.8 s after the hit; enemies in contact do not hurt you until then. After that, contact damages you normally.
- Once both the dash and the period after a hit are over, enemies and projectiles hurt you normally (1 heart per hit).
- An attack pressed during a dash is remembered and swings as soon as the dash ends.
- A dash that begins or ends while an enemy is touching you: no damage during the dash. Damage can land on the first frame after the dash ends if the 0.8 s period after a hit is also over.
- Because the period after a hit is no longer cut short by an early dash, you may feel slightly safer right after being hit than in build 0.3.
- Enemies hit by your swipe still briefly flinch and interrupt what they were doing.
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

<<<FILE goals/G-001-dash-damage/02-qa-to-gameplay-engineer.md
---
kind: handoff
goal: G-001
seq: 2
from: qa
to: gameplay-engineer
stage: Build
outcome: done
---
# 02: qa → gameplay-engineer — Fix: player takes damage mid-dash when dashing shortly after being hit

## Task

Find the root cause of the defect below and fix it, so the player takes no damage at any point during a dash. QA will verify against the acceptance criteria.

## Context

Goal G-001. The Owner reported (originally in Japanese): "Sometimes I take damage even while dashing. It is reproducible, so please fix it." No steps were provided. QA checked `design/combat.md` for the intended behavior and `sim/build-0.3.md` for the observed behavior (the dry-run stand-in for running the build).

## Findings

### Defect report

**Expected (source: `design/combat.md`, Player kit → Dash):**
"Dash: 4 tiles over 0.25 s. The player is invulnerable for the full dash duration. Cooldown 0.6 s."
The design is unambiguous: dash makes the player fully invulnerable for its whole 0.25 s. There is no spec gap on this point, so this is a defect, not a design question.

**Related rule (same document, Getting hit):** "1 heart of damage, 0.3 s hit-stun (no input), then invulnerability until 0.8 s after the hit."

**Actual (source: `sim/build-0.3.md`, last bullet):**
"Occasionally, if you dash right after being hit, you take damage partway through the dash."
Damage is taken during the dash, which contradicts the design.

**Reproduction steps (as far as the build description supports):**
1. Enter a room with enemies (Grubs, which bite on contact, or Spitters, which fire projectiles). The enemy type is not identified in the build notes.
2. Get hit once. This causes 1 heart of damage, then 0.3 s of hit-stun with no input.
3. As soon as input returns, press dash.
4. Observe: in some runs the player takes damage partway through the dash.

**Conditions and boundary (known / unknown):**
- Known: it happens when a dash is started shortly after a hit. The build notes describe it as occasional.
- Known from the design timings: input returns 0.3 s after a hit, and post-hit invulnerability ends at 0.8 s after the hit. A dash started in the 0.3–0.8 s window therefore overlaps the post-hit invulnerability period. A dash started after about 0.55 s would also outlast it (0.55 + 0.25 = 0.8 s). The observed window might be related to this overlap. This is a **hypothesis only**, not a confirmed cause.
- Not determinable from the build notes: which enemy type causes the damage, which part of the dash it falls in (start, middle or end), and whether it depends on frame rate. The build notes say nothing about FPS, so QA cannot claim the defect is or is not frame-rate dependent. Please check both 30 and 60 FPS while diagnosing.
- Not established: whether dashing without a recent hit is also affected. The build notes only describe the after-hit case. Cover this in verification.

**Severity:** Hurts the experience. It breaks a core rule of the dash (a trust issue for the player) but does not block progress. The build notes say the dash is rarely needed and the damage is occasional.

**Frequency:** Occasional. No rate was given. The Owner calls it reproducible, but the exact trigger is not known.

**Evidence:** Only the build description and the design text quoted above. No recordings or logs exist in this dry-run.

### Acceptance criteria for the fix

All checks are player-observable and must be done at **both 30 FPS and 60 FPS**.
1. After getting hit, dash at the earliest moment input returns (about 0.3 s after the hit) while a Grub is in contact range. No damage during the full 0.25 s dash.
2. Repeat criterion 1 with dashes started at about 0.4 s, 0.55 s, 0.7 s and 0.79 s after the hit. No damage at any point during any dash, including when the dash runs past the 0.8 s post-hit invulnerability end.
3. Repeat criterion 1 with a Spitter projectile crossing the dash path. No damage during the dash.
4. A dash with no recent hit is also damage-free for its full duration.
5. Regression checks:
   - Dash is still 4 tiles over 0.25 s, with a 0.6 s cooldown.
   - An attack pressed during a dash is still queued and fires when the dash ends.
   - A hit still deals 1 heart, with 0.3 s of hit-stun and invulnerability until 0.8 s after the hit.
   - The player can be damaged normally once the dash and any post-hit invulnerability have ended.

## Decisions already made

- D-001: no new input buttons beyond attack, dash and pause. The fix must not add one.

## Constraints

- Must play correctly at both 30 and 60 FPS.
- Desktop, keyboard and gamepad.
- Prefer changes that reuse existing systems (small team).
- No new input buttons (D-001).
- The root cause is yours to determine. QA has not examined the code and the hypothesis above is unverified.
- Because this is a dry-run project, state the change exactly in your handoff (what changes, where, and how to exercise it).

## Open questions

- What is the actual root cause, and does it depend on frame rate?
- Does the defect also occur with no recent hit? If so, the "after being hit" framing is incomplete.
- If the Owner can supply further detail (enemy type, exact timing, FPS), it would help, but it is not required to start diagnosis.

## Expected output

A Handoff to `qa` (Verify) stating the root cause and the exact change (what, where, how to exercise it), so QA can verify against the acceptance criteria above at 30 and 60 FPS. Put your reasoning and self-test verdicts in `## Sender assessment`; it is removed before QA receives the Handoff, so everything QA needs to exercise the change must be in the other sections. If you find that the intended behavior in the design is actually unclear when dash and post-hit invulnerability overlap, hand back with outcome `question` and the specific point; the Studio will route it to `game-designer`. If the root cause is cross-system or risky, say so; the Studio may add a Plan step.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints, design/combat.md, sim/repo-notes.md, sim/build-0.3.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-dash-damage/01-studio-to-qa.md
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
