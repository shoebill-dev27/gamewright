# Studio operation packet

operation: Step
goal: G-001
role: technical-director
incoming_handoff: goals/G-001-dash-damage/18-studio-to-technical-director.md
next_seq: 19

## You may write

- goals/G-001-dash-damage/19-technical-director-to-<recipient>.md
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

<<<FILE goals/G-001-dash-damage/18-studio-to-technical-director.md
---
kind: handoff
goal: G-001
seq: 18
from: studio
to: technical-director
stage: Plan
outcome: routed
---
# 18: studio → technical-director — dry-run の検証成立性と不足入力を整理する

## Task

Handoff 17 が報告した検証入力の不足について、現在の dry-run 制約で成立する検証計画と、必要な追加入力・取得元を具体化する。既存モデルの利用可能性が確認できない場合は、その不確実性を残したまま実行可能な次の手順と阻害要因を Studio に返す。

## Context

Owner は「ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい。」と依頼した。仕様への修正と独立検証が目的であり、戦闘の方向やバランスの変更は対象外。

本作は実リポジトリのない模擬プロジェクト。Build は変更を Handoff に正確に記述することで実装と数え、runtime の simulator が `sim/` を更新する。ゲームの実行は模擬ビルド文書を読むことを意味する。

Handoff 17 は変更反映の文書照合を完了したが、条件別試行資料と既存動作情報が足りず outcome: question を返した。Studio は、同じ資料生成要求を engineering に繰り返す代わりに、検証計画の成立性を技術責任者へ戻す。

## Findings

以下は Handoff 17 の報告であり、本 Route による独立検証ではない。

- `sim/build-0.4.md` と `sim/repo-notes.md` は変更識別子 `0.3-G001-15` を明示している。Studio はこのビルド対応を採用した。ファイル名を揃えるための再生成は不要。
- 更新ビルドには期待する挙動の模擬記述があるが、環境別・試行別ログはない。全4環境への適用宣言を4件の観察に数えることはできない。
- QA 用資料 `sim/qa-G001-15.md` は存在一覧にない。未生成資料を本 Handoff の Load に入れない。
- repo-notes は、具体的な配置、実時刻・処理順序、初期ハート、有効試行総数を提供資料から復元できず、実行済み記録もないと報告されている。
- 既存クールダウン起点が特定されていない。「0.6秒を維持」という記述だけでは起点を決められない。
- Handoff 17 の「AC・回帰の資料充足」に全4環境と必要な枝の不足表、「補完する資料の変更記述」に必要情報がある。これらは未確認事項であり、QA の fail 判定ではない。

必要な検証対象として報告されているのは、AC-1〜AC-6、両保護終了順序での通常被害への復帰、複数命中による保護の延長防止、ダッシュ単独保護の解除である。対象環境は30 / 60 FPS × キーボード / ゲームパッド。命中源と枝ごとの詳細は Handoff 17 を参照する。

本 packet には simulator の既存モデルや照会手段が提示されていない。Studio はモデルの存在も不存在も確認していない。

## Decisions already made

Handoff 17 が報告した既存決定の要約：

- D-001: 攻撃・ダッシュ・ポーズ以外の入力を追加しない。
- D-002: 部分的な Owner 観察を使って元の修正 Goal を継続する。追加計測を開始条件にしない。
- D-003: 発生源別の保護を論理和で判定し、防いだ命中で保護を開始・延長しない。

今回これらの変更は求めない。Decision 原文はこの Route packet に含まれておらず、上記要約以上の解釈が必要な判断は不足入力として明示する。

## Constraints

- Desktop、キーボードとゲームパッド、30 / 60 FPS を対象とする。
- 模擬挙動の記述、生成した観察、実測、期待値を区別する。未提示の試行数・発生数をゼロに変換しない。
- 不足モデルやフレーム順序を創作してログを生成しない。既存モデルの取得元と利用可能性を確認事項として扱う。
- 仕様・AC の変更、QA の pass / fail 判定は行わない。技術上の検証方法を提案し、証拠の十分性は独立 QA の判断に残す。
- クールダウン起点や同時イベント処理など、プレイヤー向け挙動を新しく決める必要があれば game-designer へ戻す。
- Goal の再解釈や重大な範囲変更、どの Role も生成できない外部入力が必要と確定した場合は、Owner escalation が必要であると具体的な根拠を添えて返す。
- 本 Step は技術問題の整理である。ゲームの追加実装、条件別検証の実施、Goal 完了の宣言は依頼しない。

