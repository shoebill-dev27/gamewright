# Studio operation packet

operation: Step
goal: G-001
role: technical-director
incoming_handoff: goals/G-001-dash-damage/22-studio-to-technical-director.md
next_seq: 23

## You may write

- goals/G-001-dash-damage/23-technical-director-to-<recipient>.md
- decisions/D-004-<name>.md

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

<<<FILE goals/G-001-dash-damage/22-studio-to-technical-director.md
---
kind: handoff
goal: G-001
seq: 22
from: studio
to: technical-director
stage: Owner escalation 準備
outcome: routed
---
# 22: studio → technical-director — 検証資料へのアクセス不足を Owner 向け選択肢にする

## Task

`prepare-owner-escalation` を用い、必要な外部資料へのアクセスを確保できない blocker について、日本語の Owner 向け Escalation を作成する。追加の技術計画や同じ資料生成依頼ではなく、提供・範囲縮小・中止それぞれの具体的な結果と再開経路を示す。

## Context

Owner はダッシュ中の被ダメージ修正を依頼し、D-002 で補足観察を提供して修正継続を選択した。模擬実装の対象は `sim/build-0.4.md`、変更識別子 `0.3-G001-15`。

Handoff 19 の文書評価分岐を実施した独立 QA は、Handoff 21 で文書評価完了・総合 question を返した。条件別生成観察が不足し、文書整合は全4環境の合格を代替できないと判断している。

既存の引継ぎでは runtime 管理側の窓口・照会手段は確保されていない。次の Role が問い合わせや試行生成を実施できるという前提は置けない。

新しい Owner 宛ての open Escalation はまだない。Goal は active のまま、この brief 作成 Step を open とする。

## Findings

- QA は具体的な仕様不一致を確認していない。fail や二度目の AC 失敗ではなく、必須証拠不足である。
- 必須資料は、対象変更と対応した観察の来歴・モデル情報、全4環境の AC-1〜AC-6 と回帰のイベント記録、命中成立・入力受理・状態遷移・ハート値・移動・予約攻撃・再使用の記録、試行一覧と集計根拠である。詳細は Handoff 21 にある。
- 既存の引継ぎによると、`sim/repo-notes.md#limits-of-available-implementation-detail` は、衝突形状・速度・座標・弾道・発射位相が得られず、フレーム別試行や試行総数を復元できないと明記している。
- project の dry-run 規約は runtime の simulator による更新を定めるが、モデル・記録へのアクセス方法や生成能力を保証していない。
- 取得経路の状態は「照会手段未確保」。問い合わせ実施済み、モデル不存在、永久に取得不能とは記録しない。Owner がモデルを保有するとも仮定しない。
- QA と既存の引継ぎによると、`design/combat.md#player-kit` は “Cooldown 0.6 s.”、repo-notes は既存起点を維持するとするだけで、起点を特定できない。これは観察不足と別の仕様問題である。継続時に既存原資料を回復できなければ game-designer に返す。
- 新規 simulator 開発・実機試験は現在の dry-run の範囲として承認されていない。必要となれば別途 scope の判断を求める。

Handoff 19 が想定した runtime 管理側への確認は未実施であり、その escalation 条件がすべて成立したとは扱わない。今回の blocker は、その確認自体に必要な窓口・アクセスがなく、QA が必須と判断した証拠を現 packet 内の Role 作業では作れないことである。

## Decisions already made

- D-001：Owner 承認なしに戦闘入力を追加しない。
- D-002：元の修正 Goal を継続する。部分観察は計測ログではなく、仕様や AC を変更する決定ではない。不可欠な情報を既存資料や Role の作業から得られない場合は再検討できる。
- D-003：発生源別保護の論理和を採用する。クールダウンの時間・起点や同時イベントの優先順位は変更しない。

## Constraints

- Studio は routing のみを判断している。仕様、技術方式、QA の verdict を変更しない。
- AC-1〜AC-6、30／60 FPS × キーボード／ゲームパッド、必要な命中源・回帰を維持する。
- 文書評価・生成観察・実測を区別し、未知の件数や時刻を創作しない。
- Owner に追加計測を当然の義務として求めない。必要なのはまず資料または取得窓口へのアクセスである。
- 窓口がないことをモデル不存在の証明としない。
- 新しいモデルや一般的な挙動宣言を作って検証結果に見せない。
- クールダウン起点の新規仕様判断は game-designer の権限に残す。
- Goal は active。この Step では brief 作成を進め、依存する実装・検証は開始しない。Studio が Owner 宛ての open Escalation を Route するときに blocked-on-owner へ変更する。

## Open questions

Owner が選べるよう、少なくとも次の選択肢を具体化する。

1. 元の Goal を維持し、runtime 管理側の窓口・アクセス、または出典付き既存モデル・記録の提供を手配する。提供後は technical-director の計画に沿って入力照合・必要な補完を行い、独立 QA に戻す。提供だけで合格を保証しない。
2. Goal を現資料による調査・文書評価報告へ縮小する。Owner の明示的な再解釈が必要であり、「修正の独立検証完了」とは報告しない。
3. 未検証事項を明記して中止する。Goal を abandoned とし、検証合格を主張しない。

