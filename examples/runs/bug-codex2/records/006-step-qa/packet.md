# Studio operation packet

operation: Step
goal: G-001
role: qa
incoming_handoff: goals/G-001-dash-damage/05-studio-to-qa.md
next_seq: 6

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
- Write every file you create or change as one complete file block:
  `<<<FILE <path>` on its own line, the full file content, then `>>>END` on its own line.
  Use only the paths listed under "You may write"; paths are relative to the project directory.
- Only file blocks are kept. Anything else you write is discarded and never shown to any later
  step, so put everything the next operation needs into the files.
- If the packet is not enough to do the operation, write the artifact that hands the work back or
  reports the blocker instead of guessing.
>>>END

<<<FILE goals/G-001-dash-damage/05-studio-to-qa.md
---
kind: handoff
goal: G-001
seq: 5
from: studio
to: qa
stage: Observe
outcome: routed
---
# 05: studio → qa — 補足資料の受領後に再現条件を確定する

## Task

実行環境側から補足観察資料が提供された後、既存仕様と照合し、再現条件・時系列・頻度を明記した defect report を作成する。資料が未提供の間はこの Step を開始せず、同じ資料だけで再試行しない。

## Context

Owner の依頼は「ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい」。

前回の QA は必要な既存本文を受領したが、補足観察資料がなく、追加の再現確認を実施せず Studio に戻した。Studio の今回の packet にも補足資料はない。実行環境側による提供可否・取得先・入手方法は未確認であり、本 Handoff は資料の提供を保証しない。

## Findings

`04-qa-to-studio.md` の QA 報告によると、仕様はダッシュ全期間 0.25 秒の無敵を定める一方、模擬ビルドには被弾直後のダッシュ途中で時折ダメージを受けるとの記述がある。具体的な再現条件を確定する証拠は不足している。実装変更や新しい試行結果はない。

実行環境側は、開始前に以下の観察記録の所在と本文を提供する必要がある。

- 部屋、敵の種類・数、初回と再被弾の命中源、位置関係、ダッシュ方向。
- 初回被弾、入力不能終了、ダッシュ入力・開始、再被弾、ダッシュ終了の時系列とハート変化。
- 被弾からダッシュまでの間隔を一条件ずつ変えた比較と、条件別の試行数・発生数。
- キーボード／ゲームパッド、30／60 FPS の設定別結果と未観察範囲。

提供された資料が一部に限られる場合は、確定できる事項と不足事項を区別する。未観察の結果を補完しない。

## Decisions already made

この Goal での新しい Decision はない。

既存仕様への修正として進め、追加 Design は省略する。Build はまだ開始しない。D-001 による入力追加の制約は `project.md#constraints` に記載されている。

## Constraints

- Desktop、キーボード／ゲームパッド、30／60 FPS を対象とする。
- Dry-run であり、模擬資料の読解と実機での実行確認を区別する。
- QA は実装を変更しない。実装者の自己評価や reasoning を検証根拠にしない。
- 再現条件、観察結果、技術的原因を創作しない。
- 入力不能中のダッシュ予約や完全同時の境界処理を新たに規定しない。
- 新しい入力の追加、戦闘の方向性変更、無関係な調整は対象外。
- Load の不足を補完するまで実行しない。

## Open questions

- 実行環境側は補足観察資料を提供できるか。その取得先・入手方法は何か。これは実行前に解消する blocker である。
- どの配置・操作・時系列で、何回中何回発生するか。
- 被弾からダッシュまでの間隔、攻撃種別、入力方式、FPS によって結果はどう変わるか。
- 被弾後の無敵にも違反するか。

## Expected output

結果は `to: studio` とした outgoing Handoff に記録する。再現手順、期待値と観察値、時系列、条件別試行数・発生数、重大度、未観察範囲を明記する。資料から確定できない事項は不足として残し、原因を推測して埋めない。

前回 QA が維持した以下の受け入れ条件を引き継ぐ。現時点ではすべて未検証である。

1. 被弾後、入力可能になってから開始したダッシュ全期間で、Grub の接触攻撃・Spitter の弾によってハートが減らない。
2. 直前に被弾していない場合も、同じ攻撃に対してダッシュ全期間でハートが減らない。
3. ダッシュ開始直後・途中・終了直前の接触で上記を満たす。終了後も被弾後の無敵が残る間はダメージを受けず、両方の無敵終了後の有効な命中では通常どおり 1 ハート減る。
4. 移動距離 4 タイル、時間 0.25 秒、クールダウン 0.6 秒、ダッシュ中の攻撃入力が終了時に発動する挙動を維持する。
5. Desktop のキーボード／ゲームパッドと 30／60 FPS の全組み合わせで確認する。

