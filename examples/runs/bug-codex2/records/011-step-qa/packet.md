# Studio operation packet

operation: Step
goal: G-001
role: qa
incoming_handoff: goals/G-001-dash-damage/10-studio-to-qa.md
next_seq: 11

## You may write

- goals/G-001-dash-damage/11-qa-to-<recipient>.md

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

<<<FILE goals/G-001-dash-damage/10-studio-to-qa.md
---
kind: handoff
goal: G-001
seq: 10
from: studio
to: qa
stage: Observe
outcome: routed
---
# 10: studio → qa — Owner の補足観察から不具合報告を更新する

## Task

Owner の新しい観察を既存の戦闘仕様と模擬ビルドに照合し、再現確認が可能な範囲を評価して不具合報告を更新する。確認できた事実、Owner の報告、未確認事項を区別し、修正に渡せる受け入れ条件と残る必須入力を Studio に返す。

## Context

G-001 の元の依頼は「ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい。」である。

これまでの Observe は補足観察資料が不足したまま `question` を繰り返したため、Studio は Owner にエスカレーションした。Owner は資料を補完して修正を継続する Option A を選び、下記の観察を提供した。今回の再開はこの新しい入力に基づく。

本プロジェクトは dry-run で、実機用リポジトリはない。「ビルドを実行する」とは `sim/build-0.3.md` を読むことである。

## Findings

Owner の回答原文：

> A。私のプレイでの観察です(計測ではなく体感)。部屋1〜2でGrubに噛まれたあと、硬直が解けてから少し間をおいて(被弾から体感0.5〜0.8秒くらい)ダッシュすると、ダッシュの後半で別のGrubに触れてハートが1減る。被弾直後すぐにダッシュした場合と、被弾していないときのダッシュでは起きない。60 FPSのPC・ゲームパッドで10回中6回ほど。Spitterの弾でも1回あった。30 FPSでは試していない。

この入力から得られるのは Owner が報告した発生条件と比較条件である。0.5〜0.8 秒、ダッシュ後半、10 回中 6 回ほどは計測結果として扱わない。「起きない」という比較条件も全条件での非発生保証ではない。

正確なイベント時刻、敵の総数、位置関係、ダッシュ方向、比較条件の試行数、Spitter の詳細条件、30 FPS とキーボードの結果は提供されていない。これらすべてを一律に再開条件とせず、仕様と模擬資料を読んで必要性を判断する。

Resume packet には `design/combat.md` と `sim/build-0.3.md` の本文が含まれていないため、Studio は今回それらの内容を再確認していない。QA の次の packet には Load に指定した本文が必要である。技術原因や独立した再現成功について Studio の判断はない。

## Decisions already made

- `decisions/D-002-resume-with-owner-observations.md` — Owner は Option A を選択し、部分的な観察を使って元の修正 Goal を継続する。仕様変更や修正完了の承認ではない。
- Project の既存制約：攻撃、ダッシュ、ポーズ以外の入力を Owner の承認なく追加しない。

## Constraints

- 既存仕様への不具合修正が対象。戦闘の方向性変更、入力追加、無関係なバランス調整は対象外。
- 対応条件は PC、キーボード・ゲームパッド、30 / 60 FPS。Owner の未試行条件を確認済みとしない。
- Owner の観察と模擬資料に存在しない測定値・試行結果を作らない。
- QA は仕様に対する再現性と受け入れ条件を判断する。実装原因の断定や修正方式の決定は行わない。
- 入力不能中の予約入力や完全同時の境界処理を、この Step で新しく仕様化しない。必要なら仕様上の質問として返す。
- 独立した新しい executor で実施する。実装者の説明・自己評価は入力に含めない。

## Open questions

- 既存仕様と模擬ビルドから、報告された被ダメージをどこまで独立して確認できるか。
- 被弾後に間をおいたダッシュ、直後のダッシュ、未被弾時のダッシュを比較するための手順と期待結果を、既存仕様から記述できるか。
- Grub 接触と Spitter の弾について、確認済み範囲と未確認範囲は何か。
- 修正に渡せる不具合報告と受け入れ条件を作れるか。作れない場合、不可欠な不足情報は何で、既存資料から得られない理由は何か。

## Expected output

次の Handoff を `to: studio` として作成し、Findings に次をまとめる。

- 資料と根拠を示した不具合報告：条件、手順、仕様上の期待結果、報告または確認された実際の結果。
- Owner の報告、模擬資料で確認できた事実、未実施・不明の範囲の明確な区別。
- 既存仕様に基づくプレイヤーから観察可能な受け入れ条件。30 / 60 FPS と両入力方式を含む後続検証の対象。
- Build に渡せるか、追加の調査や入力が必要かを判断できる具体的な残件。

