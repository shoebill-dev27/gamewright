# Studio operation packet

operation: Step
goal: G-001
role: gameplay-engineer
incoming_handoff: goals/G-001-dash-damage/16-studio-to-gameplay-engineer.md
next_seq: 17

## You may write

- goals/G-001-dash-damage/17-gameplay-engineer-to-<recipient>.md

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

<<<FILE goals/G-001-dash-damage/16-studio-to-gameplay-engineer.md
---
kind: handoff
goal: G-001
seq: 16
from: studio
to: gameplay-engineer
stage: Build material reconciliation
outcome: routed
---
# 16: studio → gameplay-engineer — 既存の模擬資料と変更記述を照合し、検証入力を整える

## Task

`15-gameplay-engineer-to-studio.md` の模擬実装変更と、既存の `sim/build-0.4.md`・`sim/repo-notes.md` を照合する。独立 QA が使える実在資料と不足を特定し、必要な補完をプロジェクトの dry-run 規約に従って具体化して Studio に返す。

## Context

G-001 はダッシュ中の被ダメージ不具合を既存仕様に従って修正する Goal。QA が AC-1〜AC-6 を作成し、technical-director が計画と D-003 を作成した。Build は Handoff 15 に変更を定義して完了したが、同 Handoff は simulator の資料生成を未実施と報告している。

現在の存在一覧には `sim/build-0.3.md`、`sim/build-0.4.md`、`sim/repo-notes.md` がある。Handoff 15 の指定生成先 `sim/build-0.3-G001-15.md` と `sim/qa-G001-15.md` は存在しないため、今回の Load には含めない。

## Findings

- Studio が確認できたのは Handoff 15 の内容とファイル一覧。`sim/build-0.4.md` の本文、変更反映、試行記録は未確認。
- ファイル名の違いだけでは反映失敗とも成功とも判定できない。既存資料が対象変更を含むか、明示されたビルド識別子と内容から確認する必要がある。
- Handoff 15 の期待結果、配置案、予定時刻、予定件数は観察証拠ではない。
- この Step は検証入力の照合・補完であり、独立 QA の pass / fail を出す Step ではない。

## Decisions already made

- D-001: 攻撃・ダッシュ・ポーズ以外の入力を追加しない。
- D-002: Owner の部分的観察を使って元の修正 Goal を継続する。追加計測を開始条件にしない。
- D-003: 無敵を発生源別に管理し、論理和で判定する。防いだ命中で保護を延長しない。

上記は既存 Handoff の要約。詳細は Load の Decision 本文に従う。

## Constraints

- 仕様、AC、承認済み計画の範囲内で作業する。ゲーム内容や技術方式を Studio の判断として追加しない。
- 既存資料が十分なら、指定ファイル名に合わせるためだけの再生成は求めない。実在する資料と対象変更の対応を報告する。
- 未生成ファイルを作成済みと記さない。観察のない条件を期待結果で埋めない。
- 実コード、実機試験、自動テストを実施したと扱わない。模擬資料による確認と実測を区別する。
- 全4環境、必要な接触・弾命中、AC と追加回帰の資料充足を確認する。無効試行や未確認条件を分離する。
- クールダウン起点、完全同時イベント、入力不能中の予約を新しく定義しない。仕様判断が必要なら game-designer、計画が成立しなければ technical-director への差し戻し事項を Studio に報告する。
- 原因説明、実装理由、自己評価は QA 向け資料から分離する。自己評価は outgoing Handoff の Sender assessment に置く。

## Open questions

1. `sim/build-0.4.md` と `sim/repo-notes.md` は Handoff 15 の変更に対応しているか。明示された識別子、反映内容、不一致は何か。
2. AC-1〜AC-6 と追加回帰について、どの環境・命中源・枝の観察が実在し、どこが不足しているか。
3. 既存クールダウン起点、命中成立、実際のイベント順序、ハート変化を確認できるか。
4. 不足は具体的な simulator 更新依頼で補えるか。それとも Role では生成できない入力や仕様・計画判断が必要か。

## Expected output

Studio 宛ての Handoff を作成し、次を含める。

- 読んだ既存資料、明示されたビルド識別子、Handoff 15 との対応と不一致。
- QA に渡せる実在ファイル・節の一覧。仕様・期待値と観察記録を分離し、原因説明や自己評価を混ぜない。
- AC・回帰ごとの資料充足表。全4環境と必要命中源・枝を区別し、観察済み、有効性不足、未確認を明示する。
- 補完が必要なら、対象、変更内容、試し方、生成すべき観察を記述する。dry-run 規約上の変更記述と simulator による反映完了を区別する。
- 解消できない場合は不足入力と理由を具体化し、必要な担当判断を報告する。同じ不足を根拠なく再依頼し続けない。

作業完了は `done`、必須入力や担当外判断で進めない場合は `question` とし、`to: studio` で返す。独立 Verify の判定は QA に残す。

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#vision
- Project: project.md#constraints
- Project: design/combat.md
- Project: sim/repo-notes.md
- Project: sim/build-0.3.md
- Project: sim/build-0.4.md
- Project: goals/G-001-dash-damage/11-qa-to-studio.md
- Project: goals/G-001-dash-damage/13-technical-director-to-studio.md
- Decisions: decisions/D-001-one-button-combat.md
- Decisions: decisions/D-002-resume-with-owner-observations.md
- Decisions: decisions/D-003-independent-invulnerability.md
- Previous handoff: goals/G-001-dash-damage/15-gameplay-engineer-to-studio.md
>>>END

