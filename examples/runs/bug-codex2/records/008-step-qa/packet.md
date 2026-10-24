# Studio operation packet

operation: Step
goal: G-001
role: qa
incoming_handoff: goals/G-001-dash-damage/07-studio-to-qa.md
next_seq: 8

## You may write

- goals/G-001-dash-damage/08-qa-to-<recipient>.md

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

<<<FILE goals/G-001-dash-damage/07-studio-to-qa.md
---
kind: handoff
goal: G-001
seq: 7
from: studio
to: qa
stage: Observe
outcome: routed
---
# 07: studio → qa — 補足観察資料の受領後に再現確認を再開する

## Task

補足観察資料が提供され、Studio が Load と開始条件の充足を確認した後、既存仕様に対する再現条件と未観察範囲を整理する。開始条件が満たされるまで、この Handoff による Step を実行しない。

## Context

Owner の依頼は「ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい」。

前回 QA は資料不足により追加再現確認を開始できなかった。今回も補足観察資料はなく、提供可否・取得先・入手方法は未確認である。この Handoff は資料受領後の再開用であり、同じ資料だけでの再試行を指示するものではない。

## Findings

`06-qa-to-studio.md` によると、仕様はダッシュ全期間 0.25 秒の無敵を定める一方、模擬ビルドには被弾直後のダッシュ中に時折ダメージを受けるとの記述がある。今回の新規観察ではなく、技術的原因も未確定である。

実行環境側に提供可否と取得方法の確認が必要な資料：

- 部屋、敵の種類・数、命中源、位置関係、ダッシュ方向を含む配置と操作条件。
- 初回被弾、入力不能終了、ダッシュ入力・開始、再被弾、ダッシュ終了の時刻とハート変化。
- 被弾からダッシュまでの間隔を変えた比較と、条件別の試行数・発生数。
- キーボード／ゲームパッド × 30／60 FPS の結果と未観察範囲。

提供された資料でどこまで確認できるかは QA が判断する。一部のみ提供された場合、未観察部分を明示し、結果を補って推測しない。

既存の受け入れ条件は前回報告から引き継ぎ、すべて未検証として扱う。

1. 被弾後、入力可能になってから開始したダッシュ全期間で、Grub の接触攻撃・Spitter の弾によってハートが減らない。
2. 直前に被弾していない場合も、同じ攻撃に対してダッシュ全期間でハートが減らない。
3. ダッシュ開始直後・途中・終了直前で上記を満たす。終了後も被弾後の無敵が残る間はダメージを受けず、両方の無敵終了後の有効な命中では通常どおり 1 ハート減る。
4. 移動距離 4 タイル、時間 0.25 秒、クールダウン 0.6 秒、ダッシュ中の攻撃入力が終了時に発動する挙動を維持する。
5. Desktop のキーボード／ゲームパッドと 30／60 FPS の全組み合わせで確認する。

## Decisions already made

新しい Decision はない。既存仕様への修正として進める。追加 Design は省略し、Build はまだ開始しない。入力追加の制約は `project.md#constraints` に従う。

## Constraints

- Dry-run プロジェクトであり、資料読解と実機実行を区別する。
- QA は実装を変更せず、実装者の自己評価や reasoning を検証根拠にしない。
- 再現条件、観察結果、頻度、原因を創作しない。
- 入力不能中のダッシュ予約や完全同時の境界処理を新たに規定しない。
- 戦闘の方向性変更、新しい入力、無関係な調整は対象外。
- 補足資料なしで同じ packet を再実行しない。

## Open questions

- 補足観察資料は提供可能か。取得先と入手方法は何か。実行環境側で確認し、Studio に返す必要がある。
- どの配置・操作・時系列で、何回中何回発生するか。
- 被弾からダッシュまでの間隔、攻撃種別、入力方式、FPS によって結果はどう変わるか。
- 被弾後の無敵にも違反するか。

## Expected output

開始条件の充足後、QA は出典を伴う再現手順、期待値と観察値、頻度、重大度、受け入れ条件、未観察範囲を報告し、結果を `studio` に返す。

資料の提供可否が未確認、または資料が未提供の間は Step を開始しない。実行環境側の回答と資料を Studio に返して入力を補完する。提供できないと判明した場合も、その事実と理由を Studio に返し、再ルーティングの根拠とする。

## Load

以下は再開時に必要な入力。今回の packet には Role の Works from / Independence 以外の本文、Skill、戦闘仕様、模擬ビルド、補足観察資料が含まれていないため、Studio による本文確認と補完が必要。

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: project.md#vision
- Project: project.md#current-state
- Project: project.md#constraints
- Project: design/combat.md
- Project: sim/build-0.3.md
- Project: 補足観察資料 — 未提供。再開前に実在する資料の所在と本文を追加する。
- Decisions: none
- Previous handoff: goals/G-001-dash-damage/06-qa-to-studio.md
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

<<<FILE goals/G-001-dash-damage/06-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 6
from: qa
to: studio
stage: Observe
outcome: question
---
# 06: qa → studio — 補足観察資料未提供のため再現確認は開始不可

## Task

Studio は実行環境側に補足観察資料の提供可否・取得先・入手方法を確認する。資料の所在と本文がそろうまで、同じ資料だけで QA に再試行を依頼しない。

