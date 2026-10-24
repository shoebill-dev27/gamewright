# Studio operation packet

operation: Step
goal: G-001
role: qa
incoming_handoff: goals/G-001-combat-monotony/97-studio-to-qa.md
next_seq: 98
runs: tests, play, trace, bots (0 rounds left; results in @run-results)
run_tests: python3 -m unittest discover -s tests
run_play: python3 play.py --view player {script}
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/98-qa-to-<recipient>.md

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

<<<FILE goals/G-001-combat-monotony/97-studio-to-qa.md
---
kind: handoff
goal: G-001
seq: 97
from: studio
to: qa
stage: Verify
outcome: routed
---
# 97: studio → qa — Verify the wording changes W1–W8 at 30 and 60 FPS

## Task

Verify the current build (`repo/`, sha 0f2c1f134c79) against criteria W1–W8 in `design/combat-step94.md`. Use `play.py --view player` and `--view trace` at both 30 and 60 FPS. Also run the test suite and the bots, and check for regressions.

## Context

Goal G-001 (combat feels monotonous). Review pass 3 (D-013) found one remaining gap: the player cannot tell where a shot that hits them came from, and nothing explains why a late swipe did not stop a lunge. A wording-only change was specified in `design/combat-step94.md` and then built. Nothing about rules, numbers, timing, the room 3 cap, the cue rule or inputs should differ from the previous build.

## Findings

Nothing from earlier verification is carried over. Judge only from the spec, the acceptance criteria and the build.

Two items are known not to be covered by the existing tests, so exercise them by script:
- W2: rooms 4 and 5, compared against the `cue:` trace lines.
- W7: compare traces (player view and trace view) with the previous behavior. Only wording may differ.

## Decisions already made

- D-005: a contact blocked by invulnerability consumes the shot and spends the lunge's hit.
- D-011: wind-up and hit messages name the variant.
- D-013: this wording-only round, then Close.

## Constraints

- Desktop build that must play correctly at 30 and 60 FPS.
- Attack, dash and pause are the only inputs.
- Report only what you observe and reproduce. Findings you cannot show are listed as unshown, not guessed.
- Earlier rounds could not show these items. Try them if cheap, otherwise list them as known gaps; there is no further QA try after this round: R3-8 at 60 FPS, the room 3 sidestep, and the 30 FPS cancel and recovery swipe.

## Open questions

If a criterion is ambiguous or undefined, say so as a question rather than judging it.

## Expected output

A pass/fail report per criterion W1–W8 at 30 and 60 FPS, plus the suite and bots results and any regression. Address the result to `studio` (the Studio routes to Review pass 4). A criterion that fails goes back to Build with your failure report.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat-step94.md, design/combat.md, repo/manual.md, project.md#current-state, project.md#constraints, the build in `repo/` (run commands in project.md front matter)
- Decisions: decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md, decisions/D-011-variant-named-messages-accepted.md, decisions/D-013-review-pass-3-readability-wording-then-close.md
- Previous handoff: none
>>>END

<<<FILE studio/roles/qa.md
---
kind: role
id: qa
strip_sections: Sender assessment
runs: tests, play, trace, bots
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

<<<FILE design/combat.md
# Combat design (specified in G-001 step 07, rulings in steps 14, 22, 30, 35 and 38; builds 0.5 and 0.6)

Status: Build 0.5 implements the Grub, Spitter and room changes below. Step 14 settled criteria 13–16 and the five spec gaps (marked "step 14" in the text). Step 22 settled the contact-edge graze, the shot cap, the walker margin and which document governs each text/visual contradiction (marked "step 22"). Step 30 clarified the wording at exactly the reach and recorded the measured lunge band (marked "step 30"; wording only, see D-003). Step 35 specified two changes for the next build (0.6): a cue-gap rule for the spitters in rooms 4–5, and a brute whose wind-up is not cancelled by a swipe (marked "step 35"; see D-004). **Step 38 adds two rulings for the same build 0.6: a contact that is blocked by invulnerability consumes the shot, and uses up the lunge's hit (marked "step 38"; see D-005); and a simultaneous cue start outside rooms 4–5 is accepted. Build 0.6 implements the step 35 and step 38 parts (verified by QA, handoff 82); build 0.5 behaved as described without them.** The player kit is unchanged from 0.4.

**Step 80 (documents only, no rule or number changed):** the room 3 row and purpose, criterion 11 (in-flight bound), criterion 12, the Cap paragraph's real-room sentence and the wind-up message wording were brought in line with `combat-step68.md` (D-011), `combat-step72.md` (D-012) and D-007. Where they differ, those notes and decisions govern.

**Step 94 (wording only, no rule or number changed):** the hit message for a shot now names the side the shot came from (`YOU ARE HIT by a shot from the <direction>`), and a swipe that damages a grub already in its lunge shows `the <variant>'s lunge had already started, the swipe was too late to stop it`. Exact formats and acceptance criteria W1–W8 are in `design/combat-step94.md`, which governs these two messages.

**Step 87 (documents only, no rule or number changed):** the wording items from QA report 82 section 4 (cue gap rule for room 3, two step 38 references to the room 3 simultaneous-start case, title and header build references) were corrected.

## Intent

Every threat is visible before it can hurt, and every threat has an answer other than "stand and swing". Walking straight into a fight without reading it should cost hearts. Reading the cue and using a sidestep or the dash should cost fewer. Grub rooms should differ from each other, and the dash should be worth using.

**Step 35 intent.** The three melee enemies should ask for three different answers: the runner "commit or step out fast", the standard grub "either", the brute "step aside, then punish". In the crossfire rooms a player who reads a cue should have time to act on it before the next cue aims at them.

**Step 38 intent.** Damage lands where the player can see the threat touch them, never later. A shot or lunge that reaches a player who cannot be hurt is spent, so it cannot come back as a hidden hit when the protection ends. The dash is then a clean answer to a shot or a lunge that it overlaps.

## Player kit (unchanged)

- **Attack** (one button): a short swipe in the facing direction, reach 1.5 tiles. 1 damage. 0.35 s recovery.
- **Dash**: 4 tiles over 0.25 s. The player is invulnerable for the full dash duration. Cooldown 0.6 s. An attack pressed during a dash is queued and fires when the dash ends.
- **Getting hit**: 1 heart of damage, 0.3 s hit-stun (no input), then invulnerability until 0.8 s after the hit.
- Player speed 4 tiles/s. 3 hearts per room. No new inputs (D-001).

## Timing rule (applies to everything below)

All durations are in seconds and run on accumulated time, not frame counts, so 30 and 60 FPS behave the same. Per-frame travel of a lunging grub (at most 8/30 = 0.27 tile) and of a shot (at most 3.0/30 = 0.1 tile) stays below the contact reach (0.6 and 0.4), so nothing tunnels through the player at 30 FPS.

### Contact sampling rule (step 22, accepted limitation, see D-002; step 30 wording, see D-003)

- Contact is a distance check made once per frame, after that frame's movement. A distance of exactly the reach or less counts as contact (`distance <= reach`). Reach: shot 0.4 tile, grub lunge 0.6 tile. There is no swept test between frames.
- Consequence: when a path passes the player's center at a distance (the "lateral miss") very close to the reach, whether a frame lands close enough to count depends on the frame phase, so 30 and 60 FPS can differ in hit or miss for identical input. This is accepted for the text build.
- **Step 30 (the band, defined without gaps).** The band is the range of lateral miss that is more than reach − tolerance and at most the reach, the reach itself included:
  - Shots: more than 0.39 and up to and including 0.40 tile. QA derived about 0.003 tile of actual disagreement.
  - Lunges: more than 0.57 and up to and including 0.60 tile. Measured by QA (step 24, five probes, not a full scan): a hit is guaranteed up to about 0.585 at 30 FPS, so the disagreement band is about 0.015 tile at 30 FPS and about 0.004 tile at 60 FPS. The rates disagreed only at 0.590. See D-003.
- Outside the band the result must be the same at both rates and must follow the geometry: a lateral miss of reach − tolerance or less always hits (if the player is not invulnerable), and a lateral miss greater than the reach never hits.
- **Step 30 (exactly the reach).** A lateral miss of exactly the reach (0.400 shot, 0.600 lunge) is inside the band. Hit or miss are both accepted at either rate, and the result may differ between 30 and 60 FPS. It is not a guaranteed miss, and the `<=` in the build stays.
- The band changes only hit or miss. It must never change timing, cue, message or phase of anything.

### Blocked contact (step 38, see D-005)

Contact detection is unchanged (rule above). This section says only what happens after a contact is detected while the player cannot be hurt. The player cannot be hurt during the whole dash, during the hit-stun, and during the hurt invulnerability (until 0.8 s after the hit).

- **Shot.** A shot that makes contact (distance <= 0.4) with the player in any of those states is **consumed**: it disappears on that frame, exactly as if it had hit, and deals no damage. It does not pass through, and it does not wait for the protection to end. A shot is therefore removed by the first contact, whether or not it damages.
- **Lunge.** A lunge has one hit. If a lunge makes contact while the player cannot be hurt, its hit is **spent**: it deals no damage for the rest of that lunge, even if the protection ends while the grub is still within 0.6 tile. The lunge itself is not cancelled and not stopped (the existing rule: the grub finishes the lunge wherever it ends, then does its recovery).
- A shot that arrives in the same frame in which the hurt window ends: contact is evaluated after that frame's movement and with the protection state of that frame. If the player is hurtable in that frame the shot hits, otherwise it is consumed. A difference of one frame between 30 and 60 FPS here is accepted (±1 frame), as for any hit time.
- Two shots arriving together: the first that makes contact hits (if the player can be hurt) and the other is consumed by the hurt window. The player takes 1 damage, as before. Close shots no longer chain at the end of the window.
- No new message is required in the text view; the `*` simply disappears at the player. Presentation of an absorbed shot is owned by `art-director`.

## Enemies

### Grub (A): three-phase attack with a telegraph

Phases:

1. **Approach.** Walks straight at the player at the grub's speed. Bites on contact only during the lunge (see below). Walking alone does not damage. Replaces the old "contact bite while walking".
2. **Wind-up** (starts when the player is within 2.0 tiles and no other grub is in wind-up or lunge).
   - The grub stops.
   - The aim direction is locked to the player's position at the start of the wind-up.
   - **Step 14:** if the grub is exactly on the player (distance 0), the locked direction is right (+x). The cue and line are shown as usual.
   - Visible cue for the whole wind-up duration: the grub is tinted saturated orange-red (how it pulses or flashes is presentation, see below) and a line or lane shows the lunge path (length equal to the lunge distance).
   - **Step 22:** the danger zone of a lunge is 1.2 tiles wide (0.6 either side of the locked line) and 2.4 tiles long. A graphical cue must show the lane at that real width, so the player can see that a 1-tile sidestep clears it. The text view draws a one-cell `~` line; that is the text build's presentation of the same lane and stays.
   - Text view: a message naming the variant when it starts: `a grub rears back`, `a runner rears back` or `a brute rears back` (D-011). The strings, and the matching hit messages `YOU ARE HIT by a grub/runner/brute`, are in `combat-step68.md`, which governs.
   - Cue visible at least 0.5 s before the hit for the standard grub. The player has time to step out of the line, because player speed is 4 tiles/s and the line is 0.6 tiles to either side.
3. **Lunge.** Moves along the locked direction at lunge speed for the lunge time (distance 2.4 tiles). It stops early on contact with the player. If the player is inside reach 0.6 and not invulnerable, it deals 1 damage (once per lunge). Contact follows the sampling rule above. **Step 38:** a contact while the player cannot be hurt spends the lunge's hit (see Blocked contact).
4. **Recovery.** The grub is stationary and unthreatening for the recovery time, then returns to Approach. This is the safe window to swipe it.

Rules:

- **Step 35 (cancel is a per-variant flag, "swipe cancels wind-up").** Standard grub: yes. Runner: yes. Brute: **no**. For a variant with the flag set to yes: a swipe that damages a grub in wind-up cancels the wind-up. The grub is staggered (no action) for 0.4 s, then returns to Approach.
- **Step 35 (brute, flag no).** A swipe that damages but does not kill a brute in wind-up deals its 1 damage and changes nothing else: the wind-up continues on its original timer, with no stagger, the aim stays locked, and the lunge happens at the normal time. The text view shows the message "the brute shrugs off the swipe" at the moment of the swipe. Any number of swipes in the same wind-up each deal 1 damage and each show the message. A swipe that kills the brute in wind-up defeats it as for every grub (no lunge). The brute is still hit-able and takes damage in every phase, and a hit in Approach, Lunge, Recovery or Stagger changes nothing, as for every grub.
- **Step 14:** a swipe that kills a grub does not stagger it. The grub is simply defeated (in wind-up too).
- **Step 14:** a grub that is hit but not killed during Approach, Lunge, Recovery or Stagger continues its phase unchanged. Only a hit during wind-up of a variant with the flag yes changes its phase (step 35), and a hit during stagger does not extend the stagger.
- At most one grub is in wind-up or lunge at a time. Others keep walking and wait. This prevents simultaneous unavoidable lunges.
- The player's dash invulnerability stops the damage. The lunge is not cancelled. The grub finishes the lunge, wherever it ends, then does its recovery. **Step 38:** if the lunge touched the player during the dash, its hit is spent and it does not damage after the dash ends, even if the grub is still within reach on the dash's last frame or later in the same lunge.
- Hurt-invulnerability (0.8 s) also stops the damage the same way, and spends the lunge's hit the same way (step 38).
- A lunge is clamped at the room edge like all movement.
- If the player is dead or the room is cleared, grubs stop.
- **Step 22 (what is rule and what is presentation):** the rule is that the cue is visible during the whole wind-up, shows the lunge lane at its true size, and disappears at once when the wind-up is cancelled or the grub is killed. Whether the lane stays, fades or is removed during the lunge itself, and whether the tint flashes or holds a slight pulse (no faster than 3 Hz), is presentation owned by `art-director`. The text view removes the line when the lunge starts, and that is fine.
- **Step 35 (brute cue stays).** Because a swipe does not cancel the brute, its cue is not removed by a swipe that does not kill it. The cue is removed only by the kill, and as before it ends at the lunge. The lane geometry is identical for all variants.

Consequence worth knowing when reading bot results: a wind-up always comes before the first contact. A player who ignores the cue and does not move takes one lunge per grub (1 heart each), then gets the recovery window to swipe it. **Step 35:** a player who stands and swipes a brute during its wind-up now also takes the lunge. The recovery window of the brute is 1.2 s, in which up to four swipes fit if the player is in reach and facing it from the start (0.35 s per swipe). With a human reaction time of about 0.3 s, about three fit, so killing a full-health brute normally takes two windows. This is a derivation, not a measurement.

