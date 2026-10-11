# Studio operation packet

operation: Step
goal: G-001
role: game-designer
incoming_handoff: goals/G-001-combat-monotony/07-game-director-to-game-designer.md
next_seq: 11

## You may write

- goals/G-001-combat-monotony/11-game-designer-to-<recipient>.md
- design/<name>
- decisions/D-003-<name>.md

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

<<<FILE goals/G-001-combat-monotony/07-game-director-to-game-designer.md
---
kind: handoff
goal: G-001
seq: 7
from: game-director
to: game-designer
stage: Design
outcome: done
---
# 07: game-director → game-designer — Write the design spec for G-001 per D-002 (escalation first, then enemy behaviors)

## Task

Write the design spec (skill `write-design-spec`) for the direction chosen in D-002. Phase 1 is encounter escalation within the existing 5 rooms. Phase 2 is 1–2 telegraphed enemy behavior variants. Include player-observable acceptance criteria.

## Context

Goal G-001: the Owner said 「戦闘が単調なので改善したい」. Your diagnosis (handoff 04) found that enemy behavior gives no reason to move (C1) and that encounters do not escalate (C3). The Playtester's walkthrough found that "hold position and swipe" wins every room. I chose B then A, with C in reserve, and recorded it as D-002. This handoff carries the scope and limits so you can write the spec.

## Findings

### Direction chosen (D-002)

- **Phase 1, Option B.** Using existing Grubs and Spitters, escalate across rooms 1–5 in count, Grub/Spitter mix, spawn positions and Spitter placement. Use multi-side spawns and staggered waves so a corner is not a complete answer in later rooms. One or two room-layout variants that make corners less safe are optional. Room 1 should stay approachable, and the ramp should read as a clear arc.
- **Phase 2, Option A.** In scope. Add 1–2 behavior variants on the existing enemies, for example a Grub with a telegraphed wind-up and lunge (so the dash is the answer) and/or a Spitter that repositions or fires a spread or faster shot. Specify the behaviors, but mark them **pending feasibility (`technical-director`) and telegraph visual direction (`art-director`)**.
- **Option C is not adopted.** Do not add attack/dash reward rules or passivity penalties in this spec. Do not add hit-stun or invulnerability retuning either. Note it only as a possible follow-up if passivity persists after Phases 1 and 2.

### Scope decisions answered from your open questions

- Adding new enemy behavior (A) is in scope for G-001, as Phase 2.
- `art-director` should be involved for telegraph visuals, and `technical-director` for feasibility, before Phase 2 is built. The Studio will route these after your spec exists (see Open questions). Do not wait for them to write the Phase 1 spec.
- B stays inside the 5-room, 15–20 min structure. Do not add rooms or lengthen the run. Real-time run length is unmeasured, so the spec should ask the next playtest to record it.

### Acceptance criteria (player-observable)

Use these as a base and make them testable in the spec:

1. A player cannot clear a later room (e.g. rooms 4–5) by holding one position and attacking.
2. The dash is used in combat in a typical room. This is expected to be fully met only after Phase 2.
3. Later rooms feel different from room 1 in composition, spawn directions or structure.
4. Every threat is visible before it can hurt.
5. Behavior and timing are identical at 30 and 60 FPS.
6. Run length stays within 15–20 minutes. It needs a real-time measurement, which a described walkthrough cannot give.

Mark which criteria belong to Phase 1 and which only to Phase 2.

## Decisions already made

- D-001: Combat uses one attack button plus dash. No new input buttons without Owner approval.
- D-002: Pursue B (encounter escalation, existing enemies) first, then A (telegraphed behavior variants, gated on technical and art review). C in reserve. 5 rooms and the 15–20 min run stay.

## Constraints

- No new input and no pillar change. If the spec would need either, hand it back to me for an Owner escalation.
- All timing must be frame-rate independent (30 and 60 FPS).
- Reuse existing systems (small team). Prefer data and tuning for Phase 1.
- The mid-dash damage oddity is now a confirmed build defect against the existing spec (handoff 05). The engineer fixed it in a change that restores the specified behavior (handoff 08), and QA is verifying that fix in parallel with your work. Do not change the spec for it. If your work shows a spec ambiguity (for example how hit invulnerability interacts with dash invulnerability), amend `design/combat.md` as a spec clarification and say so in your handoff.
- Choose exact numbers (counts, speeds, telegraph durations) in the spec. They are your call. Flag any you cannot justify from the evidence as needing playtest tuning.

## Open questions