完全同時の境界処理は新たに規定せず、ダッシュ終了の前後を区別できる条件で確認する。

## Load

以下は実行時に必要な資料である。この Route packet では QA の Works from と Independence、および project.md と前回 QA 報告を確認した。Role・Skill 全文、戦闘仕様、模擬ビルド、補足観察資料をすべて受領・確認済みとは扱わない。実行環境側が本文をそろえ、補足観察資料の項目を具体的な所在に置き換えるまで開始しない。

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: project.md#vision
- Project: project.md#current-state
- Project: project.md#constraints
- Project: design/combat.md
- Project: sim/build-0.3.md
- Project: 補足観察資料（未提供・所在未確認。実行前に実在する資料の所在と本文で補完必須）
- Decisions: none
- Previous handoff: goals/G-001-dash-damage/04-qa-to-studio.md
>>>END

<<<FILE project.md
---
kind: project
id: lantern-depths
name: Lantern Depths (sample)
repository: none (sample project for dry-runs; builds are simulated under sim/)
owner_language: ja
player_visible: sim/build-*.md
---
# Project: Lantern Depths (sample)

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

Vertical-slice prototype, build 0.3: 5 rooms in one cave biome, 2 enemy types, player kit of attack
and dash. Dry-run only: "running the build" means reading `sim/build-0.3.md`.

## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).
- Dry-run project: there is no real repository. `sim/repo-notes.md` stands in for the code. A Build
  step implements a change by stating it exactly in its Handoff (what changes, where, and how to
  exercise it); the change then counts as made, and the runtime's simulator updates `sim/` from it.

## Art direction

Dark caves lit by the player's lantern; warm light against cold blue-black. Threats use saturated
orange/red so they read against the dark.

## Design index

- `design/combat.md` — player kit, damage and invulnerability rules, enemies.
>>>END

<<<FILE studio/roles/qa.md
---
kind: role
id: qa
strip_sections: Sender assessment
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

<<<FILE studio/skills/reproduce-defect.md
---
name: reproduce-defect
description: Reproduce a reported problem reliably and turn it into a precise defect report with acceptance criteria for the fix.
---
# Skill: Reproduce defect

Typical roles: qa. Any Role whose responsibility covers confirming a defect may use it.

## When to use

A problem is reported but has not been reproduced first-hand, or its conditions are unclear.

## Inputs

The report, how to run the build, the design documents that define expected behavior, the
project's supported platforms and settings.

## Method

1. Reproduce exactly as reported. Then vary one condition at a time (timing, input device, frame
   rate, platform, state) to find the minimal reliable steps and the boundary where it stops.
2. Name the source of "expected": cite the design document or Decision. If no source defines the
   expected behavior, it is a spec gap, not a defect — say so and hand back to `game-designer`.
3. Rate severity from the player's view (blocks progress / hurts the experience / cosmetic) and
   frequency.
4. Write acceptance criteria for the fix: observable checks, including the conditions you varied.

## Output

Defect report: steps, expected (with source), actual, conditions and boundary, severity, frequency,
acceptance criteria, evidence (logs, recordings, notes).

## Do not

Guess at code-level causes as fact; label any hypothesis as one. Do not fix the defect.
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

<<<FILE goals/G-001-dash-damage/04-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 4
from: qa
to: studio
stage: Observe
outcome: question
---
# 04: qa → studio — 必須本文は受領、補足観察資料が未提供

## Task

Studio は再現条件を記録した補足観察資料を実行環境側から提供できるか確認し、提供可能なら所在と本文を添えて QA に戻す。提供できない場合は観察の blocker として扱い、同じ資料だけで QA を再試行しない。

## Context

Owner の依頼は「ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい」。

前回は具体的な再現条件が不足し、Studio が追加 Observe に戻した。今回の packet には QA Role、reproduce-defect Skill、Project の必要節、戦闘仕様、模擬ビルド、前回 QA 報告の本文がそろっている。ただし、要求された補足観察資料は含まれていない。

## Findings

### 今回の実施範囲と判定