Parameters (Grub is one type, with parameter sets only; same behavior and same code path):

| Variant | Mark (text) | HP | Walk speed (tiles/s) | Wind-up (s) | Lunge speed (tiles/s) / time (s) | Recovery (s) | Swipe cancels wind-up (step 35) |
|---|---|---|---|---|---|---|---|
| Standard grub | `g` | 2 | 1.0 | 0.5 | 8.0 / 0.3 | 0.8 | yes |
| Runner grub | `r` | 1 | 1.6 | 0.35 | 8.0 / 0.3 | 0.6 | yes |
| Brute grub | `G` | 4 | 0.7 | 0.7 | 8.0 / 0.3 | 1.2 | **no** |

Tuning range allowed to engineering and QA without a new spec (if bots or play need it): wind-up 0.35–0.7 s for any variant. Never below 0.35 s. The cancel flag is not part of the tuning range.

### Spitter (B): staggered, with an aim cue

- **Aim cue.** 0.6 s before each shot the spitter glows saturated orange-red, growing brighter. The shot direction is locked to the player's position at the start of the cue. The direction is shown as a thin orange-red line for the 0.6 s of the cue. Text view: "a spitter takes aim" at the start of the cue and "a spitter spits" at the shot. The shot is then fired along the locked line.
- **Step 22 (glow start):** the rule is that the cue is noticeable from its first frame, the line is at full brightness from the first frame, and only the glow ramps. The starting level of the ramp is presentation. The text view shows 0% in its `cue:` line and stays; a graphical build uses a floor of at least 30% (as in the visual spec). This changes no timing.
- **Shot.** Speed 3.0 tiles/s (was 1.6). It travels in a straight line, does 1 damage, and disappears at the room edge, on contact with the player, or after 5 s. Dash invulnerability and hurt-invulnerability stop the damage as now. Contact follows the sampling rule above. **Step 38:** "on contact with the player" means any contact: a shot that touches a player who cannot be hurt is consumed on that frame with no damage (see Blocked contact). It never waits for the protection to end.
- **Interval and stagger.** Fire interval 2.4 s (was 2.0 s). After the first shot each spitter fires every 2.4 s after its previous shot. The first shot of the k-th spitter in room order (k = 0, 1, 2…) is at 1.8 s + *offset* × k, where *offset* is a per-room parameter (step 35):
  - Default (rooms 1–3 and practice rooms): offset 0.8 s. With three spitters, shots are 0.8 s apart (room 3, unchanged).
  - **Rooms 4 and 5 (step 35): offset 1.2 s.** With the two spitters of those rooms the first shots are at 1.8 s and 3.0 s, and then every 1.2 s alternating.
- **Spitter index (step 14).** k counts only spitters, in spawn order (room table order; the practice room uses `spawn` order). A defeated spitter does not renumber the others.
- **Cue gap rule (step 35, rooms 4 and 5 only; the rule, not the offset, is what must always hold).** Intent: after a cue ends, the player has at least 0.6 s before any spitter in the room locks onto them again, whatever the spitters' own schedules say (also if two spitters would end up firing together).
  - A spitter in a gap room may start a cue only if all of these hold at the check:
    1. no other spitter in the room has a cue running;
    2. the last shot fired in the room (by any spitter) was at least 0.6 s ago (comparison with a tolerance of 1 ms, so that an exact schedule tie counts as satisfied at both frame rates);
    3. the shot cap below allows it.
  - If a condition fails, the spitter waits 0.2 s and checks again (the same mechanism as the cap delay). The delay carries forward as in "Cap delay".
  - Player-observable form: between the shot of one cue and the start of the next cue (any spitter in rooms 4–5) there are at least 0.6 s, give or take one frame. Cue windows of different spitters never overlap.
  - A cue that is cancelled because its spitter was killed does not count as a shot for condition 2. Condition 1 only looks at running cues.
  - With the offsets above the rule is met by the schedule itself (gap exactly 0.6 s), so in the normal case it adds no delay. It acts only if the cap delay or a later change moves cues closer together.
  - Room 3 and practice rooms do not use this rule. Their first-shot schedule has 0.2 s between consecutive cues; after a cap delay simultaneous starts are accepted (D-007).
  - **Step 38 (ruling, simultaneous start outside rooms 4–5).** Two cues starting at the same moment after a cap delay (QA, handoff 36, practice replica at 6.8 s) is **accepted** in room 3 and in practice rooms; the gap rule is **not** extended, and criteria 11 and 18 do not change for them. Reasons: the case has been reproduced only in a practice replica with a surviving player and not in a real room; room 3 is the room that teaches the cue and its verified timing (1.8, 2.6, 3.4 s) would stay the same either way; two simultaneous cues are two separate full-brightness lines the player can still read and the shots are not unavoidable (each can be sidestepped, and a dash clears both); and rooms 4–5, the rooms where the playtest reported crossfire, are covered by the rule. The reopen triggers are those of D-007 (revisit of D-005 item 4).
- **Cap (step 22: a limit on cue starts).** A spitter may start a cue only if fewer than 3 shots are in flight at that moment; otherwise it waits 0.2 s and checks again. The cap is not rechecked when a shot fires. So shots from cues that started earlier may briefly take the number in flight above 3. At most, the count at a check is 2, plus the checking spitter's own shot, plus one for each other spitter already in a cue: never more than 2 + the number of living spitters. In rooms 4–5 the count stays at 3 or fewer. In room 3 up to 5 is accepted after a cap delay (2 plus the living spitters, D-007; see `combat-step-46-room3-cap.md`). A practice room with four or more spitters can also go above 3 (QA saw 5 with four spitters). This is intended. The reason: the cue is the telegraph, and refusing to fire a shot whose cue is already showing would break "the cue always ends in the shot" and make cues lie.
  - **Step 35:** in rooms 4–5 the shots come 1.2 s apart (before: 0.8 s and 1.6 s alternating), and a shot lives up to 5 s, so with the player far from the spitters the cap can now delay a cue. That is accepted and wanted (fewer shots in the air). The cap stays 3 in all rooms; lowering it to 2 was considered and not taken (D-004).
  - **Step 38:** a shot consumed by a blocked contact leaves the air at once, so it frees a cap slot earlier than a shot that waited for the window to end. The cap rule itself does not change.
- **Cap delay (step 14).** The 0.2 s wait starts at the moment the cue would have started, and repeats until a slot is free. The delay moves that shot later, and the spitter's following shots keep 2.4 s from its actual shot (the delay carries forward). The first-shot times in criterion 11 are not affected, because the cap is not reached by then.
- **HP** 2, stationary, and can be swiped at any time. No change.

## Rooms (C: light pass, existing enemies and parameter variants only)

5 rooms, 3–6 enemies each. A room ends when all enemies are defeated. Positions are (x, y) in tiles. Steps 35 and 38 change no room contents.

| Room | Contents | Spitter offset / cue gap rule | Purpose |
|---|---|---|---|
| 1 | Standard grubs at (3,4), (15,4), (8,0) | n/a | Teach the lunge cue against one grub at a time |
| 2 | Runner (2,1), Runner (1,8), Brute (15,7), Standard (14,0) | n/a | Different from room 1: fast fragile ones plus a slow tough one, from four corners. Step 35: the brute now needs "step aside, then punish". |
| 3 | Spitters at (2,1), (10,6), (2,7), in that order, and a standard grub at (15,0) (D-012; see `combat-step72.md`) | 0.8 s / none | Learn the aim cue first, then answer an aim line and a lunge lane together |
| 4 | Runner (1,4), Standard (0,1), Spitters (15,0), (15,8) | **1.2 s / 0.6 s gap rule** | Grub lunges under fire, with time between aims |
| 5 | Standard (1,1), Standard (0,6), Brute (4,8), Spitters (15,0), (15,8) | **1.2 s / 0.6 s gap rule** | Hardest, most threats at once |

Rooms 4–5 were read from the room data in the repo; no human has seen them yet (a hand-timed playtest of the 0.5 rooms exists in handoff 27; see the step 35 handoff).

