# Studio operation packet

operation: Step
goal: G-001
role: qa
incoming_handoff: goals/G-001-dash-damage/03-studio-to-qa.md
next_seq: 4

## You may write

- goals/G-001-dash-damage/04-qa-to-<recipient>.md

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

<<<FILE goals/G-001-dash-damage/03-studio-to-qa.md
---
kind: handoff
goal: G-001
seq: 3
from: studio
to: qa
stage: Observe
outcome: routed
---
# 03: studio → qa — 補足観察資料による再現条件の確認

## Task

補足観察資料が提供されたら、被弾後のダッシュ中に再被弾する条件を確認し、再現手順と受け入れ条件を備えた不具合報告を完成させる。資料が不足したままの場合は条件を推測せず、確認できない項目を明示して Studio に返す。

## Context

Owner の依頼：

> ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい。

初回 QA は模擬資料と既存仕様の不一致を報告したが、具体的な再現条件が不足しているため `outcome: question` で Studio に返した。Studio は追加 Observe を次のステップとし、Build はまだ開始しない。

## Findings

前回の QA 報告は `02-qa-to-studio.md` に記録されている。

- QA によれば、既存仕様はダッシュの全期間 0.25 秒を無敵と定める。
- 模擬ビルドには、被弾後にダッシュすると時折その途中でダメージを受けるとの記述がある。
- 敵・攻撃種別、配置、入力と命中の時系列、試行数、入力方式・FPS ごとの結果は不足している。
- 前回の報告には既存仕様に基づく受け入れ条件がある。検証済みという意味ではない。

今回の Route では新しい観察結果を取得していない。補足資料は未提供であり、これが追加観察の blocker である。

実行前に、模擬ビルドの観察資料として以下を補足する必要がある：

- 部屋、敵の種類・数、命中源、位置関係、ダッシュ方向。
- 初回被弾、入力不能終了、ダッシュ入力・開始、再被弾、ダッシュ終了の時系列。
- 条件ごとの試行数と発生数、および比較条件。
- キーボード／ゲームパッド、30／60 FPS の設定と観察範囲。

資料の所在と入手方法は現 packet では確定できない。Studio が観察結果を創作したり、補足済みと扱ったりしてはならない。

## Decisions already made

この Goal での新しい Decision はなし。

既存仕様への修正として進める。QA の報告では期待挙動は明確であり、Design は省略する。入力追加や戦闘の方向変更は対象外。

## Constraints

- Dry-run project であり、実在の repository はない。資料の読解と実機での実行確認を区別する。
- 実装や技術的原因を推測して再現条件を補わない。
- 未観察の条件を確認済みと扱わない。
- 入力不能中のダッシュ予約や完全同時の境界処理を新たに規定しない。
- QA は独立した executor で実施し、実装者の自己評価や理由説明を受け取らない。
- 下記 Load の完全な本文と補足観察資料が用意されるまで、同じ資料だけの再試行を行わない。

## Open questions

- どの配置と操作で再現し、何回中何回発生するか。
- 初回被弾とダッシュ、再被弾の時間関係はどうなっているか。
- 被弾からダッシュまでの間隔を変えると、発生条件はどう変わるか。
- 攻撃種別、入力方式、FPS による差はあるか。
- 補足観察資料を実行環境から提供できるか。

## Expected output

補足資料がそろえば、QA は再現手順、観察結果、再現性、重大度、受け入れ条件、未確認範囲を含む不具合報告を `to: studio` の Handoff として返す。

資料が提供できなければ、不足資料と、その不足によって確定できない事項を `outcome: question` で Studio に返す。修正済み、再現確定、検証合格とは扱わない。

## Load

以下は次の Step に必要な入力。今回の Route packet にない本文と補足資料は、実行環境側で用意する必要がある。

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: project.md#vision
- Project: project.md#current-state
- Project: project.md#constraints
- Project: design/combat.md
- Project: sim/build-0.3.md
- Project: 補足観察資料（未提供。提供時に所在を明示する）
- Decisions: none
- Previous handoff: goals/G-001-dash-damage/02-qa-to-studio.md
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

<<<FILE goals/G-001-dash-damage/02-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 2
from: qa
to: studio
stage: Observe
outcome: question
---
# 02: qa → studio — 仕様との不一致を確認、再現条件の補足が必要

## Task

模擬ビルドの観察資料を補足し、被弾後のダッシュ中に再被弾する条件と再現性を確定する。現時点では期待挙動は明確だが、再現手順と境界条件が不足しているため、修正へ進む前に追加観察を手配する。

## Context

Owner は「ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい」と報告した。

QA は reproduce-defect の手順に従い、build 0.3 の模擬資料と戦闘仕様を独立に照合した。実ビルドの実行や実装の参照は行っていない。

## Findings

### 根拠と判定