`studio/skills/reproduce-defect.md` に従い、入力資料の充足状況を確認した。追加観察資料がないため、同じ模擬資料による再現確認の再試行は行っていない。実機実行、新しい試行結果、実装変更はない。

前回の資料上の不一致は未解決のまま：

- 期待の根拠：`design/combat.md` はダッシュの全期間 0.25 秒を無敵と定める。
- 報告された挙動：`sim/build-0.3.md` は被弾直後のダッシュ途中で時折ダメージを受けると記述する。
- この記述は仕様に反するが、具体的な再現手順・頻度・境界を確定する新しい証拠はない。

期待挙動の仕様不足ではない。修正済み、再現確定、検証合格のいずれとも判定しない。

### 不足資料と確定できない事項

| 必要な補足観察資料 | 不足により確定できない事項 |
|---|---|
| 部屋、敵の種類・数、初回と再被弾の命中源、位置関係、ダッシュ方向 | 再現可能な配置・操作手順、攻撃種別による差 |
| 初回被弾、入力不能終了、ダッシュ入力・開始、再被弾、ダッシュ終了の時系列とハート変化 | ダッシュ内の発生時刻、ダメージ量、被弾後 0.8 秒の無敵にも違反するか |
| 被弾からダッシュまでの間隔を一条件ずつ変えた比較、条件別の試行数・発生数 | 再現率、最小の再現条件、発生しなくなる境界 |
| キーボード／ゲームパッド、30／60 FPS の設定別結果と未観察範囲 | 対応する全組み合わせでの発生有無と差 |

「被弾直後」という記述だけでは、0.3 秒の入力不能中の入力か、その終了後の入力かも区別できない。入力予約や技術的原因を推測して補完しない。

### 重大度と受け入れ条件の扱い

前回の資料に基づく重大度「体験を損なう不具合」は維持する。進行不能や死亡、定量的な発生頻度を示す追加証拠はない。

前回の受け入れ条件を変更せず維持する。以下はすべて未検証：

1. 被弾後、入力可能になってから開始したダッシュ全期間で、Grub の接触攻撃・Spitter の弾によってハートが減らない。
2. 直前に被弾していない場合も、同じ攻撃に対してダッシュ全期間でハートが減らない。
3. ダッシュ開始直後・途中・終了直前の接触で上記を満たす。終了後も被弾後の無敵が残る間はダメージを受けず、両方の無敵終了後の有効な命中では通常どおり 1 ハート減る。
4. 移動距離 4 タイル、時間 0.25 秒、クールダウン 0.6 秒、ダッシュ中の攻撃入力が終了時に発動する挙動を維持する。
5. Desktop のキーボード／ゲームパッドと 30／60 FPS の全組み合わせで確認する。

完全同時の境界処理は新たに規定せず、ダッシュ終了の前後を区別できる条件で確認する。

## Decisions already made

この Goal での新しい Decision はなし。

Studio の既定方針は既存仕様への修正として進め、Design を省略すること。Build はまだ開始しない。D-001 による入力追加の制約を維持する。

## Constraints

- Dry-run であり、模擬資料の読解と実機での実行確認を区別する。
- 再現条件、観察結果、実装原因を創作しない。
- QA は実装を変更せず、実装者の自己評価を検証根拠にしない。
- 入力不能中のダッシュ予約や完全同時の境界処理を新たに規定しない。
- 補足資料が届くまで、同じ資料だけで再試行しない。

## Open questions

- 実行環境側から補足観察資料を提供できるか。提供可能なら、その所在はどこか。
- どの配置・操作・時系列で、何回中何回発生するか。
- 被弾からダッシュまでの間隔、攻撃種別、入力方式、FPS によって結果はどう変わるか。

## Expected output

Studio は補足観察資料の提供可否を明示する。提供可能なら、上記の不足項目を含む資料の所在と本文を添えて QA の追加 Observe へ渡す。

提供できなければ blocker を記録して資料の取得先・入手方法を確認する。現状の資料だけで再現確定や Build 開始へ進めない。

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: project.md#vision
- Project: project.md#current-state
- Project: project.md#constraints
- Project: design/combat.md
- Project: sim/build-0.3.md
- Project: 補足観察資料（未提供。次回 QA 実行時に所在と本文が必要）
- Decisions: none
- Previous handoff: goals/G-001-dash-damage/03-studio-to-qa.md
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