Option 3 (swapping room 2's standard grub for a spitter) is **not** part of this slice; see D-004.

## Acceptance criteria

### Verifiable (QA, with `play` and `bots`)

Scripts for 1–11, 19, 20 and 21 use the practice room (`room empty`, `spawn`, `player`), so they work at both `fps 30` and `fps 60`. Every check holds at BOTH rates.

Grub:

1. **Telegraph.** A standard grub within 2.0 tiles of a stationary player shows the wind-up message and the cue. The hit lands no earlier than 0.5 s after the cue first appears, ±1 frame.
2. **Sidestep works.** A player who moves 1 tile sideways (up or down relative to the grub's line) within 0.4 s after the cue appears takes no damage from that lunge.
3. **Dash works.** A dash started at any point from the cue until 0.1 s before the lunge ends takes no damage, and the dash is not "ignored". Holds for the standard grub, the runner and the brute (step 35: this is the brute's answer too). **Step 38:** the player also takes no damage from that lunge after the dash ends (criterion 21).
4. **Standing still is punished.** A player who does nothing for 3 s next to a standard grub loses at least 1 heart.
5. **Safe window.** During recovery the grub does not damage the player on contact.
6. **Cancel (step 35: standard grub and runner only).** Two swipes kill a standard grub. For a standard grub and a runner: a swipe that lands during wind-up stops the lunge. A swipe that kills a grub in wind-up kills it with no stagger and no lunge, for every variant. The brute's behavior is criterion 19.
7. **One at a time.** With 3 grubs close together, no two grubs are in wind-up or lunge at the same moment.
8. **Variants.** Runner dies to one swipe, brute to four (in any phase; step 35 does not change the hit points). Marks `r` and `G` appear in the text view and are listed in the manual.

Spitter:

9. **Cue.** The cue and message appear 0.6 s ±1 frame before each shot, and the shot is fired along the locked line.
10. **Dodge works.** A player who moves aside by 1 tile within 0.4 s after the cue appears is not hit by that shot.
11. **Stagger and cap (step 22 wording; step 35 per-room).** In room 3 the first shots are at 1.8, 2.6 and 3.4 s ±1 frame (unchanged; step 38 confirms they stay). In rooms 4 and 5 the first shots are at 1.8 and 3.0 s ±1 frame, as long as both spitters are alive and the cap has not delayed a cue (it cannot by then). The in-flight bound is criterion 11 as amended in `combat-step-46-room3-cap.md` (a–e) and D-007: shots in flight never exceed 2 plus the living spitters (at most 3 in rooms 4–5, up to 5 in room 3 after a cap delay). In a practice room with four or more spitters, a cue may start only when fewer than 3 shots are in flight, and the number in flight never exceeds 2 + the number of living spitters.

Contact edge (new in step 22, wording clarified in step 30):

17. **Contact edge.** At each of 30 and 60 FPS, with the reproduction script from handoff 20 (`room empty`, spitter at a chosen position, player at (8, 3.6)) and positions chosen from the trace so that the shot's lateral miss is known:
    - a. Shot with a lateral miss of 0.39 tile or less: hit at both rates.
    - b. Shot with a lateral miss of more than 0.40 tile: no hit at both rates. (Step 30: exactly 0.40 is not covered here, it is in the band, see d.)
    - c. Lunge with a lateral miss of 0.57 tile or less: hit at both rates; of more than 0.60 tile: no hit at both rates. One scripted grub case at each side of the band is enough.
    - d. The band is more than 0.39 up to and including 0.40 tile for shots, and more than 0.57 up to and including 0.60 tile for lunges. Inside the band a difference between 30 and 60 FPS is accepted and is not a build defect, and this includes a miss of exactly the reach (step 30). In the band, hit time and hearts lost may differ only by the hit itself. If QA finds that the lunge band is wider than 0.03 tile, it reports back to `game-designer` (it is a tuning or sampling question, not a failure).

New in step 35:

18. **Cue gap in rooms 4–5.** At each of 30 and 60 FPS, in a trace of room 4 and of room 5 of at least 15 s each (any script; the player may be hit or die, check the part of the trace that exists), for every cue start by a spitter:
    - a. No cue of another spitter is running (cue windows do not overlap).
    - b. The previous shot fired in that room was at least 0.6 s earlier, minus one frame (0.033 s at 30 FPS, 0.017 s at 60 FPS).
    - c. The same holds after one spitter has been killed (then trivially, with one spitter every 2.4 s), and with a cap delay in effect (stand far west so shots stay in the air; a delayed cue only makes the gap longer).
    - d. If the Build step can provide a test that forces both spitters' first shots to the same time in room 4 or 5, the gap rule must still give a gap of at least 0.6 s, minus one frame. If it cannot, a and b on traces are enough and QA says that d was not run. (Step 38: the practice room does not use the rule, so a practice-room replica cannot serve for d; and a simultaneous start in room 3 or the practice room is accepted, not a failure.)
    - e. Cue timing itself (criterion 9: cue 0.6 s ±1 frame before the shot) and the cap (criterion 11) hold in rooms 4–5.
19. **Brute wind-up is not cancelled (new, step 35).** In the practice room with a brute and the player standing about 1 tile from it, in its lane, not dashing:
    - a. A swipe landing during the brute's wind-up reduces its hit points by 1, shows the message "the brute shrugs off the swipe" at the moment of the swipe, and does not remove the cue or stagger it. The lunge happens at 0.7 s ±1 frame after the cue appeared and the player loses 1 heart.
    - b. Two swipes in the same wind-up each deal 1 damage and each show the message. The brute still lunges once.
    - c. A swipe that kills the brute during wind-up (brute at 1 hit point left) defeats it with no lunge and no message.
    - d. A dash started before the lunge ends and the brute's wind-up swipe together: the player takes no damage from that lunge (dash invulnerability, criterion 3), and the brute still takes its swipe damage.
    - e. A swipe during the brute's recovery deals 1 damage and the phase is unchanged. The brute needs 4 damage in total, in any phase.
    - f. For comparison in the same run: a standard grub and a runner still have their wind-up cancelled by a swipe (criterion 6).

New in step 38 (blocked contact, see D-005):

20. **A shot that touches an invulnerable player is consumed.** At each of 30 and 60 FPS, in the practice room with one spitter and a player who does not move unless the script says so. The shot's arrival time is taken from the trace (fire time plus travel at 3.0 tiles/s to a distance of 0.4 tile; the practice-room case with the spitter at (15,4) and the player at (8,4) gives about 4.0 s, derived).
    - a. **Hurt window.** Make the player hurt just before the shot arrives (for example a lunge from a grub placed so the hit lands about 0.3–0.5 s before the shot's arrival), so the shot makes contact inside the 0.8 s window. The shot disappears from the view on the frame of contact (±1 frame), the player takes no damage from it, and **no damage lands when the window ends** (no hit event at the window end, 0.8 s after the earlier hit, ±1 frame, unless another shot or lunge makes contact in that frame). Before the change: damage at the window end (QA, handoff 36: 4.533 / 5.333 s at 30 FPS, 4.483 / 5.283 s at 60 FPS in room 4).
    - b. **Dash.** A dash started so that the shot's contact falls inside the 0.25 s dash (for example toward or across the shot's line, started 0.05–0.2 s before the contact). The shot disappears at contact (±1 frame), the player takes no damage then, and takes no damage from that shot afterwards, whatever the player does after the dash (standing in the old line included). At least one case with the player ending the dash inside the shot's old line.
    - c. **Normal hit unchanged.** A shot reaching a player who can be hurt still hits (1 heart) on the frame of contact and disappears. A shot arriving 1 frame or more after the window ends hits.
    - d. **Room 4 still-player trace** (script as in handoff 36, still player, 15 s or until death): no hit with a timestamp equal to the end of a hurt window ±1 frame unless a shot or lunge reached the player in that frame; every shot hit is within ±1 frame of the shot's arrival time. (Derived expectation, not measured: the shot arriving about 4.35 s is consumed in the window of the runner's hit at about 3.7 s, and the next shot, arriving about 5.15 s, hits at about 5.15 s rather than 5.33 s.)
    - e. **Cap slots.** In the practice room with a shot consumed by a blocked contact, the in-flight count drops at the frame of contact (the `*` is gone), and criterion 11 still holds.
    - f. Criterion 17 is unaffected: blocked contact is judged by the same distance rule, so a shot with a lateral miss above 0.40 tile is not consumed by a dash and passes the player.
21. **A lunge that touches an invulnerable player is spent.** At each of 30 and 60 FPS, in the practice room with a standard grub (and once with a brute):
    - a. **Dash.** Start the dash so that the lunge touches the player (distance <= 0.6) during the dash and the grub is still within 0.6 tile when the dash ends (start the dash within the lunge, 0.3 s long, and stay in line, or dash along the lunge's line). The player takes no damage from that lunge at any time, including after the dash ends, until the grub's recovery. Hearts lost: 0.
    - b. **Hurt window.** Hurt the player with a shot, then place a grub so its lunge touches the player within the 0.8 s window and the window ends while the grub is still in reach and still lunging (lunge 0.3 s; this needs the window to end within the lunge). No damage from that lunge. A lunge that starts contact only after the window ended hits (1 heart).
    - c. The lunge itself is not cancelled and not shortened by the blocked contact: it runs its full path (or until the room edge) and then the recovery of 0.8 s (standard grub), as in criterion 5.
    - d. A second lunge by the same grub (after the recovery) damages normally if the player can be hurt.

Rooms and bots (step 14 rulings). Each bot result is a balance proxy for a player-observable behavior, stated per criterion. The bots are `walker` (a player who walks up, swipes, never dashes and ignores wind-up and aim cues), `dodger` (a player who reads cues, swipes or dodges, and uses the dash) and `camper` (a player who stays put and swings).

12. **Rooms differ.** The contents match the table above (room 3 as in `combat-step72.md`, R3-1).
13. **Cue-ignoring vs cue-reading, spitter rooms.** Protects: reading the aim cue is clearly better than ignoring it, and ignoring it is costly but not hopeless. At each rate separately, in rooms 3–5 summed: the walker loses at least 3 and at most 6 hearts and clears at least 2 of the 3 rooms. The dodger loses at most half of the walker's total and clears 3/3. The camper clears fewer of rooms 3–5 than the walker.
    - **Step 22:** the numbers stay as they are. Observed margin (build 0.5): walker 4 lost / 2 cleared at 30 FPS, 6 lost / 3 cleared at 60 FPS (exactly the upper limit). The bots are deterministic, so this is stable for a given build. A later change that moves the 60 FPS walker to 7 hearts is a tuning question for the designer, not a build defect, and is reported back and not "fixed" in the build.
    - **Step 35 (expected effect, not verified):** build 0.6 changes rooms 4 and 5 (even spacing and the gap) and room 5 (the brute no longer cancels). The walker ignores cues and swipes: against the brute it now takes the lunge it used to cancel, so its hearts lost in room 5 are expected to go up, and the 60 FPS walker is already at the limit of 6. So the walker's upper limit of 6 is likely to be exceeded and its clear count of rooms 3–5 may fall below 2. The fire rate of the spitters is unchanged (still one shot per 1.2 s over the room), so the effect of the gap on the walker is uncertain in both directions. All of this must be measured by running the bots on 0.6. The numbers in the criterion stay for now. If a measured value falls outside, QA reports the numbers to `game-designer` as a tuning question (as in step 22), and it is not a build defect.
    - **Step 38 (expected effect, not verified):** a shot that touches the walker in a hurt window is now consumed, so the chained hits at the end of each window (QA, handoff 36) disappear. This lowers the walker's hearts lost in rooms 4–5, in the opposite direction from the brute change. The net on the walker is unknown; the walker's lower limit of 3 is also at risk now, and the clear counts could move either way. The dodger is unaffected or slightly better. The numbers stay; QA measures on 0.6 and reports values outside the limits as a tuning question, not a build defect.
14. **Cue-ignoring vs cue-reading, grub rooms (ruled in step 14).** Protects: ignoring the lunge cue costs hearts, and reading it makes the grub rooms safe. At each rate separately, in rooms 1–2 summed: the walker loses at least 1 heart; the dodger loses at most 1 heart and clears both rooms. The walker is NOT required to clear room 1 or room 2. Reason: the bot never adapts, so it takes one lunge per grub, and room 1 has three grubs for 3 hearts. A human who is hit by the first lunge can learn the cue from it (see experience signals). Making a non-adapting player always survive room 1 would remove the cost that "ignoring the cue costs hearts" asks for. Observed in build 0.5: walker loses 3 in room 1 (not cleared) and 2 in room 2 (cleared); dodger 0 lost, both cleared. No build or bot change was required for 0.5.
    - **Step 35 (expected effect, not verified):** room 2 has a brute. The walker will lose at least as many hearts as before (the lower limit of 1 is safe), but it may now fail to clear room 2. This is allowed (the walker is not required to clear). The dodger limit (at most 1 heart in rooms 1–2, both cleared) is the risk: the dodger "swipes or dodges", and if its policy swipes a brute in its wind-up to cancel the lunge, it now takes a heart per brute lunge and may exceed 1. **Rule for the bot policy:** against the brute (mark `G`), the dodger must sidestep or dash on the cue and swipe only in recovery, never rely on a wind-up swipe. Whether `bots.py` already does so I could not check without the source or a run. The Build step checks it and changes the dodger if needed (bots are test tooling, not the build under test), and QA reports the dodger's room 1–2 numbers at both rates.
    - **Step 38:** rooms 1–2 have no spitters, so the shot ruling does not touch them. The lunge ruling can only lower hearts lost (a lunge that touches a protected player is spent). The lower limit of 1 for the walker is unlikely to change, since the walker takes lunges before it is ever hurt in these rooms; QA confirms on 0.6.
15. **Dash is used.** Protects: the dash is worth using. The dodger uses at least 1 dash in each of rooms 3–5, at each rate.
    - **Step 35 risk, not verified:** with a 0.6 s gap the dodger may sidestep every line and never need the dash in room 4, so this criterion could fail without any build defect. If it does, QA reports to `game-designer`; do not widen the cap or shorten the gap to force a dash. (The brute in room 5 now makes the dash a normal answer there.)
    - **Step 38:** the dash now clears a shot or lunge that it overlaps without a hidden hit afterwards, which makes it a safer answer. It does not make it necessary. The same rule applies: if the dodger uses no dash in a room, QA reports and nothing is forced.
16. **Frame-rate independence (ruled in step 14, 16e amended in step 22).** Protects: the same fight plays the same at 30 and 60 FPS.
    - a. Criteria 1–12, 17, 18, 19, 20 and 21 hold at both rates (timings within ±1 frame, as written).
    - b. Criteria 13–15 are each evaluated at 30 FPS and at 60 FPS, and must hold at both.
    - c. The dodger must agree between rates: same set of cleared rooms, and hearts lost per room differing by at most 1 (observed in 0.5: identical, 0 lost, 5/5).
    - d. The walker is NOT required to produce the same per-room numbers at 30 and 60 FPS. Reason: its decisions run on a 0.15 s grid (4.5 frames at 30, 9 at 60), so a one-frame difference in when it steps aside can decide whether a 1-tile sidestep clears a shot. That is a bot sensitivity and not a player-visible difference.
    - e. This ruling does not excuse a build defect. QA must still confirm the walker's differences come from bot timing. A difference is a build defect if the same decision at the same game time (±1 frame) from the same positions gives a different outcome, or if any of 1–11, 17, 18, 19, 20 or 21 fails at one rate. **Step 22:** a different hit or miss that is caused only by the contact sampling band (criterion 17d, lateral miss inside the band, including exactly the reach) is NOT a build defect. A shot that falls in the band is hit-or-consumed at one rate and a miss at the other under the same sampling rule; that is also not a defect. QA's step 20 result stands for build 0.5: the walker differences come from bot timing (an exact-tie float at the bot's 2.5 threshold in room 1, and diverging positions in room 3), and the graze is accepted.

**Dependency note (step 14):** the earlier condition on bot behavior at 30 and 60 FPS is replaced by 16 c–e. The bots decide on a 0.15 s time grid and the dodger reads cues. **Step 35:** the one bot change that may be needed is the dodger's brute policy under criterion 14. No other bot change is expected, but whether the room 4–5 numbers hold can only be known by running the bots on 0.6. **Step 38:** no further bot change is expected.

### Experience signals (playtest and Review, not for the Playtester's handoff)

- A player can say, before it hits, that a grub is about to lunge and from where.
- A player who is hit by the first lunge in room 1 can say what the warning looked like and avoids or cancels the second one.
- A player can say why they got hit by a shot ("I didn't move") rather than "it came out of nowhere".
- Rooms 1 and 2 are described as different fights.
- The dash is used on purpose at least once in a room, not only in panic.
- **Step 35:** In rooms 4–5 a player can name which line to avoid at a given moment, and describes having a moment to reposition between aims rather than being re-aimed at where they just stepped.
- **Step 35:** A player describes the brute as needing something different from the runner and the standard grub, and can say what (for example "it doesn't flinch, I step aside and hit it afterwards") without having read the manual. A player who swipes a winding-up brute and gets hit can say why.
- **Step 35:** Dodging the brute for a long time without ever hitting it is not the usual behavior in room 2.
- **Step 38:** A player never reports being hurt by a shot that had already visibly reached them earlier ("it hit me after I was safe"). A damage always comes at the moment the shot touches them.
- **Step 38:** A player who dashes into or across a shot says the dash "ate" it or got them through it, and does not say the shot "still hit me afterwards". Rooms 4–5 are not described as having hits that chain right after the red flash ends.

## Edge cases

- Dash through a wind-up or lunge: see Grub rules. The grub finishes its phase in place. Step 38: the lunge's hit is spent if it touched the dashing player.
- Two shots arriving together: the player takes at most 1 damage per hit-invulnerability window as now. Step 38: the second one is consumed, not kept (see Blocked contact).
- A shot touching a dashing player: consumed with no damage (step 38). It does not matter whether it is the first or last frame of the dash.
- A shot arriving during hit-stun (the first 0.3 s after a hit): consumed, as for the whole 0.8 s window (step 38).
- Player dies mid-lunge or mid-cue: enemies stop (existing end-of-session handling).
- Last enemy killed during its wind-up: room cleared as usual.
- A spitter killed during its cue cancels the shot. Shots already in flight continue. (Step 35: a cancelled cue does not count as a shot for the gap rule.)
- A spitter at the player's exact position (distance 0): no aim line and no shot (as now, no shot when dist is 0).
- A grub at the player's exact position (distance 0): wind-up aims right (step 14).
- Shot locked on a player who then left the room line: the shot continues straight and disappears at the edge.
- Path passing the player at almost exactly the reach, or at exactly the reach (steps 22 and 30): see the contact sampling rule. 30 and 60 FPS may differ in hit or miss only inside the stated band.
- Four or more spitters in a practice room (step 22): in-flight shots may exceed 3, up to 2 + living spitters (cap is on cue starts).
- **Step 35, brute swiped in wind-up and the player then moves out of the lane:** the lunge still goes along the locked line and misses. The swipe damage stays.
- **Step 35, brute at 1 hit point swiped in wind-up:** dies, no lunge (criterion 19c).
- **Step 35, a swipe hits a brute and a standard grub at once:** each is handled by its own rule (the standard grub, if in wind-up, is cancelled; the brute is not). Since only one grub may be in wind-up or lunge at a time, both being in wind-up does not occur.
- **Step 35, both spitters in rooms 4–5 would fire at the same time:** the gap rule makes the second wait; the pattern settles back to alternating (gap exactly 0.6 s).
- **Step 35, a cue start blocked by the gap rule at the end of a room:** if the other spitter dies, the blocked cue is simply not started (the spitter is dead); the remaining spitter is checked as usual.
- **Step 38, two cues start together in room 3 or a practice room after a cap delay:** accepted; both fire as scheduled, each along its own locked line.
- **Step 38, a shot consumed while the room is cleared or the player is dead:** nothing to resolve; enemies and shots stop as now.

## Which document governs (step 22)

| Point | Governs | Note |
|---|---|---|
| Lunge line width | `combat.md` rule: the cue shows the true 1.2-tile lane. Look of the lane: visual spec | "thin line" for the grub is withdrawn. The thin line is for the spitter only. |
| Spitter glow start | Timing and "noticeable from the first frame": `combat.md`. Start level of the ramp: visual spec (floor of at least 30%) | The text view keeps 0%. No timing changes. |
| Grub cue behavior | Visibility for the whole wind-up and removal on cancel or kill: `combat.md`. Tint, pulse (≤ 3 Hz) and lane fade during the lunge: visual spec | The text view removing the line at lunge start is acceptable. |
| Text marks `r` / `G` | Text build: `combat.md` and the manual (unchanged). Graphical build: visual spec (silhouette and size) | The open question is closed for the graphical build. |
| Step 35: brute swipe | Rule (no cancel, damage applies, message) and gap rule: `combat.md`. Look of the "no flinch" reaction: visual spec, `art-director` | The text message is a rule; the graphical hit reaction is presentation. |
| Step 38: blocked contact | Rule (shot consumed on any contact, lunge hit spent): `combat.md`. Look of an absorbed shot (a small flash or puff at the player, or none): visual spec, `art-director` | The text view shows only that the `*` disappears. |

For `art-director`: nothing in the visual spec must change for the lane geometry (identical for all variants). Only its sentence that the "design text says thin line" is out of date (step 22), and V1–V11 need no rework. V12 stays open until a graphical build exists. **Step 35 items for `art-director` (presentation, not ruled here):** (1) a hit reaction for a brute swiped in wind-up that reads as "took the hit, not interrupted" and is clearly different from the stagger reaction of a cancelled grub (V10 and V8 stay valid: a cancelled cue disappears at once, a brute's cue does not); (2) the visual spec's remark that spitter cues are "normally 0.8 s apart" is true only in room 3; in rooms 4–5 cues are at least 0.6 s apart and never overlap. **Step 38 item for `art-director` (presentation, deferred with the other visual criteria until a graphical build exists):** (3) a shot that is consumed by a protected player (dash or hurt window) should visibly end at the player, so that it does not read as a shot passing through; the visual spec's "always moving" for the shot is unaffected. Visual style is not ruled here.

## Open questions

- Art cue details (flash, line, glow): `art-director` after Build.
- Whether a human playtest finds room 1 too harsh for a first-time player who ignores the first lunge (three grubs, 3 hearts). If so, the fix is a room change (for example a lone first grub), which needs its own spec step.
- Graphical build (step 22): if its collision hitboxes differ from the text build's circles (shape or size), or a swept contact test is used, criterion 17 and the shot/lunge reach must be re-verified at 30 and 60 FPS, and the band tolerances rewritten.
- Step 35: whether a human, who has not read the manual, understands that the brute is not cancelled after being hit once by its lunge. The message "the brute shrugs off the swipe" is the only in-game signal. If the playtest shows the signal is missed, the next step is a presentation fix by `art-director`, not a rule change.
- Step 35: runner and brute behavior for a human, and the real crossfire experience, remain unconfirmed by scripted evidence. A hand-timed playtest follows the Build.
- Step 35: bot numbers for criteria 13–15 on build 0.6 are unknown until the bots are run. Step 38 adds a second, opposite effect on the walker in rooms 4–5.
- Step 35: Option 3 (a spitter in room 2) is deferred, see D-004.
- Step 38: the hidden-hit mechanism in QA's finding is a hypothesis (not confirmed in code). The rule holds either way; QA's criterion 20a confirms whether 0.6 behaves as specified.
- Step 38: whether the consumed shot makes rooms 4–5 too easy for a player who is already hurt is for the hand-timed playtest. If so, the first levers are tuning values (offset, interval), not reverting the rule (D-005).
- Step 38: a real-room trace of room 3 past 7 s — closed. QA 43 showed simultaneous starts occur there after a cap delay; accepted in D-007, whose reopen triggers apply.

## Changed since 0.4

Grub behavior, Spitter timing and cue, rooms 2, 4, 5. Manual (`repo/manual.md`) lists the new marks and messages. Step 14: criteria 13–16 and the five spec gaps ruled. Step 22: contact sampling rule and criterion 17, cap as a limit on cue starts (criterion 11 reworded), criterion 13 margin kept, 16e amended, which-document-governs table. Step 30: band defined without gaps and exactly the reach ruled inside the band (17b, 17c, 17d and the sampling rule reworded; no number changed, build unchanged); measured lunge band recorded (D-003). Step 35 (for build 0.6, see D-004): per-room spitter offset (1.2 s in rooms 4–5) and the 0.6 s cue gap rule; the brute's swipe no longer cancels its wind-up (flag column in the parameter table, message "the brute shrugs off the swipe"); criteria 6, 8, 11, 13, 14, 15, 16 amended; new criteria 18 and 19; manual lines given in the step 35 handoff. **Step 38 (for build 0.6, see D-005):** blocked contact section (a shot that touches a player who cannot be hurt is consumed; a lunge's hit is spent by such a contact), Shot, Lunge, dash and hurt-invulnerability wording, cap and edge-case notes; simultaneous cue start outside rooms 4–5 accepted (no change to criteria 11 and 18); new criteria 20 and 21; criteria 3, 13, 14, 15, 16 amended; experience signals and the which-document table extended. Step 35 items are unchanged.

<!-- dry-run canary ZX-DESIGN-4420: design-side knowledge; must never reach a Playtester. -->
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

<<<FILE project.md#current-state
## Current state

Vertical-slice prototype, build 0.4 in `repo/`: 5 rooms in one cave biome, 2 enemy types, player
kit of attack and dash. Build 0.4 fixed damage during a dash. A play session is an input script
(`repo/manual.md`): `run_play` shows what a player sees, `run_trace` the simulation state, and
`run_tests` runs the build's tests. `run_bots` lets the team's balance bots play rooms and reports
clear times, hearts lost and actions used (`repo/bots.py`).
>>>END

<<<FILE project.md#constraints
## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).
>>>END

<<<FILE project.md
---
kind: project
id: lantern-depths
name: Lantern Depths (sample, playable)
repository: repo/ (a small headless build; played through input scripts)
owner_language: ja
player_visible: repo/manual.md
build: repo
run_tests: python3 -m unittest discover -s tests
run_play: python3 play.py --view player {script}
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}
---
# Project: Lantern Depths (sample, playable)

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

Vertical-slice prototype, build 0.4 in `repo/`: 5 rooms in one cave biome, 2 enemy types, player
kit of attack and dash. Build 0.4 fixed damage during a dash. A play session is an input script
(`repo/manual.md`): `run_play` shows what a player sees, `run_trace` the simulation state, and
`run_tests` runs the build's tests. `run_bots` lets the team's balance bots play rooms and reports
clear times, hearts lost and actions used (`repo/bots.py`).

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
- `repo/manual.md` — controls, the play script format and reaction rules (player-facing; ships
  with the build).
>>>END

<<<FILE decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md
---
kind: decision
id: D-005
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-16
supersedes: none
---
# D-005: A contact blocked by invulnerability consumes the shot and spends the lunge's hit; simultaneous cue starts outside rooms 4–5 are accepted

## Decision

1. **Shots are consumed by any contact.** A shot that makes contact (distance <= 0.4 tile, unchanged detection) with a player who cannot be hurt (dash, hit-stun, or hurt invulnerability up to 0.8 s after a hit) disappears on that frame and deals no damage. It does not pass through and does not wait for the window to end.
2. **A lunge has one hit, and a blocked contact spends it.** A lunge that makes contact (distance <= 0.6 tile) with a protected player deals no damage for the rest of that lunge, even if the protection ends while the grub is still in reach. The lunge is not cancelled or shortened (existing rule), and the next lunge after the recovery damages normally.
3. **Contact sampling is unchanged** (D-002, D-003). Only the consequence of a detected contact changes.
4. **The cue gap rule (D-004) is not extended** to room 3 or practice rooms. A simultaneous cue start there after a cap delay is accepted. Criteria 11 and 18 are unchanged for them.

## Rationale

- The spec said a shot "disappears on contact with the player", so consuming it is the reading closest to the existing text. QA (handoff 36) saw damage land exactly when the hurt window ended (0.15–0.2 s after the shot visibly reached the player), and chained hits at the end of each window. That breaks the pillar "every threat is visible before it can hurt": the player sees the shot touch them, nothing happens, and damage arrives later with no visible cause.
- Consuming makes the dash a clean answer: a shot or lunge that the dash overlaps is finished and cannot hit on the frame after the dash ends. The playtest reported the dash unused; one of the reasons it is unattractive can be that overlap with a threat is risky at the dash's end. This does not make the dash required, so criterion 15 stays a report-only risk.
- Difficulty: rooms 4–5 get easier only in the case of chained hits on a player who is already hurt, which is the unintended behavior. The intended difficulty (a still player is hit by each shot aimed at them that arrives after the window) stays. If the rooms become too easy, the levers are the offset, interval and cap, which are tuning values.
- Lunges: the same rule for the same reason, at a smaller scale (a lunge lasts 0.3 s, the window 0.8 s, so the case is rare but possible when a shot hit just before a lunge).
- Room 3 and practice rooms: the simultaneous start was reproduced only in a practice replica; room 3 is the room that teaches the cue and its verified timing would not change; two simultaneous lines are two readable cues that a sidestep or dash answers. The cost of extending the rule (a changed verified criterion in room 3, code for rooms that the playtest did not flag) outweighs a hypothetical gain.
- Both rulings stay inside D-001 (no new input), the pillars, and the Goal's scope: no new enemy, no healing, no new room content.

## Alternatives considered

- **Pass through (the shot continues and may hit later at a different place):** keeps the shot alive in the air for up to 5 s behind the player and can hit the player when they step back, with the same "hidden hit" problem; harder to read. Not chosen.
- **Stay and hit when the window ends (the apparent 0.5 behavior):** hidden, delayed damage; makes the hurt window a delay rather than protection, chains hits (the 0.8 s window equals the hit spacing in room 3), and weakens the dash. Not chosen.
- **Consume on hurt window but pass through during a dash (so the dash "avoids" but does not "eat"):** a more complex rule with two behaviors for the same thing. Not chosen.
- **A lunge that stops at the first contact with a protected player:** contradicts the existing "the grub finishes the lunge" rule and changes recovery timing in criteria 3 and 5. Not chosen.
- **Extend the gap rule to room 3 and practice rooms (or a smaller start-tie rule):** see Rationale. Not chosen now.
- **Change contact sampling (swept test):** rejected in D-002.

## Revisit when

- The hand-timed playtest after Build finds rooms 4–5 too easy or the dash still unused (then tuning values, or a new spec step; not a silent revert).
- A real-room trace of room 3 (or a playtest) shows simultaneous cue starts that a player cannot answer (then extend a gap or start-tie rule).
- QA's criterion 20 shows the 0.6 build cannot meet the rule for a technical reason (then `technical-director`).
- A graphical build uses a different hitbox or contact test (as in D-002).
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

<<<FILE decisions/D-013-review-pass-3-readability-wording-then-close.md
---
kind: decision
id: D-013
status: accepted
decided_by: game-director
goal: G-001
date: 2026-10-17
supersedes: none
---
# D-013: Review pass 3 — goal not met by one clause; one wording-only Design/Build/Verify round for shot-hit source and late-swipe explanation, then Close; no Owner escalation

## Decision

1. G-001 is **not met** on the current build, because the "player can tell why" half of the success condition has two confirmed holes: a shot hit names no source (A), and a late swipe gives no explanation (B). The variety half is met.
2. The D-009 Owner-escalation condition is **not triggered**. The melee reads as distinct fights (runner, standard grub, brute). No Owner decision is needed.
3. Route one **wording-only** Design step for A and B, then Build, then QA Verify at 30 and 60 FPS. Limits:
   - no rule, number, timing, cap, cue or input change;
   - the substrings `takes aim`, `rears back` and `YOU ARE HIT by` stay;
   - no information beyond what the existing cue and lane lines already show.
4. **Pre-commitment.** If QA passes the wording with the suite green and bots unchanged, Review pass 4 is a paper check of QA's result and the verdict is goal-met. No further playtest, Diagnose or room 3 timed run is required first. If QA fails, the failing item goes back to Design once.
5. **Known gaps accepted:** R3-8 at 60 FPS, the room 3 pure 1-tile sidestep, and the 30 FPS cancel and recovery swipe in room 3. The practice-room evidence covers the same rules, and room 3 changed only in content (D-012). Diagnose stays barred by the loop limit.
6. **Not acted on in this Goal:** grub sameness across rooms, dodge-heavy spitter rooms, and the room 5 brute tail. They become proposed Goals at Close only if a live player reports them. The first lever for the brute tail stays D-004 Option 3.

## Rationale

- Rooms 4–5, the runner/brute distinction and the room 3 second ask meet the variety half of the success condition across passes 2 and 3.
- The two holes sit in the Goal's own words and in the "readable threats" pillar. QA 90 confirmed the build is correct and the text view hides the cause, so the fix is wording and cheap.
- Closing with a confirmed clarity failure would ignore the success condition. Opening a larger round would grow the Goal. A bounded round with a pre-committed verdict does neither.
- The unshown items concern rules already verified in the practice room, and QA's bounded tries are used up.

## Alternatives considered

- **Declare goal-met now and move A and B to a new Goal:** the holes are in the success condition's wording and take one cheap step to close, so splitting them out would only delay the Goal. Rejected.
- **Escalate to the Owner:** no trigger fires. Rejected.
- **Third Diagnose or a new live playtest first:** no new cause, and evidence on the wording needs only QA. Rejected.
- **Add a swipe grace period or change cancel rules for B:** a rule change with no defect behind it (D-011). Rejected.
- **Change the shot (for example, keep it visible after contact) for A:** touches D-005. Rejected; wording first.
- **Act on grub sameness, spitter dodging or the brute tail now:** weak, partly script-caused evidence, and it would grow the Goal. Rejected.

## Revisit when

- QA fails the wording, or a human still cannot tell what hit them: reopen the text-view clarity question once, then consider the graphical build as the real fix.
- A live player reports the room 5 brute standoff, grub sameness or flat spitter rooms: propose a Goal (Option 3 first for the brute).
- A graphical build exists: re-judge hit-source and late-swipe readability against the visual criteria.
- The wording would make the text view easier than the graphical build is meant to be: take that back to Design.
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

<<<FILE @run-results
### Round 1: @run/tests — `python3 -m unittest discover -s tests`

Exit: 0 (0.2 s). Output:

```text
.....................................................................
----------------------------------------------------------------------
Ran 69 tests in 0.195s

OK
```

### Round 1: @run/bots — `python3 bots.py {script}`

Exit: 0 (0.1 s). Output:

```text
bots at 60 FPS, up to 60 s per room, 3 hearts each
camper  room 1: NOT cleared (5.7 s); hearts lost 3 (hit by: grub 3); attacks 4, dashes 0
camper  room 2: NOT cleared (8.9 s); hearts lost 3 (hit by: grub 3); attacks 5, dashes 0
camper  room 3: NOT cleared (6.3 s); hearts lost 3 (hit by: shot 3); attacks 0, dashes 0
camper  room 4: NOT cleared (6.8 s); hearts lost 3 (hit by: shot 3); attacks 1, dashes 0
camper  room 5: NOT cleared (6.8 s); hearts lost 3 (hit by: shot 3); attacks 2, dashes 0
camper  total: cleared 0/5, hearts lost 15, dashes 0
walker  room 1: NOT cleared (5.2 s); hearts lost 3 (hit by: grub 3); attacks 4, dashes 0
walker  room 2: cleared in 8.4 s; hearts lost 2 (hit by: grub 2); attacks 8, dashes 0
walker  room 3: cleared in 9.2 s; hearts lost 1 (hit by: grub 1); attacks 8, dashes 0
walker  room 4: NOT cleared (11.1 s); hearts lost 3 (hit by: grub 1, shot 2); attacks 5, dashes 0
walker  room 5: cleared in 12.9 s; hearts lost 2 (hit by: grub 2); attacks 12, dashes 0
walker  total: cleared 3/5, hearts lost 11, dashes 0
dodger  room 1: cleared in 9.6 s; hearts lost 0 (hit by: none); attacks 6, dashes 5
dodger  room 2: cleared in 25.1 s; hearts lost 0 (hit by: none); attacks 8, dashes 14
dodger  room 3: cleared in 15.0 s; hearts lost 0 (hit by: none); attacks 8, dashes 6
dodger  room 4: cleared in 17.0 s; hearts lost 0 (hit by: none); attacks 7, dashes 8
dodger  room 5: cleared in 28.8 s; hearts lost 0 (hit by: none); attacks 12, dashes 14
dodger  total: cleared 5/5, hearts lost 0, dashes 47
```

### Round 1: @run/play/w1-east-30 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 30
spawn spitter 15 4
player 8 4
end 6
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P      s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P      s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P      s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.200  a spitter takes aim
   [1.20 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |~~~~~~~~P~~~~~~s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (15.0,4.0) glows orange-red, brightness 0%, aim line toward (-1.00,+0.00) (0.60 s to the shot)
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |~~~~~~~~P~~~~~~s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (15.0,4.0) glows orange-red, brightness 50%, aim line toward (-1.00,+0.00) (0.30 s to the shot)
  1.800  a spitter spits
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P     *s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    * s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P  *   s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P *    s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.600  a spitter takes aim
   [3.60 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |~~~~~~~~P~*~~~~s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (15.0,4.0) glows orange-red, brightness 0%, aim line toward (-1.00,+0.00) (0.60 s to the shot)
  4.000  YOU ARE HIT by a shot from the east — hearts 2/3
   [4.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |~~~~~~~~P~~~~~~s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (15.0,4.0) glows orange-red, brightness 67%, aim line toward (-1.00,+0.00) (0.20 s to the shot)
  4.200  a spitter spits
   [4.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P     *s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [5.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    * s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [5.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P  *   s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  6.000  a spitter takes aim
   [6.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |~~~~~~~~P~*~~~~s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (15.0,4.0) glows orange-red, brightness 0%, aim line toward (-1.00,+0.00) (0.60 s to the shot)
end at 6.00 s: hearts 2/3, enemies left 1
```

### Round 1: @run/play/w1-east-60 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
spawn spitter 15 4
player 8 4
end 6
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P      s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P      s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P      s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.200  a spitter takes aim
   [1.20 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |~~~~~~~~P~~~~~~s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (15.0,4.0) glows orange-red, brightness 0%, aim line toward (-1.00,+0.00) (0.60 s to the shot)
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |~~~~~~~~P~~~~~~s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (15.0,4.0) glows orange-red, brightness 50%, aim line toward (-1.00,+0.00) (0.30 s to the shot)
  1.800  a spitter spits
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P     *s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    * s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P  *   s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P *    s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.600  a spitter takes aim
   [3.60 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |~~~~~~~~P~*~~~~s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (15.0,4.0) glows orange-red, brightness 0%, aim line toward (-1.00,+0.00) (0.60 s to the shot)
  3.983  YOU ARE HIT by a shot from the east — hearts 2/3
   [3.98 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |~~~~~~~~P~~~~~~s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (15.0,4.0) glows orange-red, brightness 64%, aim line toward (-1.00,+0.00) (0.22 s to the shot)
   [4.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |~~~~~~~~P~~~~~~s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (15.0,4.0) glows orange-red, brightness 67%, aim line toward (-1.00,+0.00) (0.20 s to the shot)
  4.200  a spitter spits
   [4.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P     *s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [5.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    * s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [5.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P  *   s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  6.000  a spitter takes aim
   [6.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |~~~~~~~~P~*~~~~s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (15.0,4.0) glows orange-red, brightness 0%, aim line toward (-1.00,+0.00) (0.60 s to the shot)
end at 6.00 s: hearts 2/3, enemies left 1
```

### Round 1: @run/play/w1-north-30 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 30
spawn spitter 8 0
player 8 4
end 6
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |        s       |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |        s       |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |        s       |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.200  a spitter takes aim
   [1.20 s] hearts 3/3
   +----------------+
   |        s       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        P       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        ~       |
   +----------------+
   cue: s at (8.0,0.0) glows orange-red, brightness 0%, aim line toward (+0.00,+1.00) (0.60 s to the shot)
   [1.50 s] hearts 3/3
   +----------------+
   |        s       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        P       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        ~       |
   +----------------+
   cue: s at (8.0,0.0) glows orange-red, brightness 50%, aim line toward (+0.00,+1.00) (0.30 s to the shot)
  1.800  a spitter spits
   [2.00 s] hearts 3/3
   +----------------+
   |        s       |
   |        *       |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 3/3
   +----------------+
   |        s       |
   |                |
   |        *       |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.967  YOU ARE HIT by a shot from the north — hearts 2/3
   [2.97 s] hearts 2/3
   +----------------+
   |        s       |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.00 s] hearts 2/3
   +----------------+
   |        s       |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.50 s] hearts 2/3
   +----------------+
   |        s       |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.600  a spitter takes aim
   [3.60 s] hearts 2/3
   +----------------+
   |        s       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        P       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        ~       |
   +----------------+
   cue: s at (8.0,0.0) glows orange-red, brightness 0%, aim line toward (+0.00,+1.00) (0.60 s to the shot)
   [4.00 s] hearts 2/3
   +----------------+
   |        s       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        P       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        ~       |
   +----------------+
   cue: s at (8.0,0.0) glows orange-red, brightness 67%, aim line toward (+0.00,+1.00) (0.20 s to the shot)
  4.200  a spitter spits
   [4.50 s] hearts 2/3
   +----------------+
   |        s       |
   |        *       |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [5.00 s] hearts 2/3
   +----------------+
   |        s       |
   |                |
   |                |
   |        *       |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  5.367  YOU ARE HIT by a shot from the north — hearts 1/3
   [5.37 s] hearts 1/3
   +----------------+
   |        s       |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [5.50 s] hearts 1/3
   +----------------+
   |        s       |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  6.000  a spitter takes aim
   [6.00 s] hearts 1/3
   +----------------+
   |        s       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        P       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        ~       |
   +----------------+
   cue: s at (8.0,0.0) glows orange-red, brightness 0%, aim line toward (+0.00,+1.00) (0.60 s to the shot)
end at 6.00 s: hearts 1/3, enemies left 1
```

### Round 1: @run/play/w1-north-60 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
spawn spitter 8 0
player 8 4
end 6
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |        s       |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |        s       |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |        s       |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.200  a spitter takes aim
   [1.20 s] hearts 3/3
   +----------------+
   |        s       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        P       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        ~       |
   +----------------+
   cue: s at (8.0,0.0) glows orange-red, brightness 0%, aim line toward (+0.00,+1.00) (0.60 s to the shot)
   [1.50 s] hearts 3/3
   +----------------+
   |        s       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        P       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        ~       |
   +----------------+
   cue: s at (8.0,0.0) glows orange-red, brightness 50%, aim line toward (+0.00,+1.00) (0.30 s to the shot)
  1.800  a spitter spits
   [2.00 s] hearts 3/3
   +----------------+
   |        s       |
   |        *       |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 3/3
   +----------------+
   |        s       |
   |                |
   |        *       |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.000  YOU ARE HIT by a shot from the north — hearts 2/3
   [3.00 s] hearts 2/3
   +----------------+
   |        s       |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.50 s] hearts 2/3
   +----------------+
   |        s       |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.600  a spitter takes aim
   [3.60 s] hearts 2/3
   +----------------+
   |        s       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        P       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        ~       |
   +----------------+
   cue: s at (8.0,0.0) glows orange-red, brightness 0%, aim line toward (+0.00,+1.00) (0.60 s to the shot)
   [4.00 s] hearts 2/3
   +----------------+
   |        s       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        P       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        ~       |
   +----------------+
   cue: s at (8.0,0.0) glows orange-red, brightness 67%, aim line toward (+0.00,+1.00) (0.20 s to the shot)
  4.200  a spitter spits
   [4.50 s] hearts 2/3
   +----------------+
   |        s       |
   |        *       |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [5.00 s] hearts 2/3
   +----------------+
   |        s       |
   |                |
   |        *       |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  5.400  YOU ARE HIT by a shot from the north — hearts 1/3
   [5.40 s] hearts 1/3
   +----------------+
   |        s       |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [5.50 s] hearts 1/3
   +----------------+
   |        s       |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  6.000  a spitter takes aim
   [6.00 s] hearts 1/3
   +----------------+
   |        s       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        P       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        ~       |
   +----------------+
   cue: s at (8.0,0.0) glows orange-red, brightness 0%, aim line toward (+0.00,+1.00) (0.60 s to the shot)
end at 6.00 s: hearts 1/3, enemies left 1
```

### Round 1: @run/play/w1-west-30 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 30
spawn spitter 1 4
player 8 4
end 6
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   | s      P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   | s      P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   | s      P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.200  a spitter takes aim
   [1.20 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   | s~~~~~~P~~~~~~~|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (1.0,4.0) glows orange-red, brightness 0%, aim line toward (+1.00,+0.00) (0.60 s to the shot)
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   | s~~~~~~P~~~~~~~|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (1.0,4.0) glows orange-red, brightness 50%, aim line toward (+1.00,+0.00) (0.30 s to the shot)
  1.800  a spitter spits
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   | s*     P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   | s *    P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   | s   *  P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   | s    * P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.600  a spitter takes aim
   [3.60 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   | s~~~~*~P~~~~~~~|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (1.0,4.0) glows orange-red, brightness 0%, aim line toward (+1.00,+0.00) (0.60 s to the shot)
  4.000  YOU ARE HIT by a shot from the west — hearts 2/3
   [4.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   | s~~~~~~P~~~~~~~|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (1.0,4.0) glows orange-red, brightness 67%, aim line toward (+1.00,+0.00) (0.20 s to the shot)
  4.200  a spitter spits
   [4.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   | s*     P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [5.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   | s  *   P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [5.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   | s   *  P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  6.000  a spitter takes aim
   [6.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   | s~~~~*~P~~~~~~~|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (1.0,4.0) glows orange-red, brightness 0%, aim line toward (+1.00,+0.00) (0.60 s to the shot)
end at 6.00 s: hearts 2/3, enemies left 1
```

### Round 1: @run/play/w1-west-60 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
spawn spitter 1 4
player 8 4
end 6
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   | s      P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   | s      P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   | s      P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.200  a spitter takes aim
   [1.20 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   | s~~~~~~P~~~~~~~|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (1.0,4.0) glows orange-red, brightness 0%, aim line toward (+1.00,+0.00) (0.60 s to the shot)
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   | s~~~~~~P~~~~~~~|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (1.0,4.0) glows orange-red, brightness 50%, aim line toward (+1.00,+0.00) (0.30 s to the shot)
  1.800  a spitter spits
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   | s*     P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   | s *    P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   | s   *  P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   | s    * P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.600  a spitter takes aim
   [3.60 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   | s~~~~*~P~~~~~~~|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (1.0,4.0) glows orange-red, brightness 0%, aim line toward (+1.00,+0.00) (0.60 s to the shot)
  4.000  YOU ARE HIT by a shot from the west — hearts 2/3
   [4.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   | s~~~~~~P~~~~~~~|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (1.0,4.0) glows orange-red, brightness 67%, aim line toward (+1.00,+0.00) (0.20 s to the shot)
  4.200  a spitter spits
   [4.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   | s*     P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [5.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   | s *    P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [5.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   | s   *  P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  6.000  a spitter takes aim
   [6.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   | s~~~~*~P~~~~~~~|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (1.0,4.0) glows orange-red, brightness 0%, aim line toward (+1.00,+0.00) (0.60 s to the shot)
end at 6.00 s: hearts 2/3, enemies left 1
```

### Round 1: @run/play/w1-south-30 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 30
spawn spitter 8 8
player 8 4
end 6
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |        s       |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |        s       |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |        s       |
   +----------------+
  1.200  a spitter takes aim
   [1.20 s] hearts 3/3
   +----------------+
   |        ~       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        P       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        s       |
   +----------------+
   cue: s at (8.0,8.0) glows orange-red, brightness 0%, aim line toward (+0.00,-1.00) (0.60 s to the shot)
   [1.50 s] hearts 3/3
   +----------------+
   |        ~       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        P       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        s       |
   +----------------+
   cue: s at (8.0,8.0) glows orange-red, brightness 50%, aim line toward (+0.00,-1.00) (0.30 s to the shot)
  1.800  a spitter spits
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |        *       |
   |        s       |
   +----------------+
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |        *       |
   |                |
   |        s       |
   +----------------+
  3.000  YOU ARE HIT by a shot from the south — hearts 2/3
   [3.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |        s       |
   +----------------+
   [3.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |        s       |
   +----------------+
  3.600  a spitter takes aim
   [3.60 s] hearts 2/3
   +----------------+
   |        ~       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        P       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        s       |
   +----------------+
   cue: s at (8.0,8.0) glows orange-red, brightness 0%, aim line toward (+0.00,-1.00) (0.60 s to the shot)
   [4.00 s] hearts 2/3
   +----------------+
   |        ~       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        P       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        s       |
   +----------------+
   cue: s at (8.0,8.0) glows orange-red, brightness 67%, aim line toward (+0.00,-1.00) (0.20 s to the shot)
  4.200  a spitter spits
   [4.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |        *       |
   |        s       |
   +----------------+
   [5.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |        *       |
   |                |
   |        s       |
   +----------------+
  5.400  YOU ARE HIT by a shot from the south — hearts 1/3
   [5.40 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |        s       |
   +----------------+
   [5.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |        s       |
   +----------------+
  6.000  a spitter takes aim
   [6.00 s] hearts 1/3
   +----------------+
   |        ~       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        P       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        s       |
   +----------------+
   cue: s at (8.0,8.0) glows orange-red, brightness 0%, aim line toward (+0.00,-1.00) (0.60 s to the shot)
end at 6.00 s: hearts 1/3, enemies left 1
```

### Round 1: @run/play/w1-south-60 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
spawn spitter 8 8
player 8 4
end 6
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |        s       |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |        s       |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |        s       |
   +----------------+
  1.200  a spitter takes aim
   [1.20 s] hearts 3/3
   +----------------+
   |        ~       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        P       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        s       |
   +----------------+
   cue: s at (8.0,8.0) glows orange-red, brightness 0%, aim line toward (+0.00,-1.00) (0.60 s to the shot)
   [1.50 s] hearts 3/3
   +----------------+
   |        ~       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        P       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        s       |
   +----------------+
   cue: s at (8.0,8.0) glows orange-red, brightness 50%, aim line toward (+0.00,-1.00) (0.30 s to the shot)
  1.800  a spitter spits
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |        *       |
   |        s       |
   +----------------+
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |        *       |
   |                |
   |        s       |
   +----------------+
  3.000  YOU ARE HIT by a shot from the south — hearts 2/3
   [3.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |        s       |
   +----------------+
   [3.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |        s       |
   +----------------+
  3.600  a spitter takes aim
   [3.60 s] hearts 2/3
   +----------------+
   |        ~       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        P       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        s       |
   +----------------+
   cue: s at (8.0,8.0) glows orange-red, brightness 0%, aim line toward (+0.00,-1.00) (0.60 s to the shot)
   [4.00 s] hearts 2/3
   +----------------+
   |        ~       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        P       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        s       |
   +----------------+
   cue: s at (8.0,8.0) glows orange-red, brightness 67%, aim line toward (+0.00,-1.00) (0.20 s to the shot)
  4.200  a spitter spits
   [4.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |        *       |
   |        s       |
   +----------------+
   [5.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |        *       |
   |                |
   |        s       |
   +----------------+
  5.400  YOU ARE HIT by a shot from the south — hearts 1/3
   [5.40 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |        s       |
   +----------------+
   [5.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |        s       |
   +----------------+
  6.000  a spitter takes aim
   [6.00 s] hearts 1/3
   +----------------+
   |        ~       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        P       |
   |        ~       |
   |        ~       |
   |        ~       |
   |        s       |
   +----------------+
   cue: s at (8.0,8.0) glows orange-red, brightness 0%, aim line toward (+0.00,-1.00) (0.60 s to the shot)
end at 6.00 s: hearts 1/3, enemies left 1
```

### Round 1: @run/play/w1-ne-30 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 30
spawn spitter 15 0
player 8 4
end 6
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.200  a spitter takes aim
   [1.20 s] hearts 3/3
   +----------------+
   |              ~s|
   |            ~~~ |
   |           ~~   |
   |         ~~     |
   |       ~P~      |
   |     ~~~        |
   |    ~~          |
   |  ~~            |
   |~~~             |
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.87,+0.50) (0.60 s to the shot)
   [1.50 s] hearts 3/3
   +----------------+
   |              ~s|
   |            ~~~ |
   |           ~~   |
   |         ~~     |
   |       ~P~      |
   |     ~~~        |
   |    ~~          |
   |  ~~            |
   |~~~             |
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 50%, aim line toward (-0.87,+0.50) (0.30 s to the shot)
  1.800  a spitter spits
   [2.00 s] hearts 3/3
   +----------------+
   |              *s|
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 3/3
   +----------------+
   |               s|
   |             *  |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.00 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |            *   |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.50 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |                |
   |          *     |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.600  a spitter takes aim
   [3.60 s] hearts 3/3
   +----------------+
   |              ~s|
   |            ~~~ |
   |           ~~   |
   |         ~*     |
   |       ~P~      |
   |     ~~~        |
   |    ~~          |
   |  ~~            |
   |~~~             |
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.87,+0.50) (0.60 s to the shot)
   [4.00 s] hearts 3/3
   +----------------+
   |              ~s|
   |            ~~~ |
   |           ~~   |
   |         *~     |
   |       ~P~      |
   |     ~~~        |
   |    ~~          |
   |  ~~            |
   |~~~             |
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 67%, aim line toward (-0.87,+0.50) (0.20 s to the shot)
  4.200  a spitter spits
  4.333  YOU ARE HIT by a shot from the north-east — hearts 2/3
   [4.33 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [4.50 s] hearts 2/3
   +----------------+
   |              *s|
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [5.00 s] hearts 2/3
   +----------------+
   |               s|
   |             *  |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [5.50 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |            *   |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  6.000  a spitter takes aim
   [6.00 s] hearts 2/3
   +----------------+
   |              ~s|
   |            ~~~ |
   |           ~~   |
   |         ~*     |
   |       ~P~      |
   |     ~~~        |
   |    ~~          |
   |  ~~            |
   |~~~             |
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.87,+0.50) (0.60 s to the shot)
end at 6.00 s: hearts 2/3, enemies left 1
```

### Round 1: @run/play/w1-ne-60 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
spawn spitter 15 0
player 8 4
end 6
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.200  a spitter takes aim
   [1.20 s] hearts 3/3
   +----------------+
   |              ~s|
   |            ~~~ |
   |           ~~   |
   |         ~~     |
   |       ~P~      |
   |     ~~~        |
   |    ~~          |
   |  ~~            |
   |~~~             |
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.87,+0.50) (0.60 s to the shot)
   [1.50 s] hearts 3/3
   +----------------+
   |              ~s|
   |            ~~~ |
   |           ~~   |
   |         ~~     |
   |       ~P~      |
   |     ~~~        |
   |    ~~          |
   |  ~~            |
   |~~~             |
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 50%, aim line toward (-0.87,+0.50) (0.30 s to the shot)
  1.800  a spitter spits
   [2.00 s] hearts 3/3
   +----------------+
   |              *s|
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 3/3
   +----------------+
   |               s|
   |             *  |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.00 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |            *   |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.50 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |                |
   |           *    |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.600  a spitter takes aim
   [3.60 s] hearts 3/3
   +----------------+
   |              ~s|
   |            ~~~ |
   |           ~~   |
   |         ~*     |
   |       ~P~      |
   |     ~~~        |
   |    ~~          |
   |  ~~            |
   |~~~             |
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.87,+0.50) (0.60 s to the shot)
   [4.00 s] hearts 3/3
   +----------------+
   |              ~s|
   |            ~~~ |
   |           ~~   |
   |         *~     |
   |       ~P~      |
   |     ~~~        |
   |    ~~          |
   |  ~~            |
   |~~~             |
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 67%, aim line toward (-0.87,+0.50) (0.20 s to the shot)
  4.200  a spitter spits
  4.350  YOU ARE HIT by a shot from the north-east — hearts 2/3
   [4.35 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [4.50 s] hearts 2/3
   +----------------+
   |              *s|
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [5.00 s] hearts 2/3
   +----------------+
   |               s|
   |             *  |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [5.50 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |            *   |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  6.000  a spitter takes aim
   [6.00 s] hearts 2/3
   +----------------+
   |              ~s|
   |            ~~~ |
   |           ~~   |
   |         ~*     |
   |       ~P~      |
   |     ~~~        |
   |    ~~          |
   |  ~~            |
   |~~~             |
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.87,+0.50) (0.60 s to the shot)
end at 6.00 s: hearts 2/3, enemies left 1
```

### Round 1: @run/play/w1-se-30 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 30
spawn spitter 15 7
player 8 4
end 6
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |               s|
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |               s|
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |               s|
   |                |
   +----------------+
  1.200  a spitter takes aim
   [1.20 s] hearts 3/3
   +----------------+
   |~               |
   |~~~             |
   |  ~~~           |
   |     ~~~        |
   |       ~P~      |
   |         ~~~    |
   |            ~~~ |
   |              ~s|
   |                |
   +----------------+
   cue: s at (15.0,7.0) glows orange-red, brightness 0%, aim line toward (-0.92,-0.39) (0.60 s to the shot)
   [1.50 s] hearts 3/3
   +----------------+
   |~               |
   |~~~             |
   |  ~~~           |
   |     ~~~        |
   |       ~P~      |
   |         ~~~    |
   |            ~~~ |
   |              ~s|
   |                |
   +----------------+
   cue: s at (15.0,7.0) glows orange-red, brightness 50%, aim line toward (-0.92,-0.39) (0.30 s to the shot)
  1.800  a spitter spits
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |              *s|
   |                |
   +----------------+
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |             *  |
   |               s|
   |                |
   +----------------+
   [3.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |            *   |
   |               s|
   |                |
   +----------------+
   [3.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |          *     |
   |                |
   |               s|
   |                |
   +----------------+
  3.600  a spitter takes aim
   [3.60 s] hearts 3/3
   +----------------+
   |~               |
   |~~~             |
   |  ~~~           |
   |     ~~~        |
   |       ~P~      |
   |         ~*~    |
   |            ~~~ |
   |              ~s|
   |                |
   +----------------+
   cue: s at (15.0,7.0) glows orange-red, brightness 0%, aim line toward (-0.92,-0.39) (0.60 s to the shot)
   [4.00 s] hearts 3/3
   +----------------+
   |~               |
   |~~~             |
   |  ~~~           |
   |     ~~~        |
   |       ~P*      |
   |         ~~~    |
   |            ~~~ |
   |              ~s|
   |                |
   +----------------+
   cue: s at (15.0,7.0) glows orange-red, brightness 67%, aim line toward (-0.92,-0.39) (0.20 s to the shot)
  4.200  a spitter spits
  4.200  YOU ARE HIT by a shot from the south-east — hearts 2/3
   [4.20 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |               s|
   |                |
   +----------------+
   [4.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |              *s|
   |                |
   +----------------+
   [5.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |             *  |
   |               s|
   |                |
   +----------------+
   [5.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |           *    |
   |                |
   |               s|
   |                |
   +----------------+
  6.000  a spitter takes aim
   [6.00 s] hearts 2/3
   +----------------+
   |~               |
   |~~~             |
   |  ~~~           |
   |     ~~~        |
   |       ~P~      |
   |         ~*~    |
   |            ~~~ |
   |              ~s|
   |                |
   +----------------+
   cue: s at (15.0,7.0) glows orange-red, brightness 0%, aim line toward (-0.92,-0.39) (0.60 s to the shot)
end at 6.00 s: hearts 2/3, enemies left 1
```

### Round 1: @run/play/w1-se-60 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
spawn spitter 15 7
player 8 4
end 6
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |               s|
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |               s|
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |               s|
   |                |
   +----------------+
  1.200  a spitter takes aim
   [1.20 s] hearts 3/3
   +----------------+
   |~               |
   |~~~             |
   |  ~~~           |
   |     ~~~        |
   |       ~P~      |
   |         ~~~    |
   |            ~~~ |
   |              ~s|
   |                |
   +----------------+
   cue: s at (15.0,7.0) glows orange-red, brightness 0%, aim line toward (-0.92,-0.39) (0.60 s to the shot)
   [1.50 s] hearts 3/3
   +----------------+
   |~               |
   |~~~             |
   |  ~~~           |
   |     ~~~        |
   |       ~P~      |
   |         ~~~    |
   |            ~~~ |
   |              ~s|
   |                |
   +----------------+
   cue: s at (15.0,7.0) glows orange-red, brightness 50%, aim line toward (-0.92,-0.39) (0.30 s to the shot)
  1.800  a spitter spits
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |              *s|
   |                |
   +----------------+
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |             *  |
   |               s|
   |                |
   +----------------+
   [3.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |            *   |
   |               s|
   |                |
   +----------------+
   [3.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |          *     |
   |                |
   |               s|
   |                |
   +----------------+
  3.600  a spitter takes aim
   [3.60 s] hearts 3/3
   +----------------+
   |~               |
   |~~~             |
   |  ~~~           |
   |     ~~~        |
   |       ~P~      |
   |         ~*~    |
   |            ~~~ |
   |              ~s|
   |                |
   +----------------+
   cue: s at (15.0,7.0) glows orange-red, brightness 0%, aim line toward (-0.92,-0.39) (0.60 s to the shot)
   [4.00 s] hearts 3/3
   +----------------+
   |~               |
   |~~~             |
   |  ~~~           |
   |     ~~~        |
   |       ~P*      |
   |         ~~~    |
   |            ~~~ |
   |              ~s|
   |                |
   +----------------+
   cue: s at (15.0,7.0) glows orange-red, brightness 67%, aim line toward (-0.92,-0.39) (0.20 s to the shot)
  4.200  a spitter spits
  4.200  YOU ARE HIT by a shot from the south-east — hearts 2/3
   [4.20 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |               s|
   |                |
   +----------------+
   [4.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |              *s|
   |                |
   +----------------+
   [5.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |             *  |
   |               s|
   |                |
   +----------------+
   [5.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |           *    |
   |                |
   |               s|
   |                |
   +----------------+
  6.000  a spitter takes aim
   [6.00 s] hearts 2/3
   +----------------+
   |~               |
   |~~~             |
   |  ~~~           |
   |     ~~~        |
   |       ~P~      |
   |         ~*~    |
   |            ~~~ |
   |              ~s|
   |                |
   +----------------+
   cue: s at (15.0,7.0) glows orange-red, brightness 0%, aim line toward (-0.92,-0.39) (0.60 s to the shot)
end at 6.00 s: hearts 2/3, enemies left 1
```

### Round 2: @run/play/w5-grub-30 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 30
spawn grub 10 4
player 8 4
0.6 attack
end 3
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.033  a grub rears back
   [0.03 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P~g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (10.0,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P~g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (10.0,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.03 s to the lunge)
  0.600  the grub's lunge had already started, the swipe was too late to stop it
  0.600  you swipe: grub hit
  0.733  YOU ARE HIT by a grub — hearts 2/3
   [0.73 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.567  a grub rears back
   [1.57 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      ~~P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (8.4,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
   [2.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      ~~P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (8.4,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.07 s to the lunge)
  2.100  YOU ARE HIT by a grub — hearts 1/3
   [2.10 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.933  a grub rears back
   [2.93 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      ~~P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (8.1,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
   [3.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      ~~P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (8.1,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.43 s to the lunge)
end at 3.00 s: hearts 1/3, enemies left 1
```

### Round 2: @run/play/w5-grub-60 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
spawn grub 10 4
player 8 4
0.6 attack
end 3
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.017  a grub rears back
   [0.02 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P~g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (10.0,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P~g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (10.0,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.02 s to the lunge)
  0.600  the grub's lunge had already started, the swipe was too late to stop it
  0.600  you swipe: grub hit
  0.700  YOU ARE HIT by a grub — hearts 2/3
   [0.70 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.517  a grub rears back
   [1.52 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      ~~Pg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (8.5,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
   [2.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      ~~Pg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (8.5,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.02 s to the lunge)
  2.033  YOU ARE HIT by a grub — hearts 1/3
   [2.03 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.850  a grub rears back
   [2.85 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      ~~P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (8.4,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
   [3.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      ~~P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (8.4,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.35 s to the lunge)
end at 3.00 s: hearts 1/3, enemies left 1
```

### Round 2: @run/play/w5-brute-60 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
spawn brute 10 4
player 8 4
0.8 attack
end 3
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P G     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.017  a brute rears back
   [0.02 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P~G     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (10.0,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.70 s to the lunge)
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P~G     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (10.0,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.22 s to the lunge)
  0.800  the brute's lunge had already started, the swipe was too late to stop it
  0.800  you swipe: brute hit
  0.900  YOU ARE HIT by a brute — hearts 2/3
   [0.90 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.117  a brute rears back
   [2.12 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      ~~PG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (8.5,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.70 s to the lunge)
   [2.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      ~~PG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (8.5,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.32 s to the lunge)
  2.833  YOU ARE HIT by a brute — hearts 1/3
   [2.83 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 3.00 s: hearts 1/3, enemies left 1
```

### Round 3: @run/play/w5-brute-30 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 30
spawn brute 10 4
player 8 4
0.8 attack
end 1.5
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P G     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.033  a brute rears back
   [0.03 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P~G     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (10.0,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.70 s to the lunge)
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P~G     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (10.0,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.23 s to the lunge)
  0.800  the brute's lunge had already started, the swipe was too late to stop it
  0.800  you swipe: brute hit
  0.933  YOU ARE HIT by a brute — hearts 2/3
   [0.93 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 1.50 s: hearts 2/3, enemies left 1
```

### Round 3: @run/play/w6-grub-windup-30 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 30
spawn grub 10 4
player 8.8 4
0.3 attack
end 2
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         Pg     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.033  a grub rears back
   [0.03 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        ~Pg     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (10.0,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
  0.300  you swipe: grub hit
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         Pg     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.733  a grub rears back
   [0.73 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        ~Pg     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (10.0,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        ~Pg     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (10.0,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.23 s to the lunge)
  1.333  YOU ARE HIT by a grub — hearts 2/3
   [1.33 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         P      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         P      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         P      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 2.00 s: hearts 2/3, enemies left 1
```

### Round 3: @run/play/w6-grub-windup-60 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
spawn grub 10 4
player 8.8 4
0.3 attack
end 2
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         Pg     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.017  a grub rears back
   [0.02 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        ~Pg     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (10.0,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
  0.300  you swipe: grub hit
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         Pg     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.717  a grub rears back
   [0.72 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        ~Pg     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (10.0,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        ~Pg     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (10.0,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.22 s to the lunge)
  1.300  YOU ARE HIT by a grub — hearts 2/3
   [1.30 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         P      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         P      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         P      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 2.00 s: hearts 2/3, enemies left 1
```

### Round 3: @run/play/w6-brute-windup-60 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
spawn brute 10 4
player 8.8 4
0.3 attack
end 2
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         PG     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.017  a brute rears back
   [0.02 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        ~PG     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (10.0,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.70 s to the lunge)
  0.300  the brute shrugs off the swipe
  0.300  you swipe: brute hit
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        ~PG     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (10.0,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.22 s to the lunge)
  0.800  YOU ARE HIT by a brute — hearts 2/3
   [0.80 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         P      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         P      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         P      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         P      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 2.00 s: hearts 2/3, enemies left 1
```

### Round 3: @run/play/w6-grub-recovery-60 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
spawn grub 10 4
player 8.8 4
1.3 attack
end 2
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         Pg     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.017  a grub rears back
   [0.02 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        ~Pg     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (10.0,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        ~Pg     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (10.0,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.02 s to the lunge)
  0.600  YOU ARE HIT by a grub — hearts 2/3
   [0.60 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         P      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         P      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.300  you swipe: grub hit
  1.417  a grub rears back
   [1.42 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       ~~P      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (9.3,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
   [1.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       ~~P      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (9.3,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.42 s to the lunge)
  1.933  YOU ARE HIT by a grub — hearts 1/3
   [1.93 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         P      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         P      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 2.00 s: hearts 1/3, enemies left 1
```

### Round 3: @run/play/w4-dash-30 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 30
spawn spitter 15 4
player 8 4
3.8 dash right
end 4.15
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P      s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P      s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P      s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.200  a spitter takes aim
   [1.20 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |~~~~~~~~P~~~~~~s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (15.0,4.0) glows orange-red, brightness 0%, aim line toward (-1.00,+0.00) (0.60 s to the shot)
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |~~~~~~~~P~~~~~~s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (15.0,4.0) glows orange-red, brightness 50%, aim line toward (-1.00,+0.00) (0.30 s to the shot)
  1.800  a spitter spits
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P     *s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    * s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P  *   s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P *    s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.600  a spitter takes aim
   [3.60 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |~~~~~~~~P~*~~~~s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (15.0,4.0) glows orange-red, brightness 0%, aim line toward (-1.00,+0.00) (0.60 s to the shot)
  3.800  you dash right
   [4.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |~~~~~~~~~~~P~~~s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (15.0,4.0) glows orange-red, brightness 67%, aim line toward (-1.00,+0.00) (0.20 s to the shot)
end at 4.17 s: hearts 3/3, enemies left 1
```

### Round 3: @run/play/w4-dash-60 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
spawn spitter 15 4
player 8 4
3.8 dash right
end 4.15
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P      s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P      s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P      s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.200  a spitter takes aim
   [1.20 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |~~~~~~~~P~~~~~~s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (15.0,4.0) glows orange-red, brightness 0%, aim line toward (-1.00,+0.00) (0.60 s to the shot)
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |~~~~~~~~P~~~~~~s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (15.0,4.0) glows orange-red, brightness 50%, aim line toward (-1.00,+0.00) (0.30 s to the shot)
  1.800  a spitter spits
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P     *s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    * s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P  *   s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P *    s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.600  a spitter takes aim
   [3.60 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |~~~~~~~~P~*~~~~s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (15.0,4.0) glows orange-red, brightness 0%, aim line toward (-1.00,+0.00) (0.60 s to the shot)
  3.800  you dash right
   [4.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |~~~~~~~~~~~P~~~s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (15.0,4.0) glows orange-red, brightness 67%, aim line toward (-1.00,+0.00) (0.20 s to the shot)
end at 4.15 s: hearts 3/3, enemies left 1
```

### Round 3: @run/play/w3-shot-rule-60 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
spawn spitter 15 4
player 8 4
when text "by a shot" then move up
end 5.5
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P      s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P      s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P      s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.200  a spitter takes aim
   [1.20 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |~~~~~~~~P~~~~~~s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (15.0,4.0) glows orange-red, brightness 0%, aim line toward (-1.00,+0.00) (0.60 s to the shot)
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |~~~~~~~~P~~~~~~s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (15.0,4.0) glows orange-red, brightness 50%, aim line toward (-1.00,+0.00) (0.30 s to the shot)
  1.800  a spitter spits
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P     *s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    * s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P  *   s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P *    s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.600  a spitter takes aim
   [3.60 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |~~~~~~~~P~*~~~~s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (15.0,4.0) glows orange-red, brightness 0%, aim line toward (-1.00,+0.00) (0.60 s to the shot)
  3.983  YOU ARE HIT by a shot from the east — hearts 2/3
   [3.98 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |~~~~~~~~P~~~~~~s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (15.0,4.0) glows orange-red, brightness 64%, aim line toward (-1.00,+0.00) (0.22 s to the shot)
   [4.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |~~~~~~~~P~~~~~~s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (15.0,4.0) glows orange-red, brightness 67%, aim line toward (-1.00,+0.00) (0.20 s to the shot)
  4.200  a spitter spits
   [4.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P     *s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [5.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    * s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [5.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P  *   s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 5.50 s: hearts 2/3, enemies left 1
```

### Round 3: @run/play/w3-grub-rule-60 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
spawn grub 10 4
player 8 4
when text "rears back" then move aside
end 3
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.017  a grub rears back
   [0.02 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P~g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (10.0,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |        P       |
   |                |
   |        ~~g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (10.0,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.02 s to the lunge)
   [1.00 s] hearts 3/3
   +----------------+
   |        P       |
   |                |
   |                |
   |                |
   |        g       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 3/3
   +----------------+
   |        P       |
   |                |
   |                |
   |                |
   |        g       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 3/3
   +----------------+
   |        P       |
   |                |
   |                |
   |                |
   |        g       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 3/3
   +----------------+
   |        P       |
   |                |
   |                |
   |        g       |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.00 s] hearts 3/3
   +----------------+
   |        P       |
   |                |
   |                |
   |        g       |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 3.00 s: hearts 3/3, enemies left 1
```

### Round 3: @run/play/w2-room4-60 — `python3 play.py --view player {script}`

Script:

```text
room 4
fps 60
end 12
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room 4 — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |               s|
   |g               |
   |                |
   |                |
   | r      P       |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |               s|
   |g               |
   |                |
   |                |
   |  r     P       |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |               s|
   | g              |
   |                |
   |                |
   |   r    P       |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  1.200  a spitter takes aim
   [1.20 s] hearts 3/3
   +----------------+
   |              ~s|
   | g          ~~~ |
   |           ~~   |
   |         ~~     |
   |   r   ~P~      |
   |     ~~~        |
   |    ~~          |
   |  ~~            |
   |~~~            s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.87,+0.50) (0.60 s to the shot)
   [1.50 s] hearts 3/3
   +----------------+
   |              ~s|
   |            ~~~ |
   | g         ~~   |
   |         ~~     |
   |   r   ~P~      |
   |     ~~~        |
   |    ~~          |
   |  ~~            |
   |~~~            s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 50%, aim line toward (-0.87,+0.50) (0.30 s to the shot)
  1.800  a spitter spits
   [2.00 s] hearts 3/3
   +----------------+
   |              *s|
   |                |
   |  g             |
   |                |
   |    r   P       |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  2.400  a spitter takes aim
   [2.40 s] hearts 3/3
   +----------------+
   |~~~            s|
   |  ~~         *  |
   |  g ~~          |
   |     ~~~        |
   |     r ~P~      |
   |         ~~     |
   |           ~~   |
   |            ~~~ |
   |              ~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.87,-0.50) (0.60 s to the shot)
   [2.50 s] hearts 3/3
   +----------------+
   |~~~            s|
   |  ~~         *  |
   |  g ~~          |
   |     ~~~        |
   |     r ~P~      |
   |         ~~     |
   |           ~~   |
   |            ~~~ |
   |              ~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 17%, aim line toward (-0.87,-0.50) (0.50 s to the shot)
  3.000  a spitter spits
   [3.00 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |   g        *   |
   |                |
   |      r P       |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  3.150  a runner rears back
   [3.15 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |   g       *    |
   |                |
   |      r~P       |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   cue: r at (6.0,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.35 s to the lunge)
   [3.50 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |   g            |
   |           *    |
   |      r P       |
   |                |
   |                |
   |              * |
   |               s|
   +----------------+
  3.600  a spitter takes aim
   [3.60 s] hearts 3/3
   +----------------+
   |              ~s|
   |            ~~~ |
   |   g       ~~   |
   |         ~*     |
   |       rP~      |
   |     ~~~        |
   |    ~~          |
   |  ~~         *  |
   |~~~            s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.87,+0.50) (0.60 s to the shot)
  3.683  YOU ARE HIT by a runner — hearts 2/3
   [3.68 s] hearts 2/3
   +----------------+
   |              ~s|
   |            ~~~ |
   |   g       ~~   |
   |         ~*     |
   |       rP~      |
   |     ~~~        |
   |    ~~          |
   |  ~~         *  |
   |~~~            s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 14%, aim line toward (-0.87,+0.50) (0.52 s to the shot)
   [4.00 s] hearts 2/3
   +----------------+
   |              ~s|
   |            ~~~ |
   |    g      ~~   |
   |         *~     |
   |       rP~      |
   |     ~~~        |
   |    ~~      *   |
   |  ~~            |
   |~~~            s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 67%, aim line toward (-0.87,+0.50) (0.20 s to the shot)
  4.200  a spitter spits
  4.300  a runner rears back
   [4.30 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |                |
   |    g           |
   |       rP~~     |
   |                |
   |            *   |
   |                |
   |               s|
   +----------------+
   cue: r at (7.5,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.35 s to the lunge)
   [4.50 s] hearts 2/3
   +----------------+
   |              *s|
   |                |
   |                |
   |    g           |
   |       rP~~     |
   |                |
   |           *    |
   |                |
   |               s|
   +----------------+
   cue: r at (7.5,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.15 s to the lunge)
  4.667  YOU ARE HIT by a runner — hearts 1/3
   [4.67 s] hearts 1/3
   +----------------+
   |               s|
   |              * |
   |                |
   |    g           |
   |        P       |
   |           *    |
   |                |
   |                |
   |               s|
   +----------------+
  4.800  a spitter takes aim
   [4.80 s] hearts 1/3
   +----------------+
   |~~~            s|
   |  ~~         *  |
   |    ~~          |
   |    g~~~        |
   |       ~P~      |
   |         ~*     |
   |           ~~   |
   |            ~~~ |
   |              ~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.87,-0.50) (0.60 s to the shot)
   [5.00 s] hearts 1/3
   +----------------+
   |~~~            s|
   |  ~~         *  |
   |    ~~          |
   |     g~~        |
   |       ~P~      |
   |         ~*     |
   |           ~~   |
   |            ~~~ |
   |              ~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 33%, aim line toward (-0.87,-0.50) (0.40 s to the shot)
  5.283  a runner rears back
   [5.28 s] hearts 1/3
   +----------------+
   |~~~            s|
   |  ~~            |
   |    ~~      *   |
   |     g~~        |
   |       ~P~~     |
   |         *~     |
   |           ~~   |
   |            ~~~ |
   |              ~s|
   +----------------+
   cue: r at (7.6,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.35 s to the lunge)
   cue: s at (15.0,8.0) glows orange-red, brightness 81%, aim line toward (-0.87,-0.50) (0.12 s to the shot)
  5.400  a spitter spits
   [5.50 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   |            *   |
   |     g          |
   |        P~~     |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   cue: r at (7.6,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.13 s to the lunge)
  5.550  YOU ARE HIT by a shot from the south-east — hearts 0/3
  5.550  you went down
   [5.55 s] hearts 0/3
   +----------------+
   |               s|
   |                |
   |           *    |
   |     g          |
   |        x~~     |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   cue: r at (7.6,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.08 s to the lunge)
   [6.00 s] hearts 0/3
   +----------------+
   |               s|
   |                |
   |                |
   |     g    *     |
   |        x~~     |
   |                |
   |                |
   |             *  |
   |               s|
   +----------------+
   cue: r at (7.6,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.08 s to the lunge)
   [6.50 s] hearts 0/3
   +----------------+
   |               s|
   |                |
   |                |
   |     g   *      |
   |        x~~     |
   |                |
   |            *   |
   |                |
   |               s|
   +----------------+
   cue: r at (7.6,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.08 s to the lunge)
end at 6.55 s: hearts 0/3, enemies left 4
```

### Round 3: @run/play/w2-room4-30 — `python3 play.py --view player {script}`

Script:

```text
room 4
fps 30
end 12
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room 4 — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |               s|
   |g               |
   |                |
   |                |
   | r      P       |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |               s|
   |g               |
   |                |
   |                |
   |  r     P       |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |               s|
   | g              |
   |                |
   |                |
   |   r    P       |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  1.200  a spitter takes aim
   [1.20 s] hearts 3/3
   +----------------+
   |              ~s|
   | g          ~~~ |
   |           ~~   |
   |         ~~     |
   |   r   ~P~      |
   |     ~~~        |
   |    ~~          |
   |  ~~            |
   |~~~            s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.87,+0.50) (0.60 s to the shot)
   [1.50 s] hearts 3/3
   +----------------+
   |              ~s|
   |            ~~~ |
   | g         ~~   |
   |         ~~     |
   |   r   ~P~      |
   |     ~~~        |
   |    ~~          |
   |  ~~            |
   |~~~            s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 50%, aim line toward (-0.87,+0.50) (0.30 s to the shot)
  1.800  a spitter spits
   [2.00 s] hearts 3/3
   +----------------+
   |              *s|
   |                |
   |  g             |
   |                |
   |    r   P       |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  2.400  a spitter takes aim
   [2.40 s] hearts 3/3
   +----------------+
   |~~~            s|
   |  ~~         *  |
   |  g ~~          |
   |     ~~~        |
   |     r ~P~      |
   |         ~~     |
   |           ~~   |
   |            ~~~ |
   |              ~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.87,-0.50) (0.60 s to the shot)
   [2.50 s] hearts 3/3
   +----------------+
   |~~~            s|
   |  ~~         *  |
   |  g ~~          |
   |     ~~~        |
   |     r ~P~      |
   |         ~~     |
   |           ~~   |
   |            ~~~ |
   |              ~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 17%, aim line toward (-0.87,-0.50) (0.50 s to the shot)
  3.000  a spitter spits
   [3.00 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |   g        *   |
   |                |
   |      r P       |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  3.167  a runner rears back
   [3.17 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |   g       *    |
   |                |
   |      r~P       |
   |                |
   |                |
   |                |
   |              *s|
   +----------------+
   cue: r at (6.0,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.35 s to the lunge)
   [3.50 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |   g            |
   |          *     |
   |      r~P       |
   |                |
   |                |
   |              * |
   |               s|
   +----------------+
   cue: r at (6.0,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.02 s to the lunge)
  3.600  a spitter takes aim
   [3.60 s] hearts 3/3
   +----------------+
   |              ~s|
   |            ~~~ |
   |   g       ~~   |
   |         ~*     |
   |       rP~      |
   |     ~~~        |
   |    ~~          |
   |  ~~         *  |
   |~~~            s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.87,+0.50) (0.60 s to the shot)
  3.733  YOU ARE HIT by a runner — hearts 2/3
   [3.73 s] hearts 2/3
   +----------------+
   |              ~s|
   |            ~~~ |
   |   g       ~~   |
   |         ~*     |
   |       ~P~      |
   |     ~~~        |
   |    ~~          |
   |  ~~         *  |
   |~~~            s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 22%, aim line toward (-0.87,+0.50) (0.47 s to the shot)
   [4.00 s] hearts 2/3
   +----------------+
   |              ~s|
   |            ~~~ |
   |    g      ~~   |
   |         *~     |
   |       ~P~      |
   |     ~~~        |
   |    ~~      *   |
   |  ~~            |
   |~~~            s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 67%, aim line toward (-0.87,+0.50) (0.20 s to the shot)
  4.200  a spitter spits
  4.367  a runner rears back
   [4.37 s] hearts 2/3
   +----------------+
   |              *s|
   |                |
   |                |
   |    g           |
   |        P~~     |
   |                |
   |           *    |
   |                |
   |               s|
   +----------------+
   cue: r at (7.6,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.35 s to the lunge)
   [4.50 s] hearts 2/3
   +----------------+
   |              *s|
   |                |
   |                |
   |    g           |
   |        P~~     |
   |                |
   |           *    |
   |                |
   |               s|
   +----------------+
   cue: r at (7.6,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.22 s to the lunge)
  4.767  YOU ARE HIT by a runner — hearts 1/3
   [4.77 s] hearts 1/3
   +----------------+
   |               s|
   |             *  |
   |                |
   |    g           |
   |        P       |
   |          *     |
   |                |
   |                |
   |               s|
   +----------------+
  4.800  a spitter takes aim
   [4.80 s] hearts 1/3
   +----------------+
   |~~~            s|
   |  ~~         *  |
   |    ~~          |
   |    g~~~        |
   |       ~P~      |
   |         ~*     |
   |           ~~   |
   |            ~~~ |
   |              ~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.87,-0.50) (0.60 s to the shot)
   [5.00 s] hearts 1/3
   +----------------+
   |~~~            s|
   |  ~~         *  |
   |    ~~          |
   |     g~~        |
   |       ~P~      |
   |         ~*     |
   |           ~~   |
   |            ~~~ |
   |              ~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 33%, aim line toward (-0.87,-0.50) (0.40 s to the shot)
  5.400  a runner rears back
  5.400  a spitter spits
   [5.40 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   |            *   |
   |     g          |
   |        P*~     |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   cue: r at (7.9,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.35 s to the lunge)
   [5.50 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   |            *   |
   |     g          |
   |        P~~     |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   cue: r at (7.9,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.25 s to the lunge)
  5.800  YOU ARE HIT by a runner — hearts 0/3
  5.800  you went down
   [5.80 s] hearts 0/3
   +----------------+
   |               s|
   |                |
   |           *    |
   |     g          |
   |        x       |
   |                |
   |                |
   |              * |
   |               s|
   +----------------+
   [6.00 s] hearts 0/3
   +----------------+
   |               s|
   |                |
   |                |
   |     g    *     |
   |        x       |
   |                |
   |                |
   |             *  |
   |               s|
   +----------------+
   [6.50 s] hearts 0/3
   +----------------+
   |               s|
   |                |
   |                |
   |     g   *      |
   |        x       |
   |                |
   |            *   |
   |                |
   |               s|
   +----------------+
end at 6.80 s: hearts 0/3, enemies left 4
```

### Round 3: @run/play/w2-room5-60 — `python3 play.py --view player {script}`

Script:

```text
room 5
fps 60
end 12
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room 5 — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |               s|
   | g              |
   |                |
   |                |
   |        P       |
   |                |
   |g               |
   |                |
   |    G          s|
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |               s|
   | g              |
   |                |
   |                |
   |        P       |
   |                |
   |g               |
   |                |
   |    G          s|
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |               s|
   |  g             |
   |                |
   |                |
   |        P       |
   |                |
   | g              |
   |                |
   |    G          s|
   +----------------+
  1.200  a spitter takes aim
   [1.20 s] hearts 3/3
   +----------------+
   |              ~s|
   |  g         ~~~ |
   |           ~~   |
   |         ~~     |
   |       ~P~      |
   |     ~~~        |
   | g  ~~          |
   |  ~~ G          |
   |~~~            s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.87,+0.50) (0.60 s to the shot)
   [1.50 s] hearts 3/3
   +----------------+
   |              ~s|
   |            ~~~ |
   |  g        ~~   |
   |         ~~     |
   |       ~P~      |
   |     ~~~        |
   | g  ~~          |
   |  ~~ G          |
   |~~~            s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 50%, aim line toward (-0.87,+0.50) (0.30 s to the shot)
  1.800  a spitter spits
   [2.00 s] hearts 3/3
   +----------------+
   |              *s|
   |                |
   |   g            |
   |                |
   |        P       |
   |                |
   |  g             |
   |     G          |
   |               s|
   +----------------+
  2.400  a spitter takes aim
   [2.40 s] hearts 3/3
   +----------------+
   |~~~            s|
   |  ~~         *  |
   |   g~~          |
   |     ~~~        |
   |       ~P~      |
   |  g      ~~     |
   |           ~~   |
   |     G      ~~~ |
   |              ~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.87,-0.50) (0.60 s to the shot)
   [2.50 s] hearts 3/3
   +----------------+
   |~~~            s|
   |  ~~         *  |
   |   g~~          |
   |     ~~~        |
   |       ~P~      |
   |  g      ~~     |
   |           ~~   |
   |     G      ~~~ |
   |              ~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 17%, aim line toward (-0.87,-0.50) (0.50 s to the shot)
  3.000  a spitter spits
   [3.00 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |    g       *   |
   |                |
   |        P       |
   |   g            |
   |                |
   |     G          |
   |               s|
   +----------------+
   [3.50 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |    g           |
   |           *    |
   |        P       |
   |   g            |
   |      G         |
   |              * |
   |               s|
   +----------------+
  3.600  a spitter takes aim
   [3.60 s] hearts 3/3
   +----------------+
   |              ~s|
   |            ~~~ |
   |    g      ~~   |
   |         ~*     |
   |       ~P~      |
   |   g ~~~        |
   |    ~~G         |
   |  ~~         *  |
   |~~~            s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.87,+0.50) (0.60 s to the shot)
   [4.00 s] hearts 3/3
   +----------------+
   |              ~s|
   |            ~~~ |
   |           ~~   |
   |     g   *~     |
   |       ~P~      |
   |    g~~~        |
   |    ~~G     *   |
   |  ~~            |
   |~~~            s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 67%, aim line toward (-0.87,+0.50) (0.20 s to the shot)
  4.200  a spitter spits
  4.350  YOU ARE HIT by a shot from the north-east — hearts 2/3
   [4.35 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |                |
   |     g          |
   |        P       |
   |    g           |
   |      G    *    |
   |                |
   |               s|
   +----------------+
   [4.50 s] hearts 2/3
   +----------------+
   |              *s|
   |                |
   |                |
   |     g          |
   |        P       |
   |    g           |
   |      G    *    |
   |                |
   |               s|
   +----------------+
  4.800  a spitter takes aim
   [4.80 s] hearts 2/3
   +----------------+
   |~~~            s|
   |  ~~         *  |
   |    ~~          |
   |     g~~        |
   |       ~P~      |
   |     g   ~*     |
   |      G    ~~   |
   |            ~~~ |
   |              ~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.87,-0.50) (0.60 s to the shot)
   [5.00 s] hearts 2/3
   +----------------+
   |~~~            s|
   |  ~~         *  |
   |    ~~          |
   |     ~g~        |
   |       ~P~      |
   |     g   ~*     |
   |      G    ~~   |
   |            ~~~ |
   |              ~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 33%, aim line toward (-0.87,-0.50) (0.40 s to the shot)
  5.250  a brute rears back
   [5.25 s] hearts 2/3
   +----------------+
   |~~~            s|
   |  ~~            |
   |    ~~      *   |
   |     ~g~        |
   |       ~P~      |
   |     g G *~     |
   |           ~~   |
   |            ~~~ |
   |              ~s|
   +----------------+
   cue: G at (6.6,5.4) flashes orange-red, lunge line toward (+0.71,-0.71), 2.4 tiles (0.70 s to the lunge)
   cue: s at (15.0,8.0) glows orange-red, brightness 75%, aim line toward (-0.87,-0.50) (0.15 s to the shot)
  5.400  a spitter spits
   [5.50 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |            *   |
   |      g         |
   |        P       |
   |     g G        |
   |                |
   |                |
   |               s|
   +----------------+
   cue: G at (6.6,5.4) flashes orange-red, lunge line toward (+0.71,-0.71), 2.4 tiles (0.45 s to the lunge)
  5.550  YOU ARE HIT by a shot from the south-east — hearts 1/3
   [5.55 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   |           *    |
   |      g         |
   |        P       |
   |     g G        |
   |                |
   |                |
   |               s|
   +----------------+
   cue: G at (6.6,5.4) flashes orange-red, lunge line toward (+0.71,-0.71), 2.4 tiles (0.40 s to the lunge)
  6.000  a spitter takes aim
   [6.00 s] hearts 1/3
   +----------------+
   |              ~s|
   |            ~~~ |
   |           ~~   |
   |       g ~*     |
   |       ~P~      |
   |     ~gG        |
   |    ~~          |
   |  ~~         *  |
   |~~~            s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.87,+0.50) (0.60 s to the shot)
  6.267  a grub rears back
   [6.27 s] hearts 1/3
   +----------------+
   |              ~s|
   |            ~~~ |
   |           ~~   |
   |       g ~*     |
   |      g~P~      |
   |     ~~~        |
   |    ~~          |
   |  ~~         *  |
   |~~~            s|
   +----------------+
   cue: g at (6.7,3.5) flashes orange-red, lunge line toward (+0.92,+0.39), 2.4 tiles (0.50 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 44%, aim line toward (-0.87,+0.50) (0.33 s to the shot)
   [6.50 s] hearts 1/3
   +----------------+
   |              ~s|
   |            ~~~ |
   |           ~~   |
   |       g *~     |
   |      g~P~      |
   |     ~~~        |
   |    ~~      *   |
   |  ~~            |
   |~~~            s|
   +----------------+
   cue: g at (6.7,3.5) flashes orange-red, lunge line toward (+0.92,+0.39), 2.4 tiles (0.27 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 83%, aim line toward (-0.87,+0.50) (0.10 s to the shot)
  6.600  a spitter spits
  6.750  YOU ARE HIT by a shot from the north-east — hearts 0/3
  6.750  you went down
   [6.75 s] hearts 0/3
   +----------------+
   |               s|
   |                |
   |                |
   |       g        |
   |       gx~      |
   |                |
   |           *    |
   |                |
   |               s|
   +----------------+
   cue: g at (6.7,3.5) flashes orange-red, lunge line toward (+0.92,+0.39), 2.4 tiles (0.02 s to the lunge)
   [7.00 s] hearts 0/3
   +----------------+
   |               s|
   |              * |
   |                |
   |       g        |
   |       gx~      |
   |                |
   |           *    |
   |                |
   |               s|
   +----------------+
   cue: g at (6.7,3.5) flashes orange-red, lunge line toward (+0.92,+0.39), 2.4 tiles (0.02 s to the lunge)
   [7.50 s] hearts 0/3
   +----------------+
   |               s|
   |             *  |
   |                |
   |       g        |
   |       gx~      |
   |         *      |
   |                |
   |                |
   |               s|
   +----------------+
   cue: g at (6.7,3.5) flashes orange-red, lunge line toward (+0.92,+0.39), 2.4 tiles (0.02 s to the lunge)
end at 7.75 s: hearts 0/3, enemies left 5
```
>>>END

## Validation feedback

A previous executor's output was rejected for these reasons. Produce the operation's files again, fixing them:

- goals/G-001-combat-monotony/98-qa-to-studio.md: missing sections ['Constraints', 'Decisions already made', 'Findings', 'Open questions']
