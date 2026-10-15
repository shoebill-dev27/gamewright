# Studio operation packet

operation: Step
goal: G-001
role: game-designer
incoming_handoff: goals/G-001-combat-monotony/09-studio-to-game-designer.md
next_seq: 10
runs: play, bots (up to 3 rounds)
run_play: python3 play.py --view player {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/10-game-designer-to-<recipient>.md
- design/<name>
- decisions/D-003-<name>.md
- @run/<play|bots>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer

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

<<<FILE goals/G-001-combat-monotony/09-studio-to-game-designer.md
---
kind: handoff
goal: G-001
seq: 9
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 09: studio → game-designer — Specify the Option A combat rework and rule on the open spec questions

## Task

Write the design spec for Option A (D-002: rework existing enemy behavior first), with player-observable acceptance criteria. Include your rulings on the spec gaps QA found (listed under Open questions). Use `write-design-spec`.

## Context

G-001: the Owner finds combat monotonous ("戦闘が単調なので改善したい").
- Observe (playtester, rooms 1–3) and Diagnose (you) found the cause: single-state, untelegraphed enemy behavior.
- The Director chose Option A in D-002 and asked for a rooms 4–5 play round before the spec was finalized. That round is now done (08).
- QA (06) found spec gaps, not defects. They are listed below and need your rulings.
- The Director's direction for the spec is in `05-game-director-to-studio.md`; QA's spec questions are in `06-qa-to-game-designer.md`. Read both.

## Findings

Rooms 4–5 playtest (08), as a player saw it. These are observations, not causes. Method: scripted input, player view only.

- **Room 4:** 2 grubs start on the left and walk steadily at the player. The 2 spitters sit in the right-hand corners and never move. Both spitters fire at the same moment every 2 s, as a mirrored pair, with an identical rhythm from first spit to last.
- **Room 5:** 3 grubs and the same 2 spitters, with the same spit pattern. The only felt difference from room 4 was one more grub, arriving from more directions. Idle, the player went down about 1.1 s sooner (5.8 s vs 6.95 s).
- **Projectiles:** The playtester was never hit by one in any run. They were slow and visible, but gave no occasion to react. The spitters read as scenery. Both rooms felt like "kill the grubs and ignore everything else."
- **Grubs:** Visible from the start. Once next to the player they hit about every 0.8 s, and 3 hearts last about 1.6 s. A dash cleared about 3 tiles and bought a few quiet seconds that the game gave the player nothing to do with.
- **Attack feedback:** Text only ("grub hit", "grub defeated"). Nothing changes on the map. Hits-to-kill cannot be read from the screen. Some swipes showed "(nothing happens)" with no stated reason (range, timing or cooldown unclear). One swipe appeared to hit two grubs.
- **After going down:** The room keeps running with no game-over or restart.
- **Odd output:** The spit line appears twice per spit time (one per spitter).
- **Not observed:** A fight in room 5, approaching a spitter, taking a projectile hit, clearing a room, dodging by dash, moving while attacking.
- **Evidence limit:** Everything above comes from short scripted runs. Treat the unobserved items as unknown. `run_trace` and `run_bots` (see `project.md`) are available if you need to check them against the rules.

## Decisions already made

- D-001: Combat uses one attack button plus dash. No new input buttons beyond attack, dash and pause without Owner approval.
- D-002: Respond to combat sameness by reworking existing enemy behavior first (Option A). Option B is deferred. Option C is out of scope for now.

## Constraints

- Vision pillars: one-button combat, short runs (15–20 minutes), readable threats (every threat visible before it can hurt the player).
- Must play correctly at 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- Art direction: threats use saturated orange/red to read against the dark.
- Stay within D-002. If a ruling would need a new input, a change to run length, or a different direction, hand back (`question`) so the Studio can route it to the Director or Owner. Do not decide it.
- Acceptance criteria must be player-observable. Numeric values belong in the spec as parameters and criteria.

## Open questions

Rulings needed from you (from QA's report, 06):
1. **Room mix:** Is "mixed enemy types" required per room, or across rooms? Rooms 1–3 are single-type.
2. **Zero hearts:** What happens at zero hearts (down state, game-over, restart)? The playtester saw the room keep running.
3. **Room cleared:** What rule applies when the room is cleared while the player is down, and in general?
4. **Undocumented elements:** The practice room and the downed marker are not in the design docs. Document them or rule on them.
5. **30 FPS:** Nothing was verified at 30 FPS. Include 30/60 FPS criteria in the spec so Verify can check them.

Also decide, or flag for a later playtest:
6. The attack's "(nothing happens)" cases: is this intended (range, cooldown) and how should it read to the player?
7. The twice-printed spit line: intended or a defect? If a defect, say so in your result so the Studio can route it to `qa`.

## Expected output

- The spec, written into `design/combat.md` or a new design document you name, with parameters and player-observable acceptance criteria. It should cover:
  - the enemy behavior changes that address single-state, untelegraphed behavior (D-002);
  - rulings on questions 1–7.
- Record a Decision if a ruling constrains later work or rejects a real alternative.
- Address the result to `studio` (outcome `done`, or `question` if blocked). The Studio then decides whether Plan is needed and routes to Build.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md#vision, project.md#constraints, project.md#art-direction, design/combat.md, manual.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-response-scope.md
- Previous handoff: goals/G-001-combat-monotony/08-playtester-to-game-designer.md (also read goals/G-001-combat-monotony/05-game-director-to-studio.md and goals/G-001-combat-monotony/06-qa-to-game-designer.md)
>>>END

<<<FILE studio/roles/game-designer.md
---
kind: role
id: game-designer
writes: design/*, decisions/*
runs: play, bots
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

<<<FILE project.md#constraints
## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).
>>>END

<<<FILE project.md#art-direction
## Art direction

Dark caves lit by the player's lantern; warm light against cold blue-black. Threats use saturated
orange/red so they read against the dark.
>>>END

<<<FILE design/combat.md
# Combat design (build 0.4)

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

<<<FILE manual.md
# Lantern Depths — how to play build 0.4

Player-facing manual. A play session is an input script; the play command runs it and shows what a
player sees and hears, with the room drawn every half second and after every hit.

## Controls

- **Move** in four directions; you keep moving until you stop or turn.
- **Attack**: a short swipe in the direction you face.
- **Dash**: a quick burst in a direction (or the way you face).

## Script

One instruction per line; `#` starts a comment.

| Line | Meaning |
|---|---|
| `room 1` … `room 5` | Which room to play (default 1). `room empty` is the practice room. |
| `fps 30` or `fps 60` | Frame rate (default 60). |
| `end 12` | Stop the session at 12 seconds (default: 3 s after the last input; at most 60). |
| `<seconds> move left\|right\|up\|down` | Start moving at that time. |
| `<seconds> stop` | Stop moving. |
| `<seconds> attack` | Swipe. |
| `<seconds> dash [left\|right\|up\|down]` | Dash. |
| `spawn grub\|spitter <x> <y>` | Practice room setup: place an enemy. |
| `player <x> <y>` | Practice room setup: place yourself. |

The room is 16 tiles wide (x 0–15) and 9 tall (y 0–8); you start at x 8, y 4.

## On screen

`P` you, `g` grub, `s` spitter, `*` projectile. Hearts are shown above the room.
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

<<<FILE decisions/D-002-combat-response-scope.md
---
kind: decision
id: D-002
status: accepted
decided_by: game-director
goal: G-001
date: 2026-10-15
supersedes: none
---
# D-002: Respond to combat sameness by reworking existing enemy behavior first (Option A)

## Decision

1. **Option A is approved as the first response for G-001.** The existing Grub and Spitter get legible, varied behavior:
   - a visible wind-up before damage is possible;
   - a recovery pause after attacking;
   - staggered Spitter volleys with a visible charge-up;
   - clear hit feedback on the player's own attacks, including a visible damaged state.
   The game-designer owns the exact timings, knockback and feedback rules.
2. **Option B (mixed rooms, moving spitters, staggered grub arrival) is deferred.** It is not rejected. It is reconsidered only if a playtest of the Option A build still shows sameness. It is in scope for G-001 only after that playtest.
3. **Option C (new enemy types) is out of scope for G-001 for now.** It is reopened only if A and B have been playtested and sameness remains.
4. **Another play round on rooms 4 and 5 runs before the spec is finalized.** The designer may start the spec for A in parallel, but must check it against the round's results before handing it on.

## Limits

- All work stays within D-001: no new inputs beyond attack, dash and pause.
- All new timings are specified in seconds. Acceptance criteria must hold at both 30 and 60 FPS.
- Every damaging action must be preceded by a visible telegraph (pillar 3).
- Prefer reuse of existing enemy, projectile and timer systems (small-team constraint).
- This decision does not cover the possible defects (room composition vs. spec, no game-over/restart state). Those are routed to `qa` separately and may change the spec's wording or add a rule.
- It does not decide whether Spitters get a way to be approached. The designer decides that within A, using the rooms 4 and 5 evidence.

## Rationale

- The diagnosis traces all four symptoms to one root cause: each enemy has a single behavior with no state change, timing variation or readable cue. Option A addresses that root cause directly, covering S1, S2 and S3 and part of S4.
- It supports pillar 1 (depth from positioning, timing and enemy behavior) and pillar 3 (readable threats). It matches the player profile, which favors spacing and dodging.
- It is the cheapest and lowest-risk option, and it reuses existing systems.
- No escalation trigger fires. No pillar, D-001 or Goal meaning changes, and the scope and cost are modest.
- Variety (B, C) layered on flat enemies would add busyness or content cost without fixing the cause.
- The rooms 4 and 5 round is cheap. The current sample is homogeneous and was blind-scripted, so it understates winnability and cannot show whether the dash answers grubs. Specifying timings without that evidence risks mistuning.

## Alternatives considered

- **B first or A+B together:** rejected for now. Without A the fights are only busier, and it adds scope before A's effect is known.
- **C (charger, shielded enemy):** rejected for now. It has the highest cost and scope risk and leaves the existing enemies flat.
- **Spec immediately, no further play round:** rejected. Rooms 4 and 5 are the only place to check the "mixed rooms" claim, and the dash/grub question needs reactive play.

## Revisit when

- The rooms 4 and 5 round shows they already contain the missing variety or different enemy behavior, which would change what Option A needs to cover.
- A playtest of the Option A build still reports monotony (open B, then C).
- A live playtest shows the Option A changes make grubs trivial or the dash insufficient. This is a tuning matter for the designer, unless it touches D-001.
>>>END

<<<FILE goals/G-001-combat-monotony/08-playtester-to-game-designer.md
---
kind: handoff
goal: G-001
seq: 8
from: playtester
to: game-designer
stage: Diagnose
outcome: done
---
# 08: playtester → game-designer — Observation report: rooms 4 and 5

## Task

Read the observations below on rooms 4 and 5 and diagnose the combat experience. Nothing here is a cause or a fix.

## Context

G-001: the Owner finds combat monotonous. This is first-hand play evidence for rooms 4 and 5, taken with the player view only and `manual.md`.

## Findings

### Method

- Input-script automation with `python3 play.py --view player`. I did not play live and did not read source.
- Three runs in total:
  - room 4 idle (8 s)
  - room 5 idle (8 s)
  - room 4 with a short fight script: walk left, stop, four attacks, one dash right (8 s)
- The run budget ended there. **I did not play a fight in room 5** and I **never approached a spitter**. I did not run any further script to test dodging.
- Claims about room 5 come from the idle run only.

### Enemies, counts and behaviour over time

**Room 4**
- 2 grubs start on the left, at about (0,1) and (1,4).
- 2 spitters sit in the right-hand corners, at (15,0) and (15,8).
- The grubs walk steadily toward me, about 1 tile per half second. They reach me at about 5 s when I stand still.
- Spitters did not move at all during 8 s.
- Both spitters spit at the same moment, every 2 s (2.0, 4.0, 6.0, 8.0 s). Each spit is one `*` and the two always come as a mirrored pair.
- The projectiles drift leftward and toward the middle rows, closing on my row. In the idle run they passed above and below me, then bunched around my tile.
- **I was never hit by a projectile in any run.** All damage I saw came from grubs.
- Over time nothing changed except the grubs closing in. The spit rhythm was identical from the first spit to the last.

**Room 5**
- 3 grubs start on the left and bottom-left, at about (1,1), (0,6) and (4,8).
- 2 spitters sit in the right-hand corners, at the same spots as in room 4.
- Spit timing and look are the same as in room 4: a mirrored pair every 2 s.
- Idle, the grubs surrounded me and the first hit came at 4.2 s. I went down at 5.8 s.

### Do the rooms feel different?

- On paper, room 5 is room 4 plus one more grub, arriving from more directions. That is the only difference I could see.
- The spitters, the layout of the right edge and the spit pattern looked identical.
- In the idle runs, room 5 killed me about 1.1 s sooner (5.8 s against 6.95 s).
- I could not tell the two rooms apart by feel. I expect the same loop: grubs close in while the spitters repeat the same pair of shots on the same beat.

### First contact with each enemy type

**Grub**
- Visible from the start, walking at me in the open. There was no damage before I could see it coming.
- My responses are to hit it or dash away.
- In the fight run, the first hit on me came at 1.4 s. I was still walking left into the grubs, so it was my own approach.

**Spitter**
- Visible from the start in a corner. A text line "a spitter spits" appears at the moment of each shot.
- The `*` projectiles are visible and slow, a few tiles per second.
- I never got hit by one, so I cannot say what it feels like to take one or what it does.
- I could see the pattern, but I had no occasion to dodge it.

### How my choices affected the outcome

- Standing still ended in a loss in both rooms: down at 6.95 s in room 4 and at 5.8 s in room 5. I took no action in those runs.
- The grubs hit about every 0.8 s while next to me. Hits came at 5.35, 6.15 and 6.95 s in room 4, so a 3-heart bar lasts about 1.6 s once they are on me.
- In the room 4 fight script:
  - Walking toward the grubs cost me a heart straight away, at 1.4 s.
  - Swipes at 1.5 and 1.6 s showed "(nothing happens)".
  - The swipe at 2.0 s landed: "grub hit".
  - I took another hit at 2.2 s.
  - The swipe at 2.4 s showed "(nothing happens)".
  - The swipe at 2.8 s showed "grub defeated, grub hit".
  - The dash right at 3.2 s carried me about 3 tiles away and got me clear.
  - The remaining grub caught up by about 5.5 s while I stood still after the dash, and took my last heart at 6.4 s.
- Moving while shooting was never tested.
- Most of the fight I did nothing but wait. The dash bought me a few seconds of quiet and I did nothing with them. That was my choice in the script, not something the game asked of me.
- The projectiles gave me nothing to react to in these runs. Both rooms felt like "kill the grubs and ignore everything else."

### What I see when my attack lands

- The only feedback is a line of text: "you swipe: grub hit" or "grub defeated".
- On the room map nothing changes visually when a grub is hit.
- I cannot say from the screen how many hits a grub takes. In the room 4 fight, one grub was hit at 2.0 s and a "grub defeated" came at 2.8 s, so it looks like two swipes for one grub. The 2.8 s swipe also listed a second "grub hit", so that swipe seemed to hit two. I am not sure which grub was which.
- Swipes seem to have a gap: two of my four swipes did nothing. I could not tell whether they missed because of range or timing, or were blocked by a cooldown.
- Spitter hits to defeat: not observed.

### Can I approach a spitter?

- Not tested. They stay in the far corners and I never reached the right side.

### How many hits can I take

- 3 hearts. Each grub hit costs 1 heart.
- No projectile damage was observed.

### After going down

- The text says "you went down" and my `P` becomes `x`.
- The room keeps running. The grubs stay beside me and the spitters keep firing, with no game-over screen and no restart in the output.
- Clearing a room was never reached, so I have no observation of it.

### Confusing or odd

- "(nothing happens)" on attacks at 1.5, 1.6 and 2.4 s, with no stated reason.
- The "a spitter spits" line appears twice at each spit time. This looks like one line per spitter.
- "enemies left" at the end was 4 and 5 in the idle runs (every enemy still alive). It was 3 after the fight run (one grub killed).
- The same mirrored spit pair on the same 2 s beat made the spitters read as scenery. That is how it felt, not a measurement.

## Decisions already made

None.

## Constraints

- Observations are what a player could see in the player view and read in `manual.md`. Not tested: room 5 combat, approaching spitters, being hit by a projectile, clearing a room, and any dash used for dodging.

## Open questions

None.

## Expected output

The game-designer diagnoses from these observations (stage Diagnose).

## Load

- Role: studio/roles/game-designer.md
- Skills: none specified
- Project: project.md#player-profile
- Decisions: none
- Previous handoff: goals/G-001-combat-monotony/07-studio-to-playtester.md
>>>END

<<<FILE goals/G-001-combat-monotony/05-game-director-to-studio.md
---
kind: handoff
goal: G-001
seq: 5
from: game-director
to: studio
stage: Playtest
outcome: done
---
# 05: game-director → studio — Compose a play round on rooms 4 and 5; then the designer writes the spec for Option A

## Task

Compose and route a Playtester Handoff for another play round of build 0.4, covering rooms 4 and 5. After it, route the report to `game-designer` to write the design spec for the approved response (D-002).

Per the designer's handoff, do not pass the diagnosis, the options or D-002's content to the Playtester. Use only information a Playtester may have.

## Context

G-001: combat feels monotonous. The first play round (seq 02) covered rooms 1–3 with blind scripts. The designer diagnosed the cause and offered options (seq 03). The Director chose the scope in D-002. Rooms 4 and 5 and the practice room were not played, so they may already differ from rooms 1–3.

## Findings

### Decision (summary of D-002)

- Option A (rework existing enemy behavior and hit feedback) is approved as the first response.
- Option B (room composition and light movement) is deferred until A has been playtested.
- Option C (new enemy types) is out of scope for G-001 for now.
- A play round on rooms 4 and 5 runs before the spec is finalized.

No Owner escalation: no pillar or D-001 change, and the scope and cost are modest.

### What the play round must cover (the Studio phrases this neutrally for the Playtester)

- Rooms 4 and 5: which enemy types appear, how many, and what they do over time and between rooms.
- Whether rooms 4 and 5 feel different from rooms 1–3, and how.
- The first contact with each enemy type seen: what the player sees before taking damage, and whether the player has a way to respond.
- Reactive play where the tooling allows: short scripts, with the Playtester inspecting the result between runs, instead of one long blind script per room. The aim is to learn whether a player who reacts can avoid or beat the enemies, and what the dash does against them.
- Visible feedback when the player's own attack lands, and how many attacks an enemy takes to defeat.
- Any moment where the player can approach a ranged enemy, if such enemies appear.
- Hit points: how many hits the player can take.
- What happens after the player dies or clears a room (record only what is observed).

### Direction for the designer after the round

- Start the spec for Option A (`write-design-spec`) with the timings and rules in seconds and with player-observable acceptance criteria at 30 and 60 FPS. Before handing it on, check it against the rooms 4 and 5 report.
- If rooms 4 and 5 already show enemy variety or different behavior, adjust A's scope to avoid duplicating it. Report the consequences back to the Director if the finding changes B's or C's relevance.
- If the report shows the dash gives a live player no answer to grubs, include that in A's tuning (spacing, recovery, grub speed) within D-001. Do not add inputs.
- Decide within A whether Spitters can be approached between volleys.
- Take the `qa` Observe result (`04-studio-to-qa.md`) into account when it arrives. It may change the spec's wording on room composition or add a death/restart/room-clear rule.
- Return to the Director only if a trigger fires (pillar or D-001 change), the scope would grow beyond A, or the report contradicts the diagnosis.

## Decisions already made

- D-001: one attack button plus dash; no new combat inputs without Owner approval.
- D-002: Option A first; B deferred; C out of scope for now; rooms 4 and 5 are played before the spec is finalized.

## Constraints

- The Playtester receives only permitted information, with no design-side knowledge (diagnosis, options, spec contents).
- No new input buttons beyond attack, dash and pause (D-001).
- All timings in seconds; acceptance criteria hold at 30 and 60 FPS.
- Pillar 3: every threat is visible before it can hurt the player.
- Small team: prefer reuse of existing systems.

## Open questions

None for the Studio. Open design questions are listed under "Direction for the designer".

## Expected output

1. The Studio writes a Playtester Handoff for rooms 4 and 5 using the coverage list above, stripped of design-side knowledge.
2. After the Playtester's report, the Studio routes to `game-designer` (stage: Specify, `write-design-spec`) with the report and this decision.

## Sender assessment

Confidence is high that A is the right first move, since the cause is in the specified enemy behavior. Confidence on A's effect size is medium until a live, reactive playtest. The main risk is tuning that makes grubs trivial, so the spec needs a playtest after implementation. The play round is a low-cost check, not a blocker for the designer's planning.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md#vision, project.md#player-profile, project.md#constraints, design/combat.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-response-scope.md
- Previous handoff: goals/G-001-combat-monotony/03-game-designer-to-game-director.md
>>>END

<<<FILE goals/G-001-combat-monotony/06-qa-to-game-designer.md
---
kind: handoff
goal: G-001
seq: 6
from: qa
to: game-designer
stage: Observe
outcome: question
---
# 06: qa → game-designer — Room mix and the zero-heart / room-cleared behavior need a spec ruling

## Task

Rule on the two spec questions below. Both come from checking build 0.4 against `design/combat.md`. Neither is a confirmed defect yet: the spec is ambiguous on point 1 and silent on point 2. Once you have defined the intended behavior, route any needed fix through the Studio.

## Context

G-001 (combat monotony). Handoff 04 asked QA to check room composition (rooms 1–5 and the practice room) and the behavior after hearts reach zero and after a room is cleared. Everything was run from `repo/`. Unit tests: `python3 -m unittest discover -s tests` → 9 tests, OK.

## Findings

### Point 1: Room composition

Spec (`design/combat.md#rooms`): "5 rooms, 3–6 enemies each, mixed Grubs and Spitters."

Method: for each room, the script `room N` + `end 1`, run with `python3 play.py --view trace`. The setup row at t=0 lists the enemies.

| Room | Enemies at start | Count (3–6) | Both types in the room |
|---|---|---|---|
| 1 | 3 Grubs, 0 Spitters | OK | No |
| 2 | 4 Grubs, 0 Spitters | OK | No |
| 3 | 3 Spitters, 0 Grubs | OK | No |
| 4 | 2 Grubs, 2 Spitters | OK | Yes |
| 5 | 3 Grubs, 2 Spitters | OK | Yes |
| practice (`room empty`) | 0 enemies | n/a | n/a |

- **Counts:** all five rooms are within 3–6. This matches the spec.
- **Mix:** across rooms 1–5 both types appear, but rooms 1, 2 and 3 each contain a single enemy type.
  - "Mixed" can mean every room has both types, or the set of rooms uses both types. The spec doesn't say which.
  - If it means each room, rooms 1–3 contradict the spec (defect).
  - If it means the set of rooms, the build matches.
  - **Verdict: spec ambiguous.** I did not rule it a defect.
- **Practice room:** it exists and starts empty, as `manual.md` describes. `design/combat.md` doesn't mention it, so the spec is undefined for it. It is not a defect.
- **Not checked:** Spitter projectile behavior in room 3. In the 1 s runs the Spitters stayed stationary, and no projectile appeared in that window.
- **Relevance to G-001:** three of five rooms are single-type. Room 1 is 3 Grubs that walk straight at the player. Room 3 is 3 stationary Spitters. That may contribute to the monotony feeling.

### Point 2a: Hearts reach zero

Scripts:
- A: `room 1` + `end 60`, run with both the trace and player views.
- B: `room 1`, `5.5 move left`, `6.0 attack`, `6.5 dash left`, `7.0 stop`, `end 10`, run with the trace view.

Observed with no player input in room 1:
- Three Grub bites land at 2.833 s, 3.633 s and 4.433 s. Hearts go 3→2→1→0, and each hit is 0.8 s after the last. This matches the spec on hit damage, 0.3 s stun and 0.8 s invulnerability.
- At 4.433 s the player view prints "YOU ARE HIT by a grub — hearts 0/3" and "you went down". The `P` marker becomes `x`.
- After that:
  - There is no game-over screen, no restart prompt and no end of session. The session runs to the `end` time (60 s in script A).
  - Hearts stay at 0 and don't go negative.
  - The Grubs keep moving and crowd around the player, ending at about 0.54 tiles away. No further bites are logged. At 5.233 s the player's invulnerability ends, and hearts stay 0 through t=60.
  - The player view still draws the room every 0.5 s with "hearts 0/3". Its output was cut at 20,000 characters, so I did not see the end of the 60 s run.
- Input while down (script B): the move, attack and dash at 5.5–6.5 s produced no trace rows. The position stayed (8.00, 4.00) from 5.233 s to the end. Inputs have no effect.
  - Unlike the hit-stun case, no "ignored" row is logged for these inputs. In the practice-room run, an attack during stun is logged `ignored {'reason': 'stunned'}`.
  - I did not run the player view of script B, so I don't know what the player is told when they press a button while down.
- Compared with the spec: `design/combat.md` says nothing about zero hearts. There is no defined down state, no game-over or restart, and no rule for input or enemies afterwards. **Verdict: spec undefined, not a defect.**
- Player impact if it stays as is: after going down the player can do nothing, and nothing ends the session. A real game would soft-lock with no feedback. This is a severity concern for the spec to resolve, not a defect rating.
- Manual gap: the `x` marker for a downed player is not listed in `manual.md#on-screen`.

### Point 2b: Room cleared

Script (practice room): `room empty`, `player 8 4`, `spawn grub 10 4`, `0.1 move right`, `0.2 stop`, `1.0 attack`, `1.5 attack`, `2.0 attack`, `2.5 attack`, `3.0 attack`, `3.5 attack`, `end 8`. Run with both views.

Observed:
- The Grub reached the player and bit at 0.85 s (hearts 3→2). The attack at 1.0 s was ignored because of hit-stun, and the player view said "(nothing happens)". This matches the spec.
- The attack at 1.5 s hit the Grub (hp 2→1). A second bite landed at 1.65 s (hearts 2→1), exactly when the 0.8 s invulnerability from the first bite ended. This matches the spec.
- The attack at 2.0 s defeated the Grub. At 2.017 s the player view printed "room cleared" and the trace logged `cleared`.
- After clearing:
  - The session keeps running to the `end` time.
  - There is no transition, no results screen and no next room.
  - Attacks at 2.5, 3.0 and 3.5 s were accepted and logged as misses.
  - Hearts stay at 1, with no healing and no reset.
  - The player view ends with "end at 8.00 s: hearts 1/3, enemies left 0".
- Compared with the spec: "A room ends when all enemies are defeated." The build announces "room cleared", but the spec defines nothing about what happens after (transition, input lock, hearts carrying over). **Verdict: the build matches the spec as written; further behavior is undefined, not a defect.**
- I ran this in the practice room only, because clearing a numbered room needs an actual combat script.

### Not obtained

`python3 bots.py room 1` failed: `script line 1: cannot read 'room 1'`, exit 1. `bots.py` evidently takes a different input than the play-script format. The bots were not needed for these two points, so I did not retry.

## Decisions already made

None.

## Constraints

- QA did not modify the build or the design documents.
- Per the QA role, QA does not decide intended behavior where the spec is silent. These questions are yours.
- Project constraints that matter to any rule you write:
  - It must play correctly at 30 and 60 FPS. All runs here were at 60 FPS only, so nothing is verified at 30 FPS.
  - There is no new input button without Owner approval (D-001). A restart or continue prompt has to work with attack, dash and pause only.

## Open questions

1. Does "mixed Grubs and Spitters" apply to every room, or to the set of rooms? If it applies to every room, rooms 1, 2 and 3 contradict it and need a fix.
2. What should happen when hearts reach zero? Define:
   - game-over or restart;
   - what the player sees;
   - whether enemies keep acting;
   - whether input is accepted.
3. What does "a room ends" mean after "room cleared"? Define:
   - the transition;
   - whether hearts carry over or reset;
   - whether input is accepted afterwards.
4. Should the practice room (`room empty`) and the `x` downed marker be documented in the spec and manual?

## Expected output

A spec ruling from `game-designer` (an update to `design/combat.md`). For each rule that the build then fails to meet, the Studio routes a defect to `gameplay-engineer`. Suggested acceptance criteria for those defects, once the intended behavior is defined:
- **Room mix:** at start, each of rooms 1–5 contains the types the ruling requires, confirmed by the trace setup row with `play.py --view trace`, at both 30 and 60 FPS.
- **Zero hearts:** after the third hit, the player view shows the defined outcome. The trace shows the defined state for enemies and input, with no silent no-op input.

## Load

- Role: studio/roles/game-designer.md
- Skills: none
- Project: design/combat.md, manual.md, project.md#current-state, project.md#constraints
- Decisions: none
- Previous handoff: goals/G-001-combat-monotony/04-studio-to-qa.md
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
