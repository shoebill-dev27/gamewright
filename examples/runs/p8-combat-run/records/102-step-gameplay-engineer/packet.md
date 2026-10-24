# Studio operation packet

operation: Step
goal: G-001
role: gameplay-engineer
incoming_handoff: goals/G-001-combat-monotony/99-studio-to-gameplay-engineer.md
next_seq: 101
runs: tests, trace, bots (up to 3 rounds)
run_tests: python3 -m unittest discover -s tests
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/101-gameplay-engineer-to-<recipient>.md
- repo/<path> (full file content)
- @run/<tests|trace|bots>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer (EDIT blocks always apply to the project files as written, never to a proposal)

## Inputs

<<<FILE studio/execution.md#executor-instructions
## Executor instructions

You are executing exactly one Studio operation, in isolation.

- Everything you may use is in this packet: the operation header, the input files, and the paths
  you may write. You know nothing else about this project, its history, or other steps, and you
  must not assume anything beyond the packet.
- Follow the procedure for this operation in the Studio files included. For a Step, act as the
  receiving Role within its contract and listed Skills; do not perform other Roles' work.
- Write every file you create as one complete file block: `<<<FILE <path>` on its own line, the
  full file content, then `>>>END` on its own line. To change part of an existing file, you may
  instead write `<<<EDIT <path>` with `<<<<<<< SEARCH` / `=======` / `>>>>>>> REPLACE` pairs and
  `>>>END` (Output protocol); each SEARCH must match the file exactly once, so include enough
  lines. Use only the paths listed under "You may write"; paths are relative to the project
  directory.
- Only file blocks are kept. Anything else you write is discarded and never shown to any later
  step, so put everything the next operation needs into the files.
- If the packet is not enough to do the operation, write the artifact that hands the work back or
  reports the blocker instead of guessing.
>>>END

<<<FILE goals/G-001-combat-monotony/99-studio-to-gameplay-engineer.md
---
kind: handoff
goal: G-001
seq: 99
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 99: studio → gameplay-engineer — Remove a stray edit marker from repo/manual.md (text only)

## Task

Open `repo/manual.md`. QA reports a leftover edit marker in the player-facing text. If it is there, remove it and restore the text below. Change nothing else, and make no code change.

## Context

Goal G-001 (combat feels monotonous). Build 29b was a wording-only round (shot-hit direction words, late-swipe line, manual text) per `design/combat-step94.md`. QA's verification (98) found that W1 and W5 pass and the suite is green (69 tests). QA saw the manual only as it was given in its packet and did not open the repo file, so the defect is unconfirmed.

## Findings

QA's report of the defect: in the "Warnings" section, the bullet starting `Being hit shows … by a shot from the <direction> (…)` is followed by the line `>>>REPLACE_PLACEHOLDER A swipe that interrupts the warning of a`. The next line continues `grub or runner staggers it for 0.4 s; …`. The result is a leftover marker in the player text, and the hit-message bullet and the stagger sentence are merged.

Expected fix:
- remove the marker;
- keep the hit-message bullet as it is, with the direction wording from step 94;
- restore a separate bullet: "A swipe that interrupts the warning of a grub or runner staggers it for 0.4 s; a brute is not interrupted." Keep the exact existing wording of that sentence's remainder.

Acceptance criteria:
1. `repo/manual.md` has no `>>>`, `<<<`, `REPLACE_PLACEHOLDER`, `SEARCH` or `=======` marker lines.
2. The hit-message bullet and the stagger bullet are two separate bullets.
3. The step 94 manual wording (direction words, the late-swipe sentence) is unchanged.
4. Search the other files you touched in build 29b (`repo/game.py`, the tests) for the same kind of marker. Report the result.
5. Run `python3 -m unittest discover -s tests` and report the result.

## Decisions already made

- D-011: variant names in messages (accepted).
- D-013: wording-only round, then Close.

## Constraints

- Text only. No gameplay, timing or parameter changes.
- If the marker is not in the file, change nothing and say so; that is a valid result.
- Stop and hand back if the file differs from this description in a way you cannot resolve.

## Open questions

None.

## Expected output

