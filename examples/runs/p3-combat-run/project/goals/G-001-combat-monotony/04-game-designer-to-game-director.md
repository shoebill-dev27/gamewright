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
