# Studio operation packet

operation: Step
goal: G-001
role: qa
incoming_handoff: goals/G-001-dash-damage/05-gameplay-engineer-to-qa.md
next_seq: 6
runs: tests, play, trace (0 rounds left; results in @run-results)
run_tests: python3 -m unittest discover -s tests
run_play: python3 play.py --view player {script}
run_trace: python3 play.py --view trace {script}
context_request: used (the requested files are in Inputs)

## You may write

- goals/G-001-dash-damage/06-qa-to-<recipient>.md

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
- Nothing exists beyond this packet and what it offers: build runs (`@run`), one request for more
  files (`@need`), and the operations that follow. There is no other environment, staff, device,
  budget or log store, so never ask the Owner for them; say plainly what your means cannot show.
>>>END

<<<FILE goals/G-001-dash-damage/05-gameplay-engineer-to-qa.md
---
kind: handoff
goal: G-001
seq: 5
from: gameplay-engineer
to: qa
stage: Verify
outcome: done
---
# 05: gameplay-engineer → qa — Verify fix: no damage during a dash begun in the post-hit window (test corrected, suite green)

## Task

Verify independently, from the acceptance criteria below and the build, that the player cannot take damage at any moment of a dash at 30 and 60 FPS. Use `verify-change`.

## Context

Goal G-001. The Owner reported taking damage while dashing. QA's defect report (02, in the Load list) reproduced it: a dash begun with less than 0.25 s left of the 0.8 s post-hit invulnerability, where the invulnerability dropped mid-dash. A fix is in `repo/game.py`. The runtime's test run on the build is green. Judge the build by running it, not by this note.

## Findings

### What changed and where

- `repo/game.py`: invulnerability now follows both the dash timer and the post-hit timer.
- `repo/tests/test_game.py`: a regression test for the late-window dash exists and was adjusted in the last pass (no assertion weakened).
- `design/combat.md`, inputs, dash and cooldown values: unchanged.

### Acceptance criteria (full text in 02)

1. Script A at 30 and 60 FPS: no hit during or at the dash; hearts stay 2/3.
2. A dash started anywhere in the post-hit window is invulnerable for its full duration.
3. Invulnerability persists after the dash ends until the post-hit window ends.
4. Unchanged behaviors: hit damage (1 heart), 0.3 s stun, 0.8 s post-hit window, 0.25 s plain-dash invulnerability, cooldown, inputs.
5. Test suite passes; a regression test exists covering both frame rates.

### How to exercise

Run `python3 play.py --view trace {script}` and `--view player {script}` for these, each at `fps 60` and `fps 30`:

Script A:
```text
room empty
fps 60
end 4
player 8 4
spawn grub 10 4
spawn spitter 14 4
0.2 dash right
1.0 dash left
2.0 dash right
```
Script B:
```text
room empty
fps 60
end 4
player 8 4
spawn grub 10 4
0.2 dash right
1.0 dash left
1.9 dash left
```

Also cover, with your own scripts:
- The criterion 3 case: a dash that ends while the post-hit window is still running, with a threat arriving after the dash ends.
- A Grub contact arriving during a dash begun late in the post-hit window.
- A hit outside any dash or window (1 heart, 0.3 s stun).
- The exact frame at which a dash ends with a shot or contact already overlapping the player. `design/combat.md` says "invulnerable for the full dash duration" and may not define that instant; report what you observe, and if the expected behavior is undefined say so.

Run the suite: `python3 -m unittest discover -s tests`.

## Decisions already made

- D-001: one attack button plus dash. No inputs were added.

## Constraints

- Must play correctly at 30 and 60 FPS.
- `design/combat.md` is unchanged and is the reference for intended behavior.
- Verify from the criteria and the build.

## Open questions

None blocking.

## Expected output

A verification verdict (pass/fail) with evidence at 30 and 60 FPS for script A, script B, the criterion 3 case and the unchanged behaviors. Address the result to `studio`. On pass, the Goal goes to Close (Review is not part of this defect Goal); on fail, the return rules apply.

## Build check

The runtime ran `run_tests` (`python3 -m unittest discover -s tests`) on the build exactly as this step wrote it: exit 0 (0.0 s).