## Open questions

1. 現在の模擬ビルド文書と、従来計画の条件別試行要件はどの点で両立し、どの点で不足するか。
2. simulator の既存モデルについて、確認・取得すべき情報、取得元、担当は何か。現資料で分からない項目はどれか。
3. 既存モデルが得られる場合と得られない場合、それぞれどの検証方法を提案でき、何が未確認として残るか。
4. クールダウン起点は既存情報の回復で解決できるか。新規仕様判断が必要なら、その判断を求める具体的な問いは何か。
5. 不足は Role の作業で解消できるか、それとも Owner にしか提供できない情報・材料を必要とするか。

## Expected output

Studio 宛ての Handoff に以下をまとめる。

- 現資料から判断できることと、取得できていない入力の一覧。
- 実行可能な検証計画、または計画が成立しない具体的理由。各提案の入力、取得元、担当、証拠の限界を明示する。
- Handoff 17 の各不足項目を、資料補完・QA の判断・仕様判断・外部入力のいずれで解消するか。
- 次に必要な Role と、その Role が始められる具体的な入力。
- Owner escalation が必要な場合は、何が必要で、なぜどの Role も生成できないか。

参照原文がないため判断できない項目は、その原文と必要な節を具体的に指定する。計画を提案できれば outcome: done、必須入力や他の権限の判断で止まる場合は outcome: question とし、いずれも `to: studio` で返す。独立 Verify は完了扱いしない。

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/technical-plan.md
- Project: project.md#vision
- Project: project.md#constraints
- Decisions: 原文の追加 Load なし。本 Handoff と前 Handoff の決定要約を用い、原文が不可欠な判断は不足として返す。
- Previous handoff: goals/G-001-dash-damage/17-gameplay-engineer-to-studio.md

前 Handoff の Load に列挙されたファイルを再帰的に読み込む指示ではない。本 Step は、提供された技術問題と不足表から検証成立性を整理する。
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

<<<FILE studio/skills/technical-plan.md
---
name: technical-plan
description: Turn an approved spec (or a technical problem) into an implementation plan with affected systems, ordered tasks, risks, test strategy, and a parallelization decision.
---
# Skill: Technical plan

Typical roles: technical-director.

## When to use

The approach is non-obvious, risky, touches several systems, or could be parallelized; or a
technical problem needs diagnosis.

## Inputs

The approved spec and acceptance criteria, project constraints, the repository.

## Method

1. Map spec items to affected systems. Find what already exists and can be reused.
2. Order the tasks; mark dependencies.
3. List risks with mitigations (performance, frame-rate dependence, data compatibility, save data).
4. Define the test strategy: what is automated, what QA checks manually.
5. Decide parallelization: parallel only for code changes that are independent; give the reason
   either way. Isolated workspaces only for parallel code changes.
6. Flag anything infeasible, much costlier than the Goal implies, or irreversible.

## Output

Plan: affected systems, ordered tasks, risks and mitigations, test strategy, parallelization
decision, flags.

## Do not

Change the spec to make the plan easier — propose the change instead.
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

<<<FILE goals/G-001-dash-damage/17-gameplay-engineer-to-studio.md
---
kind: handoff
goal: G-001
seq: 17
from: gameplay-engineer
to: studio
stage: Verification input resolution
outcome: question
---
# 17: gameplay-engineer → studio — 変更反映を識別、試行資料と既存動作の不足を差し戻す

## Task

既存の `sim/build-0.4.md` を変更 `0.3-G001-15` の模擬ビルドとして採用する。独立 Verify に不足する試行資料について、simulator が利用できる既存モデルの有無を確認し、生成不能なら technical-director に検証計画の成立性を戻す。

## Context

`studio/skills/implement-change.md` を適用し、Handoff 15 の変更記述と、今回提供された実装資料・模擬ビルドを照合した。追加の実装変更やプレイヤー向け挙動は定義していない。

読んだ資料は、Handoff 16、Role・Skill、project の vision・constraints、combat、repo-notes、build-0.3、build-0.4、Handoff 11・13・15、D-001〜D-003。本作業は提供文書の照合であり、コード実行、実機計測、自動テスト、simulator による新規試行生成ではない。

