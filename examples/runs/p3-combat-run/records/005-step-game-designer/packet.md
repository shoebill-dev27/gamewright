# Studio operation packet

operation: Step
goal: G-001
role: game-designer
incoming_handoff: goals/G-001-combat-monotony/02-playtester-to-game-designer.md
next_seq: 4

## You may write

- goals/G-001-combat-monotony/04-game-designer-to-<recipient>.md
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

<<<FILE goals/G-001-combat-monotony/02-playtester-to-game-designer.md
---
kind: handoff
goal: G-001
seq: 2
from: playtester
to: game-designer
stage: Diagnose
outcome: done
---
# 02: playtester → game-designer — Playtest report on combat in the current build

## Task

Diagnose why combat in the current build is experienced as monotonous, using the playtest report and the Owner's original report below. Give causes and solution options in design terms, staying within D-001 and the vision pillars. This is a player-side observation report only; it contains no causes or fixes.

## Context

Goal G-001: the Owner said (verbatim): 「戦闘が単調なので改善したい」 ("Combat is monotonous and I want to improve it"). The success condition is that a player from the project's player profile finds combat varied and engaging rather than repetitive, without new input buttons (D-001), while keeping threats readable and playing correctly at 30 and 60 FPS.

The first playtest of the current prototype (build 0.3), focused on combat, is below. The Playtester did not see the Owner's wording.

The dash-damage behavior the Playtester saw is being checked separately by `qa` (handoff 03, running in parallel). It is not part of your Diagnose scope except where it affects your reading of "dash feels pointless". If QA's result arrives before you finish, the Studio will pass it on. Do not wait for it.

## Findings

### Method

There is no executable. I "played" by reading `sim/build-0.3.md` and following the player-observable description as a player from the profile would (action player, short intense runs, comfortable with dodging and spacing, dislikes combo memorization, gamepad). This is a described walkthrough, not live play, so I could not observe things like feel of controls, timing, animation, audio, or exact damage numbers. I only played the content the description covers (rooms 1–5 and the run as a whole).

### Session summary

I went through rooms 1–5 using the same approach almost every time: stand my ground, press attack, step aside for projectiles. It worked each time with little risk. By the later rooms I was repeating what I did in room 1.

### Moments in sequence

1. **Rooms 1–2 (Grubs).** Grubs crawl toward me. I stood still and pressed attack. Two swipes killed each one before it reached me. I only took damage when three arrived together. Felt: easy, no tension. I did not need to move.
2. **Room 3 (Spitters).** Their projectile is slow, and one step sideways avoided it. I walked up and swiped each twice. Felt: a small new action (the sidestep), but it was trivial. Not a real threat.
3. **Rooms 4–5 (mixed).** I backed into a corner, faced the Grubs, swiped, and stepped aside from projectiles. The same pattern worked again. Felt: nothing new. My attention dropped here.
4. **Dash.** I rarely needed it. I used it mostly to cross the room faster, not to fight. Felt: as if I had a tool I was never asked to use. For a player who likes dodging and spacing, this was a letdown.
5. **Whole run.** Every room ended the same way: hold position, swipe until empty. Minute 2 felt the same as minute 15. I wanted escalation, and none came.

### Issues and impact

- **Combat is the same in every room (high impact).** One approach (hold position, swipe) wins everywhere. Player quote: "I figured out the answer in room 1 and it never stopped being the answer."
- **Little pressure to move or dodge (high impact).** Standing in a corner is safe. Damage only came when three Grubs arrived at once. Spitters needed one step. As a player who wants intense runs, I did not feel intensity.
- **Dash feels pointless in combat (medium–high impact).** I only used it for travel. Player quote: "Why do I have a dash?"
- **No sense of progression within a run (medium–high impact).** Later rooms did not feel harder or different.
- **Enemy variety feels shallow (medium).** Spitters and Grubs mixed together did not change what I did.

### Positives

- Attacks are quick to kill: two swipes per enemy. This is clear and readable.
- Spitter projectiles are easy to read.
- Nothing felt unfair or confusing.

### Behavior that looks plainly broken

- **Dash after being hit:** occasionally, if I dash right after taking a hit, I take damage partway through the dash. As a player it looked like the dash did not protect me, or damage landed late. It was rare, and I could not tell what triggered it. This may be a defect. I am reporting only what I saw. (Routed to `qa` by the Studio, handoff 03.)
- No crashes or stuck states observed.