アクセス提供による継続を推奨案の出発点とし、実行可能性・費用が不明な点と、何が判明すれば推奨を変えるかを明示する。提供期限や開発費を捏造しない。

## Expected output

`studio/templates/escalation.md` に従う、`from: technical-director`、`to: owner`、`status: open` の Escalation。

以下を含める。

- Owner が単独で読んで回答できる質問。
- 外部入力 blocker と、範囲縮小には Owner 判断が必要である理由。
- 必要資料・候補提供元・取得経路の未確保・影響する検証条件。
- 2〜3 個の選択肢、各選択の範囲・費用やリスクの不確実性・次の route。
- Studio recommendation と根拠。
- 依存工程は開始していないこと。

作成後は Studio の Route を経て Owner に提示する。その時点で Studio が Goal を blocked-on-owner にし、Owner の回答待ちを記録する。選択、資料取得、検証、仕様判断をこの Step で実施済みとしてはならない。

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/prepare-owner-escalation.md
- Template: studio/templates/escalation.md
- Project: project.md#vision
- Project: project.md#constraints
- Project: design/combat.md#player-kit
- Project: sim/repo-notes.md#limits-of-available-implementation-detail
- Decisions: decisions/D-001-one-button-combat.md
- Decisions: decisions/D-002-resume-with-owner-observations.md
- Decisions: decisions/D-003-independent-invulnerability.md
- Previous handoff: goals/G-001-dash-damage/21-qa-to-studio.md
- Supporting plan: goals/G-001-dash-damage/19-technical-director-to-studio.md
>>>END