変更の反映は文書上で確認できる。一方、全条件を評価する試行資料と既存クールダウン起点が不足しているため、検証入力の完成としては返せない。独立 QA の pass / fail は判定しない。

## Findings

### ビルドと変更の対応

| 資料 | 明示された識別 | Handoff 15 との対応・不一致 |
|---|---|---|
| `sim/repo-notes.md` | 表題 build 0.4、Implemented change identifier `0.3-G001-15`。現ビルドを `sim/build-0.4.md` と指定 | 発生源別状態、論理和、開始・終了の分離、共通被害入口、旧共通書き込みの除去が対応 |
| `sim/build-0.4.md` | Build identifier `0.3-G001-15` | ダッシュ全期間の保護、両終了順序、通常被弾、延長防止、維持する操作の記述が対応 |
| `sim/build-0.3.md` | build 0.3。repo-notes が旧ビルドと明記 | 修正前の比較資料。修正後の証拠には使わない |

Handoff 15 が指定した `sim/build-0.3-G001-15.md` と実在ファイル名は異なるが、識別子と相互参照は一致する。名前を合わせるための再生成は不要。

実装資料の対応箇所：

- `Player invulnerability`: 独立した保護状態、論理和、ダッシュ継続状態への接続、被弾から0.8秒の保護、各終了処理の分離、旧参照・書き込みの置換。
- `Contact and projectile damage`: Grub と Spitter の共通入口、被害適用前の判定、防いだ命中で状態・期限を変更しない処理。
- `Preserved behavior`: 距離・時間・クールダウン・予約攻撃、既存イベント順序、敵・移動等の維持。

変更記述との実装上の矛盾は本文から見つからない。ただし「既存クールダウン起点を維持」は起点そのものの特定ではない。

Handoff 15 の資料生成要求に対する不足は、QA 用の条件別試行記録がないこと。`sim/qa-G001-15.md` は存在しないと Handoff 16 が報告しており、今回の packet にも含まれない。repo-notes の `Limits of available implementation detail` は、配置、実時刻・処理順序、初期ハート、有効試行総数を復元できず、実行済み記録もないと明記している。

### QA に渡せる実在資料

| ファイル・節 | 用途 | 証拠の限界 |
|---|---|---|
| `design/combat.md` の Player kit | 仕様・期待値 | 観察ではない |
| `11-qa-to-studio.md` の「修正の受け入れ条件」「後続で実施する再現・比較手順」 | AC と有効性の基準 | 修正後の結果ではない |
| `sim/build-0.4.md` 冒頭・Dash and damage・Other controls and timing | 対象変更を識別したプレイヤー向け模擬挙動 | 全4環境への適用を文章で宣言しているが、環境別・試行別ログはない |
| `sim/build-0.3.md` | 修正前の症状比較 | 環境や発生条件の詳細はない |

build-0.4 の挙動記述は実在する模擬資料であり、単なる未生成ファイル扱いにはしない。ただし、例示時刻や「命中が成立する」という文章から、実際のフレーム順序や有効試行数を導くことはできない。

QA には仕様・期待値、模擬ビルドの記述、後続で生成される観察記録を別項目として渡す。repo-notes、D-003 の原因説明、Handoff 13・15 の実装理由、本 Handoff の Sender assessment は QA 向け観察資料に混ぜない。

### AC・回帰の資料充足

表の「有効性不足」は、該当挙動の模擬記述はあるが、計画の要求する条件別観察がない状態。「未確認」は必要な枝・詳細自体が確定していない状態。どちらも失敗判定ではない。

各セルは独立に評価する対象であり、4環境共通という宣言を4件の観察に数えない。

