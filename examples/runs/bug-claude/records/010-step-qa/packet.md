# Studio operation packet

operation: Step
goal: G-001
role: qa
incoming_handoff: goals/G-001-damage-during-dash/05-studio-to-qa.md
next_seq: 6

## You may write

- goals/G-001-damage-during-dash/06-qa-to-<recipient>.md

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

<<<FILE goals/G-001-damage-during-dash/05-studio-to-qa.md
---
kind: handoff
goal: G-001
seq: 5
from: studio
to: qa
stage: Verify
outcome: routed
---
# 05: studio → qa — Verify the dash-damage fix against build 0.4 (description is the build)

## Task

Verify the change for G-001 against acceptance criteria 1–6 from the defect report (`02-qa-to-gameplay-engineer.md`), using `sim/build-0.4.md` as the build under test, and issue a `pass` or `fail` verdict per criterion and overall.

## Context

Goal G-001: the player sometimes took damage partway through a dash, especially a dash started shortly after taking a hit. QA reproduced it (02) and a fix has been built (build 0.4). Your earlier attempt (04) returned a blocker because the build is only a description and not runnable. The Studio has resolved this: this is a dry-run sample project with no repository, and `project.md` states that builds are simulated under `sim/` and that "running the build" means reading the `sim/build-*.md` file, which is the project's player-visible artifact. So `sim/build-0.4.md` is the build. You are not asked to run code.

## Findings

Ruling on your 04 questions:

1. **Exercisable build:** `sim/build-0.4.md` is the build under test. No other build exists or is expected. Treat its player-observable statements as the observed behavior of the build, and check them against each criterion.
2. **Description-only check:** accepted for this project, because it is the project's defined way of running the build. This does not relax independence: judge from the criteria, `design/combat.md` and the build text, not from any explanation of why the fix should work. If the build text is silent or vague on a case a criterion needs (for example a specific delay, enemy type or frame rate), mark that criterion not verifiable from the build and say exactly what is missing, instead of assuming a pass.
3. **Criterion 6 tolerance (one-frame difference at an expiry boundary):** not decided here. Verify first. If the build text shows a difference between 30 and 60 FPS only in the single frame at an expiry boundary, record it as an observation with the exact wording. If you cannot decide criterion 6 from the criteria and `design/combat.md`, hand back with `outcome: question` and state the question precisely; the Studio will route it to `game-designer`. Do not redefine the criteria yourself.

Per-criterion handling reminder (the criteria themselves are in 02 and are unchanged):

- 1: no damage during a dash started right after hit-stun (about 0.3 s), for Grub and Spitter, at both frame rates.
- 2: no damage for dashes started at several delays inside the 0.8 s post-hit window, including the 0.55–0.8 s range.
- 3: regression, dash with no recent hit takes no damage.
- 4: regression, an undashed hit costs 1 heart, 0.3 s hit-stun, invulnerable until 0.8 s.
- 5: regression, dash 4 tiles / 0.25 s, cooldown 0.6 s, attack queued during a dash fires at its end.
- 6: same results at 30 and 60 FPS.

Also re-check the original reproduction (hit, then dash as soon as input returns) against the build text.

## Decisions already made

- D-001 (one attack button plus dash): no new inputs. Flag it if the build text implies any.

## Constraints

- Must play correctly at 30 and 60 FPS.
- No new input buttons beyond attack, dash and pause (D-001).
- Do not modify production code or redefine the acceptance criteria.
- Verify from the spec, the criteria and the build only.

## Open questions

- Criterion 6: is a one-frame difference at an expiry boundary within tolerance? Answer it only if the criteria and `design/combat.md` settle it; otherwise hand back with `question`.

## Expected output

A verification report in Findings with per-criterion status (pass / fail / not verifiable from build, with the exact missing information) at 30 and 60 FPS, plus any regressions. Write it as a Handoff addressed to `studio` (`to: studio`), with `outcome: pass`, `fail` or `question`. For a fail, give the exact delay, frame rate and enemy type, so the Studio can route it to `gameplay-engineer`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md (Constraints; the dry-run note under Current state and `player_visible`), design/combat.md, sim/build-0.4.md, goals/G-001-damage-during-dash/02-qa-to-gameplay-engineer.md (acceptance criteria 1–6)
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-damage-during-dash/04-qa-to-studio.md
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

<<<FILE project.md
---
kind: project
id: lantern-depths
name: Lantern Depths (sample)
repository: none (sample project for dry-runs; builds are simulated under sim/)
owner_language: ja
player_visible: sim/build-*.md
---
# Project: Lantern Depths (sample)

## Vision

A short-session top-down action roguelite: descend through lantern-lit caves, one room at a time.
Pillars:

1. **One-button combat.** Depth comes from positioning, timing and enemy behavior, not from input
   complexity. Attack and dash are the whole kit (D-001).
2. **Short runs.** A full run takes 15–20 minutes.
3. **Readable threats.** Every threat is visible before it can hurt the player.

## Player profile

Action players who want short, intense runs. Comfortable with dodging and spacing; not interested in
memorizing combo lists. Mostly play with a gamepad.

## Current state

Vertical-slice prototype, build 0.3: 5 rooms in one cave biome, 2 enemy types, player kit of attack
and dash. Dry-run only: "running the build" means reading `sim/build-0.3.md`.

## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).

## Art direction

Dark caves lit by the player's lantern; warm light against cold blue-black. Threats use saturated
orange/red so they read against the dark.