- Request to the Studio: route `technical-director` (feasibility and cost of the Phase 2 behaviors for a small team) and `art-director` (telegraph visuals meeting pillar 3) once your Phase 2 behavior proposal is written. Their input gates the Phase 2 build, not the Phase 1 build.
- Can the Phase 1 ramp make corners unsafe enough without layout changes, or are one or two layout variants needed? Decide in the spec.
- Does any Phase 1 composition rely on behavior the current Grub/Spitter cannot show (for example, simultaneous multi-side arrival at the current Grub speed)? Flag it if so.
- Carried over from QA and the engineer (non-blocking, unspecified in `design/combat.md`): should a dash pressed during hit-stun be ignored or buffered? Decide it in the spec or state that it stays as is.

## Expected output

A design spec for G-001 (written via `write-design-spec`) that:
- covers Phase 1 in full and Phase 2 as proposed behaviors pending review;
- includes the player-observable acceptance criteria above, mapped to phases;
- states what is out of scope (new input, extra rooms, Option C rules).

Address your outgoing Handoff to `studio`, so it can send Phase 1 to Build and the Phase 2 proposals to `technical-director` and `art-director`. Playtest follows each phase and should record real-time run length.

## Sender assessment

Confidence is high that B-then-A is the right order. It fits the evidence, the vision and the small team, and it keeps Phase 2 cost visible before it is committed. The main uncertainties are tuning and Phase 2 feasibility, which a described walkthrough cannot settle, so the decision leaves both to later review and playtest. No escalation trigger applies.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md#vision; project.md#player-profile; project.md#constraints; design/combat.md
- Decisions: decisions/D-001-one-button-combat.md; decisions/D-002-combat-variety-direction.md
- Previous handoff: goals/G-001-combat-monotony/04-game-designer-to-game-director.md
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

<<<FILE project.md#vision
## Vision

A short-session top-down action roguelite: descend through lantern-lit caves, one room at a time.
Pillars:

1. **One-button combat.** Depth comes from positioning, timing and enemy behavior, not from input
   complexity. Attack and dash are the whole kit (D-001).
2. **Short runs.** A full run takes 15–20 minutes.
3. **Readable threats.** Every threat is visible before it can hurt the player.
>>>END

<<<FILE project.md#player-profile
## Player profile

Action players who want short, intense runs. Comfortable with dodging and spacing; not interested in
memorizing combo lists. Mostly play with a gamepad.
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

<<<FILE decisions/D-002-combat-variety-direction.md
---
kind: decision
id: D-002
status: accepted
decided_by: game-director
goal: G-001
date: 2026-10-11
supersedes: none
---
# D-002: Fix combat monotony with encounter escalation first, then enemy behaviors that demand movement and the dash

## Decision

G-001 pursues **Option B, then Option A**, in two phases. Option C is held in reserve.

**Phase 1 (Option B: encounter design and escalation, existing enemies).**
- Escalate across the existing 5 rooms in enemy count, Grub/Spitter mix, spawn positions and Spitter placement.
- Use multi-side spawns and staggered waves so that a single corner or stance is not safe in later rooms.
- Optionally add one or two room-layout variants that make corners less safe.
- Stay inside the 5-room structure. Do not add rooms or lengthen the run.

**Phase 2 (Option A: new behaviors on the existing enemies).** In scope for G-001.
- Add 1–2 behavior variants built on the Grub and Spitter. Examples are a Grub with a telegraphed wind-up and lunge, which gives the dash a purpose, and a Spitter that repositions or fires a spread or faster shot.
- Every new behavior must show a clear telegraph before it can hurt (pillar 3).
- Phase 2 goes to build only after `technical-director` has assessed feasibility for the small team and `art-director` has given the telegraph visual direction. The Designer may specify Phase 2 behaviors, but they are marked "pending feasibility and telegraph review".

**Option C is not adopted now.** Reconsider a minimal form only if a playtest after Phases 1 and 2 still shows passivity. It must be one rule a player understands on sight and must not add combo vocabulary.

**Limits of this decision**
- No new input. D-001 is untouched. No pillar changes.
- The 5-room structure and the 15–20 min run target stay. Real-time run length has not been measured. The spec must not add content that lengthens the run, and the next playtest should record run time.
- This does not decide the mid-dash damage behavior. It is with `qa` (handoff 03). If it is a build defect, the Designer does not change the spec. If it is a spec gap, the Designer amends the spec.
- Exact numbers (counts, speeds, timings) are the Designer's to set in the spec. All timing must be frame-rate independent (correct at 30 and 60 FPS).

## Rationale

- Causes C1 (enemy behavior gives no reason to move) and C3 (no escalation or variety across rooms) explain all five symptoms. B addresses C3 and S4 cheaply with data and tuning on existing systems. A addresses C1 and C2, which is why one stance wins and why the dash has no purpose.
- Neither alone is enough. B alone risks "more of the same" with simple enemies, and A alone leaves rooms identical in structure.
- B first gives a quick, low-cost improvement and shows how much of the problem remains before the costlier A work. A is the answer to the root problem and fits the vision: depth through positioning, timing and enemy behavior.
- C risks drifting toward combo-style vocabulary, which the player profile dislikes, and has little to act on without A or B.
- No escalation trigger fires: no new button, no pillar change, no change to an Owner Decision, and the Goal's meaning is unchanged.

