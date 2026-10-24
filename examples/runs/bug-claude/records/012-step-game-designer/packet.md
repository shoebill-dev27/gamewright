# Studio operation packet

operation: Step
goal: G-001
role: game-designer
incoming_handoff: goals/G-001-damage-during-dash/07-studio-to-game-designer.md
next_seq: 8

## You may write

- goals/G-001-damage-during-dash/08-game-designer-to-<recipient>.md
- design/<name>
- decisions/D-002-<name>.md

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

<<<FILE goals/G-001-damage-during-dash/07-studio-to-game-designer.md
---
kind: handoff
goal: G-001
seq: 7
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 07: studio → game-designer — Rule on the frame-rate tolerance at protection-expiry boundaries (criterion 6)

## Task

Decide what "same results at 30 and 60 FPS" means for the moment protection ends (the end of a dash, or the 0.8 s post-hit mark), and state it as a player-observable rule with a tolerance QA can verify. Record it in `design/combat.md`, and also as a Decision if it constrains work beyond this Goal.

## Context

Goal G-001 (Owner's report): "ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい。" The player took damage partway through a dash that started shortly after a hit. `design/combat.md` already says the player is invulnerable for the full dash duration. Build 0.4 fixes the defect. QA verified acceptance criteria 1–6 (from `02-qa-to-gameplay-engineer.md`; the criteria are unchanged). Criteria 1–5 pass at 30 and 60 FPS, including the original reproduction. Criterion 6 ("same results at 30 and 60 FPS") could not be decided, because neither the criterion nor the design gives a tolerance for the case below. QA may not redefine the criterion, so the question comes to you.

## Findings

From QA's report (`06-qa-to-studio.md`):

- The build says behavior is the same at both frame rates apart from one edge-timing difference. Exact wording in `sim/build-0.4.md`: "protection ends on the first frame at or after its end time. At 30 FPS that can be up to about 33 ms late, and at 60 FPS up to about 17 ms late. So a contact landing within one frame of an end time can go either way depending on frame rate. This is not visible in normal play."
- Protection ends late, never early, so it cannot cause damage inside the 0.25 s dash. Criteria 1 and 2 are unaffected.
- The affected case is a contact in the single frame just after a protection end time: the dash end, or the 0.8 s post-hit expiry. The result can differ between 30 and 60 FPS.
- `design/combat.md` gives no frame-rate or tolerance rule for this.

## Decisions already made

- D-001: one attack button plus dash. No new inputs. This is not at stake here.

## Constraints

- Must play correctly at both 30 and 60 FPS (`project.md#constraints`).
- Small team: prefer rules that reuse existing systems.
- Stay within the current dash and damage design (full-duration dash invulnerability, 1 heart per hit, 0.3 s hit-stun, invulnerable until 0.8 s). Changing those rules as a design improvement is out of scope for G-001.
- The vision pillar "Readable threats" and the player-facing intent in `design/combat.md` still apply.

## Open questions

1. Is a one-frame difference at a protection-expiry boundary acceptable under "same results at 30 and 60 FPS"? If yes, state the tolerance in player-observable terms (for example, which direction it may differ and by how much) so QA can verify it against the build. If no, state the intended behavior (for example, whether expiry must be time-exact and independent of frame rate) so the engineer can build to it.
2. Does the answer apply to both expiry boundaries (the dash end and the 0.8 s post-hit mark) and both enemy types, or does it differ?
3. If your answer would change the dash or damage rules, or touches the vision or scope, say so and hand back for `game-director` rather than deciding it.

## Expected output

- A ruling on criterion 6, written into `design/combat.md` as a short rule with a player-observable acceptance criterion, and a Decision if it constrains later work.
- Your outgoing Handoff addressed to `studio` (not directly to `qa` or `gameplay-engineer`), so the Studio can recompose the next step. The outcome should be `done` with the ruling in Findings, or `question` if you hand back.
- The Studio then routes Verify to `qa` for the final verdict if the difference is accepted, or Build to `gameplay-engineer` if expiry must change.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md, studio/skills/make-decision.md
- Project: project.md#constraints, design/combat.md, sim/build-0.4.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-damage-during-dash/06-qa-to-studio.md
>>>END

<<<FILE studio/roles/game-designer.md
---
kind: role
id: game-designer
writes: design/*, decisions/*
---
# Role: Game Designer

## Responsibility

Turns the intended player experience into rules, systems and parameters, specified precisely enough
that an engineer can build it and QA can verify it without guessing.

## Decides

- Rules, systems, tuning and player-facing behavior within the approved direction.
- Answers to spec questions raised by engineering or QA.
- Player-observable acceptance criteria.

## Must not

- Change direction, priorities or the Goal's scope — that is `game-director`.
- Write production code or choose the technical approach.
- Overrule a QA verdict; change the spec instead, and the change is verified again.

## Works from

- Playtest observations, Director decisions, spec questions from engineering or QA.
- Project vision, constraints, relevant design documents and Decisions.

## Produces

- A diagnosis: causes in design terms and solution options with trade-offs.
- A design spec: rules, parameters, edge cases, acceptance criteria, open questions.
- Answers to spec questions, applied to the design documents, plus Decisions for significant ones.

## Hands back / escalates when

- The diagnosis implies a choice of direction, priority or scope → `game-director`.
- The problem or solution is mainly about what the player sees → involve `art-director`.
- Feasibility or cost is unclear → `technical-director`.
- An Owner escalation trigger fires → `game-director`, who prepares the brief.

## Typical skills

diagnose-experience, write-design-spec, make-decision
>>>END

<<<FILE studio/skills/write-design-spec.md
---
name: write-design-spec
description: Specify player-facing behavior — rules, parameters, edge cases — with player-observable acceptance criteria, precise enough to build and verify without guessing.
---
# Skill: Write design spec

Typical roles: game-designer, art-director (for what the player sees).

## When to use

Intended behavior is not specified well enough for an engineer to build and QA to verify.

## Inputs

The approved direction (Decision), the problem it answers, current design documents, constraints.

## Method

1. State the experience intent in one or two sentences.
2. Specify behavior as rules and numbers, not adjectives. Give every parameter a value and unit.
3. Walk the edge cases: interruptions, simultaneous events, state changes mid-action, every
   supported platform condition. Each case either gets a rule or is listed as an open question.
4. Write acceptance criteria two ways: verifiable checks for QA, and experience signals for the
   playtest and Review (kept away from the Playtester's handoff).
5. Update the project's design documents; record significant choices as Decisions.

## Output

Design spec: intent, rules and parameters, edge cases, acceptance criteria (verification and
experience), open questions, changed design documents.

## Do not

Leave "feels good" as a criterion. Do not specify the code structure.
>>>END

<<<FILE studio/skills/make-decision.md
---
name: make-decision
description: Choose between options within one's own authority, check for escalation triggers, and record significant choices as Decisions.
---
# Skill: Make decision

Typical roles: game-director, game-designer, technical-director, art-director.

## When to use

A choice is needed and it falls within your Role's "Decides" section.

## Inputs

The options with evidence and trade-offs, the vision, constraints and existing Decisions.

## Method

1. Confirm the choice is yours. Check the escalation triggers in `studio/orchestration.md`; if one
   fires, use `prepare-owner-escalation` instead.
2. Judge on evidence and fit with the vision — not on how many opinions favor an option.
3. Decide. State the limits of the decision (what it does not cover).
4. Record a Decision (`studio/templates/decision.md`) if it constrains future work, a real
   alternative was rejected, or it changes a design document. Otherwise note it in the Handoff.

## Output

The decision in the outgoing Handoff, and a Decision file when warranted.

## Do not

Defer a decision you own to the Owner. Do not decide by vote.
>>>END

<<<FILE project.md#constraints
## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).
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

<<<FILE studio/templates/decision.md
---
kind: decision
id: D-NNN
status: accepted        # proposed | accepted | superseded
decided_by: <role-id | owner>
goal: <G-NNN, or none>
date: YYYY-MM-DD
supersedes: <D-NNN, or none>
---
# D-NNN: <the decision in a few words>

## Decision

<What was decided, and its limits.>

## Rationale

<Why.>

## Alternatives considered

<Other options and why they were not chosen.>

## Revisit when

<What change in evidence or circumstances should reopen this.>
>>>END