### Not observed

- Controller feel, hit feedback, sound, visuals, and enemy types beyond Grubs and Spitters.
- Anything past room 5, and the overall length of a run in real time.
- How the damage-during-dash case is triggered.

## Decisions already made

- D-001: Combat uses one attack button plus dash. No new input buttons without Owner approval.

## Constraints

- This report covers only what a player could see and feel. It makes no claims about causes in code or design.
- I have no authority over design decisions.
- Solutions must stay inside D-001 and the pillars: one-button combat, short runs (15–20 minutes), readable threats. They must work at 30 and 60 FPS, and should reuse existing systems where possible (small team).
- If the only viable options need a new button or change a pillar, say so plainly. That triggers an Owner escalation through `game-director`.

## Open questions

- Is the dash meant to protect the player? As a player I expected it to, and it sometimes did not. (Check against `design/combat.md`; QA is checking the build.)
- Are there rooms beyond 5 that change the pattern? I could not tell.

## Expected output

A diagnosis with causes and solution options in design terms (skill `diagnose-experience`). Put it in Findings of your outgoing Handoff. Recommend which options to pursue, and name any option that touches D-001 or a pillar.

Send the outgoing Handoff to `game-director` for the Decide stage if the diagnosis offers a real choice of direction, priority or scope. If the diagnosis shows a single obvious fix inside your own authority (rules, tuning, enemy behavior), say so. The Studio will then route to Design instead.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/diagnose-experience.md
- Project: project.md#vision; project.md#player-profile; project.md#constraints; design/combat.md; sim/build-0.3.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/01-studio-to-playtester.md
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

<<<FILE studio/skills/diagnose-experience.md
---
name: diagnose-experience
description: Turn experience observations into likely causes and solution options in design terms, with trade-offs, without choosing a direction that is not yours.
---
# Skill: Diagnose experience

Typical roles: game-designer, game-director.

## When to use

Observations show an experience problem whose cause is not understood.

## Inputs

Observation reports, the project vision and player profile, relevant design documents, Decisions.

## Method

1. Cluster observations into symptoms. Keep the evidence attached to each.
2. For each symptom, name candidate causes in design terms (rules, systems, parameters, feedback,
   pacing, readability). Prefer causes that explain several symptoms.
3. Generate 2–3 genuinely different solution options. For each: what it changes, which symptoms it
   addresses, cost, risk, and fit with the vision and Decisions.
4. Mark any option that would change a pillar, a Decision, scope or risk significantly — those are
   not yours to choose.
5. State what the evidence cannot settle.

## Output

Diagnosis: symptoms with evidence, causes, options with trade-offs and vision fit, unknowns, and
your recommendation if one is defensible.

## Do not

Pick a direction outside your authority. Do not present a single option as if it were the only one.
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

<<<FILE goals/G-001-combat-monotony/01-studio-to-playtester.md
---
kind: handoff
goal: G-001
seq: 1
from: studio
to: playtester
stage: Observe
outcome: routed
---
# 01: studio → playtester — Play the current build, focusing on combat, and report your experience

## Task

Play the current build as a player from the profile below, paying attention to combat. Report what you observe and experience, using only what a player can see and feel.

## Context

This is a first playtest of the current prototype build. No implementation history or expected result is provided, on purpose.

How to run the build: this is a dry-run project with no real executable. "Running the build" means reading `sim/build-0.3.md` and playing through it as described there.

Player profile (from the Project Context): action players who want short, intense runs. They are comfortable with dodging and spacing, and are not interested in memorizing combo lists. They mostly play with a gamepad.

Play focus: combat.

## Findings

None (this is the first step).

## Decisions already made

None.

## Constraints

- Report observable experience only: what you saw, did and felt, and when. Do not guess at causes in the code or design.
- Use only the build and the player profile. Do not open design documents, repository notes or Decisions.
- You have no authority over the game's design. Report accuracy matters; fixes are not asked for.

## Open questions

None.

## Expected output

An observation report following the `playtest-session` skill: what was played, the observed combat experience in sequence, moments that stood out (good or bad), and any behavior that looks plainly broken (crash, stuck state), listed separately. Address the report to `game-designer`, who runs Diagnose next. The Studio will add the Owner's original report for the Designer when routing.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: sim/build-0.3.md; project.md#player-profile
- Decisions: none
- Previous handoff: none
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