<<<FILE studio/roles/gameplay-engineer.md
---
kind: role
id: gameplay-engineer
load_forbid: goals/*/*-playtester-to-*.md
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

<<<FILE sim/repo-notes.md
# Simulated repository notes — lantern-depths (build 0.4)

Implemented change identifier: `0.3-G001-15`.
Current build description: `sim/build-0.4.md`.
`sim/build-0.3.md` describes the previous build.

Implementation facts only — never load this for a Playtester.

- Enemies share one controller with the states Idle, Chase and Attack. Per-type behavior is data (speed, HP, attack type) plus a small per-type attack routine.
- Hit reaction: an enemy hit by the player enters a 0.2 s Flinch state that interrupts whatever it is doing (including Attack), then returns to Chase. Not described in `design/combat.md`.
- Damage: the player's attack is a short arc hitbox in front of the player. Enemies take damage on overlap. There is no concept of blocking or facing yet.
- Movement: simple steering; walls stop movement.
- Game loop uses variable delta time; 30 and 60 FPS supported. Desktop keyboard and gamepad are supported.
- Tests: none for invulnerability or enemies.

## Player invulnerability

- The writable shared invulnerability flag is removed. `dashProtectionActive` and `hitProtectionActive` are independently maintained. Effective invulnerability is their logical OR.
- An accepted dash starts dash protection only. It does not modify hit protection or its expiration.
- Dash protection follows the existing dash continuation state and ends in the existing dash termination processing. No separate dash-protection timer is added.
- A successful damaging hit starts hit protection until 0.8 s after that hit.
- Hit-protection expiration clears only hit protection. Dash termination clears only dash protection.
- Input loss ends after the existing 0.3 s duration without clearing hit protection.
- All previous invulnerability reads use the OR result. The old shared writes at dash start, dash end, damage application and hit-timer expiration are replaced by the corresponding source-specific operations. Any cached derived value is not directly overwritten by individual timers.

## Contact and projectile damage

Grub contact and Spitter projectile hits both enter the same player-damage gate:

1. Contact or projectile impact is established.
2. Effective invulnerability is checked before heart loss or input loss.
3. If either protection is active, player-damage processing returns without changing hearts, input loss, hit protection or its expiration.
4. Otherwise, the hit removes one heart, applies 0.3 s of input loss and starts 0.8 s of hit protection.

Neither hit source retains a bypass that directly manipulates the removed shared flag. Non-damage impact behavior, including existing projectile disappearance, is unchanged.

Blocked hits neither start hit protection nor extend either protection. Consequently, expiration of one source cannot cancel the other, and hits after both sources have ended can cause normal damage.

## Preserved behavior

- Dash distance remains four tiles and duration remains 0.25 s.
- Dash cooldown remains 0.6 s with its existing origin.
- An attack queued during a dash activates once at dash termination.
- Existing variable-delta-time and timer mechanisms are reused; no fixed-frame replacement is introduced.
- Existing event scheduling is unchanged. The damage-gate order does not establish priority between coincident dash transitions and hits.
- Enemy AI, Flinch, movement, walls, attack damage and recovery are unchanged.
- No new input buttons or save-format changes are defined.

## Limits of available implementation detail

- The cooldown origin is not specified in the supplied repository description and cannot be identified as dash start or dash end.
- At 30 FPS, the 0.25 s dash duration is not an integer number of frame intervals. Exact timer-update ordering, movement integration at the final interval and the observable termination frame are unspecified. No rounding tolerance or new timing policy is introduced.
- Exact collision geometry, enemy speeds, room coordinates, projectile trajectories and firing phases are unavailable. Frame-by-frame collision trials, numerical initial heart counts and valid-trial totals cannot be reconstructed from these inputs.
- The specified scenario times are exercise targets, not measured event logs. No independent QA result or executed test record is available.
- Input buffering during input loss, coincident-event priority, and unspecified save/restore or dash-interruption behavior remain undefined by this change.
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

<<<FILE sim/build-0.4.md
# Build 0.4 — what playing it looks like

Build identifier: 0.3-G001-15.

The following behavior applies on desktop with keyboard or gamepad, at both 30 and 60 FPS.

- Room 1–2: Grubs crawl toward you. Standing still and pressing attack kills each in two swipes before it reaches you. Outside protected periods, you take damage if three arrive at once.
- Room 3: Spitter projectiles are slow; a single step sideways avoids them. You can walk up and defeat a Spitter with two swipes.
- Room 4–5: backing into a corner, facing the Grubs and swiping remains effective. Stepping aside avoids projectiles.
- Dashing is rarely necessary to clear rooms. Holding position and swiping remains effective throughout a run.

## Dash and damage

A dash covers four tiles over 0.25 seconds on an unobstructed straight path. Walls still stop movement. Grub contact and Spitter projectile hits cost no hearts throughout the dash, including its early and late portions.

Without protection from a dash or recent damage, either kind of hit removes one heart and prevents input for 0.3 seconds. Input then recovers, while further hits remain harmless until 0.8 seconds after the damaging hit.

Dashing as soon as input recovers does not expose you to damage during the dash. Ending that dash does not cut short the remaining protection from the earlier hit.

For example, after taking damage at 0 seconds:

- If you begin a dash around 0.70 seconds, a contact or projectile hit around 0.85 seconds costs no additional hearts while you are still dashing. A hit around 1.10 seconds removes one heart, provided you have not started another dash or taken another damaging hit.
- If you begin a dash around 0.34 seconds, a hit around 0.70 seconds costs no additional hearts even though the dash has ended. A hit around 0.95 seconds removes one heart under the same conditions.
- Without another dash, contacts around 0.15, 0.45 and 0.70 seconds cost no additional hearts. Input is unavailable during the first 0.3 seconds and available afterward.

These timings describe hits that actually connect strictly before or after the stated boundaries.

Harmless hits do not start another period of input loss or postpone when damage can occur again. Multiple harmless contacts or projectile hits have the same result. With no preceding damage, hits during a dash leave hearts unchanged, and a hit 0.40 seconds after dash start removes one heart once that dash has ended. Projectile disappearance on impact remains unchanged.

## Other controls and timing

An attack pressed during a dash waits until the dash ends, then occurs once. Dash reuse remains restricted by the existing 0.6-second cooldown. Attack, dash and pause remain the available action buttons.

At 60 FPS, 0.25 seconds spans 15 frame intervals. At 30 FPS, it falls between seven and eight frame intervals; the dash ending is visible on an updated frame rather than at a separately displayed halfway point. The exact displayed ending frame and the outcome of a hit coinciding precisely with dash start or end are not established here. The protection behavior above applies to hits clearly inside the dash or clearly within the protection following damage at either frame rate.
>>>END

<<<FILE goals/G-001-dash-damage/11-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 11
from: qa
to: studio
stage: Observe
outcome: done
---
# 11: qa → studio — ダッシュ中被ダメージの仕様不一致と修正受け入れ条件

## Task

本報告を基に、既存仕様を維持する修正の技術調査・計画へルーティングする。修正後は更新された模擬ビルドを独立した QA に渡し、下記の受け入れ条件を検証する。

## Context

G-001 は「ダッシュ中なのにダメージを受けることがある」という不具合の修正である。D-002 により Owner の部分的な観察を使って継続することが決まった。

今回は `studio/skills/reproduce-defect.md` に従い、Owner の観察、`design/combat.md`、`sim/build-0.3.md` を照合した。dry-run のためビルド実行に相当する作業は模擬資料の読解であり、新しい実測や試行は行っていない。Observe の評価完了であり、修正完了・Verify 合格ではない。

## Findings

### 不具合報告

**件名:** 被弾後のダッシュ中に再度ダメージを受けることがある。

**仕様上の期待結果:** `design/combat.md` の Player kit は、ダッシュを 0.25 秒、その全時間を無敵と定義している。先行する被弾の有無にかかわらず、ダッシュが継続している間の Grub 接触や Spitter 弾の命中によってハートが減ってはならない。被弾時は 1 ハート減少、0.3 秒の入力不能、その後は被弾から 0.8 秒まで無敵となる。

**実際の結果と根拠:**

| 根拠 | 得られた情報 | 確認の限界 |
|---|---|---|
| `sim/build-0.3.md` 末尾のプレイヤー観察 | 被弾直後にダッシュすると、ときどきダッシュ途中でダメージを受けると明記されている | 敵種、入力方式、FPS、イベント時刻、頻度は不明 |
| Owner の観察（D-002） | 部屋1〜2、PC・60 FPS・ゲームパッド。Grub に噛まれ、硬直終了後に少し待ってダッシュすると、後半で別の Grub に接触して 1 ハート減少 | 被弾から約 0.5〜0.8 秒、約 10 回中 6 回はいずれも体感・概数 |
| Owner の比較観察（D-002） | 被弾直後すぐのダッシュと未被弾時のダッシュでは発生を観察していない | 比較試行数と実際のダッシュ開始時刻が不明。非発生の保証ではない |
| Owner の追加観察（D-002） | Spitter 弾でも 1 回あった | 部屋、タイミング、先行被弾源などの詳細は不明 |

模擬資料だけからも「ダッシュ途中の被ダメージ」と「全ダッシュ時間無敵」の仕様不一致を確認できる。一方、Owner の詳細条件を独立した試行で再現したとは判断しない。最小の安定再現手順と発生境界は未確定である。

模擬資料の「被弾直後」と Owner の「硬直終了後に少し待つ」は、同じタイミングを意味するとは限らない。どちらも正確な時刻がなく、比較条件の一致や矛盾の解消まではできない。

**重大度:** プレイ体験を損なう。仕様上安全な回避行動中にハートを失い、回避の信頼性に影響する。進行不能を示す資料はない。頻度は模擬資料の「ときどき」と Owner の概数のみで、測定済みの発生率はない。

### 後続で実施する再現・比較手順

以下は検証手順であり、実施済みの結果ではない。

1. PC・60 FPS・ゲームパッドで、部屋1〜2の Grub 接触を対象にする。ダッシュが使用可能な状態とハート数を記録する。
2. Grub に噛まれて初回の 1 ハート減少を確認する。初回被弾、入力不能終了、ダッシュ入力・実際の開始、再接触、ダッシュ終了とハート変化を区別して記録する。
3. 入力可能になってから少し待ち、Owner の体感範囲である被弾後約 0.5〜0.8 秒を探索対象としてダッシュする。別の Grub とダッシュ中に接触する配置を用いる。総敵数、位置、方向、実際の開始時刻を記録する。
4. 先行被弾後の待ち時間だけを変え、入力可能になった直後にダッシュする比較を行う。入力不能中の予約操作は前提にしない。
5. 先行被弾がない状態でもダッシュ中に Grub と接触する比較を行う。
6. 命中源を Spitter 弾に変えて同じ比較を行う。先行被弾源は別途記録し、Owner の詳細条件が判明したとは扱わない。
7. 各条件を PC の 30 / 60 FPS とキーボード・ゲームパッドの全4組合せで確認する。各試行の条件・回数・発生数を残す。

比較対象でもダッシュ中の接触・命中を確認する。攻撃が届かなかった試行だけでは、無敵の検証にはならない。

### 修正の受け入れ条件

以下は `design/combat.md` に基づく。全条件を PC・30 / 60 FPS・キーボード / ゲームパッドで検証する。現時点の判定はすべて未検証。

| ID | 条件・操作 | プレイヤーから観察できる期待結果 |
|---|---|---|
| AC-1 | 被弾していない状態でダッシュし、Grub 接触／Spitter 弾命中を受ける | ダッシュ中はハートが減らない |
| AC-2 | 被弾後、0.3 秒の入力不能が終了してから直ちにダッシュし、接触／弾命中を受ける | 実際のダッシュ中はハートが減らない |
| AC-3 | 被弾後に間をおいてダッシュし、ダッシュ途中で被弾後 0.8 秒を経過する条件を作る。その経過後かつダッシュ終了前に接触／弾命中を受ける | ダッシュ後半もハートが減らない |
| AC-4 | ダッシュ終了後も被弾後 0.8 秒までの無敵時間が残る条件で、終了後かつ無敵時間内に接触／弾命中を受ける | ハートが減らない |
| AC-5 | ダッシュ中でも被弾後の無敵時間中でもない状態で Grub に接触する | 通常どおり 1 ハート減り、0.3 秒入力不能となる。その後、被弾から 0.8 秒までは追加のハート減少がない |
| AC-6 | 通常のダッシュとダッシュ中の攻撃入力を確認する | 4 タイルを 0.25 秒で移動し、クールダウン 0.6 秒を維持する。ダッシュ中の攻撃は終了時に発動する |

AC-3 の検証用設定例は「被弾後 0.7 秒にダッシュ開始、0.85 秒に命中」である。仕様上のダッシュ終了は 0.95 秒となるため、被弾由来の無敵終了後にもダッシュ中の保護を検証できる。これは仕様から算出した予定条件であり、Owner の計測値や実施結果ではない。各 FPS で実際のイベント順序を確認し、完全同時の境界は避ける。

入力不能中の予約入力、ダッシュ開始・終了と命中が完全同時の場合の優先順位は、この受け入れ条件で新たに定義しない。それらの判断が修正や検証に必要になった場合は game-designer へ戻す。

### 解消した不足と具体的な残件

**解消した事項:**

- 必須の戦闘仕様と模擬ビルド本文が揃い、期待結果と既知の仕様不一致を照合できた。
- Owner の追加観察から、優先調査条件、比較条件、環境、主な命中源を設定できた。
- 修正へ渡す不具合報告と受け入れ条件を作成できた。追加の Owner 計測を Observe 再開の必須条件とする必要はない。

**技術調査・計画に残る事項:**

- 実装原因と変更箇所は未確認。担当 Role が `sim/repo-notes.md` 等の実装資料から調査する必要がある。本 packet に同資料はなく、QA は原因や方式を断定しない。
- 安定再現に必要な配置・時刻と発生境界は未確定。技術調査と後続の模擬検証で扱い、既存資料から得られる測定値として補完しない。
- Spitter の詳細、30 FPS、キーボードは未確認。修正後の検証対象に含める。
- Verify には、変更を反映した模擬ビルドと、各受け入れ条件を評価できる観察資料が必要。資料が結果を示さない項目は合格にしない。

**ルーティング判断:** 不具合報告は修正の技術調査・計画へ渡せる。QA の追加 Observe を同じ資料で繰り返す必要はない。ただし本報告だけでは具体的な Build 変更内容は定まっていないため、Studio は担当 Role に実装資料を渡して調査・計画を進める。修正を実施した、または合格したという判断ではない。

## Decisions already made

- `decisions/D-002-resume-with-owner-observations.md`: 部分的な観察を使って元の修正 Goal を継続する。仕様変更や修正完了の承認ではない。
- 既存の入力制約: Owner 承認なく攻撃・ダッシュ・ポーズ以外の入力を追加しない。

## Constraints

- 既存仕様の不具合修正に限定し、戦闘の方向性変更や無関係なバランス調整はしない。
- Owner の体感、模擬資料の記述、今後の検証結果を区別する。
- QA は実装を変更せず、原因や修正方式を決定しない。
- 仕様未定義の境界処理が必要になった場合は game-designer に判断を返す。

## Open questions

- 技術担当は、既存の実装資料から修正箇所と変更内容を特定できるか。
- 後続の模擬ビルドで、AC-1〜AC-6 と全4環境組合せの観察結果をどのように提供するか。

現時点で Owner に追加回答を求めなければ調査へ進めない質問はない。

## Expected output

Studio が技術調査・計画へルーティングし、必要な実装資料を次の packet に含める。その後、具体的な変更内容と検証手順を備えた Build、更新済み模擬ビルドを用いる独立した Verify へ進める。

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: project.md#vision
- Project: project.md#current-state
- Project: project.md#constraints
- Project: design/combat.md
- Project: sim/build-0.3.md
- Decisions: decisions/D-002-resume-with-owner-observations.md
- Previous handoff: goals/G-001-dash-damage/10-studio-to-qa.md
>>>END

<<<FILE goals/G-001-dash-damage/13-technical-director-to-studio.md
---
kind: handoff
goal: G-001
seq: 13
from: technical-director
to: studio
stage: Build routing
outcome: done
---
# 13: technical-director → studio — 無敵の競合解除を分離する修正計画

## Task

本計画と D-003 を gameplay-engineer に渡し、Build に進める。Build の変更を反映した模擬資料を用意した後、独立した QA に AC-1〜AC-6 の Verify を依頼する。

## Context

G-001 はダッシュ中に被害が発生する不具合の修正である。D-002 により Owner の部分的な観察を使って継続している。

本 Step は提供された `studio/skills/technical-plan.md` を適用し、仕様、実装資料、模擬ビルド、QA 報告を照合した。実リポジトリは存在せず、コード実行・新しい再現試行・修正は行っていない。以下の時刻例は検証用の予定条件であり、測定結果ではない。

## Findings

### 診断と根拠

`sim/repo-notes.md` の Player invulnerability には、次の実装が明記されている。

1. 無敵は一つのオン／オフフラグ。
2. ダッシュがフラグをオンにし、0.25 秒タイマーを開始する。
3. 被弾もフラグをオンにし、被弾から 0.8 秒で終了するタイマーを開始する。
4. 各タイマーは終了時に共通フラグをオフにする。

この構造では、一方のタイマー終了が他方の保護を解除する。実装資料に根拠のある原因であり、単に Owner の時刻の重なりから推測したものではない。

たとえば被弾時刻を t=0、ダッシュ開始を t=0.70 とすると、仕様上のダッシュ終了は t=0.95 となる。現方式では t=0.80 に被弾タイマーが共通フラグをオフにするため、t=0.85 の命中を防げなくなる。この順序は Owner の「待ってからダッシュし、後半に被害」と整合する。ただし実際の配置やフレーム処理順序を含む再現は未実施であり、Owner の発生率や Spitter の一例まで実証したものではない。

逆順の欠陥も導ける。入力不能終了後、たとえば t=0.34 にダッシュを開始すると終了予定は t=0.59。現方式ではこの終了が、t=0.80 まで残るべき被弾由来の保護を消す。これは資料から導いた AC-4 の回帰対象であり、新たな観察済み不具合としては扱わない。

### 変更箇所と順序

実装資料にファイル名・関数名はないため、以下は変更する責務の指定である。架空のソースパスを作らず、Build Handoff では対応する模擬実装項目を明示する。

| 順序 | 対象 | 変更・確認内容 |
|---|---|---|
| 1 | プレイヤー無敵とダメージ入口 | 現在の共通フラグの設定・解除・参照箇所を整理する。Grub 接触と Spitter 弾の双方が新しい判定を利用することを確認する |
| 2 | 無敵状態 | ダッシュ由来と被弾由来を分離する。有効な無敵は `dashProtectionActive OR hitProtectionActive` とし、共通値を残す場合もこの派生値だけにする |
| 3 | ダッシュ開始・終了 | 既存のダッシュの開始・終了に保護を結び付ける。開始・終了で被弾由来の状態を変更しない |
| 4 | 被弾処理・タイマー終了 | 実際の被害成立で 1 ハート減少、0.3 秒入力不能、被弾後 0.8 秒までの保護を開始する。タイマー終了は被弾由来の状態だけを解除する |
| 5 | 全ダメージ経路 | 接触・弾命中とも、被害や入力不能を適用する前に有効な無敵を確認する。防いだ命中で被害処理や保護時間の再開始を行わない |
| 6 | 回帰確認・模擬資料更新依頼 | 下記の検証条件、変更後の挙動と証拠の要件を Build Handoff に正確に記載し、simulator に反映させる |

時間は既存の可変 delta time に従って処理し、フレーム数を固定値として無敵時間に置き換えない。ダッシュが継続中なのに保護だけが先に切れる独立タイマーを追加しない。

ダッシュは 4 タイル・0.25 秒・クールダウン 0.6 秒、ダッシュ中の攻撃入力は終了時発動を維持する。移動、壁、敵 AI、敵の Flinch、攻撃の威力・硬直は変更しない。既存のクールダウン起点は資料に明記されていないため、起点を新しく決定しない。

### 検証条件

全条件を PC の「30 FPS・キーボード」「30 FPS・ゲームパッド」「60 FPS・キーボード」「60 FPS・ゲームパッド」で評価する。以下の t は各試行の初回被弾からの予定経過秒であり、実際のフレーム時刻とは区別する。

| AC | 設定・確認手順 | 必要な観察 |
|---|---|---|
| AC-1 | 先行被弾なし、ダッシュ使用可能な状態で開始。ダッシュ前半・後半の接触と弾命中を別試行で確認 | 実際のダッシュ開始・終了、保護期間内の接触／命中、前後のハート不変 |
| AC-2 | 被弾後、入力不能終了を確認した最初の入力可能な機会にダッシュ。入力不能中の予約は使わない | 入力不能終了、入力受理、実際のダッシュ開始、期間内の接触／命中とハート不変 |
| AC-3 | t=0.70 開始、t=0.85 命中、t=0.95 終了予定を候補にする | 実際に「被弾後 0.8 秒経過 < 命中 < ダッシュ終了」が成立し、ハート不変 |
| AC-4 | 入力不能終了後の t=0.34 開始、t=0.59 終了、t=0.70 命中を候補にする | 実際に「ダッシュ終了 < 命中 < 被弾後 0.8 秒」が成立し、ハート不変 |
| AC-5 | 保護のない状態で Grub 接触。その後、入力不能中とその終了後から t=0.8 までに追加接触を設定 | 初回 1 ハート減少、0.3 秒入力不能、その後の入力回復、無敵期間内の追加被害なし |
| AC-6 | 壁のない直線でダッシュ。期間中に一度攻撃入力。クールダウン内・経過後の再入力を確認 | 4 タイル移動、0.25 秒継続、0.6 秒クールダウン、予約攻撃が途中で発動せず終了時に一度発動 |

AC-1〜AC-4 は Grub 接触と Spitter 弾命中の両方を、それぞれ独立した試行として記録する。各試行はダッシュ使用可能・既存の保護なしの初期状態から始め、先行被弾が必要な場合はその被害成立を記録する。

追加回帰として、両方の保護が終了した後に別の攻撃を受け、通常の被害が成立することを確認する。これにより無敵の解除漏れを検出する。短時間に防いだ命中を複数回配置しても保護が延長されないことも確認する。

時刻例は完全同時の命中を避けた設定である。各 FPS で実際に成立した順序を記録し、条件を満たさなければ配置や予定時刻を調整して再試行する。丸めだけで条件成立や合格としない。0.25 秒などがフレーム境界に一致しない場合は、論理上の時間と観察フレームの両方を示す。許容誤差や同時イベントの新仕様はここでは定めない。

### 安定した試行と模擬資料の要件

Build は Handoff に「何を、どこで、どう変更し、どう試すか」を記載し、実行環境の simulator が `sim/` を更新する。technical-director は本 Step で `sim/` を変更しない。

更新する資料には次の情報が必要である。

- **実装資料:** 発生源別の状態、開始・終了の操作、有効な無敵の判定、両ダメージ経路への適用、旧共通フラグの直接解除を除去したこと。
- **プレイヤー向け模擬ビルド:** 更新対象を識別できるビルド識別子と、接触・弾命中時、ダッシュ時、通常被弾時の観察可能な挙動。内部実装の説明を混在させない。
- **QA 用の試行資料:** 各 AC・環境・命中源について、条件と実際の観察を対応させた記録。期待結果だけの表を実行結果の代用にしない。

試行記録に必要な項目：

1. 試行 ID、対象ビルド、AC、FPS、入力方式、試行回数と発生数。
2. 部屋、敵の種類・数・位置、プレイヤー位置・向き、ダッシュ方向、初期ハート、クールダウンと保護の初期状態。Spitter は発射時刻と弾の経路も記載する。
3. 初回被害成立、入力不能開始・終了、入力操作と受理、ダッシュ開始・終了、攻撃入力・発動、再使用可能になる時刻。
4. 各接触／弾命中の時刻、フレーム、同一フレーム内の順序、ハートの前後値。無敵で被害を防いだ場合にも接触／命中が成立した証拠を残す。
5. 計画時刻と実際のイベント時刻の区別。初回被弾から 0.8 秒の基準点、ダッシュ終了との前後関係。
6. 移動の始点・終点とタイル距離、ダッシュ継続時間、クールダウンの既存起点・終了、攻撃発動回数。
7. 「仕様からの期待」「simulator が生成した観察」「未実施／資料不足」の区別。実機測定や Owner の追加観察を装わない。

接触が成立しなかった試行や、AC-3 の命中が実際にはダッシュ終了後だった試行は、該当 AC の有効な試行数に含めない。再現用配置を Build／simulator が具体化し、QA が同条件を読み取れる形にする。現資料から配置座標や実施回数を創作しない。

### テスト戦略とリスク

既存テストはない。後続で状態遷移を自動確認できる場合は、「被弾保護が先に終了」「ダッシュ保護が先に終了」「両方終了」「防いだ命中はタイマーを延長しない」を最小の回帰項目とする。dry-run ではこれらを試行資料の明示的な検証シナリオとして扱い、実行可能なテストを走らせたとは報告しない。

独立 QA は全4環境の観察資料から AC を評価する。Build の自己確認は QA 合格の代わりにならない。

| リスク | 対策 |
|---|---|
| 古いタイマーや一部の命中経路が共通フラグを操作し続ける | 全設定・解除・参照箇所を Build で整理し、両命中源と両終了順序を確認 |
| 保護が永久に残る、または命中で延長される | 両保護終了後の通常被弾と、防いだ連続命中を回帰確認 |
| 可変 delta time による順序差 | 30 / 60 FPS ごとに実時刻と処理順序を記録し、境界同時命中を避ける |
| ダッシュ終了の変更が攻撃予約や移動へ影響する | 既存ライフサイクルを再利用し、AC-6 を全環境で確認 |
| 資料にないクールダウン起点や境界仕様を補ってしまう | 既存動作を保存し、判断が必要なら Studio 経由で game-designer に返す |

追加の状態と論理和は一定量の処理で、大規模な性能変更を必要としない。性能を実測したわけではない。保存形式への変更は計画に含めない。該当状態が保存対象だと Build で判明した場合は互換性の影響を報告して計画を再評価する。

**並列化:** 実装は並列化しない。無敵状態・タイマー・両命中経路が同じ判定に依存し、分担による不整合のリスクが利益を上回る。小規模な一連の修正として Build を行い、その後に独立 Verify を置く。

## Decisions already made

- D-001: 攻撃・ダッシュ・ポーズ以外の入力を Owner 承認なく追加しない。
- D-002: Owner の部分的な観察を使い、元の修正 Goal を継続する。
- D-003: 無敵の発生源を分離し、論理和で有効な保護を判定する。既存の時間・入力仕様は変更しない。

## Constraints

- 本 Step は診断と修正計画の完了であり、Build 完了・QA 合格ではない。
- 戦闘の方向性、バランス、敵の挙動、新しい入力を変更しない。
- 入力不能中の予約入力、ダッシュ開始・終了と命中が完全同時の場合の優先順位を決めない。
- QA に必要な観察資料と開発者向け実装資料を区別する。Playtester に実装資料を渡さない。
- Owner の体感値、仕様からの予定条件、模擬実装上の推論、後続の観察結果を区別する。

## Open questions

Build を阻止する必須資料の不足はない。追加の Owner 計測を要求せずに進められる。

Build で具体化する事項は、再現用配置、実際のフレーム内イベント順序、両命中経路の判定接続、既存クールダウン起点である。現資料にない実装上の事情が本方式を妨げる場合は、推測で補わず Studio に返す。

仕様上の完全同時イベントの優先順位や入力不能中の予約を決めなければ修正できないと判明した場合は、具体的な競合例を添えて game-designer に戻す。

## Expected output

Studio は gameplay-engineer に本計画、D-003、仕様・実装資料を渡して Build を依頼する。Build Handoff は変更内容と模擬資料の更新・試行要件を具体化する。

更新後、独立 QA が AC-1〜AC-6 を全4環境で Verify する。観察結果が欠ける条件は合格とせず、不足または失敗として返す。修正 Goal の完了判断はこの計画だけでは行わない。

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/technical-plan.md
- Project: project.md#vision
- Project: project.md#current-state
- Project: project.md#constraints
- Project: design/combat.md
- Project: sim/repo-notes.md
- Project: sim/build-0.3.md
- Decisions: decisions/D-001-one-button-combat.md
- Decisions: decisions/D-002-resume-with-owner-observations.md
- Decisions: decisions/D-003-independent-invulnerability.md
- Project: goals/G-001-dash-damage/11-qa-to-studio.md
- Previous handoff: goals/G-001-dash-damage/12-studio-to-technical-director.md
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

<<<FILE decisions/D-002-resume-with-owner-observations.md
---
kind: decision
id: D-002
status: accepted
decided_by: owner
goal: G-001
date: 2026-10-10
supersedes: none
---
# D-002: Owner の補足観察を受けて修正を継続する

## Decision

Owner は `goals/G-001-dash-damage/09-studio-to-owner.md` の Option A を選択した。提供された部分的な観察を新しい入力として QA の Observe を再開し、元の修正 Goal を継続する。ゲーム仕様、実装、受け入れ条件を変更する決定ではない。

Owner の回答原文：

> A。私のプレイでの観察です(計測ではなく体感)。部屋1〜2でGrubに噛まれたあと、硬直が解けてから少し間をおいて(被弾から体感0.5〜0.8秒くらい)ダッシュすると、ダッシュの後半で別のGrubに触れてハートが1減る。被弾直後すぐにダッシュした場合と、被弾していないときのダッシュでは起きない。60 FPSのPC・ゲームパッドで10回中6回ほど。Spitterの弾でも1回あった。30 FPSでは試していない。

この回答は Owner の体感による観察であり、計測ログや独立した再現確認ではない。QA が既存仕様と照合し、確認可能な範囲と未確認事項を判断する。

## Rationale

元の依頼は不具合の修正である。発生場面、被弾後の操作、比較条件、環境、おおよその頻度という新しい情報が提供されたため、同じ資料だけの再試行を避けて調査を再開できる。

## Alternatives considered

- Option B — 現資料での調査報告への範囲縮小。Owner は修正の継続を選択した。
- Option C — 未修正のまま中止。Owner は継続を選択した。

## Revisit when

追加観察を評価しても、修正に不可欠な情報が Role の作業や既存の模擬資料から得られないと判明した場合。範囲変更、中止、または既存仕様を変更する必要が生じた場合は、適切な権限へ判断を戻す。
>>>END

<<<FILE decisions/D-003-independent-invulnerability.md
---
kind: decision
id: D-003
status: accepted
decided_by: technical-director
goal: G-001
date: 2026-10-10
supersedes: none
---
# D-003: 無敵の終了を発生源ごとに管理する

## Decision

ダッシュ由来と被弾由来の無敵を独立して管理し、ダメージ判定時の有効な無敵を両者の論理和とする。

- ダッシュ開始はダッシュ由来の保護だけを開始し、終了はその保護だけを終了する。
- 実際に被害が成立した場合にのみ、既存の被弾処理と被弾後 0.8 秒までの保護を開始する。
- 被弾由来の保護の終了は、ダッシュ由来の保護を解除しない。
- 無敵で防いだ接触・命中によって、被弾由来のタイマーを開始・延長しない。
- 既存のタイマー機構を再利用し、共通フラグを各タイマーが直接オフにする方式を廃止する。

これは既存仕様に合わせる内部実装の判断である。ダッシュ、入力不能、攻撃予約、クールダウンの時間や起点、同時イベントの優先順位は変更しない。

## Rationale

`sim/repo-notes.md` では、二種類のタイマーが一つの無敵フラグをそれぞれオフにする。先に終了したタイマーが、まだ継続すべき別の保護を消す構造になっている。

発生源を分離すれば、被弾由来の保護がダッシュ途中で終了するケースと、ダッシュ終了後も被弾由来の保護が残るケースの両方を扱える。小規模な変更で既存システムを再利用できる。

## Alternatives considered

- **被弾タイマー終了時だけダッシュ中か確認する:** ダッシュ終了が被弾由来の保護を消す逆順の問題を残すため不採用。
- **無敵の長さを延ばす、被弾後のダッシュを制限する:** 既存のプレイヤー向け仕様を変更するため不採用。
- **単一の無敵終了時刻を最大値で更新する:** 現在の二つの固定時間でも実現可能だが、ダッシュの実際の継続状態と保護の対応、および各発生源の終了を明確に扱える独立管理を採用する。
- **汎用の参照カウント／トークン機構を導入する:** 現資料の二つの発生源に対して過大で、解除漏れなどの新たな管理負担があるため不採用。

## Revisit when

第三の無敵発生源、ダッシュの中断、状態の保存・復元など、現資料にない要件が判明した場合。ゲーム仕様の判断が必要なら game-designer に戻し、この Decision だけで挙動を追加しない。
>>>END

<<<FILE goals/G-001-dash-damage/15-gameplay-engineer-to-studio.md
---
kind: handoff
goal: G-001
seq: 15
from: gameplay-engineer
to: studio
stage: Build materialization
outcome: done
---
# 15: gameplay-engineer → studio — 発生源別の無敵管理を模擬実装し、資料更新を依頼する

## Task

以下の模擬実装変更を simulator に反映し、ビルド `0.3-G001-15` と QA 用観察資料を生成する。その後、実装理由と Sender assessment を除いた資料を新しい executor の QA に渡し、独立 Verify を依頼する。

## Context

G-001 はダッシュ中にダメージを受ける不具合の修正。提供された `studio/skills/implement-change.md` を適用し、仕様、AC-1〜AC-6、technical-director の計画、D-001〜D-003 の本文に従って変更を定義した。

本 Handoff の変更記述が dry-run の模擬実装となる。実コード、実機試験、自動テストの実行はない。simulator による資料更新と観察生成は未実施であり、更新済みビルドの存在や QA 合格を報告するものではない。

## Findings

### プレイヤーから見える変更と仕様の対応

| 挙動 | 根拠 |
|---|---|
| 先行被弾の有無によらず、ダッシュ全期間の接触・弾命中でハートを失わない | combat のダッシュ仕様、AC-1〜AC-3 |
| ダッシュ終了後も、先行被弾から0.8秒までの保護が残る | 被弾仕様、AC-4、D-003 |
| 防いだ命中でハート減少や入力不能を開始せず、保護時間を延長しない | D-003 |
| 両保護が終了すれば通常の被害が成立する | 被弾仕様、AC-5 |
| ダッシュ距離・時間・クールダウン、攻撃予約、通常被弾の量と時間を維持する | combat、AC-5〜AC-6 |

新しい入力やプレイヤー向けのルールは追加しない。

### 模擬実装変更

対象は `sim/repo-notes.md` の Player invulnerability と、それに接続するダッシュ、被弾、接触・弾命中の責務。ソースのファイル名や関数名は資料にないため指定しない。下記の状態名は今回の模擬実装で定義する名称である。

| 対象 | 変更後 |
|---|---|
| 無敵状態 | `dashProtectionActive` と `hitProtectionActive` を独立管理する。有効な無敵は両者の論理和。書き込み可能な旧共通フラグは廃止する |
| ダッシュ開始 | 既存のダッシュ開始が成立した時点でダッシュ保護だけを開始する。被弾保護とその終了時刻を変更しない |
| ダッシュ継続・終了 | 保護は既存のダッシュ継続状態に対応させる。既存の終了処理でダッシュ保護だけを解除する。保護専用の独立タイマーを追加しない |
| Grub 接触 | 接触によるプレイヤー被害を共通の被害入口に接続する。ハート減少・入力不能の適用前に有効な無敵を判定する |
| Spitter 弾命中 | 弾命中によるプレイヤー被害も同じ入口・同じ判定を使用する |
| 保護中の命中 | プレイヤー被害処理を終了する。ハート、入力不能、被弾保護の状態・終了時刻を変更しない。既存の弾の消滅等、被害以外の命中処理は変更しない |
| 保護なしの命中 | 既存どおり1ハート減少、0.3秒入力不能を適用する。被害成立時刻から0.8秒まで被弾保護を有効にする |
| 入力不能終了 | 既存どおり入力を回復する。被弾保護を解除しない |
| 被弾保護終了 | 被弾保護だけを解除する。ダッシュ保護を変更しない |
| 無敵の参照 | 旧共通フラグへの参照を論理和の参照に置換する。派生値を保持する場合も、各タイマーから直接書き換えない |

共通被害入口の判定順序は次のとおりとする。

1. 接触／弾命中が成立する。
2. `dashProtectionActive OR hitProtectionActive` を確認する。
3. 真ならプレイヤー被害を適用せず終了する。
4. 偽なら既存の通常被弾処理を適用し、被弾保護を開始する。

既存イベントの実行順序は変更しない。この順序指定は被害入口内の処理順序であり、同時刻のダッシュ開始・終了と命中の優先順位を新設するものではない。

旧操作の置換範囲は、ダッシュ開始の共通オン、ダッシュ終了の共通オフ、被害成立の共通オン、被弾タイマー終了の共通オフ、および無敵判定の全参照。両命中源に旧フラグを直接操作する迂回経路を残さない。提供資料にない操作箇所まで実コード検索で確認したという意味ではない。

既存の可変 delta time とタイマー機構を再利用する。ダッシュは4タイル・0.25秒、クールダウン0.6秒。クールダウンの既存起点、ダッシュ中の攻撃予約と終了時発動は変更しない。保存形式への変更は定義しない。

### simulator に依頼する資料更新

以下は生成先の指定であり、本 Step で作成済みのファイルではない。

| 資料 | 更新・生成先 | 内容・用途 |
|---|---|---|
| 開発者向け実装資料 | `sim/repo-notes.md` | 本変更、ビルド識別子、両命中経路、旧共通操作の置換を記録。他の実装項目は維持 |
| プレイヤー向け模擬ビルド | `sim/build-0.3-G001-15.md` | ビルド識別子、読み方、ダッシュ・接触・弾命中・通常被弾の観察可能な挙動。内部状態・原因・自己評価を含めない |
| QA 用試行資料 | `sim/qa-G001-15.md` | 下記シナリオの設定、実際に生成した模擬観察、無効試行、未確認項目を分離して記録 |

旧 `sim/build-0.3.md` は修正前の比較資料として識別する。新資料が未生成の間は旧資料を修正後の証拠として扱わない。

dry-run の実行・確認方法は、新ビルドの説明と QA 用試行資料を読むこと。実行コマンドは存在しない。simulator は期待結果をそのまま観察結果として転記せず、各条件の模擬イベントとハート変化を生成すること。生成できない項目は資料不足と記す。

### 試行の共通設定

全シナリオを PC の30 FPS・キーボード、30 FPS・ゲームパッド、60 FPS・キーボード、60 FPS・ゲームパッドで扱う。AC-1〜AC-4 は Grub 接触と Spitter 弾命中を独立試行にする。AC-1 はさらに前半・後半を分ける。

以下は新しく用意する試行配置の指定であり、既存の部屋座標や観察済み配置ではない。

- Grub 試行は部屋1〜2の壁に遮られない直線区間を使う。ダッシュ始点を基準点、進行方向を正方向として、4タイルの経路とその先に通常被弾を確認できる余地を確保する。
- 先行被弾なしの試行では対象 Grub を1体、先行被弾ありでは初回被弾用と評価対象の Grub を各1体とする。初回被弾用が予定外の再接触を起こさない配置を選ぶ。
- 弾試行は混在部屋の開けた区間で Spitter を1体使い、先行被弾が必要な場合は Grub を1体加える。既存の発射間隔2秒、弾速、AIを変えず、発射位相と初期位置で評価時刻に弾道がプレイヤーと交差するよう設定する。
- 他の敵・弾が予定外に干渉した場合は、そのイベントも記録し、条件を満たさない試行を無効とする。
- 各試行はダッシュ使用可能、保護なし、入力可能から開始する。初期ハート `H` は既存仕様で実在する値を使い、予定被弾で死亡しない状態を選ぶ。最大ハート数は新設しない。
- 具体的な座標、当たり判定寸法、敵の移動速度は資料にない。simulator は実際に用いたプレイヤー・敵の座標、向き、弾の発射位置・時刻・経路を記録し、再読可能な配置にする。これらを生成できない場合は配置未確定と報告する。

攻撃が通り過ぎただけの試行を保護成功に数えない。接触または弾の当たり判定が成立した記録が必要である。

### AC ごとの入力・命中設定

`t` は先行被弾成立からの予定経過秒、`d` は実際のダッシュ開始時刻。下表の数値は試行の目標であり、観察結果ではない。

| ID | 操作・命中の目標 | 期待するハートと確認点 |
|---|---|---|
| AC-1 前半 | 先行被弾なしでダッシュ入力。`d+0.07秒`付近に接触／弾命中を配置 | `H→H`。実際の開始後かつ終了前であること |
| AC-1 後半 | 別試行で`d+0.18秒`付近に接触／弾命中を配置 | `H→H`。前半だけの確認で代用しない |
| AC-2 | t=0で通常被弾。0.3秒の入力不能終了を観察した最初の入力可能な機会にダッシュ入力。`d+0.10秒`付近で命中 | 初回`H→H−1`、評価命中`H−1→H−1`。入力不能中の予約を使わない |
| AC-3 | t=0で被弾、t=0.70付近にダッシュ開始、t=0.85付近に命中 | 初回以外の減少なし。実際に「被弾保護終了 < 命中 < ダッシュ終了」が成立すること |
| AC-4 | t=0で被弾、入力可能になってからt=0.34付近にダッシュ開始、t=0.70付近に命中 | 初回以外の減少なし。実際に「ダッシュ終了 < 命中 < 被弾保護終了」が成立すること |
| AC-5 | 保護なしで Grub 接触。追加接触をt=0.15、0.45、0.70付近に設定。入力不能中と終了後の既存入力の受理状況を記録 | 初回のみ`H→H−1`。0.3秒入力不能、終了後の入力回復、0.8秒まで追加減少なし |
| AC-6 | 敵・壁に干渉しない直線でダッシュ。`d+0.10秒`付近で攻撃を一度入力。クールダウン内と終了後の再入力は別試行で行う | 4タイル、論理時間0.25秒。攻撃は途中発動せず終了時に一度。既存起点から0.6秒の再使用制限を維持 |

AC-6 のクールダウン試行は、既存の起点を `c` と記録できた後に、`c+0.50秒`付近と`c+0.70秒`付近の入力を設定する。起点をダッシュ開始または終了と仮定しない。既存起点が資料化できなければ、この項目は未確認として戻す。

### 追加回帰

次を全4環境、Grub／Spitter の別試行で用意する。

1. **被弾保護が先に終了:** AC-3の配置でダッシュ中の命中を防ぎ、両保護終了後のt=1.10付近に別の命中を置く。期待は後者のみ1ハート減少。
2. **ダッシュ保護が先に終了:** AC-4の配置でダッシュ終了後の命中を防ぎ、両保護終了後のt=0.95付近に別の命中を置く。期待は後者のみ1ハート減少。
3. **防いだ命中による延長なし:** 上記に加え、被弾保護終了前またはダッシュ終了前に、異なるフレームで少なくとも2回の成立した命中を配置する。元の保護終了後の命中で通常被害が成立することを確認する。命中回数が不足した試行はこの回帰の証拠にしない。
4. **ダッシュのみの解除:** 先行被弾なしでダッシュ中に複数命中を防ぎ、終了後の`d+0.40秒`付近に命中を置く。期待は終了後に1ハート減少。防いだ命中が被弾保護を新規開始していないことも確認する。

複数の弾・接触が必要な配置は既存の敵挙動で成立させる。成立しない場合は時刻や配置を調整して記録し、敵の発射頻度や攻撃仕様を変更しない。

### 記録形式と有効性

試行IDを `G001-15/<ACまたは回帰>/<FPS>/<入力>/<命中源>/<枝>/<連番>` とする。各セルについて少なくとも1件の有効な模擬試行を生成することを依頼する。これは予定件数であり、実施数ではない。

各試行に次を残す。

- 対象ビルド、AC、環境、部屋、全敵の種類・数・位置、プレイヤー位置・向き・ダッシュ方向、初期ハート、保護・クールダウンの初期状態。
- 計画時刻と実際の模擬イベント時刻を別欄にする。各イベントのフレーム番号、delta time、同一フレーム内の処理順番号を記録する。
- 初回被害、入力不能開始・終了、入力操作・受理、ダッシュ開始・終了、各接触／命中、ハート前後値、攻撃入力・発動、再使用可能時刻。
- 被弾後0.8秒の論理基準点、ダッシュの論理終了時刻と観察フレーム、実際の前後関係。
- 移動始点・終点、距離、継続時間、クールダウン起点と終了、攻撃発動回数。
- 試行総数、有効数、無効数、条件を満たす試行での被害発生数。無効理由と再試行の対応。

30 FPSでは0.25秒が整数フレームに一致しない。論理時間と観察フレームを併記し、丸めによる独自の許容誤差を設けない。同時境界、命中不成立、予定外の先行被弾、AC-3／AC-4の順序不成立は該当条件の有効試行に含めず、配置や入力時刻を調整する。

## Decisions already made

- D-001: 攻撃・ダッシュ・ポーズ以外の入力を追加しない。
- D-002: Owner の部分的観察を使って元の修正 Goal を継続する。追加計測を開始条件にしない。
- D-003: 無敵を発生源別に管理し、論理和で判定する。防いだ命中で保護を延長しない。

## Constraints

戦闘の方向性、バランス、敵 AI、Flinch、移動・壁、攻撃の威力・硬直を変更しない。固定フレーム数への置換、ダッシュ保護専用の別タイマー、保存形式変更は行わない。実装は並列化しない。

入力不能中の予約、完全同時イベントの優先順位、クールダウン起点の新仕様を決めない。判断が不可欠な具体例が出た場合は Studio 経由で game-designer に戻す。

プレイヤー向け資料に実装資料や自己評価を混在させない。QA には期待と観察を分離して渡す。Build の自己確認は独立 QA の合格を代替しない。

## Open questions

模擬実装変更を定義するための必須資料不足はない。次の事項は資料生成時に確認する必要がある。

- 各 FPS で命中が成立する正確な配置、発射位相、実際のイベント順序。
- 既存クールダウン起点。資料から復元できなければ推測せず AC-6 の不足として返す。
- 更新ビルドと観察資料が指定識別子に対応して生成されたか。
- 提供資料にない保存・復元やダッシュ中断が判明した場合の影響。その場合は対象部分を止め、technical-director に再計画を求める。

これらの未確認事項を観察済みとして埋めない。仕様判断や計画変更が必要になった場合は、解決前に QA へ完成品として渡さない。

## Expected output

Studio は simulator に本変更と資料生成を依頼し、更新ビルド、全 AC・全4環境・必要命中源の観察資料を揃える。不足した資料は具体的な条件を付けて補完または差し戻す。

その後、仕様・AC・更新ビルド・観察資料を新しい executor の QA に渡す。原因説明、実装理由、Sender assessment は除外する。QA は不足を合格で補わず、独立した Verify 結果を Studio に返す。

## Sender assessment

提供資料上の原因は、二つの終了処理が共通フラグを解除し、他方の保護まで失わせること。今回の変更は両終了順序を同じ発生源別管理で扱い、片方だけを修正する方式にはしていない。

自己確認は文書照合のみ実施した。D-003 の各項目に対応する変更、両命中経路、旧操作の置換、AC-1〜AC-6、解除漏れと延長防止の回帰条件が記載されていることを確認した。承認済み仕様との文面上の整合は確認したが、挙動の合格判定はしていない。

コード実行、自動テスト、実機計測、新しい再現試行、simulator 観察生成は未実施。正確な配置、イベントログ、クールダウン起点は未確認。保存互換性への影響も資料から有無を断定できない。変更記述は完了しているが、実行結果の信頼性は後続資料と独立 QA で確認する必要がある。

## Load

- Project: project.md#vision
- Project: project.md#current-state
- Project: project.md#constraints
- Project: design/combat.md
- Project: sim/repo-notes.md
- Project: sim/build-0.3.md
- Project: goals/G-001-dash-damage/11-qa-to-studio.md
- Project: goals/G-001-dash-damage/13-technical-director-to-studio.md
- Decisions: decisions/D-001-one-button-combat.md
- Decisions: decisions/D-002-resume-with-owner-observations.md
- Decisions: decisions/D-003-independent-invulnerability.md
- Previous handoff: goals/G-001-dash-damage/14-studio-to-gameplay-engineer.md
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