## Alternatives considered

- **A first, or A only:** higher cost and art/tech dependency up front, and rooms would stay structurally identical. Rejected as the starting point.
- **B only:** cheap, but does not fix the dash's lack of purpose (S3) or shallow enemies (S5).
- **C as a primary fix:** a supplement that depends on A or B and carries the combo-vocabulary risk. Deferred.
- **Extend run length or add rooms to get escalation:** conflicts with the short-runs pillar and is unmeasured. Rejected.

## Revisit when

- Playtests after Phase 1 show that the one-stance problem is already solved. Phase 2 could then shrink.
- `technical-director` finds the Phase 2 behaviors do not fit the small team. Rescope them.
- A measured run exceeds 20 minutes, or escalation cannot fit within 5 rooms.
- Passivity persists after both phases (reconsider C).
- Playtests show the depth ceiling cannot be reached without new input (D-001 "revisit" condition, an Owner matter).
>>>END

<<<FILE goals/G-001-combat-monotony/04-game-designer-to-game-director.md
---
kind: handoff
goal: G-001
seq: 4
from: game-designer
to: game-director
stage: Decide
outcome: done
---
# 04: game-designer → game-director — Choose the direction for fixing combat monotony (G-001)

## Task

Choose which direction to pursue for G-001 from the options below (or a combination), and settle scope and priority. The diagnosis is done. The options differ in scope and cost, so the choice is yours, not the Designer's.

## Context

Owner's report (verbatim): 「戦闘が単調なので改善したい」. The success condition is that a player from the profile (action player, short intense runs, dodging and spacing, no combo memorization, gamepad) finds combat varied and engaging. It also has to stay inside D-001 (attack + dash only), keep threats readable, and play correctly at 30 and 60 FPS.

The Playtester's walkthrough of build 0.3 (handoff 02) found one approach, hold position and swipe, wins every room. The dash-damage oddity is with `qa` (handoff 03). I did not wait for it. Its result does not change the diagnosis below.

## Findings

### Symptoms (evidence from playtest 02)

- **S1. One strategy wins everywhere.** "I figured out the answer in room 1 and it never stopped being the answer."
- **S2. Standing still is safe.** Damage came only when three Grubs arrived together. Spitters needed one sidestep.
- **S3. Dash is pointless in combat.** It was used only for travel: "Why do I have a dash?"
- **S4. No progression within a run.** Minute 2 felt like minute 15.
- **S5. Enemy variety is shallow.** Mixing Grubs and Spitters did not change player behavior.

### Causes (design terms, checked against design/combat.md)

- **C1. Enemy behavior gives no reason to move (explains S1, S2, S3, S5).**
  - Grubs walk straight at the player, with no telegraph and no special behavior. They arrive from one direction at a steady pace, and the player kills them in 2 swipes (2 HP, 1 damage per swipe) before contact. A corner with the attack aimed at the approach lane is a complete answer.
  - Spitters are stationary and fire a slow projectile every 2 s, so one sidestep beats them. Neither enemy creates area denial, flanking or timing pressure.
  - Both enemies are answered by the same stance, so combining them adds nothing.
- **C2. The dash has no problem to solve (S3).**
  - It has a strong spec (full-duration invulnerability, 0.6 s cooldown). But no threat requires a fast, timed escape. The Grubs' contact bite has no wind-up to dodge through, and slow projectiles are sidestepped.
  - This is a missing demand, not a weak tool. The spec says the dash is invulnerable throughout, so the damage the Playtester saw mid-dash contradicts the spec. That is either a build defect (QA) or a spec gap I would amend. It does not explain "pointless".
- **C3. Encounters do not escalate or vary (S1, S4, S5).** Every room is 3–6 enemies of the same two types, with no ramp in count, mix, spawn position or room structure. Nothing in a room differs from room 1 except the count.
- **C4. Hit economy favors standing still (S2).** The player kills before contact, and a hit costs 1 heart but brings 0.8 s of invulnerability. Little is lost by playing passively, and nothing is gained by playing aggressively or with good spacing.

C1 and C3 together explain most of the evidence.

### Options

All three stay within D-001 (no new input) and fit the pillars unless noted.

**Option A: Make enemy behaviors demand movement and the dash (targets C1, C2; S1, S2, S3, S5).**
- What changes:
  - Add 1–2 behavior variants built on the existing Grub and Spitter, for example:
    - a Grub that winds up and lunges, with a readable telegraph, so the dash is the answer;
    - a Spitter that repositions or fires a spread or a faster shot.
  - Optionally add a Grub spawn path that flanks.