A handoff to `studio` (not to qa) with `outcome: done`. State what you found in the file and what you changed, and give the marker search and test results. Studio will compose the verification step for QA.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: repo/manual.md, design/combat-step94.md
- Decisions: decisions/D-011-variant-named-messages-accepted.md
- Previous handoff: goals/G-001-combat-monotony/98-qa-to-studio.md
>>>END

<<<FILE studio/roles/gameplay-engineer.md
---
kind: role
id: gameplay-engineer
load_forbid: goals/*/*-playtester-to-*.md
writes: @build
runs: tests, trace, bots
---
# Role: Gameplay Engineer

## Responsibility

Implements approved designs and plans as working changes to the game, and fixes defects, with tests.

## Decides

- Implementation details inside the approved spec and plan: code structure, naming, local algorithms.
- The root cause of a defect in code.

## Must not

- Decide player-facing behavior the spec does not define, or "interpret" an ambiguous spec — hand
  back instead.
- Change the spec, the plan's architecture, or the Goal's scope.
- Approve its own work; `qa` verifies.

## Works from

- An approved spec or a defect report, each with acceptance criteria.
- A plan, when the Technical Director made one.
- Project constraints and the repository.

## Produces

- The change, with tests where the project supports them.
- A Handoff to `qa`: what changed and where, how to exercise it, which acceptance criteria it
  addresses, known risks. Root cause reasoning, own test results and confidence go under
  `## Sender assessment`, which QA never receives.
- Or a hand-back: the open question, what is blocked, what could proceed.

## Hands back / escalates when

- The spec is ambiguous, contradictory, or missing a case → `game-designer`.
- The plan does not work or the risk is larger than planned → `technical-director`.
- The change would conflict with the vision or a Decision → `game-director`.
- The work needs an irreversible operation → Studio (Owner escalation trigger).

## Typical skills

implement-change
>>>END

<<<FILE studio/skills/implement-change.md
---
name: implement-change
description: Change the game per an approved spec or defect report and plan, with tests — and stop with a precise question when the spec does not define a behavior.
---
# Skill: Implement change

Typical roles: gameplay-engineer.

## When to use

An approved spec or a defect report with acceptance criteria exists, and the game must change.

## Inputs

Spec or defect report, acceptance criteria, plan (if any), constraints, repository.

## Method

1. Before coding, list every player-observable behavior the change will produce. Check each one
   against the spec or defect report. Any behavior the spec does not define is an open question,
   not a choice to make.
2. If a question blocks the work, stop that part. Hand back with: the question, the cases at
   stake, the options you can see with their technical cost, what is blocked and what can proceed.
   Do not pick an option. Do the unblocked work now if no answer would undo it, but deliver nothing
   to QA until the blocked part is resolved. For minor gaps you may propose a default for the
   designer to accept or change; never apply it before they do.
3. For defects, find and fix the root cause in the shared code path rather than patching the
   reported path only.
4. Implement, add or update tests, run them under the project's supported conditions.
5. Describe the change for QA: what changed and where, how to exercise it, which criteria it
   addresses, known risks. Put your root cause reasoning, own test results and confidence under
   `## Sender assessment` — QA verifies independently and never receives that section.

## Output

Change plus Handoff to `qa`, or a hand-back Handoff with the open question.

## Do not

Fill spec gaps with your own judgment. Do not expand scope. Do not mark your own work verified.
>>>END

<<<FILE repo/manual.md
# Lantern Depths — how to play build 0.6

Player-facing manual. A play session is an input script; the play command runs it and shows what a
player sees and hears, with the room drawn every half second and after every hit or warning.

## Controls

- **Move** in four directions; you keep moving until you stop or turn.
- **Attack**: a short swipe in the direction you face.
- **Dash**: a quick burst in a direction (or the way you face). You cannot be hurt while dashing.

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
| `spawn grub\|runner\|brute\|spitter <x> <y>` | Practice room setup: place an enemy. |
| `player <x> <y>` | Practice room setup: place yourself. |
| `when <condition> then <action>` | A reaction rule (below). |

## Reactions

Instead of (or as well as) timed inputs, you can play by reacting to what is on screen. Each frame
the rules are checked from the top; the first one whose condition holds acts. A rule acts at most
every 0.15 s, like a player's reaction time, so the next rule down can act meanwhile. A session
with rules runs until the room is cleared or you go down (at most 60 s), unless `end` says
otherwise.

| Condition | Holds when |
|---|---|
| `see <mark> within <n>` | that mark (`g`, `r`, `G`, `s`, `*`, …) is on screen within n tiles of you |
| `see <mark> coming within <n>` | the same, and it has moved closer since the last frame |
| `nothing within <n>` | no enemy or shot is on screen within n tiles |
| `text "<words>"` | a message with those words was just shown (for example `text "rears back"`) |
| `hearts <= <n>` | you have n hearts or fewer |

| Action | Does |
|---|---|
| `attack` | turn to what the condition saw (if anything) and swipe |
| `face` | turn to it without moving |
| `move <dir>`, `move toward`, `move away`, `move aside`, `stop` | move (`aside` steps across its line, toward the open side of the room) |
| `dash`, `dash <dir>`, `dash toward`, `dash away`, `dash aside` | dash |

Example:

```text
room 2
when see * coming within 1.5 then move aside
when see r within 1.4 then attack
when see g within 3 then face
```

The room is 16 tiles wide (x 0–15) and 9 tall (y 0–8); you start at x 8, y 4.

## On screen

`P` you, `g` grub, `r` runner grub, `G` brute grub, `s` spitter, `*` projectile, `~` an orange-red
line (see warnings below). Hearts are shown above the room.

- **Grub (`g`)**: 2 swipes. **Runner (`r`)**: fast, 1 swipe, short warning. **Brute (`G`)**: slow,
  4 swipes, long warning, and it does not flinch: a swipe does not interrupt its warning.
- **Spitter (`s`)**: 2 swipes, stays where it is.

## Warnings

Nothing hurts you without a warning. Every warning is shown for the whole time before the hit, and
the player view prints a picture when one starts.

- **A grub rears back** (message `a grub rears back`, `a runner rears back` or `a brute rears back`): the grub stops and flashes orange-red, and a
  line of `~` marks the 2.4 tiles it is about to lunge along. Under the room a line starting with
  `cue:` names the grub, says it flashes, and gives the line's direction and the seconds left. The
  line is fixed where you stood when the grub began; step 1 tile to the side or dash to avoid the
  lunge, or swipe a grub or runner to cancel it. A swipe cancels only during the warning, and only if the enemy is within 1.5 tiles at that moment. A grub starts rearing back about 2 tiles away, beyond your reach, so step in to within 1.5 tiles during the warning. A swipe that lands after the lunge has begun does not cancel it. When it happens the game says so: `the grub's lunge had already started, the swipe was too late to stop it` (or runner, or brute). One swipe is enough to cancel a grub or a runner. A brute is never cancelled. The warning lasts 0.5 s for a
  grub, 0.35 s for a runner, 0.7 s for a brute. After a lunge the grub is harmless for a while:
  that is the time to swipe it. Only one grub rears back or lunges at a time.
- **The brute does not flinch** (message `the brute shrugs off the swipe`): a swipe that hits a
  brute while it rears back still hurts it, but the warning goes on and the lunge still comes.
  Step aside or dash, then swipe it once it has lunged.
- **A spitter takes aim** (message `a spitter takes aim`): 0.6 s before it spits, the spitter glows
  orange-red, growing brighter, and a line of `~` shows where the shot will go. The `cue:` line
  under the room gives its brightness and the seconds left. The shot goes along that line
  (`a spitter spits`). Moving 1 tile aside or dashing avoids it. Shots are slow-looking but travel
  3 tiles a second. A spitter will not start aiming while 3 shots are already in the air, but shots from aims already under way still fire, so in room 3 up to 5 can be in the air at once. In rooms 4 and 5 the two spitters
  take aim one at a time: a spitter does not start aiming until the other has spat and 0.6 s have
  passed, so there is time to move between aims.
- Being hit shows `YOU ARE HIT by a grub`, `by a runner`, `by a brute` or `by a shot from the <direction>` (north, north-east, east, south-east, south, south-west, west or north-west: the side the shot came from, the same line the `cue:` line and `~` showed before the shot).
>>>REPLACE_PLACEHOLDER A swipe that interrupts the warning of a
  grub or runner staggers it for 0.4 s; a brute is not interrupted.
- A shot that reaches you while you are dashing or still flashing after a hit is stopped and does
  no damage.
- A grub's lunge that touches you while you cannot be hurt does no damage, even if your protection
  ends during that lunge.
>>>END

<<<FILE design/combat-step94.md
# Combat text view: shot-hit source and late-swipe wording (G-001 step 94)

Owner: game-designer. Basis: handoff 93, Review 92, QA 90, playtest 88, D-005, D-007, D-011, D-013. Wording only. No rule, number, timing, cap, cue or input changes. Where this note and `combat.md` differ on these two messages, this note governs.

## Intent

The player can tell why they got hurt. A shot hit says which way the shot came from. A swipe that was too late says so. The build already behaves correctly in both cases; only the text view hides the cause.

## Message A: shot-hit source

**Format.** The damaging-hit message becomes:

`YOU ARE HIT by a shot from the <direction>`

and the existing suffix (` — hearts n/3`) follows unchanged. The prefix `YOU ARE HIT by a shot` is untouched, so reaction rules and `bots.py` that match it keep working.

`<direction>` is one of eight words: `north`, `north-east`, `east`, `south-east`, `south`, `south-west`, `west`, `north-west`. North is the top of the drawn room (smaller y). East is the right (larger x).

**What the direction means.** It is the side the shot came from, relative to the player: the reverse of the shot's travel direction. A shot travelling west was fired from the east, so the message says `from the east`.

**How to compute it.** Take the shot's locked travel vector (vx, vy) at the contact frame, and let (dx, dy) = (-vx, -vy). Let a = |dx| and b = |dy|.
- If min(a, b) / max(a, b) <= 0.4142 (tan 22.5°), the direction is the cardinal word for the larger axis.
- Otherwise it is the diagonal word for the signs of dx and dy.

This depends only on the shot's fixed velocity, so it is identical at 30 and 60 FPS and independent of the hit frame.

**What the engineer must carry.** Nothing new. The shot already has a locked travel direction in order to move. The engineer reads it at the contact frame, before the shot is removed, when building the message. No spitter id, origin, fire time or position needs to be stored.

**Why this reveals nothing new.** The `cue:` line already gives the line's direction, and the `~` line already draws it for 0.6 s before the shot. The message repeats that same locked direction, from the player's side. It gives no distance, no time and no spitter identity, and the graphical build shows the same direction by sight.

**Scope.**
- It applies only to a hit that deals damage.
- A shot absorbed by a dash or the hurt window still shows no message (D-005, unchanged).
- Grub, runner and brute hit messages are unchanged.

## Message B: swipe too late to stop a lunge

**Trigger.** A swipe damages a grub, runner or brute that is in its Lunge phase and does not kill it. Hits in other phases and kills are unchanged.

**Format.** One line, at the moment of the swipe result and before any `YOU ARE HIT by` line of the same frame:

- `the grub's lunge had already started, the swipe was too late to stop it`
- `the runner's lunge had already started, the swipe was too late to stop it`
- `the brute's lunge had already started, the swipe was too late to stop it`

The line uses the variant name, as in D-011. It must not contain `rears back`, `takes aim` or `YOU ARE HIT by`, so no existing reaction rule fires on it. A runner has 1 HP, so a damaging swipe kills it and the runner line appears only if a future HP change allows it. The text is still defined for all three variants.

**Unchanged.**
- The brute's wind-up line `the brute shrugs off the swipe` and its rules (criterion 19).
- The lunge itself. A swipe in the lunge does not cancel, shorten or delay it, and the swipe's 1 damage applies as before.
- A swipe that kills a grub in its lunge shows no new line.

**Why this reveals nothing new.** It states a fact the player could already see: the `cue:` line and `~` lane end when the lunge starts. It gives no prediction.

## Edge cases

- Two shots hit in one frame: only one damages (D-005). One message, with the direction of the shot that dealt the damage.
- Swipe and hit in the same frame: the swipe line comes first, then the hit line.
- Swipes in recovery, approach or stagger: no new line.
- One message per swipe. No batching and no repeat suppression.

## Acceptance criteria (QA, 30 and 60 FPS, `play.py --view player`)

Practice room (`room empty`, `spawn`, `player`), all at both rates.

- **W1. Direction words.** A still player at (8,4) is hit by a single spitter's shot. Check these placements:
  - spitter at (15,4): `from the east`;
  - spitter at (8,0): `from the north`;
  - spitter at (1,4): `from the west`;
  - spitter at (8,8): `from the south`;
  - spitter at (15,0): `from the north-east` (ratio 4/7 = 0.57 > 0.4142);
  - spitter at (15,7): `from the east` (ratio 3/7 = 0.43, which is above 0.4142, so the diagonal `south-east` is expected; QA records the traced value and checks it matches the formula).
  
  In every case the full line begins `YOU ARE HIT by a shot from the `.
- **W2. Real room.** In room 4 and room 5 a damaging shot hit shows a direction word consistent with the `cue:` line direction of the spitter that fired it (the reverse of the cue direction).
- **W3. Prefix kept.** `text "YOU ARE HIT by"` and `text "by a shot"` match, and `rears back` and `takes aim` still match their lines. A reaction-rule script using each of the three substrings behaves as before the change.
- **W4. Absorbed shots.** A shot absorbed by a dash or the hurt window produces no hit message, as before.
- **W5. Late swipe.** A standard grub at (10,4), player at (8,4) facing it, one swipe timed from the trace during the lunge (0.3 s long, after the 0.5 s wind-up) so it lands on the grub in reach. The player view shows `the grub's lunge had already started, the swipe was too late to stop it`, and it appears before `YOU ARE HIT by a grub`. The grub loses 1 HP and still finishes the lunge. Repeat once with a brute and the `brute` wording.
- **W6. No line elsewhere.** The late-swipe line does not appear for a swipe in wind-up (the grub is cancelled; the brute shows `shrugs off`), in recovery, in approach or in stagger, and not for a kill.
- **W7. No behavior change.** Compared with the build before the change, with the same scripts at the same rate: hit times, hearts, cue times, shot fire and contact times, lunge and recovery times and the in-flight counts are identical to ±1 frame. Criteria 1–21 of `combat.md` hold. `bots.py` runs unchanged with the suite green, and the bots' hearts and clears are as before.
- **W8. Frame-rate independence.** W1 to W6 give the same wording at 30 and 60 FPS.

## Experience signals (Review and playtest, not for the Playtester's handoff)

- A player can say which side a hitting shot came from, and can connect it to a cue line they saw.
- A player who swiped a lunging grub and was hit can say "I was too late", and does not ask what makes a swipe cancel.

## Rejected alternatives

- Naming the spitter by coordinates or an ordinal: needs the shot to carry an origin, and adds identity the cue lines never showed. Not chosen.
- Showing distance or fire time in the hit message: gives the text view more than the graphical build gives. Not chosen.
- Keeping the shot visible after contact: touches D-005. Not chosen.
- A line for every swipe that does not cancel: noise, and it explains nothing in the other phases. Not chosen.
- No Decision record: none of these alternatives constrains later work beyond this note.

## Changed documents

- New: this note.
- `design/combat.md`: pointer added at the top (edit below).
- **`repo/manual.md` could not be edited (not in my write paths).** The text to apply is given below.

### Manual wording (for the Build step)

Replace the sentence "Being hit shows `YOU ARE HIT by a grub`, `by a runner`, `by a brute` or `by a shot`." with:

"Being hit shows `YOU ARE HIT by a grub`, `by a runner`, `by a brute` or `by a shot from the <direction>` (north, north-east, east, south-east, south, south-west, west or north-west: the side the shot came from, the same line the `cue:` line and `~` showed before the shot)."

After "A swipe that lands after the lunge has begun does not cancel it." add:

"When it happens the game says so: `the grub's lunge had already started, the swipe was too late to stop it` (or runner, or brute)."
>>>END

<<<FILE decisions/D-011-variant-named-messages-accepted.md
---
kind: decision
id: D-011
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-16
supersedes: D-008
---
# D-011: Text-view wind-up and hit messages name the variant (accepted); swipe timing stays a wording matter

## Decision

1. The wind-up messages are `a grub rears back`, `a runner rears back` and `a brute rears back`. The hit messages are `YOU ARE HIT by a grub`, `by a runner` and `by a brute`. The shot message stays `by a shot`. The strings and acceptance criteria V-a to V-e are in `design/combat-step68.md`.
2. This completes D-008, which left the hit message out. Playtest 63 showed the hit message was the other half of the confusion.
3. No swipe-timing rule change. The late-swipe manual wording from step 59 is specified in `design/combat-step68.md` and is ready to build.
4. The change is player-facing wording within the designer's authority. It adds no input (D-001), no timing change and no new information beyond the existing `cue:` line, so it stays inside the "readable threats" pillar.
5. Build only after Review 65. It must not be mixed silently into a playtest pass of 0.6.1 (D-009 item 5): hold it until after any further 0.6.1 playtest, or state the new build number in that brief.

## Rationale

- A text-view player sees the message line first. A brute or runner reported as "a grub" hides which answer applies, and playtest 63 rated this medium impact on clarity.
- Naming the variant gives the text view the early information the graphical build gets from silhouette and size. It changes no timing or hit points.
- The shared words `rears back` keep existing reaction rules working.
- Wording alone explains the two reported late-swipe hits (QA 56). A grace period or larger reach would let a swipe cancel a started lunge and weaken "step aside or dash".

## Alternatives considered

- Keep one message for all variants: leaves the playtest confusion, and reaction-script players must parse the `cue:` line.
- Put distance and time left in the message: duplicates the `cue:` line and may make the text view easier than the graphical build.
- Wind-up renames only: leaves a brute hit labelled "a grub".
- A swipe grace period or a larger wind-up reach: needs a rule change with no defect behind it.

## Revisit when

- The next playtest still shows wasted dashes or "I could not tell what it was" after the rename.
- A human still reports late swipes as unfair after the manual wording is in.
- A graphical build makes the text messages irrelevant.
>>>END

<<<FILE goals/G-001-combat-monotony/98-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 98
from: qa
to: studio
stage: Verify (report for routing to Review pass 4 or back to Build)
outcome: fail
---
# 98: qa → studio — Verification of W1–W8 on build sha 0f2c1f134c79: NOT a pass (manual defect, several criteria not fully shown)

## Task

Report the pass/fail result per criterion W1–W8 at 30 and 60 FPS, the suite and bots results, and regressions. Route to Build if the manual defect below is confirmed. Otherwise decide whether the unshown items are accepted as known gaps.

## Context

Verification of the wording-only change from `design/combat-step94.md` (handoff 97). This round had one set of runs: tests, bots and play views. The results hold play-view runs only. No `--view trace` run is in the results, and no previous build or baseline output was available. Zero rounds are left, so unshown items stay unshown. I did not modify any code.

## Findings

**Verdict: fail.** W1 and W5 pass. The player-visible manual shows a defect. W2, W3, W4, W6, W7 and W8 are only partly shown or not shown.

### Suite and bots
- Suite: `python3 -m unittest discover -s tests` ran 69 tests, OK, exit 0.
- Bots ran at 60 FPS only. No 30 FPS bot run was possible in this packet.
  - Walker: rooms 3–5 summed 6 hearts lost and 2 cleared. Rooms 1–2: 5 hearts lost.
  - Dodger: 5/5 cleared, 0 hearts lost, dashes in every room (rooms 3, 4 and 5: 6, 8 and 14).
  - Camper: 0/5 cleared.
  - Against the combat.md limits (criteria 13, 14, 15): walker 6 hearts, within 3–6; walker clears 2 of rooms 3–5; dodger at most half the walker's hearts and clears 3/3; camper clears fewer than the walker; rooms 1–2 walker loses at least 1, dodger loses at most 1 and clears both; dodger uses at least 1 dash in each of rooms 3–5. All hold at 60 FPS.
  - The bots classify hits as "shot", so the unchanged prefix `YOU ARE HIT by a shot` still parses.
  - There is no baseline in the packet, so "bots as before" (W7) is not shown. These are the current values only.

### W1 Direction words (spitter and player in the practice room, player at (8,4), both rates)

| Spitter at | Hit line seen, 30 FPS | Hit line seen, 60 FPS | Expected | Result |
|---|---|---|---|---|
| (15,4) | 4.000 `YOU ARE HIT by a shot from the east — hearts 2/3` | 3.983, same text | east | pass |
| (8,0) | 2.967 `…from the north…` | 3.000, same | north | pass |
| (1,4) | 4.000 `…from the west…` | 4.000, same | west | pass |
| (8,8) | 3.000 `…from the south…` | 3.000, same | south | pass |
| (15,0) | 4.333 `…from the north-east…` | 4.350, same | north-east (ratio 0.57) | pass |
| (15,7) | 4.200 `…from the south-east…` | 4.200, same | formula | pass |

- For (15,7) the cue is (-0.92,-0.39). The reversed vector is (0.92,0.39), ratio 0.42 > 0.4142, so the formula gives south-east, and the trace shows south-east.
- Every line begins `YOU ARE HIT by a shot from the `. W1: **pass at 30 and 60 FPS.**
- Spec ambiguity: the (15,7) bullet is self-contradictory. It labels the case `from the east` and then says the diagonal is expected. I judged against the formula, as the bullet itself tells QA to do (see Open questions).

### W2 Real rooms
- Room 4, 60 FPS: one shot hit, at 5.550, `from the south-east`.
  - It came from the spitter at (15,8), which has cue direction (-0.87,-0.50). Reversed, that is south-east, so it is consistent.
  - The shot was fired at 3.0 s. Arrival is 3.0 + 2.55 = 5.55 s (derived).
- Room 5, 60 FPS: three shot hits. Matching each hit to the spitter by fire time (derived) gives:
  - 4.350 `north-east`, from the (15,0) spitter fired at 1.8 s, cue (-0.87,+0.50).
  - 5.550 `south-east`, from the (15,8) spitter fired at 3.0 s.
  - 6.750 `north-east`, from the (15,0) spitter fired at 4.2 s.
  - All three are consistent with the reversed cue direction.
- **Pass at 60 FPS in rooms 4 and 5.**
- At 30 FPS the room 4 run ended with 0 shot hits (the player was downed by runners at 5.8 s). Room 5 was not run at 30 FPS. **W2 at 30 FPS is not shown.**

### W3 Prefix kept
- Suite is green. Bots parse `shot` hits.
- `text "rears back"` rule at 60 FPS, grub at (10,4): the rule fired (player stepped up at about 0.5 s) and there was no damage. This shows `rears back` still matches.
- `text "by a shot"` rule: the hit line was shown at 3.983, but the player did not move up afterwards (`P` stayed on row y=4 to 5.5 s). The action fell inside the 0.3 s hit-stun, or the rule did not fire. The run cannot tell which, so it does not show the match.
- `text "YOU ARE HIT by"` and `text "takes aim"` were not run.
- **W3 is partly shown, not passed.** There is no before/after comparison either.

### W4 Absorbed shots
- Dash case at 30 and 60 FPS: dash right at 3.8 s into the shot (first shot fired at 1.8 s, arriving about 4.0 s).
  - No hit message, hearts stayed 3/3 at the end (4.17 s and 4.15 s), and no `*` remains on the frame at 4.00 s.
  - **Pass for the dash case at both rates.** The run ended 0.1–0.15 s after contact, so "no damage afterwards" is not shown.
- Hurt-window case: not run. **W4 is partly shown.**

### W5 Late swipe

| Case | Rate | Swipe | Late-swipe line | Hit |
|---|---|---|---|---|
| Grub at (10,4) | 30 | 0.6 | `0.600 the grub's lunge had already started, the swipe was too late to stop it`, before `0.600 you swipe: grub hit` | 0.733 `YOU ARE HIT by a grub` |
| Grub at (10,4) | 60 | 0.6 | same | 0.700 |
| Brute at (10,4) | 60 | 0.8 | `the brute's lunge…`, 0.800 | 0.900 |
| Brute at (10,4) | 30 | 0.8 | same | 0.933 |

- In all four, the late-swipe line comes before the hit line and the swipe result shows "hit", not "killed". The lunge completed and the hit landed.
- The remaining grub HP is not visible in the player view (it was not checked in a trace view).
- **W5: pass at 30 and 60 FPS** for line, wording and ordering. "Loses 1 HP" rests on the `hit` message only.

### W6 No line elsewhere
- Grub wind-up swipe (swipe at 0.3, player at 8.8) at 30 and 60 FPS: `you swipe: grub hit`, no late line, and the cue is cancelled. The grub rears back again later. Pass.
- Brute wind-up swipe, 60 FPS only: `the brute shrugs off the swipe`, no late line. Pass at 60.
- Grub recovery swipe (at 1.3 s), 60 FPS only: `you swipe: grub hit`, no late line. Pass at 60.
- Not run: approach, stagger, kill in the lunge, and brute wind-up and recovery at 30 FPS. **W6 is partly shown.**

### W7 No behavior change
- No trace view was run and there is no baseline, so a comparison with the previous build cannot be made.
- Observed values match the spec's numbers, but this is not a comparison with the previous build:
  - first shots at 1.8 s and 3.0 s in rooms 4 and 5;
  - 2.4 s fire interval;
  - cue at 0.6 s before the shot;
  - grub wind-up 0.5 s and brute 0.7 s;
  - shot arrival about 2.2 s after the shot at 7 tiles.
- **W7 is not shown.**

### W8 Frame-rate independence
- Same wording at both rates for W1 and W5, and for the W6 grub wind-up case.
- Not shown for W2, W6 (several items) and W3, because those were not run at both rates. **W8 is partly shown.**

### Defect: `repo/manual.md` (as given in this packet) contains stray text
- In the "Warnings" section, the bullet that starts `Being hit shows … by a shot from the <direction> (…)` is followed by the line `>>>REPLACE_PLACEHOLDER A swipe that interrupts the warning of a`. The next line continues `grub or runner staggers it for 0.4 s; …`.
- A leftover edit marker is in the player-facing text, and the hit-message bullet and the stagger sentence are merged. The intended manual wording from step 94 is otherwise present, including the late-swipe sentence and the hit wording.
- I saw only the packet's copy and did not open the repo file. Severity: low to medium (player-facing documentation, no gameplay effect). Fix: remove the marker and restore a separate bullet "A swipe that interrupts the warning of a grub or runner staggers it for 0.4 s; a brute is not interrupted."
- This is not a W1–W8 gameplay failure. The manual text was part of the Build task in `combat-step94.md`, so it blocks a pass.

### Known gaps from handoff 97
- R3-8 at 60 FPS, the room 3 sidestep, and the 30 FPS cancel and recovery swipe in room 3 were not tried and stay known gaps.
- The 30 FPS grub cancel was seen in the practice room only (W6 above), not in room 3. The 30 FPS recovery swipe was not seen.

## Decisions already made

- D-005: blocked contact consumes the shot and spends the lunge's hit. Only the dash case was observed, with no message and no damage.
- D-011: variant names in messages. Confirmed in all W5 lines and the cue lines.
- D-013: wording-only round, then Close, with a pre-commitment. This report does not meet the "pass" condition for that, so nothing here supports goal-met yet.

## Constraints

- No production code was changed.
- No QA rounds are left.
- Findings are limited to what is shown above. Derived figures (arrival times, matching a hit to a spitter by fire time) are marked as derived.

## Open questions

1. To `game-designer`: the W1 bullet for the spitter at (15,7) says `from the east` and then says the diagonal is expected. The formula and the build give `south-east`. Please correct the criterion text. I judged by the formula.
2. To the Studio: the manual stray marker, if confirmed in the repo, needs a Build fix. Do you want a re-verify of the manual line only?
3. To the Studio: are the unshown items (W2 at 30 FPS, W3 other substrings, W4 hurt window and post-dash, W6 approach, stagger, kill and 30 FPS cases, W7 trace comparison, bots at 30 FPS) accepted as known gaps like those in D-013 item 5, or do they need another QA round?

## Expected output

The Studio reads this report. If the manual defect is confirmed, it routes to Build for a manual-only fix. Otherwise it decides on Review pass 4 and the gap acceptance in Open questions 2 and 3. A criterion that fails goes back to Build with this report.

## Load

- Role: Studio routing (Review or Build, chosen by the Studio)
- Skills: studio/skills/verify-change.md
- Project: design/combat-step94.md, design/combat.md, repo/manual.md, the build in `repo/`
- Decisions: decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md, decisions/D-011-variant-named-messages-accepted.md, decisions/D-013-review-pass-3-readability-wording-then-close.md
- Previous handoff: goals/G-001-combat-monotony/97-studio-to-qa.md
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