- `design/combat.md` の Player kit：ダッシュは 0.25 秒間で、その全期間が無敵。ダッシュ中の攻撃入力は終了時に発動する。
- 同仕様：通常の被弾は 1 ハートのダメージと 0.3 秒の入力不能を伴い、その後も被弾から 0.8 秒後まで無敵が続く。
- `sim/build-0.3.md` の末尾：被弾直後にダッシュすると、時折ダッシュの途中でダメージを受けるとの観察記述がある。

模擬資料に記載された挙動は、ダッシュ全期間無敵という仕様に反する。Owner の報告を支持する独立した資料上の根拠はあるが、具体的な操作条件・試行結果がないため、最小の再現手順や再現率を確定した報告は未完成。期待挙動の仕様不足ではない。

### 再現手順と条件

資料から抽出できる操作順序は以下までである。確定済みの再現手順ではない。

1. 敵から被弾する。
2. 被弾後、ダッシュを行う。
3. ダッシュの移動途中で再びダメージを受ける場合がある。

不足している条件：

- 部屋、敵の種類・数、最初の被弾と再被弾の攻撃種別。
- 初回被弾からダッシュ入力・開始・再被弾までの時間。
- ダッシュの方向、敵や弾との位置関係。
- キーボード／ゲームパッド、30／60 FPS の設定。
- 試行数、発生数、発生しなくなる条件。

「被弾直後」が 0.3 秒の入力不能中の入力を指すのか、入力不能の終了後を指すのかは不明。被弾中のダッシュ入力の予約可否は仕様に記載されておらず、推測しない。

### 期待挙動と実際の挙動

- 期待：ダッシュ開始から終了までの 0.25 秒間、敵や弾に接触してもハートが減らない。直前の被弾の有無によってこの規則は変わらない。
- 実際：模擬資料では、被弾後のダッシュ途中でダメージが発生する場合がある。
- 未確定：ダメージ量、命中源、ダッシュ内の発生時刻。初回被弾から 0.8 秒以内かどうかも不明なため、被弾後の無敵規則にも違反しているかは判断できない。

### 再現性と重大度

- 再現性：資料上は「時折」。定量的な頻度と確実に発生させる条件は不明。
- 重大度：体験を損なう不具合。仕様上安全な回避行動で体力を失い、回避の信頼性が低下する。進行不能や死亡に至った証拠はない。
- 確認範囲：模擬資料の読解のみ。入力方式・FPS ごとの実行確認や、条件を一つずつ変える比較観察はできていない。

### 既存仕様に基づく受け入れ条件

以下はプレイヤーから観察可能な確認事項であり、実施結果ではない。

1. 被弾後、入力可能になってから開始したダッシュの全期間で、Grub の接触攻撃・Spitter の弾によってハートが減らない。
2. 直前に被弾していない場合も、同じ攻撃に対してダッシュ全期間でハートが減らない。
3. ダッシュ開始直後・途中・終了直前の各接触で上記を満たす。終了後も被弾後の無敵が残っている間はダメージを受けず、両方の無敵が終了した後の有効な命中では通常どおり 1 ハート減る。
4. ダッシュの移動距離 4 タイル、時間 0.25 秒、クールダウン 0.6 秒、およびダッシュ中に入力した攻撃が終了時に発動する挙動を維持する。
5. Desktop のキーボード／ゲームパッドと 30／60 FPS の全組み合わせで確認する。

ダッシュ終了と命中が完全に同時の場合の処理順は仕様から定義しない。境界確認は、終了より前・後と区別できる条件で行う。

## Decisions already made

この Goal での Decision はなし。

既存の D-001 により、攻撃・ダッシュ・ポーズ以外の入力追加には Owner 承認が必要。本報告では入力追加、仕様変更、技術方式の決定を行っていない。

## Constraints

- 実在のゲーム repository はない。模擬資料の記述と実行確認を混同しない。
- QA は実装を変更せず、コード上の原因も断定しない。
- 未観察の入力方式・FPS・攻撃種別を検証済みと扱わない。
- ダッシュ全期間無敵という既存仕様を受け入れ条件の根拠とする。

## Open questions

- 最初と次の命中は、それぞれどの敵・攻撃によるものか。
- 被弾、入力不能終了、ダッシュ入力、ダッシュ開始、再被弾、ダッシュ終了の時系列はどうなっているか。
- どの配置・操作なら再現でき、何回中何回発生するか。
- 被弾からダッシュまでの間隔だけを変えると、発生しなくなる境界はあるか。
- キーボード／ゲームパッド、30／60 FPS で差はあるか。

## Expected output

Studio は、上記の条件と時系列を確認できる模擬観察資料の補足を手配し、QA に再現確認を戻す。

QA は補足資料から再現手順・発生条件・頻度・境界を確定し、受け入れ条件と併せて完成した不具合報告を Studio に返す。現在の資料だけでは条件を補完できないため、`outcome: question` とする。

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: project.md#vision
- Project: project.md#current-state
- Project: project.md#constraints
- Project: design/combat.md
- Project: sim/build-0.3.md
- Decisions: none
- Previous handoff: goals/G-001-dash-damage/01-studio-to-qa.md
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
