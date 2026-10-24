# Studio operation packet

operation: Step
goal: G-001
role: game-designer
incoming_handoff: goals/G-001-combat-monotony/03-studio-to-game-designer.md
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

<<<FILE goals/G-001-combat-monotony/03-studio-to-game-designer.md
---
kind: handoff
goal: G-001
seq: 3
from: studio
to: game-designer
stage: Diagnose
outcome: routed
---
# 03: studio → game-designer — ビルド 0.3 の戦闘が単調に感じられる原因の診断

## Task

プレイテスターが報告した体験の問題(A〜C)の原因を、デザインの言葉で診断し、D-001 の枠内で取れる解決策の選択肢を示す。解決策は決めず、選択肢と各案の影響を出す。

## Context

Goal G-001 の Owner の依頼は「戦闘が単調なので改善したい」。成功条件は、想定プレイヤーが戦闘中に、同じ行動の繰り返しではなく、位置取り・タイミング・敵の挙動への対応といった判断を実感できること。
Observe の段階で、プレイテスターがビルド 0.3 を全5部屋通してプレイし、観察報告(`goals/G-001-combat-monotony/02-playtester-to-studio.md`)を出した。原因の特定はまだで、これが最初の Diagnose になる。

## Findings

プレイテスターの観察(プレイヤー視点の体験のみ。実装や設計意図は読まずに書かれている)。

観察の制約: ドライランのため `sim/build-0.3.md` の記述から推定した体験であり、ゲームパッドの操作感、音、演出、各部屋の実時間は確認されていない。

体験の問題:

- **A. 戦闘が毎部屋同じ型で、進んでも変化しない(影響度 大)**
  - 全5部屋、最初から最後まで「位置を決めて、空になるまで振る」が通用した。プレイテスターは「2分目も15分目も同じ」と感じた。
  - 部屋4〜5の混成でも、角に下がり、Grub に向き直って振り、弾は横にずれる、という同じ型が通った。新しい判断は求められなかった。
- **B. 緊張感がほとんどない(影響度 大)**
  - 部屋1〜2: Grub はその場で攻撃ボタンを押すだけで2振りで倒れる。ダメージを受けるのは3体が同時に来たときだけ。「立って振っていれば終わる」と感じた。
  - 部屋3: Spitter の弾は遅く、横に1歩動けば避けられる。近づいて2回振れば倒せる。避けること自体は成立しているが、危うさや駆け引きはなかった。
- **C. ダッシュが戦闘で使われず、回避や位置取りの腕前が活きない(影響度 中〜大)**
  - ダッシュは部屋を早く横切るときにしか使わなかった。「ダッシュを戦闘で使う理由がない」。
  - プレイヤーとしての疑問: 「ダッシュは何のためにあるのか」「部屋が進んでも敵の脅威が変わらないのはなぜか」。

良かった点: 攻撃の結果は分かりやすく(2振りで倒れる)、操作の理解に迷いはなかった。Spitter の弾が遅く、避けられることは読み取れた。

別ルートで扱う件: 被弾直後にダッシュすると、ダッシュの途中でダメージを受けることが時々ある(問題 D、不具合の疑い)。`qa` が別に再現するので、この診断では原因や修正を扱わない。

## Decisions already made

- D-001: 戦闘は攻撃ボタン1つとダッシュのみ。新しい入力ボタンは Owner の承認なしには追加できない。深みは位置取り・タイミング・敵の挙動から生む。

## Constraints

- D-001 の枠内(攻撃とダッシュだけ、新ボタンなし)。枠を超える案が必要な場合は、その案を選択肢に含めるのではなく「D-001 の変更が必要」と明記して `game-director` に渡す(Owner のエスカレーション対象になる可能性がある)。
- ビジョンの柱: ワンボタン戦闘、短いラン(15–20分)、読める脅威(脅威は害を与える前に見える)。
- 小さなチームのため、既存のシステムを再利用する案を優先する。
- 30 FPS と 60 FPS の両方で正しく動く必要がある。
- 範囲外: 戦闘以外のシステム、ラン長、ビジョンの柱の変更。
- 観察の制約(上記)により、操作感や実時間に依存する原因は、確認が必要な仮説として区別して書く。

## Open questions

- A〜C の原因は何か。敵の種類・挙動、部屋の構成と進行、ダメージや無敵の数値、プレイヤーキットの幅などのうち、何が支配的か。複数の原因が重なっている場合は、それぞれの寄与を分けて示す。
- 診断の選択肢が、方向・優先度・スコープの本当の選択になるか。なる場合は、どの選択か。
- 選択肢のどれかが D-001 の変更や新ボタンを必要とするか。
- 設計文書(`design/combat.md`)が、被弾後のダッシュ中の無敵などの規則を未定義のままにしていると気づいた場合は、その事実を記録する。それは欠陥 D の期待される挙動に関わるが、D の再現は `qa` が行う。

## Expected output

- 診断と選択肢を、このステップの出力 Handoff の Findings に書く(`diagnose-experience`)。
  - 原因の診断: A〜C ごとに、設計文書に基づく原因と、根拠(設計文書のどこか、観察のどの部分か)を示す。確認できていない仮説は分けて書く。
  - 選択肢: D-001 の枠内の案を、プレイヤーの体験への効果、コスト(既存システムの再利用度)、リスク、元に戻しやすさとともに示す。推奨があれば理由とともに書く。
  - 検証すべき観点(後で Play や Review で確認できる、プレイヤーが観察できる形のもの)。
- 宛先は `game-director`(Decide)。選択肢が方向・優先度・スコープの選択であるか、D-001 の変更に触れる場合はその旨を明記する。診断の結果、`game-director` の判断が不要と判断した場合は、`studio` 宛てにして理由を書く。
- ゲームの仕様や数値の最終決定はまだ行わない(選択肢の段階)。

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/diagnose-experience.md
- Project: project.md#vision, project.md#player-profile, project.md#current-state, project.md#constraints, design/combat.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/02-playtester-to-studio.md
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