```text
..........
----------------------------------------------------------------------
Ran 10 tests in 0.001s

OK
```

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md#constraints, design/combat.md, manual.md, repo/README.md, the build in `repo/` (run with `run_play` and `run_trace`)
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-dash-damage/02-qa-to-gameplay-engineer.md
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

<<<FILE manual.md
# Lantern Depths — how to play build 0.3

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

<<<FILE repo/README.md
# Lantern Depths build

- `game.py`: the combat simulation (fixed frames, 30 or 60 FPS).
- `play.py`: runs an input script (`../manual.md`) and prints the player view or a trace.
- `tests/`: `python3 -m unittest discover -s tests`
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
# 02: qa → gameplay-engineer — Fix: player takes damage while dashing (dash begun during post-hit invulnerability)

## Task

Fix the reproduced defect below so that the player cannot take damage at any moment of a dash, at both 30 and 60 FPS. The acceptance criteria are in Findings.

## Context

Goal G-001. The Owner reported (ja): 「ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい。」 ("I sometimes take damage even while dashing."). QA reproduced it in the practice room with deterministic scripts, at both 30 and 60 FPS. The Studio handoff (01) asked for a defect report. `design/combat.md` defines the intended behavior, so this goes to the engineer.

## Findings

### Summary

Damage can be taken while a dash is still in progress. The conditions seen:

1. The player is still in the post-hit invulnerability window (0.8 s after a hit).
2. The player starts a dash while that window has less time left than the dash duration (0.25 s). In the runs, 0.067 s were left.
3. The post-hit invulnerability ends while the dash is still active (`dash_left` > 0).
4. At that moment the player is vulnerable, and an attack that arrives during the remaining dash time hurts them.

The confirmed case is a Spitter shot. A Grub contact in the same window was not tested to a hit (see "Not established").

### Source of "expected" (quoted from `design/combat.md`)

- "**Dash**: 4 tiles over 0.25 s. The player is invulnerable for the full dash duration."
- "**Getting hit**: 1 heart of damage, 0.3 s hit-stun (no input), then invulnerability until 0.8 s after the hit."

Both rules grant invulnerability. The dash rule says "the full dash duration" without exception. Damage during a dash is therefore a defect against the document, and the spec is not silent. The document does not state how the two invulnerability sources combine. The dash rule alone is enough to decide the cases below, because the dash lasts the full 0.25 s.

### Reproduction script A (Spitter shot), deterministic

```text
room empty
fps 60
end 4
player 8 4
spawn grub 10 4
spawn spitter 14 4
0.2 dash right
1.0 dash left
2.0 dash right
```

Run with `python3 play.py --view player {script}` or `--view trace`. Frequency: 2 of 2 runs, with identical results because the simulation is scripted. The same script with `fps 30` also reproduced it.

**Setup:** the first dash at 0.2 s works. The Grub reaches the player after that dash and hits at about 1.28 s (hearts 3→2). That is expected, because the player is not dashing. The 1.0 s dash is ignored ("dash not ready"), which is also not a defect. The Spitter fires at 2.000 s. The player dashes right at about 2.0 s, which is inside the 0.8 s post-hit window.

**60 FPS trace:**
- t=2.000: `hurt_left=0.083`, `invulnerable=True`, spit.
- t=2.017 (frame 121): dash starts, `dash_left=0.233`, `hurt_left=0.067`.
- t=2.083 (frame 125): `invulnerable {'value': False, 'why': 'hurt timer ended'}`, then `hurt {'source': 'shot', 'hearts': 1}`. At this point `dash_left=0.167`, so the dash is still active.
- The player-view line reads "2.083 YOU ARE HIT by a shot — hearts 1/3". Hearts go 2→1.
- The dash ended at t=2.250.

**30 FPS trace:**
- t=2.033 (frame 61): dash starts, `hurt_left=0.033`.
- t=2.067 (frame 62): `invulnerable False ('hurt timer ended')`, `dash_left=0.183`.
- t=2.100 (frame 63): `hurt {'source': 'shot', 'hearts': 1}`, `dash_left=0.150`. Hit during the dash.
- The dash ended at frame 68.