評価を完了できれば `outcome: done`、必須資料や判断が不足して進めない場合は `outcome: question` とする。これは修正後の Verify ではなく、修正合格を宣言しない。資料不足の場合も、今回の観察で何が解消し、何がなお不可欠かを明記する。

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: project.md#vision
- Project: project.md#current-state
- Project: project.md#constraints
- Project: design/combat.md
- Project: sim/build-0.3.md
- Decisions: decisions/D-002-resume-with-owner-observations.md
- Previous handoff: goals/G-001-dash-damage/09-studio-to-owner.md（Owner 回答を含む解決済み Escalation）
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

<<<FILE goals/G-001-dash-damage/09-studio-to-owner.md
---
kind: escalation
goal: G-001
seq: 9
from: studio
to: owner
status: resolved
decision: D-002
---
# 09: Owner decision needed — 再現資料の補完と継続方法

## Question

ダッシュ中の被ダメージ修正を進めるため、補足観察資料または取得方法を提供しますか、それとも調査報告への範囲縮小か中止を選びますか。

## Why this needs the Owner

QA は同じ補足観察資料の不足について繰り返し `question` を返しており、最新の `08-qa-to-studio.md` でも不足は解消していません。`studio/orchestration.md` の Loop limits は、同じ不足入力について新しい情報なしに二回 question が返った場合、Role に再投入せず Owner にその入力を求めるよう定めています。

このプロジェクトは模擬資料を読む dry-run で、実機用リポジトリはありません。現在の packet に追加観察記録も取得手段もないため、Role は既存記述から実際のイベント時刻や試行結果を生成できません。資料の提供可否は未確認であり、提供不能と判断したわけではありません。

ゲーム内容の判断ではなく、繰り返し不足している入力と継続方法についての手続き上のエスカレーションです。

## Options

### Option A — 資料を補完して修正を継続する

補足観察資料の本文、または取得先と入手方法を提供してください。実行環境側で補完できる場合は、その方法と提供可能な範囲を知らせてください。

必要な情報は次のとおりです。部分的な資料でも、未観察・不明の範囲を明記して受け付けます。

- 部屋、敵の種類・数、命中源、位置関係、ダッシュ方向と操作手順。
- 初回被弾、入力不能終了、ダッシュ入力・開始、再被弾、ダッシュ終了の時刻とハート変化。
- 被弾からダッシュまでの間隔、攻撃種別、入力方式、FPS ごとの試行数・発生数と未観察範囲。

資料を揃える手間は必要ですが、元の修正 Goal を維持できます。ゲーム仕様や実装はこの選択だけでは変更しません。

If chosen: Studio が資料を確認して QA の Observe を再開します。一部のみ提供された場合は確認可能な範囲を QA が判断します。その結果に応じて必要な技術調査・計画、Build、独立した Verify へ進みます。取得先だけが示された場合は資料取得後に再開し、同じ packet を再投入しません。

### Option B — 現資料での調査報告に範囲を縮小する

修正ではなく、既知の仕様不一致と未確認事項をまとめる Goal に変更します。追加資料の準備負担を避けられますが、不具合は未修正のままで、再現確定や検証合格は主張できません。

If chosen: Studio が Owner による範囲変更を Decision に記録し、ルートを調査報告の取りまとめへ変更します。修正は資料が揃った時点で別 Goal として扱えます。

### Option C — 中止する

今回の Goal を未修正のまま終了します。追加作業は不要ですが、報告された問題は残ります。

If chosen: Studio が中止理由と未解決事項を記録し、Goal を abandoned にします。

## Studio recommendation

Option A。まず提供できる資料と取得方法を知らせてください。全項目が揃っていることを回答の条件にはしません。

## Reasoning

Owner の元の依頼は修正であり、QA は既存仕様に基づく受け入れ条件を引き継いでいます。追加資料が得られれば、その依頼を維持して進められます。

基本資料の補完は済みましたが、再現条件に関する新しい観察はありません。同じ資料で QA を繰り返しても、この不足は解消しません。提供が難しいことや追加作業を望まないことが確認された場合は、B または C を選ぶ根拠になります。

## Meanwhile

エスカレーション中は独立して進められる作業がなく、残る作業を停止した。回答受領後の再開先は `10-studio-to-qa.md`。Build や仕様変更はこの回答だけでは開始しない。

## Owner decision required

回答済み。Option A を選択し、体感による部分的な観察を提供した。選択と観察の扱いを `decisions/D-002-resume-with-owner-observations.md` に記録した。

---

**Owner response (2026-10-10):** A。私のプレイでの観察です(計測ではなく体感)。部屋1〜2でGrubに噛まれたあと、硬直が解けてから少し間をおいて(被弾から体感0.5〜0.8秒くらい)ダッシュすると、ダッシュの後半で別のGrubに触れてハートが1減る。被弾直後すぐにダッシュした場合と、被弾していないときのダッシュでは起きない。60 FPSのPC・ゲームパッドで10回中6回ほど。Spitterの弾でも1回あった。30 FPSでは試していない。

## Resolution

2026-10-10 — D-002 により解決。Goal を active に戻し、新しい観察を入力として QA の Observe を再開する。資料不足がすべて解消した、再現できた、修正できたという意味ではない。残る不足と確認可能な範囲は QA が判断する。
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
