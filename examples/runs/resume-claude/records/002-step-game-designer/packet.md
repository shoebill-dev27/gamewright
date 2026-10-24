# Studio operation packet

operation: Step
goal: G-002
role: game-designer
incoming_handoff: goals/G-002-combat-monotony/05-studio-to-game-designer.md
next_seq: 6

## You may write

- goals/G-002-combat-monotony/06-game-designer-to-<recipient>.md
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

<<<FILE goals/G-002-combat-monotony/05-studio-to-game-designer.md
---
kind: handoff
goal: G-002
seq: 5
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 05: studio → game-designer — specify enemy-side combat depth (Option A) with player-observable acceptance criteria

## Task

Write a design spec for the Option A changes: telegraphed enemy attacks, a Charger enemy, a Shieldbearer enemy, and room compositions across the 5-room slice. The spec must be precise enough to plan, build and verify, and its acceptance criteria must be observable by a player.

## Context

Goal G-002: the Owner said "戦闘が単調なので改善したい" (combat feels monotonous). A playtest (01–02) found monotony. The diagnosis (03) offered options. The Game Director escalated the choice between enemy-side depth (A) and a heavy-attack button (B). The Owner chose **A** on 2026-10-10 and recorded it as D-002. The intended outcome: across the 5 rooms the player must make different decisions (where to stand, when to dash, which enemy first) instead of repeating one pattern.

## Findings

From the Owner's decision and the escalation (04); the playtest and diagnosis detail is in 02 and 03, which you load:

- Option A content: telegraphed attacks; new enemy **Charger** (rushes the player); new enemy **Shieldbearer** (guards the front); room compositions that ask where to stand, when to dash and which enemy first. The Game Director folded room-composition tuning (former Option C) into A.
- Symptoms Option A is meant to address (3 of the 4 observed): the same tactic clears every room; dash is not used in combat; enemies do not differ in how they must be fought. The 4th symptom, wanting a heavy hit, is deliberately not addressed in this Goal.
- The Owner's condition: keep one-button combat. Hold-to-charge on the attack button may be considered in the future but is **not** part of this Goal.

## Decisions already made

- D-001: combat uses one attack button plus dash. Unchanged.
- D-002 (Owner, 2026-10-10): fix the monotony through enemy behavior and room composition. No heavy-attack button, no new input, and no hold-to-charge in this Goal.

## Constraints

- No new input buttons beyond attack, dash and pause. Do not specify hold, charge or any new player action (D-001, D-002).
- Pillar 3, readable threats: every threat must be visible before it can hurt the player. Telegraphs must be visible and use the saturated orange/red threat language from the art direction. If a telegraph's visual treatment needs art direction beyond that, name it as an open question for `art-director` rather than deciding it.
- Must play correctly at both 30 and 60 FPS. Express timings so they are not frame-rate dependent (for example in seconds, or with an explicit statement of how they scale).
- Small team: prefer changes that reuse existing systems. Say which existing rules, such as damage and invulnerability rules in `design/combat.md`, each new behavior reuses.
- Stay inside the existing 5-room cave slice. No new biomes, meta-progression or run-length changes.
- Acceptance criteria must be qualitative and observable by a player or tester (for example what the player sees and can react to, and how rooms differ in the decisions they require). Numeric parameters belong in the spec's parameter section.

## Open questions

- Which of the 5 rooms get which compositions, so the player faces different decisions rather than a repeated pattern? Decide this in the spec.
- Whether any telegraph or Shieldbearer-guard presentation needs an `art-director` visual spec. If so, list it as a follow-up in your output instead of designing it yourself.
- Any case where D-001 or pillar 3 seems to conflict with the intended behavior. Do not resolve it yourself: hand back to `studio` with outcome `question`, and the Studio will route it to `game-director`.

## Expected output

A design spec with parameters and player-observable acceptance criteria, covering:

1. Enemy attack telegraphs (what the player sees, how long, and how dash interacts with them under the existing invulnerability rules).
2. Charger behavior.
3. Shieldbearer behavior, including how the player gets past the guard using only attack and dash.
4. Room-by-room compositions for the 5 rooms.

