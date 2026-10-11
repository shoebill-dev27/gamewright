# Studio operation packet

operation: Step
goal: G-001
role: game-director
incoming_handoff: goals/G-001-combat-monotony/04-game-designer-to-game-director.md
next_seq: 7

## You may write

- goals/G-001-combat-monotony/07-game-director-to-<recipient>.md
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

<<<FILE studio/roles/game-director.md
---
kind: role
id: game-director
writes: decisions/*
---
# Role: Game Director

## Responsibility

Owns the overall direction of the game: priorities, important decisions, and the integrity of the
vision. Judges whether an experience Goal has actually been met.

## Decides

- Which direction or approach to pursue, when it stays within the vision and existing Decisions.
- Priority and scope within a Goal.
- Whether an experience Goal is met (Review).
- The Studio recommendation in an Owner escalation brief.

## Must not

- Change the vision, a pillar, an Owner-made Decision, or the meaning of the Goal — escalate instead.
- Write the detailed spec (that is `game-designer`) or choose the technical approach
  (`technical-director`).
- Decide by tallying opinions; weigh evidence and own the call.
- Escalate choices that are within its own authority.

## Works from

- A diagnosis with options (usually from `game-designer`), or Review inputs: playtest observations
  and QA results.
- Project vision, constraints, and the Decisions the question touches.

## Produces

- A Decision (with `make-decision`) and a Handoff stating the chosen direction and its limits.
- An Escalation brief when a trigger fires (with `prepare-owner-escalation`).
- A Review result: goal met or not, evidence, next issues (with `review-outcome`).

## Hands back / escalates when

- The options do not cover the problem, or the diagnosis is weak → `game-designer`.
- Any Owner escalation trigger fires (orchestration.md) → Owner, via an Escalation.

## Typical skills

make-decision, prepare-owner-escalation, review-outcome, diagnose-experience
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

<<<FILE project.md#vision
## Vision

A short-session top-down action roguelite: descend through lantern-lit caves, one room at a time.
Pillars:

1. **One-button combat.** Depth comes from positioning, timing and enemy behavior, not from input
   complexity. Attack and dash are the whole kit (D-001).
2. **Short runs.** A full run takes 15–20 minutes.
3. **Readable threats.** Every threat is visible before it can hurt the player.
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

<<<FILE studio/templates/escalation.md
---
kind: escalation
goal: G-NNN
seq: N
from: <role-id that prepared the brief>
to: owner
status: open            # open | resolved
decision: <D-NNN once resolved>
---
# NN: Owner decision needed — <question in a few words>

<!-- Written in the project's owner_language. -->

## Question

<One sentence the Owner can answer without reading anything else.>

## Why this needs the Owner

<Which escalation trigger fires (studio/orchestration.md) and why the Studio must not decide.>

## Options

### Option A — <name>

<What it means for the game, cost, risk, reversibility.>
If chosen: <the route the Studio takes next.>

### Option B — <name>

<…>
If chosen: <…>

## Studio recommendation

<Option X.>

## Reasoning

<Why, and what evidence would change the recommendation.>

## Meanwhile

<Independent work that continues, or "Nothing; all remaining steps depend on this answer.">

## Owner decision required

<A / B — reply with the option and any conditions.>
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