The defect does **not** depend on frame rate. Only the exact timestamps shift by a frame or two.

### Related observations (trace evidence, no cause asserted)

- **Flag drops mid-dash.** In script B (below, no Spitter), `invulnerable` also becomes False when "hurt timer ended" at t=2.083 with `dash_left=0.067`, and stays False until `dash_end` at 2.150 (frames 125–129). No damage followed because the Grub was about 2 tiles away. This confirms the window exists independently of the Spitter. It also shows a damaging source in that window would hurt.
- **Flag drops after a dash.** In script A at 60 FPS, after the second hit (2.083) the player has `hurt_left=0.800`. At `dash_end` (t=2.250) the trace shows `invulnerable=False` while `hurt_left=0.633` and `stun_left=0.133` remain. The doc says invulnerability lasts until 0.8 s after a hit, so this looks like a second discrepancy. The 30 FPS trace shows the same at frame 68. No damage was observed in that window, because the enemies were far away. It should be checked as part of the fix.
- **Hypothesis only (not verified):** the invulnerable flag appears to be driven by whichever timer ended most recently rather than by the combination of the two sources. The engineer decides the actual cause.

### Script B (Grub only, no damage; evidence of the window)

```text
room empty
fps 60
end 4
player 8 4
spawn grub 10 4
0.2 dash right
1.0 dash left
1.9 dash left
```

Result: the flag drops at 2.083 mid-dash, no hit. The player is hit at 3.400 after the dash, which is expected.

### Boundary

- Hit during the dash is shown when the post-hit invulnerability ends while the dash is active (dash started with `hurt_left` 0.067 at 60 FPS and 0.033 at 30 FPS).
- Dashes started when there was no post-hit invulnerability left, and the first dash at 0.2 s, were invulnerable for the whole dash in all runs (`invulnerable=True, why 'dash'` until `dash_end`).
- QA did not sweep other `hurt_left` values or dash timings.

### Not established (explicitly)

- Whether a Grub contact hit during a dash is reproducible. Script B shows the vulnerable window, but not an actual Grub hit during the dash.
- The full range of start offsets (other `hurt_left` values) that expose the window.
- The `run_tests` result was not obtained. The existing tests were not run, so the baseline test status is unknown.

### Severity and frequency

- **Severity:** hurts the experience. The player loses a heart during an action the rules call invulnerable, and in a one-button game with dash as the only defense this is felt as unfair. It does not block progress.
- **Frequency:** deterministic once the conditions are met. In real play it needs a dash started shortly before the post-hit window ends and an attack arriving in the remaining dash time. That is plausible for "dash out right after being hit", the most common panic response.
- **Reproducibility:** 100% with script A at 30 and 60 FPS.

### Acceptance criteria (player-observable; each at 30 FPS and at 60 FPS)

1. **Script A** (and its `fps 30` variant): no "YOU ARE HIT" line appears between a "you dash" line and the dash's end. Specifically, the shot at about 2.08–2.10 s does not reduce hearts. Hearts stay 2/3 through the dash.
2. A dash started at any point during the post-hit invulnerability window, including with under 0.25 s remaining, is invulnerable for its full 0.25 s. A Spitter shot or Grub contact arriving at any time in that dash does not hurt.
3. Invulnerability lasts until the later of dash end and 0.8 s after the last hit. After the dash ends, if the 0.8 s window has not elapsed, hits are still ignored. In script A the trace at `dash_end` must still report invulnerable while `hurt_left` > 0.
4. Unchanged behavior:
   - A hit while not dashing and not in the post-hit window still costs 1 heart, with 0.3 s hit-stun.
   - The post-hit invulnerability still ends 0.8 s after the hit.
   - A dash with no preceding hit is still invulnerable for exactly 0.25 s.
   - Dash cooldown behavior is unchanged.
5. `python3 -m unittest discover -s tests` passes, with a regression test added for the dash-in-post-hit-window case at both frame rates.

## Decisions already made

- D-001: combat uses one attack button plus dash. No new input buttons. The fix must not add inputs.

## Constraints