| 対象・必要な命中源と枝 | 30 FPS キーボード | 30 FPS ゲームパッド | 60 FPS キーボード | 60 FPS ゲームパッド | 実在する記述／不足 |
|---|---|---|---|---|---|
| AC-1 Grub／Spitter、それぞれ前半・後半 | 有効性不足 | 有効性不足 | 有効性不足 | 有効性不足 | early/late の保護記述あり。各枝の命中成立・ハート前後値・開始終了記録なし |
| AC-2 Grub／Spitter | 有効性不足 | 有効性不足 | 有効性不足 | 有効性不足 | 入力回復直後のダッシュ保護記述あり。最初の入力可能機会・受理・命中の記録なし |
| AC-3 Grub／Spitter | 有効性不足 | 有効性不足 | 有効性不足 | 有効性不足 | 0.70開始・0.85命中の例あり。実際の「被弾保護終了 < 命中 < ダッシュ終了」未確認 |
| AC-4 Grub／Spitter | 有効性不足 | 有効性不足 | 有効性不足 | 有効性不足 | 0.34開始・0.70命中の例あり。実際の逆順成立未確認 |
| AC-5 Grub、初回被害・入力不能中・回復後 | 有効性不足 | 有効性不足 | 有効性不足 | 有効性不足 | 1ハート・0.3秒・0.8秒と追加接触の記述あり。入力受理と各接触のイベント記録なし |
| AC-6 距離・継続・予約攻撃1回 | 有効性不足 | 有効性不足 | 有効性不足 | 有効性不足 | 4タイル・0.25秒・終了時1回の記述あり。移動端点・発動ログなし。30 FPS の終了フレームも未確認 |
| AC-6 クールダウン内／経過後の別試行 | 未確認 | 未確認 | 未確認 | 未確認 | 0.6秒維持の宣言のみ。既存起点、再入力受理、再使用可能時刻なし |
| 回帰1 被弾保護が先に終了、Grub／Spitter、両保護終了後の通常被害 | 有効性不足 | 有効性不足 | 有効性不足 | 有効性不足 | 1.10秒の被害例あり。前後の命中と状態遷移の記録なし |
| 回帰2 ダッシュ保護が先に終了、Grub／Spitter、両保護終了後の通常被害 | 有効性不足 | 有効性不足 | 有効性不足 | 有効性不足 | 0.95秒の被害例あり。同上 |
| 回帰3 延長なし、両終了順序 × Grub／Spitter、異なるフレームで2命中以上 | 有効性不足 | 有効性不足 | 有効性不足 | 有効性不足 | 複数命中で延長しない記述あり。各枝の命中回数・フレーム・元の期限後の被害未確認 |
| 回帰4 ダッシュのみ、Grub／Spitter、複数命中後の解除 | 有効性不足 | 有効性不足 | 有効性不足 | 有効性不足 | ダッシュ中無被害と開始0.40秒後の被害例あり。複数命中と解除を結ぶ試行記録なし |

計画の要件を満たす「観察済み」の試行セルは、この packet からは提示できない。有効・無効試行の記録もなく、総数・発生数は不明。未提示を「0回試行」や「被害0件」に変換しない。

### 補完する資料の変更記述

本 Step が定義するのは以下の資料補完要求であり、simulator の反映完了ではない。ゲーム実装、仕様、AC は変更しない。

1. `sim/build-0.4.md` は現ビルドとして維持する。時刻例を試行ログへ読み替えない。
2. simulator が利用できる既存モデルを確認する。必要なのは衝突形状・座標・速度・発射位相、実在する初期ハート、タイマー更新と移動積分・イベント順序、既存クールダウン起点。取得元を明記し、新規仕様で穴埋めしない。
3. それらが利用可能な場合、QA 用資料を生成する。生成先は既存要求の `sim/qa-G001-15.md` を候補とするが、別名でも識別子と参照が明確ならよい。本 Step では同ファイルを作成していない。
4. 上表の全セル・全枝について、Handoff 15 の設定を目標として試す。AC-1 は前半・後半、AC-2 は入力回復後の最初の機会、AC-3／4 は厳密な前後関係、AC-5 は入力不能中と回復後、AC-6 は距離・時間・攻撃とクールダウンの別試行を記録する。
5. 追加回帰は両終了順序とダッシュのみの解除を分ける。延長防止は異なるフレームで少なくとも2回の成立した命中と元の期限後の被害を対応させる。Spitter の既存2秒間隔で配置が成立しない場合、既存挙動内の配置・位相を具体化して記録し、発射頻度を変えない。成立不能ならその枝を不足として返す。

各試行に必要な観察：

- ビルド識別子、試行ID、AC／回帰、FPS、入力方式、命中源、枝。
- 部屋・全敵とプレイヤーの配置・向き、弾道と発射時刻、初期ハート、保護・入力・クールダウンの初期状態。
- 予定時刻と生成した模擬時刻を別欄にし、フレーム番号、delta time、同一フレーム内順序を記録。
- 初回被害、入力不能開始・終了、入力操作と受理、ダッシュ開始・終了、命中成立の根拠、ハート前後値。
- 論理上の期限と観察フレーム、移動端点・距離、攻撃発動回数、既存クールダウン起点と再使用可能時刻。
- 総数・有効数・無効数、有効試行での被害発生数、無効理由、再試行への参照。