<<<FILE project.md#current-state
## Current state

Vertical-slice prototype, build 0.3: 5 rooms in one cave biome, 2 enemy types, player kit of attack
and dash. Dry-run only: "running the build" means reading `sim/build-0.3.md`.
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

<<<FILE goals/G-001-combat-monotony/02-playtester-to-studio.md
---
kind: handoff
goal: G-001
seq: 2
from: playtester
to: studio
stage: Route
outcome: done
---
# 02: playtester → studio — ビルド 0.3 の戦闘体験の観察報告

## Task

ビルド 0.3 を全5部屋通してプレイした観察報告を渡す。次の宛先(体験の問題は `game-designer`、不具合は `qa`)の判断は Studio が行う。

## Context

Goal G-001 の Observe ステップ。ビルド 0.3 を、戦闘に注目して、アクション志向・短く濃い走りを好み、ゲームパッドで遊ぶプレイヤーとして遊んだ。内部実装や設計意図は読んでおらず、推測もしていない。

## Findings

### 観察方法

- ドライランのため、実機の操作は行っていない。`sim/build-0.3.md`(プレイヤーに見える挙動の記述)を読むことを「ビルドを実行する」ことの代わりとした。
- 以下は、その記述から読み取れるプレイヤー視点の体験だけを書いている。
- 観察できなかったこと:
  - ゲームパッドでの操作感(入力の反応、スティックの感触)。
  - 音、演出、画面の見た目。
  - 各部屋にかかる実時間。
  - 記述にない敵の種類や挙動。
- 感じたことの記述は、この記述から推定した体験であり、実際に操作した感覚の記録ではない。

### セッション概要

全5部屋を通して遊んだ。

- 部屋1〜2: Grub が近づいてくる。
- 部屋3: Spitter が登場する。
- 部屋4〜5: 混成の部屋。

どの部屋でも、同じやり方で突破できた。

### 具体的な場面

1. **部屋1〜2(Grub)**
   - その場に立って攻撃ボタンを押すだけで、Grub は2振りで倒れる。近づかれる前に片付く。
   - ダメージを受けるのは3体が同時に来たときだけ。
   - 感じたこと: 「立って振っていれば終わる」。位置取りも回避も必要なく、緊張はほぼなかった。

2. **部屋3(Spitter)**
   - 弾は遅く、横に1歩動けば避けられる。
   - 近づいて2回振れば倒せる。
   - 感じたこと: 避けること自体は成立しているが、1歩動くだけの簡単な作業で、危うさや駆け引きはなかった。

3. **部屋4〜5(混成)**
   - 角に下がり、Grub に向き直って振る。弾は横にずれて避ける。この型がそのまま通用した。
   - 感じたこと: 敵の組み合わせが変わっても、やることは部屋1〜3と変わらない。新しい判断を求められなかった。

4. **ダッシュ**
   - ほとんど必要にならなかった。使うのは部屋を早く横切るときくらい。
   - 感じたこと: 「ダッシュを戦闘で使う理由がない」。ダッシュや位置取りに慣れたプレイヤーには、持ち味を使う場面がなかった。

5. **全体の流れ**
   - どの部屋も「位置を決めて、空になるまで振る」で終わる。
   - 感じたこと: 「2分目も15分目も同じ」。進んでも変化や盛り上がりを感じなかった。

6. **ダッシュ中のダメージ(不具合の疑い)**
   - 被弾した直後にダッシュすると、ダッシュの途中でダメージを受けることがあった。毎回ではなく、時々。
   - 感じたこと: ダッシュで逃げたのに当たるのは納得しづらい。ただし戦闘でダッシュを使う機会が少ないので、遭遇頻度は低い。

### 問題点と影響度

| # | 問題 | 影響度 | 根拠 |
|---|------|--------|------|
| A | 戦闘が毎部屋同じ型(立つ→振る→避ける)で、プレイが進んでも変化しない | **大** | 全5部屋、最初から最後まで同じやり方が通用し、「2分目も15分目も同じ」と感じた |
| B | 緊張感がほとんどない。被弾は3体同時のときだけ、弾も1歩で避けられる | **大** | 短く濃い走りを求めるプレイヤーには、危機感や手応えが足りない |
| C | ダッシュが戦闘で使われず、回避や位置取りの腕前が活きない | **中〜大** | ダッシュは部屋の移動にしか使わなかった |
| D | 被弾直後のダッシュ中にダメージを受けることがある | **小〜中** | 時々起きる。理不尽に感じる。頻度は低い |

### 良かった点

- 観察できた範囲では、攻撃の結果は分かりやすかった(2振りで倒れる)。操作の理解に迷いはなかった。
- Spitter の弾が遅く、避けられることは読み取れた。避ける動作自体は成立している。

### プレイヤーとしての疑問

- 「ダッシュは何のためにあるのか」。戦闘で使う場面がなかった。
- 「部屋が進んでも敵の脅威が変わらないのはなぜか」。

## Decisions already made

None

## Constraints

- 観察は `sim/build-0.3.md` の記述に基づく。ゲームパッド操作感や実時間は未確認。
- 原因の推測や、コードレベルの修正案は書いていない。

## Open questions

- 宛先の判断は Studio に委ねる。
  - A〜C は体験の問題なので `game-designer` が妥当。
  - D は不具合の疑いなので `qa` が妥当。

## Expected output

Studio が Route で宛先を確認する。体験の問題(A〜C)は `game-designer`、不具合の疑い(D)は `qa` に回す想定。

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, sim/build-0.3.md
- Decisions: none
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