- Must play correctly at both 30 and 60 FPS (`project.md`).
- Do not change `design/combat.md`. The intended behavior (invulnerable for the full dash) is already specified.
- Small team: prefer reusing existing systems.
- QA will verify independently from the criteria and the build, not from the engineer's explanation.

## Open questions

- None blocking. For the engineer to decide: whether the "flag drops after a dash" observation (criterion 3) is part of this fix. It follows from the quoted rule "invulnerability until 0.8 s after the hit". If the engineer thinks the design intends otherwise, hand it to `game-designer` rather than deciding it.

## Expected output

A fix in `repo/` that meets all acceptance criteria, with a regression test. Hand back to `qa` for verification (`verify-change`). Include the exact scripts that QA should re-run: script A at 30 and 60 FPS, and script B.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints, design/combat.md, manual.md, repo/README.md, repo/game.py, repo/play.py, repo/tests/test_game.py
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-dash-damage/01-studio-to-qa.md
>>>END

<<<FILE @files/repo
Files in this directory (names only, not their contents; ask for the ones you need with @need):

- repo/README.md
- repo/game.py
- repo/play.py
- repo/tests/test_game.py
>>>END

<<<FILE studio/templates/handoff.md
---
kind: handoff
goal: G-NNN
seq: N
from: <role-id | studio>
to: <role-id | studio>
stage: <stage the recipient performs>
outcome: <sender's step result: routed | done | partial | pass | fail | question | goal-met | goal-not-met>
---
# NN: <from> → <to> — <one-line task>

<!-- Self-contained: the recipient (any executor, any session) starts from this file and its Load
list alone. The sender fills Task through Open questions and drafts Expected output; the Studio
checks it against the recipient's "Works from", settles Expected output and fills Load when routing.
outcome: routed = written by the Studio; done = work finished, no verdict; partial = work under way,
nothing missing, to be continued by the same Role; pass/fail = verification verdict; question =
handed back with an open question; goal-met/goal-not-met = Review verdict.
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

Exit: 0 (0.0 s). Output:

```text
..........
----------------------------------------------------------------------
Ran 10 tests in 0.001s

OK
```