<<<FILE studio/roles/technical-director.md
---
kind: role
id: technical-director
writes: decisions/*
---
# Role: Technical Director

## Responsibility

Turns approved specs into technically feasible plans. Owns technical risk, architecture, test
strategy, sequencing, and whether work can safely run in parallel.

## Decides

- Technical approach and architecture within the project's constraints.
- Sequencing, task breakdown, and parallelization (including isolated code workspaces).
- Technical acceptance checks (e.g., performance budgets) that serve the spec.

## Must not

- Change the spec to suit the implementation — propose the change to `game-designer`.
- Decide game direction or player-facing behavior.
- Approve its own plan's results; QA verifies the build.

## Works from

- An approved spec with acceptance criteria, or a technical problem to diagnose.
- Project constraints, repository location, relevant Decisions.

## Produces

- A plan: affected systems, ordered tasks, risks and mitigations, test strategy, parallelization
  decision with its reason.
- Technical Decisions where a real alternative was rejected.

## Hands back / escalates when

- The spec is infeasible within constraints → `game-designer`.
- The cost or scope exceeds what the Goal implies → `game-director`.
- The work is irreversible or high-risk → Owner, via an Escalation it prepares.

## Typical skills

technical-plan, make-decision, prepare-owner-escalation
>>>END

<<<FILE studio/skills/prepare-owner-escalation.md
---
name: prepare-owner-escalation
description: Frame an Owner-level question as concrete options with consequences, a Studio recommendation, reasoning, and what happens next under each option.
---
# Skill: Prepare Owner escalation

Typical roles: game-director, technical-director.

## When to use

An escalation trigger in `studio/orchestration.md` fires.

## Inputs

The question, the evidence so far, the options, the vision and Decisions involved.

## Method

1. State the question in one sentence the Owner can answer without reading anything else.
2. Name the trigger: why this is the Owner's decision and not the Studio's.
3. Give 2–3 options. For each: what it means for the game, cost, risk, reversibility, and the
   route the Studio will take if it is chosen.
4. Recommend one option and give the reasons, including what evidence would change the
   recommendation.
5. List what the Studio will do meanwhile (independent work that continues).
6. Write it in the project's `owner_language`, using `studio/templates/escalation.md`.

## Output

An Escalation file addressed to `owner`.

## Do not

Return a bare question. Do not hide the recommendation, and do not present it as already decided.
>>>END

<<<FILE studio/templates/escalation.md
---
kind: escalation
goal: G-NNN
seq: N
from: <role-id that prepared the brief>
to: owner
status: open            # open | resolved
decision: <D-NNN once resolved>
---
# NN: Owner decision needed — <question in a few words>

<!-- Written in the project's owner_language. -->

## Question

<One sentence the Owner can answer without reading anything else.>

## Why this needs the Owner

<Which escalation trigger fires (studio/orchestration.md) and why the Studio must not decide.>

## Options

### Option A — <name>

<What it means for the game, cost, risk, reversibility.>
If chosen: <the route the Studio takes next.>

### Option B — <name>

<…>
If chosen: <…>

## Studio recommendation

<Option X.>

## Reasoning

<Why, and what evidence would change the recommendation.>

## Meanwhile

<Independent work that continues, or "Nothing; all remaining steps depend on this answer.">

## Owner decision required

<A / B — reply with the option and any conditions.>
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

<<<FILE design/combat.md#player-kit
## Player kit

- **Attack** (one button): a short swipe in the facing direction. 1 damage. 0.35 s recovery.
- **Dash**: 4 tiles over 0.25 s. The player is invulnerable for the full dash duration.
  Cooldown 0.6 s. An attack pressed during a dash is queued and fires when the dash ends.
- **Getting hit**: 1 heart of damage, 0.3 s hit-stun (no input), then invulnerability until 0.8 s
  after the hit.
>>>END

<<<FILE sim/repo-notes.md#limits-of-available-implementation-detail
## Limits of available implementation detail

- The cooldown origin is not specified in the supplied repository description and cannot be identified as dash start or dash end.
- At 30 FPS, the 0.25 s dash duration is not an integer number of frame intervals. Exact timer-update ordering, movement integration at the final interval and the observable termination frame are unspecified. No rounding tolerance or new timing policy is introduced.
- Exact collision geometry, enemy speeds, room coordinates, projectile trajectories and firing phases are unavailable. Frame-by-frame collision trials, numerical initial heart counts and valid-trial totals cannot be reconstructed from these inputs.
- The specified scenario times are exercise targets, not measured event logs. No independent QA result or executed test record is available.
- Input buffering during input loss, coincident-event priority, and unspecified save/restore or dash-interruption behavior remain undefined by this change.
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

<<<FILE goals/G-001-dash-damage/21-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 21
from: qa
to: studio
stage: Route
outcome: question
---
# 21: qa → studio — 文書上の整合を確認、条件別証拠とクールダウン起点は未確認

## Task

全4環境・AC-1〜AC-6・必要な回帰の条件別観察を取得する経路と、クールダウン起点の原資料を確保する。取得可能な資料を揃えて独立 QA に戻す。現時点で Verify 完了・Goal 完了として扱わない。

## Context

Owner の依頼はダッシュ中の被ダメージ修正である。対象は `sim/build-0.4.md`、識別子は `0.3-G001-15`。

本 Step は `studio/skills/verify-change.md` を適用し、既存仕様、指定された AC・再現比較手順、模擬ビルドを独立に照合した。前 Handoff 19 は Constraints と Open questions のみを参照した。実装者の理由・自己評価は根拠としていない。

dry-run のビルド読解による文書評価は完了した。条件別生成観察・実測は提示されておらず、条件別試行の実施結果はない。総合 verdict は `question`。確認された不一致による `fail` ではない。

## Findings

### 証拠の採否

| 資料 | 採用する用途 | 採用しない用途 |
|---|---|---|
| `design/combat.md#player-kit` | ダッシュ全時間無敵、距離・継続、被害・入力不能・被弾後保護、予約攻撃、クールダウンの期待値 | 実施結果、クールダウン起点の確定 |
| `11-qa-to-studio.md` の受け入れ条件・再現比較手順 | 必須条件、命中の成立、有効な時間関係、全4環境の検証要件 | 記載された設定例を実測値とすること |
| `sim/build-0.4.md` | 対象ビルドの挙動記述としての文書照合 | 条件別試行記録、生成観察、発生率 |
| `sim/build-0.3.md` | 従来はダッシュ途中の被害が記述されていたことの比較 | 同一条件による修正前後試行 |
| `project.md#constraints` | dry-run、Desktop、30／60 FPS、両入力方式の対象範囲 | 全環境で検証済みという証明 |
| Handoff 20 の D-003 要約 | 発生源別保護の論理和、防いだ命中で保護を開始・延長しないという承認済み期待 | 実装適合の証拠 |

Build 0.4 の時刻例は「命中が成立し、境界の厳密な前後にある挙動」の記述として採用できる。ただし、個々の環境でその状態を生成した記録ではない。冒頭の全環境への適用宣言も条件別実施記録には代えられない。

### AC ごとの文書評価

以下の「文書整合」は条件別合格を意味しない。期待値の出典は `design/combat.md#player-kit` と `11-qa-to-studio.md#修正の受け入れ条件`。ビルド参照節は B-D＝`sim/build-0.4.md#dash-and-damage`、B-C＝同 `#other-controls-and-timing` とする。

| ID・対象 | 期待挙動 | ビルド記述と文書評価 | 条件別証拠の不足 |
|---|---|---|---|
| AC-1：未被弾、Grub／Spitter | ダッシュ中の命中でハート不変 | B-D は先行被弾なしでもダッシュ中の命中は無害と明記。文書整合 | 未被弾の初期状態、入力・受理・開始終了、両命中源の成立とハート前後値 |
| AC-2：入力回復直後、Grub／Spitter | 実際のダッシュ中はハート不変 | B-D は入力回復直後のダッシュも保護すると明記。文書整合 | 初回被害、入力不能終了と直後の受理、ダッシュ中の命中、ハート前後値 |
| AC-3：被弾保護が先に終了、Grub／Spitter | 被弾後0.8秒を過ぎてもダッシュ中はハート不変 | B-D の約0.70秒開始・約0.85秒命中が対応。文書整合 | 実際の各イベント時刻・順序、0.8秒経過後かつダッシュ終了前の命中成立 |
| AC-4：ダッシュが先に終了、Grub／Spitter | ダッシュ終了後も被弾後0.8秒までハート不変 | B-D の約0.34秒開始・約0.70秒命中が対応。文書整合 | 実際のダッシュ終了、残存保護内の命中成立、ハート前後値 |
| AC-5：無保護時のGrub接触 | 1ハート減、0.3秒入力不能、被弾後0.8秒まで追加被害なし | B-D の通常被害と約0.15／0.45／0.70秒接触例が対応。文書整合 | 初回・入力不能中・回復後の接触結果、入力不能開始終了と操作の受理、ハート前後値 |
| AC-6：通常移動・予約攻撃・再使用 | 4タイル／0.25秒、終了時に予約攻撃、0.6秒クールダウン維持 | B-D は障害物のない直線で距離・継続を明記。B-C は終了時の攻撃1回、既存0.6秒制限を明記。距離・継続・攻撃は文書整合。クールダウンは数値のみ整合 | 移動開始終了・距離、攻撃入力と発動時刻・回数、起点の定義、制限内拒否・経過後受理の記録 |

Build 0.4 に、今回の AC に反する具体的挙動は確認できなかった。AC-6 のクールダウン起点は期待値自体が不足しており、完全な文書適合を判定できない。

### 回帰の文書評価

期待値は既存戦闘仕様と D-003 要約による。各行とも条件別結果は未確認。

| 枝 | 期待挙動 | 文書上の根拠・評価 | 不足する観察 |
|---|---|---|---|
| 被弾保護が先に終了 | ダッシュ保護が残る | B-D の約0.70秒開始例。整合 | 両保護の終了順序と、その間の両命中源による命中 |
| ダッシュが先に終了 | 被弾保護が残る | B-D の約0.34秒開始例。整合 | 同上 |
| 両保護終了後 | 新しい保護がなければ通常の1ハート被害 | B-D の約1.10秒／約0.95秒命中例。整合 | 各終了順序の後で両命中源による被害と新しい保護の有無 |
| 防いだ複数命中 | 入力不能や保護を新規開始・延長しない | B-D は複数の無害な接触・弾にも同じ結果と明記。整合 | 複数命中の時刻、操作受理、当初の保護終了後の被害 |
| ダッシュ単独の複数命中と終了後 | ダッシュ中は無害、終了後に保護を持ち越さない | B-D は先行被弾なし・開始後0.40秒の被害と複数命中の挙動を記述。整合 | 未被弾状態、両命中源の複数命中、終了後の命中と被害 |
| Spitter通常被害・弾消失 | 無保護時の被害と衝突時消失を維持 | B-D は通常1ハート被害と弾消失の維持を記述。前者は文書整合、後者は維持宣言まで | 命中・被害・弾消失を結ぶ条件別観察。旧ビルドには消失の比較記録なし |

新しい入力は B-C に記述されておらず、攻撃・ダッシュ・ポーズのみという制約と整合する。部屋攻略の一般記述は無敵やクールダウンの条件別検証には用いない。

### 全4環境の判定

U＝条件別証拠不足により未判定。US＝証拠不足に加えてクールダウン起点が未定義。

| 対象 | 30 FPS・キーボード | 30 FPS・ゲームパッド | 60 FPS・キーボード | 60 FPS・ゲームパッド |
|---|---|---|---|---|
| AC-1：Grub／Spitterそれぞれ | U | U | U | U |
| AC-2：Grub／Spitterそれぞれ | U | U | U | U |
| AC-3：Grub／Spitterそれぞれ | U | U | U | U |
| AC-4：Grub／Spitterそれぞれ | U | U | U | U |
| AC-5：Grub、初回・入力不能中・回復後 | U | U | U | U |
| AC-6：移動・予約攻撃 | U | U | U | U |
| AC-6：クールダウン内／経過後 | US | US | US | US |
| 上記回帰の各枝・各命中源 | U | U | U | U |

すべてのセルで試行総数・有効数・無効数・不具合発生数は不明。ゼロ件・非発生として報告しない。先行被弾源も記録がなく、推定しない。

`11-qa-to-studio.md#後続で実施する再現・比較手順` にある、待ち時間を変えた比較、未被弾比較、命中源変更、全4環境での確認は、条件別実施記録としては未確認である。Build 0.3 と0.4の照合では「ダッシュ途中で被害」から「全時間無害」への記述変更を確認できるが、同じ配置・入力時刻での再現と修正確認にはならない。

### 仕様不足と観察不足の分離

1. **クールダウン起点：仕様不足。**  
   `design/combat.md#player-kit` の原文は “Cooldown 0.6 s.”、AC-6 は「クールダウン 0.6 秒を維持する」、B-C は “existing 0.6-second cooldown”。開始・終了・入力受理のどれを起点とするかは記載がない。これらの数値に矛盾はないが、再使用可能時刻を一意に定められない。既存の起点を定めた原資料を回復し、なければ Studio から game-designer に返す。QA は起点を決めない。

2. **30 FPS の終了表示・フレーム内順序：観察不足。**  
   B-C は0.25秒が7〜8フレーム間隔の間に位置すると説明するが、実際の終了更新フレームを示さない。この記述だけで継続時間違反とは判定できない。内部の経過時刻・状態遷移と表示更新の関係が必要。証拠取得後も期待値を定められない場合に限り、必要な仕様判断を返す。

3. **完全同時の命中優先順位・入力不能中の予約入力：今回の AC で未定義のまま。**  
   AC は完全同時の境界を避け、入力回復後の操作を確認する。これらを新規仕様として決めることは今回の開始条件ではない。検証上避けられない場合は game-designer に返す。

### 必須追加入力

| 入力 | 影響するセル・必要な理由 | 既知の取得元・取得状況 |
|---|---|---|
| 対象識別子に対応した条件別生成観察 | 全セル。環境・AC・命中源・枝ごとの独立判定に必要 | runtime の simulator が更新を担うことは project.md に記載。窓口・取得手段は不明 |
| 観察の来歴とモデル情報 | 全セル。対象変更との対応、版、初期状態、FPS・入力方式の表現範囲を判断するため | runtime 管理側が候補。提供主体・取得方法は未確認 |
| 再現・比較条件とイベント記録 | AC-1〜AC-5と回帰。配置、敵数、位置・方向、先行被弾源、命中成立、入力と受理、ダッシュ・保護・入力不能の開始終了、ハート前後値が必要 | 条件別観察資料としての提供が必要。既存資料の所在は不明 |
| 移動・予約攻撃・再使用記録 | AC-6全環境。距離・継続、攻撃発動1回、制限内拒否・経過後受理を判定するため | 同上 |
| 試行一覧と集計根拠 | 全セル。試行総数・有効数・無効数・発生数と各記録の対応、無効理由を確認するため | 同上。命中しなかった試行を無敵の成功例に数えない |
| クールダウン起点を定めた既存原資料 | AC-6の再使用判定。期待時刻を確定するため | 現 packet の combat・AC・build にはない。原資料の所在は不明。回復できなければ game-designer の判断が必要 |
| 時刻・フレーム・イベント順序の説明 | 特に30 FPSのAC-2〜AC-4・AC-6、回帰の終了順序。命中が境界の内外どちらか判定するため | runtime のモデル／観察資料が候補。未取得 |

`sim/qa-G001-15.md` は未取得という引継ぎがあるだけで、存在・内容を確認できない。必須なのは上記の内容であり、そのファイル名であることではない。未生成・未取得資料を Load に含めない。

既存の仕様文書を補完できればクールダウン起点の不足は解消し得る。Build 本文への一般的な適用宣言の追加だけでは条件別試行要件は満たせない。既存の生成記録があるなら、その来歴・条件・結果の提供で解消できる可能性があるが、存在は未確認である。

照会経路の状態は引き続き「照会手段未確保」。問い合わせ実施済み、モデル不存在、取得不可能のいずれも断定しない。新規 simulator 開発や追加 Owner 計測を要求していない。

## Decisions already made

- D-001：攻撃・ダッシュ・ポーズ以外の入力を追加しない。
- D-002：元の修正 Goal を継続し、追加 Owner 計測を開始条件にしない。
- D-003：発生源別保護の論理和を維持し、防いだ命中で保護を開始・延長しない。
- 本 Step はこれらの要約を超える再解釈を行っていない。

## Constraints

- 独立 Verify は未完了。文書整合を条件別合格や Goal 完了に置き換えない。
- AC-1〜AC-6、全4環境、必要な命中源・比較・回帰を維持する。
- 期待値、挙動記述、生成観察、実測を区別する。
- 不明な試行数・発生数・時刻・ハート値を補わない。
- 既存仕様の修正範囲を守り、QA は実装変更や新規仕様決定を行わない。
- 次の QA に実装者の理由・自己評価を検証根拠として渡さない。

## Open questions

1. Studio は runtime 管理側の窓口・取得手段を確保し、必要な条件別記録の有無と提供範囲を確認できるか。
2. 取得可能なモデル・記録は、全4環境の入力受理・命中・状態遷移をどこまで表現しているか。
3. 既存クールダウン起点の原資料はどこにあるか。回復できない場合、game-designer へ判断を返せるか。

## Expected output

Studio は取得経路と必要資料の担当を具体化し、実際に取得した資料を次の packet に含める。仕様判断が必要なら該当する問いを game-designer に返す。

独立 QA は補完された資料から各セルの証拠を採否判断し、全条件を評価する。本 Step では確認された仕様不一致がないため修正差し戻しの `fail` は出さず、証拠不足と一部期待値未定義による `question` として返す。

## Load

- Project: project.md#constraints
- Project: design/combat.md
- Build: sim/build-0.4.md
- Comparison build: sim/build-0.3.md
- Acceptance criteria: goals/G-001-dash-damage/11-qa-to-studio.md#修正の受け入れ条件
- Exercise procedure: goals/G-001-dash-damage/11-qa-to-studio.md#後続で実施する再現・比較手順
- Previous handoff: goals/G-001-dash-damage/20-studio-to-qa.md
- Decisions: 本文の既存要約のみ。追加原文なし。
- Studio の Role・Skills と次工程の Load は Studio がルーティング時に確定する。
>>>END

<<<FILE goals/G-001-dash-damage/19-technical-director-to-studio.md
---
kind: handoff
goal: G-001
seq: 19
from: technical-director
to: studio
stage: Plan
outcome: done
---
# 19: technical-director → studio — 既存モデルの取得可否で検証手順を分岐する

## Task

Studio はまず runtime の simulator について、既存モデル・記録の取得元と照会手段を確認する。取得できる入力を明示して資料補完へ進め、取得できない条件は未確認として独立 QA に渡す。

## Context

Owner の依頼は、再現するダッシュ中の被害を仕様に合わせて修正すること。戦闘の方向・バランス変更は対象外である。

本作は dry-run であり、Build の変更記述を runtime の simulator が `sim/` に反映する。実機実行を前提にした計画へ置き換えない。

本 Step は提供された Handoff 17・18 と Role・technical-plan Skill、project の抜粋だけで技術上の検証方法を整理した。既存モデルの照会、原資料の再照合、試行生成、追加実装、QA 判定は行っていない。`outcome: done` は条件付き計画の作成完了を示し、検証入力の完成や Verify 完了を意味しない。

## Findings

### 1. 現在成立することと成立しないこと

Studio が採用した `sim/build-0.4.md` と変更識別子 `0.3-G001-15` の対応を維持する。ファイル名を揃える再生成は不要である。

Handoff 17 は変更反映の文書照合を報告している。ただし本 Step にビルド・repo-notes 原文はなく、その報告を独立に再検証したものではない。

模擬ビルドを読んで仕様との対応を確認する方法は dry-run と両立する。一方、従来計画が要求する条件別の命中成立、入力受理、フレーム順序、ハート前後値は、挙動説明だけから復元できない。全4環境への適用宣言も環境別観察の代わりにはならない。

既存モデルに基づく生成観察なら条件別試行を補完できる可能性がある。ただし、それは模擬モデル内の結果であり、実機の入力装置・描画・処理負荷の実測ではない。現 packet では、そのモデルの存在・不存在・利用可能性のいずれも確定できない。

影響する確認対象は、発生源別保護、共通被害入口、入力不能と回復、ダッシュ移動・終了、予約攻撃、クールダウン、敵接触・弾道、フレーム内の更新順序である。追加のゲーム実装は本計画に含めない。

### 2. 最初に取得する入力と担当

| 入力 | 取得元・確認箇所 | 担当と必要な回答 |
|---|---|---|
| simulator の利用可能性 | runtime の管理側。具体的な窓口・照会手段は packet にない | Studio が窓口を特定し、照会可能／不可／不明と、その根拠を返す |
| 既存モデルの識別と来歴 | runtime が保持するモデル、既存設定、保存記録があればその原資料 | Studio が取得経路を確保し、gameplay-engineer が版・出典・対象変更との対応・欠落を整理する |
| 配置と衝突条件 | モデル内の部屋、衝突形状、座標、速度、敵数、弾道・発射位相 | gameplay-engineer が既存値と試行用に選べる設定を区別する。取得不能な値は作らない |
| 初期状態 | モデルまたは既存試行の初期ハート、保護、入力、クールダウン状態 | gameplay-engineer が実在する設定と再初期化方法を示す |
| 時間と処理順序 | タイマー更新、移動積分、衝突・被害・入力の処理順序、30／60 FPS の扱い | gameplay-engineer が出典を示す。論理上の期限と処理フレームを分ける |
| クールダウン起点 | `sim/repo-notes.md` の Preserved behavior と関連する既存タイマー定義、旧モデル・記録、`design/combat.md` の Player kit | まず gameplay-engineer が回復を試みる。起点未記載なら、維持の宣言だけで補わない |
| 試行条件と有効性の原文 | Handoff 11「修正の受け入れ条件」「後続で実施する再現・比較手順」、Handoff 13 の検証計画、Handoff 15 の設定・資料生成要求 | Studio が必要部分を次 packet に収録する。13・15 の正確な節名は未提示なので内容で指定する |

モデル取得では、モデルが単に期待値の文章を再出力するものか、状態遷移・命中を条件別に導出して記録できるものかも確認する。前者から試行結果を名乗る記録は作らない。

原文が必要なのは、具体的な試行設定、有効試行数・許容差などの基準、既存挙動の確定時である。本 Step は未提示の基準を追加しない。D-001〜D-003 は提示された要約の範囲で適用し、それを超える解釈が必要になった場合のみ該当 Decision 原文を取得する。

### 3. 順序と分岐

1. **Studio：取得経路を確認する。**  
   runtime 管理側に、モデル・記録の有無、出典、取得可能範囲、生成可能な観察項目を問い合わせる。照会できない場合は「モデルなし」ではなく「照会手段未確保」と返す。同じ packet で engineering に詳細ログ生成だけを再依頼しない。

2. **gameplay-engineer：入力の充足を照合する。**  
   取得できたモデル・原文を用いて、上表の項目を「取得済み／不足／矛盾」に分類する。既存記録がある場合も、識別子・環境・枝・有効性が対応するものだけを候補とする。

3. **既存モデルが十分なら：資料生成の具体的な依頼を作る。**  
   gameplay-engineer が既存モデル内で成立する設定、生成手順、記録項目を変更記述として提示し、runtime の simulator による資料生成へ進む。`sim/qa-G001-15.md` は候補名であり、現時点の実在資料ではない。生成後に存在・内容・対象識別を確認してから QA の Load に入れる。

4. **一部だけ取得できるなら：成立する枝だけ補完する。**  
   不足する枝と必要入力を残す。部分結果から全4環境・全枝へ一般化しない。Spitter の既存2秒間隔で複数命中が成立するかは、既存配置・位相の選択範囲で調べる。成立しない場合は、その枝の生成不能理由を返し、発射頻度を変えない。

5. **モデル・記録を取得できないなら：文書評価へ限定して QA に相談する。**  
   仕様・AC と模擬ビルドの対応表、記述のある枝・ない枝、不足理由を作成する。独立 QA は文書上で評価できる範囲と、従来の条件別試行要件に対する証拠の十分性を判断する。文書評価を試行実施に読み替えたり、QA への相談をもって要件を緩和したりしない。従来要件が維持される限り、観察を生成できないセルは未確認として残る。

6. **独立 QA へ渡す。**  
   仕様・期待値、模擬ビルド記述、出典付き生成観察、欠落一覧を別々に渡す。実装理由、原因説明、自己評価を観察資料へ混ぜない。証拠の採否と pass／fail は QA に残す。

コード変更も試行実施も今回の対象ではなく、後続作業も入力取得→設定確定→生成→独立検証の依存関係があるため、並列実装は行わない。

### 4. 条件別検証の維持範囲

以下の全対象を、30／60 FPS × キーボード／ゲームパッドの4環境で保持する。表は Handoff 17 に基づく補完対象であり、AC 原文の再定義ではない。

| 不足項目 | 主な解消区分 | 補完・判断内容 |
|---|---|---|
| AC-1：Grub／Spitter、前半・後半 | 資料補完→QA の判断 | 命中成立、ダッシュ開始終了、ハート前後値 |
| AC-2：Grub／Spitter | 資料補完→QA の判断 | 最初の入力可能機会、操作・受理、命中 |
| AC-3：Grub／Spitter | 資料補完→QA の判断 | 被弾保護終了 < 命中 < ダッシュ終了 |
| AC-4：Grub／Spitter | 資料補完→QA の判断 | ダッシュ終了 < 命中 < 被弾保護終了 |
| AC-5：Grub、初回・入力不能中・回復後 | 資料補完→QA の判断 | 初回被害、各接触、入力不能の開始終了、入力受理 |
| AC-6：距離・継続・予約攻撃1回 | 資料補完→QA の判断 | 移動端点、距離、論理期限と終了フレーム、攻撃発動 |
| AC-6：クールダウン内／経過後の別試行 | 既存資料補完。回復不能なら仕様判断 | 起点・再使用可能時刻を確定してから再入力受理を確認 |
| 回帰1・2：両終了順序、各 Grub／Spitter | 資料補完→QA の判断 | 保護の遷移と両保護終了後の通常被害 |
| 回帰3：両終了順序 × Grub／Spitter | 資料補完→QA の判断 | 異なるフレームで2命中以上、元の期限、期限後の被害 |
| 回帰4：ダッシュ単独 × Grub／Spitter | 資料補完→QA の判断 | 複数命中、ダッシュ終了、解除後の被害の対応 |
| 総数・有効数・無効数・発生数 | 記録の資料補完→QA の判断 | 記録に基づいてのみ集計。不明は不明のままにする |
| モデル・記録そのものの提供不能 | 取得経路の確認。必要性が確定すれば外部入力 | Role が生成できない既存情報を明示し、Studio が escalation 要否を判断 |

各試行には、ビルド・モデル識別子と出典、試行ID、対象セル・枝、配置・向き・弾道、初期状態、予定時刻と生成時刻、フレーム・delta time・同一フレーム内順序、操作と受理、状態遷移、命中根拠、ハート前後値、移動・攻撃・クールダウン記録を含める。有効性判定と無効理由、再試行参照も保存する。

命中不成立、予定外の被害、必要順序の不成立、完全同時境界を該当枝の有効試行に数えない。無効試行も記録から消さない。30 FPS の端数に独自の許容差を設けない。必要試行数は原文を回復するまで定めない。

自動化は既存 simulator が対応する生成・記録・集計に限定する。対応機能は未確認である。QA は出典、条件と記録の対応、有効性、期待値との差を独立に読む。

### 5. 仕様判断が必要になる条件

クールダウン起点は、まず既存情報の回復で解決する。回復不能、または原資料間の矛盾が残る場合に game-designer へ次の問いを渡す。

> ダッシュ再使用までの0.6秒は、入力受理・ダッシュ開始・ダッシュ終了のどのイベントを起点とするか。継続0.25秒のダッシュを時刻tに開始した場合、開始起点ならt+0.6、終了起点ならt+0.85となるが、どの既存仕様を採用すべきか。既存仕様を回復できない場合、新規判断としてどう定義するか。

これは選択肢の差を示す論理時刻の例であり、観察値ではない。入力受理と開始が別イベントなら、その違いも出典付きで渡す。

同時イベントと入力不能中の予約は、現在の非同時境界の計画で不要なら判断を求めない。不可避と判明した場合のみ、具体的に競合するイベント、既存順序の不足、受理・被害が変わる枝を game-designer に提示する。技術側でプレイヤー向け挙動を選ばない。

### 6. リスクと証拠の限界

- 期待値を再出力した文章による循環検証を避けるため、モデルの来歴・設定・生成過程を明示する。
- フレーム依存の見落としを避けるため、30／60 FPS を分け、論理期限と観察フレームを別記する。
- 入力方式の名前だけを変えた重複資料を避けるため、モデルがキーボード／ゲームパッドの何を表現するか記載する。区別できなければ環境別観察としての限界を残す。
- 初期ハート・状態・敵配置の欠落で有効性が判断できない試行は、期待通りの結果でも充足扱いしない。
- 実機性能、実際の装置遅延、セーブ互換性の証拠は本計画から得られない。今回これらを追加要件にはしない。

### 7. Owner escalation の条件

現時点では Owner にしか提供できない入力は確定していない。モデル照会手段が packet にないことだけを理由に、Owner 計測を要求しない。

次の両方が確認された場合に、Studio が具体的な escalation を準備する。

1. runtime 管理側への確認により、必要な既存モデル・記録を Role が取得・生成できない理由が判明した。
2. QA が利用可能な文書・部分観察では必要な検証を成立させられないと判断した。

その場合は、必要な外部材料の名称・保有元・取得不能理由・影響するセルを添え、材料へのアクセス提供、または検証範囲・Goal の扱いについて判断を求める。既存モデルを捏造することは Role の資料補完ではない。実機試験や新しい simulator の開発が必要なら、dry-run の範囲を超える提案として扱う。Owner が材料を保有するとは仮定しない。

## Decisions already made

提示された要約の範囲で維持する。

- D-001：攻撃・ダッシュ・ポーズ以外の入力を追加しない。
- D-002：部分的な Owner 観察を使って元の修正 Goal を継続する。追加計測を開始条件にしない。
- D-003：発生源別保護を論理和で判定し、防いだ命中で保護を開始・延長しない。

新規仕様・アーキテクチャの採択はなく、D-004 は作成しない。

## Constraints

- 仕様・AC・全4環境・必要な命中源と枝を維持する。
- 模擬挙動の記述、生成観察、実測、期待値を区別する。
- 未提示の試行数・発生数をゼロに変換しない。
- 未取得モデル、処理順序、初期状態、既存起点を創作しない。
- 追加実装・条件別試行の実施・QA 判定・Goal 完了は本 Step に含めない。
- 未生成資料を Load に入れない。

## Open questions

1. runtime 管理側の照会窓口・手段は何か。既存モデル・記録のどの部分を取得できるか。
2. モデルは条件別の状態遷移と命中を生成できるか。入力方式とFPSをどこまで表現するか。
3. クールダウン起点とフレーム順序を既存原資料から回復できるか。
4. 原文を回復した試行要件に対し、独立 QA が採用できる証拠はどこまでか。

## Expected output

Studio は最初に取得経路と利用可能情報を確認し、出典または取得不能理由を記録する。

取得できる場合、次の作業 Role は gameplay-engineer。開始入力は、取得したモデル・記録、Handoff 11・13・15 の必要部分、対象ビルド・repo-notes の原文、本 Handoff の補完表とする。求める成果は入力充足表と、成立する枝についての具体的な資料生成要求であり、同じ不足入力でのログ生成再依頼にはしない。

取得できない場合、利用可能な仕様・AC 原文と模擬ビルド、不足一覧を QA に渡し、文書評価の範囲と証拠不足を判断してもらう。既存挙動の回復不能は game-designer、Role 外の必須入力が確定した場合は Owner escalation に分ける。

いずれの経路でも独立 Verify は未完了のままとする。

## Load

- Project: project.md#vision
- Project: project.md#constraints
- Previous handoff: goals/G-001-dash-damage/18-studio-to-technical-director.md
- Supporting handoff: goals/G-001-dash-damage/17-gameplay-engineer-to-studio.md
- Decisions: 原文の追加 Load なし。提示された要約の範囲を維持する。
- Routing note: Studio が次の受信 Role・Skill を指定し、取得済みの原資料だけを追加する。モデル資料と QA 用試行資料は現時点で未取得。
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

<<<FILE studio/templates/escalation.md
---
kind: escalation
goal: G-NNN
seq: N
from: <role-id that prepared the brief>
to: owner
status: open            # open | resolved
decision: <D-NNN once resolved>
---
# NN: Owner decision needed — <question in a few words>

<!-- Written in the project's owner_language. -->

## Question

<One sentence the Owner can answer without reading anything else.>

## Why this needs the Owner

<Which escalation trigger fires (studio/orchestration.md) and why the Studio must not decide.>

## Options

### Option A — <name>

<What it means for the game, cost, risk, reversibility.>
If chosen: <the route the Studio takes next.>

### Option B — <name>

<…>
If chosen: <…>

## Studio recommendation

<Option X.>

## Reasoning

<Why, and what evidence would change the recommendation.>

## Meanwhile

<Independent work that continues, or "Nothing; all remaining steps depend on this answer.">

## Owner decision required

<A / B — reply with the option and any conditions.>
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