Write the spec into the project's design documents. Extend `design/combat.md` or add a new file, and name the file in Findings. Then write the outgoing Handoff to `technical-director` (stage Plan, Skill `technical-plan`). If the spec shows that scope must change, or needs a direction choice, hand back to `studio` with a question instead.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md#vision, project.md#player-profile, project.md#constraints, project.md#art-direction, design/combat.md, sim/build-0.3.md (current state of the slice), goals/G-002-combat-monotony/02-playtester-to-game-designer.md (playtest observations)
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-enemy-side-depth-one-button.md
- Previous handoff: goals/G-002-combat-monotony/03-game-designer-to-game-director.md (the diagnosis and options; the Owner's answer is in goals/G-002-combat-monotony/04-game-director-to-owner.md)
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
>>>END

<<<FILE project.md#art-direction
## Art direction

Dark caves lit by the player's lantern; warm light against cold blue-black. Threats use saturated
orange/red so they read against the dark.
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

<<<FILE goals/G-002-combat-monotony/02-playtester-to-game-designer.md
---
kind: handoff
goal: G-002
seq: 2
from: playtester
to: game-designer
stage: Diagnose
outcome: done
---
# 02: playtester → game-designer — Observation report, build 0.3

## Task

Diagnose the experience reported below: likely causes in design terms and solution options.

## Context

G-002, Owner request 「戦闘が単調なので改善したい」. Step 1 was a blind playtest of build 0.3; the
Playtester was not told the request.

## Findings

Observation report (method: dry-run, read `sim/build-0.3.md` as two runs of play).

- **Rooms 1–2:** Grubs walk straight at me. Standing still and swiping kills each before it arrives.
  "I'm just holding a corner and tapping."
- **Room 3:** Spitter shots are slow; one sidestep and they miss. Then I walk up and swipe twice.
- **Rooms 4–5:** the same corner-and-swipe works in mixed rooms. Attention dropped noticeably here.
- **Dash:** used almost only to cross rooms faster. "Nothing ever makes me dodge."
- **Enemies:** "They look different but I fight them all the same way."
- **Power:** "I kind of want a big, heavy hit — every swing feels the same." (said once, mid-run)
- **Defect seen:** once took damage partway through a dash right after being hit (already handled
  as G-001; mentioned for completeness).
- **Overall:** minute 2 and minute 15 feel the same. Impact: high — I would stop after one run.
- **Positives:** controls are crisp; the lantern-lit look is appealing.

## Decisions already made

None.

## Constraints

Observations only; no design intent was read.

## Open questions

None from the Playtester.

## Expected output

Diagnosis with options, to `game-director` for a direction decision.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/diagnose-experience.md
- Project: project.md, design/combat.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-002-combat-monotony/01-studio-to-playtester.md
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

<<<FILE decisions/D-002-enemy-side-depth-one-button.md
---
kind: decision
id: D-002
status: accepted
decided_by: owner
goal: G-002
date: 2026-10-10
supersedes: none
---
# D-002: Fix combat monotony through enemy behavior; keep one-button combat

## Decision

The Owner chose Option A of escalation `goals/G-002-combat-monotony/04-game-director-to-owner.md`.
Combat depth for G-002 is built on the enemy side while the player kit stays attack plus dash:

- Telegraphed enemy attacks.
- Two new enemy types: a Charger (rushes the player) and a Shieldbearer (guards the front).
- Room compositions that ask the player where to stand, when to dash and which enemy to hit first.
  This is the former "Option C", folded into A by the Game Director.

D-001 (one attack button plus dash) stays in force and is not changed. No heavy-attack button and no
new input are added.

Owner's own words (2026-10-10):

> Aで。ワンボタンは守りたい。ただ、同じボタンの長押しで溜め攻撃、みたいな案なら将来は検討してもいい。今回はやらない。

Conditions and limits:

- Hold-to-charge on the same attack button is **not** part of G-002 and must not appear in the spec,
  plan or build for this Goal.
- The Owner is open to hold-to-charge as a possible future direction. It would be a separate Goal
  and a new Owner decision. This note does not approve it.

## Rationale

The observed monotony comes mainly from enemies that demand no positioning or timing. Option A
addresses that directly. It protects pillar 1 (one-button combat) and D-001, is reversible, and
leaves Option B (or a hold-charge variant) open for later. The only evidence for B was one player
remark.

## Alternatives considered

- **Option B: add a heavy-attack button.** It would replace D-001 and answers the "I want a heavy
  hit" remark, but only partly addresses "the same tactic clears every room". The Owner declined it.
- **Room-composition tuning alone.** The Game Director judged its ceiling too low on its own, so it
  is included in A.
- **Hold-to-charge on the attack button.** Raised by the Owner as a possible future idea. Explicitly
  not for this Goal.

## Revisit when

- The re-playtest after Option A is built still shows that the cause is "the player has too few
  actions available". This matches D-001's own revisit condition.
- The Owner wants to explore hold-to-charge or any other player-side option. That would be a new Goal
  and a new Owner decision.
>>>END

<<<FILE goals/G-002-combat-monotony/03-game-designer-to-game-director.md
---
kind: handoff
goal: G-002
seq: 3
from: game-designer
to: game-director
stage: Decide
outcome: done
---
# 03: game-designer → game-director — Diagnosis and direction options for monotonous combat

## Task

Choose the direction for making combat less monotonous, or escalate if the choice is not the
Studio's.

## Context

G-002 「戦闘が単調なので改善したい」. Blind playtest of build 0.3 in 02.

## Findings

Symptoms (evidence in 02):

- **S1** One dominant strategy — corner and swipe — clears every room.
- **S2** The dash has no combat purpose.
- **S3** Enemies differ in looks, not in how they must be fought.
- **S4** The player wants offense with more weight ("a big, heavy hit").

Causes:

- **C1** No enemy forces repositioning: Grubs walk straight in; Spitter shots are trivially avoided.
- **C2** No telegraphed threats, so dash timing is never tested.
- **C3** Room compositions all ask the same question.
- **C4** The single attack offers no choice or commitment.

Options:

| | Option | Addresses | Cost | Fit |
|---|---|---|---|---|
| A | **Enemy-side depth:** telegraphed attacks, two new enemies that demand dashing and flanking (Charger, Shieldbearer), rooms that each ask a different question | S1, S2, S3 | medium: extends the shared enemy controller | Fully within the pillars and D-001 |
| B | **Player-side depth:** add a heavy attack on a second button | S4, partly S1 | medium: new input, animations, balance pass | **Conflicts with D-001** (Owner decision: no new combat inputs) |
| C | **Encounters only:** re-mix rooms, add hazards, keep current enemies | S1 partly | low | Within pillars; low ceiling — enemies stay trivially readable |

Designer recommendation: A, with C's room re-mixing folded in. A choice involving B is not mine or
the Director's to make alone: it changes an Owner Decision.

Unknown: whether S4 is a lasting need or will fade once fights demand more (only one remark so far).

## Decisions already made

- D-001: one attack button plus dash; new combat inputs need the Owner.

## Constraints

Pillars: one-button combat, short runs, readable threats. Small team; reuse systems.

## Open questions

- Which direction: A, B or C?

## Expected output

A direction Decision, or an Owner escalation if a trigger fires.

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/make-decision.md, studio/skills/prepare-owner-escalation.md
- Project: project.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-002-combat-monotony/02-playtester-to-game-designer.md
>>>END

<<<FILE goals/G-002-combat-monotony/04-game-director-to-owner.md
---
kind: escalation
goal: G-002
seq: 4
from: game-director
to: owner
status: resolved
decision: D-002
---
# 04: Owner decision needed — 戦闘の深みを「敵側」で作るか「プレイヤー側」で作るか

## Question

戦闘の単調さを、ワンボタンのまま敵の行動で解決しますか（A）、それとも重攻撃ボタンを追加して D-001 を変更しますか（B）？

## Why this needs the Owner

- **Owner が決めた Decision（D-001「攻撃1ボタン＋ダッシュ」）が変わりうる**選択肢が、証拠上も有力な方向として残っているため。
- **大きな方向性が複数あり**、現時点の証拠（Playtest 1回分）ではどちらが正しいか決着しないため。

Studio の権限内の判断は済ませています。案 C（部屋構成の調整のみ）は単独では天井が低いため、Director 判断で A に組み込みました。

## Options

### Option A — 敵側で深みを作る（ワンボタン維持）

予兆（テレグラフ）付きの攻撃と、新しい敵 2 種（突進してくる Charger、正面をガードする Shieldbearer）を追加し、部屋ごとに「どこに立つか・いつ避けるか・どれから倒すか」を問う構成にします。
単調さの症状 4 つのうち 3 つ（同じ戦法で全部屋を突破できる／ダッシュを戦闘で使わない／敵ごとの戦い方の差がない）に効きます。コストは中。D-001 と柱をすべて守ります。後から B を追加することも妨げません。
If chosen: 詳細設計（Game Designer）→ 技術計画（Technical Director）→ 実装 → QA → 再 Playtest → Director レビュー。

### Option B — プレイヤー側で深みを作る（重攻撃ボタン追加）

2 つ目の攻撃ボタンとして重攻撃を追加します。「重い一撃が欲しい」という声には直接応えますが、「同じ戦法で全部屋を突破できる」問題には部分的にしか効きません。コストは中（入力・アニメーション・バランス調整）。
**D-001 を変更**することになり、「コンボを覚えたくない層でも遊べる」という前提が変わります。
If chosen: D-001 を置き換える Decision を記録 → 重攻撃の詳細設計 → 技術計画 → 実装 → QA → 再 Playtest → レビュー。

## Studio recommendation

Option A。

## Reasoning

- 観察された単調さの主因は「敵が位置取りやタイミングを要求しないこと」で、A はそこに直接効きます。
- B を支える証拠は、プレイヤーの 1 回の発言だけです。
- A は柱と Owner の過去の判断を守り、可逆で、B を将来選ぶ余地も残します。

推奨を変える条件：A の実装後の再 Playtest でも、単調さの原因が「プレイヤーの取れる行動が少ないこと」だと示された場合。これは D-001 の「再検討条件」とも一致します。

## Meanwhile

なし。以降の工程はすべてこの判断に依存するため、停止しています。

## Owner decision required

A / B — 選んだ案と、条件があれば併せて返答してください。

---

**Owner response (2026-10-10):** Aで。ワンボタンは守りたい。ただ、同じボタンの長押しで溜め攻撃、みたいな案なら将来は検討してもいい。今回はやらない。

**Resolved:** Recorded as D-002 (`decisions/D-002-enemy-side-depth-one-button.md`).
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