### Round 1: @run/trace/A60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
end 4
player 8 4
spawn grub 10 4
spawn spitter 14 4
0.2 dash right
1.0 dash left
2.0 dash right
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(10.00,4.00,hp=2) spitter(14.00,4.00,hp=2) | setup
t=0.217 frame=13 pos=(8.27,4.00) hearts=3 invulnerable=True dash_left=0.233 hurt_left=0.000 stun_left=0.000 | grub(9.57,4.00,hp=2) spitter(14.00,4.00,hp=2) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'right'}
t=0.450 frame=27 pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.77,4.00,hp=2) spitter(14.00,4.00,hp=2) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=1.017 frame=61 pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(10.90,4.00,hp=2) spitter(14.00,4.00,hp=2) | ignored {'action': 'dash', 'reason': 'dash not ready'}
t=1.283 frame=77 pos=(12.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(11.43,4.00,hp=2) spitter(14.00,4.00,hp=2) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=2.000 frame=120 pos=(12.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.083 stun_left=0.000 | grub(11.46,4.00,hp=2) spitter(14.00,4.00,hp=2) | spit
t=2.017 frame=121 pos=(12.27,4.00) hearts=2 invulnerable=True dash_left=0.233 hurt_left=0.067 stun_left=0.000 | grub(11.49,4.00,hp=2) spitter(14.00,4.00,hp=2) | dash {'direction': 'right'}
t=2.250 frame=135 pos=(15.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(11.96,4.00,hp=2) spitter(14.00,4.00,hp=2) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=3.483 frame=209 pos=(15.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(14.43,4.00,hp=2) spitter(14.00,4.00,hp=2) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=4.000 frame=240 pos=(15.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.283 stun_left=0.000 | grub(14.46,4.00,hp=2) spitter(14.00,4.00,hp=2) | spit
t=4.000 frame=240 pos=(15.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.283 stun_left=0.000 | grub(14.46,4.00,hp=2) spitter(14.00,4.00,hp=2) | end
```

### Round 1: @run/trace/A30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
end 4
player 8 4
spawn grub 10 4
spawn spitter 14 4
0.2 dash right
1.0 dash left
2.0 dash right
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(10.00,4.00,hp=2) spitter(14.00,4.00,hp=2) | setup
t=0.233 frame=7 pos=(8.53,4.00) hearts=3 invulnerable=True dash_left=0.217 hurt_left=0.000 stun_left=0.000 | grub(9.53,4.00,hp=2) spitter(14.00,4.00,hp=2) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'right'}
t=0.467 frame=14 pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.86,4.00,hp=2) spitter(14.00,4.00,hp=2) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=1.033 frame=31 pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(10.99,4.00,hp=2) spitter(14.00,4.00,hp=2) | ignored {'action': 'dash', 'reason': 'dash not ready'}
t=1.267 frame=38 pos=(12.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(11.46,4.00,hp=2) spitter(14.00,4.00,hp=2) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=2.000 frame=60 pos=(12.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.067 stun_left=0.000 | grub(11.46,4.00,hp=2) spitter(14.00,4.00,hp=2) | spit
t=2.033 frame=61 pos=(12.53,4.00) hearts=2 invulnerable=True dash_left=0.217 hurt_left=0.033 stun_left=0.000 | grub(11.53,4.00,hp=2) spitter(14.00,4.00,hp=2) | dash {'direction': 'right'}
t=2.267 frame=68 pos=(15.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(11.99,4.00,hp=2) spitter(14.00,4.00,hp=2) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=3.500 frame=105 pos=(15.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(14.46,4.00,hp=2) spitter(14.00,4.00,hp=2) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=4.000 frame=120 pos=(15.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.300 stun_left=0.000 | grub(14.46,4.00,hp=2) spitter(14.00,4.00,hp=2) | spit
t=4.000 frame=120 pos=(15.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.300 stun_left=0.000 | grub(14.46,4.00,hp=2) spitter(14.00,4.00,hp=2) | end
```

### Round 2: @run/trace/C3_60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
end 3
player 15 4
spawn grub 13 4
1.05 dash right
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(15.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(13.00,4.00,hp=2) | setup
t=0.717 frame=43 pos=(15.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(14.43,4.00,hp=2) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=1.067 frame=64 pos=(15.00,4.00) hearts=2 invulnerable=True dash_left=0.233 hurt_left=0.450 stun_left=0.000 | grub(14.46,4.00,hp=2) | dash {'direction': 'right'}
t=1.300 frame=78 pos=(15.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.217 stun_left=0.000 | grub(14.46,4.00,hp=2) | dash_end
t=1.517 frame=91 pos=(15.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(14.46,4.00,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=2.317 frame=139 pos=(15.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(14.46,4.00,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0}; down
t=3.000 frame=180 pos=(15.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.117 stun_left=0.000 | grub(14.46,4.00,hp=2) | end
```

### Round 2: @run/trace/LATE_60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
end 3
player 15 4
spawn grub 13 4
1.38 dash right
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(15.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(13.00,4.00,hp=2) | setup
t=0.717 frame=43 pos=(15.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(14.43,4.00,hp=2) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=1.400 frame=84 pos=(15.00,4.00) hearts=2 invulnerable=True dash_left=0.233 hurt_left=0.117 stun_left=0.000 | grub(14.46,4.00,hp=2) | dash {'direction': 'right'}
t=1.633 frame=98 pos=(15.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(14.46,4.00,hp=2) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=2.433 frame=146 pos=(15.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(14.46,4.00,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0}; down
t=3.000 frame=180 pos=(15.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.233 stun_left=0.000 | grub(14.46,4.00,hp=2) | end
```

### Round 2: @run/trace/B60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
end 4
player 8 4
spawn grub 10 4
0.2 dash right
1.0 dash left
1.9 dash left
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(10.00,4.00,hp=2) | setup
t=0.217 frame=13 pos=(8.27,4.00) hearts=3 invulnerable=True dash_left=0.233 hurt_left=0.000 stun_left=0.000 | grub(9.57,4.00,hp=2) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'right'}
t=0.450 frame=27 pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.77,4.00,hp=2) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=1.017 frame=61 pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(10.90,4.00,hp=2) | ignored {'action': 'dash', 'reason': 'dash not ready'}
t=1.283 frame=77 pos=(12.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(11.43,4.00,hp=2) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=1.917 frame=115 pos=(11.73,4.00) hearts=2 invulnerable=True dash_left=0.233 hurt_left=0.167 stun_left=0.000 | grub(11.46,4.00,hp=2) | dash {'direction': 'left'}
t=2.150 frame=129 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(11.09,4.00,hp=2) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=3.400 frame=204 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(8.59,4.00,hp=2) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=4.000 frame=240 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.200 stun_left=0.000 | grub(8.54,4.00,hp=2) | end
```

### Round 3: @run/trace/B30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
end 4
player 8 4
spawn grub 10 4
0.2 dash right
1.0 dash left
1.9 dash left
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(10.00,4.00,hp=2) | setup
t=0.233 frame=7 pos=(8.53,4.00) hearts=3 invulnerable=True dash_left=0.217 hurt_left=0.000 stun_left=0.000 | grub(9.53,4.00,hp=2) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'right'}
t=0.467 frame=14 pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(9.86,4.00,hp=2) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=1.033 frame=31 pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(10.99,4.00,hp=2) | ignored {'action': 'dash', 'reason': 'dash not ready'}
t=1.267 frame=38 pos=(12.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(11.46,4.00,hp=2) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=1.933 frame=58 pos=(11.47,4.00) hearts=2 invulnerable=True dash_left=0.217 hurt_left=0.133 stun_left=0.000 | grub(11.46,4.00,hp=2) | dash {'direction': 'left'}
t=2.167 frame=65 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(11.06,4.00,hp=2) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=3.400 frame=102 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(8.59,4.00,hp=2) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=4.000 frame=120 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.200 stun_left=0.000 | grub(8.54,4.00,hp=2) | end
```

### Round 3: @run/trace/C3_30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
end 3
player 15 4
spawn grub 13 4
1.05 dash right
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 pos=(15.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(13.00,4.00,hp=2) | setup
t=0.733 frame=22 pos=(15.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(14.46,4.00,hp=2) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=1.100 frame=33 pos=(15.00,4.00) hearts=2 invulnerable=True dash_left=0.217 hurt_left=0.433 stun_left=0.000 | grub(14.46,4.00,hp=2) | dash {'direction': 'right'}
t=1.333 frame=40 pos=(15.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.200 stun_left=0.000 | grub(14.46,4.00,hp=2) | dash_end
t=1.533 frame=46 pos=(15.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(14.46,4.00,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=2.333 frame=70 pos=(15.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(14.46,4.00,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0}; down
t=3.000 frame=90 pos=(15.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.133 stun_left=0.000 | grub(14.46,4.00,hp=2) | end
```

### Round 3: @run/trace/LATE_30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
end 3
player 15 4
spawn grub 13 4
1.38 dash right
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 pos=(15.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(13.00,4.00,hp=2) | setup
t=0.733 frame=22 pos=(15.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(14.46,4.00,hp=2) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=1.433 frame=43 pos=(15.00,4.00) hearts=2 invulnerable=True dash_left=0.217 hurt_left=0.100 stun_left=0.000 | grub(14.46,4.00,hp=2) | dash {'direction': 'right'}
t=1.667 frame=50 pos=(15.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(14.46,4.00,hp=2) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=2.467 frame=74 pos=(15.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(14.46,4.00,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0}; down
t=3.000 frame=90 pos=(15.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.267 stun_left=0.000 | grub(14.46,4.00,hp=2) | end
```
>>>END

<<<FILE repo/tests/test_game.py
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from game import DASH_DISTANCE, HEARTS, Game  # noqa: E402


def run(game, seconds):
    for _ in range(round(seconds * game.fps)):
        game.step()


class CombatTest(unittest.TestCase):
    def test_two_swipes_defeat_a_grub(self):
        game = Game(room="empty")
        game.spawn("grub", 9.2, 4)
        game.press("attack")
        run(game, 1.0)  # the grub closes in and bites; the hit-stun passes
        game.press("attack")
        run(game, 0.1)
        self.assertEqual(game.enemies[0].hp, 0)
        self.assertTrue(game.cleared)

    def test_swipe_misses_behind_the_player(self):
        game = Game(room="empty")
        game.spawn("grub", 7.0, 4)
        game.press("attack")
        self.assertEqual(game.enemies[0].hp, 2)

    def test_grub_bite_costs_a_heart(self):
        game = Game(room="empty")
        game.spawn("grub", 8.5, 4)
        run(game, 0.1)
        self.assertEqual(game.hearts, HEARTS - 1)

    def test_spitter_fires_every_two_seconds(self):
        game = Game(room="empty")
        game.spawn("spitter", 1, 1)
        run(game, 4.05)
        self.assertEqual(sum(1 for _, kind, _ in game.events if kind == "spit"), 2)


class DashTest(unittest.TestCase):
    def test_dash_covers_four_tiles_at_both_frame_rates(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.place_player(2, 4)
            game.press("dash", "right")
            run(game, 0.5)
            self.assertAlmostEqual(game.x, 2 + DASH_DISTANCE, places=6)

    def test_attack_during_dash_fires_when_it_ends(self):
        game = Game(room="empty")
        game.place_player(2, 4)
        game.press("dash", "right")
        run(game, 0.1)
        game.press("attack")
        self.assertFalse(any(kind == "attack" for _, kind, _ in game.events))
        run(game, 0.2)
        self.assertTrue(any(kind == "attack" for _, kind, _ in game.events))

    def test_dash_has_a_cooldown(self):
        game = Game(room="empty")
        game.press("dash", "left")
        run(game, 0.5)
        game.press("dash", "left")
        self.assertEqual(game.events[-1][1], "ignored")


class DashInvulnerabilityTest(unittest.TestCase):
    def hurt_then_wait(self, fps, wait):
        game = Game(fps=fps, room="empty")
        game.place_player(15, 4)  # against the wall: a rightward dash does not move the player
        game._hurt("grub")
        run(game, wait)
        return game

    def test_dash_begun_late_in_hurt_window_is_invulnerable_throughout(self):
        for fps in (30, 60):
            game = self.hurt_then_wait(fps, 0.7)  # about 0.1 s of post-hit window left
            hearts = game.hearts
            self.assertGreater(game.hurt_left, 0)
            self.assertLess(game.hurt_left, 0.25)
            game.press("dash", "right")
            self.assertGreater(game.dash_left, 0)
            while game.dash_left > 0:
                game.shots.clear()  # shots from earlier frames must not carry into the final frame
                if game.dash_left - game.dt > 1e-6:  # dash still active after this frame
                    game.shots.append([game.x, game.y, 0.0, 0.0])
                game.step()
                if game.dash_left > 0:
                    self.assertTrue(game.invulnerable, f"fps {fps} t={game.t}")
                self.assertEqual(game.hearts, hearts, f"fps {fps} t={game.t}")

    def test_invulnerable_until_hurt_window_ends_after_dash(self):
        for fps in (30, 60):
            game = self.hurt_then_wait(fps, 0.4)
            game.press("dash", "right")
            while game.dash_left > 0:
                game.step()
            self.assertGreater(game.hurt_left, 0)
            self.assertTrue(game.invulnerable)
            run(game, 0.3)
            self.assertEqual(game.hurt_left, 0.0)
            self.assertFalse(game.invulnerable)

    def test_plain_dash_is_invulnerable_for_exactly_its_duration(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.press("dash", "left")
            self.assertTrue(game.invulnerable)
            while game.dash_left > 0:
                self.assertTrue(game.invulnerable)
                game.step()
            self.assertFalse(game.invulnerable)


if __name__ == "__main__":
    unittest.main()
>>>END

## Your answer

- Write the outgoing Handoff as goals/G-001-dash-damage/06-qa-to-<recipient>.md with every section of studio/templates/handoff.md, in this order: Task, Context, Findings, Decisions already made, Constraints, Open questions, Expected output, Load. Your own report goes inside Findings. Address it to the recipient the incoming Handoff's Expected output names, if it names one.
- Wrap each file in a <<<FILE path … >>>END or <<<EDIT path … >>>END block (Output protocol in studio/execution.md).