- Cost: medium. New enemy behaviors and tuning, and small telegraph visuals.
- Risk: the readable-threats pillar requires clear telegraphs, so `art-director` should be involved. Unfair-feeling damage is also possible.
- Fit: strong. It is depth through enemy behavior and positioning, which is exactly what D-001 and the vision rely on.

**Option B: Encounter design and in-run escalation, using existing enemies (targets C3; S1, S4, S5).**
- What changes:
  - Per-room composition and spawn positions, such as enemies from several sides or staggered waves.
  - A ramp across rooms 1–5 in count, mix and Spitter placement, plus a clear difficulty arc.
  - Optionally one or two room-layout variants that make corners less safe.
- Cost: low to medium. It is mostly data and tuning, reusing existing systems.
- Risk: on its own it may not fix S3. If Grubs and Spitters stay this simple, higher counts could merely feel like more of the same.
- Fit: strong. It is cheap, fits the small team, and fits short runs.

**Option C: Reward good positioning and dash use in the core rules (targets C4, C2; S2, S3).**
- What changes:
  - Tune the attack/dash relationship, for example a short damage bonus or a free attack after a dash (the attack-queue-after-dash already exists).
  - Make passivity cost something, such as a Grub's front being resistant to damage so that getting behind it matters.
  - Retune hit-stun and invulnerability so mistakes are punished.
- Cost: low to medium. It is all tuning and rule changes.
- Risk: it can drift toward combo-style vocabulary, which the profile dislikes. Keep it to one rule players grasp on sight. Without Option A or B there is little to apply it to.
- Fit: acceptable, but it is a supplement, not a fix by itself.

### Recommendation

Pursue **B first, then A**, with a minimal form of C only if the playtest after A and B still shows passivity.

- B is cheap and addresses progression (S4). A addresses the core problem that one stance beats everything, and gives the dash a purpose.
- A alone would leave rooms identical in structure. B alone would leave enemies simple.
- This is a recommendation. Scope and priority are yours to settle.

### What touches a pillar, a Decision or scope

- **No option needs a new button, so D-001 is not touched. No Owner escalation is triggered by what is proposed.**
- Pillar 2 (short runs, 15–20 min): if B is implemented by adding rooms or extending run length, that must be checked against the 15–20 min target. I recommend a ramp inside the existing 5 rooms. Run length in real time has not been measured.
- Pillar 3 (readable threats): all new behavior in A must telegraph before it can hurt. Needing `art-director` input for telegraphs is a scope and cost question for you.
- Adding new enemy types or behaviors (A) is a scope and priority decision. I recommend you decide it.

### What the evidence cannot settle

- Real-time run length, and whether anything exists beyond room 5. The design spec lists only 5 rooms.
- Controller feel, animation timing and exact numbers, such as Grub speed relative to the 0.35 s attack recovery. The playtest was a described walkthrough, not live play.
- Whether the mid-dash damage is a defect or a spec gap. QA's result is pending. If QA confirms a build defect, the Designer will not change the spec. If it shows a spec ambiguity, the Designer will amend the spec.
- Whether engineering cost for telegraphed behaviors fits the small team. `technical-director` could assess this if you choose A.

## Decisions already made

- D-001: Combat uses one attack button plus dash. No new input buttons without Owner approval. All options above respect it.

## Constraints

- Stay within D-001 and the pillars: one-button combat, 15–20 minute runs, readable threats.
- Must work at 30 and 60 FPS, so timing mechanics must not depend on frame rate.
- Reuse existing systems where possible (small team).
- If a chosen direction would require a new button or a pillar change, an Owner escalation through you is needed.

## Open questions

- Which option or combination, and in what order? Is adding new enemy behavior (A) in scope for G-001?
- If A is chosen: should `art-director` be involved for telegraph visuals, and `technical-director` for feasibility?
- Are you comfortable with B staying inside the 5-room, 15–20 min structure?

## Expected output

A Decision (`decisions/D-NNN-...md`, skill `make-decision`) with the chosen direction and scope. The Designer then writes the design spec (`write-design-spec`) with player-observable acceptance criteria. Suggested criteria for the spec:

- A player cannot clear a later room by holding one position and attacking.
- The dash is used in combat in a typical room.
- Later rooms feel different from room 1.
- Every threat is visible before it can hurt.
- Behavior is identical at 30 and 60 FPS.

## Sender assessment

Confidence is medium-high that C1 and C3 are the main causes, since they are directly visible in design/combat.md and match all five symptoms. Confidence is lower on exact tuning, because the evidence comes from a described walkthrough. This is not a single obvious fix inside my authority alone, because the options differ in scope, cost and art involvement. That is why I am routing to the Decide stage.

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/make-decision.md
- Project: project.md#vision; project.md#constraints; design/combat.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/02-playtester-to-game-designer.md
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