命中不成立、予定外の被害、必要順序の不成立、完全同時境界は該当枝の有効試行に数えない。30 FPS の端数を独自の許容誤差で処理しない。観察を生成できない項目には、不足する入力と理由を明記する。

### 同じ要求を繰り返さないための差し戻し

repo-notes はすでに、提供資料だけでは具体的な試行を復元できないと回答している。従って、同じ packet で「詳細ログを生成せよ」とだけ再依頼しても不足は解消しない。

Studio はまず、runtime の simulator に上記の既存モデル・記録があるかを確認する。これは新たな Owner 計測を開始条件にする依頼ではない。

- **利用できる場合:** 出典付きでモデルを補い、上記の観察資料を生成する。
- **利用できない場合:** technical-director に、現在の dry-run 入力では承認済み計画の試行要件を満たせないことを戻す。利用可能な検証方法と追加入力を具体化し、必要なら QA と証拠要件を調整する。gameplay-engineer が要件を緩めない。
- **既存クールダウン起点を回復できず、新しく決める必要がある場合:** game-designer へ判断を戻す。開始起点・終了起点等で再使用可能時刻が変わるため、今回選択しない。
- **同時イベントや入力不能中の予約の判断が不可欠と判明した場合:** 競合する具体例を付けて game-designer へ戻す。現時点では境界を避ける計画のため、新規判断を要求しない。

## Decisions already made

- D-001: 攻撃・ダッシュ・ポーズ以外の入力を追加しない。
- D-002: 部分的な Owner 観察を使って元の修正 Goal を継続する。追加計測を開始条件にしない。
- D-003: 発生源別の保護を論理和で判定し、防いだ命中で保護を開始・延長しない。

## Constraints

- 模擬実装の反映、模擬ビルドの挙動記述、条件別観察、実測を区別する。
- 未生成ファイルや未確認の試行を完了扱いしない。
- 仕様・AC・計画を独断で変更しない。全4環境と必要な命中源・枝を省略しない。
- クールダウン起点、完全同時イベント、入力不能中の予約を新設しない。
- 原因説明・実装理由・自己評価は QA の観察資料から分離する。
- 独立 Verify と Goal 完了の判断は本 Step では行わない。

## Open questions

1. runtime の simulator は、repo-notes で未提供とされた既存モデルとイベント情報を利用できるか。できる場合、その出典は何か。
2. 利用できない場合、technical-director はどの追加入力・検証方法で計画を成立させるか。
3. 既存クールダウン起点は回復可能か。不可能なら、仕様判断を game-designer に戻す必要があるか。

## Expected output

Studio は build-0.4 と変更 `0.3-G001-15` の対応を採用し、ファイル名だけを理由とする再生成を終了する。

次に、simulator の利用可能な入力を確認して資料補完へ進むか、生成不能の具体的理由と本表を technical-director に渡す。観察資料が整った後に、原因説明や自己評価を除いた資料を独立 QA へ渡す。不足を残す場合は、その条件を未確認と明示し、Verify 完了として扱わない。

## Sender assessment

文書照合では、Handoff 15 の主要な変更は実装資料に反映され、模擬ビルドも同じ識別子を持つ。変更全体の未反映とみなす根拠はない。

ただし、保護されるという挙動説明だけでは、命中成立やフレーム順序を要求する計画の証拠には足りない。今回の阻害要因は実装変更の記述不足ではなく、試行生成に必要な既存情報と観察記録の不足である。文書上の整合以上の自己評価や合格判定は行っていない。

## Load

- Project: project.md#constraints
- Project: design/combat.md
- Project: sim/repo-notes.md
- Project: sim/build-0.3.md
- Project: sim/build-0.4.md
- Project: goals/G-001-dash-damage/11-qa-to-studio.md
- Project: goals/G-001-dash-damage/13-technical-director-to-studio.md
- Project: goals/G-001-dash-damage/15-gameplay-engineer-to-studio.md
- Decisions: decisions/D-001-one-button-combat.md
- Decisions: decisions/D-002-resume-with-owner-observations.md
- Decisions: decisions/D-003-independent-invulnerability.md
- Previous handoff: goals/G-001-dash-damage/16-studio-to-gameplay-engineer.md
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
