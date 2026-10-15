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