## Design index

- `design/combat.md` — player kit, damage and invulnerability rules, enemies.
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

<<<FILE goals/G-001-damage-during-dash/04-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 4
from: qa
to: studio
stage: Verify
outcome: question
---
# 04: qa → studio — Verify blocked: the build cannot be exercised, so no pass/fail verdict on G-001

## Task

Provide something QA can actually exercise (a runnable build, or logs or recordings from one), then re-route Verify. Alternatively, rule that a description-only check is acceptable. QA has not issued `pass` or `fail`, because either verdict would be a guess.

## Context

Goal G-001: the player took damage partway through a dash started shortly after a hit. The defect report (02) set six acceptance criteria, which are unchanged in 03. The Build step has since changed the game, and Verify is the step that follows. The handoff (03) says to report a blocker instead of guessing a verdict if the build cannot be exercised.

## Findings

### Why this is a blocker

- The only build artifact in the packet is `sim/build-0.4.md`. It is a player-observable description, not a runnable build, and has no logs, recordings or test output.
- Its last bullet says: "The fix has not been run or tested in this simulation; the description follows the change as specified." The text therefore restates the intended behavior and is not an observation of it.
- Passing on that basis would amount to relying on the implementer's account of why the fix works. `studio/roles/qa.md` (Independence) and `studio/skills/verify-change.md` (Do not) forbid this.
- Several criteria need observation that a description cannot give:
  - Criterion 1 needs at least 20 repetitions per frame rate, against both a Grub contact and a Spitter projectile.
  - Criterion 2 needs dashes at several delays after the hit, with extra repetitions between about 0.55 s and 0.8 s, at both frame rates.
  - Criterion 6 needs actual 30 vs. 60 FPS runs.
- The known intermittent defect and the boundary-timing risk (a dash within about one frame of the 0.8 s expiry) are exactly the cases a written description cannot establish.

### Per-criterion status

None of the six was observed, so none is marked pass or fail. The third column shows what the description claims, for the record only. It is not evidence.

| # | Criterion | Status | What `sim/build-0.4.md` claims (not evidence) |
|---|---|---|---|
| 1 | No damage during a dash started right after hit-stun (~0.3 s), ≥20 reps per FPS, Grub and Spitter | Not verified (30 FPS: none, 60 FPS: none) | No damage from dash start to dash end, for both enemy types |
| 2 | No damage for dashes at several delays in the 0.8 s window | Not verified (30 FPS: none, 60 FPS: none) | Dash started at 0.6–0.75 s stays protected through the whole dash; early dashes (~0.3 s, ~0.5 s) keep protection to 0.8 s |
| 3 | No-recent-hit dash: no damage (regression) | Not verified (30 FPS: none, 60 FPS: none) | Unchanged |
| 4 | Undashed hit: 1 heart, 0.3 s hit-stun, invulnerable until 0.8 s (regression) | Not verified (30 FPS: none, 60 FPS: none) | Unchanged |
| 5 | Dash 4 tiles / 0.25 s, cooldown 0.6 s, attack queued during a dash fires at its end | Not verified (30 FPS: none, 60 FPS: none) | Unchanged |
| 6 | Same results at 30 and 60 FPS | Not verified | Same, except frame-sized edge differences |

The original reproduction steps from 02 (hit, then dash as soon as input returns) were not re-run, because there was nothing to run.

### Observations from reading the description

These are not verdicts.

- The description says protection ends on the first frame at or after its end time. That can be up to about 33 ms late at 30 FPS and about 17 ms late at 60 FPS. A contact within one frame of an end time "can go either way depending on frame rate".
- Criterion 6 says results must be the same at 30 and 60 FPS. A strict reading could conflict with this edge behavior, even though the described difference is only frame quantization. Once the build is exercisable, QA needs a ruling on the tolerance: is a difference of one frame at an expiry boundary acceptable? If the intended behavior is not defined, the Studio should route that to `game-designer`.
- The description is consistent with the design in `design/combat.md` (full dash invulnerability, 0.3 s hit-stun, invulnerability until 0.8 s after the hit). This is only a consistency check, not a pass.

## Decisions already made

- D-001 (one attack button plus dash): no input was added, and nothing in the description suggests otherwise.

## Constraints

- Must play correctly at 30 and 60 FPS.
- No new input buttons beyond attack, dash and pause (D-001).
- QA must not modify the production code under verification, and must not redefine the acceptance criteria.

## Open questions

1. Can the Studio supply a build QA can run, or recorded output from one? It needs to cover the six criteria at 30 and 60 FPS, including the 0.55–0.8 s dash delays and the one-frame edge at the 0.8 s expiry.
2. If no runnable build exists, will the Studio explicitly accept a description-only check? QA does not recommend this, because the description says the fix was never run.
3. For criterion 6, is a one-frame difference at an expiry boundary within tolerance? If the spec is silent, route to `game-designer`.

## Expected output

The Studio resolves the blocker and re-routes Verify to `qa` with an exercisable build. QA then issues a `pass` or `fail` verdict against criteria 1–6 at 30 and 60 FPS. A failure goes to `gameplay-engineer` with the exact delay, frame rate and enemy type. No failure has been recorded, so the "same criterion fails a second time" escalation is not triggered.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md#constraints, design/combat.md, sim/build-0.4.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-damage-during-dash/03-gameplay-engineer-to-qa.md
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
