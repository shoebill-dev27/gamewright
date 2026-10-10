<!-- Verbatim output of dry-run probe C (fresh executor, no prior context): Step 7 of
lantern-depths G-002 run from handoff 07 alone. Kept as evidence; not part of the sample project. -->

---
kind: handoff
goal: G-002
seq: 8
from: gameplay-engineer
to: game-designer
stage: Design
outcome: handed-back
---
# 08: gameplay-engineer → game-designer — Spec does not define what a player hit does to a telegraphing enemy

## Task

Answer the open questions below so the telegraph, Charger and Shieldbearer changes (plan from step 6)
can be built and verified. The Build is handed back, not delivered to `qa`: V1 and V3 cannot be
signed off honestly while Q1 is open.

## Context

G-002, direction D-002. Step 7 asked for `design/enemy-telegraphs.md` to be implemented per the
Technical Director's plan. Before coding, every player-observable behavior the change would produce
was checked against the spec (`implement-change`, Method 1). Most are defined; the ones below are
not. No code was changed in this step (dry-run project; the sim files stand in for the repository).

## Findings

**Repository fact that creates the gap** (`sim/repo-notes.md`): an enemy hit by the player enters a
0.2 s Flinch state that interrupts whatever it is doing, including Attack, then returns to Chase.
`design/combat.md` does not describe this, `design/enemy-telegraphs.md` does not mention it, and
the plan's state list (Idle → Chase → Telegraph → Attack, plus Recovery for the Charger) leaves it
out. Once Telegraph, lunge, bash and Recovery exist, "player hits the enemy during X" becomes a
frequent, player-visible case, and the spec is silent on it.

**Defined by the spec, no question:** telegraph durations and the attack starting right after them
(V1); Charger approach to 5 tiles, direction lock at telegraph start, 6-tile / 0.3 s lunge, contact
damage during the lunge only, 1.0 s recovery in place (V2, V3); Shieldbearer speed, 90°/s turn,
front-arc block with spark, bash after a 0.6 s telegraph (V4, V5); room compositions (V7); dash
invulnerability intact (V6); Grub unchanged. A shield-bearing enemy deals no contact damage (the
spec names contact damage only for the Grub and the lunge).

**Not defined (details under Open questions):** Q1 hit reactions during Telegraph / lunge / bash /
Recovery, and whether a blocked hit staggers; Q2 Spitter cadence; Q3 aim/facing during a telegraph;
Q4 Shieldbearer attack trigger and post-bash behavior; Q5 Charger lunge edge cases.

**What is blocked and what can proceed:** the rule for whether Flinch applies while an enemy is in
Telegraph, Attack or Recovery (Q1) and the details in Q2–Q5 are blocked; I will not pick them, and
leaving the existing Flinch code untouched would silently choose Q1 option A, so that part is held
back too. Everything else can be built as soon as the answers are in: the telegraph state and
timers (V1), the Charger and its direction lock (V2), the Shieldbearer's facing and front-arc block
(V4, V5), and the room compositions (V7). I will deliver it to `qa` as one change after your answers
rather than in two rounds.

## Decisions already made

- D-001 (one-button combat), D-002 (enemy-side depth). Neither addresses hit reactions.

## Constraints

Reuse the enemy controller; 30 and 60 FPS; no new inputs; do not change the spec.

## Open questions

**Q1 (blocks the Build). What does a player hit do to an enemy that is in Telegraph, lunge, bash or
Recovery?** Cases at stake: (a) Spitter, Charger or Shieldbearer hit during its telegraph; (b)
Charger hit during the lunge; (c) Charger hit during its 1.0 s recovery; (d) Shieldbearer hit during
its bash; (e) a Shieldbearer attack that is blocked (damage 0, spark): does it stagger the enemy at
all? As written, the existing Flinch would cancel a telegraph or lunge and end Recovery early (back
to Chase, so the enemy moves), which contradicts V1 ("attack starts immediately after") and V3
("1.0 s with no movement or attack") as worded. Options I can see, with technical cost:
- A. Keep Flinch in every state. No new code, but V1 and V3 need an "unless hit" clause, and you
  must say what an interrupted attack does afterwards (does a cancelled Spitter shot restart the
  2 s cycle; does a Charger re-telegraph at once or approach again).
- B. No Flinch while in Telegraph, Attack or Recovery; damage still applies. Small guard where
  Flinch is entered; V1 and V3 stay true as written. Hit feedback for a hit that does not stagger
  is then yours to define.
- C. Flinch interrupts Telegraph only. Needs a cancel path out of Telegraph and a restart rule
  (delay before the next telegraph); V1 needs an "unless interrupted" clause.
- D. Differs per enemy type (e.g., one type interruptible, another not). One data flag per type and
  a test per type.
E3 (no single strategy clears every room) is the experience criterion most exposed to this choice,
but that is your and the Game Director's call, not mine.

**Q2. Spitter cadence.** The Spitter fires "every 2 s". Is the 0.5 s telegraph inside that cycle
(telegraph starts at 1.5 s, shot cadence unchanged) or added to it (a shot every 2.5 s)? The spec
says "Unchanged, except each shot is preceded by a 0.5 s telegraph", which supports either reading.

**Q3. Aim and facing during a telegraph.** The Charger's direction is explicitly locked at telegraph
start. For the Spitter, is the shot aimed at the player's position at telegraph start or at release?
For the Shieldbearer, does it keep walking and turning during its 0.6 s telegraph, and is the bash
direction its facing at telegraph start or at bash time? "Holds a wind-up pose" may mean no movement
or tracking, but that is not stated, and it decides whether circling behind a Shieldbearer works.

**Q4. Shieldbearer attack trigger and aftermath.** At what distance or condition does it start its
telegraph (the spec gives a bash reach of 1 tile but no trigger range)? After the bash, does it
return to Chase and may it telegraph again immediately, or is there a cooldown or recovery?

**Q5. Charger lunge edge cases.** After hitting the player during the lunge, does it continue the
full 6 tiles or stop at contact? If a wall ends the lunge early, does the 1.0 s recovery still apply
in full?

## Expected output

Answers to Q1–Q5 applied to `design/enemy-telegraphs.md` (reword V1/V3 or add an edge-case rule
wherever the answer requires it), a Decision if Q1 constrains work beyond this Goal or rejects a real
alternative, and a Handoff to `gameplay-engineer` to resume the Build. If an answer needs a direction
change or an Owner trigger fires, hand to `game-director` instead; if feasibility or cost of an
option is unclear, ask `technical-director`.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md, studio/skills/make-decision.md
- Project: project.md#vision, project.md#constraints, design/combat.md, design/enemy-telegraphs.md
- Decisions: decisions/D-002-enemy-side-combat-depth.md
- Previous handoff: goals/G-002-combat-monotony/07-technical-director-to-gameplay-engineer.md