## Context

Owner の依頼は「ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい」。

今回の packet には QA Role、reproduce-defect Skill、Project の必要節、戦闘仕様、模擬ビルド、前回 QA 報告、incoming Handoff が含まれている。しかし、05 が開始条件とした補足観察資料は未提供であり、所在・提供可否も不明のままである。

## Findings

### 実施範囲と判定

`studio/skills/reproduce-defect.md` に照らして入力資料の充足状況を確認した。05 の開始条件を満たさないため、追加の再現確認は開始していない。同じ模擬資料による再試行、実機実行、実装変更、新しい試行結果はない。

資料上の不一致は維持される。

- 期待値：`design/combat.md` はダッシュ全期間 0.25 秒の無敵を定める。
- 観察値の出典：`sim/build-0.3.md` に、被弾直後にダッシュすると時折ダッシュ途中でダメージを受けるとの記述がある。今回の新規観察ではない。
- 再現手順：配置・操作・タイミングが不足し、確定できない。
- 時系列：初回被弾、入力不能終了、ダッシュ入力・開始、再被弾、ダッシュ終了の具体的な時刻とハート変化は不明。
- 頻度：条件別の試行数・発生数は未提供。「時折」を定量化できない。
- 重大度：既存報告の「体験を損なう不具合」を維持する。進行不能や死亡を裏付ける証拠はない。

期待挙動の仕様不足ではない。再現確定、修正済み、検証合格のいずれとも判定しない。技術的原因は未確定である。

### 不足資料と未観察範囲

| 必要な資料 | 現時点で確定できない事項 |
|---|---|
| 部屋、敵の種類・数、初回と再被弾の命中源、位置関係、ダッシュ方向 | 再現可能な配置と操作手順、攻撃種別による差 |
| 初回被弾からダッシュ終了までの時刻とハート変化 | ダッシュ内の発生時刻、ダメージ量、被弾後 0.8 秒の無敵にも違反するか |
| 被弾からダッシュまでの間隔を一条件ずつ変えた比較、条件別試行数・発生数 | 最小再現条件、再現率、発生しなくなる境界 |
| Desktop のキーボード／ゲームパッド × 30／60 FPS の設定別結果 | 全4組み合わせでの発生有無と差、各設定の未観察範囲 |

「被弾直後」だけでは、0.3 秒の入力不能中の入力と、その終了後の入力を区別できない。入力予約の有無は推測しない。

### 引き継ぐ受け入れ条件

以下は変更せず維持し、すべて未検証とする。

1. 被弾後、入力可能になってから開始したダッシュ全期間で、Grub の接触攻撃・Spitter の弾によってハートが減らない。
2. 直前に被弾していない場合も、同じ攻撃に対してダッシュ全期間でハートが減らない。
3. ダッシュ開始直後・途中・終了直前の接触で上記を満たす。終了後も被弾後の無敵が残る間はダメージを受けず、両方の無敵終了後の有効な命中では通常どおり 1 ハート減る。
4. 移動距離 4 タイル、時間 0.25 秒、クールダウン 0.6 秒、ダッシュ中の攻撃入力が終了時に発動する挙動を維持する。
5. Desktop のキーボード／ゲームパッドと 30／60 FPS の全組み合わせで確認する。

完全同時の境界処理は新たに規定せず、ダッシュ終了の前後を区別できる条件で確認する。

## Decisions already made

新しい Decision はない。

既存仕様への修正として進め、追加 Design は省略するという Studio の方針を維持する。Build はまだ開始しない。D-001 による入力追加の制約は `project.md#constraints` に従う。

## Constraints

- Dry-run の資料読解と実機実行を区別する。
- QA は実装を変更せず、実装者の自己評価や reasoning を検証根拠にしない。
- 再現条件、観察結果、頻度、技術的原因を創作しない。
- 入力不能中のダッシュ予約や完全同時の境界処理を新たに規定しない。
- 新しい入力、戦闘の方向性変更、無関係な調整は対象外。
- 補足資料が届くまで、同じ資料だけで再現確認を再試行しない。

## Open questions

- 実行環境側は補足観察資料を提供できるか。取得先と入手方法は何か。
- どの配置・操作・時系列で、何回中何回発生するか。
- 被弾からダッシュまでの間隔、攻撃種別、入力方式、FPS によって結果はどう変わるか。
- 被弾後の無敵にも違反するか。

## Expected output

Studio は資料の提供可否と取得先・入手方法を明示する。提供可能なら、不足項目に対応する資料の実在する所在と本文を添えて QA に渡す。一部のみ提供された場合は、残る不足を明記する。

提供できない場合は観察の blocker を記録する。現状の資料だけで再現確定や Build 開始へ進めず、同じ packet による QA 再試行を行わない。

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: project.md#vision
- Project: project.md#current-state
- Project: project.md#constraints
- Project: design/combat.md
- Project: sim/build-0.3.md
- Project: 補足観察資料（未提供・所在未確認。QA 再開前に実在する所在と本文で補完必須）
- Decisions: none
- Previous handoff: goals/G-001-dash-damage/05-studio-to-qa.md
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
